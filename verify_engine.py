#!/usr/bin/env python3
"""
Verification script for StellarForge C++ Engine installation.
Tests import, basic functionality, and performance.
"""

import sys
import time
from pathlib import Path
import numpy as np

# Add src directory to path (same pattern as main.py)
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def print_status(message, status="INFO"):
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}{message}{colors['RESET']}")

def test_import():
    """Test if C++ engine can be imported."""
    print_status("=== Testing C++ Engine Import ===", "INFO")
    
    try:
        from engine_bridge.cpp_engine import CppEngine
        print_status("✓ CppEngine imported successfully", "SUCCESS")
        return True, CppEngine
    except ImportError as e:
        print_status(f"✗ Failed to import CppEngine: {e}", "ERROR")
        print_status("  Make sure you've built the engine: ./build_engine.sh", "WARNING")
        return False, None

def test_backends(CppEngine):
    """Test available backends."""
    print_status("\n=== Testing Available Backends ===", "INFO")
    
    backends = []
    
    # Test OpenMP (should always work)
    try:
        engine = CppEngine(backend='openmp')
        backend = engine.get_backend()
        print_status(f"✓ OpenMP backend available: {backend}", "SUCCESS")
        backends.append('openmp')
    except Exception as e:
        print_status(f"✗ OpenMP backend failed: {e}", "ERROR")
    
    # Test CUDA
    try:
        engine = CppEngine(backend='cuda')
        backend = engine.get_backend()
        if backend == 'cuda':
            print_status(f"✓ CUDA backend available: {backend}", "SUCCESS")
            backends.append('cuda')
        else:
            print_status(f"⚠ CUDA requested but fell back to: {backend}", "WARNING")
    except Exception as e:
        print_status(f"⚠ CUDA backend not available: {e}", "WARNING")
    
    return backends

def test_basic_simulation(CppEngine, backend='openmp'):
    """Test basic simulation functionality."""
    print_status(f"\n=== Testing Basic Simulation ({backend}) ===", "INFO")
    
    try:
        # Initialize
        engine = CppEngine(backend=backend)
        engine.initialize(100)
        print_status("✓ Engine initialized with 100 particles", "SUCCESS")
        
        # Set particle data
        positions = np.random.randn(100, 3).astype(np.float32) * 10
        velocities = np.random.randn(100, 3).astype(np.float32) * 0.1
        masses = np.ones(100, dtype=np.float32)
        
        engine.set_positions(positions)
        engine.set_velocities(velocities)
        engine.set_masses(masses)
        print_status("✓ Particle data set successfully", "SUCCESS")
        
        # Run simulation
        for i in range(10):
            engine.step(0.016)
        print_status("✓ Simulated 10 steps", "SUCCESS")
        
        # Get results
        new_positions = engine.get_positions()
        new_velocities = engine.get_velocities()
        
        assert new_positions.shape == (100, 3)
        assert new_velocities.shape == (100, 3)
        print_status("✓ Retrieved particle data with correct shapes", "SUCCESS")
        
        # Check that particles moved
        position_change = np.linalg.norm(new_positions - positions)
        if position_change > 0.001:
            print_status(f"✓ Particles moved (Δ={position_change:.4f})", "SUCCESS")
        else:
            print_status(f"⚠ Particles didn't move much (Δ={position_change:.4f})", "WARNING")
        
        return True
        
    except Exception as e:
        print_status(f"✗ Simulation test failed: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return False

def benchmark(CppEngine, backend='openmp', particle_count=10000, steps=100):
    """Benchmark performance."""
    print_status(f"\n=== Benchmarking {backend} with {particle_count:,} particles ===", "INFO")
    
    try:
        engine = CppEngine(backend=backend)
        engine.initialize(particle_count)
        
        # Generate data
        positions = np.random.randn(particle_count, 3).astype(np.float32) * 100
        velocities = np.random.randn(particle_count, 3).astype(np.float32) * 0.1
        masses = np.random.rand(particle_count).astype(np.float32)
        
        engine.set_positions(positions)
        engine.set_velocities(velocities)
        engine.set_masses(masses)
        
        # Warmup
        print_status("  Warming up...", "INFO")
        for _ in range(10):
            engine.step(0.016)
        
        # Benchmark
        print_status(f"  Running {steps} steps...", "INFO")
        start = time.time()
        for _ in range(steps):
            engine.step(0.016)
        elapsed = time.time() - start
        
        # Results
        metrics = engine.get_performance_metrics()
        avg_step_time = metrics['step_time_ms']
        fps = 1000.0 / avg_step_time if avg_step_time > 0 else 0
        total_time = elapsed
        
        print_status(f"  Average step time: {avg_step_time:.2f} ms", "INFO")
        print_status(f"  Effective FPS: {fps:.1f}", "INFO")
        print_status(f"  Total time: {total_time:.2f} s", "INFO")
        print_status(f"  Steps per second: {steps/total_time:.1f}", "INFO")
        
        if fps >= 60:
            print_status(f"✓ Excellent performance! 60+ FPS", "SUCCESS")
        elif fps >= 30:
            print_status(f"✓ Good performance! 30+ FPS", "SUCCESS")
        else:
            print_status(f"⚠ Low performance: {fps:.1f} FPS", "WARNING")
        
        return True, metrics
        
    except Exception as e:
        print_status(f"✗ Benchmark failed: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return False, None

def main():
    """Run all verification tests."""
    print_status("=" * 60, "INFO")
    print_status("StellarForge C++ Engine Verification", "INFO")
    print_status("=" * 60, "INFO")
    
    # Test import
    success, CppEngine = test_import()
    if not success:
        sys.exit(1)
    
    # Test backends
    backends = test_backends(CppEngine)
    if not backends:
        print_status("\n✗ No backends available!", "ERROR")
        sys.exit(1)
    
    # Test basic simulation
    all_passed = True
    for backend in backends:
        if not test_basic_simulation(CppEngine, backend):
            all_passed = False
    
    # Benchmark
    if 'cuda' in backends:
        print_status("\n=== CUDA Performance Benchmark ===", "INFO")
        benchmark(CppEngine, 'cuda', 10000, 100)
        benchmark(CppEngine, 'cuda', 50000, 50)
    
    if 'openmp' in backends:
        print_status("\n=== OpenMP Performance Benchmark ===", "INFO")
        benchmark(CppEngine, 'openmp', 1000, 100)
        benchmark(CppEngine, 'openmp', 10000, 100)
    
    # Final summary
    print_status("\n" + "=" * 60, "INFO")
    if all_passed:
        print_status("✓ All tests passed! C++ engine is ready to use.", "SUCCESS")
        print_status("\nTo use in StellarForge:", "INFO")
        print_status("  python main.py --engine cpp --backend cuda", "INFO")
        print_status("  python main.py --engine cpp --backend openmp", "INFO")
    else:
        print_status("✗ Some tests failed. Check errors above.", "ERROR")
        sys.exit(1)
    print_status("=" * 60, "INFO")

if __name__ == "__main__":
    main()
