"""
Code from sentdex
"""

from tensorflow.keras.callbacks import TensorBoard
from tensorflow import summary


class ModifiedTensorBoard(TensorBoard):

    # We override init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = summary.create_file_writer(self.log_dir)

    def set_model(self, model):
        """
        Overriding this to stop creating default log writer
        """
        pass

    def on_epoch_end(self, epoch, logs=None):
        """
        Overrided, saves logs with our step number (otherwise every .fit() will start writing from 0th step)
        """
        self.update_stats(**logs)

    def on_batch_end(self, batch, logs=None):
        """
        Overrided, We train for one batch only, no need to save anything at epoch end
        """
        pass

    def on_train_end(self, _):
        """
        Overrided, so we dont close writer
        """
        pass

    def _write_logs(self, logs, index):
        with self.writer.as_default():
            for name, value in logs.items():
                summary.scalar(name, value, step=index)
                self.step += 1
                self.writer.flush()

    def update_stats(self, **stats):
        """
        Custom method for saving metrics - creates writer, writes custom metrics and closes writer
        """
        self._write_logs(stats, self.step)
