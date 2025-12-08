"""
Control panel widget for simulation controls and settings.
Contains mode toggles, object spawner, and physics settings.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QPushButton, QCheckBox, QLabel, QRadioButton,
                             QFrame)
from PyQt6.QtCore import pyqtSignal, Qt
from .styles import get_button_style
from .timeline_widget import TimelineWidget
from core import SimulationMode

class ControlPanel(QWidget):
    """
    Side panel with simulation controls.
    Implements the Control aspect of the MVC pattern.
    """
    
    # Signals
    mode_changed = pyqtSignal(SimulationMode)
    spawn_object = pyqtSignal(str)  # 'star', 'planet', 'black_hole'
    physics_toggle = pyqtSignal(str, bool)  # setting name, enabled
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_mode = SimulationMode.OBSERVATION
        self.init_ui()
    
    def init_ui(self):
        """Initialize the control panel UI."""
        self.setObjectName("controlPanel")
        
        layout = QVBoxLayout()
        layout.setSpacing(16) # Increased spacing for cleaner look
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header = QLabel("Simulation Controls")
        header.setProperty("class", "section-header")
        layout.addWidget(header)
        
        # Mode selection
        mode_group = self.create_mode_group()
        layout.addWidget(mode_group)
        
        # Object spawner (sandbox mode only)
        self.spawner_group = self.create_spawner_group()
        layout.addWidget(self.spawner_group)
        self.spawner_group.setEnabled(False)
        
        # Physics settings
        physics_group = self.create_physics_group()
        layout.addWidget(physics_group)

        # Spacer before timeline
        layout.addStretch()

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Playback controls
        self.timeline_widget = TimelineWidget()
        layout.addWidget(self.timeline_widget)
        
        self.setLayout(layout)
        self.setMaximumWidth(320) # Slightly wider for better readability
    
    def create_mode_group(self) -> QGroupBox:
        """Create user mode selection group."""
        group = QGroupBox("User Mode")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 24, 12, 12)
        
        self.observation_radio = QRadioButton("Observation Mode")
        self.observation_radio.setToolTip("View and explore simulations without modification")
        
        self.sandbox_radio = QRadioButton("Sandbox Mode")
        self.sandbox_radio.setToolTip("Interactive mode - add and manipulate objects")
        
        self.observation_radio.setChecked(True)
        self.observation_radio.toggled.connect(self.on_mode_changed)
        
        layout.addWidget(self.observation_radio)
        layout.addWidget(self.sandbox_radio)
        
        # Helper text
        desc = QLabel("Switch to Sandbox to interact.")
        desc.setProperty("class", "info")
        layout.addWidget(desc)
        
        group.setLayout(layout)
        return group
    
    def create_spawner_group(self) -> QGroupBox:
        """Create object spawner group."""
        group = QGroupBox("Object Spawner")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 24, 12, 12)
        
        # Grid for buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        # Helper to create buttons
        def create_btn(text, type_key):
            btn = QPushButton(text)
            btn.setStyleSheet(get_button_style("spawn"))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda: self.spawn_object.emit(type_key))
            return btn

        self.spawn_star_btn = create_btn("Star", 'star')
        self.spawn_planet_btn = create_btn("Planet", 'planet')
        
        buttons_layout.addWidget(self.spawn_star_btn)
        buttons_layout.addWidget(self.spawn_planet_btn)
        layout.addLayout(buttons_layout)
        
        self.spawn_blackhole_btn = create_btn("Black Hole", 'black_hole')
        layout.addWidget(self.spawn_blackhole_btn)
        
        group.setLayout(layout)
        return group
    
    def create_physics_group(self) -> QGroupBox:
        """Create physics settings group."""
        group = QGroupBox("Physics Settings")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 24, 12, 12)
        
        self.gravity_lines_cb = QCheckBox("Show Gravity Lines")
        self.collisions_cb = QCheckBox("Enable Collisions")
        self.relativistic_cb = QCheckBox("Relativistic Mode")
        
        self.collisions_cb.setChecked(True)
        
        # Connect signals
        self.gravity_lines_cb.toggled.connect(
            lambda checked: self.physics_toggle.emit('gravity_lines', checked)
        )
        self.collisions_cb.toggled.connect(
            lambda checked: self.physics_toggle.emit('collisions', checked)
        )
        self.relativistic_cb.toggled.connect(
            lambda checked: self.physics_toggle.emit('relativistic', checked)
        )
        
        layout.addWidget(self.gravity_lines_cb)
        layout.addWidget(self.collisions_cb)
        layout.addWidget(self.relativistic_cb)
        
        group.setLayout(layout)
        return group
    
    def on_mode_changed(self, checked: bool):
        """Handle mode change."""
        if self.observation_radio.isChecked():
            self.current_mode = SimulationMode.OBSERVATION
            self.spawner_group.setEnabled(False)
        else:
            self.current_mode = SimulationMode.SANDBOX
            self.spawner_group.setEnabled(True)
        
        self.mode_changed.emit(self.current_mode)
    
    def set_mode(self, mode: SimulationMode):
        """Set the current mode programmatically."""
        if mode == SimulationMode.OBSERVATION:
            self.observation_radio.setChecked(True)
        else:
            self.sandbox_radio.setChecked(True)
