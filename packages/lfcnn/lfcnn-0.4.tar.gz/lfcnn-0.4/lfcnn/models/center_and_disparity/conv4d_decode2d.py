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
Encoder-decoder network based on spatio-angular separable 4D convolution
for estimating disparity and a central view from spectrally coded light fields.
"""
from typing import List

import tensorflow.keras as keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Add
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Concatenate
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Permute
from tensorflow.keras.layers import Reshape
from tensorflow.keras.layers import TimeDistributed

from lfcnn.generators import CentralAndDisparityGenerator
from lfcnn.generators.reshapes import lf_distributed
from lfcnn.layers import res_block_2d
from lfcnn.layers import sample_up_2d
from lfcnn.models import BaseModel


class Conv4dDecode2d(BaseModel):

    def __init__(self, num_filters_base=24, skip=True, kernel_reg=1e-5, **kwargs):
        super(Conv4dDecode2d, self).__init__(**kwargs)
        self.num_filters_base = num_filters_base
        self.skip = skip
        self.kernel_reg = kernel_reg

    def set_generator_and_reshape(self):
        self._generator = CentralAndDisparityGenerator
        self._reshape_func = lf_distributed
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:
        # Single input model
        input = inputs[0]

        downsample_strides = 2
        upsample_strides = 2
        kernel_reg = keras.regularizers.l2(self.kernel_reg)
        fb = self.num_filters_base

        res_kwargs = dict(kernel_regularizer=kernel_reg)
        downsample_spt_kwargs = dict(downsample_strides=downsample_strides, kernel_regularizer=kernel_reg)
        downsample_ang_kwargs = dict(kernel_regularizer=kernel_reg)
        upsample_kwargs = dict(strides=upsample_strides, kernel_regularizer=kernel_reg)

        ###########
        # ENCODER #
        ###########
        ###################
        # AS-CONV BLOCK 1 #
        ###################
        # Angular convolution and downsampling
        x = self.spt_to_ang(input)
        x_ang_1 = self.res_block_td(x, filters=fb, name='encode_res_1', **res_kwargs)
        x = self.ang_sample_down(x_ang_1, filters=fb, **downsample_ang_kwargs)
        x = self.ang_to_spt(x)
        # Spatial convolution and downsampling
        x_spt_1 = self.res_block_td(x, filters=fb, name='encode_res_2', **res_kwargs)
        x = self.spt_sample_down(x_spt_1, filters=2*fb, **downsample_spt_kwargs)

        ###################
        # AS-CONV BLOCK 2 #
        ###################
        # Angular convolution and downsampling
        x = self.spt_to_ang(x)
        x_ang_2 = self.res_block_td(x, filters=2*fb, name='encode_res_3', **res_kwargs)
        x = self.ang_sample_down(x_ang_2, filters=2*fb, **downsample_ang_kwargs)
        x = self.ang_to_spt(x)
        # Spatial convolution and downsampling
        x_spt_2 = self.res_block_td(x, filters=2*fb, name='encode_res_4', **res_kwargs)
        x = self.spt_sample_down(x_spt_2, filters=4*fb, **downsample_spt_kwargs)

        ###################
        # AS-CONV BLOCK 3 #
        ###################
        # Angular convolution and downsampling
        x = self.spt_to_ang(x)
        x_ang_3 = self.res_block_td(x, filters=4*fb, name='encode_res_5', **res_kwargs)
        x = self.ang_sample_down(x_ang_3, filters=4*fb, **downsample_ang_kwargs)
        x = self.ang_to_spt(x)
        # Spatial convolution and downsampling
        x_spt_3 = self.res_block_td(x, filters=4*fb, name='encode_res_6', **res_kwargs)
        x = self.spt_sample_down(x_spt_3, filters=8*fb, **downsample_spt_kwargs)

        ##############
        # BOTTLENECK #
        ##############
        x = self.bottleneck_reshape(x)
        x = res_block_2d(x, filters=8*fb, name='bottleneck_res', **res_kwargs)

        ####################
        # SKIP CONNECTIONS #
        ####################
        if self.skip:
            x_skip_1 = self.ang_to_spt(x_ang_1)
            x_skip_1 = self.bottleneck_reshape(x_skip_1)
            x_skip_1 = Concatenate()([x_skip_1, self.bottleneck_reshape(x_spt_1)])

            x_skip_2 = self.ang_to_spt(x_ang_2)
            x_skip_2 = self.bottleneck_reshape(x_skip_2)
            x_skip_2 = Concatenate()([x_skip_2, self.bottleneck_reshape(x_spt_2)])

            x_skip_3 = self.ang_to_spt(x_ang_3)
            x_skip_3 = self.bottleneck_reshape(x_skip_3)
            x_skip_3 = Concatenate()([x_skip_3, self.bottleneck_reshape(x_spt_3)])

        ###########
        # DECODER #
        ###########
        #############
        # DISPARITY #
        #############
        x1 = sample_up_2d(x, filters=8*fb, name='decode_disp_up_1', **upsample_kwargs)
        if self.skip:
            x1 = Concatenate()([x1, x_skip_3])
        x1 = res_block_2d(x1, filters=8*fb, name='decode_disp_res_1', **res_kwargs)
        x1 = sample_up_2d(x1, filters=4*fb, name='decode_disp_up_2', **upsample_kwargs)
        if self.skip:
            x1 = Concatenate()([x1, x_skip_2])
        x1 = res_block_2d(x1, filters=4*fb, name='decode_disp_res_2', **res_kwargs)
        x1 = sample_up_2d(x1, filters=2*fb, name='decode_disp_up_3', **upsample_kwargs)
        if self.skip:
            x1 = Concatenate()([x1, x_skip_1])
        x1 = res_block_2d(x1, filters=2*fb, name='decode_disp_res_3', **res_kwargs)
        x1 = keras.layers.Conv2D(filters=1, kernel_size=1, strides=1,
                                 padding='valid',
                                 kernel_initializer='he_normal',
                                 kernel_regularizer=None,
                                 dtype='float32',  # set explicitly for mixed precision case
                                 name='disparity')(x1)
        ################
        # CENTRAL VIEW #
        ################
        x2 = sample_up_2d(x, filters=8*fb, name='decode_central_up_1', **upsample_kwargs)
        if self.skip:
            x2 = Concatenate()([x2, x_skip_3])
        x2 = res_block_2d(x2, filters=8*fb, name='decode_central_res_1', **res_kwargs)
        x2 = sample_up_2d(x2, filters=4*fb, name='decode_central_up_2', **upsample_kwargs)
        if self.skip:
            x2 = Concatenate()([x2, x_skip_2])
        x2 = res_block_2d(x2, filters=4*fb, name='decode_central_res_2', **res_kwargs)
        x2 = sample_up_2d(x2, filters=2*fb, name='decode_central_up_3', **upsample_kwargs)
        if self.skip:
            x2 = Concatenate()([x2, x_skip_1])
        x2 = res_block_2d(x2, filters=2*fb, name='decode_central_res_3', **res_kwargs)
        x2 = keras.layers.Conv2D(filters=augmented_shape[-1], kernel_size=1, strides=1,
                                 padding='valid',
                                 kernel_initializer='he_normal',
                                 kernel_regularizer=None,
                                 dtype='float32',  # set explicitly for mixed precision case
                                 name='central_view')(x2)

        return keras.Model(input, [x1, x2], name="Conv4dDecode2D")

    @staticmethod
    def res_block_td(x,
                     filters,
                     kernel_regularizer,
                     name=None):
        """Time Distributed Residual Convolution"""

        name_1 = name + "_conv_1" if name is not None else None
        name_bn_1 = name + "_bn_1" if name is not None else None
        name_2 = name + "_conv_2" if name is not None else None
        name_bn_2 = name + "_bn_2" if name is not None else None
        name_3 = name + "_conv_3" if name is not None else None

        conv_kwargs = dict(strides=1,
                           padding='same',
                           kernel_initializer='he_normal',
                           kernel_regularizer=kernel_regularizer)

        x1 = TimeDistributed(
            Conv2D(filters=filters, kernel_size=3, name=name_1, **conv_kwargs))(x)
        x1 = BatchNormalization(name=name_bn_1)(x1)
        x1 = Activation('relu')(x1)
        x1 = TimeDistributed(
            Conv2D(filters=filters, kernel_size=3, name=name_2, **conv_kwargs))(x1)
        x1 = BatchNormalization(name=name_bn_2)(x1)
        x2 = TimeDistributed(
            Conv2D(filters=filters, kernel_size=1, name=name_3, **conv_kwargs))(x)
        return Add()([x1, x2])

    @staticmethod
    def sample_down_base(x,
                         filters,
                         kernel_size,
                         strides,
                         padding,
                         kernel_regularizer,
                         name=None):
        """Downsampling via strided convolution
        """
        name_conv = name + "_conv" if name is not None else None
        name_bn = name + "_bn" if name is not None else None

        x = TimeDistributed(
            Conv2D(filters=filters, kernel_size=kernel_size, strides=strides,
                   padding=padding, kernel_initializer='he_normal',
                   kernel_regularizer=kernel_regularizer), name=name_conv)(x)
        x = BatchNormalization(name=name_bn)(x)
        x = Activation('relu')(x)
        return x

    @staticmethod
    def spt_sample_down(x, filters, downsample_strides, kernel_regularizer, name=None):
        return Conv4dDecode2d.sample_down_base(
            x, filters=filters, kernel_size=3, strides=downsample_strides,
            padding='same', kernel_regularizer=kernel_regularizer, name=name)

    @staticmethod
    def ang_sample_down(x, filters, kernel_regularizer, name=None):
        """
        Implicit angular downsampling via valid padding.
        Input shape (batch, s*t, u, v, channel)
        """
        return Conv4dDecode2d.sample_down_base(
            x, filters=filters, kernel_size=3, strides=1,
            padding='valid', kernel_regularizer=kernel_regularizer, name=name)

    @staticmethod
    def spt_to_ang(x):
        """
        Spatial to angular reshape. Only works for square angular resolution.
        Reshape (batch, u*v, s, t, channel) -> (batch, s*t, u, v, channel)
        """
        (b, ang, s, t, c) = K.int_shape(x)
        x = Permute([2, 3, 1, 4])(x)
        ang_size = int(ang**0.5)
        return Reshape((s * t, ang_size, ang_size, c))(x)

    @staticmethod
    def ang_to_spt(x):
        """
        Angular to spatial reshape. Only works for square spatial resolution.
        Reshape (batch, s*t, u, v, channel) -> (batch, u*v, s, t, channel)
        """
        (b, spt, u, v, c) = K.int_shape(x)
        x = Permute([2, 3, 1, 4])(x)
        spt_size = int(spt**0.5)
        return Reshape((u * v, spt_size, spt_size, c))(x)

    @staticmethod
    def bottleneck_reshape(x):
        (b, ang, s, t, c) = K.int_shape(x)
        x = Permute([2, 3, 1, 4])(x)
        return Reshape((s, t, ang * c))(x)
