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


"""The LFCNN central view and disparity estimator models.
"""

from .conv3d_decode2d import Conv3dDecode2d, Conv3dDecode2dMasked
from .conv3d_decode2d_st import Conv3dDecode2dStCentral, Conv3dDecode2dStDisp
from .conv4d_decode2d import Conv4dDecode2d
from .dummy import Dummy
from .dictionary_sparse_coding_epinet import DictionarySparseCodingEpinet


def get(model: str):
    """Given a model name, returns an lfcnn model instance.

    Args:
        model: Name of the model.

    Returns:
        Model instance.
    """
    # Available model classes
    classes = {
        "conv3ddecode2d": Conv3dDecode2d,
        "conv3ddecode2dmasked": Conv3dDecode2dMasked,
        "conv3ddecode2dstcentral": Conv3dDecode2dStCentral,
        "conv3ddecode2dstdisp": Conv3dDecode2dStDisp,
        "conv4ddecode2d": Conv4dDecode2d,
        "dictionarysparsecodingepinet": DictionarySparseCodingEpinet,
        "dummy": Dummy
    }
    try:
        return classes[model.lower()]
    except KeyError:
        raise ValueError(f"Unknown central view and disparity estimator model '{model}'.")
