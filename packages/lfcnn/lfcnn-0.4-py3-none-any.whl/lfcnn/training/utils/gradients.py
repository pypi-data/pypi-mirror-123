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
Some utils for gradient calculations.
"""

from typing import List

import tensorflow as tf


@tf.function
def gradients_add(gradients_a: List[tf.Tensor], gradients_b: List[tf.Tensor]) -> List[tf.Tensor]:
    """Element-wise addition of list of gradients as for example obtained
    from GradientTape.gradient.

    This calculate ignores None in the sense that 5 + None = 5.

    """
    if len(gradients_a) == 0:
        return gradients_b
    if len(gradients_b) == 0:
        return gradients_a

    assert len(gradients_a) == len(gradients_b)
    return [tf.add(grad_a, grad_b) if grad_a is not None and grad_b is not None
                                   else grad_a if grad_a is not None
                                   else grad_b if grad_b is not None
                                   else None
            for grad_a, grad_b in zip(gradients_a, gradients_b)]


@tf.function
def gradients_reduce_sum(gradient_list: List[List[tf.Tensor]]) -> List[tf.Tensor]:
    """Reduce a list of gradients by elemt-wise summation across the list index.

    This differs from regular tf.reduce_sum in that summation is not performed
    within a single gradient but across gradients.
    """

    mapper = lambda x: tf.reduce_sum(x, axis=0) if x != [] else None

    return [mapper([vec for vec in grads if vec is not None])
            for grads in zip(*gradient_list)]


@tf.function
def gradients_scalar_multiply(scalar: float, gradients: List[tf.Tensor]) -> List[tf.Tensor]:
    """Element-wise scalar multiplication of list of gradients as for example
    obtained from GradientTape.gradient.

    This calculate ignores None in the sense that 5*None = 5.

    """
    return [tf.multiply(scalar, grad) if grad is not None else None
            for grad in gradients]
