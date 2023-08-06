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


"""Custom initializer classes.
"""
import tensorflow as tf
from tensorflow.keras.initializers import TruncatedNormal


class NormalizedTruncatedNormal(TruncatedNormal):
    """Initializer that generates a truncated normal distribution with
    unit norm along a specified axis.
    """

    def __init__(self, axis=0, order=2, *args, **kwargs):

        super(NormalizedTruncatedNormal, self).__init__(*args, **kwargs)
        self.axis = axis
        self.order = order

    def __call__(self, *args, **kwargs):

        init_val = super(NormalizedTruncatedNormal, self).__call__(*args, **kwargs)
        return init_val / tf.linalg.norm(init_val, ord=self.order, axis=self.axis, keepdims=True)
