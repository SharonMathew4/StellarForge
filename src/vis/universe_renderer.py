"""
Main universe renderer using VisPy SceneCanvas.
Handles the 3D visualization of particles with error handling.
"""

import numpy as np
from vispy import scene
from vispy.scene import visuals
from typing import Optional

from core.exceptions import RenderingError, DataValidationError
from core.error_logger import get_error_logger, ErrorSeverity


class UniverseRenderer:
    """
    High-performance 3D renderer using VisPy.
    Renders particles as a point cloud with colors.
    Includes comprehensive error handling and validation.
    """
    
    def __init__(self, canvas: scene.SceneCanvas):
        """
        Initialize the renderer with error handling.
        
        Args:
            canvas: VisPy SceneCanvas to render on
            
        Raises:
            RenderingError: If renderer initialization fails
        """
        self.error_logger = get_error_logger()
        
        try:
            if canvas is None:
                raise RenderingError(
                    "Canvas cannot be None",
                    context={'canvas': None}
                )
            
            self.canvas = canvas
            
            try:
                self.view = canvas.central_widget.add_view()
            except Exception as view_error:
                self.error_logger.log_exception(
                    view_error,
                    component="RENDERER_INIT",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'view_creation'}
                )
                raise RenderingError(
                    "Failed to create view",
                    cause=view_error
                )
            
            try:
                # Setup camera with turntable controller
                self.camera = scene.TurntableCamera(
                    fov=60,
                    distance=150,
                    elevation=30,
                    azimuth=45
                )
                self.view.camera = self.camera
            except Exception as camera_error:
                self.error_logger.log_exception(
                    camera_error,
                    component="RENDERER_INIT",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'camera_setup'}
                )
                raise RenderingError(
                    "Failed to setup camera",
                    cause=camera_error
                )
            
            try:
                # Create markers visual for particles
                self.markers = visuals.Markers()
                self.markers.set_gl_state('translucent', blend=True, depth_test=True)
                self.view.add(self.markers)
            except Exception as markers_error:
                self.error_logger.log_exception(
                    markers_error,
                    component="RENDERER_INIT",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'markers_creation'}
                )
                raise RenderingError(
                    "Failed to create markers visual",
                    cause=markers_error
                )
            
            try:
                # Add axis for reference
                self.axis = visuals.XYZAxis(parent=self.view.scene)
                
                # Grid for reference (optional, can be toggled)
                self.grid = visuals.GridLines()
                self.grid.parent = self.view.scene
                self.grid.visible = False
            except Exception as visual_error:
                self.error_logger.log_exception(
                    visual_error,
                    component="RENDERER_INIT",
                    severity=ErrorSeverity.WARNING,
                    context={'stage': 'axis_grid_creation'}
                )
                # Don't fail if axis/grid fails
            
            # Data
            self.positions: Optional[np.ndarray] = None
            self.colors: Optional[np.ndarray] = None
            self.sizes: Optional[np.ndarray] = None
            
            # Rendering settings
            self.point_size = 5.0
            self.show_axis = True
            self.show_grid = False
            
            self.error_logger.log_error(
                "Renderer initialized successfully",
                component="RENDERER_INIT",
                severity=ErrorSeverity.INFO
            )
        
        except RenderingError:
            raise
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="RENDERER_INIT",
                severity=ErrorSeverity.CRITICAL
            )
            raise RenderingError(
                f"Renderer initialization failed: {str(e)}",
                cause=e
            )
    
    def update_particles(self, positions: np.ndarray, 
                        colors: Optional[np.ndarray] = None,
                        sizes: Optional[np.ndarray] = None):
        """
        Update particle positions and colors with validation.
        
        Args:
            positions: Array of shape (N, 3) with x, y, z coordinates
            colors: Array of shape (N, 3) or (N, 4) with RGB or RGBA values
            sizes: Array of shape (N,) with point sizes (optional)
            
        Raises:
            RenderingError: If update fails
            DataValidationError: If data is invalid
        """
        try:
            # Validate positions
            if positions is None:
                raise DataValidationError(
                    "Positions array cannot be None",
                    context={'positions': None}
                )
            
            if len(positions) == 0:
                self.error_logger.log_error(
                    "Empty positions array received",
                    component="RENDERER_UPDATE",
                    severity=ErrorSeverity.WARNING
                )
                return
            
            try:
                # Validate positions array shape and type; keep float32 to avoid copies
                positions = np.asarray(positions, dtype=np.float32)
                if positions.ndim != 2 or positions.shape[1] != 3:
                    raise DataValidationError(
                        f"Positions must be shape (N, 3), got {positions.shape}",
                        context={'shape': positions.shape}
                    )
                
                # Check for NaN or Inf values
                if np.any(~np.isfinite(positions)):
                    self.error_logger.log_error(
                        "Invalid values (NaN/Inf) in positions array",
                        component="RENDERER_UPDATE",
                        severity=ErrorSeverity.WARNING,
                        context={'particle_count': len(positions)}
                    )
                    # Replace invalid values with zero
                    positions = np.nan_to_num(positions, nan=0.0, posinf=0.0, neginf=0.0)
                
                self.positions = positions
            
            except DataValidationError:
                raise
            except Exception as pos_error:
                self.error_logger.log_exception(
                    pos_error,
                    component="RENDERER_UPDATE",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'positions_validation'}
                )
                raise DataValidationError(
                    f"Invalid positions data: {str(pos_error)}",
                    cause=pos_error
                )
            
            try:
                # Handle colors
                if colors is None:
                    if self.colors is None or len(self.colors) != len(positions):
                        colors = np.ones((len(positions), 3), dtype=np.float32)
                    else:
                        colors = self.colors
                else:
                    colors = np.asarray(colors, dtype=np.float32)
                    
                    # Validate colors shape
                    if colors.shape[0] != len(positions):
                        raise DataValidationError(
                            f"Colors array length ({colors.shape[0]}) doesn't match positions ({len(positions)})",
                            context={'colors_len': colors.shape[0], 'positions_len': len(positions)}
                        )
                    
                    if colors.ndim < 2 or colors.shape[1] not in (3, 4):
                        raise DataValidationError(
                            f"Colors must be shape (N, 3) or (N, 4), got {colors.shape}",
                            context={'shape': colors.shape}
                        )
                
                # Ensure colors are in [0, 1] range
                if np.any(colors > 1.0):
                    colors = colors / 255.0
                
                # Clamp to [0, 1]
                colors = np.clip(colors, 0.0, 1.0)
                
                self.colors = colors
            
            except DataValidationError:
                raise
            except Exception as color_error:
                self.error_logger.log_exception(
                    color_error,
                    component="RENDERER_UPDATE",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'colors_validation'}
                )
                # Use default colors
                self.colors = np.ones((len(positions), 3), dtype=np.float32)
            
            try:
                # Handle sizes
                if sizes is None:
                    if self.sizes is None or len(self.sizes) != len(positions):
                        sizes = np.ones(len(positions), dtype=np.float32) * self.point_size
                    else:
                        sizes = self.sizes
                else:
                    sizes = np.asarray(sizes, dtype=np.float32)
                    if len(sizes) != len(positions):
                        raise DataValidationError(
                            f"Sizes array length doesn't match positions",
                            context={'sizes_len': len(sizes), 'positions_len': len(positions)}
                        )
                
                self.sizes = sizes
            
            except DataValidationError:
                raise
            except Exception as size_error:
                self.error_logger.log_exception(
                    size_error,
                    component="RENDERER_UPDATE",
                    severity=ErrorSeverity.WARNING,
                    context={'stage': 'sizes_validation'}
                )
                # Use default sizes
                self.sizes = np.ones(len(positions)) * self.point_size
            
            try:
                # Update markers (always provide explicit buffers to avoid driver churn)
                self.markers.set_data(
                    pos=self.positions,
                    face_color=self.colors,
                    edge_color=None,
                    size=self.point_size
                )
            except Exception as render_error:
                self.error_logger.log_exception(
                    render_error,
                    component="RENDERER_UPDATE",
                    severity=ErrorSeverity.ERROR,
                    context={'stage': 'markers_update', 'particle_count': len(positions)}
                )
                raise RenderingError(
                    f"Failed to update markers: {str(render_error)}",
                    context={'particle_count': len(positions)},
                    cause=render_error
                )
        
        except (RenderingError, DataValidationError):
            raise
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="RENDERER_UPDATE",
                severity=ErrorSeverity.ERROR
            )
            raise RenderingError(
                f"Particle update failed: {str(e)}",
                cause=e
            )
    
    def clear(self):
        """Clear all particles from the view."""
        self.positions = None
        self.colors = None
        self.sizes = None
        self.markers.set_data(pos=np.zeros((0, 3)))
    
    def set_camera_position(self, distance: float = 150, 
                           elevation: float = 30,
                           azimuth: float = 45):
        """
        Set camera position.
        
        Args:
            distance: Distance from origin
            elevation: Elevation angle in degrees
            azimuth: Azimuth angle in degrees
        """
        if isinstance(self.camera, scene.TurntableCamera):
            self.camera.distance = distance
            self.camera.elevation = elevation
            self.camera.azimuth = azimuth
    
    def zoom(self, factor: float):
        """
        Zoom camera in/out.
        
        Args:
            factor: Zoom factor (>1 zooms in, <1 zooms out)
        """
        if isinstance(self.camera, scene.TurntableCamera):
            self.camera.distance /= factor
    
    def reset_camera(self):
        """Reset camera to default position."""
        self.set_camera_position(distance=150, elevation=30, azimuth=45)
    
    def toggle_axis(self):
        """Toggle visibility of coordinate axis."""
        self.show_axis = not self.show_axis
        self.axis.visible = self.show_axis
    
    def toggle_grid(self):
        """Toggle visibility of reference grid."""
        self.show_grid = not self.show_grid
        self.grid.visible = self.show_grid
    
    def set_point_size(self, size: float):
        """
        Set the size of rendered points.
        
        Args:
            size: Point size in pixels
        """
        self.point_size = size
        if self.positions is not None:
            self.markers.set_data(
                pos=self.positions,
                face_color=self.colors,
                size=self.point_size
            )
    
    def set_background_color(self, color: tuple):
        """
        Set background color.
        
        Args:
            color: RGB or RGBA tuple (values 0-1)
        """
        self.canvas.bgcolor = color
    
    def get_particle_count(self) -> int:
        """Get the number of rendered particles."""
        if self.positions is not None:
            return len(self.positions)
        return 0
    
    def screenshot(self, filename: str):
        """
        Save a screenshot of the current view.
        
        Args:
            filename: Output filename (e.g., 'screenshot.png')
        """
        img = self.canvas.render()
        from vispy.io import write_png
        write_png(filename, img)
