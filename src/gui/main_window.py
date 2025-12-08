"""
Main window for StellarForge application.
Combines all UI components and integrates with VisPy rendering.
Includes comprehensive error handling and diagnostics.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QDockWidget, QMenuBar, QMenu, QFileDialog,
                             QMessageBox, QStatusBar)
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QKeySequence, QAction, QIcon
from vispy import scene, app

from .control_panel import ControlPanel
from .timeline_widget import TimelineWidget
from .info_panel import InfoPanel
from .styles import MAIN_STYLESHEET
from core import AppState, SimulationMode, ScenarioManager
from core.exceptions import (
    EngineInitializationError, RenderingError, SimulationError, UIError
)
from core.error_logger import get_error_logger, ErrorSeverity
from vis import UniverseRenderer
from engine_bridge import MockEngine
from proc_gen import UniverseGenerator

# Try to import C++ engine, fallback to MockEngine
try:
    from engine_bridge import CppEngine
    CPP_ENGINE_AVAILABLE = True
except ImportError:
    CPP_ENGINE_AVAILABLE = False
    CppEngine = None

import numpy as np
import time


class MainWindow(QMainWindow):
    """
    Main application window implementing the View in MVC pattern.
    Integrates PyQt6 UI with VisPy 3D rendering.
    """
    
    def __init__(self, use_cpp_engine=False, backend='openmp'):
        super().__init__()
        
        self.error_logger = get_error_logger()
        
        try:
            # Initialize components
            self.app_state = AppState()
            
            # Initialize physics engine
            if use_cpp_engine and CPP_ENGINE_AVAILABLE:
                try:
                    self.engine = CppEngine(backend=backend)
                    self.error_logger.log_error(
                        f"Using C++ physics engine with backend: {backend}",
                        component="MAIN_WINDOW_INIT",
                        severity=ErrorSeverity.INFO
                    )
                except Exception as e:
                    self.error_logger.log_exception(
                        e,
                        component="CPP_ENGINE_INIT",
                        severity=ErrorSeverity.WARNING
                    )
                    self.error_logger.log_error(
                        "Falling back to MockEngine",
                        component="MAIN_WINDOW_INIT",
                        severity=ErrorSeverity.WARNING
                    )
                    self.engine = MockEngine()
            else:
                if use_cpp_engine and not CPP_ENGINE_AVAILABLE:
                    self.error_logger.log_error(
                        "C++ engine requested but not available. Using MockEngine.",
                        component="MAIN_WINDOW_INIT",
                        severity=ErrorSeverity.WARNING
                    )
                self.engine = MockEngine()
            
            self.scenario_manager = ScenarioManager()
            self.universe_generator = UniverseGenerator()
            
            # UI components
            self.control_panel = None
            self.timeline_widget = None
            self.info_panel = None
            self.renderer = None
            self.canvas = None
            
            # Performance tracking
            self.last_frame_time = time.perf_counter()
            self.frame_times = []
            self.fps = 0.0
            self.ui_update_stride = 4  # Update heavy UI labels every N frames
            self.ui_update_counter = 0
            
            # Update timer
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self.update_simulation)
            self.update_timer.setInterval(16)  # ~60 FPS
            try:
                self.update_timer.setTimerType(Qt.TimerType.PreciseTimer)
            except Exception:
                pass
            
            self.init_ui()
            self.init_engine()
            
            self.error_logger.log_error(
                "MainWindow initialized successfully",
                component="MAIN_WINDOW",
                severity=ErrorSeverity.INFO
            )
        
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="MAIN_WINDOW_INIT",
                severity=ErrorSeverity.CRITICAL
            )
            raise UIError(
                f"Failed to initialize MainWindow: {str(e)}",
                context={'initialization_step': 'constructor'},
                cause=e
            )
    
    def init_ui(self):
        """Initialize the main window UI with error handling."""
        try:
            self.setWindowTitle("StellarForge - Cosmic Simulation")
            self.setGeometry(100, 100, 1280, 720)
            self.setMinimumSize(QSize(1024, 600))
            
            # Apply modern stylesheet from ThemeManager
            try:
                from .theme import theme_manager
                self.setStyleSheet(theme_manager.get_main_stylesheet())
            except Exception as style_error:
                self.error_logger.log_exception(
                    style_error,
                    component="UI_INIT",
                    severity=ErrorSeverity.WARNING,
                    context={'stage': 'stylesheet_loading'}
                )
                # Continue without stylesheet
            
            # Create central widget with VisPy canvas
            central_widget = QWidget()
            central_layout = QVBoxLayout()
            central_layout.setContentsMargins(0, 0, 0, 0)
            
            try:
                # Create VisPy canvas
                self.canvas = scene.SceneCanvas(keys='interactive', show=False)
                self.canvas.native.setParent(central_widget)
                
                # Initialize renderer
                self.renderer = UniverseRenderer(self.canvas)
                self.renderer.set_background_color((0.02, 0.02, 0.05, 1.0))
                
                central_layout.addWidget(self.canvas.native)
            except Exception as canvas_error:
                self.error_logger.log_exception(
                    canvas_error,
                    component="UI_INIT",
                    severity=ErrorSeverity.CRITICAL,
                    context={'stage': 'canvas_creation'}
                )
                raise RenderingError(
                    f"Failed to create VisPy canvas: {str(canvas_error)}",
                    context={'stage': 'canvas_init'},
                    cause=canvas_error
                )
            
            central_widget.setLayout(central_layout)
            self.setCentralWidget(central_widget)
            
            # Create control panel dock
            try:
                self.control_panel = ControlPanel()
                self.control_panel.mode_changed.connect(self.on_mode_changed)
                self.control_panel.spawn_object.connect(self.on_spawn_object)
                self.control_panel.physics_toggle.connect(self.on_physics_toggle)
                
                dock = QDockWidget("Controls", self)
                dock.setObjectName("ControlPanelDock")
                dock.setWidget(self.control_panel)
                dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                QDockWidget.DockWidgetFeature.DockWidgetFloatable)
                dock.setMinimumWidth(280)
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

                # Connect timeline signals from the control panel
                self.timeline_widget = self.control_panel.timeline_widget
                self.timeline_widget.play_pause_clicked.connect(self.on_play_pause)
                self.timeline_widget.reset_clicked.connect(self.on_reset)
                self.timeline_widget.speed_changed.connect(self.on_speed_changed)
            except Exception as control_error:
                self.error_logger.log_exception(
                    control_error,
                    component="UI_INIT",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'control_panel_creation'}
                )
            
            # Create info panel dock
            try:
                self.info_panel = InfoPanel()
                info_dock = QDockWidget("Info", self)
                info_dock.setObjectName("InfoPanelDock")
                info_dock.setWidget(self.info_panel)
                info_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                                     QDockWidget.DockWidgetFeature.DockWidgetFloatable)
                info_dock.setMinimumWidth(280)
                self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, info_dock)
            except Exception as info_error:
                self.error_logger.log_exception(
                    info_error,
                    component="UI_INIT",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'info_panel_creation'}
                )
            
            # Create menu bar
            try:
                self.create_menus()
            except Exception as menu_error:
                self.error_logger.log_exception(
                    menu_error,
                    component="UI_INIT",
                    severity=ErrorSeverity.WARNING,
                    context={'stage': 'menu_creation'}
                )
            
            # Create status bar
            self.statusBar().showMessage("Ready")
            
            self.error_logger.log_error(
                "UI initialized successfully",
                component="UI_INIT",
                severity=ErrorSeverity.INFO
            )
        
        except RenderingError:
            raise
        except UIError:
            raise
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="UI_INIT",
                severity=ErrorSeverity.CRITICAL
            )
            raise UIError(
                f"Failed to initialize UI: {str(e)}",
                cause=e
            )
    
    def create_menus(self):
        """Create application menus."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        new_action = QAction("🆕 New Simulation", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.setStatusTip("Create a new simulation")
        new_action.triggered.connect(self.on_new_simulation)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("💾 Save Scenario", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.setStatusTip("Save current scenario")
        save_action.triggered.connect(self.on_save_scenario)
        file_menu.addAction(save_action)
        
        load_action = QAction("📂 Load Scenario", self)
        load_action.setShortcut(QKeySequence("Ctrl+O"))
        load_action.setStatusTip("Load a saved scenario")
        load_action.triggered.connect(self.on_load_scenario)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("🚪 Exit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("👁 View")
        
        reset_camera_action = QAction("🎥 Reset Camera", self)
        reset_camera_action.setShortcut(QKeySequence("R"))
        reset_camera_action.setStatusTip("Reset camera to default position")
        reset_camera_action.triggered.connect(self.renderer.reset_camera)
        view_menu.addAction(reset_camera_action)
        
        toggle_axis_action = QAction("📐 Toggle Axis", self)
        toggle_axis_action.setShortcut(QKeySequence("A"))
        toggle_axis_action.setStatusTip("Show/hide coordinate axes")
        toggle_axis_action.triggered.connect(self.renderer.toggle_axis)
        view_menu.addAction(toggle_axis_action)
        
        toggle_grid_action = QAction("⊞ Toggle Grid", self)
        toggle_grid_action.setShortcut(QKeySequence("G"))
        toggle_grid_action.setStatusTip("Show/hide reference grid")
        toggle_grid_action.triggered.connect(self.renderer.toggle_grid)
        view_menu.addAction(toggle_grid_action)
        
        view_menu.addSeparator()
        
        fullscreen_action = QAction("🖵 Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.setStatusTip("Toggle fullscreen mode")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        
        about_action = QAction("ℹ About StellarForge", self)
        about_action.setShortcut(QKeySequence("F1"))
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def init_engine(self):
        """Initialize simulation engine with default particles and error handling."""
        try:
            self.error_logger.log_error(
                "Starting universe generation...",
                component="ENGINE_INIT",
                severity=ErrorSeverity.INFO
            )
            
            # Validate engine initialization
            if self.engine is None:
                raise EngineInitializationError(
                    "MockEngine instance is None",
                    context={'step': 'engine_validation'}
                )
            
            try:
                # Use procedural generation
                positions, velocities, types = self.universe_generator.generate_universe(
                    seed=42,
                    volume_size=(32, 32, 32),
                    num_galaxies=3,
                    world_scale=150.0
                )
                
                # Validate generated data
                if positions is None or len(positions) == 0:
                    raise SimulationError(
                        "Universe generator produced empty dataset",
                        context={'volume_size': (32, 32, 32), 'num_galaxies': 3}
                    )
                
                self.error_logger.log_error(
                    f"Universe generated: {len(positions)} particles",
                    component="ENGINE_INIT",
                    severity=ErrorSeverity.INFO,
                    context={'particle_count': len(positions)}
                )
            
            except Exception as gen_error:
                self.error_logger.log_exception(
                    gen_error,
                    component="ENGINE_INIT",
                    severity=ErrorSeverity.ERROR,
                    context={'step': 'universe_generation'}
                )
                raise SimulationError(
                    f"Universe generation failed: {str(gen_error)}",
                    context={'step': 'generation'},
                    cause=gen_error
                )
            
            try:
                # Initialize engine with generated data
                self.engine.initialize(len(positions), distribution='sphere', scale=50.0)
                self.engine.set_positions(positions)
                self.engine.set_velocities(velocities)
            except Exception as init_error:
                self.error_logger.log_exception(
                    init_error,
                    component="ENGINE_INIT",
                    severity=ErrorSeverity.CRITICAL,
                    context={'step': 'engine_initialization', 'particle_count': len(positions)}
                )
                raise EngineInitializationError(
                    f"Engine initialization failed: {str(init_error)}",
                    context={'particle_count': len(positions)},
                    cause=init_error
                )
            
            try:
                # Update app state with validated data
                positions_result = self.engine.get_positions()
                velocities_result = self.engine.get_velocities()
                masses_result = self.engine.get_masses()
                colors_result = self.engine.get_colors()
                types_result = self.engine.get_types()
                
                # Validate all arrays have matching sizes
                expected_size = len(positions)
                arrays = {
                    'positions': positions_result,
                    'velocities': velocities_result,
                    'masses': masses_result,
                    'colors': colors_result,
                    'types': types_result
                }
                
                for name, arr in arrays.items():
                    if arr is None:
                        raise SimulationError(
                            f"Engine returned None for {name}",
                            context={'expected_size': expected_size}
                        )
                    if len(arr) != expected_size:
                        raise SimulationError(
                            f"Array size mismatch for {name}: expected {expected_size}, got {len(arr)}",
                            context={'array': name, 'expected': expected_size, 'actual': len(arr)}
                        )
                
                self.app_state.positions = positions_result
                self.app_state.velocities = velocities_result
                self.app_state.masses = masses_result
                self.app_state.colors = colors_result
                self.app_state.types = types_result
            
            except SimulationError:
                raise
            except Exception as state_error:
                self.error_logger.log_exception(
                    state_error,
                    component="ENGINE_INIT",
                    severity=ErrorSeverity.ERROR,
                    context={'step': 'app_state_update'}
                )
                raise SimulationError(
                    f"Failed to update app state: {str(state_error)}",
                    context={'step': 'state_update'},
                    cause=state_error
                )
            
            try:
                # Initial render
                self.update_visualization()
            except Exception as render_error:
                self.error_logger.log_exception(
                    render_error,
                    component="ENGINE_INIT",
                    severity=ErrorSeverity.ERROR,
                    context={'step': 'initial_rendering'}
                )
                # Don't crash on render error - log and continue
            
            try:
                # Update UI elements
                if self.timeline_widget:
                    self.timeline_widget.update_particle_count(self.app_state.get_particle_count())
                self.statusBar().showMessage(
                    f"Initialized with {self.app_state.get_particle_count()} particles"
                )
            except Exception as ui_error:
                self.error_logger.log_exception(
                    ui_error,
                    component="ENGINE_INIT",
                    severity=ErrorSeverity.WARNING,
                    context={'step': 'ui_update'}
                )
            
            self.error_logger.log_error(
                "Engine initialized successfully",
                component="ENGINE_INIT",
                severity=ErrorSeverity.INFO
            )
        
        except (EngineInitializationError, SimulationError):
            raise
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="ENGINE_INIT",
                severity=ErrorSeverity.CRITICAL
            )
            raise EngineInitializationError(
                f"Engine initialization failed: {str(e)}",
                cause=e
            )
        
    
    def update_simulation(self):
        """Update simulation step with error handling (called by timer)."""
        try:
            # Calculate FPS
            current_time = time.perf_counter()
            frame_time = (current_time - self.last_frame_time) * 1000  # ms
            self.last_frame_time = current_time
            
            # Keep last 30 frame times for smoothing
            self.frame_times.append(frame_time)
            if len(self.frame_times) > 30:
                self.frame_times.pop(0)
            
            # Calculate and display FPS
            try:
                self.ui_update_counter = (self.ui_update_counter + 1) % self.ui_update_stride
                if len(self.frame_times) > 0 and self.ui_update_counter == 0:
                    avg_frame_time = sum(self.frame_times) / len(self.frame_times)
                    self.fps = 1000.0 / avg_frame_time if avg_frame_time > 0 else 0
                    
                    # Update info panel safely at reduced cadence
                    if self.info_panel:
                        self.info_panel.update_fps(self.fps)
                        self.info_panel.update_frame_time(avg_frame_time)
            except Exception as fps_error:
                self.error_logger.log_exception(
                    fps_error,
                    component="SIMULATION_UPDATE",
                    severity=ErrorSeverity.DEBUG,
                    context={'stage': 'fps_calculation'}
                )
            
            if not self.app_state.is_playing:
                return
            
            try:
                # Step the engine
                dt = self.app_state.dt * self.app_state.simulation_speed
                if dt <= 0:
                    raise SimulationError(
                        "Invalid time step",
                        context={'dt': dt, 'speed': self.app_state.simulation_speed}
                    )
                
                self.engine.step(dt)
            except Exception as step_error:
                self.error_logger.log_exception(
                    step_error,
                    component="SIMULATION_UPDATE",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'engine_step', 'dt': dt}
                )
                # Pause simulation on error
                self.update_timer.stop()
                self.app_state.is_playing = False
                if self.timeline_widget:
                    self.timeline_widget.set_playing(False)
                self.statusBar().showMessage("Simulation paused due to error")
                return
            
            try:
                # Update app state with validated data
                new_positions = self.engine.get_positions()
                new_velocities = self.engine.get_velocities()
                
                if new_positions is None or len(new_positions) == 0:
                    raise SimulationError(
                        "Engine returned invalid positions",
                        context={'positions_len': len(new_positions) if new_positions is not None else 0}
                    )
                
                self.app_state.positions = new_positions
                self.app_state.velocities = new_velocities
                self.app_state.update_time(self.app_state.dt)
            
            except SimulationError:
                raise
            except Exception as state_error:
                self.error_logger.log_exception(
                    state_error,
                    component="SIMULATION_UPDATE",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'state_update'}
                )
                raise SimulationError(
                    f"Failed to update app state: {str(state_error)}",
                    cause=state_error
                )
            
            try:
                # Update visualization
                self.update_visualization()
            except RenderingError as render_error:
                self.error_logger.log_exception(
                    render_error,
                    component="SIMULATION_UPDATE",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'rendering'}
                )
                # Continue without visualization update
            except Exception as viz_error:
                self.error_logger.log_exception(
                    viz_error,
                    component="SIMULATION_UPDATE",
                    severity=ErrorSeverity.WARNING,
                    context={'stage': 'visualization_update'}
                )
            
            try:
                # Update UI elements
                if self.timeline_widget and self.ui_update_counter == 0:
                    self.timeline_widget.update_time(self.app_state.current_time)
                if self.info_panel and self.ui_update_counter == 0:
                    self.info_panel.update_active_particles(self.app_state.get_particle_count())
            except Exception as ui_error:
                self.error_logger.log_exception(
                    ui_error,
                    component="SIMULATION_UPDATE",
                    severity=ErrorSeverity.DEBUG,
                    context={'stage': 'ui_update'}
                )
        
        except SimulationError:
            # Already handled
            pass
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="SIMULATION_UPDATE",
                severity=ErrorSeverity.ERROR
            )
    
    def update_visualization(self):
        """Update the 3D visualization."""
        if self.app_state.positions is not None:
            self.renderer.update_particles(
                self.app_state.positions,
                self.app_state.colors
            )
    
    def on_play_pause(self, is_playing: bool):
        """Handle play/pause."""
        self.app_state.is_playing = is_playing
        
        if is_playing:
            self.update_timer.start()
            self.statusBar().showMessage("Simulation running")
        else:
            self.update_timer.stop()
            self.statusBar().showMessage("Simulation paused")
    
    def on_reset(self):
        """Handle reset."""
        self.update_timer.stop()
        self.engine.reset()
        self.app_state.reset()
        
        # Update state
        self.app_state.positions = self.engine.get_positions()
        self.app_state.velocities = self.engine.get_velocities()
        
        self.update_visualization()
        self.statusBar().showMessage("Simulation reset")
    
    def on_speed_changed(self, speed: float):
        """Handle speed change."""
        self.app_state.set_speed(speed)
    
    def on_mode_changed(self, mode: SimulationMode):
        """Handle mode change."""
        self.app_state.set_mode(mode)
        mode_name = "Sandbox" if mode == SimulationMode.SANDBOX else "Observation"
        self.statusBar().showMessage(f"Switched to {mode_name} mode")
    
    def on_spawn_object(self, object_type: str):
        """Handle object spawning in sandbox mode."""
        if self.app_state.mode != SimulationMode.SANDBOX:
            return
        
        # Spawn at random position near camera
        position = np.random.uniform(-20, 20, 3)
        velocity = np.random.uniform(-1, 1, 3)
        mass = 1.0
        
        # Map object type
        type_map = {'star': 0, 'planet': 1, 'black_hole': 2}
        particle_type = type_map.get(object_type, 0)
        
        # Add to engine
        self.engine.add_particle(position, velocity, mass, particle_type)
        
        # Update state
        self.app_state.positions = self.engine.get_positions()
        self.app_state.velocities = self.engine.get_velocities()
        self.app_state.colors = self.engine.get_colors()
        self.app_state.types = self.engine.get_types()
        
        self.update_visualization()
        self.timeline_widget.update_particle_count(self.app_state.get_particle_count())
        self.statusBar().showMessage(f"Added {object_type}")
    
    def on_physics_toggle(self, setting: str, enabled: bool):
        """Handle physics setting toggle."""
        if setting == 'gravity_lines':
            self.app_state.show_gravity_lines = enabled
        elif setting == 'collisions':
            self.app_state.enable_collisions = enabled
        elif setting == 'relativistic':
            self.app_state.relativistic_mode = enabled
        
        self.statusBar().showMessage(f"{setting}: {'ON' if enabled else 'OFF'}")
    
    def on_new_simulation(self):
        """Create a new simulation."""
        # Stop current simulation
        self.update_timer.stop()
        self.app_state.reset()
        
        # Reinitialize engine
        self.init_engine()
        
        self.timeline_widget.set_playing(False)
        self.statusBar().showMessage("New simulation created")
    
    def on_save_scenario(self):
        """Save current scenario."""
        name, ok = QFileDialog.getSaveFileName(
            self,
            "Save Scenario",
            "",
            "Scenario Files (*.json)"
        )
        
        if ok and name:
            scenario_name = name.replace('.json', '').split('/')[-1].split('\\')[-1]
            self.scenario_manager.save_scenario(self.app_state, scenario_name)
            self.statusBar().showMessage(f"Scenario saved: {scenario_name}")
    
    def on_load_scenario(self):
        """Load a saved scenario."""
        scenarios = self.scenario_manager.list_scenarios()
        
        if not scenarios:
            QMessageBox.information(self, "No Scenarios", "No saved scenarios found.")
            return
        
        name, ok = QFileDialog.getOpenFileName(
            self,
            "Load Scenario",
            "data",
            "Settings Files (*_settings.json)"
        )
        
        if ok and name:
            scenario_name = name.replace('_settings.json', '').split('/')[-1].split('\\')[-1]
            
            if self.scenario_manager.load_scenario(scenario_name, self.app_state):
                # Update engine with loaded data
                if self.app_state.positions is not None:
                    self.engine.initialize(len(self.app_state.positions))
                    self.engine.set_positions(self.app_state.positions)
                    self.engine.set_velocities(self.app_state.velocities)
                
                self.update_visualization()
                self.timeline_widget.update_particle_count(self.app_state.get_particle_count())
                self.timeline_widget.update_time(self.app_state.current_time)
                self.statusBar().showMessage(f"Scenario loaded: {scenario_name}")
            else:
                QMessageBox.warning(self, "Load Failed", "Failed to load scenario.")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
            self.statusBar().showMessage("Exited fullscreen mode")
        else:
            self.showFullScreen()
            self.statusBar().showMessage("Entered fullscreen mode (Press F11 to exit)")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About StellarForge",
            "<h2>🌌 StellarForge</h2>"
            "<p><b>Cosmic Simulation Application</b></p>"
            "<p>Built with PyQt6 and VisPy</p>"
            "<p>Features procedural galaxy generation, "
            "N-body simulation, and interactive 3D visualization.</p>"
            "<hr>"
            "<p><i>Explore the cosmos with physics-based simulation</i></p>"
        )
    
    def resizeEvent(self, event):
        """Handle window resize for responsive UI."""
        super().resizeEvent(event)
        
        # Adjust dock sizes based on window size
        width = self.width()
        height = self.height()
        
        # On smaller windows, auto-hide info panel
        if hasattr(self, 'info_panel'):
            info_dock = self.findChild(QDockWidget, "")
            if width < 1200:
                # Consider hiding or minimizing panels
                pass
        
        self.statusBar().showMessage(f"Window: {width}x{height}px", 2000)
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.update_timer.stop()
        
        # Save window geometry
        from PyQt6.QtCore import QSettings
        settings = QSettings("StellarForge", "StellarForge")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        
        event.accept()
    
    def showEvent(self, event):
        """Handle window show event."""
        super().showEvent(event)
        
        # Restore window geometry
        from PyQt6.QtCore import QSettings
        settings = QSettings("StellarForge", "StellarForge")
        geometry = settings.value("geometry")
        window_state = settings.value("windowState")
        
        if geometry:
            self.restoreGeometry(geometry)
        if window_state:
            self.restoreState(window_state)
