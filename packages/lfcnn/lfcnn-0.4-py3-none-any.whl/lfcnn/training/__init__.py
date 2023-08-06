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


"""The LFCNN training module.

The training module defines some (optional) keras.Model subclasses implementing
specific training strategies, mostly in the context of multi-task learning.

The keras.Model subclasses can then be passed to lfcnn.Model instantiation.
"""
from typing import Optional, Callable

from .auxiliary_loss.gradient_similarity import GradientSimilarity
from .auxiliary_loss.normalized_gradient_similarity import NormalizedGradientSimilarity
from .multi_task.grad_norm import GradNorm
from .multi_task.multi_task_uncertainty import MultiTaskUncertainty
from .mask_optimization import MaskOptimization


def get_model_cls(model_cls: str) -> Optional[Callable]:
    """Given a model class name, returns the corresponding model class.

    Args:
        model_cls: Name of the model class.

    Returns:
        Model class.
    """

    if model_cls is None:
        return None

    # Available model type classes
    classes = {
        "none": None,
        "gradnorm": GradNorm,
        "multitaskuncertainty": MultiTaskUncertainty,
        "gradientsimilarity": GradientSimilarity,
        "normalizedgradientsimilarity": NormalizedGradientSimilarity,
        "maskoptimization": MaskOptimization,
    }
    try:
        return classes[model_cls.lower()]
    except KeyError:
        raise ValueError(f"Unknown model class '{model_cls}'.")
