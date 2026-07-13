import sys

# predict (and therefore torch) must be imported before PyQt5: on some Windows
# setups, once PyQt5's bundled Qt5 DLL directory is added to the DLL search
# path, torch's own c10.dll fails to initialize (WinError 1114) if loaded
# afterwards.
import predict  # noqa: F401

from PyQt5.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui.styles import STYLESHEET


def main():
    # Create the Qt application and apply the global stylesheet.
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    # Build and show the main window.
    window = MainWindow()
    window.show()

    # Hand control to the Qt event loop.
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
