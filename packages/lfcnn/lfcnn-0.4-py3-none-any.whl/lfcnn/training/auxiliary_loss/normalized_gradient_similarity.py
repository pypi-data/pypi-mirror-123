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
A keras.Model subclass implementing the Normalized Gradient Similarity [1]
training strategy for adaptive auxiliary loss weighting.

[1]: M. Schambach, J. Shi, and M. Heizmann:
"Spectral Reconstruction and Disparity from Spatio-Spectrally Coded Light Fields via Multi-Task Deep Learning"
International Conference on 3D Vision (3DV), 2021.
"""
import random
from typing import Dict, List, Optional, Union

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.constraints import NonNeg
from tensorflow.keras.initializers import Constant
from tensorflow.python.ops import math_ops
from tensorflow.python.keras.utils import losses_utils

from lfcnn.training.utils.aux_losses_container import AuxLossesContainer
from lfcnn.training.utils.regularizers import Log
from lfcnn.training.utils.constraints import MinVal
from lfcnn.losses import get as get_loss


class NormalizedGradientSimilarity(keras.Model):

    def __init__(self,
                 aux_losses: Dict[str, List[Union[str, keras.losses.Loss]]],
                 gradient_approximation: Optional[str] = None,
                 approximation_percentage: Optional[float] = None,
                 multi_task_uncertainty: bool = False,
                 weights_init: Optional[Dict[str, float]] = None,
                 **kwargs):
        """A keras.Model subclass implementing the Normalized Gradient Similarity [1]
        training strategy for adaptive auxiliary loss weighting.

        [1]: M. Schambach, J. Shi, and M. Heizmann:
        "Spectral Reconstruction and Disparity from Spatio-Spectrally Coded Light Fields via Multi-Task Deep Learning"
        International Conference on 3D Vision (3DV), 2021.

        Args:
            aux_losses: A dictionary containing a list of auxiliary losses per task.
                        Either pass the loss name as string or a loss class.
                        If passing classes, the losses should not have been
                        initialized yet, i.e. just pass the class object, not an instance.

            gradient_approximation: Whether to approximate the auxiliary gradient
                                   calculation. Can be either a name of layers
                                   to use, e.g. "shared" or "last_shared".
                                   Or apply stochastic gradient approximation,
                                   use "stochastic" or "stochastic_eager".
                                   Default is to not use any approximation.
                                   This may be quite memory intensive.

            approximation_percentage: Only used when gradient_approximation="stochastic".
                                      Percentage of layers to use for stochastic
                                      sampling. Defaults to 0.1 = 10%.

            multi_task_uncertainty: Whether to use adaptive multi-task weighting.
                                    See Also: MultiTaskUncertainty model.

            weights_init: Dictionary of initial weights for each tasks when using multitask uncertainty.

            **kwargs: kwargs passed to keras.Model init.
        """

        super(NormalizedGradientSimilarity, self).__init__(**kwargs)

        # Map loss names to loss classes, if applicable
        self.aux_losses = {name: [get_loss(i) if type(i) == str else i
                                  for i in loss_list]
                           for name, loss_list in aux_losses.items()}

        self.gradient_approximation = gradient_approximation
        self.approximation_percentage = approximation_percentage or 0.1
        self.multi_task_uncertainty = multi_task_uncertainty
        self.weights_init = weights_init
        self.nums_layers_use = None
        self.main_loss_variables = None
        self.aux_variables = None
        self.aux_variables_built = False
        self.aux_loss_weights_alpha = None
        self.aux_loss_weights_beta = None

    def compile(self, **kwargs):
        """Overwrite keras.Model compile()."""
        loss_weights = None
        if "loss_weights" in kwargs and kwargs["loss_weights"] is not None:
            if self.multi_task_uncertainty:
                print("WARNING: Not possible to specify loss weights explicitly "
                      "when using NormalizedGradientSimilarity model "
                      "with multi-task uncertainty. "
                      "Loss weights are adaptive. "
                      "Ignoring specified loss weights.")
            else:
                loss_weights = kwargs["loss_weights"]

        # Remove loss_weights kwarg
        kwargs.pop("loss_weights", None)

        # Compile to get number of tasks
        if self.gradient_approximation == "stochastic_eager":
            print("INFO: Training will run in eager execution as the stochastic_eager "
                  "gradient sampling is not implemented in graph mode.")
            run_eagerly = True
        else:
            run_eagerly = False

        # Compile (without loss weights)
        super(NormalizedGradientSimilarity, self).compile(run_eagerly=run_eagerly,
                                                          **kwargs)

        # Set loss weights
        if self.multi_task_uncertainty:
            # Set loss weights as trainable variables of the Model
            # w_i = 1 / (2 * sigma^2_i)

            # Initialize w_i = 1 or with specified weights_init
            self.weights_init = self.weights_init or {name: 1.0 for name in self.output_names}

            # Use regularizer ln sigma_i = -0.5 ln(w_i) added to loss
            weight_kwargs = dict(shape=(),
                                 constraint=MinVal(),
                                 regularizer=Log(-0.5),
                                 trainable=True)
            loss_weights = [
                self.add_weight(name='loss_weight_' + name, **weight_kwargs, initializer=Constant(self.weights_init[name]))
                for name in self.output_names
            ]

        elif loss_weights is None:
            num_outputs = len(self.output_names)
            num_outputs_inv = 1.0/num_outputs
            loss_weights = [num_outputs_inv for _ in self.output_names]

        alpha_kwargs = dict(shape=(),
                            initializer=Constant(0.1),
                            trainable=True,
                            constraint=NonNeg())
        self.aux_loss_weights_alpha = [
            [self.add_weight(name=f"loss_aux_weight_alpha_{name}_{aux.__name__}", **alpha_kwargs)
             for aux in self.aux_losses[name]]
            for name in self.output_names]

        beta_kwargs = dict(shape=(),
                           initializer=Constant(1.0),
                           trainable=True,
                           constraint=NonNeg())
        self.aux_loss_weights_beta = [
            [self.add_weight(name=f"loss_aux_weight_beta_{name}_{aux.__name__}", **beta_kwargs)
             for aux in self.aux_losses[name]]
            for name in self.output_names]

        # Compile (with loss weights)
        super(NormalizedGradientSimilarity, self).compile(run_eagerly=run_eagerly,
                                                          loss_weights=loss_weights,
                                                          **kwargs)

        # Add container for aux losses
        # When built, this converts the dictionary to a list of list of aux losses
        # conform to the output naming scheme.
        self.aux_losses = AuxLossesContainer(self.aux_losses, self.output_names)

        # Get all trainable variables, excluding loss and aux loss weights
        self.main_loss_variables = [var for var in self.trainable_variables
                                    if "loss_aux_weight" not in var.name]

        # Initialize length of aux variable list
        self.aux_variables = [None for _ in self.output_names]

    def train_step(self, data):
        """Overwrite keras.Model train_step() which is called in fit()."""

        # Unpack the data passed to fit()
        # x is input tensor, y is label dictionary
        x, y = data

        # Calculate normalization using current loss weights
        single_task_normalizations = [1.0 + tf.reduce_sum(aux_loss_alpha) for aux_loss_alpha in self.aux_loss_weights_alpha]

        # For the first run, obtain trainable variables per output
        if not self.aux_variables_built:

            with tf.GradientTape(persistent=True, watch_accessed_variables=False) as tape:
                tape.watch(self.main_loss_variables)

                # Forward pass prediction
                y_pred = self(x, training=True)

                # Compute the overall loss to build loss container
                self.compiled_loss(y, y_pred, regularization_losses=self.losses)

                # Build aux losses
                self.aux_losses.build(y_pred)

                # Wrap single-output models in list due to inconsistent keras interface
                if len(self.output_names) == 1:
                    y_pred = [y_pred]

                # Get trainable variables per output for stochastic sampling
                # To reduce memory load, calculate gradients in loop rather than
                # list comprehension
                for output_num, (loss_fn, output) in enumerate(zip(self.compiled_loss._losses, self.output_names)):

                    # Calculate single task losses
                    single_task_loss_val = loss_fn(y[output], y_pred[output_num])

                    with tape.stop_recording():
                        # Compute single task main gradients
                        single_task_gradients = tape.gradient(single_task_loss_val, self.main_loss_variables)

                        # Get variables for each output by looking up non-None gradients
                        self.aux_variables[output_num] = [var
                                                          for var, gradient
                                                          in zip(self.main_loss_variables, single_task_gradients)
                                                          if gradient is not None]

            # Sample static subset of the auxiliary variables
            if self.gradient_approximation is not None:
                if self.gradient_approximation == "every_second":
                    self.aux_variables = [vars[::2] for vars in self.aux_variables]
                elif self.gradient_approximation == "every_third":
                    self.aux_variables = [vars[::3] for vars in self.aux_variables]
                elif self.gradient_approximation == "every_tenth":
                    self.aux_variables = [vars[::10] for vars in self.aux_variables]
                elif self.gradient_approximation == "every_twentieth":
                    self.aux_variables = [vars[::20] for vars in self.aux_variables]
                elif self.gradient_approximation == "shared":
                    self.aux_variables = [[var for var in vars if "shared" in var.name]
                                          for vars in self.aux_variables]
                elif self.gradient_approximation == "last_shared":
                    self.aux_variables = [[var for var in vars if "last_shared" in var.name]
                                          for vars in self.aux_variables]
                elif self.gradient_approximation == "stochastic_eager":
                    # Use all variables, sample randomly later
                    # Specify number of layers to use for sampling
                    self.nums_layers_use = [max(1, int(self.approximation_percentage*len(vars)))
                                            for vars in self.aux_variables]
                    print(f"INFO: Stochastic sampling with {self.nums_layers_use} layers.")
                elif self.gradient_approximation == "stochastic":
                    print(f"INFO: Stochastic sampling with {100*self.approximation_percentage}% of network weights.")

            self.aux_variables_built = True
            # Release tape
            del tape

        # First, calculate main loss gradients w.r.t. to layer variables
        with tf.GradientTape(persistent=True, watch_accessed_variables=False) as tape:
            # Do not watch loss_weights as variables
            tape.watch(self.main_loss_variables)

            # Forward pass prediction
            y_pred = self(x, training=True)

            # Wrap single-output models in list due to inconsistent keras interface
            if len(self.output_names) == 1:
                y_pred = [y_pred]
                aux_losses = [self.aux_losses._losses]
            else:
                aux_losses = self.aux_losses._losses

            with tape.stop_recording():
                # Compute the overall loss for metrics update and loss build
                total_loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

            # Calculate single task loss values
            # This specifically needs to be called after compiled_loss
            # has been called once and hence is built
            single_task_loss_vals = [
                loss_fn(y[output], y_pred[output_num]) for
                output_num, (loss_fn, output) in enumerate(zip(self.compiled_loss._losses, self.output_names))
            ]

            # Calculate auxiliary loss values for each task
            single_task_aux_loss_vals = [
                [loss_fn(y[output], y_pred[output_num]) for
                 loss_fn in aux_loss_list]
                for output_num, (output, aux_loss_list) in enumerate(zip(self.output_names, aux_losses))
            ]

            # Build main loss
            main_loss = tf.reduce_sum(
                [tf.multiply(weight,
                             tf.divide(tf.add(main_loss,
                                              tf.reduce_sum([alpha*beta*aux_loss
                                                             for alpha,
                                                                 beta,
                                                                 aux_loss
                                                             in zip(alpha_list,
                                                                    beta_list,
                                                                    aux_loss_list)])),
                                       normalization))
                 for weight,
                     main_loss,
                     alpha_list,
                     beta_list,
                     aux_loss_list,
                     normalization
                 in zip(self.compiled_loss._loss_weights,
                        single_task_loss_vals,
                        self.aux_loss_weights_alpha,
                        self.aux_loss_weights_beta,
                        single_task_aux_loss_vals,
                        single_task_normalizations)
                 ]
            )

            # Calculate regularization losses (possibly empty list)
            if self.losses:
                reg_loss = losses_utils.cast_losses_to_common_dtype(self.losses)
                reg_loss = math_ops.add_n(reg_loss)
                main_loss += reg_loss

        # Calculate full model weight gradients
        full_gradients = tape.gradient(main_loss, self.main_loss_variables)

        # Randomly sample variables for gradient calculation
        if self.gradient_approximation == "stochastic_eager":
            curr_vars = [random.sample(vars, n)
                         for vars, n in zip(self.aux_variables, self.nums_layers_use)]
        else:
            curr_vars = self.aux_variables

        # Compute single task main gradients
        single_task_gradients = [
            tape.gradient(loss, vars)
            for loss, vars in zip(single_task_loss_vals, curr_vars)
        ]

        # Compute single task aux loss gradients
        single_task_aux_gradients = [
            [tape.gradient(loss, vars) for loss in loss_list]
            for loss_list, vars
            in zip(single_task_aux_loss_vals, curr_vars)
        ]

        # Release persistent gradient tape
        del tape

        # Flatten gradient array, s.t. every gradient is a vector
        # Then concat all layer gradients into single vector.
        single_task_gradients = [tf.concat([tf.reshape(vec, [-1]) for vec in grad], axis=0)
                                 for grad in single_task_gradients]

        # Flatten gradient array, s.t. every gradient is a vector
        single_task_aux_gradients = [[
            tf.concat([tf.reshape(vec, [-1]) for vec in grad], axis=0)
            for grad in grad_list]
            for grad_list in single_task_aux_gradients]

        # Multiply gradients with random mask tensor
        if self.gradient_approximation == "stochastic":
            grad_masks = [tf.cast(tf.random.uniform(shape, 0, 1) < self.approximation_percentage,
                                  tf.dtypes.bool)
                          for shape in [grad.shape for grad in single_task_gradients]]

            single_task_gradients = [tf.boolean_mask(grad, grad_mask)
                                     for grad_mask, grad
                                     in zip(grad_masks, single_task_gradients)]
            single_task_aux_gradients = [[
                tf.boolean_mask(grad, grad_mask) for grad in grad_list]
                for grad_mask, grad_list
                in zip(grad_masks, single_task_aux_gradients)]

        # Calculate the single task gradient norms. The single task gradients
        # themselves are lists, e.g. for layer kernel and bias.
        # Hence, they are flattened and concatenated first.
        single_task_gradient_norms = [tf.norm(grad) for grad in single_task_gradients]

        # Calculate the single task auxiliary gradient norms.
        single_task_aux_gradient_norms = [
            [tf.norm(grad) for grad in grad_list] for
            grad_list in single_task_aux_gradients
        ]

        with tf.GradientTape(persistent=True, watch_accessed_variables=False) as tape:
            # Only watch loss weights
            tape.watch(self.aux_loss_weights_alpha)
            tape.watch(self.aux_loss_weights_beta)

            # L_alpha = | alpha - GS(G_main, G_aux) |
            loss_alpha = tf.reduce_sum(
                [tf.reduce_sum([tf.math.abs(alpha - tf.divide(tf.maximum(0.0, tf.reduce_sum(grad_main*grad_aux)),
                                                    grad_main_norm*grad_aux_norm))
                                for alpha, grad_aux, grad_aux_norm
                                in zip(alpha_list, grad_aux_list, grad_aux_norm_list)])
                 for alpha_list, grad_aux_list, grad_aux_norm_list, grad_main, grad_main_norm
                 in zip(self.aux_loss_weights_alpha,
                        single_task_aux_gradients,
                        single_task_aux_gradient_norms,
                        single_task_gradients,
                        single_task_gradient_norms)])

            # L_beta = | ||G_main|| - || beta*G_aux|| |
            loss_beta = tf.reduce_sum(
                [tf.reduce_sum([tf.math.abs(grad_main_norm - tf.multiply(tf.abs(beta), grad_aux_norm))
                                for beta, grad_aux_norm
                                in zip(beta_list, grad_aux_norm_list)])
                 for beta_list,
                     grad_aux_norm_list,
                     grad_main_norm
                 in zip(self.aux_loss_weights_beta,
                        single_task_aux_gradient_norms,
                        single_task_gradient_norms)])

        # Calculate loss weight loss gradients
        gradients_alpha = [tape.gradient(loss_alpha, alpha) for alpha in self.aux_loss_weights_alpha]
        gradients_beta = [tape.gradient(loss_beta, beta) for beta in self.aux_loss_weights_beta]

        # Release persistent gradient tape
        del tape

        # Update model weights, including loss weights
        self.optimizer.apply_gradients(zip(full_gradients, self.main_loss_variables))

        # Update model loss weights
        [self.optimizer.apply_gradients(zip(gradient, alpha))
         for gradient, alpha
         in zip(gradients_alpha, self.aux_loss_weights_alpha)]

        [self.optimizer.apply_gradients(zip(gradient, beta))
         for gradient, beta
         in zip(gradients_beta, self.aux_loss_weights_beta)]

        # Unwrap single-output prediction for metrics update
        if len(self.output_names) == 1:
            y_pred = y_pred[0]

        # Update metrics (includes the metric that tracks the loss)
        self.compiled_metrics.update_state(y, y_pred)

        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}
