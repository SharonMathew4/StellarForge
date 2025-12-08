"""
Theme Management System for StellarForge.
Provides centralized color palettes and QSS generation for an enterprise-grade UI.
"""

from typing import Dict, NamedTuple
from dataclasses import dataclass

@dataclass
class ColorPalette:
    """Defines a comprehensive color palette for the application."""
    # Backgrounds
    bg_primary: str   # Main window background
    bg_secondary: str # Panel/Dock background
    bg_tertiary: str  # Input/Widget background
    bg_hover: str     # Hover state background
    bg_selected: str  # Selected state background
    
    # Text
    text_primary: str   # Main text
    text_secondary: str # Secondary labels/descriptions
    text_tertiary: str  # Placeholder/Disabled text
    text_inverse: str   # Text on dark accents
    
    # Accents - Professional/Scientific
    accent_primary: str   # Primary interaction color (e.g., Indigo/Blue)
    accent_secondary: str # Secondary interaction color (e.g., Teal)
    accent_hover: str
    accent_pressed: str
    
    # Semantic
    success: str
    warning: str
    error: str
    info: str
    
    # Borders
    border_light: str
    border_focus: str

# "Cosmic Enterprise" Theme Definition
COSMIC_ENTERPRISE = ColorPalette(
    # Backgrounds - Dark Slate/Gunmetal for reduced eye strain vs pure black
    bg_primary="#0f1115",    # Very dark cool grey (almost black)
    bg_secondary="#181b21",  # Slightly lighter container bg
    bg_tertiary="#232830",   # Input/Widget bg
    bg_hover="#2e3540",      # Hover bg
    bg_selected="#353e4b",   # Selected bg
    
    # Text - High readability
    text_primary="#f0f4f8",   # Near white
    text_secondary="#9fb3c8", # Muted blue-grey
    text_tertiary="#627d98",  # Darker muted blue-grey
    text_inverse="#ffffff",   # White text for accent buttons
    
    # Accents - Professional Indigo & Cyan
    accent_primary="#4c6ef5",   # Professional Indigo/Blue
    accent_secondary="#22b8cf", # Cyan/Teal
    accent_hover="#4263eb",     # Slightly darker indigo
    accent_pressed="#364fc7",   # Deep indigo
    
    # Semantic
    success="#37b24d", # Modern Green
    warning="#f59f00", # Amber
    error="#f03e3e",   # Red
    info="#1c7ed6",    # Blue
    
    # Borders
    border_light="#323a45", # Subtle border
    border_focus="#4c6ef5"  # Matches accent primary
)

class ThemeManager:
    """Manages application themes and generates stylesheets."""
    
    def __init__(self):
        self._current_theme = COSMIC_ENTERPRISE
        self._font_family = "'Segoe UI', 'Inter', 'Roboto', 'Arial', sans-serif"
        self._font_size = "9.5pt"
        self._mono_font = "'Consolas', 'Roboto Mono', 'Monospace'"

    @property
    def theme(self) -> ColorPalette:
        return self._current_theme
        
    def get_main_stylesheet(self) -> str:
        """Generate the main application QSS."""
        t = self.theme
        return f"""
        /* Global Application Style */
        QMainWindow {{
            background-color: {t.bg_primary};
        }}
        
        QWidget {{
            background-color: {t.bg_secondary};
            color: {t.text_primary};
            font-family: {self._font_family};
            font-size: {self._font_size};
        }}
        
        /* Headers & Labels */
        QLabel {{
            background-color: transparent;
            color: {t.text_primary};
        }}
        
        QLabel.section-header {{
            font-weight: bold;
            font-size: 10pt;
            color: {t.text_secondary};
            padding: 4px 0;
            border-bottom: 2px solid {t.border_light};
            margin-bottom: 8px;
        }}
        
        QLabel.info {{
            color: {t.text_secondary};
            font-size: 9pt;
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {t.bg_tertiary};
            color: {t.text_primary};
            border: 1px solid {t.border_light};
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: 600;
        }}
        
        QPushButton:hover {{
            background-color: {t.bg_hover};
            border-color: {t.text_tertiary};
        }}
        
        QPushButton:pressed {{
            background-color: {t.bg_selected};
        }}
        
        QPushButton:disabled {{
            background-color: {t.bg_primary};
            color: {t.text_tertiary};
            border-color: {t.bg_secondary};
        }}
        
        /* Action Buttons (Primary) */
        QPushButton.primary {{
            background-color: {t.accent_primary};
            color: {t.text_inverse};
            border: 1px solid {t.accent_primary};
        }}
        
        QPushButton.primary:hover {{
            background-color: {t.accent_hover};
            border-color: {t.accent_hover};
        }}
        
        QPushButton.primary:pressed {{
            background-color: {t.accent_pressed};
            border-color: {t.accent_pressed};
        }}
        
        /* Inputs */
        QSpinBox, QDoubleSpinBox, QLineEdit {{
            background-color: {t.bg_tertiary};
            border: 1px solid {t.border_light};
            border-radius: 4px;
            padding: 4px 8px;
            color: {t.text_primary};
            selection-background-color: {t.accent_primary};
        }}
        
        QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {{
            border: 1px solid {t.border_focus};
            background-color: {t.bg_secondary};
        }}
        
        /* Sliders */
        QSlider::groove:horizontal {{
            height: 4px;
            background-color: {t.bg_tertiary};
            border-radius: 2px;
        }}
        
        QSlider::handle:horizontal {{
            background-color: {t.accent_secondary};
            width: 16px;
            height: 16px;
            margin: -6px 0;
            border-radius: 8px;
            border: 2px solid {t.bg_secondary};
        }}
        
        QSlider::handle:horizontal:hover {{
            background-color: {t.text_primary};
            transform: scale(1.1);
        }}
        
        QSlider::sub-page:horizontal {{
            background-color: {t.accent_primary};
            border-radius: 2px;
        }}
        
        /* Groups & Panels */
        QGroupBox {{
            border: 1px solid {t.border_light};
            border-radius: 6px;
            margin-top: 1.2em; /* Leave space for title */
            background-color: {t.bg_secondary};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 4px;
            color: {t.text_secondary};
            font-weight: 600;
        }}
        
        /* Dock Widgets */
        QDockWidget::title {{
            background-color: {t.bg_primary};
            padding: 8px;
            border-bottom: 1px solid {t.border_light};
            font-weight: 600;
        }}
        
        QDockWidget .QWidget {{ 
            background-color: {t.bg_secondary}; 
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {t.bg_primary};
            border-bottom: 1px solid {t.border_light};
        }}
        
        QMenuBar::item:selected {{
            background-color: {t.bg_hover};
            border-radius: 4px;
        }}
        
        QMenu {{
            background-color: {t.bg_secondary};
            border: 1px solid {t.border_light};
        }}
        
        QMenu::item:selected {{
            background-color: {t.accent_primary};
            color: {t.text_inverse};
        }}
        """

# Singleton instance
theme_manager = ThemeManager()
