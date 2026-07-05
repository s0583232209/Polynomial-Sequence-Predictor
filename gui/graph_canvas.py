import matplotlib

matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

PAPER = "#FAF7F0"
INK = "#1B2A4A"
INDIGO = "#28407A"
GOLD = "#C9A227"
GRID = "#D8D2C4"


class GraphCanvas(FigureCanvasQTAgg):
    """Embedded matplotlib canvas showing the input sequence and, once
    available, the model's predicted continuation."""

    def __init__(self, parent=None):
        self.figure = Figure(figsize=(5, 3), dpi=100, facecolor=PAPER)
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

        ax.tick_params(colors=INK, labelsize=9)
        ax.grid(True, color=GRID, linewidth=0.8, linestyle="--", alpha=0.8)
        ax.set_xlabel("n", color=INK, fontsize=10, style="italic")
        ax.set_ylabel("a(n)", color=INK, fontsize=10, style="italic")
        ax.set_title("Sequence", color=INK, fontsize=11, fontweight="bold")

    def plot_sequence(self, input_values, predicted_values=None):
        ax = self.axes
        ax.clear()
        self._style_axes()

        input_x = list(range(len(input_values)))
        ax.plot(input_x, input_values, color=INDIGO, linewidth=1.5, zorder=2)
        ax.scatter(
            input_x, input_values,
            color=INDIGO, s=45, zorder=3, label="Input",
        )

        if predicted_values:
            pred_x = list(range(
                len(input_values) - 1,
                len(input_values) + len(predicted_values),
            ))
            pred_y = [input_values[-1]] + list(predicted_values)

            ax.plot(
                pred_x, pred_y,
                color=GOLD, linewidth=1.5, linestyle="--", zorder=2,
            )
            ax.scatter(
                pred_x[1:], pred_y[1:],
                color=GOLD, s=55, marker="D", zorder=3, label="Predicted",
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
