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
A Model subclass for end-to-end mask optimization.
"""

import tensorflow as tf
from tensorflow import keras


class MaskOptimization(keras.Model):

    def __init__(self, mask_lr=1e-3, mask_weights_name="mask_weights", **kwargs):
        """A Model subclass for end-to-end mask optimization.

        Mask weights and the downstream network weights can be trained
        using different optimizer with different learning rates.

        Args:
            **kwargs: kwargs passed to keras.Model init.
        """
        super(MaskOptimization, self).__init__(**kwargs)
        self._mask_lr = mask_lr
        self._mask_weights_name = mask_weights_name
        self._cnn_weights = None
        self._mask_weights = None
        self.optimizer_mask = None
        return

    def compile(self, **kwargs):
        """Overwrite keras.Model compile()."""
        super(MaskOptimization, self).compile(**kwargs)

        # Get model weights
        self._cnn_weights = [vars for vars in self.trainable_variables
                             if not self._mask_weights_name in vars.name]
        self._mask_weights = [vars for vars in self.trainable_variables
                              if self._mask_weights_name in vars.name]

        # For mask, use SGD optimizer
        self.optimizer_mask = keras.optimizers.SGD(self._mask_lr, momentum=0.95, nesterov=True)
        return

    def train_step(self, data):
        """The logic for one training step.
        """
        # Unpack the data.
        x, y = data

        # Run forward pass.
        with tf.GradientTape(persistent=True) as tape:
            y_pred = self(x, training=True)
            loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

        # Minimize CNN variables using default optimizer
        # and mask variables using mask optimizer
        cnn_grads = tape.gradient(loss, self._cnn_weights)
        mask_grads = tape.gradient(loss, self._mask_weights)
        self.optimizer.apply_gradients(zip(cnn_grads, self._cnn_weights))
        self.optimizer_mask.apply_gradients(zip(mask_grads, self._mask_weights))

        # Release persistent tape
        del tape

        self.compiled_metrics.update_state(y, y_pred)

        # Collect metrics to return
        return_metrics = {}
        for metric in self.metrics:
            result = metric.result()
            if isinstance(result, dict):
                return_metrics.update(result)
            else:
                return_metrics[metric.name] = result

        return return_metrics
