"""Light, academic/mathematics-themed stylesheet for the PolySeqNet GUI."""

PAPER = "#FAF7F0"
CARD = "#FFFFFF"
INK = "#1B2A4A"
INDIGO = "#28407A"
INDIGO_DARK = "#1B2A4A"
BORDER = "#D8D2C4"
MUTED = "#7A7566"
GOLD = "#C9A227"
GOLD_BG = "#FFF6DD"
ERROR = "#B3261E"

STYLESHEET = f"""
QWidget {{
    background-color: {PAPER};
    color: {INK};
    font-family: "Georgia", "Cambria", serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {PAPER};
}}

QFrame#card {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}

QLabel#titleLabel {{
    color: {INDIGO_DARK};
    font-size: 22px;
    font-weight: bold;
}}

QLabel#subtitleLabel {{
    color: {MUTED};
    font-size: 12px;
    font-style: italic;
}}

QLabel#sectionLabel {{
    color: {INDIGO_DARK};
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 1px;
}}

QLabel#fieldIndex {{
    color: {MUTED};
    font-family: "Consolas", "Courier New", monospace;
    font-size: 11px;
}}

QLineEdit {{
    background-color: {PAPER};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    color: {INDIGO_DARK};
}}

QLineEdit:focus {{
    border: 1px solid {INDIGO};
}}

QPushButton#predictButton {{
    background-color: {INDIGO};
    color: {CARD};
    border: none;
    border-radius: 6px;
    padding: 9px 22px;
    font-size: 14px;
    font-weight: bold;
}}

QPushButton#predictButton:hover {{
    background-color: {INDIGO_DARK};
}}

QPushButton#predictButton:disabled {{
    background-color: {BORDER};
    color: {MUTED};
}}

QPushButton#clearButton {{
    background-color: transparent;
    color: {INDIGO};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 9px 18px;
    font-size: 13px;
}}

QPushButton#clearButton:hover {{
    background-color: {PAPER};
    border: 1px solid {INDIGO};
}}

QPushButton#linkButton {{
    background-color: transparent;
    color: {INDIGO};
    border: none;
    font-size: 12px;
    text-decoration: underline;
}}

QPushButton#linkButton:hover {{
    color: {INDIGO_DARK};
}}

QStatusBar {{
    background-color: {CARD};
    color: {MUTED};
    border-top: 1px solid {BORDER};
    font-size: 11px;
}}
"""

OUTPUT_DEFAULT_STYLE = f"""
QLabel {{
    background-color: {PAPER};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    color: {MUTED};
}}
"""

OUTPUT_LOADING_STYLE = f"""
QLabel {{
    background-color: {PAPER};
    border: 1px solid {INDIGO};
    border-radius: 6px;
    padding: 6px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    color: {INDIGO};
}}
"""

OUTPUT_RESULT_STYLE = f"""
QLabel {{
    background-color: {GOLD_BG};
    border: 1px solid {GOLD};
    border-radius: 6px;
    padding: 6px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 15px;
    font-weight: bold;
    color: {INDIGO_DARK};
}}
"""

OUTPUT_ERROR_STYLE = f"""
QLabel {{
    background-color: {CARD};
    border: 1px solid {ERROR};
    border-radius: 6px;
    padding: 6px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    color: {ERROR};
}}
"""
