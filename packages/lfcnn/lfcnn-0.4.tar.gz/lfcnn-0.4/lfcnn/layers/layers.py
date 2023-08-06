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
import uuid

import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Add
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Conv2DTranspose
from tensorflow.keras.layers import Conv3D
from tensorflow.keras.layers import Conv3DTranspose
from tensorflow.keras.layers import Reshape


def _res_block_factory(conv_class,
                       x,
                       filters,
                       kernel_size,
                       kernel_regularizer,
                       name):
    """Factory to create residual convolution layers in 2D or 3D.
    Should not be used directly, instead use `:func:res_block_2d`or
    `:func:res_block_3d`.

    Args:
        conv_class: Used convolution class.
                    Use 'keras.layers.Conv2D' for 2D residual convolution.
                    Use 'keras.layers.Conv3D' for 2D residual convolution.

        x:          Input tensor.

        filters: Number of filters per convolution layer.

        kernel_size: Size of the convolution kernels.

        kernel_regularizer: Optional kernel regularizer.

        name: Optional name for the layer.
    """

    name_1 = name + "_conv_1" if name is not None else None
    name_bn_1 = name + "_bn_1" if name is not None else None
    name_2 = name + "_conv_2" if name is not None else None
    name_bn_2 = name + "_bn_2" if name is not None else None
    name_3 = name + "_conv_3" if name is not None else None

    # Arguments common to all layers
    conv_kwargs = dict(filters=filters,
                       padding='same',
                       kernel_initializer='he_normal',
                       kernel_regularizer=kernel_regularizer)

    # Convolutional path
    x1 = conv_class(kernel_size=kernel_size, name=name_1, **conv_kwargs)(x)
    x1 = BatchNormalization(name=name_bn_1)(x1)
    x1 = Activation('relu')(x1)
    x1 = conv_class(kernel_size=kernel_size, name=name_2, **conv_kwargs)(x1)
    x1 = BatchNormalization(name=name_bn_2)(x1)

    # Residual connection
    x2 = conv_class(kernel_size=1, name=name_3, **conv_kwargs)(x)
    return Add(name=name)([x1, x2])


def res_block_2d(x,
                 filters,
                 kernel_size=(3, 3),
                 kernel_regularizer=None,
                 name=None):
    """Residual convolution using Conv2D.
    For options, see `:func:res_block_factory`.
    """
    return _res_block_factory(Conv2D,
                              x,
                              filters=filters,
                              kernel_size=kernel_size,
                              kernel_regularizer=kernel_regularizer,
                              name=name)


def res_block_3d(x,
                 filters,
                 kernel_size=(3, 3, 3),
                 kernel_regularizer=None,
                 name=None):
    """Residual convolution using Conv3D.
    For options, see `:func:res_block_factory`.
    """
    return _res_block_factory(Conv3D,
                              x,
                              filters=filters,
                              kernel_size=kernel_size,
                              kernel_regularizer=kernel_regularizer,
                              name=name)


def _sample_up_down_factory(conv_class,
                            x,
                            filters,
                            kernel_size=3,
                            strides=2,
                            kernel_regularizer=None,
                            name=None):
    """Factory to create up/downsampling layers based on strided/transposed
    convolution.
    Should not be used directly, instead use
    `:func:sample_up_2d` and `:func:sample_down_2d` or
    `:func:sample_up_3d` and `:func:sample_down_3d`.

    Args:
        conv_class: Used convolution class.
                    Use 'keras.layers.Conv2D' for 2D residual convolution.
                    Use 'keras.layers.Conv3D' for 2D residual convolution.

        x:          Input tensor.

        num_filters: Number of filters per convolution layer.

        kernel_size: Size of the convolution kernels.

        strides: Stride used for up/downsampling.

        kernel_regularizer: Optional kernel regularizer.

        name: Optional name for the layer.

    Returns:

    """

    name_conv = name + "_conv" if name is not None else None
    name_bn = name + "_bn" if name is not None else None
    x = conv_class(filters=filters,
                   kernel_size=kernel_size,
                   strides=strides,
                   padding='same',
                   kernel_initializer='he_normal',
                   kernel_regularizer=kernel_regularizer,
                   name=name_conv)(x)
    x = BatchNormalization(name=name_bn)(x)
    x = Activation('relu')(x)
    return x


def sample_down_2d(x,
                   filters,
                   kernel_size=(3, 3),
                   strides=(2, 2),
                   kernel_regularizer=None,
                   name=None):
    """Downsampling via 2D strided convolution.
    For options, see `:func:sample_up_down_factory`.
    """
    return _sample_up_down_factory(Conv2D,
                                   x,
                                   filters=filters,
                                   kernel_size=kernel_size,
                                   strides=strides,
                                   kernel_regularizer=kernel_regularizer,
                                   name=name)


def sample_up_2d(x,
                 filters,
                 kernel_size=(3, 3),
                 strides=(2, 2),
                 kernel_regularizer=None,
                 name=None):
    """Upsampling via 2D transposed convolution.
    For options, see `:func:sample_up_down_factory`.
    """
    return _sample_up_down_factory(Conv2DTranspose,
                                   x,
                                   filters=filters,
                                   kernel_size=kernel_size,
                                   strides=strides,
                                   kernel_regularizer=kernel_regularizer,
                                   name=name)


def sample_down_3d(x,
                   filters,
                   kernel_size=(3, 3, 3),
                   strides=(2, 2, 2),
                   kernel_regularizer=None,
                   name=None):
    """Downsampling via 3D strided convolution.
    For options, see `:func:sample_up_down_factory`.
    """
    return _sample_up_down_factory(Conv3D, x,
                                   filters=filters,
                                   kernel_size=kernel_size,
                                   strides=strides,
                                   kernel_regularizer=kernel_regularizer,
                                   name=name)


def sample_up_3d(x,
                 filters,
                 kernel_size=(3, 3, 3),
                 strides=(2, 2, 2),
                 kernel_regularizer=None,
                 name=None):
    """Downsampling via 3D transposed convolution.
    For options, see `:func:sample_up_down_factory`.
    """
    return _sample_up_down_factory(Conv3DTranspose, x,
                                   filters=filters,
                                   kernel_size=kernel_size,
                                   strides=strides,
                                   kernel_regularizer=kernel_regularizer,
                                   name=name)


def reshape_3d_to_2d(x, name=None):
    _, w, h, s, t = K.int_shape(x)
    return Reshape((w, h, s * t), name=name)(x)


def soft_threshold(x, value):
    return tf.math.sign(x) * Activation('relu')(tf.math.abs(x) - value)
