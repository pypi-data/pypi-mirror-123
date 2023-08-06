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

from tensorflow import keras
from tensorflow.keras.initializers import Constant

from lfcnn.training.utils.regularizers import Log
from lfcnn.training.utils.constraints import MinVal


class MultiTaskUncertainty(keras.Model):

    def __init__(self, **kwargs):
        """A Model subclass for Multi-Task Training with Uncertainty [1].

        The loss is calculated as

        L = sum_i 1/(2*sigma^2_i)*L_i + ln(simga_i)

        where sigma_i are trainable variables and L_i are the single task losses.
        Minimizing L is equivalent to minimizing, substituting w_i = 1/(2*sigma^2_i)

        L = sum_i w_i L_i - 0.5 ln(w_i)

        where w_i are trainable variables.


        [1] Alex Kendall, Yarin Gal, and Roberto Cipolla:
        "Multi-task learning using uncertainty to weigh losses for scene geometry
        and semantics."
        IEEE Conference on Computer Vision and Pattern Recognition. 2018.

        Args:
            **kwargs: kwargs passed to keras.Model init.
        """

        super(MultiTaskUncertainty, self).__init__(**kwargs)

    def compile(self, **kwargs):
        """Overwrite keras.Model compile()."""

        if "loss_weights" in kwargs and kwargs["loss_weights"] is not None:
                print("WARNING: Not possible to specify loss weights explicitly "
                      "when using MultiTaskUncertainty model. "
                      "Loss weights are adaptive. "
                      "Ignoring speciefied loss weights.")

        # Remove loss_weights kwarg (is set to None by default) and compile
        kwargs.pop("loss_weights", None)

        # Set loss weights as trainable variables of the Model
        # w_i = 1 / (2 * sigma^2_i)
        # Initialize w_i = 1
        # Use regularizer ln sigma_i = -0.5 ln(w_i) added to loss
        weight_kwargs = dict(shape=(),
                             initializer=Constant(1.0),
                             constraint=MinVal(),
                             regularizer=Log(-0.5),
                             trainable=True)
        loss_weights = [
            self.add_weight(name='loss_weight_' + name, **weight_kwargs)
            for name in self.output_names
        ]

        # Compile again now that we have added the loss weights to the model
        super(MultiTaskUncertainty, self).compile(loss_weights=loss_weights, **kwargs)

        # Do not need to implement train_step as loss weights and regularizer
        # are observed by default in fit().
