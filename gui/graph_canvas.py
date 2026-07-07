import matplotlib

matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

PAPER = "#FFF9EF"
INK = "#2E2B45"
BLUE = "#2F80ED"
CORAL = "#FF6B4A"
GRID = "#EDE1C6"


class GraphCanvas(FigureCanvasQTAgg):
    """Embedded matplotlib canvas showing the input sequence and, once
    available, the model's predicted continuation."""

    def __init__(self, parent=None):
        self.figure = Figure(figsize=(5, 1.7), dpi=100, facecolor=PAPER)
        super().__init__(self.figure)
        self.setParent(parent)

        self.axes = self.figure.add_subplot(111)
        self._style_axes()
        self.figure.tight_layout()

    def _style_axes(self):
        ax = self.axes
        ax.set_facecolor(PAPER)

        for spine in ax.spines.values():
            spine.set_color(GRID)

        ax.tick_params(colors=INK, labelsize=8)
        ax.grid(True, color=GRID, linewidth=0.8, linestyle="--", alpha=0.8)
        ax.set_xlabel("n", color=INK, fontsize=9, style="italic")
        ax.set_ylabel("a(n)", color=INK, fontsize=9, style="italic")

    def plot_sequence(self, input_values, predicted_values=None):
        ax = self.axes
        ax.clear()
        self._style_axes()

        input_x = list(range(len(input_values)))
        ax.plot(input_x, input_values, color=BLUE, linewidth=2, zorder=2)
        ax.scatter(
            input_x, input_values,
            color=BLUE, s=55, zorder=3, label="Input",
        )

        if predicted_values:
            pred_x = list(range(
                len(input_values) - 1,
                len(input_values) + len(predicted_values),
            ))
            pred_y = [input_values[-1]] + list(predicted_values)

            ax.plot(
                pred_x, pred_y,
                color=CORAL, linewidth=2, linestyle="--", zorder=2,
            )
            ax.scatter(
                pred_x[1:], pred_y[1:],
                color=CORAL, s=65, marker="D", zorder=3, label="Predicted",
            )

        ax.legend(
            loc="upper left", frameon=False, fontsize=9, labelcolor=INK,
        )
        self.figure.tight_layout()
        self.draw()

    def clear_plot(self):
        ax = self.axes
        ax.clear()
        self._style_axes()
        self.figure.tight_layout()
        self.draw()
