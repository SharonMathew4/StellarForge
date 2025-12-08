"""
Timeline widget for simulation playback controls.
Placed inside the right control panel.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
    QFrame
)
from PyQt6.QtCore import pyqtSignal, Qt
from .styles import get_button_style

class TimelineWidget(QWidget):
    """Playback controls and basic stats."""

    play_pause_clicked = pyqtSignal(bool)  # is_playing
    reset_clicked = pyqtSignal()
    speed_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_playing = False
        self.init_ui()
        self.setup_shortcuts()

    def setup_shortcuts(self):
        """Setup keyboard shortcuts for timeline controls."""
        from PyQt6.QtGui import QShortcut, QKeySequence

        play_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        play_shortcut.activated.connect(self.on_play_pause)

        reset_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        reset_shortcut.activated.connect(self.on_reset)

    def init_ui(self):
        """Initialize the timeline UI (compact for side panel)."""
        self.setObjectName("timeline")
        
        # Main layout
        root = QVBoxLayout()
        root.setContentsMargins(0, 8, 0, 8)
        root.setSpacing(12)

        # 1. Playback Controls Row
        controls_group = QWidget()
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setContentsMargins(0,0,0,0)
        controls_layout.setSpacing(8)

        self.play_pause_btn = QPushButton("Play")
        self.play_pause_btn.setFixedHeight(32)
        self.play_pause_btn.setStyleSheet(get_button_style("play"))
        self.play_pause_btn.setToolTip("Start/pause simulation (Space)")
        self.play_pause_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_pause_btn.clicked.connect(self.on_play_pause)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedHeight(32)
        self.reset_btn.setStyleSheet(get_button_style("reset"))
        self.reset_btn.setToolTip("Reset simulation (Ctrl+R)")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.on_reset)

        controls_layout.addWidget(self.play_pause_btn, 2)
        controls_layout.addWidget(self.reset_btn, 1)
        root.addWidget(controls_group)

        # 2. Speed Slider
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Speed")
        speed_label.setProperty("class", "info")
        
        self.speed_display = QLabel("1.0x")
        self.speed_display.setStyleSheet("font-family: 'Consolas', monospace; font-weight: bold;")
        self.speed_display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)   # 0.1x
        self.speed_slider.setMaximum(100) # 10.0x
        self.speed_slider.setValue(10)    # 1.0x
        self.speed_slider.setToolTip("Adjust simulation speed (0.1x - 10.0x)")
        self.speed_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)

        root.addLayout(speed_layout)
        
        speed_row = QHBoxLayout()
        speed_row.addWidget(speed_label)
        speed_row.addStretch()
        speed_row.addWidget(self.speed_display)
        root.addLayout(speed_row)
        root.addWidget(self.speed_slider)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: transparent; border-top: 1px solid #323a45;")
        root.addWidget(line)

        # 3. Metrics Grid (Time / Particles)
        metrics_layout = QVBoxLayout()
        metrics_layout.setSpacing(4)
        
        # Time Row
        time_row = QHBoxLayout()
        time_lbl = QLabel("Time Evolved:")
        time_lbl.setProperty("class", "info")
        self.time_display = QLabel("0.00 s")
        self.time_display.setStyleSheet("font-family: 'Consolas', monospace; color: #f0f4f8;")
        time_row.addWidget(time_lbl)
        time_row.addStretch()
        time_row.addWidget(self.time_display)
        metrics_layout.addLayout(time_row)

        # Particles Row
        part_row = QHBoxLayout()
        part_lbl = QLabel("Active Particles:")
        part_lbl.setProperty("class", "info")
        self.particle_count_display = QLabel("0")
        self.particle_count_display.setStyleSheet("font-family: 'Consolas', monospace; color: #4c6ef5;")
        part_row.addWidget(part_lbl)
        part_row.addStretch()
        part_row.addWidget(self.particle_count_display)
        metrics_layout.addLayout(part_row)

        root.addLayout(metrics_layout)
        root.addStretch()
        self.setLayout(root)

    def on_play_pause(self):
        """Handle play/pause button click."""
        self.is_playing = not self.is_playing

        if self.is_playing:
            self.play_pause_btn.setText("Pause")
            self.play_pause_btn.setStyleSheet(get_button_style("pause"))
            self.play_pause_btn.setToolTip("Pause simulation (Space)")
        else:
            self.play_pause_btn.setText("Play")
            self.play_pause_btn.setStyleSheet(get_button_style("play"))
            self.play_pause_btn.setToolTip("Start simulation (Space)")

        self.play_pause_clicked.emit(self.is_playing)

    def on_reset(self):
        """Handle reset button click."""
        self.is_playing = False
        self.play_pause_btn.setText("Play")
        self.play_pause_btn.setStyleSheet(get_button_style("play"))
        self.play_pause_btn.setToolTip("Start simulation (Space)")
        self.update_time(0.0)
        self.reset_clicked.emit()

    def on_speed_changed(self, value: int):
        """Handle speed slider change."""
        speed = value / 10.0
        self.speed_display.setText(f"{speed:.1f}x")
        self.speed_changed.emit(speed)

    def update_time(self, time_val: float):
        """Update time display."""
        self.time_display.setText(f"{time_val:.2f} s")

    def update_particle_count(self, count: int):
        """Update particle count display."""
        self.particle_count_display.setText(f"{count:,}")

    def set_playing(self, playing: bool):
        """Set play state programmatically."""
        if self.is_playing != playing:
            self.on_play_pause()
