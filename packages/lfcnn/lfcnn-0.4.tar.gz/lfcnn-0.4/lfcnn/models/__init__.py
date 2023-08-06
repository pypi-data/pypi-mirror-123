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


"""The LFCNN models module.
"""
from typing import Optional, Callable

from .abstracts import BaseModel
from . import autoencoder
from . import center_and_disparity
from . import disparity
from . import sparse_coding
from . import superresolution


def get_model_type(model_type: str):
    """Given a model type name, returns the corresponding model type module.

    Args:
        model_type: Name of the model type.

    Returns:
        Model instance.
    """
    # Available model type classes
    classes = {
        "autoencoder": autoencoder,
        "center_and_disparity": center_and_disparity,
        "disparity": disparity,
        "sparse_coding": sparse_coding,
        "superresolution": superresolution,
    }
    try:
        return classes[model_type.lower()]
    except KeyError:
        raise ValueError(f"Unknown model type '{model_type}'.")
