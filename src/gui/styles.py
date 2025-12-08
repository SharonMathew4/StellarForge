"""
Modern stylesheet definitions for StellarForge UI.
Delegates generation to the ThemeManager.
"""

from pathlib import Path
from .theme import theme_manager

_ASSETS_DIR = Path(__file__).resolve().parent
_CHECKBOX_TICK_URL = (_ASSETS_DIR / "checkbox_tick.svg").as_posix()

# Main application stylesheet
# Generated dynamically from the current theme
MAIN_STYLESHEET = theme_manager.get_main_stylesheet()

# Inject absolute asset paths if needed (currently ThemeManager handles structure, 
# but we can add specific asset replacements here if the theme uses them)
MAIN_STYLESHEET = MAIN_STYLESHEET.replace("CHECKBOX_TICK_URL", _CHECKBOX_TICK_URL)

# Legacy exports for compatibility (will be deprecated)
TIMELINE_STYLESHEET = "" 
CONTROL_PANEL_STYLESHEET = ""


def get_button_style(button_type: str = "default") -> str:
    """
    Get specific button style by type.
    Uses the ThemeManager's palette for consistency.
    
    Args:
        button_type: 'play', 'pause', 'reset', 'spawn', or 'default'
    """
    t = theme_manager.theme
    
    base_style = f"""
        QPushButton {{
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 600;
            border: none;
            color: {t.text_inverse};
        }}
    """
    
    styles = {
        "play": base_style + f"""
            QPushButton {{ background-color: {t.success}; }}
            QPushButton:hover {{ background-color: #40c057; }} /* Lighter green */
            QPushButton:pressed {{ background-color: #2b8a3e; }}
        """,
        "pause": base_style + f"""
            QPushButton {{ background-color: {t.warning}; color: {t.bg_primary}; }}
            QPushButton:hover {{ background-color: #fab005; }}
            QPushButton:pressed {{ background-color: #f08c00; }}
        """,
        "reset": base_style + f"""
            QPushButton {{ background-color: {t.error}; }}
            QPushButton:hover {{ background-color: #fa5252; }}
            QPushButton:pressed {{ background-color: #c92a2a; }}
        """,
        "spawn": base_style + f"""
            QPushButton {{ 
                background-color: {t.accent_secondary}; 
                margin: 4px 0;
            }}
            QPushButton:hover {{ background-color: #3bc9db; }}
            QPushButton:pressed {{ background-color: #0b7285; }}
        """,
    }
    return styles.get(button_type, "")
