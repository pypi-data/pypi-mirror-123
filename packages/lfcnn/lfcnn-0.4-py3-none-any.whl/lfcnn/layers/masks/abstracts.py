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


"""Abstract layer for light field coding masks.
"""

from typing import List
from typing import Optional

import tensorflow as tf
import tensorflow.keras as keras

from numpy.core import ndarray


class AbstractMaskLayer(keras.layers.Layer):

    def __init__(self,
                 roll: bool = True,
                 *args, **kwargs):
        """An abstract base keras.Layer implementing a light field coding mask.

        Args:
            *args, **kwargs: Passed to keras.Layer instantiation.
        """
        super(AbstractMaskLayer, self).__init__(*args, **kwargs)
        self._roll = roll
        return

    @staticmethod
    def roll(mask, max_amount: int, axis: List[int] = [0, 1]):
        """Apply a random roll of the mask. Useful in the training phase.


        Args:
            mask:        Mask to roll.
            max_amount:  Maximum absolute roll amount. One value for all axes.
            axis:        Which axes to roll.

        Returns:
            Rolled mask
        """
        # Generate random shift and roll mask
        shift = tf.random.uniform((len(axis), ), minval=-max_amount, maxval=max_amount, dtype=tf.int32)
        return tf.roll(mask, shift=shift, axis=axis)

    def get_mask(self) -> ndarray:
        """Return the light field coding mask.

        Should be a shape that can be broadcasted for direct element-wise
        multiplication with a light field batch of shape (b, u, v, s, t, ch)
        """
        raise NotImplementedError("This needs to be implemented by the derived class.")

    def get_mask_weights(self) -> Optional[ndarray]:
        """Return the non-binarized light field coding mask.

        Should be a shape that can be broadcasted for direct element-wise
        multiplication with a light field batch of shape (b, u, v, s, t, ch)
        """
        raise NotImplementedError("This needs to be implemented by the derived class.")

    def call(self, input, training=None, binarize=None):
        raise NotImplementedError("This needs to be implemented by the derived class.")
