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

"""Callbacks to schedule regularization parameters of mask layers."""

import os
from pathlib import Path
import subprocess
import tempfile

import matplotlib.pyplot as plt
import numpy as np

from tensorflow.keras.callbacks import Callback


class MaskEntryopyLossScheduler(Callback):
    """Callback that schedules entropy regularization strength."""

    def __init__(self, val_init, val_final, max_epochs):
        super(MaskEntryopyLossScheduler, self).__init__()
        self._alpha = (val_final/val_init)**(1.0/max_epochs)
        self._max_epochs = max_epochs

    def on_epoch_end(self, epoch, logs=None):
        if epoch < self._max_epochs:
            mask_layer = self.model.get_layer(name='mask_layer')
            mask_layer.set_lambda_e(self._alpha * mask_layer.lambda_e)


class MaskEntryopyRelativeLossScheduler(Callback):

    def __init__(self, perc_init, perc_final, max_epochs, offset=0):
        """Callback that schedules entropy regularization strength relative to the main loss.
        That is, the regularization Lagrange multiplier is set, such that

        lambda * L_reg = percentage * main_loss

        where `percentage` is scheduled exponentially.

        Args:
            perc_init: Initial percentage.

            perc_final: Final percentage.

            offset: Number of epochs after which to start the exponential annealing.

            max_epochs: Maximum number of epochs after which the regularization
                        is kept at the constant value `perc_final`.
        """
        super(MaskEntryopyRelativeLossScheduler, self).__init__()

        if offset >= max_epochs:
            raise ValueError("Offset larger than maximum epoch number.")

        self._exp_multiplier = (perc_final/perc_init)**(1.0/(max_epochs - offset))
        self._alpha = perc_init
        self._offset = offset
        self._max_epochs = max_epochs

    def on_epoch_end(self, epoch, logs=None):

        if epoch > self._offset and epoch < self._max_epochs:
            # Retrieve current loss values and weights
            metric_vals = [val.result() for val in self.model.compiled_loss._per_output_metrics]
            weights = [w if w is not None else 1.0 for w in self.model.compiled_loss._loss_weights]

            # Calculate reg multiplier
            lambda_e = self._alpha * sum(w*val for w, val in zip(weights, metric_vals)) / (logs['mask_entropy_loss'])

            mask_layer = self.model.get_layer(name='mask_layer')
            mask_layer.set_lambda_e(lambda_e)

            # Update schedule
            self._alpha *= self._exp_multiplier


class MaskTemperatureScheduler(Callback):
    """Callback that schedules the mask softmax temperature."""

    def __init__(self, val_init, val_final, max_epochs):
        super(MaskTemperatureScheduler, self).__init__()
        self._max_epochs = max_epochs - 1
        self._alpha = (val_final/val_init)**(1.0/self._max_epochs)
        self._val_init = val_init

    def on_train_begin(self, logs=None):
        mask_layer = self.model.get_layer(name='mask_layer')
        mask_layer.set_inv_temp(self._val_init)

    def on_epoch_end(self, epoch, logs=None):
        if epoch < self._max_epochs:
            mask_layer = self.model.get_layer(name='mask_layer')
            mask_layer.set_inv_temp(self._alpha * mask_layer.inv_temp)


class MaskSaveCallback(Callback):

    def __init__(self, run, batchskip: int = 250, filename=None):
        super(MaskSaveCallback, self).__init__()
        self._run = run
        self._masks = []
        self._mask_weights = []
        self._batchskip = batchskip
        self._filename = filename or "mask_history"

        # Get path to FFMPEG either from environment or system
        ffmpeg = None
        for bin in os.environ['PATH'].split(":"):
            ffmpeg_bin = bin + "/ffmpeg"
            if os.path.exists(ffmpeg_bin):
                ffmpeg = ffmpeg_bin
                break
        if ffmpeg is None:
            raise ValueError("FFMPEG not found in environment or system path.")
        print(f"INFO: Found ffmpeg at {ffmpeg}")
        self._ffmpeg = ffmpeg
        return

    def on_batch_end(self, batch, logs=None):
        if not batch % self._batchskip:
            mask_layer = self.model.get_layer(name='mask_layer')
            self._masks.append(mask_layer.get_mask())
            self._mask_weights.append(mask_layer.get_mask_weights())

    def on_train_end(self, logs=None):
        # Save masks to GIF
        with tempfile.TemporaryDirectory() as temp_dir:
            for num, (mask, mask_weight) in enumerate(zip(self._masks, self._mask_weights)):

                num_ch = mask.shape[-1]
                fig, ax = plt.subplots(2, num_ch, sharex=True, sharey=True, figsize=(2*num_ch, 4))
                imkwargs = dict(vmin=0, vmax=1)
                for i in range(num_ch):
                    ax[0, i].imshow(mask[..., i], **imkwargs)
                    ax[1, i].imshow(mask_weight[..., i], **imkwargs)
                    ax[0, i].set_axis_off()
                    ax[1, i].set_axis_off()

                fig.suptitle(f"Iteration {num}")
                plt.tight_layout()
                filename = temp_dir + f"/mask_{num:07d}.png"
                plt.savefig(filename)
                plt.close(fig)

            # Concat figures to MP4
            base_path = Path(temp_dir) / self._filename
            vid_path = base_path.with_suffix(".mp4")
            command = [f"{self._ffmpeg}",
                       "-framerate", "4",           # input framerate
                       "-pattern_type", "glob",
                       "-i", f"{temp_dir}/*.png",
                       "-c:v", "libx264",
                       "-crf", "15",
                       "-pix_fmt", "yuv420p",
                       "-r", "10",                  # Output framerate
                       vid_path]

            subprocess.run(command)
            self._run.add_artifact(vid_path)

            # Also save raw data
            masks = np.asarray(self._masks, dtype=np.bool)
            mask_weights = np.asarray(self._mask_weights, dtype=np.float32)
            masks_path = base_path.with_suffix(".npz")
            np.savez(masks_path, masks=masks, mask_weights=mask_weights)
            self._run.add_artifact(masks_path)
