"""
Info panel widget for displaying simulation statistics.
Shows FPS, performance metrics, and other real-time information.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGroupBox, 
                             QGridLayout, QFrame)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


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
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
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
        self.setMaximumWidth(280)
        self._fps_band = None
    
    def create_performance_group(self) -> QGroupBox:
        """Create performance metrics group."""
        group = QGroupBox("Performance")
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # FPS display
        fps_label = QLabel("FPS:")
        fps_label.setProperty("class", "info")
        self.fps_value = QLabel("0")
        self.fps_value.setProperty("class", "bold")
        self.fps_value.setToolTip("Frames per second")
        layout.addWidget(fps_label, 0, 0)
        layout.addWidget(self.fps_value, 0, 1)
        
        # Frame time
        frame_label = QLabel("Frame Time:")
        frame_label.setProperty("class", "info")
        self.frame_value = QLabel("0 ms")
        self.frame_value.setProperty("class", "bold")
        self.frame_value.setToolTip("Time to render one frame")
        layout.addWidget(frame_label, 1, 0)
        layout.addWidget(self.frame_value, 1, 1)
        
        # Memory usage (placeholder)
        mem_label = QLabel("Memory:")
        mem_label.setProperty("class", "info")
        self.mem_value = QLabel("N/A")
        self.mem_value.setProperty("class", "bold")
        self.mem_value.setToolTip("Memory usage")
        layout.addWidget(mem_label, 2, 0)
        layout.addWidget(self.mem_value, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_stats_group(self) -> QGroupBox:
        """Create simulation statistics group."""
        group = QGroupBox("Statistics")
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Total energy
        energy_label = QLabel("Total Energy:")
        energy_label.setProperty("class", "info")
        self.energy_value = QLabel("N/A")
        self.energy_value.setProperty("class", "bold")
        self.energy_value.setToolTip("Total system energy")
        layout.addWidget(energy_label, 0, 0)
        layout.addWidget(self.energy_value, 0, 1)
        
        # Momentum
        momentum_label = QLabel("Momentum:")
        momentum_label.setProperty("class", "info")
        self.momentum_value = QLabel("N/A")
        self.momentum_value.setProperty("class", "bold")
        self.momentum_value.setToolTip("System momentum")
        layout.addWidget(momentum_label, 1, 0)
        layout.addWidget(self.momentum_value, 1, 1)
        
        # Active particles
        active_label = QLabel("Active:")
        active_label.setProperty("class", "info")
        self.active_value = QLabel("0")
        self.active_value.setProperty("class", "bold")
        self.active_value.setToolTip("Active particles")
        layout.addWidget(active_label, 2, 0)
        layout.addWidget(self.active_value, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_camera_group(self) -> QGroupBox:
        """Create camera information group."""
        group = QGroupBox("Camera")
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Position
        pos_label = QLabel("Position:")
        pos_label.setProperty("class", "info")
        self.pos_value = QLabel("(0, 0, 0)")
        self.pos_value.setProperty("class", "bold")
        self.pos_value.setToolTip("Camera position")
        self.pos_value.setWordWrap(True)
        layout.addWidget(pos_label, 0, 0)
        layout.addWidget(self.pos_value, 0, 1)
        
        # Distance
        dist_label = QLabel("Distance:")
        dist_label.setProperty("class", "info")
        self.dist_value = QLabel("0")
        self.dist_value.setProperty("class", "bold")
        self.dist_value.setToolTip("Distance from origin")
        layout.addWidget(dist_label, 1, 0)
        layout.addWidget(self.dist_value, 1, 1)
        
        group.setLayout(layout)
        return group
    
    # Update methods
    
    def update_fps(self, fps: float):
        """Update FPS display."""
        self.fps_value.setText(f"{fps:.1f}")
        
        # Color code based on performance
        if fps >= 55:
            band = "high"
            color = "#28a745"  # Green
        elif fps >= 30:
            band = "medium"
            color = "#ffc107"  # Yellow
        else:
            band = "low"
            color = "#dc3545"  # Red

        # Only update stylesheet when band changes to avoid per-frame CSS churn
        if band != self._fps_band:
            self.fps_value.setStyleSheet(f"color: {color}; font-weight: bold;")
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
