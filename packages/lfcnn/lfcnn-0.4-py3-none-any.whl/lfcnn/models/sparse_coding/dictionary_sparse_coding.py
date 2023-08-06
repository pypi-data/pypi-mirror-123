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


"""Light field sparse coding using online dictionary learning.
"""
from typing import List

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Permute
from tensorflow.keras.layers import Reshape


from lfcnn.models import BaseModel
from lfcnn.generators import LfGenerator
from lfcnn.generators.reshapes import lf_identity
from lfcnn.training.utils.initializer import NormalizedTruncatedNormal

from .utils.patching import Patch
from .utils.patching import DePatch
from .utils.patching import DePatchEfficient
from .utils.sparse_coding import sparse_code_fista
from .utils.sparse_tensor_coding import sparse_tensor_code_fista


class SparseCodingLayer(keras.layers.Layer):

    def __init__(self,
                 overcompleteness,
                 use_mask,
                 couple_strength,
                 iterations_fista,
                 iterations_eigenval,
                 measure_sparsity,
                 *args, **kwargs):
        """A keras.Layer implementing FISTA-based sparse coding.
        Can be used to train a sparse dictionary using a training dataset
        (online dictionary learning).
        But also to use a pre-trained dictionary to reconstruct coded
        measurements (compressed sensing).

        Input of the layer is assumed to be a batch of light field patches,
        i.e. of shape (b, N, u', v', s', t', ch).

        Args:
            overcompleteness: Dictionary overcompleteness. The dictionary
                              will be of shape (N, overcompleteness*N).

            use_mask: Whether to use a coding mask. Used for Compressed Sensing
                      reconstruction of coded input.

            couple_strength: Coupling of the L1-norm term during FISTA sparse coding.

            iterations_fista: Iterations of the FISTA main loop.

            iterations_eigenval: Iterations of the von Mises eigenvalue
                                 approximation routine.

            measure_sparsity: Whether to measure sparsity of coded signal and
                              log it as a metric. This may be very memory
                              consuming when working with very large
                              input batches.

            *args, **kwargs: Passed to keras.Layer instantiation.
        """
        super(SparseCodingLayer, self).__init__(*args, **kwargs)
        self.overcompleteness = overcompleteness
        self.couple_strength = couple_strength
        self.use_mask = use_mask
        self.iter_fista = iterations_fista
        self.iter_eigenval = iterations_eigenval
        self.measure_sparsity = measure_sparsity
        self.dictionary = None

    def build(self, input_shape):

        # Calculate signal dimensions (exclude batch axis)
        _, N, u, v, s, t, ch = input_shape
        dim_signal = u*v*s*t*ch
        dim_dict = int(self.overcompleteness*dim_signal)

        # Initialize dictionary shape  (N x overcompleteness*N)
        # Dictionary atoms are normalized to unit norm.
        weight_kwargs = dict(shape=(dim_signal, dim_dict),
                             initializer=NormalizedTruncatedNormal(axis=0),
                             trainable=True,
                             constraint=keras.constraints.UnitNorm(axis=0))
        # Add dictionary as layer weights
        self.dictionary = self.add_weight(name='dictionary', **weight_kwargs)

    def call(self, input):

        _, N, u, v, s, t, ch = input.shape

        # Flatten (b, N, u', v', s', t', ch) -> (b, N, u' * v' * s' * t' * ch)
        x = Reshape((N, u*v*s*t*ch))(input)

        # Sparse coding, shape (b * N, overcomplete * u' * v' * s' * t' * ch)
        # Do not backprop gradient here
        x = tf.stop_gradient(
            sparse_code_fista(x,
                              self.dictionary,
                              use_mask=self.use_mask,
                              couple_strength=self.couple_strength,
                              iterations=self.iter_fista,
                              iterations_eigenval=self.iter_eigenval)
        )
        if self.measure_sparsity:
            # Measure Sparsity of sparse coded representation
            m = tf.stop_gradient(tf.abs(x) < 0.001)
            sparsity = tf.stop_gradient(tf.reduce_sum(tf.cast(m, tf.int32)) / tf.size(m))
            self.add_metric(sparsity, aggregation='mean', name="sparsity")

        # Decode using dictionary , shape (b, N, u' * v' * s' * t' * ch)
        x = tf.matmul(x, self.dictionary, transpose_b=True)

        # Reshape back to (b, N, u', v', s', t', ch)
        x = Reshape((N, u, v, s, t, ch))(x)
        return x


class TensorDecompositionLayer(keras.layers.Layer):

    def __init__(self,
                 overcompleteness,
                 use_mask,
                 couple_strength,
                 iterations_fista,
                 iterations_eigenval,
                 measure_sparsity,
                 *args, **kwargs):
        """A keras.Layer implementing FISTA-based sparse coding using
        Tucker tensor decomposition.
        Can be used to train a sparse dictionary using a training dataset
        (online dictionary learning).
        But also to use a pre-trained dictionary to reconstruct coded
        measurements (compressed sensing).

        Decomposition is performed to separate the angular, spatial, and
        spectral component of the input light field.

        Args:
            overcompleteness: Dictionary overcompleteness. The dictionary
                              will be of shape (N, overcompleteness*N).

            use_mask: Whether to use a coding mask. Used for Compressed Sensing
                      reconstruction of coded input.

            couple_strength: Coupling of the L1-norm term during FISTA sparse coding.

            iterations_fista: Iterations of the FISTA main loop.

            iterations_eigenval: Iterations of the von Mises eigenvalue
                                 approximation routine.

            measure_sparsity: Whether to measure sparsity of coded signal and
                              log it as a metric. This may be very memory
                              consuming when working with very large
                              input batches.

            *args, **kwargs: Passed to keras.Layer instantiation.
        """
        super(TensorDecompositionLayer, self).__init__(*args, **kwargs)
        self.overcompleteness = overcompleteness
        self.couple_strength = couple_strength
        self.use_mask = use_mask
        self.iter_fista = iterations_fista
        self.iter_eigenval = iterations_eigenval
        self.measure_sparsity = measure_sparsity
        self.dictionary_angular = None
        self.dictionary_spatial = None
        self.dictionary_spectral = None

    def build(self, input_shape):
        # Input shape (b, N, u', v', s', t', ch)
        _, N, u, v, s, t, ch = input_shape
        dim_angular = input_shape[2]*input_shape[3]
        dim_spatial = input_shape[4]*input_shape[5]
        dim_spectral = input_shape[6]

        num_angular = int(self.overcompleteness*dim_angular)
        num_spatial = int(self.overcompleteness*dim_spatial)
        num_spectral = int(self.overcompleteness*dim_spectral)

        # Initialize dictionaries
        # Dictionary atoms are normalized to unit norm.
        weight_kwargs = dict(initializer=NormalizedTruncatedNormal(axis=0),
                             trainable=True,
                             constraint=keras.constraints.MinMaxNorm(min_value=0.95, max_value=1.05, rate=0.95, axis=0))

        self.dictionary_angular = self.add_weight(name='dictionary_angular',
                                                  shape=(num_angular, u, v),
                                                  **weight_kwargs)

        self.dictionary_spatial = self.add_weight(name='dictionary_spatial',
                                                  shape=(num_spatial, s, t),
                                                  **weight_kwargs)

        self.dictionary_spectral = self.add_weight(name='dictionary_spectral',
                                                   shape=(num_spectral, ch),
                                                   **weight_kwargs)

    def call(self, input):

        _, N, u, v, s, t, ch = input.shape

        # Code light field (b, N, u, v, s, t, ch) -> (b, N, N_uv, N_st, N_ch)
        x = tf.stop_gradient(
            sparse_tensor_code_fista(input,
                                     self.dictionary_angular,
                                     self.dictionary_spatial,
                                     self.dictionary_spectral,
                                     use_mask=self.use_mask,
                                     couple_strength=self.couple_strength,
                                     iterations=self.iter_fista,
                                     iterations_eigenval=self.iter_eigenval)
        )
        if self.measure_sparsity:
            # Measure Sparsity of sparse coded representation
            m = tf.stop_gradient(tf.abs(x) < 0.001)
            sparsity = tf.stop_gradient(tf.reduce_sum(tf.cast(m, tf.int32)) / tf.size(m))
            self.add_metric(sparsity, aggregation='mean', name="sparsity")

        # (b, N, N_uv, N_st, N_ch) -> (b, N, N_uv, N_st, ch)
        x = tf.tensordot(x, self.dictionary_spectral, axes=[[4], [0]])
        # (b, N, N_uv, N_st, ch) -> (b, N, N_uv, s', t', ch)
        x = tf.tensordot(x, self.dictionary_spatial, axes=[[3], [0]])
        # (b, N, N_uv, s', t', ch) -> (b, N, u', v', s', t', ch)
        x = tf.tensordot(x, self.dictionary_angular, axes=[[2], [0]])
        x = Permute((1, 5, 6, 3, 4, 2))(x)

        return x


class DictionarySparseCoding(BaseModel):

    def __init__(self,
                 overcompleteness,
                 use_mask=False,
                 patch_size_st=(8, 8),
                 patch_size_uv=(5, 5),
                 patch_step_st=(4, 4),
                 patch_step_uv=(4, 4),
                 couple_strength=1e-5,
                 iterations_fista=20,
                 iterations_eigenval=100,
                 efficient_depatch=False,
                 measure_sparsity=True,
                 decomposition='sparse_coding',
                 **kwargs):
        """A lfcnn.BaseModel implementing FISTA-based sparse coding.
        Can be used to train a sparse dictionary using a training dataset
        (online dictionary learning).
        But also to use a pre-trained dictionary to reconstruct coded
        measurements (compressed sensing).

        Since light fields are usually too large for full dictionary representation
        and compressed sensing, the input light field batch is patched
        in the angular and spatial domain. The coding/reconstruction is then
        performed on the patches. The full light fields are then recovered
        from the patches using a de-patch layer.

        E.g. a light field batch of shape (b, 9, 9, 32, 32, ch)
        can be patched to (b*N_patches, 5, 5, 8, 8, ch) using

        patch_size_st = [8, 8]
        (with 50% spatial overlap)
        patch_step_st = [p - p//2 for p in patch_size_st]
        patch_size_uv = [5, 5]
        patch_step_uv = [4, 4]
        (since 2 * (5, 5) with (1, 1) overlap -> (9, 9) )

        See Also:
            :func:`lfcnn.models.sparse_coding.utils.sparse_coding.sparse_code_fista`
            and
            :func:`lfcnn.models.sparse_coding.utils.patching.patch`
            and
            :func:`lfcnn.models.sparse_coding.utils.patching.depatch`

        Args:
            overcompleteness: Dictionary overcompleteness. The dictionary
                              will be of shape (N, overcompleteness*N).
                              Here, N denotes the vectorized signal dimension
                              after patching.

            use_mask: Whether to use a coding mask. Used for Compressed Sensing
                      reconstruction of coded input.

            patch_size_st: Spatial patch size (s', t')

            patch_size_uv: Angular patch size (u', v')

            patch_step_st: Spatial patch step (s_s, s_t)

            patch_step_uv: Angular patch step (s_u, s_v)

            couple_strength: Coupling of the L1-norm term during FISTA sparse coding.

            iterations_fista: Iterations of the FISTA main loop.

            iterations_eigenval: Iterations of the von Mises eigenvalue
                                 approximation routine.

            efficient_depatch: Whether to use a more memory efficient depatch
                               implementation. Cannot be used during training.
                               Is only meant for depatching very large batches.

            measure_sparsity: Whether to measure sparsity of coded signal and
                              log it as a metric. This may be very memory
                              consuming when working with very large
                              input batches.

            **kwargs: Passed to model instantiation.

        """

        super(DictionarySparseCoding, self).__init__(**kwargs)
        self.overcompleteness = overcompleteness
        self.use_mask = use_mask
        self.patch_size_st = patch_size_st
        self.patch_size_uv = patch_size_uv
        self.patch_step_st = patch_step_st
        self.patch_step_uv = patch_step_uv

        self.couple_strength = couple_strength
        self.iterations_fista = iterations_fista
        self.iterations_eigenval = iterations_eigenval
        self.efficient_depatch = efficient_depatch
        self.measure_sparsity = measure_sparsity

        self.decomposition = decomposition

    def set_generator_and_reshape(self):
        self._generator = LfGenerator
        self._reshape_func = lf_identity
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:

        # Single input model
        x = inputs[0]
        original_shape = inputs[0].shape[1:]
        ch = x.shape[-1]

        # Patch light fields
        # (b, u, v, s, t, ch) -> (b, N, u', v', s', t', ch)
        patch_layer = Patch(name='patch_light_field',
                            patch_size_st=self.patch_size_st,
                            patch_size_uv=self.patch_size_uv,
                            patch_step_st=self.patch_step_st,
                            patch_step_uv=self.patch_step_uv)
        x = patch_layer(x)

        # Sparse code light field
        coding_kwargs = dict(overcompleteness=self.overcompleteness,
                             use_mask=self.use_mask,
                             couple_strength=self.couple_strength,
                             iterations_fista=self.iterations_fista,
                             iterations_eigenval=self.iterations_eigenval,
                             measure_sparsity=self.measure_sparsity)
        if self.decomposition == "sparse_coding":
            coding_layer = SparseCodingLayer(**coding_kwargs)
        elif self.decomposition == 'tensor_decomposition':
            coding_layer = TensorDecompositionLayer(**coding_kwargs)
        else:
            raise ValueError(f"Unknown decomposition type '{self.decomposition}'")
        x = coding_layer(x)

        # De-patch light fields
        depatch_kwags = dict(name='light_field',
                             original_shape=original_shape,
                             patch_size_st=patch_layer.patch_size_st,
                             patch_step_st=patch_layer.patch_step_st,
                             num_patches_st=patch_layer.num_patches_st,
                             patch_size_uv=patch_layer.patch_size_uv,
                             patch_step_uv=patch_layer.patch_step_uv,
                             num_patches_uv=patch_layer.num_patches_uv)

        if self.efficient_depatch:
            depatch_layer = DePatchEfficient(**depatch_kwags)
        else:
            depatch_layer = DePatch(**depatch_kwags)

        x = depatch_layer(x)

        return keras.Model(inputs, x, name="DictionarySparseCoding")
