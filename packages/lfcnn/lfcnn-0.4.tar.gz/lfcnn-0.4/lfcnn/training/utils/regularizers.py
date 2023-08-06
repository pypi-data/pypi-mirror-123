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
Some Regularizer classes used for multi-task learning strategies.
"""

from tensorflow.python.keras import backend as K
from tensorflow.python.keras.regularizers import Regularizer
from tensorflow.python.ops import math_ops


class Sum(Regularizer):
    """A regularizer that applies Sum regularization penalty.
    The regularization penalty is computed as:
    `loss = alpha * reduce_sum(x)`

    Attributes:
        alpha: Float; regularization factor.
    """

    def __init__(self, alpha=1.0):
        self.alpha = K.cast_to_floatx(alpha)

    def __call__(self, x):
        return self.alpha * math_ops.reduce_sum(x)

    def get_config(self):
        return {'alpha': float(self.alpha)}


class Log(Regularizer):
    """A regularizer that applies natural logarithm regularization penalty.
    The regularization penalty is computed as:
    `loss = alpha * reduce_sum(log(x))`

    For example, this is used in the MultiTaskUncertainty training strategy.

    Attributes:
        alpha: Float; regularization factor.
    """

    def __init__(self, alpha=1.0):
        self.alpha = K.cast_to_floatx(alpha)

    def __call__(self, x):
        return self.alpha * math_ops.reduce_sum(math_ops.log(x))

    def get_config(self):
        return {'alpha': float(self.alpha)}
