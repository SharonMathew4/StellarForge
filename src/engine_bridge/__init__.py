"""
Engine bridge module for connecting to the C++ physics engine.
Contains mock implementations for testing UI without the real engine.
"""

from .simulation_engine import SimulationEngine
from .mock_engine import MockEngine

# Try to import C++ engine (optional - only if compiled)
try:
    from .cpp_engine import CppEngine
    __all__ = ['SimulationEngine', 'MockEngine', 'CppEngine']
except ImportError:
    __all__ = ['SimulationEngine', 'MockEngine']
