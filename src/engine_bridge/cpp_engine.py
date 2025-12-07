"""
C++ Physics Engine wrapper for StellarForge.
Provides high-performance N-body simulation with CUDA and OpenGL compute support.
"""

import numpy as np
from typing import Optional, Tuple
import sys

from .simulation_engine import SimulationEngine

try:
    # Import the compiled C++ module
    from . import stellarforge_cpp_engine as cpp_engine
    CPP_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: C++ engine not available: {e}", file=sys.stderr)
    print("Please compile the C++ engine using: cd cpp_engine && mkdir build && cd build && cmake .. && make install", file=sys.stderr)
    CPP_ENGINE_AVAILABLE = False
    cpp_engine = None


class CppEngine(SimulationEngine):
    """
    High-performance C++ physics engine with multi-backend support.
    
    Backends:
    - 'single': Single-threaded CPU (debugging)
    - 'openmp': Multi-threaded CPU with OpenMP (default, fastest CPU)
    - 'cuda': NVIDIA CUDA GPU acceleration (requires CUDA-capable GPU)
    - 'opengl': OpenGL compute shaders (requires OpenGL 4.3+)
    
    The engine automatically falls back to CPU if GPU backends are unavailable.
    """
    
    def __init__(self, backend: str = 'openmp'):
        """
        Initialize the C++ physics engine.
        
        Args:
            backend: Compute backend to use ('single', 'openmp', 'cuda', 'opengl')
        
        Raises:
            ImportError: If C++ engine module is not compiled
        """
        super().__init__()
        
        if not CPP_ENGINE_AVAILABLE:
            raise ImportError(
                "C++ engine not available. Please compile it first:\n"
                "cd cpp_engine && mkdir -p build && cd build && cmake .. && make install"
            )
        
        self.engine = cpp_engine.PhysicsEngine()
        self.backend = backend
        self.initialized = False
    
    def initialize(self, particle_count: int, **kwargs):
        """
        Initialize the engine with a given number of particles.
        
        Args:
            particle_count: Number of particles to simulate
            **kwargs: Additional parameters:
                - backend: Override default backend
                - G: Gravitational constant (default: 1.0)
                - softening: Softening length (default: 0.01)
                - theta: Barnes-Hut theta parameter (default: 0.5)
                - enable_collisions: Enable collision detection (default: False)
        """
        backend = kwargs.get('backend', self.backend)
        
        self.engine.initialize(particle_count, backend)
        self.particle_count = particle_count
        self.initialized = True
        
        # Set physics parameters
        if 'G' in kwargs:
            self.engine.set_gravitational_constant(kwargs['G'])
        if 'softening' in kwargs:
            self.engine.set_softening_length(kwargs['softening'])
        if 'theta' in kwargs:
            self.engine.set_theta(kwargs['theta'])
        if 'enable_collisions' in kwargs:
            self.engine.enable_collisions(kwargs['enable_collisions'])
    
    def step(self, dt: float):
        """
        Advance the simulation by one time step.
        
        Args:
            dt: Time step in simulation units
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized. Call initialize() first.")
        
        self.engine.step(dt)
    
    def get_positions(self) -> np.ndarray:
        """
        Get current particle positions.
        
        Returns:
            Array of shape (N, 3) with x, y, z coordinates
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        return self.engine.get_positions()
    
    def get_velocities(self) -> np.ndarray:
        """
        Get current particle velocities.
        
        Returns:
            Array of shape (N, 3) with vx, vy, vz components
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        return self.engine.get_velocities()
    
    def get_masses(self) -> np.ndarray:
        """
        Get particle masses.
        
        Returns:
            Array of shape (N,) with mass values
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        return self.engine.get_masses()
    
    def set_positions(self, positions: np.ndarray):
        """
        Set particle positions.
        
        Args:
            positions: Array of shape (N, 3)
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        if not isinstance(positions, np.ndarray):
            positions = np.array(positions, dtype=np.float32)
        
        if positions.dtype != np.float32:
            positions = positions.astype(np.float32)
        
        self.engine.set_positions(positions)
    
    def set_velocities(self, velocities: np.ndarray):
        """
        Set particle velocities.
        
        Args:
            velocities: Array of shape (N, 3)
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        if not isinstance(velocities, np.ndarray):
            velocities = np.array(velocities, dtype=np.float32)
        
        if velocities.dtype != np.float32:
            velocities = velocities.astype(np.float32)
        
        self.engine.set_velocities(velocities)
    
    def set_masses(self, masses: np.ndarray):
        """
        Set particle masses.
        
        Args:
            masses: Array of shape (N,)
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        if not isinstance(masses, np.ndarray):
            masses = np.array(masses, dtype=np.float32)
        
        if masses.dtype != np.float32:
            masses = masses.astype(np.float32)
        
        self.engine.set_masses(masses)
    
    def add_particle(self, position: np.ndarray, velocity: np.ndarray,
                    mass: float, particle_type: int = 0):
        """
        Add a new particle to the simulation.
        
        Args:
            position: 3D position [x, y, z]
            velocity: 3D velocity [vx, vy, vz]
            mass: Particle mass
            particle_type: Particle type (0=star, 1=planet, 2=black_hole)
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        pos = np.array(position, dtype=np.float32)
        vel = np.array(velocity, dtype=np.float32)
        
        self.engine.add_particle(pos, vel, float(mass), int(particle_type))
        self.particle_count += 1
    
    def remove_particle(self, index: int):
        """
        Remove a particle from the simulation.
        
        Args:
            index: Index of particle to remove
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        self.engine.remove_particle(index)
        self.particle_count -= 1
    
    def reset(self):
        """Reset the simulation to initial conditions."""
        if self.initialized:
            self.engine.reset()
    
    def get_types(self) -> np.ndarray:
        """
        Get particle types.
        
        Returns:
            Array of shape (N,) with particle types
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        return self.engine.get_types()
    
    def get_colors(self) -> np.ndarray:
        """
        Get particle colors (RGB). 
        Generated from particle types.
        
        Returns:
            Array of shape (N, 3) with RGB colors in [0, 1]
        """
        if not self.initialized:
            raise RuntimeError("Engine not initialized")
        
        types = self.engine.get_types()
        colors = np.zeros((len(types), 3), dtype=np.float32)
        
        # Color mapping (same as MockEngine)
        for i, ptype in enumerate(types):
            if ptype == 0:  # Star
                colors[i] = [1.0, 0.9, 0.7]
            elif ptype == 1:  # Planet
                colors[i] = [0.5, 0.7, 1.0]
            elif ptype == 2:  # Black hole
                colors[i] = [0.8, 0.0, 0.8]
            else:
                colors[i] = [0.8, 0.8, 0.8]
        
        return colors
    
    def get_backend(self) -> str:
        """Get the current compute backend."""
        return self.engine.get_backend()
    
    def set_backend(self, backend: str):
        """
        Change the compute backend.
        
        Args:
            backend: 'single', 'openmp', 'cuda', or 'opengl'
        """
        self.engine.set_backend(backend)
        self.backend = backend
    
    def get_performance_metrics(self) -> dict:
        """
        Get performance metrics for the last simulation step.
        
        Returns:
            Dictionary with timing information
        """
        return {
            'step_time_ms': self.engine.get_last_step_time_ms(),
            'backend': self.get_backend(),
            'particle_count': self.particle_count
        }
