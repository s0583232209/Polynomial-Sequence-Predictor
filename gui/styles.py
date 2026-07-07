"""Light, playful mathematics-themed stylesheet for the PolySeqNet GUI."""

PAPER = "#FFF9EF"
CARD = "#FFFFFF"
INK = "#2E2B45"
MUTED = "#7B7391"
BORDER = "#EDE1C6"

BLUE = "#2F80ED"
BLUE_DARK = "#1C5FC4"

TEAL = "#0FA88F"
TEAL_DARK = "#0B8A75"

CORAL = "#FF6B4A"
CORAL_DARK = "#E85436"
CORAL_BG = "#FFEEE7"

YELLOW = "#F5B301"
YELLOW_BG = "#FFF6DD"

ERROR = "#E5484D"
ERROR_BG = "#FDEDEE"

STYLESHEET = f"""
QWidget {{
    background-color: {PAPER};
    color: {INK};
    font-family: "Segoe UI", "Verdana", sans-serif;
    font-size: 15px;
}}

QMainWindow {{
    background-color: {PAPER};
}}

QFrame#card {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

QLabel#titleLabel {{
    color: {BLUE_DARK};
    font-size: 34px;
    font-weight: 800;
}}

QLabel#subtitleLabel {{
    color: {TEAL_DARK};
    font-size: 16px;
}}

QLabel#sectionLabelInput {{
    color: {BLUE_DARK};
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QLabel#sectionLabelOutput {{
    color: {CORAL_DARK};
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QLabel#fieldIndexInput {{
    color: {BLUE};
    font-family: "Consolas", "Courier New", monospace;
    font-size: 30px;
    font-weight: 700;
}}

QLabel#fieldIndexOutput {{
    color: {CORAL_DARK};
    font-family: "Consolas", "Courier New", monospace;
    font-size: 30px;
    font-weight: 700;
}}

QLineEdit {{
    background-color: {CARD};
    border: 2px solid {BORDER};
    border-radius: 10px;
    padding: 8px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 34px;
    font-weight: 600;
    color: {INK};
}}

QLineEdit:focus {{
    border: 2px solid {BLUE};
}}

QPushButton#predictButton {{
    background-color: {BLUE};
    color: {CARD};
    border: none;
    border-radius: 10px;
    padding: 16px 34px;
    font-size: 22px;
    font-weight: 700;
}}

QPushButton#predictButton:hover {{
    background-color: {BLUE_DARK};
}}

QPushButton#predictButton:disabled {{
    background-color: {BORDER};
    color: {MUTED};
}}

QPushButton#clearButton {{
    background-color: transparent;
    color: {TEAL_DARK};
    border: 2px solid {TEAL};
    border-radius: 10px;
    padding: 14px 26px;
    font-size: 20px;
    font-weight: 600;
}}

QPushButton#clearButton:hover {{
    background-color: #E9FBF7;
}}

QPushButton#linkButton {{
    background-color: transparent;
    color: {CORAL_DARK};
    border: none;
    font-size: 16px;
    font-weight: 600;
    text-decoration: underline;
}}

QPushButton#linkButton:hover {{
    color: {CORAL};
}}

QStatusBar {{
    background-color: {CARD};
    color: {MUTED};
    border-top: 1px solid {BORDER};
    font-size: 13px;
}}
"""

_OUTPUT_BASE = """
QLabel {{
    border-radius: 10px;
    padding: 8px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 34px;
    font-weight: 700;
    background-color: {bg};
    border: 2px solid {border};
    color: {fg};
}}
"""

OUTPUT_DEFAULT_STYLE = _OUTPUT_BASE.format(bg=CARD, border=BORDER, fg=MUTED)
OUTPUT_LOADING_STYLE = _OUTPUT_BASE.format(bg=YELLOW_BG, border=YELLOW, fg="#9A7200")
OUTPUT_RESULT_STYLE = _OUTPUT_BASE.format(bg=CORAL_BG, border=CORAL, fg=CORAL_DARK)
OUTPUT_ERROR_STYLE = _OUTPUT_BASE.format(bg=ERROR_BG, border=ERROR, fg=ERROR)
