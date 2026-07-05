from PyQt5.QtCore import QThread, pyqtSignal

from predict import predict_sequence


class PredictWorker(QThread):
    """Runs model inference off the UI thread."""

    finished = pyqtSignal(list)
    failed = pyqtSignal(str)

    def __init__(self, sequence, parent=None):
        super().__init__(parent)
        self.sequence = sequence

    def run(self):
        try:
            result = predict_sequence(self.sequence)
            self.finished.emit(result)
        except Exception as e:
            self.failed.emit(str(e))
