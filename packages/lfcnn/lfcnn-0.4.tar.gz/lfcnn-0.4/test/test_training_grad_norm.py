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


"""Test lfcnn.models.custom_training
"""
# Set CPU as device:
from lfcnn.utils.tf_utils import use_cpu
use_cpu()

from pytest import raises, approx

import numpy as np

from tensorflow.keras.backend import clear_session
from tensorflow.keras import optimizers
from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D

from lfcnn.losses import MAE
from lfcnn.metrics import get_central_metrics_small
from lfcnn.metrics import get_disparity_metrics
from lfcnn.models import BaseModel
from lfcnn.training import GradNorm

from lfcnn.generators import CentralAndDisparityGenerator
from lfcnn.generators.reshapes import lf_subaperture_stack


class MockMultiTaskModel(BaseModel):

    def __init__(self, **kwargs):
        super(MockMultiTaskModel, self).__init__(**kwargs)

    def set_generator_and_reshape(self):
        self._generator = CentralAndDisparityGenerator
        self._reshape_func = lf_subaperture_stack
        return

    def create_model(self, inputs, augmented_shape=None):
        """Create simple multi-task model"""
        # Single input model
        input = inputs[0]
        x = Conv2D(filters=3, kernel_size=(3, 3), name='last_shared', padding='same')(input)
        out_1 = Conv2D(filters=3, kernel_size=(3, 3), padding='same', name="central_view")(x)
        out_2 = Conv2D(filters=1, kernel_size=(3, 3), padding='same', name="disparity")(x)

        return Model(inputs, [out_1, out_2], name="MockMultiTaskModel")


def get_model_kwargs():
    optimizer = optimizers.SGD(learning_rate=0.1)

    loss = dict(central_view=MAE(), disparity=MAE())
    metrics = dict(central_view=get_central_metrics_small(), disparity=get_disparity_metrics())
    callbacks = []
    model_cls = GradNorm
    model_cls_kwargs = dict(alpha=1.0, min_val=1e-3)

    model_kwargs = dict(
        optimizer=optimizer,
        loss=loss,
        metrics=metrics,
        callbacks=callbacks,
        model_cls=model_cls,
        model_cls_kwargs=model_cls_kwargs
    )

    return model_kwargs


def get_train_kwargs(generated_shape,
                     input_shape=(9, 9, 36, 36, 3),
                     augmented_shape=(9, 9, 32, 32, 3)):

    dat = np.random.rand(8, *input_shape)
    lbl = np.random.rand(8, *input_shape[2:4], 1)
    data = dict(data=dat, disp=lbl)

    dat = np.random.rand(8, *input_shape)
    lbl = np.random.rand(8, *input_shape[2:4], 1)
    valid_data = dict(data=dat, disp=lbl)

    train_kwargs = dict(data=data,
                        valid_data=valid_data,
                        data_key="data",
                        label_keys="disp",
                        augmented_shape=augmented_shape,
                        generated_shape=generated_shape,
                        batch_size=2,
                        epochs=1,
                        verbose=0
                        )

    return train_kwargs


def get_test_kwargs(generated_shape,
                    input_shape=(9, 9, 36, 36, 3),
                    augmented_shape=(9, 9, 32, 32, 3)):

    dat = np.random.rand(8, *input_shape)
    lbl = np.random.rand(8, *input_shape[2:4], 1)
    data = dict(data=dat, disp=lbl)

    test_kwargs = dict(data=data,
                       data_key="data",
                       label_keys="disp",
                       augmented_shape=augmented_shape,
                       generated_shape=generated_shape,
                       batch_size=1,
                       verbose=0
                       )

    return test_kwargs


def get_eval_kwargs(generated_shape,
                    input_shape=(9, 9, 64, 64, 3),
                    augmented_shape=(9, 9, 64, 64, 3)):

    dat = np.random.rand(8, *input_shape)
    lbl = np.random.rand(8, *input_shape[2:4], 1)
    data = dict(data=dat, disp=lbl)

    eval__kwargs = dict(data=data,
                        data_key="data",
                        label_keys="disp",
                        augmented_shape=augmented_shape,
                        generated_shape=generated_shape,
                        batch_size=1,
                        verbose=0
                        )

    return eval__kwargs


def test_model_build():

    model_kwargs = get_model_kwargs()
    model = MockMultiTaskModel(**model_kwargs)

    assert model.keras_model is None

    generated_shape = [(32, 32, 9*9*3)]
    model.__build_model__(generated_shape, (9, 9, 32, 32, 3), gpus=1, cpu_merge=False)

    assert isinstance(model.keras_model, GradNorm)
    assert model.keras_model.name == "MockMultiTaskModel"
    assert isinstance(model.optimizer, optimizers.SGD)
    assert isinstance(model.loss['central_view'], MAE)
    assert isinstance(model.loss['disparity'], MAE)
    clear_session()

    model = MockMultiTaskModel(**model_kwargs)
    train_kwargs = get_train_kwargs(generated_shape)
    model.train(**train_kwargs)

    loss_weights = model.keras_model.loss_weights
    print(loss_weights)
    for weight in loss_weights:
        assert "loss_weight" in weight.name
        # Check that weights have been updated
        assert weight.numpy() < 0.5 or weight.numpy() > 0.5
        # Check that weights are within constraint
        assert weight.numpy() > 1e-3 and weight.numpy() <= 1.0

    # Check that weights sum to one
    approx(1.0, np.sum([val.numpy() for val in loss_weights]))

    test_kwargs = get_test_kwargs(generated_shape)
    model.test(**test_kwargs)

    generated_shape = [(64, 64, 9*9*3)]
    eval_kwargs = get_eval_kwargs(generated_shape)
    model.evaluate_challenges(**eval_kwargs)

    return
