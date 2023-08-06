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

"""
A keras.Model subclass implementing the GradNorm [1] training strategy
for adaptive multi-task loss weighting.

[1]: Chen, Zhao, et al.
"Gradnorm: Gradient normalization for adaptive loss balancing in deep
multitask networks."
International Conference on Machine Learning. 2018.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.initializers import Constant

from lfcnn.training.utils.constraints import MinVal


class GradNorm(keras.Model):

    def __init__(self,
                 alpha: float = 1.0,
                 layers_name="last_shared",
                 min_val=1e-7,
                 **kwargs):
        """A Model subclass for adaptive loss weighting via GradNorm [1].

        In the created model, there needs to be one or more layers with names
        containing the string "last_shared". The trainable variables of these
        layers will be used to calculate the gradients of the individual
        loss terms. As suggested in the original paper, usually the last layer
        that is shared by all tasks is used.
        If you want to specify more shared layers, e.g. for residual layers,
        you can specify multiple names starting with "last_shared".

        Currently, this implementation *does not* support distributed
        strategies via tf.distribute.Strategy such as multi-GPU training.

        [1]: Chen, Zhao, et al.
        "Gradnorm: Gradient normalization for adaptive loss balancing in deep
        multitask networks."
        International Conference on Machine Learning. 2018.

        Args:
            alpha: Symmetry factor as specified in original paper [1].

            layers_name: Name of the layers used for gradient norm calculation.
                         By default, uses the last shared layers indicated by
                         "last_shared" layer names. Otherwise, pass string
                         that is contained in all layers you want to use, e.g.
                         "shared".

            min_val: Minimum value to clip the loss weights with to avoid
                     weights to become zero.

            **kwargs: kwargs passed to keras.Model init.
        """

        super(GradNorm, self).__init__(**kwargs)
        self.alpha = float(alpha)
        self.layers_name = layers_name
        self.min_val = float(min_val)
        self.shared_vars = None
        self.main_loss_vars = None
        self.loss_weights = None
        self.initial_losses = None

    def compile(self, **kwargs):
        """Overwrite keras.Model compile()."""

        if "loss_weights" in kwargs and kwargs["loss_weights"] is not None:
                print("WARNING: Not possible to specify loss weights explicitly "
                      "when using GradNorm model."
                      "Loss weights are adaptive. "
                      "Ignoring speciefied loss weights.")

        # Remove loss_weights kwarg (is set to None by default) and compile
        kwargs.pop("loss_weights", None)
        super(GradNorm, self).compile(**kwargs)

        # Set loss weights as trainable variables of the Model
        # Initialize loss weights, s.t. SUM_i w_i = 1, i = 1, ..., N
        # Constrain weights min_val < w_i
        # Weights are normalized to sum-to-one after gradient update
        num_outputs = len(self.output_names)
        num_outputs_inv = 1.0 / num_outputs

        weight_kwargs = dict(shape=(),
                             initializer=Constant(num_outputs_inv),
                             trainable=True,
                             constraint=MinVal(self.min_val))
        self.loss_weights = [self.add_weight(name='loss_weight_' + name, **weight_kwargs)
                             for name in self.output_names]

        # Compile again with loss weights
        super(GradNorm, self).compile(loss_weights=self.loss_weights, **kwargs)

        # Get trainable variables of last shared layer
        self.shared_vars = [vars for vars in self.trainable_variables
                            if self.layers_name in vars.name]
        if len(self.shared_vars) == 0:
            raise ValueError(f"No '{self.layers_name}' variables found. "
                             "Either, there are no layers with names containing "
                             f"'{self.layers_name}' or the specified layers does not "
                             "contain any trainable variables.")

        # Get all trainable variables, excluding loss weights
        self.main_loss_vars = [var for var in self.trainable_variables
                               if "loss_weight" not in var.name]

    def set_weights(self, weights):
        """Set the weights for GradNorm Model. Since the loss weights are
        added as trainable weights, they have to first be detached from the
        given weights.
        """
        try:
            # If no loss weights have been added, simply call super method
            super(GradNorm, self).set_weights(weights)
        except ValueError:
            # Exclude last N elements (loss weights have been added last)
            num_outputs = len(self.output_names)
            super(GradNorm, self).set_weights(weights[:-num_outputs])

    def train_step(self, data):
        """Overwrite keras.Model train_step() which is called in fit()."""

        # Unpack the data passed to fit()
        # x is input tensor, y is label dictionary
        x, y = data

        # First, calculate main loss gradients w.r.t. to total variables
        # and single task loss gradients w.r.t. to last shared variables
        with tf.GradientTape(persistent=True, watch_accessed_variables=False) as tape:
            # Do not watch loss_weights as variables
            tape.watch(self.main_loss_vars)
            tape.watch(self.shared_vars)

            # Forward pass prediction
            y_pred = self(x, training=True)

            # Compute the overall loss as passed to compile()
            total_loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

            # Calculate UNWEIGHTED single task loss values
            # This specifically needs to be called after compiled_loss
            # has been called once and hence is built
            single_task_loss_vals = [
                loss_fn(y[output], y_pred[output_num]) for
                output_num, (loss_fn, output) in enumerate(zip(self.compiled_loss._losses, self.output_names))
            ]

        # Compute main loss gradients
        total_gradients = tape.gradient(total_loss, self.main_loss_vars)

        # Compute UNWEIGHTED single task gradients
        single_task_gradients = [tape.gradient(loss, self.shared_vars) for loss in single_task_loss_vals]

        # Release gradient tape
        del tape

        # Calculate the UNWEIGHTED gradient norms. The single task gradients
        # themselves might be lists, e.g. for layer kernel and bias.
        # Hence, they are flattened and concatinated first.
        single_task_gradient_norms = [
            tf.norm(tf.concat([tf.reshape(vec, [-1]) for vec in grad], axis=0))
            for grad in single_task_gradients
        ]

        # Calculate WEIGHTED norms, this correspond to G_i[t] as in the paper
        # Since w_i > 0: || d/dW (w_i * L_i) || = w_i * || d/dW L_i ||
        weighted_single_task_gradient_norms = [
            tf.multiply(weight, gradient_norm)
            for weight, gradient_norm in zip(self.loss_weights, single_task_gradient_norms)
        ]

        # Calculate mean of all weighted gradient norms
        mean_weighted_gradient_norm = tf.reduce_mean(tf.stack(weighted_single_task_gradient_norms, axis=0))

        # For first step, set initial loss values from current values
        if self.initial_losses is None:
            self.initial_losses = [
                tf.Variable(loss, trainable=False, name="init_loss_"+str(i))
                for i, loss in enumerate(single_task_loss_vals)
            ]

        # Calculate loss gains \tilde{L}_i[t] = L_i[t] / L_i[0]
        single_task_loss_gains = [
            tf.math.divide(loss, initial_loss)
            for loss, initial_loss in zip(single_task_loss_vals, self.initial_losses)
        ]

        # Calculate mean loss gain
        mean_loss_gain = tf.reduce_mean(tf.stack(single_task_loss_gains, axis=0))

        # Calculate relative inverse training rate
        # r_i[t] = \tilde{L}_i[t] / (1/N sum_i \tilde{L}_i[t])
        single_task_training_rates = [loss_gain / mean_loss_gain for loss_gain in single_task_loss_gains]

        # Calculate gradients for loss weights
        with tf.GradientTape(persistent=False, watch_accessed_variables=False) as tape:
            # Only watch loss weights
            tape.watch(self.loss_weights)

            # Calculate loss_weights loss term as specified in the paper [1]
            # L_grad = sum_i | w_i*g_i - mean(w_i*g_i)*r_i**alpha |
            # where the mean and r_i is considered fixed w.r.t. to w_i differentiation
            # Differing from the paper, g_i here denotes the UNWEIGHTED gradient norms
            loss_weight_loss = tf.reduce_sum(tf.norm(
                [weight*grad_norm - mean_weighted_gradient_norm*(train_rate**self.alpha)
                 for grad_norm, weight, train_rate in zip(single_task_gradient_norms, self.loss_weights, single_task_training_rates)],
                ord=1))

        # Calculate gradient w.r.t. loss weights
        loss_weight_gradients = tape.gradient(loss_weight_loss, self.loss_weights)

        # Update layer weights
        self.optimizer.apply_gradients(zip(total_gradients, self.main_loss_vars))

        # Update loss weights
        self.optimizer.apply_gradients(zip(loss_weight_gradients, self.loss_weights))

        # Normalize updated weights to sum_i w_i = 1
        weights_sum = tf.reduce_sum(self.loss_weights)
        for i, weight in enumerate(self.loss_weights):
            self.loss_weights[i].assign(tf.maximum(weight / weights_sum, self.min_val))

        # Update metrics (includes the metric that tracks the loss)
        self.compiled_metrics.update_state(y, y_pred)

        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}
