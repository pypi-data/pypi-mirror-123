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
A loss container used for auxiliary losses, for example within the
GradientSimilarity training strategy.
"""

from inspect import isclass

from tensorflow.python.keras.engine.compile_utils import Container
from tensorflow.python.util import nest


class AuxLossesContainer(Container):
    """A container class for auxiliary losses.

    This is mostly analogous to keras LossesContainer, however without
    flattening the losses for the different outputs as we need to know
    which auxiliary loss belongs to which output and there may be a different
    number of auxiliary losses per output.
    """

    def __init__(self, losses, output_names=None):
        super(AuxLossesContainer, self).__init__(output_names=output_names)

        # Keep user-supplied values untouched for recompiling and serialization.
        self._user_losses = losses
        self._losses = losses
        self._built = False

        # Init all losses.
        # Since this is called within the scope of the model, this enables
        # distributed training
        for loss_list in losses.values():
            for loss in loss_list:
                if not isclass(loss):
                    raise ValueError(
                        f"You have passed in instantiated auxilary loss {loss}. "
                        f"Please only specify the loss class, not an instance.")
        self._losses = {name: [loss() for loss in loss_list]
                        for name, loss_list in losses.items()}

    def build(self, y_pred):
        """One-time setup of loss objects."""
        try:
            super(AuxLossesContainer, self).build(y_pred)  # tf 2.3 syntax
        except AttributeError:
            super(AuxLossesContainer, self)._build(y_pred)  # tf < 2.3 syntax
        self._losses = self._maybe_broadcast_to_outputs(y_pred, self._losses)
        self._losses = self._conform_to_outputs(y_pred, self._losses)
        self._built = True

    def _should_broadcast(self, obj):
        return not nest.is_sequence(obj)

    def _copy_object(self, obj):
        return obj  # Losses don't need to be copied.
