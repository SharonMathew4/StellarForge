"""
Modern stylesheet definitions for StellarForge UI.
Provides dark theme with hover effects, smooth transitions, and polished look.
"""

from pathlib import Path

_ASSETS_DIR = Path(__file__).resolve().parent
_CHECKBOX_TICK_URL = (_ASSETS_DIR / "checkbox_tick.svg").as_posix()

# Main application stylesheet
MAIN_STYLESHEET = """
/* Global Application Style */
QMainWindow {
    background-color: #0f172a;
}

QWidget {
    background-color: #111827;
    color: #e5e7eb;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9.5pt;
}

/* Menu Bar */
QMenuBar {
    background-color: #0b1220;
    color: #e5e7eb;
    border-bottom: 1px solid #1f2937;
    padding: 3px;
}

QMenuBar::item {
    padding: 5px 10px;
    background-color: transparent;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #303a6d;
}

QMenuBar::item:pressed {
    background-color: #374799;
}

QMenu {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 6px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 30px 8px 20px;
    border-radius: 4px;
    margin: 2px 4px;
}

QMenu::item:selected {
    background-color: #303a6d;
    color: #ffffff;
}

QMenu::separator {
    height: 1px;
    background-color: #1f2937;
    margin: 6px 10px;
}

/* Status Bar */
QStatusBar {
    background-color: #0f0f1e;
    color: #a0a0b0;
    border-top: 1px solid #2a2a4e;
    font-size: 9pt;
}

/* Dock Widget */
QDockWidget {
    titlebar-close-icon: url(close.png);
    titlebar-normal-icon: url(float.png);
    color: #e8e8e8;
    font-weight: bold;
}

QDockWidget::title {
    background-color: #0f0f1e;
    padding: 8px;
    border-bottom: 2px solid #533483;
    text-align: center;
}

QDockWidget::close-button, QDockWidget::float-button {
    background-color: transparent;
    border: none;
    padding: 4px;
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background-color: #533483;
    border-radius: 4px;
}

/* Group Box */
QGroupBox {
    background-color: #1a1a2e;
    border: 2px solid #2a2a4e;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 14px;
    font-weight: bold;
    color: #b8b8d0;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 3px 9px;
    background-color: #533483;
    color: #ffffff;
    border-radius: 4px;
    left: 12px;
}

/* Push Button */
QPushButton {
    background-color: #533483;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: bold;
    font-size: 10pt;
    min-height: 22px;
}

QPushButton:hover {
    background-color: #6a43a0;
    border: 2px solid #8b5fd4;
}

QPushButton:pressed {
    background-color: #3f2866;
    padding-top: 12px;
    padding-bottom: 8px;
}

QPushButton:disabled {
    background-color: #2a2a3e;
    color: #606070;
}

/* Special Button Styles */
QPushButton#playButton {
    background-color: #28a745;
}

QPushButton#playButton:hover {
    background-color: #34d058;
}

QPushButton#pauseButton {
    background-color: #ffc107;
}

QPushButton#pauseButton:hover {
    background-color: #ffcd38;
}

QPushButton#resetButton {
    background-color: #dc3545;
}

QPushButton#resetButton:hover {
    background-color: #e74c3c;
}

QPushButton#spawnButton {
    background-color: #17a2b8;
    margin: 4px 0;
}

QPushButton#spawnButton:hover {
    background-color: #1fc8e3;
}

/* Radio Button */
QRadioButton {
    color: #e8e8e8;
    spacing: 6px;
    padding: 4px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #533483;
    background-color: #1a1a2e;
}

QRadioButton::indicator:checked {
    background-color: #6a43a0;
    border: 2px solid #8b5fd4;
}

QRadioButton::indicator:hover {
    border: 2px solid #8b5fd4;
    background-color: #2a2a4e;
}

QRadioButton:hover {
    background-color: #1f1f3a;
    border-radius: 4px;
}

/* Check Box */
QCheckBox {
    color: #e8e8e8;
    spacing: 6px;
    padding: 4px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 2px solid #533483;
    background-color: #1a1a2e;
    background-position: center;
    background-repeat: no-repeat;
}

QCheckBox::indicator:checked {
    background-color: #111827;
    border: 2px solid #8b5fd4;
    background-position: center;
    background-repeat: no-repeat;
    image: url("CHECKBOX_TICK_URL");
}

QCheckBox::indicator:hover {
    border: 2px solid #8b5fd4;
    background-color: #2a2a4e;
}

/* Keep tick visible while hovered and checked */
QCheckBox::indicator:checked:hover {
    background-color: #1a2133;
    border: 2px solid #9aa8ff;
    image: url("CHECKBOX_TICK_URL");
}

QCheckBox:hover {
    background-color: #1f1f3a;
    border-radius: 4px;
}

/* Slider */
QSlider::groove:horizontal {
    height: 6px;
    background-color: #2a2a4e;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background-color: #6a43a0;
    border: 2px solid #8b5fd4;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background-color: #8b5fd4;
    border: 2px solid #a67fd8;
    width: 18px;
    height: 18px;
    margin: -7px 0;
}

QSlider::handle:horizontal:pressed {
    background-color: #533483;
}

QSlider::sub-page:horizontal {
    background-color: #6a43a0;
    border-radius: 3px;
}

/* Label */
QLabel {
    color: #e8e8e8;
    background-color: transparent;
}

QLabel[class="info"] {
    color: #a0a0b0;
    font-size: 9pt;
    font-style: italic;
}

QLabel[class="bold"] {
    font-weight: bold;
    color: #ffffff;
}

QLabel[class="title"] {
    font-size: 12pt;
    font-weight: bold;
    color: #8b5fd4;
}

/* Spin Box */
QSpinBox, QDoubleSpinBox {
    background-color: #1a1a2e;
    border: 2px solid #2a2a4e;
    border-radius: 4px;
    padding: 6px;
    color: #e8e8e8;
}

QSpinBox:hover, QDoubleSpinBox:hover {
    border: 2px solid #533483;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #6a43a0;
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    background-color: #533483;
    border-top-right-radius: 4px;
    width: 20px;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {
    background-color: #6a43a0;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #533483;
    border-bottom-right-radius: 4px;
    width: 20px;
}

QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #6a43a0;
}

/* Scroll Bar */
QScrollBar:vertical {
    background-color: #1a1a2e;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #533483;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #6a43a0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #1a1a2e;
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #533483;
    border-radius: 6px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #6a43a0;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Tool Tip */
QToolTip {
    background-color: #2a2a4e;
    color: #ffffff;
    border: 1px solid #533483;
    border-radius: 4px;
    padding: 6px;
    font-size: 9pt;
}

/* Message Box */
QMessageBox {
    background-color: #16213e;
}

QMessageBox QPushButton {
    min-width: 80px;
    padding: 8px 16px;
}

/* File Dialog */
QFileDialog {
    background-color: #16213e;
}

/* Tab Widget */
QTabWidget::pane {
    border: 2px solid #2a2a4e;
    border-radius: 6px;
    background-color: #1a1a2e;
    top: -2px;
}

QTabBar::tab {
    background-color: #2a2a4e;
    color: #a0a0b0;
    padding: 10px 20px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #533483;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #3a3a5e;
}
"""

# Inject absolute asset paths for resources referenced in the stylesheet
MAIN_STYLESHEET = MAIN_STYLESHEET.replace("CHECKBOX_TICK_URL", _CHECKBOX_TICK_URL)

# Timeline widget specific styles
TIMELINE_STYLESHEET = """
QWidget#timeline {
    background-color: #0f0f1e;
    border-top: 2px solid #2a2a4e;
}
"""

# Control panel specific styles
CONTROL_PANEL_STYLESHEET = """
QWidget#controlPanel {
    background-color: #16213e;
    border-left: 2px solid #2a2a4e;
}
"""

def get_button_style(button_type: str = "default") -> str:
    """
    Get specific button style by type.
    
    Args:
        button_type: 'play', 'pause', 'reset', 'spawn', or 'default'
    """
    styles = {
        "play": """
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34d058;
                border: 2px solid #4ae068;
            }
            QPushButton:pressed {
                background-color: #218838;
            }
        """,
        "pause": """
            QPushButton {
                background-color: #ffc107;
                color: #1a1a2e;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffcd38;
                border: 2px solid #ffd966;
            }
            QPushButton:pressed {
                background-color: #e0a800;
            }
        """,
        "reset": """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                border: 2px solid #f85c5c;
            }
            QPushButton:pressed {
                background-color: #c82333;
            }
        """,
        "spawn": """
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
                margin: 4px 0;
            }
            QPushButton:hover {
                background-color: #1fc8e3;
                border: 2px solid #3fd9f0;
            }
            QPushButton:pressed {
                background-color: #138496;
            }
        """,
    }
    return styles.get(button_type, MAIN_STYLESHEET)
