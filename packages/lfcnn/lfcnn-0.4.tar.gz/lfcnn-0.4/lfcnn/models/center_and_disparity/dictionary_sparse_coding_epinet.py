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

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Lambda
from tensorflow.keras.layers import Permute
from tensorflow.keras.layers import Reshape
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Concatenate

from lfcnn.generators import CentralAndDisparityGenerator
from lfcnn.generators.reshapes import lf_identity

from lfcnn.models import BaseModel
from lfcnn.models.sparse_coding import DictionarySparseCoding
from lfcnn.models.disparity.epinet import Epinet

from lfcnn.models.sparse_coding.dictionary_sparse_coding import SparseCodingLayer
from lfcnn.models.sparse_coding.dictionary_sparse_coding import TensorDecompositionLayer
from lfcnn.models.sparse_coding.utils.patching import Patch
from lfcnn.models.sparse_coding.utils.patching import DePatch
from lfcnn.models.sparse_coding.utils.patching import DePatchEfficient


class DictionarySparseCodingEpinet(BaseModel):

    def __init__(self,
                 sparse_coding_kwargs,
                 **kwargs):

        super(DictionarySparseCodingEpinet, self).__init__(**kwargs)
        self.sparse_coding_kwargs = sparse_coding_kwargs
        self.padding = 'valid'

        self.overcompleteness = sparse_coding_kwargs['overcompleteness']
        self.use_mask = sparse_coding_kwargs['use_mask']
        self.patch_size_st = sparse_coding_kwargs['patch_size_st']
        self.patch_size_uv = sparse_coding_kwargs['patch_size_uv']
        self.patch_step_st = sparse_coding_kwargs['patch_step_st']
        self.patch_step_uv = sparse_coding_kwargs['patch_step_uv']

        self.couple_strength = sparse_coding_kwargs['couple_strength']
        self.iterations_fista = sparse_coding_kwargs['iterations_fista']
        self.iterations_eigenval = sparse_coding_kwargs['iterations_eigenval']
        self.efficient_depatch = sparse_coding_kwargs['efficient_depatch']
        self.measure_sparsity = sparse_coding_kwargs['measure_sparsity']
        self.decomposition = sparse_coding_kwargs.get('decomposition', 'sparse_coding')

    def set_generator_and_reshape(self):
        self._generator = CentralAndDisparityGenerator
        self._reshape_func = lf_identity
        return

    def create_model(self, inputs: List[keras.Input], augmented_shape=None) -> keras.Model:

        # Get (u, v, s, t, ch) shape
        u, v, s, t, ch = inputs[0].shape[1:].as_list()
        u_cent, v_cent = u//2, v//2

        # Single input model
        x = inputs[0]
        original_shape = inputs[0].shape[1:]
        ch = x.shape[-1]

        # Patch light fields
        # (b, u, v, s, t, ch) -> (b, N, u', v', s', t', ch)
        patch_layer = Patch(name='patch_light_field',
                            patch_size_st=self.patch_size_st,
                            patch_size_uv=self.patch_size_uv,
                            patch_step_st=self.patch_step_st,
                            patch_step_uv=self.patch_step_uv)
        x = patch_layer(x)

        # Sparse code light field
        coding_kwargs = dict(overcompleteness=self.overcompleteness,
                             use_mask=self.use_mask,
                             couple_strength=self.couple_strength,
                             iterations_fista=self.iterations_fista,
                             iterations_eigenval=self.iterations_eigenval,
                             measure_sparsity=self.measure_sparsity)
        if self.decomposition == "sparse_coding":
            coding_layer = SparseCodingLayer(**coding_kwargs)
        elif self.decomposition == 'tensor_decomposition':
            coding_layer = TensorDecompositionLayer(**coding_kwargs)
        else:
            raise ValueError(f"Unknown decomposition type '{self.decomposition}'")
        x = coding_layer(x)

        # De-patch light fields
        depatch_kwags = dict(name='light_field',
                             original_shape=original_shape,
                             patch_size_st=patch_layer.patch_size_st,
                             patch_step_st=patch_layer.patch_step_st,
                             num_patches_st=patch_layer.num_patches_st,
                             patch_size_uv=patch_layer.patch_size_uv,
                             patch_step_uv=patch_layer.patch_step_uv,
                             num_patches_uv=patch_layer.num_patches_uv)

        if self.efficient_depatch:
            depatch_layer = DePatchEfficient(**depatch_kwags)
        else:
            depatch_layer = DePatch(**depatch_kwags)

        x = depatch_layer(x)

        # Crop spatially because EPINET crops due to valid padding
        central_view = Lambda(lambda y: y[:, u_cent, v_cent, 11:-11, 11:-11], name='central_view')(x)

        # Convert to mono, shape (b, u, v, s, t, 1)
        # Factor 3 is due to a bug in the generator's "to_mono" conversion
        # which summs rather than means. Therefore, during training, EPINET
        # was exposed to lightfields ranged in (0, 3) rather then (0, 1).
        x = keras.layers.Lambda(lambda y: 3.0*tf.reduce_mean(y, axis=-1, keepdims=True), name='to_mono')(x)

        # Extract crosshair input for EPINET
        horz = Lambda(lambda y: y[:, u_cent])(x)
        horz = Permute((2, 3, 1, 4))(horz)
        horz = Reshape((s, t, u, 1))(horz)

        vert = Lambda(lambda y: y[:, :, v_cent])(x)
        vert = Permute((2, 3, 1, 4))(vert)
        vert = Reshape((s, t, v, 1))(vert)

        # Reshape to (ch, s, t, u, v)
        diag = Permute((5, 3, 4, 1, 2))(x)

        # Extract diagonal in u,v (last two axes)
        diag1 = Lambda(lambda y: tf.linalg.diag_part(y))(diag)
        # Extract mirrored diagonal
        diag2 = Lambda(lambda y: tf.reverse(y, (-1,)))(diag)
        diag2 = Lambda(lambda y: tf.linalg.diag_part(y))(diag2)

        # Reshape (ch, s, t, d) to (s, t, d, ch)
        diag1 = Permute((2, 3, 4, 1))(diag1)
        diag2 = Permute((2, 3, 4, 1))(diag2)
        diag2 = Lambda(lambda y: tf.reverse(y, (3,)))(diag2)

        # Copy from EPINET
        # For mono light fields, squeeze channel axis
        mid1 = Epinet.base_block(tf.squeeze(horz, axis=-1), kernel_size=2, num_filters=70, reps=3, padding=self.padding,
                                 name='horz')
        mid2 = Epinet.base_block(tf.squeeze(vert, axis=-1), kernel_size=2, num_filters=70, reps=3, padding=self.padding,
                                 name='vert')
        mid3 = Epinet.base_block(tf.squeeze(diag1, axis=-1), kernel_size=2, num_filters=70, reps=3,
                                 padding=self.padding, name='diag1')
        mid4 = Epinet.base_block(tf.squeeze(diag2, axis=-1), kernel_size=2, num_filters=70, reps=3,
                                 padding=self.padding, name='diag2')

        disparity = Concatenate(axis=-1, name='mid_merged')([mid1, mid2, mid3, mid4])
        disparity = Epinet.base_block(disparity, kernel_size=2, num_filters=280, reps=7, padding=self.padding, name='merge')

        # set dtype explicitly for mixed precision case
        disparity = Conv2D(filters=280, kernel_size=2, strides=1, padding=self.padding, name='last_conv1', dtype='float32')(
            disparity)
        disparity = Activation('relu', name='last_relu', dtype='float32')(disparity)
        disparity = Conv2D(filters=1, kernel_size=2, strides=1, padding=self.padding, name='disparity', dtype='float32')(disparity)
        self._model_crop = (11, 11)

        return keras.Model(inputs, [central_view, disparity], name="DictionarySparseCodingEpinet")
