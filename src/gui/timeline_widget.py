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
)
from PyQt6.QtCore import pyqtSignal, Qt
from .styles import get_button_style, TIMELINE_STYLESHEET


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
        self.setStyleSheet(TIMELINE_STYLESHEET)

        root = QVBoxLayout()
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(10)

        # Row: play/pause + reset
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(8)

        self.play_pause_btn = QPushButton("Play")
        self.play_pause_btn.setFixedHeight(32)
        self.play_pause_btn.setStyleSheet(get_button_style("play"))
        self.play_pause_btn.setToolTip("Start/pause simulation (Space)")
        self.play_pause_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_pause_btn.clicked.connect(self.on_play_pause)
        buttons_row.addWidget(self.play_pause_btn)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedHeight(32)
        self.reset_btn.setStyleSheet(get_button_style("reset"))
        self.reset_btn.setToolTip("Reset simulation (Ctrl+R)")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.on_reset)
        buttons_row.addWidget(self.reset_btn)

        root.addLayout(buttons_row)

        # Row: time display
        time_row = QHBoxLayout()
        time_row.setSpacing(6)
        time_label = QLabel("Time:")
        time_label.setProperty("class", "info")
        self.time_display = QLabel("0.00 s")
        self.time_display.setProperty("class", "bold")
        time_row.addWidget(time_label)
        time_row.addWidget(self.time_display, 1)
        root.addLayout(time_row)

        # Row: speed slider + value
        speed_row = QVBoxLayout()
        speed_label_row = QHBoxLayout()
        speed_label = QLabel("Speed:")
        speed_label.setProperty("class", "info")
        self.speed_display = QLabel("1.0x")
        self.speed_display.setProperty("class", "bold")
        speed_label_row.addWidget(speed_label)
        speed_label_row.addStretch()
        speed_label_row.addWidget(self.speed_display)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)   # 0.1x
        self.speed_slider.setMaximum(100) # 10.0x
        self.speed_slider.setValue(10)    # 1.0x
        self.speed_slider.setToolTip("Adjust simulation speed (0.1x - 10.0x)")
        self.speed_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)

        speed_row.addLayout(speed_label_row)
        speed_row.addWidget(self.speed_slider)
        root.addLayout(speed_row)

        # Row: particle count
        particles_row = QHBoxLayout()
        particles_row.setSpacing(6)
        particles_label = QLabel("Particles:")
        particles_label.setProperty("class", "info")
        self.particle_count_display = QLabel("0")
        self.particle_count_display.setProperty("class", "bold")
        particles_row.addWidget(particles_label)
        particles_row.addStretch()
        particles_row.addWidget(self.particle_count_display)
        root.addLayout(particles_row)

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
