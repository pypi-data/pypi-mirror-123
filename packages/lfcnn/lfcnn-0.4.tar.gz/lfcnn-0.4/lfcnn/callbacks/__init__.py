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


"""The LFCNN callbacks module.
"""

from .cyclic_learning import OneCycle
from .cyclic_learning import OneCycleCosine
from .cyclic_learning import OneCycleMomentum
from .cyclic_learning import OneCycleCosineMomentum
from .lr_finder import LearningRateFinder
from .lr_schedules import ExponentialDecay
from .lr_schedules import LinearDecay
from .lr_schedules import PolynomialDecay
from .lr_schedules import SigmoidDecay
from .lr_schedules import StepDecay
from .lr_schedules import StepListDecay
from .lr_schedules import ReduceLROnPlateauRelative
from .sacred import SacredEpochLogger
from .sacred import SacredLearningRateLogger
from .sacred import SacredMetricLogger
from .sacred import SacredTimeLogger
from .sacred import SacredLossWeightLogger


def get(callback: str):
    """Given a callback name, returns an Keras callback instance.

    Args:
        callback: Name of the callback.

    Returns:
        Callback instance.
    """
    # Available callback classes
    classes = {
        "sacredepochlogger": SacredEpochLogger,
        "sacredlearningratelogger": SacredLearningRateLogger,
        "sacredlossweightlogger": SacredLossWeightLogger,
        "sacredmetriclogger": SacredMetricLogger,
        "sacredtimelogger": SacredTimeLogger,
        "exponentialdecay": ExponentialDecay,
        "lineardecay": LinearDecay,
        "polynomialdecay": PolynomialDecay,
        "sigmoiddecay": SigmoidDecay,
        "stepdecay": StepDecay,
        "onecycle": OneCycle,
        "onecyclemomentum": OneCycleMomentum,
        "onecyclecosine": OneCycleCosine,
        "onecyclecosinemomentum": OneCycleCosineMomentum,
        "learningratefinder": LearningRateFinder,
    }
    try:
        return classes[callback.lower()]
    except KeyError:
        raise ValueError(f"Unknown callback '{callback}'.")
