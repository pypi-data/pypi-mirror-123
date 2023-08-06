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
A keras.Model subclass implementing the Gradient Similarity [1]
training strategy for adaptive auxiliary loss weighting.
More precisely, this implements the "weighted version" of the proposed method
as described in Algorithm 2, Appendix C of [1].

[1]: Du, Y., Czarnecki, W. M., Jayakumar, S. M., Pascanu, R., & Lakshminarayanan, B.:
"Adapting auxiliary losses using gradient similarity."
arXiv preprint arXiv:1812.02224. 2018.
"""
from typing import Dict, List, Union

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.ops import math_ops
from tensorflow.python.keras.utils import losses_utils

from lfcnn.training.utils.aux_losses_container import AuxLossesContainer
from lfcnn.losses import get as get_loss


class GradientSimilarity(keras.Model):

    def __init__(self,
                 aux_losses: Dict[str, List[Union[str, keras.losses.Loss]]],
                 **kwargs):
        """A keras.Model subclass implementing the Gradient Similarity [1]
        training strategy for adaptive auxiliary loss weighting.
        More precisely, this implements the "weighted version" of the proposed
        method as described in Algorithm 2, Appendix C of [1].

        [1]: Du, Y., Czarnecki, W. M., Jayakumar, S. M., Pascanu, R., & Lakshminarayanan, B.:
        "Adapting auxiliary losses using gradient similarity."
        arXiv preprint arXiv:1812.02224. 2018.

        Args:
            aux_losses: A dictionary containing a list of auxilary losses per task.
                        Either pass the loss name as string or a loss class.
                        If passing classes, the losses should not have been
                        initialized yet, i.e. just pass the class object, not an instance.

            **kwargs: kwargs passed to keras.Model init.
        """

        super(GradientSimilarity, self).__init__(**kwargs)

        # Map loss names to loss classes, if applicable
        self.aux_losses = {name: [get_loss(i) if type(i) == str else i
                                  for i in loss_list]
                           for name, loss_list in aux_losses.items()}
        self.aux_variables = None

    def compile(self, **kwargs):
        """Overwrite keras.Model compile()."""
        if "loss_weights" in kwargs and kwargs["loss_weights"] is not None:
            raise NotImplementedError("Currently, loss_weights are not supported "
                                      "with GradientSimilarity.")

        # Remove loss_weights kwarg (is set to None by default) and compile
        kwargs.pop("loss_weights", None)

        # Compile to get number of tasks
        super(GradientSimilarity, self).compile(**kwargs)

        # Add container for aux losses
        # When built, this converts the dictionary to a list of list of aux losses
        # conform to the output naming scheme.
        self.aux_losses = AuxLossesContainer(self.aux_losses, self.output_names)

        # Use all trainable variables for auxiliary gradient calculation
        self.aux_variables = self.trainable_variables

    def train_step(self, data):
        """Overwrite keras.Model train_step() which is called in fit()."""

        # Unpack the data passed to fit()
        # x is input tensor, y is label dictionary
        x, y = data

        # First, calculate main loss gradients w.r.t. to total variables
        # and single task loss gradients w.r.t. to last shared variables
        with tf.GradientTape(persistent=True) as tape:

            # Forward pass prediction
            y_pred = self(x, training=True)

            with tape.stop_recording():
                # Compute the overall loss for metrics update
                total_loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

                if not self.aux_losses._built:
                    self.aux_losses.build(y_pred)

            # Wrap single-output models in list due to inconsistent keras interface
            if len(self.output_names) == 1:
                y_pred = [y_pred]
                aux_losses = [self.aux_losses._losses]
            else:
                aux_losses = self.aux_losses._losses

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

            with tape.stop_recording():
                # Compute single task main gradients
                single_task_gradients = [
                    tape.gradient(loss, self.aux_variables)
                    for loss in single_task_loss_vals
                ]

                # Compute single task aux loss gradients
                single_task_aux_gradients = [
                    [tape.gradient(loss, self.aux_variables) for loss in loss_list] for
                    loss_list in single_task_aux_loss_vals
                ]

                # Flatten gradient array, s.t. every gradient is a vector
                # Since not all weights are shared by each task, some gradients are None
                # We drop those values for each task
                single_task_gradients = [tf.concat([tf.reshape(vec, [-1]) for vec in grad if vec is not None], axis=0)
                                         for grad in single_task_gradients]

                # Flatten gradient array, s.t. every gradient is a vector
                single_task_aux_gradients = [[
                    tf.concat([tf.reshape(vec, [-1]) for vec in grad if vec is not None], axis=0)
                    for grad in grad_list]
                    for grad_list in single_task_aux_gradients
                ]

                # Calculate the single task gradient norms. The single task gradients
                # themselves are lists, e.g. for layer kernel and bias.
                # Hence, they are flattened and concatenated first.
                single_task_gradient_norms = [tf.norm(grad) for grad in single_task_gradients]

                # Calculate the single task auxiliary gradient norms.
                single_task_aux_gradient_norms = [
                    [tf.norm(grad) for grad in grad_list] for
                    grad_list in single_task_aux_gradients
                ]

                # Calculate aux loss weights
                # weight = max(0, CS(G_main, G_aux))*||G_main|| / ||G_aux||
                aux_loss_weights_alpha = [
                    [tf.divide(
                        tf.maximum(0.0, tf.reduce_sum(grad_main*grad_aux)),
                        grad_main_norm*grad_aux_norm)
                        for grad_aux, grad_aux_norm in zip(grad_aux_list, grad_aux_norm_list)]
                    for grad_main, grad_aux_list, grad_main_norm, grad_aux_norm_list
                    in zip(single_task_gradients,
                           single_task_aux_gradients,
                           single_task_gradient_norms,
                           single_task_aux_gradient_norms)
                ]

                del single_task_gradients
                del single_task_aux_gradients

            # Resume tape variable watching
            # Build main loss
            main_loss = tf.reduce_sum(
                [
                    tf.add(main_loss,
                           tf.reduce_sum([alpha*aux_loss
                                          for alpha, aux_loss
                                          in zip(alpha_list, aux_loss_list)]))
                    for main_loss, alpha_list, aux_loss_list
                    in zip(single_task_loss_vals,
                           aux_loss_weights_alpha,
                           single_task_aux_loss_vals)
                ])

            # Calculate regularization losses (possibly empty list)
            if self.losses:
                reg_loss = losses_utils.cast_losses_to_common_dtype(self.losses)
                reg_loss = math_ops.add_n(reg_loss)
                reg_loss = tf.reduce_sum(reg_loss)
                main_loss = tf.add(main_loss, reg_loss)

        # Calculate full model weight gradients
        full_gradients = tape.gradient(main_loss, self.trainable_variables)

        # Release gradient tape
        del tape

        # Update model weights
        self.optimizer.apply_gradients(zip(full_gradients, self.trainable_variables))
        del full_gradients

        # Unwrap single-output prediction for metrics update
        if len(self.output_names) == 1:
            y_pred = y_pred[0]

        # Update metrics (includes the metric that tracks the loss)
        self.compiled_metrics.update_state(y, y_pred)

        # Return a dict mapping metric names to current value
        return {m.name: m.result() for m in self.metrics}
