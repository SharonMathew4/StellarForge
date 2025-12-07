
"""
Mock physics engine for testing the UI without the C++ backend.
Implements simple linear motion for particles with error handling.
"""

import numpy as np
from typing import Optional

from core.exceptions import (
    EngineInitializationError, SimulationError, DataValidationError
)
from core.error_logger import get_error_logger, ErrorSeverity
from .simulation_engine import SimulationEngine


class MockEngine(SimulationEngine):
    """
    Mock simulation engine that generates random particles and updates them
    with simple linear motion. Used for UI testing without the C++ engine.
    Includes comprehensive error handling and validation.
    """
    
    # Particle type constants
    STAR = 0
    PLANET = 1
    BLACK_HOLE = 2
    
    def __init__(self):
        super().__init__()
        self.error_logger = get_error_logger()
        self.positions: Optional[np.ndarray] = None
        self.velocities: Optional[np.ndarray] = None
        self.masses: Optional[np.ndarray] = None
        self.types: Optional[np.ndarray] = None
        self.colors: Optional[np.ndarray] = None
        self.initial_positions: Optional[np.ndarray] = None
        self.initial_velocities: Optional[np.ndarray] = None
    
    def initialize(self, particle_count: int, **kwargs):
        """
        Initialize with random particles.
        
        Args:
            particle_count: Number of particles to create
            **kwargs: Additional parameters:
                - distribution: 'random', 'sphere', 'disk', 'galaxy' (default: 'sphere')
                - scale: Spatial scale factor (default: 50.0)
                - seed: Random seed for reproducibility (default: None)
                
        Raises:
            EngineInitializationError: If initialization fails
        """
        try:
            # Validate inputs
            if particle_count <= 0:
                raise EngineInitializationError(
                    f"Invalid particle count: {particle_count}",
                    context={'particle_count': particle_count}
                )
            
            distribution = kwargs.get('distribution', 'sphere')
            scale = kwargs.get('scale', 50.0)
            seed = kwargs.get('seed', None)
            
            if scale <= 0:
                raise EngineInitializationError(
                    f"Invalid scale: {scale}",
                    context={'scale': scale}
                )
            
            try:
                if seed is not None:
                    np.random.seed(seed)
                
                self.particle_count = particle_count
                
                # Generate positions based on distribution
                try:
                    if distribution == 'sphere':
                        self.positions = self._generate_sphere_distribution(particle_count, scale)
                    elif distribution == 'disk':
                        self.positions = self._generate_disk_distribution(particle_count, scale)
                    elif distribution == 'galaxy':
                        self.positions = self._generate_galaxy_distribution(particle_count, scale)
                    else:  # random
                        self.positions = np.random.uniform(-scale, scale, (particle_count, 3))
                    
                    if self.positions is None or len(self.positions) != particle_count:
                        raise EngineInitializationError(
                            f"Position generation failed: expected {particle_count}, got {len(self.positions) if self.positions is not None else 0}",
                            context={'distribution': distribution, 'particle_count': particle_count}
                        )
                    self.positions = self.positions.astype(np.float32, copy=False)
                except Exception as pos_error:
                    self.error_logger.log_exception(
                        pos_error,
                        component="MOCK_ENGINE_INIT",
                        severity=ErrorSeverity.ERROR,
                        context={'stage': 'position_generation', 'distribution': distribution}
                    )
                    raise EngineInitializationError(
                        f"Failed to generate positions: {str(pos_error)}",
                        cause=pos_error
                    )
                
                # Generate velocities (orbital-ish motion around origin)
                try:
                    self.velocities = self._generate_velocities(self.positions)
                    self.velocities = self.velocities.astype(np.float32, copy=False)
                    if self.velocities is None or len(self.velocities) != particle_count:
                        raise EngineInitializationError(
                            "Velocity generation produced invalid result"
                        )
                except Exception as vel_error:
                    self.error_logger.log_exception(
                        vel_error,
                        component="MOCK_ENGINE_INIT",
                        severity=ErrorSeverity.ERROR,
                        context={'stage': 'velocity_generation'}
                    )
                    raise EngineInitializationError(
                        f"Failed to generate velocities: {str(vel_error)}",
                        cause=vel_error
                    )
                
                # Generate masses (log-normal distribution for realistic variety)
                try:
                    self.masses = np.random.lognormal(0, 1.5, particle_count).astype(np.float32, copy=False)
                    if len(self.masses) != particle_count:
                        raise EngineInitializationError("Mass generation size mismatch")
                except Exception as mass_error:
                    self.error_logger.log_exception(
                        mass_error,
                        component="MOCK_ENGINE_INIT",
                        severity=ErrorSeverity.ERROR,
                        context={'stage': 'mass_generation'}
                    )
                    raise EngineInitializationError(
                        f"Failed to generate masses: {str(mass_error)}",
                        cause=mass_error
                    )
                
                # Assign types and colors
                try:
                    self.types = self._assign_types(particle_count)
                    self.colors = self._generate_colors(self.types).astype(np.float32, copy=False)
                    if len(self.types) != particle_count or len(self.colors) != particle_count:
                        raise EngineInitializationError("Type/color generation size mismatch")
                except Exception as type_error:
                    self.error_logger.log_exception(
                        type_error,
                        component="MOCK_ENGINE_INIT",
                        severity=ErrorSeverity.ERROR,
                        context={'stage': 'type_color_generation'}
                    )
                    raise EngineInitializationError(
                        f"Failed to assign types/colors: {str(type_error)}",
                        cause=type_error
                    )
                
                # Store initial state for reset
                try:
                    self.initial_positions = self.positions.copy()
                    self.initial_velocities = self.velocities.copy()
                except Exception as copy_error:
                    self.error_logger.log_exception(
                        copy_error,
                        component="MOCK_ENGINE_INIT",
                        severity=ErrorSeverity.WARNING,
                        context={'stage': 'initial_state_copy'}
                    )
                
                self.initialized = True
                
                self.error_logger.log_error(
                    f"MockEngine initialized with {particle_count} particles",
                    component="MOCK_ENGINE_INIT",
                    severity=ErrorSeverity.INFO,
                    context={'particle_count': particle_count, 'distribution': distribution}
                )
            
            except EngineInitializationError:
                raise
            except Exception as init_error:
                self.error_logger.log_exception(
                    init_error,
                    component="MOCK_ENGINE_INIT",
                    severity=ErrorSeverity.CRITICAL
                )
                raise EngineInitializationError(
                    f"Engine initialization failed: {str(init_error)}",
                    context={'particle_count': particle_count},
                    cause=init_error
                )
        
        except EngineInitializationError:
            raise
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="MOCK_ENGINE_INIT",
                severity=ErrorSeverity.CRITICAL
            )
            raise EngineInitializationError(
                f"Unexpected error during initialization: {str(e)}",
                cause=e
            )
    
    def _generate_sphere_distribution(self, count: int, scale: float) -> np.ndarray:
        """Generate particles in a spherical distribution with error handling."""
        try:
            # Use rejection sampling for uniform sphere
            positions = []
            max_iterations = count * 10  # Prevent infinite loops
            iterations = 0
            
            while len(positions) < count and iterations < max_iterations:
                remaining = count - len(positions)
                candidate = np.random.uniform(-1, 1, (remaining, 3))
                distances = np.linalg.norm(candidate, axis=1)
                valid = candidate[distances <= 1.0]
                positions.extend(valid)
                iterations += 1
            
            if len(positions) < count:
                self.error_logger.log_error(
                    f"Could not generate enough valid sphere positions",
                    component="POSITION_GENERATION",
                    severity=ErrorSeverity.WARNING,
                    context={'requested': count, 'generated': len(positions)}
                )
            
            result = np.array(positions[:count]) * scale
            if len(result) != count:
                raise DataValidationError(f"Generated {len(result)} positions instead of {count}")
            
            return result
        
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="POSITION_GENERATION",
                severity=ErrorSeverity.ERROR,
                context={'stage': 'sphere_distribution'}
            )
            raise
    
    def _generate_disk_distribution(self, count: int, scale: float) -> np.ndarray:
        """Generate particles in a disk distribution."""
        try:
            r = np.random.exponential(scale * 0.3, count)
            theta = np.random.uniform(0, 2 * np.pi, count)
            z = np.random.normal(0, scale * 0.05, count)
            
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            result = np.column_stack([x, y, z])
            if len(result) != count:
                raise DataValidationError(f"Generated {len(result)} positions instead of {count}")
            
            return result
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="POSITION_GENERATION",
                severity=ErrorSeverity.ERROR,
                context={'stage': 'disk_distribution'}
            )
            raise
    
    def _generate_galaxy_distribution(self, count: int, scale: float) -> np.ndarray:
        """Generate particles in a spiral galaxy distribution."""
        try:
            # Central bulge (30%) and spiral arms (70%)
            bulge_count = int(count * 0.3)
            arm_count = count - bulge_count
            
            if bulge_count > 0:
                # Bulge: spherical distribution
                bulge = self._generate_sphere_distribution(bulge_count, scale * 0.3)
            else:
                bulge = np.empty((0, 3))
            
            # Spiral arms
            r = np.random.exponential(scale * 0.4, arm_count)
            theta = np.random.uniform(0, 4 * np.pi, arm_count)
            # Add spiral pattern
            theta += r / (scale * 0.2) * np.pi
            z = np.random.normal(0, scale * 0.03, arm_count)
            
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            arms = np.column_stack([x, y, z])
            
            result = np.vstack([bulge, arms])
            if len(result) != count:
                raise DataValidationError(f"Generated {len(result)} positions instead of {count}")
            
            return result
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="POSITION_GENERATION",
                severity=ErrorSeverity.ERROR,
                context={'stage': 'galaxy_distribution'}
            )
            raise
    
    def _generate_velocities(self, positions: np.ndarray) -> np.ndarray:
        """Generate orbital velocities around the origin with error handling."""
        try:
            if positions is None or len(positions) == 0:
                raise DataValidationError("Positions array is empty")
            
            # Calculate distance from origin
            r = np.linalg.norm(positions[:, :2], axis=1, keepdims=True)
            r = np.maximum(r, 0.1)  # Avoid division by zero
            
            # Orbital velocity proportional to 1/sqrt(r) (Keplerian)
            v_magnitude = 2.0 / np.sqrt(r)
            
            # Perpendicular direction in XY plane
            vx = -positions[:, 1:2] / r * v_magnitude
            vy = positions[:, 0:1] / r * v_magnitude
            vz = np.random.normal(0, 0.1, (len(positions), 1))
            
            result = np.hstack([vx, vy, vz])
            
            # Validate no NaN values
            if np.any(~np.isfinite(result)):
                self.error_logger.log_error(
                    "Generated velocities contain NaN/Inf values",
                    component="VELOCITY_GENERATION",
                    severity=ErrorSeverity.WARNING
                )
                result = np.nan_to_num(result, nan=0.0, posinf=0.0, neginf=0.0)
            
            return result
        
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="VELOCITY_GENERATION",
                severity=ErrorSeverity.ERROR
            )
            raise
    
    def _assign_types(self, count: int) -> np.ndarray:
        """Assign particle types with error handling."""
        try:
            types = np.random.choice(
                [self.STAR, self.PLANET, self.BLACK_HOLE],
                size=count,
                p=[0.85, 0.14, 0.01]  # 85% stars, 14% planets, 1% black holes
            )
            return types
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="TYPE_ASSIGNMENT",
                severity=ErrorSeverity.ERROR
            )
            raise
    
    def _generate_colors(self, types: np.ndarray) -> np.ndarray:
        """Generate colors based on particle types."""
        colors = np.zeros((len(types), 3))
        
        for i, ptype in enumerate(types):
            if ptype == self.STAR:
                # Stars: Various colors (blue, white, yellow, orange, red)
                temp = np.random.choice([0, 1, 2, 3, 4], p=[0.1, 0.2, 0.4, 0.2, 0.1])
                if temp == 0:  # Blue
                    colors[i] = [0.5, 0.7, 1.0]
                elif temp == 1:  # White
                    colors[i] = [1.0, 1.0, 1.0]
                elif temp == 2:  # Yellow
                    colors[i] = [1.0, 1.0, 0.6]
                elif temp == 3:  # Orange
                    colors[i] = [1.0, 0.7, 0.3]
                else:  # Red
                    colors[i] = [1.0, 0.3, 0.2]
            elif ptype == self.PLANET:
                # Planets: Earth-like colors
                colors[i] = np.random.uniform([0.2, 0.3, 0.5], [0.5, 0.6, 0.8])
            else:  # Black hole
                # Black holes: Purple/magenta
                colors[i] = [0.8, 0.2, 0.8]
        
        return colors
    
    def step(self, dt: float):
        """
        Advance simulation with simple linear motion and error handling.
        
        Args:
            dt: Time step for integration
            
        Raises:
            SimulationError: If simulation step fails
        """
        try:
            if not self.initialized:
                raise SimulationError(
                    "Engine not initialized",
                    context={'initialized': self.initialized}
                )
            
            if dt < 0:
                raise SimulationError(
                    f"Invalid time step: {dt}",
                    context={'dt': dt}
                )
            
            if self.positions is None or self.velocities is None:
                raise SimulationError(
                    "Positions or velocities are None",
                    context={'positions_is_none': self.positions is None,
                            'velocities_is_none': self.velocities is None}
                )
            
            try:
                # Simple Euler integration
                self.positions = self.positions + self.velocities * dt
                
                # Validate positions after update
                if np.any(~np.isfinite(self.positions)):
                    self.error_logger.log_error(
                        "Invalid values in positions after integration",
                        component="SIMULATION_STEP",
                        severity=ErrorSeverity.WARNING
                    )
                    # Replace invalid values
                    self.positions = np.nan_to_num(
                        self.positions, nan=0.0, posinf=0.0, neginf=0.0
                    )
                
                # Optional: Add some gravitational-like acceleration toward origin
                # (very simplified, just for visual effect)
                r = np.linalg.norm(self.positions, axis=1, keepdims=True)
                r = np.maximum(r, 1.0)
                acceleration = -0.5 * self.positions / (r ** 3)
                
                # Check acceleration values
                if np.any(~np.isfinite(acceleration)):
                    self.error_logger.log_error(
                        "Invalid acceleration values",
                        component="SIMULATION_STEP",
                        severity=ErrorSeverity.WARNING
                    )
                    acceleration = np.nan_to_num(
                        acceleration, nan=0.0, posinf=0.0, neginf=0.0
                    )
                
                self.velocities = self.velocities + acceleration * dt
                
                # Validate velocities
                if np.any(~np.isfinite(self.velocities)):
                    self.error_logger.log_error(
                        "Invalid values in velocities after acceleration",
                        component="SIMULATION_STEP",
                        severity=ErrorSeverity.WARNING
                    )
                    self.velocities = np.nan_to_num(
                        self.velocities, nan=0.0, posinf=0.0, neginf=0.0
                    )
            
            except SimulationError:
                raise
            except Exception as step_error:
                self.error_logger.log_exception(
                    step_error,
                    component="SIMULATION_STEP",
                    severity=ErrorSeverity.ERROR,
                    context={'dt': dt, 'particle_count': len(self.positions) if self.positions is not None else 0}
                )
                raise SimulationError(
                    f"Simulation step failed: {str(step_error)}",
                    context={'dt': dt},
                    cause=step_error
                )
        
        except SimulationError:
            raise
        except Exception as e:
            self.error_logger.log_exception(
                e,
                component="SIMULATION_STEP",
                severity=ErrorSeverity.CRITICAL
            )
            raise SimulationError(
                f"Unexpected error in simulation step: {str(e)}",
                cause=e
            )
    
    def get_positions(self) -> np.ndarray:
        """Get current particle positions with validation."""
        if self.positions is None:
            self.error_logger.log_error(
                "Positions array is None",
                component="GET_POSITIONS",
                severity=ErrorSeverity.WARNING
            )
            return np.array([])
        return self.positions
    
    def get_velocities(self) -> np.ndarray:
        """Get current particle velocities."""
        return self.velocities
    
    def get_masses(self) -> np.ndarray:
        """Get particle masses."""
        return self.masses
    
    def get_colors(self) -> np.ndarray:
        """Get particle colors (RGB)."""
        return self.colors
    
    def get_types(self) -> np.ndarray:
        """Get particle types."""
        return self.types
    
    def set_positions(self, positions: np.ndarray):
        """Set particle positions."""
        self.positions = positions.copy()
    
    def set_velocities(self, velocities: np.ndarray):
        """Set particle velocities."""
        self.velocities = velocities.copy()
    
    def add_particle(self, position: np.ndarray, velocity: np.ndarray, 
                    mass: float, particle_type: int = 0):
        """Add a single particle to the simulation."""
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        self.positions = np.vstack([self.positions, position])
        self.velocities = np.vstack([self.velocities, velocity])
        self.masses = np.append(self.masses, mass)
        self.types = np.append(self.types, particle_type)
        
        # Generate color for new particle
        new_color = self._generate_colors(np.array([particle_type]))[0]
        self.colors = np.vstack([self.colors, new_color])
        
        self.particle_count += 1
    
    def remove_particle(self, index: int):
        """Remove a particle from the simulation."""
        if not self.initialized or index >= self.particle_count:
            raise RuntimeError("Invalid particle index")
        
        self.positions = np.delete(self.positions, index, axis=0)
        self.velocities = np.delete(self.velocities, index, axis=0)
        self.masses = np.delete(self.masses, index)
        self.types = np.delete(self.types, index)
        self.colors = np.delete(self.colors, index, axis=0)
        
        self.particle_count -= 1
    
    def reset(self):
        """Reset to initial conditions."""
        if self.initial_positions is not None:
            self.positions = self.initial_positions.copy()
            self.velocities = self.initial_velocities.copy()
