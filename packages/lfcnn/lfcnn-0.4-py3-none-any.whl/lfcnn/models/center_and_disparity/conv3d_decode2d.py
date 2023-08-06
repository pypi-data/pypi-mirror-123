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
from typing import List, Optional

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Concatenate
from tensorflow.keras.layers import Permute
from tensorflow.keras.layers import Reshape

from lfcnn.models import BaseModel
from lfcnn.generators import CentralAndDisparityGenerator
from lfcnn.generators.reshapes import lf_subaperture_channel_stack, lf_identity
from lfcnn.layers import res_block_3d, res_block_2d
from lfcnn.layers import sample_down_3d, sample_up_2d
from lfcnn.layers import reshape_3d_to_2d
from lfcnn.layers.masks import get as get_mask_layer


class Conv3dDecode2d(BaseModel):

    def __init__(self,
                 num_filters_base: int = 24,
                 skip: bool = True,
                 superresolution: bool = False,
                 kernel_reg: float = 1e-5,
                 **kwargs):
        """Estimate a central view and disparity from a (coded) light field.
        Based on 3D Convolution for encoding and 2D convolution for decoding.

        Args:
            num_filters_base: Number of filters in the base layer.
                              For each downsampling, the number of filters is doubled.

            skip: Whether to use skip connections (U-net architecture).

            superresolution: Whethter to perform superresolution for output.

            kernel_reg: Strength of the L2 kernel regularizer during training.

            **kwargs: Passed to lfcnn.models.BaseModel.
        """
        super(Conv3dDecode2d, self).__init__(**kwargs)
        self.num_filters_base = num_filters_base
        self.skip = skip
        self.superresolution = superresolution
        self.kernel_reg = keras.regularizers.l2(kernel_reg)
        self.downsample_strides = 2
        self.upsample_strides = 2

    def set_generator_and_reshape(self):
        self._generator = CentralAndDisparityGenerator
        self._reshape_func = lf_subaperture_channel_stack
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]

        # Encoder
        x_en_1, x_en_2, x_en_3, x_en_4 = self.encoder(input)

        # Decoder disparity
        x1 = self.decoder_disparity([x_en_1, x_en_2, x_en_3, x_en_4])

        # Decoder central_view
        x2 = self.decoder_central([x_en_1, x_en_2, x_en_3, x_en_4],
                                  num_ch_out=augmented_shape[-1])

        return keras.Model(input, [x1, x2], name="Conv3dDecode2D")

    def encoder(self, input):

        filters_base = self.num_filters_base
        kernel_reg = self.kernel_reg
        down_strides = self.downsample_strides

        x_en_1 = res_block_3d(input,
                              filters=filters_base,  kernel_regularizer=kernel_reg,
                              name='encode_res_1')

        x_en_2 = sample_down_3d(x_en_1,
                                filters=2*filters_base,  strides=down_strides,
                                kernel_regularizer=kernel_reg,
                                name='encode_down_1')
        x_en_2 = res_block_3d(x_en_2, filters=2*filters_base,
                              kernel_regularizer=kernel_reg, name='encode_res_2')

        x_en_3 = sample_down_3d(x_en_2,
                                filters=4*filters_base, strides=down_strides,
                                kernel_regularizer=kernel_reg, name='encode_down_2')
        x_en_3 = res_block_3d(x_en_3,
                              filters=4*filters_base,
                              kernel_regularizer=kernel_reg, name='encode_res_3')

        x_en_4 = sample_down_3d(x_en_3,
                                filters=8*filters_base, strides=down_strides,
                                kernel_regularizer=kernel_reg, name='encode_down_3')
        x_en_4 = res_block_3d(x_en_4,
                              filters=8*filters_base,
                              kernel_regularizer=kernel_reg, name='encode_res_4')
        x_en_4 = reshape_3d_to_2d(x_en_4,
                                  name='encode_bottleneck_reshape')
        return x_en_1, x_en_2, x_en_3, x_en_4

    def decoder_disparity(self, inputs):
        x_en_1, x_en_2, x_en_3, x_en_4 = inputs

        filters_base = self.num_filters_base
        kernel_reg = self.kernel_reg
        up_strides = self.upsample_strides

        x1 = sample_up_2d(x_en_4,
                          filters=8*filters_base, strides=up_strides,
                          kernel_regularizer=kernel_reg, name='decode_disp_up_1')
        if self.skip:
            x1 = Concatenate(name='decode_disp_skip_concat_1')([x1, reshape_3d_to_2d(x_en_3, name='decode_disp_skip_reshape_1')])
        x1 = res_block_2d(x1,
                          filters=8*filters_base,
                          kernel_regularizer=kernel_reg, name='decode_disp_res_1')
        x1 = sample_up_2d(x1,
                          filters=4*filters_base, strides=up_strides,
                          kernel_regularizer=kernel_reg, name='decode_disp_up_2')
        if self.skip:
            x1 = Concatenate(name='decode_disp_skip_concat_2')([x1, reshape_3d_to_2d(x_en_2, name='decode_disp_skip_reshape_2')])
        x1 = res_block_2d(x1,
                          filters=4*filters_base,
                          kernel_regularizer=kernel_reg, name='decode_disp_res_2')
        x1 = sample_up_2d(x1,
                          filters=2*filters_base, strides=up_strides,
                          kernel_regularizer=kernel_reg, name='decode_disp_up_3')
        if self.skip:
            x1 = Concatenate(name='decode_disp_skip_concat_3')([x1, reshape_3d_to_2d(x_en_1, name='decode_disp_skip_reshape_3')])
        x1 = res_block_2d(x1,
                          filters=2*filters_base,
                          kernel_regularizer=kernel_reg, name='decode_disp_res_3')

        if self.superresolution:
            # No skip connection available for SR upsampling
            x1 = sample_up_2d(x1,
                              filters=filters_base, strides=up_strides,
                              kernel_regularizer=kernel_reg, name='decode_disp_superresolution_up')
            x1 = res_block_2d(x1,
                              filters=filters_base,
                              kernel_regularizer=kernel_reg, name='decode_disp_superresolution_res')

        x1 = keras.layers.Conv2D(filters=1,
                                 kernel_size=1,
                                 strides=1,
                                 padding='valid',
                                 kernel_initializer='he_normal',
                                 kernel_regularizer=None,
                                 dtype='float32',  # set explicitly for mixed precision case
                                 name='decode_disp_last_conv')(x1)

        return keras.layers.Lambda(lambda x: x, name="disparity")(x1)

    def decoder_central(self, inputs, num_ch_out):
        x_en_1, x_en_2, x_en_3, x_en_4 = inputs

        filters_base = self.num_filters_base
        kernel_reg = self.kernel_reg
        up_strides = self.upsample_strides

        x2 = sample_up_2d(x_en_4,
                          filters=8*filters_base, strides=up_strides,
                          kernel_regularizer=kernel_reg, name='decode_central_up_1')
        if self.skip:
            x2 = Concatenate(name='decode_central_skip_concat_1')(
                [x2, reshape_3d_to_2d(x_en_3, name='decode_central_skip_reshape_1')])
        x2 = res_block_2d(x2,
                          filters=8*filters_base,
                          kernel_regularizer=kernel_reg, name='decode_central_res_1')
        x2 = sample_up_2d(x2,
                          filters=4*filters_base, strides=up_strides,
                          kernel_regularizer=kernel_reg, name='decode_central_up_2')
        if self.skip:
            x2 = Concatenate(name='decode_central_skip_concat_2')(
                [x2, reshape_3d_to_2d(x_en_2, name='decode_central_skip_reshape_2')])
        x2 = res_block_2d(x2,
                          filters=4*filters_base,
                          kernel_regularizer=kernel_reg, name='decode_central_res_2')
        x2 = sample_up_2d(x2,
                          filters=2*filters_base, strides=up_strides,
                          kernel_regularizer=kernel_reg, name='decode_central_up_3')
        if self.skip:
            x2 = Concatenate(name='decode_central_skip_concat_3')(
                [x2, reshape_3d_to_2d(x_en_1, name='decode_central_skip_reshape_3')])
        x2 = res_block_2d(x2,
                          filters=2*filters_base,
                          kernel_regularizer=kernel_reg, name='decode_central_res_3')

        if self.superresolution:
            # No skip connection available for SR upsampling
            x2 = sample_up_2d(x2,
                              filters=2*filters_base, strides=up_strides,
                              kernel_regularizer=kernel_reg, name='decode_central_superresolution_up')
            x2 = res_block_2d(x2,
                              filters=2*filters_base,
                              kernel_regularizer=kernel_reg, name='decode_central_superresolution_res')

        x2 = keras.layers.Conv2D(filters=num_ch_out,
                                 kernel_size=1,
                                 strides=1,
                                 padding='valid',
                                 kernel_initializer='he_normal',
                                 kernel_regularizer=None,
                                 dtype='float32',  # set explicitly for mixed precision case
                                 name='decode_central_last_conv')(x2)
        return keras.layers.Lambda(lambda x: x, name='central_view')(x2)


class Conv3dDecode2dMasked(Conv3dDecode2d):

    def __init__(self,
                 mask_type: str = "neuralfractal",
                 mask_kwargs: Optional[dict] = None,
                 warmup: bool = False,
                 finetune: bool = False,
                 **kwargs):
        """
            **kwargs: See Conv3dDecode2d model.
        """
        super(Conv3dDecode2dMasked, self).__init__(**kwargs)
        self.mask_type = mask_type
        self.mask_kwargs = mask_kwargs or {}
        self._warmup = warmup
        self._finetune = finetune
        self.mask_layer = None

    def set_warmup(self, value):
        self._warmup = value
        self._build_necessary = True

    def set_finetune(self, value):
        self._finetune = value
        self._build_necessary = True

    def set_generator_and_reshape(self):
        self._generator = CentralAndDisparityGenerator
        self._reshape_func = lf_identity
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]
        _, u, v, s, t, ch = input.shape

        # Apply light field mask, when finetuning, fix mask and binarize
        self.mask_layer = get_mask_layer(self.mask_type)(**self.mask_kwargs, name="mask_layer")
        if self._finetune:
            print("INFO: Model finetuning. Only training encoder/decoder.")
            self.mask_layer.trainable = False
            binarize = True
        else:
            binarize = None  # determined by training option in mask call()

        x = self.mask_layer(input, binarize=binarize)
        ch_mask = x.shape[-1]
        # Permute (b, u, b, s, t, ch) -> (b, s, t, u, v, ch)
        # possibly: (b, u, b, s, t, 1) -> (b, s, t, u, v, 1)
        # Reshape (b, s, t, u, v, ch) -> (b, s, t, u*v, ch)
        x = Permute((3, 4, 1, 2, 5))(x)
        x = Reshape((s, t, u*v, ch_mask))(x)

        # Encoder
        x_en_1, x_en_2, x_en_3, x_en_4 = self.encoder(x)

        # Decoder disparity
        x1 = self.decoder_disparity([x_en_1, x_en_2, x_en_3, x_en_4])

        # Decoder central_view
        x2 = self.decoder_central([x_en_1, x_en_2, x_en_3, x_en_4],
                                  num_ch_out=augmented_shape[-1])

        model = keras.Model(input, [x1, x2], name="Conv3dDecode2DMasked")

        # During warmup, do not train Encoder & Decoder
        if self._warmup:
            print("INFO: Model warmup. Only training mask layer.")
            for layer in model.layers:
                if not layer.name == "mask_layer":
                    layer.trainable = False

        return model

    def get_mask(self):
        return self.mask_layer.get_mask()
