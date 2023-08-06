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

"""Learningrate schedulers to automatically adjust the learning rate during
training.
"""
from typing import List

import numpy as np

from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.callbacks import ReduceLROnPlateau


class StepDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 steps: int,
                 decay: float = 0.5,
                 **kwargs):
        """Learning rate is dropped every steps epochs to
        decay*learning_rate starting with the initial learning rate.
        That is, the learning rate is given by
        ```
        lr = lr_init * decay**N
        ```
        where
        ```
        N = epoch // steps
        ```

        Args:
            lr_init: Initial learning rate.

            steps: Decay learning rate every steps epoch.

            decay: Decay factor.
        """
        super(StepDecay, self).__init__(schedule=self.step_decay, **kwargs)
        self.lr_init = lr_init
        self.steps = steps
        self.decay = decay
        self.name = f"StepDecay, decay {decay}"

    def step_decay(self, epoch: int, lr: float) -> float:
        # Correct epoch index start at 0
        n = epoch // self.steps

        return self.lr_init * self.decay**n


class StepListDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 steps: List[int],
                 decay: float = 0.5,
                 **kwargs):
        """Learning rate is dropped at specified steps to
        decay*learning_rate starting with the initial learning rate.


        Args:
            lr_init: Initial learning rate.

            steps: List of epoch numbers when to drop the learning rate.

            decay: Decay factor.
        """
        super(StepListDecay, self).__init__(schedule=self.step_decay, **kwargs)
        self.lr_init = lr_init
        self.steps = steps
        self.decay = decay
        self.name = f"StepListDecay, decay {decay}"

    def step_decay(self, epoch: int, lr: float) -> float:
        # Count numer of steps smaller than current epoch
        num_steps = len([step for step in self.steps if step <= epoch])
        return self.lr_init * self.decay**num_steps


class PolynomialDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 max_epoch: int,
                 power: int = 2,
                 lr_min: float = 1e-6,
                 **kwargs):
        """Learning rate decays polynomially from initial learning rate
        to minimal learning rate at max_epoch epochs. For epochs larger then
        max_epoch, the learning rate stays constant at lr_min.

        Args:
            lr_init: Initial learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_min.

            power. Polynomial power.

            lr_init: Minimum learning rate.
        """
        super(PolynomialDecay   , self).__init__(schedule=self.polynomial_decay, **kwargs)
        if type(power) != int:
            raise ValueError("Polynomial decay only works with integer powers.")

        self.power = float(power)
        self.e_max = max_epoch
        self.a = (lr_init - lr_min)/((-max_epoch)**self.power)
        self.b = lr_min
        self.name = f"PolynomialDecay, power {power}"

    def polynomial_decay(self, epoch: int, lr: float) -> float:
        return self.a * min(epoch - self.e_max, 0)**self.power + self.b


class LinearDecay(PolynomialDecay):
    def __init__(self,
                 lr_init: float,
                 max_epoch: int,
                 lr_min: float = 1e-6,
                 **kwargs):
        """Learning rate decays linearly. Corresponds to PolynomialDecay
        with power=1.

        Args:
            lr_init: Initial learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_min.

            lr_init: Minimum learning rate.
        """
        super(LinearDecay, self).__init__(
            lr_init=lr_init, lr_min=lr_min, power=1, max_epoch=max_epoch, **kwargs)
        self.name = "LinearDecay"


class ExponentialDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 max_epoch: int,
                 alpha: float = 0.02,
                 lr_min: float = 1e-6,
                 **kwargs):
        """Learning rate decays exponentially from initial learning rate
        to minimal learning rate at max_epoch epoch. For epochs larger then
        max_epoch, the learning rate stays constant at lr_min.

        Args:
            lr_init: Initial learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_min.

            power. Polynomial power.

            lr_init: Minimum learning rate.
        """
        super(ExponentialDecay, self).__init__(schedule=self.exponential_decay, **kwargs)
        self.e_max = max_epoch
        self.alpha = float(alpha)
        self.a = (lr_min - lr_init) / (np.exp(-self.alpha*max_epoch) - 1)
        self.b = lr_init - self.a
        self.name = f"ExponentialDecay, alpha {alpha}"

    def exponential_decay(self, epoch: int, lr: float) -> float:
        return self.a * np.exp(-self.alpha*min(epoch, self.e_max)) + self.b


class SigmoidDecay(LearningRateScheduler):
    def __init__(self,
                 lr_init: float,
                 max_epoch: int,
                 alpha=0.1,
                 offset: int = 0,
                 lr_min: float = 1e-6,
                 **kwargs):
        """Sigmoid decay. The sigmoid function is create symmetrically around
        max_epoch // 2.

        Args:
            lr_init: Initial learning rate.

            max_epoch: Epoch where decay ends. For epochs larger than max_epoch,
                       the learning rate stays constant at lr_min.

            alpha. Decay factor tuning the width of the sigmoid.

            offset: Offset when to start with sigmoid decay.

            lr_init: Minimum learning rate.
        """
        super(SigmoidDecay, self).__init__(schedule=self.sigmoid_decay, **kwargs)
        self.lr_min = lr_min
        self.lr_init = lr_init
        self.alpha = alpha
        self.offset = offset
        center = offset + (max_epoch - offset) // 2
        self.name = f"SigmoidDecay, alpha {alpha}"

        # Initial sigmoid function
        fn = lambda x: (lr_init - lr_min) / (1 + np.exp(alpha*(x - center))) + lr_min
        # Rescale to fit lr_init and lr_final exactly
        # This is necessary due to the asymptotic behaviour of sigmoid(x)
        lr_end = fn(max_epoch)
        self.fn = lambda x: (lr_init - lr_min)/(lr_init - lr_end)*(fn(x) - lr_init) + lr_init

    def sigmoid_decay(self, epoch: int, lr: float) -> float:
        return self.fn(epoch)


class ReduceLROnPlateauRelative(ReduceLROnPlateau):
    """Reduce the learning rate on plateau of monitored loss using a relative
    improvement monitoring.

    This scheduler is basically equivalent to the ReduceLROnPlateau callback
    except that the monitored values are compared relatively rather than
    absolute, using the min_delta value.

    """
    # dynamic_threshold = best*(1 + threshold) in ‘max’ mode or best*(1 - threshold) in min mode.

    def __init__(self, **kwargs):
        super(ReduceLROnPlateauRelative, self).__init__(**kwargs)

    def _reset(self):
        """Set relative thresholding
        """
        super(ReduceLROnPlateauRelative, self)._reset()
        if (self.mode == 'min' or
                (self.mode == 'auto' and 'acc' not in self.monitor)):
            # Use relative threshold value instead of absolute
            self.monitor_op = lambda a, b: np.less(a, b*(1 - self.min_delta))
            self.best = np.Inf
        else:
            # Use relative threshold value instead of absolute
            self.monitor_op = lambda a, b: np.greater(a, b*(1 + self.min_delta))
            self.best = -np.Inf
