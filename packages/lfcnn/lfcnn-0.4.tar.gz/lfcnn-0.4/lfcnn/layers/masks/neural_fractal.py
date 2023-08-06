# Copyright (C) 2021  The LFCNN Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Neural fractal coding mask.
"""

import math
from typing import Optional

import tensorflow as tf
from tensorflow import nn
from tensorflow.keras.initializers import Initializer

from .abstracts import AbstractMaskLayer


class NeuralFractal(AbstractMaskLayer):

    def __init__(self,
                 pattern_shape,
                 inv_temp: float = 5.0,
                 hard_forward: bool = False,
                 lambda_e: Optional[float] = None,
                 lambda_s: Optional[float] = None,
                 regular: bool = False,
                 initializer: str = 'truncated_normal',
                 compress: Optional[str] = None,
                 *args, **kwargs):
        """A keras.Layer implementing a neural fractal coding mask.

        Args:
            pattern_shape: Spatial shape (m, n) of the pattern

            inv_temp: Temperature applied to softmax in pattern generation.
                      Higher temperature yields a spikier mask.
                      Only important during training as mask is binarized
                      for inference.

            hard_forward: Whether to use binarization in the forward pass.
                          The backwards call is still perfomed with the
                          temperature softmax.

            lambda_e: Entropy regularization strength.

            lambda_s: Symmetry regularization strength

            regular: Whether to reduce the pattern to exactly regular ones.

            initializer: Either "truncated_normal" or "own".

            compress: Specify, whether and how a spectral projection is performed
                      after applying the mask. Defaults to "full", reducing
                      the spectral axis via summation.

            *args: Passed to keras.Layer init()

            **kwargs: Passed to keras.Layer init()
        """
        super(NeuralFractal, self).__init__(*args, **kwargs)
        self._pattern_shape = pattern_shape
        self._inv_temp = self.add_weight(name='inv_temp',
                                         shape=(),
                                         initializer=tf.keras.initializers.Constant(inv_temp),
                                         trainable=False)
        self._hard_forward = hard_forward
        self._initializer = initializer
        self._compress = compress
        if compress not in [None, "full", "own", "own_repeat"]:
            raise ValueError(f"Unknown compress option {compress}.")

        if lambda_e is not None:
            self._lambda_e = self.add_weight(name='lambda_e',
                                             shape=(),
                                             initializer=tf.keras.initializers.Constant(lambda_e),
                                             trainable=False)
        else:
            self._lambda_e = None

        if lambda_s is not None:
            self._lambda_s = self.add_weight(name='lambda_e',
                                             shape=(),
                                             initializer=tf.keras.initializers.Constant(lambda_s),
                                             trainable=False)
        else:
            self._lambda_s = None
        self._regular = regular
        self._pattern_weights = None
        self._root = None
        self._depth = None
        self._needs_crop = None
        self._crop_kwargs = None
        self._num_ch = None

        if self._regular and self._lambda_s is not None:
            raise ValueError("Using a regular pattern together with a symmetry regularizer does not make sense. "
                             "Either specify _regular=False or _lambda_s=None.")
        return

    def get_mask(self):
        mask = self.generate_fractal(binarize=True)
        return mask.numpy()

    def get_mask_weights(self):
        mask = self.generate_fractal(binarize=False)
        return mask.numpy()

    @property
    def inv_temp(self):
        return self._inv_temp

    def set_inv_temp(self, value: float):
        self._inv_temp.assign(value)

    @property
    def lambda_e(self):
        return self._lambda_e

    def set_lambda_e(self, value: float):
        if self.lambda_e is None:
            raise ValueError("Cannot set previously undefined regularizer. Initialize layer with regularizer.")
        self._lambda_e.assign(value)

    @property
    def lambda_s(self):
        return self._lambda_s

    def set_lambda_s(self, value: float):
        if self._lambda_s is None:
            raise ValueError("Cannot set previously undefined regularizer. Initialize layer with regularizer.")
        self._lambda_s.assign(value)

    def build(self, input_shape):

        _, u, v, s, t, ch = input_shape
        m, n = self._pattern_shape
        self._num_ch = ch

        # Calculate mask size and _depth needed to generate the fractal
        d_s, d_t = math.ceil(math.log(s, m)), math.ceil(math.log(t, n))
        self._depth = max(d_s, d_t)

        # Calculate whether a crop of the generated fractal is needed to fit the input
        s_gen, t_gen = m**self._depth, n**self._depth
        offset_s, offset_t = (s_gen - s)//2, (t_gen - t)//2
        if offset_s > 0 or offset_t > 0:
            self._needs_crop = True
            self._crop_kwargs = dict(offset_height=offset_s, offset_width=offset_t,
                                     target_height=s, target_width=t)

        # Initialize pattern weights
        if self._regular:
            shape = (m, n, 1, input_shape[-1])
        else:
            shape = (m, n, input_shape[-1], input_shape[-1])

        # Create _root of shape (1, 1, ch) with first element 1.
        self._root = tf.expand_dims(tf.one_hot([0], input_shape[-1]), axis=0)

        # Create pattern as trainable weights
        if self._initializer == "truncated_normal":
            initializer = tf.keras.initializers.TruncatedNormal(mean=0.0, stddev=0.1)
        elif self._initializer == "own":
            initializer = MaskInitializer()
        else:
            raise ValueError(f"Unkown initializer type {self._initializer}")

        self._pattern_weights = self.add_weight(name='mask_weights',
                                                shape=shape,
                                                initializer=initializer,
                                                trainable=True)

        return

    def call(self, input, training=None, binarize=None):

        # During training, do not binarize pattern if not explicitly specified
        if training and binarize is None:
            binarize = False
        if not training and binarize is None:
            binarize = True

        mask = self.generate_fractal(binarize=binarize)

        # Add regularization losses
        if self._lambda_e is not None:
            if not binarize:
                entropy_loss = self.entropy_loss(self._pattern_weights)
            else:
                # For inference, pattern is binarized
                entropy_loss = 0.0
            if self.trainable:
                self.add_loss(self._lambda_e.read_value()*entropy_loss)
            self.add_metric(entropy_loss, name="mask_entropy_loss")
            self.add_metric(self._lambda_e, name="mask_entropy_reg_strength")

        if self._lambda_s is not None:
            symmetry_loss = self.symmetry_loss(self._pattern_weights)
            self.add_loss(self._lambda_s.read_value()*symmetry_loss)
            self.add_metric(symmetry_loss, name="mask_symmetry_loss")
            self.add_metric(self._lambda_s, name="mask_symmetry_reg_strength")

        if training:
            self.add_metric(self._inv_temp, name="mask_inv_temp")
            if self._roll:
                mask = self.roll(mask, max_amount=max(self._pattern_shape), axis=(0, 1))

        # Apply mask to input
        output = tf.multiply(input, mask)

        if self._compress is not None:
            if self._compress == "full":
                output = tf.reduce_sum(output, axis=-1, keepdims=True)

            elif self._compress == "own":
                # Reduce coded output in gradients
                output = tf.reduce_sum(output, axis=-1, keepdims=True) + \
                         tf.stop_gradient(output - tf.reduce_sum(output, axis=-1, keepdims=True))

            elif self._compress == "own_repeat":
                # Reduce coded output in gradients
                output = tf.reduce_sum(output, axis=-1, keepdims=True)
                output = tf.repeat(output, self._num_ch, axis=-1)
                output = tf.multiply(output, tf.stop_gradient(mask))

        return output

    def hard_pattern(self):
        """Use argmax in channel axis to binarize pattern"""
        # return tf.math.round(nn.softmax(1e6*self._pattern_weights, axis=-1))  # numerically unstable
        return tf.one_hot(tf.argmax(self._pattern_weights, axis=-1), depth=self._num_ch, axis=-1)

    def soft_pattern(self):
        """Use temperature softmax as a diff'able approximation of argmax."""
        return nn.softmax(self._inv_temp.read_value()*self._pattern_weights, axis=-1)

    def get_pattern(self, binarize):
        """Generate the pattern from the internal pattern weights.
        Basically, this just applies the softmax along the channel axis.

        Args:
            binarize: Whether to binarize the pattern.

        Returns:
            pattern.
        """
        if binarize:
            return self.hard_pattern()
        else:
            if self._hard_forward:
                # Use hard/binary pattern in farward pass, soft pattern in backwards pass
                return self.soft_pattern() + tf.stop_gradient(self.hard_pattern() - self.soft_pattern())
            else:
                # Use simple temperature softmax for forward and backward pass
                return self.soft_pattern()

    def apply_pattern(self, state, binarize=False):
        pattern = self.get_pattern(binarize=binarize)
        if self._regular:
            state = tf.reduce_sum(state, axis=-1, keepdims=True)
        state = tf.einsum("i j k, a b k l -> i a j b l", state, pattern)
        a, b, c, d, e = state.shape
        state = tf.reshape(state, (a*b, c*d, e))
        return state

    def generate_fractal(self, binarize=False):
        state = self._root
        # Apply recursion to generate the fractal from the pattern
        for _ in range(self._depth):
            state = self.apply_pattern(state, binarize=binarize)

        # Crop generated fractal to fit target size
        if self._needs_crop:
            state = tf.image.crop_to_bounding_box(state, **self._crop_kwargs)
        return state

    @staticmethod
    def entropy_loss(pattern):
        # MINIMIZE entropy along last axis to regularize one-hot mask
        return -tf.reduce_mean(tf.reduce_sum(nn.softmax(pattern, axis=-1)*nn.log_softmax(pattern, axis=-1), axis=-1))

    @staticmethod
    def symmetry_loss(pattern):
        # MAXIMIZE entropy along second to last axis to regularize mask symmetry
        return tf.reduce_mean(tf.reduce_sum(nn.softmax(pattern, axis=-2)*nn.log_softmax(pattern, axis=-2), axis=-2))

    def get_config(self):
        lambda_e = None if self._lambda_e is None else float(self._lambda_e)
        lambda_s = None if self._lambda_s is None else float(self._lambda_s)
        config = dict(
            pattern_shape=self._pattern_shape,
            inv_temp=self._inv_temp,
            hard_forward=self._hard_forward,
            lambda_e=lambda_e,
            lambda_s=lambda_s,
            regular=self._regular,
            initializer=self._initializer)
        return config


class MaskInitializer(Initializer):

    def __init__(self, *args, **kwargs):
        super(MaskInitializer, self).__init__(*args, **kwargs)

    def __call__(self, shape, dtype=None, **kwargs):
        s, t, ch, _ = shape
        # random_pattern = tf.random.normal(shape[:-1], mean=0, stddev=0.01)
        # random_pattern = tf.random.uniform(shape[:-1], minval=-0.1, maxval=0.1)

        # Draw 10k random patterns
        random_pattern = tf.random.uniform((s, t, 10000*ch), minval=-0.05, maxval=0.05)
        # Select those, with the lowest standard deviation in the (s, t) domain
        stds = tf.math.reduce_std(random_pattern, axis=(0, 1))
        topk = tf.math.top_k(-stds, ch)
        random_pattern = tf.gather(random_pattern, topk.indices, axis=-1)
        # Make them mean-free
        random_pattern -= tf.math.reduce_mean(random_pattern, axis=(0, 1))
        # Tile pattern to create a regular mask
        pattern = tf.repeat(tf.expand_dims(random_pattern, axis=-1), ch, axis=-1)
        pattern = tf.transpose(pattern, (0, 1, 3, 2))
        # Add noise to distort regularity
        pattern += tf.random.uniform(pattern.shape, -0.005, 0.005)
        return pattern
