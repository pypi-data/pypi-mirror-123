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
Some Constraint classes used for multi-task learning strategies.
"""

import tensorflow as tf
from tensorflow.python.keras.constraints import Constraint


class MinVal(Constraint):
    def __init__(self, min_value: float = 1e-7):
        """Constrains the weights to be larger than a specified min_value.

        Within some multi-task strategies, this constraint is used to ensure
        that no loss weight is set to zero (or even negative) during the loss
        weight update.

        Args:
            min_value: Minimum value of weight.
        """
        self.min_value = min_value

    def __call__(self, w):
        return tf.maximum(w, self.min_value)
