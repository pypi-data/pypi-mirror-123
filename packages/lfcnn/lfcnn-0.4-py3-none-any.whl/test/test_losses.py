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


"""Test lfcnn.losses
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

from pytest import approx

from tensorflow import convert_to_tensor
import tensorflow.keras.backend as K
import numpy as np

from lfcnn import losses

ALL_LOSSES = [losses.dummy,
              losses.mean_absolute_error,
              losses.mean_squared_error,
              losses.huber_loss,
              losses.pseudo_huber_loss,
              losses.total_variation,
              losses.psnr, losses.psnr_clipped,
              losses.cosine_proximity, losses.normalized_cosine_proximity,
              losses.spectral_information_divergence,
              losses.bad_pix_01, losses.bad_pix_03, losses.bad_pix_07]

SSIM_LOSSES = [losses.structural_similarity,
               losses.normalized_structural_similarity,
               losses.multiscale_structural_similarity,
               losses.normalized_multiscale_structural_similarity]

LF_LOSSES = [losses.mean_absolute_error,
             losses.mean_squared_error,
             losses.huber_loss,
             losses.pseudo_huber_loss,
             losses.psnr, losses.psnr_clipped,
             losses.cosine_proximity, losses.normalized_cosine_proximity,
             losses.spectral_information_divergence]


def test_shape_ssim():
    """Test that all losses return a single float value (reduce batch mean)
    """
    # MS SSIM needs larger shape
    for shape in [(10, 256, 256, 3), (10, 256, 256, 1)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for loss in SSIM_LOSSES:
            res = loss(y_true, y_pred)
            # Always returns batch size list of floats
            assert res.ndim == 1


def test_shape_images():
    """Test that all losses return a single float value (reduce batch mean)
    """
    for shape in [(10, 5, 5, 1), (10, 5, 5, 3)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for loss in ALL_LOSSES:
            res = loss(y_true, y_pred)
            # Always returns batch size list of floats
            assert res.ndim == 1


def test_shape_lightfield():
    """Test that all losses return a single float value (reduce batch mean)
    """
    for shape in [(10, 9, 9, 5, 5, 3), (10, 9, 5, 5, 3)]:
        y_true = K.variable(np.random.random(shape))
        y_pred = K.variable(np.random.random(shape))
        for loss in LF_LOSSES:
            res = loss(y_true, y_pred)
            # Always returns batch size list of floats
            assert res.ndim == 1


def test_mae():
    loss_inst = losses.MeanAbsoluteError()
    loss = losses.mean_absolute_error

    # Identical true, pred
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy()

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0 for _ in range(10)]))

    # Opposite true, pred
    y_true = np.ones((10, 3, 3, 7))
    y_pred = np.zeros((10, 3, 3, 7))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([1.0 for _ in range(10)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([1.0 for _ in range(10)]))

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([0, 1]))

    return


def test_mse():
    loss_inst = losses.MeanSquaredError()
    loss = losses.mean_squared_error

    # Identical true, pred
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy()

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0 for _ in range(10)]))

    # Opposite true, pred
    y_true = np.ones((10, 3, 3, 7))
    y_pred = np.zeros((10, 3, 3, 7))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([1.0 for _ in range(10)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([1.0 for _ in range(10)]))

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([0, 1]))

    return


def test_huber():
    for ver in ['fcnn', 'keras']:
        delta = 1
        loss_inst = losses.Huber(delta=delta, ver=ver)
        loss = losses.huber_loss

        # Identical true, pred
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = y_true.copy()

        y_true = convert_to_tensor(y_true)
        y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0 for _ in range(10)]))

    # Test Keras compatible version
    delta = 1
    loss_inst = losses.Huber(delta=delta, ver='keras')
    loss = losses.huber_loss

    # Opposite true, pred
    y_true = np.ones((10, 3, 3, 7))
    y_pred = np.zeros((10, 3, 3, 7))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred, ver='keras')), np.asarray([0.5 for _ in range(10)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0.5 for _ in range(10)]))

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred, ver='keras')), np.asarray([0, 0.5]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0, 0.5]))

    # Test scaled version
    delta = 1
    loss_inst = losses.Huber(delta=delta)
    loss = losses.huber_loss

    # Opposite true, pred
    y_true = np.ones((10, 3, 3, 7))
    y_pred = np.zeros((10, 3, 3, 7))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([1.0 for _ in range(10)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([1.0 for _ in range(10)]))

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([0, 1]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0, 1]))

    return


def test_pseudo_huber():
    for ver in ['lfcnn', 'keras']:
        delta = 1
        loss_inst = losses.PseudoHuber(delta=delta, ver=ver)
        loss = losses.pseudo_huber_loss

        # Identical true, pred
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = y_true.copy()

        y_true = convert_to_tensor(y_true)
        y_pred = convert_to_tensor(y_pred)
        abs = 1e-4
        assert np.allclose(K.eval(loss(y_true, y_pred, ver=ver)), np.asarray([0 for _ in range(10)]), atol=abs)
        assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0 for _ in range(10)]), atol=abs)

    delta = 1
    loss_inst = losses.PseudoHuber(delta=delta, ver='keras')
    loss = losses.pseudo_huber_loss

    # Opposite true, pred
    y_true = convert_to_tensor(np.ones((10, 3, 3, 7)))
    y_pred = convert_to_tensor(np.zeros((10, 3, 3, 7)))

    assert np.allclose(K.eval(loss(y_true, y_pred, ver='keras')), np.asarray([0.4142 for _ in range(10)]), atol=abs)
    assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([0.4142 for _ in range(10)]), atol=abs)

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred, ver='keras')), np.asarray([0, 0.4142]), atol=abs)
    assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([0, 0.4142]), atol=abs)

    delta = 1
    loss_inst = losses.PseudoHuber(delta=delta, ver='lfcnn')
    loss = losses.pseudo_huber_loss

    # Opposite true, pred
    y_true = convert_to_tensor(np.ones((10, 3, 3, 7)))
    y_pred = convert_to_tensor(np.zeros((10, 3, 3, 7)))

    assert np.allclose(K.eval(loss(y_true, y_pred, ver='lfcnn')), np.asarray([2*0.4142 for _ in range(10)]), atol=abs)
    assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([2*0.4142 for _ in range(10)]), atol=abs)

    # 2 batches, one identical, one opposite
    y_true = np.zeros((2, 1, 1, 1))
    y_true[1, ...] = 1
    y_pred = np.zeros((2, 1, 1, 1))

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred, ver='lfcnn')), np.asarray([0, 2*0.4142]), atol=abs)
    assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([0, 2*0.4142]), atol=abs)

    return


def test_total_variation():
    loss_inst = losses.TotalVariation()
    loss = losses.total_variation

    # y_true is ignored
    y_true = K.variable(np.random.rand(10, 3, 3, 3))

    for c in [0, 0.25, 0.5, 1]:
        y = K.variable(c*np.ones((10, 3, 3, 3)))
        assert np.array_equal(K.eval(loss(y_true, y)), np.asarray([0 for _ in range(10)]))
        assert np.array_equal(K.eval(loss_inst.call(y_true, y)), np.asarray([0 for _ in range(10)]))

    y = np.zeros((5, 10, 10, 1))
    y[:, 5:, 5:] = 1
    y = K.variable(y)
    assert np.array_equal(K.eval(loss(y_true, y)), np.asarray([10 for _ in range(5)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y)), np.asarray([10 for _ in range(5)]))

    y = np.zeros((10, 10, 3))
    y[5:, 5:, :] = 1
    y = K.variable(y)
    assert np.array_equal(K.eval(loss(y_true, y)), np.asarray(30))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y)), np.asarray(30))

    y = np.zeros((5, 10, 10, 3))
    y[:, 5:, 5:, :] = 1
    y = K.variable(y)
    assert np.array_equal(K.eval(loss(y_true, y)), np.asarray([30 for _ in range(5)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y)), np.asarray([30 for _ in range(5)]))

    return


def test_cosine_proximity():

    loss_inst = losses.CosineProximity()
    loss = losses.cosine_proximity

    # Identical true, pred, scaling invariant, 0 degrees
    for c in [0.5, 1, 1.5]:
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = c*y_true.copy()

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)
        assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([1 for _ in range(10)]))
        assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([1 for _ in range(10)]))

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]))
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([0 for _ in range(10)]))

    # 45 degrees true, pred
    y_true = np.asarray([1, 0])
    y_true = np.stack([y_true for _ in range(10)], axis=0)
    y_pred = np.asarray([1, 1])
    y_pred = np.stack([y_pred for _ in range(10)], axis=0)

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), [np.cos(0.25*np.pi) for _ in range(10)])
    assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), [np.cos(0.25*np.pi) for _ in range(10)])

    return


def test_normalized_cosine_proximity():

    loss_inst = losses.NormalizedCosineProximity()
    loss = losses.normalized_cosine_proximity
    abs = 1e-4
    # Identical true, pred, scaling invariant, 0 degrees
    for c in [0.5, 1, 1.5]:
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = c*y_true.copy()

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)
        assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]), atol=abs)
        assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0 for _ in range(10)]), atol=abs)

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([0.5 for _ in range(10)]), atol=abs)
    assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)),  np.asarray([0.5 for _ in range(10)]), atol=abs)

    # Identical true, pred, scaling invariant, 180 degrees
    for c in [-0.5, -1, -1.5]:
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = c*y_true.copy()

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)
        assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([1.0 for _ in range(10)]), atol=abs)
        assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([1.0 for _ in range(10)]), atol=abs)

    return


def test_spectral_information_divergence():

    loss_inst = losses.SpectralInformationDivergence()
    loss = losses.spectral_information_divergence

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))
    abs = 1e-4
    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]), atol=abs)
    assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([0 for _ in range(10)]), atol=abs)


    # Identical true, pred, scaling invariant, 0 degrees
    for c in [0.25, 0.5, 1]:
        y_true = np.random.rand(10, 3, 3, 7)
        y_pred = c*y_true.copy()

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)
        assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]), atol=abs)
        assert np.allclose(K.eval(loss_inst.call(y_true, y_pred)), np.asarray([0 for _ in range(10)]), atol=abs)

    return


def test_psnr():
    loss = losses.psnr

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]), atol=1e-3)

    # 20 dB
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy() - 0.1

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([20 for _ in range(10)]), atol=1e-2)

    # 40 dB
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy() - 0.01

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([40 for _ in range(10)]), atol=1e-2)

    # 60 dB
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy() - 0.001

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([60 for _ in range(10)]), atol=0.5)

    return


def test_psnr_clipped():
    loss = losses.psnr_clipped

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), np.asarray([0 for _ in range(10)]), atol=1e-4)

    # 20 dB
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy() - 0.1

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), K.eval(losses.psnr(y_true, K.clip(y_pred, 0, 1))), atol=1e-4)

    return


def test_mae_clipped():
    loss = losses.mae_clipped

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), [1 for _ in range(10)], atol=1e-4)

    # Identical true, pred, 90 degrees
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy()

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), [0 for _ in range(10)], atol=1e-4)

    # Random
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = np.random.rand(10, 3, 3, 7)

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), K.eval(losses.mae(y_true, K.clip(y_pred, 0, 1))))

    return


def test_mse_clipped():
    loss = losses.mse_clipped

    # Opposite true, pred, 90 degrees
    y_true = np.zeros((10, 3, 3, 7))
    y_pred = np.ones((10, 3, 3, 7))

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), [1 for _ in range(10)], atol=1e-4)

    # Identical true, pred, 90 degrees
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = y_true.copy()

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), [0 for _ in range(10)], atol=1e-4)

    # Random
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = np.random.rand(10, 3, 3, 7)

    y_true = K.variable(y_true)
    y_pred = K.variable(y_pred)
    assert np.allclose(K.eval(loss(y_true, y_pred)), K.eval(losses.mse(y_true, K.clip(y_pred, 0, 1))))

    return


def test_bad_pix():

    for c in [0, 0.011, 0.033, 0.077]:
        # Identical values, manipulate singles
        y_true = np.random.rand(5, 10, 10)
        y_pred = y_true.copy()
        y_pred[0, 0, 0] += c

        y_pred[1, 0, 0] += c
        y_pred[1, 1, 0] += c

        y_pred[2, 0, 0] += c
        y_pred[2, 1, 0] += c
        y_pred[2, 0, 1] += c

        y_pred[3, 0, 0] += c
        y_pred[3, 0, 1] += c
        y_pred[3, 1, 0] += c
        y_pred[3, 1, 1] += c

        y_pred[4, 0, 0] += c
        y_pred[4, 0, 1] += c
        y_pred[4, 1, 0] += c
        y_pred[4, 1, 1] += c
        y_pred[4, 2, 0] += c

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)

        if c > 0.01:
            assert np.allclose(K.eval(losses.bad_pix_01(y_true, y_pred)), [(i + 1)*1.0 for i in range(5)])
        else:
            assert np.allclose(K.eval(losses.bad_pix_01(y_true, y_pred)), [0.0 for _ in range(5)])
        if c > 0.03:
            assert np.allclose(K.eval(losses.bad_pix_03(y_true, y_pred)), [(i + 1)*1.0 for i in range(5)])
        else:
            assert np.allclose(K.eval(losses.bad_pix_03(y_true, y_pred)), [0.0 for _ in range(5)])
        if c > 0.07:
            assert np.allclose(K.eval(losses.bad_pix_07(y_true, y_pred)), [(i + 1)*1.0 for i in range(5)])
        else:
            assert np.allclose(K.eval(losses.bad_pix_07(y_true, y_pred)), [0.0 for _ in range(5)])

        y_true = np.random.rand(1, 10, 10)
        y_pred = y_true.copy()
        y_pred += c

        y_true = K.variable(y_true)
        y_pred = K.variable(y_pred)

        if c > 0.01:
            assert np.allclose(K.eval(losses.bad_pix_01(y_true, y_pred)), [100.0])
        else:
            assert np.allclose(K.eval(losses.bad_pix_01(y_true, y_pred)), [0.0])
        if c > 0.03:
            assert np.allclose(K.eval(losses.bad_pix_03(y_true, y_pred)), [100.0])
        else:
            assert np.allclose(K.eval(losses.bad_pix_03(y_true, y_pred)), [0.0])
        if c > 0.07:
            assert np.allclose(K.eval(losses.bad_pix_07(y_true, y_pred)), [100.0])
        else:
            assert np.allclose(K.eval(losses.bad_pix_07(y_true, y_pred)), [0.0])

    return


def test_dummy():
    loss_inst = losses.Dummy()
    loss = losses.dummy

    # Identical true, pred
    y_true = np.random.rand(10, 3, 3, 7)
    y_pred = np.random.rand(10, 3, 3, 7)

    y_true = convert_to_tensor(y_true)
    y_pred = convert_to_tensor(y_pred)
    assert np.array_equal(K.eval(loss(y_true, y_pred)), [1.0 for _ in range(10)])
    assert np.array_equal(K.eval(loss_inst.call(y_true, y_pred)), [1.0 for _ in range(10)])

    return
