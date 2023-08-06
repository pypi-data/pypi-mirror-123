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


"""Sparse tensor coding utilities.
"""

import tensorflow as tf
from tensorflow.keras.backend import epsilon

from lfcnn.layers.layers import soft_threshold


def sparse_tensor_code_fista(y: tf.Tensor,
                             a: tf.Tensor,
                             b: tf.Tensor,
                             c: tf.Tensor,
                             use_mask=False,
                             couple_strength: float = 1e-5,
                             iterations: int = 25,
                             iterations_eigenval: int = 100) -> tf.Tensor:
    """Use the Fast Iterative Shrinkage-Thresholding Algorithm (FISTA)
    by Beck and Teboulle [1].

    [1]: Beck, A. and Teboulle, M.
    "A fast iterative shrinkage-thresholding algorithm for linear inverse problems."
    SIAM Journal on Imaging Sciences 2.1 (2009): 183-202.

    Args:
        y: Input batch of signals to code. Shape (b, N, u, v, s, t, ch)

        a: Angular dictionary to code the signals. Shape (N_uv, u, v)

        b: Spatial dictionary to code the signals. Shape (N_st, s, t)

        c: Spectral dictionary to code the signals. Shape (N_ch, ch)

        use_mask: Whether to apply coding mask for Compressed Sensing reconstruction.
                  The coding mask is extracted from zero values in input y.

        couple_strength: Coupling constant of the ||x||_1 regularizer

        iterations: Numbers of FISTA iterations.

        iterations_eigenval: Numbers of iterations for the Von Mises eigenvalue
                             estimator. See :func:`estimate_eigenval`

    Returns:
        x, shape (b, N, u, v, s, t, ch)
        Sparsely coded coefficients such that || y - Dx ||_2 < eps
    """
    if use_mask:
        # Get coding mask from zero values in input batch
        phi = tf.cast(y > epsilon(),  dtype=tf.float32)

        # Estimate largest eigenvalue of (D^T m^T m D)
        # Since m = diag(phi) and m^2 = m, we use a more efficient approach
        lambda_max = estimate_eigenval_masked_tensor(a, b, c, phi, iterations=iterations_eigenval)

    else:
        # Estimate largest eigenvalue of (D^T D)
        # Because 2*lambda_max is the (smallest) Liptschitz constant of (D^T D) for
        # FISTA in the used minimization case f(x) = ||y - Dx||_2, g(x) = ||x||_1
        lambda_max = estimate_eigenval_tensor(a, b, c, iterations=iterations_eigenval)

    eta = 1.0 / lambda_max
    # y shape (b, N, u, v, s, t, ch)
    x_curr = tf.tensordot(y, a, axes=[[2, 3], [1, 2]])
    # x shape (b, N, s, t, ch, N_uv)
    x_curr = tf.tensordot(x_curr, b, axes=[[2, 3], [1, 2]])
    # x shape (b, N, ch, N_uv, N_st)
    x_curr = tf.tensordot(x_curr, c, axes=[[2], [1]])
    x_curr = soft_threshold(eta*x_curr, couple_strength)
    # x shape (b, N, N_uv, N_st, N_ch)

    y_curr = x_curr
    t_curr = tf.constant(1.0)

    for _ in range(iterations):
        x_prev = x_curr
        t_prev = t_curr

        residual = tf.tensordot(y_curr, c, axes=[[4], [0]])
        residual = tf.tensordot(residual, b, axes=[[3], [0]])
        residual = tf.tensordot(residual, a, axes=[[2], [0]])
        residual = tf.transpose(residual, (0, 1, 5, 6, 3, 4, 2))

        if use_mask:
            residual *= phi

        residual = residual - y

        residual = tf.tensordot(residual, a, axes=[[2, 3], [1, 2]])
        residual = tf.tensordot(residual, b, axes=[[2, 3], [1, 2]])
        residual = tf.tensordot(residual, c, axes=[[2], [1]])
        x_curr = soft_threshold(y_curr - eta*residual, couple_strength / lambda_max)

        # Update t[i+1] <- 0.5*( 1 + sqrt(1 + 4*t[k]^2) )
        t_curr = 0.5*(1 + tf.sqrt(1 + 4*t_curr**2))

        # Update y[i+1] = x[k] + (t[k] - 1)/(t[k+1]) * (x[k] - x[k-1])
        y_curr = x_curr + ((x_curr - x_prev) * (t_prev - 1) / t_curr)

    return x_curr


def estimate_eigenval_tensor(a, b, c, iterations: int = 100):
    """Estimate the largest eigenvalue from tensor product ((abc)^T (abc))
    using the von Mises iteration, also known as the Power Method.
    Args:
        a: Angular dictionary
        b: Spatial dictionary
        c: Spectral dictionary
        iterations: Number of iterations

    Returns:
        lambda_max
        The largest eigenvalue of (x^T x).
    """

    y = tf.random.normal((a.shape[0], b.shape[0], c.shape[0]))

    for i in range(iterations):
        y = tf.tensordot(y, tf.tensordot(a, a, axes=[[1, 2], [1, 2]]), axes=[[0], [0]])
        y = tf.tensordot(y, tf.tensordot(b, b, axes=[[1, 2], [1, 2]]), axes=[[0], [0]])
        y = tf.tensordot(y, tf.tensordot(c, c, axes=[[1], [1]]), axes=[[0], [0]])
        y_norm = tf.norm(y)
        y /= y_norm

    return y_norm


def estimate_eigenval_masked_tensor(a, b, c, phi, iterations: int = 100):
    """Estimate the largest eigenvalue from tensor product ((abc)^T (abc))
    using the von Mises iteration, also known as the Power Method.
    Args:
        a: Angular dictionary
        b: Spatial dictionary
        c: Spectral dictionary
        phi: Tensor mask
        iterations: Number of iterations

    Returns:
        lambda_max
        The largest eigenvalue of (x^T x).
    """
    y = tf.random.normal((tf.shape(phi)[0], phi.shape[1], a.shape[0], b.shape[0], c.shape[0]))

    for i in range(iterations):
        y = tf.tensordot(y, a, axes=[[2], [0]])
        y = tf.tensordot(y, b, axes=[[2], [0]])
        y = tf.tensordot(y, c, axes=[[2], [0]])
        y *= phi
        y = tf.tensordot(y, a, axes=[[2, 3], [1, 2]])
        y = tf.tensordot(y, b, axes=[[2, 3], [1, 2]])
        y = tf.tensordot(y, c, axes=[[2], [1]])
        y_norm = tf.norm(y)
        y /= y_norm

    return y_norm

