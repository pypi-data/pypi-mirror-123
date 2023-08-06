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


"""The LFCNN multi-task training strategies.
"""

from .grad_norm import GradNorm
from .multi_task_uncertainty import MultiTaskUncertainty


def get(strategy: str):
    """Given a strategy name, returns a Keras model subclass.

    Args:
        model: Name of the strategy.

    Returns:
        Keras model subclass.
    """
    # Available classes
    classes = {
        "gradnorm": GradNorm,
        "multitaskuncertainty": MultiTaskUncertainty
    }
    try:
        return classes[strategy.lower()]
    except KeyError:
        raise ValueError(f"Unknown multi-task strategy '{strategy}'.")
