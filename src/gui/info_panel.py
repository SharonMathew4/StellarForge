"""
Info panel widget for displaying simulation statistics.
Shows FPS, performance metrics, and other real-time information.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox, 
                             QGridLayout, QFrame)
from PyQt6.QtCore import pyqtSignal, Qt
from .theme import theme_manager

class InfoPanel(QWidget):
    """
    Panel displaying real-time simulation statistics.
    Can be docked or floating.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the info panel UI."""
        self.setObjectName("infoPanel")
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header = QLabel("Metric Telemetry")
        header.setProperty("class", "section-header")
        layout.addWidget(header)
        
        # Performance group
        perf_group = self.create_performance_group()
        layout.addWidget(perf_group)
        
        # Simulation stats group
        stats_group = self.create_stats_group()
        layout.addWidget(stats_group)
        
        # Camera info group
        camera_group = self.create_camera_group()
        layout.addWidget(camera_group)
        
        layout.addStretch()
        
        self.setLayout(layout)
        self.setMaximumWidth(320)
        self._fps_band = None
    
    def create_performance_group(self) -> QGroupBox:
        """Create performance metrics group."""
        group = QGroupBox("System Performance")
        layout = QGridLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 24, 12, 12)
        
        # Helper to create metrics
        def add_metric(row, label, tooltip, value_id):
            lbl = QLabel(label)
            lbl.setProperty("class", "info")
            val = QLabel("0")
            val.setProperty("class", "bold")
            val.setToolTip(tooltip)
            val.setStyleSheet("font-family: 'Consolas', monospace;")
            layout.addWidget(lbl, row, 0)
            layout.addWidget(val, row, 1)
            return val

        self.fps_value = add_metric(0, "FPS:", "Frames per second", "fps")
        self.frame_value = add_metric(1, "Frame Time:", "Time to render one frame", "ft")
        self.mem_value = add_metric(2, "Memory:", "Memory usage", "mem")
        self.mem_value.setText("N/A")
        
        group.setLayout(layout)
        return group
    
    def create_stats_group(self) -> QGroupBox:
        """Create simulation statistics group."""
        group = QGroupBox("Physics Statistics")
        layout = QGridLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 24, 12, 12)
        
        def add_metric(row, label, tooltip):
            lbl = QLabel(label)
            lbl.setProperty("class", "info")
            val = QLabel("N/A")
            val.setProperty("class", "bold")
            val.setToolTip(tooltip)
            val.setStyleSheet("font-family: 'Consolas', monospace;")
            layout.addWidget(lbl, row, 0)
            layout.addWidget(val, row, 1)
            return val
        
        self.energy_value = add_metric(0, "Total Energy:", "Total system energy")
        self.momentum_value = add_metric(1, "Momentum:", "System momentum")
        
        # Active particles with number formatting
        lbl = QLabel("Active Bodies:")
        lbl.setProperty("class", "info")
        self.active_value = QLabel("0")
        self.active_value.setProperty("class", "bold")
        self.active_value.setStyleSheet(f"font-family: 'Consolas', monospace; color: {theme_manager.theme.accent_secondary};")
        layout.addWidget(lbl, 2, 0)
        layout.addWidget(self.active_value, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_camera_group(self) -> QGroupBox:
        """Create camera information group."""
        group = QGroupBox("Camera Telemetry")
        layout = QGridLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 24, 12, 12)
        
        def add_metric(row, label, tooltip):
            lbl = QLabel(label)
            lbl.setProperty("class", "info")
            val = QLabel("(0.0, 0.0, 0.0)")
            val.setProperty("class", "bold")
            val.setToolTip(tooltip)
            val.setStyleSheet("font-family: 'Consolas', monospace;")
            layout.addWidget(lbl, row, 0)
            layout.addWidget(val, row, 1)
            return val
        
        self.pos_value = add_metric(0, "Position:", "Camera position")
        self.dist_value = add_metric(1, "Distance:", "Distance from origin")
        self.dist_value.setText("0.0")
        
        group.setLayout(layout)
        return group
    
    # Update methods
    
    def update_fps(self, fps: float):
        """Update FPS display."""
        self.fps_value.setText(f"{fps:.1f}")
        
        # Color code based on performance
        t = theme_manager.theme
        if fps >= 55:
            band = "high"
            color = t.success
        elif fps >= 30:
            band = "medium"
            color = t.warning
        else:
            band = "low"
            color = t.error

        # Only update stylesheet when band changes to avoid per-frame CSS churn
        if band != self._fps_band:
            self.fps_value.setStyleSheet(f"color: {color}; font-family: 'Consolas', monospace; font-weight: bold;")
            self._fps_band = band
    
    def update_frame_time(self, ms: float):
        """Update frame time display."""
        self.frame_value.setText(f"{ms:.1f} ms")
    
    def update_memory(self, mb: float):
        """Update memory usage display."""
        self.mem_value.setText(f"{mb:.1f} MB")
    
    def update_energy(self, energy: float):
        """Update total energy display."""
        self.energy_value.setText(f"{energy:.2e}")
    
    def update_momentum(self, momentum: float):
        """Update momentum display."""
        self.momentum_value.setText(f"{momentum:.2e}")
    
    def update_active_particles(self, count: int):
        """Update active particle count."""
        self.active_value.setText(f"{count:,}")
    
    def update_camera_pos(self, x: float, y: float, z: float):
        """Update camera position."""
        self.pos_value.setText(f"({x:.1f}, {y:.1f}, {z:.1f})")
    
    def update_camera_distance(self, dist: float):
        """Update camera distance."""
        self.dist_value.setText(f"{dist:.1f}")
