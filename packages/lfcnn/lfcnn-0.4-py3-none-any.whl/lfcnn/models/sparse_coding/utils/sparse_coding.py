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


"""Sparse coding utilities.
"""

import tensorflow as tf
from tensorflow.keras.backend import epsilon

from lfcnn.layers.layers import soft_threshold


def sparse_code_fista(y: tf.Tensor,
                      d: tf.Tensor,
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
        y: Input batch of signals to code. Shape (..., N)

        d: Dictionary to code the signals. Shape (N, M)

        use_mask: Whether to apply coding mask for Compressed Sensing reconstruction.
                  The coding mask is extracted from zero values in input y.

        couple_strength: Coupling constant of the ||x||_1 regularizer

        iterations: Numbers of FISTA iterations.

        iterations_eigenval: Numbers of iterations for the Von Mises eigenvalue
                             estimator. See :func:`estimate_eigenval`

    Returns:
        x, shape (..., M)
        Sparsely coded coefficients such that || y - Dx ||_2 < eps
    """
    if use_mask:
        # Get coding mask from zero values in input batch
        phi = tf.cast(y > epsilon(),  dtype=tf.float32)

        # Estimate largest eigenvalue of (D^T m^T m D)
        # Because 2*lambda_max is the (smallest) Liptschitz constant of (D^T D) for
        # FISTA in the used minimization case f(x) = ||y - mDx||_2, g(x) = ||x||_1
        # Since m = diag(phi) and m^2 = m, we use a more efficient approach
        lambda_max = estimate_eigenval_xtphix(d, phi, iterations=iterations_eigenval)
        eta = 1.0 / lambda_max
        x_curr = soft_threshold(eta*tf.matmul(phi*y, d), couple_strength)

    else:
        # Estimate largest eigenvalue of (D^T D)
        # Because 2*lambda_max is the (smallest) Liptschitz constant of (D^T D) for
        # FISTA in the used minimization case f(x) = ||y - Dx||_2, g(x) = ||x||_1
        lambda_max = estimate_eigenval_xtx(d, iterations=iterations_eigenval)
        eta = 1.0 / lambda_max
        x_curr = soft_threshold(eta*tf.matmul(y, d), couple_strength)

    y_curr = x_curr
    t_curr = tf.constant(1.0)

    for _ in range(iterations):
        x_prev = x_curr
        t_prev = t_curr

        residual = tf.matmul(y_curr, d, transpose_b=True)

        if use_mask:
            residual *= phi

        residual = residual - y

        x_curr = soft_threshold(y_curr - eta*tf.matmul(residual, d), couple_strength / lambda_max)

        # Update t[i+1] <- 0.5*( 1 + sqrt(1 + 4*t[k]^2) )
        t_curr = 0.5*(1 + tf.sqrt(1 + 4*t_curr**2))

        # Update y[i+1] = x[k] + (t[k] - 1)/(t[k+1]) * (x[k] - x[k-1])
        y_curr = x_curr + ((x_curr - x_prev) * (t_prev - 1) / t_curr)

    return x_curr


def estimate_eigenval_xtx(x, iterations: int = 100):
    """Estimate the largest eigenvalue from matrix (x^T x) using the von Mises
    iteration, also known as the Power Method.

    This is more memory efficient since (x^T x), which may become very large,
    is never calculated directly.

    Args:
        x: Matrix x
        iterations: Number of iterations

    Returns:
        lambda_max
        The largest eigenvalue of (x^T x).
    """
    y = tf.random.normal((1, x.shape[1]))

    for i in range(iterations):
        y = tf.matmul(y, x, transpose_b=True)  # = Xy
        y = tf.matmul(y, x)                    # = X^T(Xy)
        y_norm = tf.norm(y)
        y /= y_norm

    return y_norm


def estimate_eigenval_xtphix(x, phi, iterations: int = 100):
    """Estimate the largest eigenvalue from matrix (x^T diag(phi) x) using the
    von Mises iteration, also known as the Power Method.

    This is more memory efficient since (x^T diag(phi) x), which may become very large,
    is never calculated directly.

    Args:
        x: Matrix x
        iterations: Number of iterations

    Returns:
        lambda_max
        The largest eigenvalue of (x^T x).
    """
    y = tf.random.normal((1, x.shape[1]))

    for i in range(iterations):
        y = tf.matmul(y, x, transpose_b=True)  # = Xy
        y *= phi                               # = phi*(Xy)
        y = tf.matmul(y, x)                    # = X^T(phi*Xy)
        y_norm = tf.norm(y)
        y /= y_norm

    return y_norm
