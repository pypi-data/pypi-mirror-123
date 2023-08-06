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


"""Light field patching and de-patching utilities.
"""

from itertools import product
from typing import Tuple

import tensorflow as tf
from tensorflow import Tensor
from tensorflow.keras.layers import Permute
from tensorflow.keras.layers import Reshape
from tensorflow.image import extract_patches


class Patch(tf.keras.layers.Layer):
    def __init__(self,
                 patch_size_st,
                 patch_size_uv,
                 patch_step_st,
                 patch_step_uv,
                 *args, **kwargs):
        super(Patch, self).__init__(*args, **kwargs)
        self.patch_size_st = patch_size_st
        self.patch_size_uv = patch_size_uv
        self.patch_step_st = patch_step_st
        self.patch_step_uv = patch_step_uv
        self.num_patches_st = None
        self.num_patches_st_total = None
        self.num_patches_uv = None
        self.num_patches_uv_total = None
        self.num_patches_total = None

        self.patch_st_kwargs = dict(sizes=[1, *self.patch_size_st, 1],
                                    strides=[1, *self.patch_step_st, 1],
                                    rates=[1, 1, 1, 1],
                                    padding="VALID")

        self.patch_uv_kwargs = dict(sizes=[1, *self.patch_size_uv, 1],
                                    strides=[1, *self.patch_step_uv, 1],
                                    rates=[1, 1, 1, 1],
                                    padding="VALID")

    def build(self, input_shape):
        _, u, v, s, t, ch = input_shape

        # Find out number of patches by patching a dummy tensor
        # Spatial patching
        tmp = tf.ones((1, s, t, u*v*ch), dtype=tf.float32)
        tmp = extract_patches(tmp, **self.patch_st_kwargs)
        _, *num_patches_st, _ = tmp.shape.as_list()
        num_patches_st_total = tf.math.reduce_prod(num_patches_st).numpy()

        # Angular patching
        tmp = tf.ones((1, u, v, tf.math.reduce_prod(self.patch_size_st)*ch), dtype=tf.float32)
        tmp = extract_patches(tmp, **self.patch_uv_kwargs)
        _, *num_patches_uv, _ = tmp.shape.as_list()
        num_patches_uv_total = tf.math.reduce_prod(num_patches_uv).numpy()

        self.num_patches_st = num_patches_st
        self.num_patches_st_total = num_patches_st_total
        self.num_patches_uv = num_patches_uv
        self.num_patches_uv_total = num_patches_uv_total
        self.num_patches_total = num_patches_uv_total * num_patches_st_total

        self.reshape_1 = (s, t, u*v*ch)
        self.reshape_2 = (self.num_patches_st_total, *self.patch_size_st, u, v, ch)
        self.reshape_3 = (u, v, self.patch_size_st[0]*self.patch_size_st[1]*ch*self.num_patches_st_total)
        self.reshape_4 = (num_patches_uv_total, *self.patch_size_uv, *self.patch_size_st, ch, self.num_patches_st_total)
        self.reshape_5 = (self.num_patches_total, *self.patch_size_uv, *self.patch_size_st, ch)
        return

    def call(self, input):
        # Input (b, u, v, s, t, ch)
        x = Permute((3, 4, 1, 2, 5))(input)
        # Reshape light field subaperture stack (b, s, t, u*v*ch)
        x = Reshape(self.reshape_1)(x)
        x = extract_patches(x, **self.patch_st_kwargs)
        # Reshape (b, n_s, n_t, s'*t'*u*v*ch) to (b, n_s*n_t, s', t', u, v, ch)
        x = Reshape(self.reshape_2)(x)
        # Reshape light field angular stack (b, u, v, s'*t'*ch*N_st)
        x = Permute((4, 5, 2, 3, 6, 1))(x)
        x = Reshape(self.reshape_3)(x)
        x = extract_patches(x, **self.patch_uv_kwargs)

        # Reshape (b, N_u, N_v, u', v', s'*t'*ch*N_st) to (b, N_uv, u', v', s', t', ch, N_st)
        x = Reshape(self.reshape_4)(x)

        # Reshape (b, N_uv, u', v', s', t', ch, N_st) to (b, N, u', v', s', t', ch)
        x = Permute((7, 1, 2, 3, 4, 5, 6))(x)
        x = Reshape(self.reshape_5)(x)
        return x


class DePatch(tf.keras.layers.Layer):
    def __init__(self,
                 original_shape,
                 patch_size_st,
                 patch_step_st,
                 num_patches_st,
                 patch_size_uv,
                 patch_step_uv,
                 num_patches_uv,
                 *args, **kwargs):
        super(DePatch, self).__init__(*args, **kwargs)
        self.original_shape = original_shape
        self.patch_size_st = patch_size_st
        self.patch_size_uv = patch_size_uv
        self.patch_step_st = patch_step_st
        self.patch_step_uv = patch_step_uv
        self.num_patches_st = num_patches_st
        self.num_st = num_patches_st[0] * num_patches_st[1]
        self.num_patches_uv = num_patches_uv
        self.num_uv = num_patches_uv[0] * num_patches_uv[1]

    def call(self, input):
        # Input shape (b, N, u', v', s', t', ch)
        x = input
        s = tf.shape(x)
        b_range = tf.range(s[0])
        ch_range = tf.range(s[-1])

        recovered = tf.zeros((s[0], *self.original_shape))
        mask = tf.zeros((s[0], *self.original_shape),
                        dtype=tf.int32)
        ones_patch = tf.ones((s[0], *self.patch_size_uv, *self.patch_size_st, s[-1]),
                             dtype=tf.int32)

        # Iterate over all patches
        for s, t, u, v in product(
                range(self.num_patches_st[0]),
                range(self.num_patches_st[1]),
                range(self.num_patches_uv[0]),
                range(self.num_patches_uv[1])):
            # Calculate indices conversion
            p_idx = s*self.num_patches_st[1]*self.num_uv + t*self.num_uv + u*self.num_patches_uv[1] + v
            u_idx = self.patch_step_uv[0]*u, self.patch_size_uv[0] + self.patch_step_uv[0]*u
            v_idx = self.patch_step_uv[1]*v, self.patch_size_uv[1] + self.patch_step_uv[1]*v
            s_idx = self.patch_step_st[0]*s, self.patch_size_st[0] + self.patch_step_st[0]*s
            t_idx = self.patch_step_st[1]*t, self.patch_size_st[1] + self.patch_step_st[1]*t

            # Construct indices
            indices = tf.meshgrid(
                b_range,  # batch
                tf.range(*u_idx),  # angular u
                tf.range(*v_idx),  # angular v
                tf.range(*s_idx),  # spatial s
                tf.range(*t_idx),  # spatial t
                ch_range,  # channel
                indexing='ij')

            indices = tf.stack(indices, axis=-1)

            # Add sliced image to recovered image indices
            recovered = tf.tensor_scatter_nd_add(recovered, indices, x[:, p_idx])

            # Update mask, used to count inserts from overlapping regions
            mask = tf.tensor_scatter_nd_add(mask, indices, ones_patch)

        # Divide by mask to overage overlapping regions
        return recovered/tf.cast(mask, tf.float32)


class DePatchEfficient(DePatch):
    def __init__(self, *args, **kwargs):
        super(DePatchEfficient, self).__init__(*args, **kwargs)

    def call(self, input):
        # Input shape (b, N, u', v', s', t', ch)
        x = input
        in_shape = tf.shape(x)
        b_range = tf.range(in_shape[0])
        ch_range = tf.range(in_shape[-1])

        recovered = tf.zeros((in_shape[0], *self.original_shape))
        mask = tf.zeros((in_shape[0], *self.original_shape),
                        dtype=tf.int32)
        ones_patch = tf.ones((in_shape[0], *self.patch_size_uv, *self.patch_size_st, in_shape[-1]),
                             dtype=tf.int32)

        num_patches_s = self.num_patches_st[0]
        num_patches_t = self.num_patches_st[1]
        num_patches_u = self.num_patches_uv[0]
        num_patches_v = self.num_patches_uv[1]
        num_uv = self.num_uv

        patch_step_s = self.patch_step_st[0]
        patch_step_t = self.patch_step_st[1]
        patch_step_u = self.patch_step_uv[0]
        patch_step_v = self.patch_step_uv[1]

        patch_size_s = self.patch_size_st[0]
        patch_size_t = self.patch_size_st[1]
        patch_size_u = self.patch_size_uv[0]
        patch_size_v = self.patch_size_uv[1]

        s = tf.constant(0)
        cond_s = lambda s, recovered, mask: tf.less(s, num_patches_s)

        def body_s(s, recovered, mask):
            t = tf.constant(0)
            cond_t = lambda s, t, recovered, mask: tf.less(t, num_patches_t)

            def body_t(s, t, recovered, mask):
                u = tf.constant(0)
                cond_u = lambda s, t, u, recovered, mask: tf.less(u, num_patches_u)

                def body_u(s, t, u, recovered, mask):
                    v = tf.constant(0)
                    cond_v = lambda s, t, u, v, recovered, mask: tf.less(v, num_patches_v)

                    def body_v(s, t, u, v, recovered, mask):
                        # Calculate indices conversion
                        p_idx = s*num_patches_t*num_uv + t*num_uv + u*num_patches_v + v
                        u_idx = patch_step_u*u, patch_size_u + patch_step_u*u
                        v_idx = patch_step_v*v, patch_size_v + patch_step_v*v
                        s_idx = patch_step_s*s, patch_size_s + patch_step_s*s
                        t_idx = patch_step_t*t, patch_size_t + patch_step_t*t

                        # Construct indices
                        indices = tf.meshgrid(
                            b_range,  # batch
                            tf.range(*u_idx),  # angular u
                            tf.range(*v_idx),  # angular v
                            tf.range(*s_idx),  # spatial s
                            tf.range(*t_idx),  # spatial t
                            ch_range,  # channel
                            indexing='ij')

                        indices = tf.stack(indices, axis=-1)

                        return (s, t, u, tf.add(v, 1),
                                tf.tensor_scatter_nd_add(recovered, indices, x[:, p_idx]),
                                tf.tensor_scatter_nd_add(mask, indices, ones_patch))

                    s, t, u, v, recovered, mask = tf.while_loop(cond_v, body_v, [s, t, u, v, recovered, mask])
                    return s, t, tf.add(u, 1), recovered, mask

                s, t, u, recovered, mask = tf.while_loop(cond_u, body_u, [s, t, u, recovered, mask])
                return s, tf.add(t, 1), recovered, mask

            s, t, recovered, mask = tf.while_loop(cond_t, body_t, [s, t, recovered, mask])
            return tf.add(s, 1), recovered, mask

        _, recovered, mask = tf.while_loop(cond_s, body_s, [s, recovered, mask])

        # Divide by mask to overage overlapping regions
        return recovered/tf.cast(mask, tf.float32)


def patch(light_fields,
          patch_size_st, patch_size_uv,
          patch_step_st, patch_step_uv) -> Tuple[Tensor, dict]:
    """Patch a batch of light fields with possibly overlapping patches.
    The returned patches are stacked along the batch axis so that the
    resulting dimension is equivalent to the input dimension.

    I.e. the light fields batch
    (b, u, v, s, t, ch)
    is patched into shape
    (b*N, u', v', s', t', ch)
    where N is the number of patches per single light field.

    The patches can possibly overlap in the spatial as well as the angular
    domain depending on the chose patch size and step size.

    Patches can be recovered using :func:`depatch()`

    Notes:
        Care has to be taken specifying the patch size and the step size to
        obtain a full patch from the input. Right now it is only tested with
        even-valued spatial shape and odd-valued angular shape.
        The step size and patch size must be such that the resulting number of
        patches is a true divisor of the light field dimension.

        E.g. a light field batch of shape (b, 9, 9, 32, 32, ch)
        can be patched to (b*N, 5, 5, 8, 8, ch) using

        patch_size_st = [8, 8]
        (with 50% spatial overlap)
        patch_step_st = [p - p//2 for p in patch_size_st]
        patch_size_uv = [5, 5]
        patch_step_uv = [4, 4]
        (since 2 * (5, 5) with (1, 1) overlap -> (9, 9) )

    Args:
        light_fields: Batch of light fields to patch. Shape (b, u, v, s, t, ch)

        patch_size_st: Spatial patch size (s', t')

        patch_size_uv: Angular patch size (u', v')

        patch_step_st: Spatial patch step (s_s, s_t)

        patch_step_uv: Angular patch step (s_u, s_v)

    Returns:
        patches, patch_result
        Tuple of light field patches of shape (b*N, u', v', s', t', ch)
        and result dictionary containing metadata needed for de-patching.

    """

    # Get input shape
    original_shape = light_fields.shape.as_list()
    b, u, v, s, t, ch = original_shape

    # Reshape light field subaperture stack (b, s, t, u*v*ch)
    patches = tf.reshape(tf.transpose(light_fields, (0, 3, 4, 1, 2, 5)), (b, s, t, u*v*ch))

    # Create spatial patches from input images
    patches = extract_patches(patches,
                              sizes=[1, *patch_size_st, 1],
                              strides=[1, *patch_step_st, 1],
                              rates=[1, 1, 1, 1],
                              padding="VALID")

    # Extract number of patches in s- and t-dimension
    _, *num_patches_st, _ = patches.shape.as_list()
    num_patches_st_total = tf.math.reduce_prod(num_patches_st)

    # Reshape (b, n_s, n_t, s_p*t_p*u*v*ch) to (b*n_s*n_t, s_p, t_p, u, v, ch)
    patches = tf.reshape(patches, (b*num_patches_st_total, *patch_size_st, u, v, ch))

    # Transpose and reshape to (b*n_s*n_t, u, v, s_p*t_p*ch)
    patches = tf.transpose(patches, (0, 3, 4, 1, 2, 5))
    patches = tf.reshape(patches, (b*num_patches_st_total, u, v, tf.math.reduce_prod(patch_size_st)*ch))

    # Create angular patches
    patches = extract_patches(patches,
                              sizes=[1, *patch_size_uv, 1],
                              strides=[1, *patch_step_uv, 1],
                              rates=[1, 1, 1, 1],
                              padding="VALID")

    # Extract number of patches in s- and t-dimension
    _, *num_patches_uv, _ = patches.shape.as_list()
    num_patches_uv_total = tf.math.reduce_prod(num_patches_uv)

    # Reshape (b*n_s*n_t, n_u, n_v, u_p*v_p*s_p*t_p*ch) to (b*n_s*n_t*n_u*n_v, u_p, v_p, s_p, t_p, ch)
    patches = tf.reshape(patches, (b*num_patches_st_total*num_patches_uv_total, *patch_size_uv, *patch_size_st, ch))

    patch_res = dict(original_shape=original_shape,
                     patch_size_st=patch_size_st,
                     patch_step_st=patch_step_st,
                     num_patches_st=num_patches_st,
                     num_patches_st_total=num_patches_st_total,
                     patch_size_uv=patch_size_uv,
                     patch_step_uv=patch_step_uv,
                     num_patches_uv=num_patches_uv,
                     num_patches_uv_total=num_patches_uv_total)

    return patches, patch_res


def depatch(patches, patch_result):
    """
    De-patch light field patches obtained with patch()
    into batch of original light fields.
    Overlapping regions are averaged.

    Args:
        patches: Input patches of shape (b*N, u', v', s', t', ch)

        patch_result: Dictionary containing the patch result returned by patch()

    Returns:
        Recovered patches of shape (b, u, v, s, t, ch).
    """
    original_shape = patch_result['original_shape']
    b, u, v, s, t, ch = original_shape
    patch_size_st = patch_result['patch_size_st']
    patch_step_st = patch_result['patch_step_st']
    num_patches_st = patch_result['num_patches_st']
    num_st = patch_result['num_patches_st_total']
    patch_size_uv = patch_result['patch_size_uv']
    patch_step_uv = patch_result['patch_step_uv']
    num_patches_uv = patch_result['num_patches_uv']
    num_uv = patch_result['num_patches_uv_total']

    # Check that patch result is compatible
    n, *patch_shape, ch_patch = patches.shape.as_list()

    # Reshape to separate patch batches
    patches = tf.reshape(patches, (b, num_st*num_uv, *patch_size_uv, *patch_size_st, ch))

    # Init recovered images
    recovered = tf.zeros(original_shape)
    mask = tf.zeros(original_shape, dtype=tf.int32)
    ones_patch = tf.ones((b, *patch_shape, ch), dtype=tf.int32)

    b_range = tf.range(b)
    ch_range = tf.range(ch)

    # Iterate over all patches
    idx = []

    for s, t, u, v in product(
            range(num_patches_st[0]),
            range(num_patches_st[1]),
            range(num_patches_uv[0]),
            range(num_patches_uv[1])):

        # Calculate indices conversion
        p_idx = s*num_patches_st[1]*num_uv + t*num_uv + u*num_patches_uv[1] + v
        u_idx = patch_step_uv[0]*u, patch_shape[0] + patch_step_uv[0]*u
        v_idx = patch_step_uv[1]*v, patch_shape[1] + patch_step_uv[1]*v
        s_idx = patch_step_st[0]*s, patch_shape[2] + patch_step_st[0]*s
        t_idx = patch_step_st[1]*t, patch_shape[3] + patch_step_st[1]*t
        idx.append(p_idx)

        # Construct indices
        indices = tf.meshgrid(
            b_range,  # batch
            tf.range(*u_idx),  # angular u
            tf.range(*v_idx),  # angular v
            tf.range(*s_idx),  # spatial s
            tf.range(*t_idx),  # spatial t
            ch_range,          # channel
            indexing='ij')

        indices = tf.stack(indices, axis=-1)

        # Add sliced image to recovered image indices
        recovered = tf.tensor_scatter_nd_add(recovered, indices, patches[:, p_idx])

        # Update mask, used to count inserts from overlapping regions
        mask = tf.tensor_scatter_nd_add(mask, indices, ones_patch)

    # Divide by mask to overage overlapping regions
    return recovered/tf.cast(mask, tf.float32)
