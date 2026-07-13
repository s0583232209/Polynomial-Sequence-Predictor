from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import predict
from gui.graph_canvas import GraphCanvas
from gui.predict_worker import PredictWorker
from gui.styles import (
    CORAL,
    OUTPUT_DEFAULT_STYLE,
    OUTPUT_ERROR_STYLE,
    OUTPUT_LOADING_STYLE,
    OUTPUT_RESULT_STYLE,
)

# Number of values expected as model input and output.
INPUT_COUNT = 8
OUTPUT_COUNT = 3

# Unicode subscript characters used for sequence indices.
SUBSCRIPTS = "₀₁₂₃₄₅₆₇₈₉"

# Example polynomial sequence used for demonstration.
EXAMPLE_SEQUENCE = [5, 8, 13, 20, 29, 40, 53, 68]


def subscript(n: int) -> str:
    """Convert an integer into its Unicode subscript representation."""
    return "".join(SUBSCRIPTS[int(d)] for d in str(n))


def format_value(value: float) -> str:
    """Format prediction values for display.

    Values that are sufficiently close to integers are rounded to
    improve readability.
    """
    if abs(value - round(value)) < 0.05:
        return str(round(value))
    return f"{value:.1f}"


class MainWindow(QMainWindow):
    """Main application window for the PolySeqNet graphical interface."""

    def __init__(self):
        super().__init__()

        # Configure the main window.
        self.setWindowTitle("PolySeqNet — Polynomial Sequence Predictor")
        self.setMinimumSize(1400, 820)
        self.resize(1500, 900)

        # Store references to dynamically created widgets.
        self.input_fields: list[QLineEdit] = []
        self.output_labels: list[QLabel] = []

        # Background worker used for model prediction.
        self.worker: PredictWorker | None = None

        self._build_ui()
        self._refresh_model_status()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        """Build the main window layout."""

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(24, 20, 24, 12)
        root.setSpacing(16)

        # Header section.
        root.addWidget(self._build_header())

        # Main content area.
        body = QHBoxLayout()
        body.setSpacing(20)

        body.addWidget(self._build_input_card(), 2)
        body.addWidget(self._build_output_card(), 1)

        root.addLayout(body, 1)

        # Sequence visualization.
        graph_card = self._build_graph_card()
        graph_card.setMaximumHeight(190)
        root.addWidget(graph_card, 0)

        # Status bar displayed at the bottom of the window.
        self.status = self.statusBar()
        self.status.showMessage("Ready.")

    def _build_header(self) -> QWidget:
        """Create the application header."""

        header = QWidget()

        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Application title.
        title = QLabel(f'<span style="color:{CORAL};">∑</span>&nbsp;&nbsp;PolySeqNet')
        title.setObjectName("titleLabel")

        # Short description shown below the title.
        subtitle = QLabel(
            "Enter 8 consecutive terms of an integer polynomial sequence "
            "to predict the next 3."
        )
        subtitle.setObjectName("subtitleLabel")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        return header

    def _build_input_card(self) -> QFrame:
        """Create the input panel containing the sequence fields and controls."""

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)
        layout.addStretch()

        label = QLabel("INPUT SEQUENCE")
        label.setObjectName("sectionLabelInput")
        layout.addWidget(label)

        # Grid containing the eight sequence input fields.
        grid = QGridLayout()
        grid.setSpacing(18)

        # Accept floating-point values only.
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

        self.input_fields = []

        for i in range(INPUT_COUNT):

            # Create one labeled input field.
            col_wrap = QVBoxLayout()
            col_wrap.setSpacing(6)

            idx_label = QLabel(f"a{subscript(i)}")
            idx_label.setObjectName("fieldIndexInput")
            idx_label.setAlignment(Qt.AlignCenter)

            field = QLineEdit()
            field.setValidator(validator)
            field.setAlignment(Qt.AlignCenter)
            field.setFixedSize(150, 84)

            # Pressing Enter starts the prediction.
            field.returnPressed.connect(self._on_predict_clicked)

            col_wrap.addWidget(idx_label)
            col_wrap.addWidget(field)

            # Arrange fields in a 2×4 grid.
            row, col = divmod(i, 4)

            wrapper = QWidget()
            wrapper.setLayout(col_wrap)

            grid.addWidget(wrapper, row, col)

            self.input_fields.append(field)

        layout.addLayout(grid)

        # ------------------------------------------------------------------
        # Action buttons
        # ------------------------------------------------------------------

        buttons = QHBoxLayout()
        buttons.setSpacing(12)

        predict_btn = QPushButton("Predict  ▶")
        predict_btn.setObjectName("predictButton")
        predict_btn.clicked.connect(self._on_predict_clicked)

        self.predict_button = predict_btn

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self._on_clear_clicked)

        buttons.addWidget(predict_btn)
        buttons.addWidget(clear_btn)

        layout.addLayout(buttons)

        # Load a predefined example sequence.
        example_btn = QPushButton("Load example sequence")
        example_btn.setObjectName("linkButton")
        example_btn.setCursor(Qt.PointingHandCursor)
        example_btn.clicked.connect(self._on_load_example)

        layout.addWidget(example_btn, alignment=Qt.AlignLeft)

        # Display the current model status.
        self.model_status_label = QLabel("")
        self.model_status_label.setObjectName("subtitleLabel")
        layout.addWidget(self.model_status_label)

        layout.addStretch()

        return card

    def _build_output_card(self) -> QFrame:
        """Create the output panel displaying the predicted values."""

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)
        layout.addStretch()

        label = QLabel("PREDICTED CONTINUATION")
        label.setObjectName("sectionLabelOutput")
        layout.addWidget(label)

        # Vertical layout containing the prediction labels.
        row = QVBoxLayout()
        row.setSpacing(18)

        self.output_labels = []

        for i in range(OUTPUT_COUNT):

            # Create one output field for each predicted value.
            col_wrap = QVBoxLayout()
            col_wrap.setSpacing(6)

            idx_label = QLabel(f"a{subscript(INPUT_COUNT + i)}")
            idx_label.setObjectName("fieldIndexOutput")
            idx_label.setAlignment(Qt.AlignCenter)

            value_label = QLabel("—")
            value_label.setAlignment(Qt.AlignCenter)
            # Configure the appearance of the output value label.
            value_label.setFixedSize(150, 84)
            value_label.setStyleSheet(OUTPUT_DEFAULT_STYLE)

            # Assemble one prediction column.
            col_wrap.addWidget(idx_label)
            col_wrap.addWidget(value_label)

            wrapper = QWidget()
            wrapper.setLayout(col_wrap)
            row.addWidget(wrapper)

            self.output_labels.append(value_label)

        layout.addLayout(row)
        layout.addStretch()
        return card

    def _build_graph_card(self) -> QFrame:
        """Create the graph panel used to visualize the sequence."""
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)

        # Create the embedded matplotlib canvas.
        self.canvas = GraphCanvas(card)
        layout.addWidget(self.canvas)
        return card

    # ------------------------------------------------------------------
    # State helpers
    # ------------------------------------------------------------------

    def _refresh_model_status(self):
        """Update the UI based on whether a trained model is available."""
        if predict.model_available():
            self.model_status_label.setText("Model: loaded from best_model.pth")
            self.predict_button.setEnabled(True)
        else:
            self.model_status_label.setText(
                "Model not found — train the model first (best_model.pth missing)."
            )
            self.predict_button.setEnabled(False)

    def _read_input_sequence(self) -> list[float] | None:
        """Read and validate the sequence entered by the user."""
        values = []

        # Validate each input field.
        for i, field in enumerate(self.input_fields):
            text = field.text().strip()

            if not text:
                QMessageBox.warning(
                    self,
                    "Missing value",
                    f"Please fill in field a{subscript(i)}.",
                )
                return None

            try:
                values.append(float(text))
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid value",
                    f"'{text}' in field a{subscript(i)} is not a valid number.",
                )
                return None

        return values

    def _set_output_state(self, state: str, values=None):
        """Update the prediction display according to the current application state."""
        style_map = {
            "default": OUTPUT_DEFAULT_STYLE,
            "loading": OUTPUT_LOADING_STYLE,
            "result": OUTPUT_RESULT_STYLE,
            "error": OUTPUT_ERROR_STYLE,
        }

        style = style_map[state]

        # Apply the selected state to every output label.
        for i, label in enumerate(self.output_labels):
            label.setStyleSheet(style)

            if state == "default":
                label.setText("—")
            elif state == "loading":
                label.setText("…")
            elif state == "result" and values is not None:
                label.setText(format_value(values[i]))
            elif state == "error":
                label.setText("!")

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _on_predict_clicked(self):
        """Start a prediction if no prediction is currently running."""

        # Prevent multiple concurrent prediction requests.
        if self.worker is not None and self.worker.isRunning():
            return

        sequence = self._read_input_sequence()
        if sequence is None:
            return

        # Display the input sequence before prediction.
        self.canvas.plot_sequence(sequence)
        self._set_output_state("loading")
        self.predict_button.setEnabled(False)
        self.status.showMessage("Predicting…")

        # Run the prediction in a background thread.
        self.worker = PredictWorker(sequence)
        self.worker.finished.connect(
            lambda result: self._on_predict_finished(sequence, result)
        )
        self.worker.failed.connect(self._on_predict_failed)
        self.worker.start()

    def _on_predict_finished(self, sequence, result):
        """Handle a successful prediction."""
        self.predict_button.setEnabled(True)
        self._set_output_state("result", result)

        # Display both the input and the predicted continuation.
        self.canvas.plot_sequence(sequence, result)

        self.status.showMessage("Prediction complete.", 5000)

    def _on_predict_failed(self, message: str):
        """Handle prediction failures."""
        self.predict_button.setEnabled(True)
        self._set_output_state("error")
        self.status.showMessage(f"Error: {message}", 8000)

        QMessageBox.critical(self, "Prediction failed", message)

    def _on_clear_clicked(self):
        """Reset the interface to its initial state."""

        # Clear all user input.
        for field in self.input_fields:
            field.clear()

        self._set_output_state("default")
        self.canvas.clear_plot()
        self.status.showMessage("Cleared.", 3000)

    def _on_load_example(self):
        """Load the predefined example sequence."""

        # Populate the input fields with the example values.
        for field, value in zip(self.input_fields, EXAMPLE_SEQUENCE):
            field.setText(str(value))

        self.canvas.plot_sequence(EXAMPLE_SEQUENCE)
        self.status.showMessage("Loaded example sequence.", 3000)