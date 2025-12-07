"""
Splash screen for StellarForge application startup.
Shows loading animation and initialization progress.
"""

from PyQt6.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QLinearGradient


class StellarForgeSplash(QSplashScreen):
    """
    Custom splash screen with animated loading.
    """
    
    def __init__(self):
        # Create a custom pixmap
        pixmap = self.create_splash_pixmap()
        
        super().__init__(pixmap, Qt.WindowType.WindowStaysOnTopHint)
        
        self.progress = 0
    
    def create_splash_pixmap(self) -> QPixmap:
        """Create the splash screen pixmap with custom graphics."""
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor(26, 26, 46))  # Dark background
        
        # Create custom painting
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw gradient background
        gradient = QLinearGradient(0, 0, 600, 400)
        gradient.setColorAt(0, QColor(15, 15, 30))
        gradient.setColorAt(1, QColor(26, 26, 46))
        painter.fillRect(0, 0, 600, 400, gradient)
        
        # Draw title
        title_font = QFont("Segoe UI", 36, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.setPen(QColor(139, 95, 212))  # Purple
        painter.drawText(0, 0, 600, 200, Qt.AlignmentFlag.AlignCenter, "StellarForge")
        
        # Draw subtitle
        subtitle_font = QFont("Segoe UI", 14)
        painter.setFont(subtitle_font)
        painter.setPen(QColor(160, 160, 176))
        painter.drawText(0, 220, 600, 50, Qt.AlignmentFlag.AlignCenter, 
                        "Cosmic Simulation Engine")
        
        # Draw version
        version_font = QFont("Segoe UI", 10)
        painter.setFont(version_font)
        painter.setPen(QColor(106, 67, 160))
        painter.drawText(0, 360, 600, 30, Qt.AlignmentFlag.AlignCenter, 
                        "Version 1.0.0 | Loading...")
        
        painter.end()
        return pixmap
    
    def showMessage(self, message: str, color=None):
        """
        Show a status message on the splash screen.
        
        Args:
            message: Message to display
            color: Color for the message (optional)
        """
        if color is None:
            color = Qt.GlobalColor.white
        
        super().showMessage(
            f"\n\n\n\n\n\n\n\n\n\n\n{message}",
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
            color
        )
    
    def set_progress(self, value: int):
        """Set progress (0-100)."""
        self.progress = value
    
    def finish_loading(self):
        """Complete the loading animation."""
        self.showMessage("Ready", QColor(40, 167, 69))


def show_splash_screen():
    """
    Show splash screen and return instance.
    
    Returns:
        StellarForgeSplash instance
    """
    splash = StellarForgeSplash()
    splash.show()
    return splash
