# StellarForge

High-performance N-body cosmic simulation application with GPU acceleration via CUDA and real-time 3D visualization. Built with Python (PyQt6, VisPy) for UI and C++ for physics computation. StellarForge combines procedural galaxy generation with N-body physics simulation using Barnes-Hut octree algorithms, and the architecture separates the UI layer (Python/PyQt6) from the compute layer (C++ with optional CUDA acceleration), allowing for efficient parallel simulation of 100k+ particles in real-time.


## Technology Stack

### Frontend & UI
- **PyQt6** (v6.6.0+) - Desktop GUI framework with native look-and-feel
- **VisPy** (v0.14.0+) - GPU-accelerated 3D visualization via OpenGL
- **Vispy Visuals** - Mesh and marker rendering primitives
- **OpenGL** - 3D graphics rendering (abstracted by VisPy)

### Backend Physics Engine
- **C++** (C++17 standard) - High-performance N-body physics computation
- **CUDA** (v11.8+) - GPU compute kernels for parallel particle simulation
- **OpenMP** - CPU multi-threading for parallel gravity calculations
- **pybind11** - Python/C++ binding layer for seamless integration

### Core Scientific Computing
- **NumPy** (v1.24.0+) - Numerical arrays, particle data structures
- **SciPy** - Scientific algorithms (optimization, sorting)
- **Astropy** - Astronomical computations and constants
- **Noise** (Perlin/Simplex) - Procedural universe generation

### Data & File I/O
- **HDF5** (via h5py) - Efficient particle data serialization
- **JSON** - Scenario metadata storage
- **GLB/GLTF** - 3D model asset format support
- **Trimesh** - 3D mesh processing and optimization
- **PIL/Pillow** - Texture image processing (PNG, JPG, EXR)

### Physics Algorithms
- **Barnes-Hut Octree** - O(N log N) gravity approximation
- **Verlet Integration** - Stable particle position integration
- **Collision Detection** - AABB spatial partitioning
- **Perlin Noise Fields** - Galaxy density distributions

### Build & Development Tools
- **CMake** (v3.20+) - Cross-platform C++ build system
- **Git** - Version control
- **Python 3.10+** - Runtime environment
- **Virtual Environment** (venv) - Isolated Python dependencies

### Operating System Support
- **Linux** (Ubuntu, Debian, Fedora, Arch, etc.)
- **macOS** (Intel & Apple Silicon)
- **Windows 10/11** (with MSVC or WSL2)

### Hardware Acceleration
- **NVIDIA CUDA** - Support for RTX 3050+, Tesla, Quadro GPUs
- **CUDA Compute Capability 3.5+** - Architecture support
- **6GB+ VRAM** - Recommended for 100k+ particles

### Architecture Pattern
- **MVC** (Model-View-Controller) - Separation of concerns
- **Plugin Architecture** - Swappable physics engines (Mock vs C++)
- **Observer Pattern** - State change propagation
- **Abstraction Layers** - Engine bridge decouples physics from UI

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
- RAM: 12GB+
- GPU: NVIDIA RTX 3050+ with 6GB+ VRAM
- Python 3.10+

## Controls

- **Mouse**: Click + drag to rotate camera
- **Scroll**: Zoom in/out
- **Space**: Play/Pause simulation
- **R**: Reset camera
- **Ctrl+L**: Load solar system
- **Ctrl+S**: Save scenario
- **Ctrl+O**: Load scenario
- **Esc**: Exit

## License

See LICENSE file.

## References

- C++ engine build: See `cpp_engine/README.md`
- Physics algorithm: Barnes-Hut O(N log N) tree code
- Configuration: `config/default_settings.json`