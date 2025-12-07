# C++ Physics Engine Build Instructions

## Overview
The StellarForge C++ physics engine provides high-performance N-body simulation with multiple compute backends:

- **CPU Single-threaded**: For debugging
- **CPU OpenMP**: Multi-threaded CPU (recommended default)
- **CUDA**: NVIDIA GPU acceleration (RTX 3050/4050 support)
- **OpenGL Compute**: Cross-platform GPU compute (planned)

## Prerequisites

### Linux (Ubuntu/Debian/Zorin OS)
```bash
sudo apt update
sudo apt install -y \
    build-essential \
    cmake \
    python3-dev \
    python3-numpy \
    git

# For CUDA support (optional but recommended for RTX GPUs)
# Install CUDA Toolkit from: https://developer.nvidia.com/cuda-downloads
# Or use system package manager:
sudo apt install nvidia-cuda-toolkit

# For OpenMP (usually included with gcc)
# Verify: gcc -fopenmp --version
```

### Windows
```powershell
# Install Visual Studio 2019+ with C++ development tools
# Install CMake: https://cmake.org/download/
# Install Python 3.10+: https://www.python.org/downloads/
# Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
```

## Build Process

### Automatic Build (Linux)
```bash
cd /path/to/StellarForge
chmod +x build_engine.sh
./build_engine.sh
```

### Manual Build (All Platforms)
```bash
cd /path/to/StellarForge

# Clone pybind11 if not system-installed
git clone --depth 1 --branch v2.11.1 https://github.com/pybind/pybind11.git external/pybind11

# Create build directory
cd cpp_engine
mkdir -p build
cd build

# Configure
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_CUDA=ON \
    -DUSE_OPENMP=ON \
    -DUSE_OPENGL_COMPUTE=OFF

# Build
cmake --build . --config Release -j $(nproc)

# Install
cmake --build . --target install
```

### CMake Options
- `-DUSE_CUDA=ON/OFF`: Enable CUDA support (default: ON if nvcc found)
- `-DUSE_OPENMP=ON/OFF`: Enable OpenMP multi-threading (default: ON)
- `-DUSE_OPENGL_COMPUTE=ON/OFF`: Enable OpenGL compute (default: OFF, not yet implemented)
- `-DCMAKE_BUILD_TYPE=Release/Debug`: Build type (Release recommended)

## Verification

### Test Import
```python
python3 << EOF
from src.engine_bridge import CppEngine

engine = CppEngine(backend='openmp')
print(f"✓ C++ engine loaded successfully")
print(f"  Backend: {engine.get_backend()}")

# Test with small simulation
import numpy as np
engine.initialize(100)
engine.set_positions(np.random.randn(100, 3).astype(np.float32) * 10)
engine.set_velocities(np.random.randn(100, 3).astype(np.float32))
engine.set_masses(np.ones(100, dtype=np.float32))
engine.step(0.01)
print(f"✓ Simulation step successful")
EOF
```

### Benchmark
```python
from src.engine_bridge import CppEngine
import numpy as np
import time

# Test with 10,000 particles
engine = CppEngine(backend='cuda')  # or 'openmp'
engine.initialize(10000)
engine.set_positions(np.random.randn(10000, 3).astype(np.float32) * 100)
engine.set_velocities(np.random.randn(10000, 3).astype(np.float32) * 0.1)
engine.set_masses(np.random.rand(10000).astype(np.float32))

# Warmup
for _ in range(5):
    engine.step(0.016)

# Benchmark
start = time.time()
for _ in range(100):
    engine.step(0.016)
elapsed = time.time() - start

metrics = engine.get_performance_metrics()
print(f"Backend: {metrics['backend']}")
print(f"Avg step time: {metrics['step_time_ms']:.2f} ms")
print(f"FPS: {1000.0 / metrics['step_time_ms']:.1f}")
print(f"Total time for 100 steps: {elapsed:.2f}s")
```

## Troubleshooting

### "CUDA not found"
- Ensure CUDA Toolkit is installed: `nvcc --version`
- Check CUDA path: `export PATH=/usr/local/cuda/bin:$PATH`
- Rebuild: `cmake .. -DUSE_CUDA=ON`

### "pybind11 not found"
- Install via pip: `pip install pybind11`
- Or clone to `external/pybind11` as shown above

### "Module not found" when importing
- Check install path: Module should be in `src/engine_bridge/`
- Add to PYTHONPATH: `export PYTHONPATH=/path/to/StellarForge/src:$PYTHONPATH`
- Or install package: `pip install -e .`

### Build errors with CUDA
- Check CUDA architecture: Edit `CMakeLists.txt` line `set(CMAKE_CUDA_ARCHITECTURES ...)`
- RTX 3050: Ampere (86)
- RTX 4050: Ada Lovelace (89)
- Both supported by default in our build

### Performance Issues
- Use `Release` build: `-DCMAKE_BUILD_TYPE=Release`
- Enable optimizations: `-DCMAKE_CXX_FLAGS="-O3 -march=native"`
- For CUDA: Use `cuda` backend, not `openmp`
- Monitor GPU usage: `nvidia-smi -l 1`

## Integration with StellarForge

### Using C++ Engine
Edit `src/gui/main_window.py`:

```python
# Replace MockEngine with CppEngine
from engine_bridge import CppEngine

# In init_engine() method:
self.engine = CppEngine(backend='cuda')  # or 'openmp'
```

### Runtime Backend Selection
```python
# Auto-detect best backend
from engine_bridge import CppEngine

try:
    engine = CppEngine(backend='cuda')
    print("Using CUDA")
except:
    engine = CppEngine(backend='openmp')
    print("Using OpenMP")
```

## Performance Expectations

### RTX 4050 (6GB VRAM, 14 TFLOPS)
- CPU OpenMP: ~1,000 particles @ 60 FPS
- CUDA: ~100,000+ particles @ 60 FPS

### RTX 3050 (6GB VRAM, 9 TFLOPS)  
- CPU OpenMP: ~1,000 particles @ 60 FPS
- CUDA: ~50,000+ particles @ 60 FPS

### CPU Only (Core i5, 8 threads)
- OpenMP: ~1,000 particles @ 60 FPS
- Single-thread: ~100 particles @ 60 FPS

*Note: Actual performance depends on physics parameters (theta, softening) and collision detection settings*

## Next Steps

1. **Optimize CUDA kernels**: Implement Barnes-Hut tree traversal on GPU
2. **OpenGL compute**: Direct GPU-to-GPU data flow with rendering
3. **Advanced collisions**: Spatial hashing, SPH for fluid dynamics
4. **Stellar evolution**: Particle aging and state transitions

## Support

For build issues or questions:
- Check logs in `cpp_engine/build/`
- GitHub Issues: [Repository URL]
- Documentation: `docs/ARCHITECTURE.md`
