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
Encoder-decoder network based on 3D convolution for estimating
disparity and a central view from spectrally coded light fields.
"""
from typing import List

import tensorflow.keras as keras

from .conv3d_decode2d import Conv3dDecode2d
from lfcnn.generators import CentralGenerator, DisparityGenerator
from lfcnn.generators.reshapes import lf_subaperture_channel_stack


class Conv3dDecode2dStCentral(Conv3dDecode2d):

    def __init__(self,
                 **kwargs):
        """Estimate a central view from a (coded) light field.
        Based on 3D Convolution for encoding and 2D convolution for decoding.

        """
        super(Conv3dDecode2dStCentral, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = CentralGenerator
        self._reshape_func = lf_subaperture_channel_stack
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]

        # Encoder
        x_en_1, x_en_2, x_en_3, x_en_4 = self.encoder(input)
        # Decoder central_view
        x2 = self.decoder_central([x_en_1, x_en_2, x_en_3, x_en_4],
                                  num_ch_out=augmented_shape[-1])

        return keras.Model(input, [x2], name="Conv3dDecode2DStCentral")


class Conv3dDecode2dStDisp(Conv3dDecode2d):

    def __init__(self,
                 **kwargs):
        """Estimate a disparity from a (coded) light field.
        Based on 3D Convolution for encoding and 2D convolution for decoding.

        """
        super(Conv3dDecode2dStDisp, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = DisparityGenerator
        self._reshape_func = lf_subaperture_channel_stack
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]

        # Encoder
        x_en_1, x_en_2, x_en_3, x_en_4 = self.encoder(input)

        # Decoder disparity
        x1 = self.decoder_disparity([x_en_1, x_en_2, x_en_3, x_en_4])

        return keras.Model(input, [x1], name="Conv3dDecode2dStDisp")