# StellarForge

High-performance N-body cosmic simulation application with GPU acceleration via CUDA and real-time 3D visualization. Built with Python (PyQt6, VisPy) for UI and C++ for physics computation.

## Overview

StellarForge combines procedural galaxy generation with N-body physics simulation using Barnes-Hut octree algorithms. The architecture separates the UI layer (Python/PyQt6) from the compute layer (C++ with optional CUDA acceleration), allowing for efficient parallel simulation of 100k+ particles in real-time.

## Features

- GPU-accelerated N-body physics (CUDA 11.x+)
- Barnes-Hut O(N log N) gravity calculation algorithm
- Real-time 3D rendering with VisPy (OpenGL)
- Procedural galaxy generation (spiral, elliptical, irregular)
- Scenario save/load (HDF5 for particle data, JSON for metadata)
- Dual-mode operation (Observation and Sandbox)
- Timeline controls with adjustable simulation speed
- MVC architecture with pluggable physics backends

## Project Structure

```
StellarForge/
├── src/
│   ├── core/                   # State management and error handling
│   │   ├── app_state.py        # Central state container
│   │   ├── exceptions.py        # Custom exception types
│   │   └── error_logger.py      # Error tracking and logging
│   ├── gui/                    # PyQt6 UI components
│   │   ├── main_window.py      # Main application window
│   │   ├── control_panel.py    # Simulation controls
│   │   └── styles.py           # Stylesheet definitions
│   ├── vis/                    # VisPy visualization layer
│   │   └── universe_renderer.py # Main 3D renderer
│   ├── engine_bridge/          # Physics engine abstraction
│   │   ├── simulation_engine.py # ABC for physics engines
│   │   ├── mock_engine.py       # CPU-only reference implementation
│   │   └── cpp_engine.pyd/.so   # Compiled C++ bindings (after build)
│   └── proc_gen/               # Procedural universe generation
│       ├── universe_generator.py
│       ├── density_field.py
│       └── galaxy_placer.py
├── cpp_engine/                 # C++ physics engine source
│   ├── src/                    # C++ implementation
│   ├── cuda/                   # CUDA kernels
│   ├── include/                # Header files
│   ├── CMakeLists.txt          # Build configuration
│   └── README.md               # Build instructions
├── config/                     # Configuration files
├── data/                       # Saved scenarios (HDF5 + JSON)
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── setup.py                    # Python package setup
```

## Quick Start

### Linux/Unix/macOS Setup

```bash
# Automatic setup (detects system, installs all dependencies)
./setup.sh

# Launch application
./launch.sh
```

The `setup.sh` script automatically:
- Detects your OS and hardware (CPU cores, RAM, GPU)
- Checks Python and dependencies
- Creates virtual environment
- Installs all required packages
- Shows system configuration

The `launch.sh` script automatically:
- Detects NVIDIA GPU and enables CUDA if available
- Falls back to OpenMP (CPU multi-threading) if no GPU
- Shows detailed system information
- Handles any missing dependencies

### Windows 10/11 Setup

```powershell
# Run setup script
powershell -ExecutionPolicy Bypass -File setup.ps1

# Then launch
python main.py --engine mock --backend openmp
# Or with GPU (if NVIDIA GPU available):
python main.py --engine cpp --backend cuda
```

The `setup.ps1` script automatically:
- Detects Windows version and hardware specs
- Checks Python, CMake, CUDA installation
- Creates virtual environment
- Installs all dependencies
- Shows detailed system configuration (CPU/GPU/RAM/OS)

## Manual Installation (if scripts fail)

### Linux/Unix/macOS

```bash
cd StellarForge

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS: same command

# Install dependencies
pip install --upgrade pip
pip install PyQt6 vispy numpy scipy h5py trimesh pillow noise

# Optional: Build C++ engine for better performance
cd cpp_engine && mkdir -p build && cd build
cmake .. && make && make install
cd ../..

# Run application
python3 main.py
```

### Windows 10/11

```powershell
cd StellarForge

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install PyQt6 vispy numpy scipy h5py trimesh pillow noise

# Run application
python main.py
```

## Running the Application

### Default (Mock Physics Engine - CPU)
```bash
python3 main.py  # Linux/macOS
python main.py   # Windows
```

### With C++ Physics Engine + OpenMP (Multi-core CPU)
```bash
python3 main.py --engine cpp --backend openmp
```

### With C++ Physics Engine + CUDA (NVIDIA GPU)
```bash
python3 main.py --engine cpp --backend cuda
```

### Universal Launcher (Auto-detects everything)
```bash
./launch.sh  # Linux/Unix/macOS
```

Windows users can run directly from PowerShell after setup:
```bash
python main.py --engine mock --backend openmp
```

## GPU Acceleration

### NVIDIA GPUs (Recommended)

Supported GPUs: RTX series (3050+), Tesla, Quadro

**Install CUDA Toolkit:**
- Download: https://developer.nvidia.com/cuda-downloads
- Select your OS and follow installation steps
- Verify: `nvidia-smi` should show your GPU

Once CUDA is installed and C++ engine built:
```bash
python3 main.py --engine cpp --backend cuda
```

### CPU-Only Mode

If no GPU available or CUDA not installed:
```bash
python3 main.py --engine mock --backend openmp
```

Uses all available CPU cores via OpenMP - still performs well for 10k-50k particles.

## Troubleshooting

### Python not found
- Linux: `sudo apt install python3.10 python3.10-venv`
- macOS: `brew install python@3.10`
- Windows: Download from https://www.python.org/downloads/ (enable "Add to PATH")

### GPU not detected
- Verify NVIDIA GPU: `nvidia-smi` in system terminal (not VS Code)
- Check CUDA: `nvcc --version`
- On WSL2: GPU support requires special setup

### C++ engine build fails
- Application still works with Python mock engine
- For C++ build: ensure CMake and compiler installed
- Linux: `sudo apt install cmake build-essential`
- macOS: `brew install cmake`
- Windows: Install Visual Studio Build Tools

### VisPy/OpenGL issues
- Update GPU drivers to latest version
- On Linux: `sudo apt install libgl1-mesa-glx`

## System Requirements

### Minimum
- CPU: 4 cores
- RAM: 8GB
- GPU: Optional (OpenMP fallback available)
- Python 3.10+

### Recommended
- CPU: 8+ cores
- RAM: 16GB+
- GPU: NVIDIA RTX 3060+ with 6GB+ VRAM
- Python 3.10+

## Performance Notes

- Mock Engine (Python): ~1000-5000 particles at 60 FPS
- C++ + OpenMP: ~10,000-50,000 particles at 30-60 FPS
- C++ + CUDA: ~100,000+ particles at 30-60 FPS (RTX 4050 with 6GB VRAM)

Actual performance depends on particle density, 3D model complexity, and visualization features enabled.

## Controls

- **Mouse**: Click + drag to rotate camera
- **Scroll**: Zoom in/out
- **Space**: Play/Pause simulation
- **R**: Reset camera
- **Ctrl+L**: Load solar system
- **Ctrl+S**: Save scenario
- **Ctrl+O**: Load scenario
- **Esc**: Exit
mkdir -p build && cd build
cmake .. -DUSE_CUDA=ON -DUSE_OPENMP=ON
make -j$(nproc)
cd ../..
```

5. Run application:
```bash
# With CPU-based mock engine (no build required)
python main.py

# With C++ engine (after build)
python main.py --engine cpp --backend openmp

# With CUDA GPU (RTX 3050/4050)
python main.py --engine cpp --backend cuda
```

### Windows Setup

1. Clone repository:
```cmd
git clone https://github.com/SharonMathew4/StellarForge.git
cd StellarForge
```

2. Create virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install Python dependencies:
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Build C++ physics engine (optional but recommended):

**Prerequisites for C++ build:**
- Install Visual Studio 2022 with C++ workload
- Install CMake from https://cmake.org/download/
- For CUDA: Install CUDA Toolkit from https://developer.nvidia.com/cuda-downloads

**Without CUDA (CPU-only with OpenMP):**
```cmd
build_engine.bat
```

**With CUDA (GPU acceleration):**
```cmd
build_with_cuda.bat
```

Or manually:
```cmd
cd cpp_engine
mkdir build && cd build
cmake .. -DUSE_CUDA=ON -DUSE_OPENMP=ON -G "Visual Studio 17 2022"
cmake --build . --config Release
cd ..\..
```

5. Run application:
```cmd
# With CPU-based mock engine (no build required)
python main.py

# With C++ engine (after build)
python main.py --engine cpp --backend openmp

# With CUDA GPU (RTX 3050/4050)
python main.py --engine cpp --backend cuda
```

## Running the Application

Launch using command line with optional parameters:

```bash
# Default: MockEngine (pure Python, no C++ build required)
python main.py

# With C++ engine and multi-threaded CPU
python main.py --engine cpp --backend openmp

# With GPU acceleration (NVIDIA CUDA)
python main.py --engine cpp --backend cuda

# View available options
python main.py --help
```

## Configuration

Application settings are in `config/default_settings.json`:

- Window dimensions and title
- Default particle counts per galaxy
- Camera zoom and FOV parameters
- Physics simulation timestep
- Procedural generation parameters

Modify as needed for your system specifications.
## Architecture

**Engine Bridge Pattern**: SimulationEngine abstract interface allows swapping physics backends.

Available implementations:
- `MockEngine`: Pure Python, development/testing
- `CppEngine`: C++ with CUDA/OpenMP backends, production

```python
# Optional - C++ bindings only available after successful build
from engine_bridge import CppEngine
engine = CppEngine(backend='cuda')
engine.initialize(100000)  # 100k particles
engine.step(0.016)  # 16ms timestep
positions = engine.get_positions()
```

**Compute Backends**:
- `openmp`: Multi-threaded CPU via OpenMP
- `cuda`: NVIDIA CUDA GPU acceleration
- `single`: Single-threaded CPU (testing only)

## Performance

Tested on RTX 4050:
- MockEngine: 1,000 particles at 60 FPS
- CppEngine (OpenMP): 10,000 particles at 60 FPS
- CppEngine (CUDA): 100,000 particles at 60 FPS
- CppEngine (CUDA): 1,000,000 particles at 30 FPS

## Technology Stack

| Component | Technology |
|-----------|-----------|
| GUI | PyQt6 |
| Visualization | VisPy + OpenGL |
| Physics | C++ with CUDA/OpenMP |
| Python bindings | pybind11 |
| Build system | CMake |
| Data storage | HDF5 |

## Dependencies

### Python
- PyQt6 >= 6.6.0
- NumPy >= 1.24.0
- VisPy >= 0.14.0
- h5py >= 3.10.0
- scipy, astropy, noise

### C++ (optional)
- CMake >= 3.20
- CUDA Toolkit >= 11.8 (optional)
- OpenMP (included with most compilers)

## Troubleshooting

**Black screen in visualization:**
Ensure graphics drivers are current. Update VisPy if needed.

**C++ engine fails to load:**
Verify build completed successfully: `python verify_engine.py`

**Performance issues:**
- Reduce particle count
- Use CUDA backend if available
- Disable timeline visualization features

## License

See LICENSE file.

## References

- C++ engine build: See `cpp_engine/README.md`
- Physics algorithm: Barnes-Hut O(N log N) tree code
- Configuration: `config/default_settings.json`