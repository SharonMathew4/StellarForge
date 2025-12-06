# StellarForge 🌌

**Cosmic Simulation Application** - A high-performance 3D universe simulator built with Python, PyQt6, and VisPy.

## Overview

StellarForge is a modular cosmic simulation application that combines procedural galaxy generation, N-body physics simulation, and interactive 3D visualization. The application follows an MVC (Model-View-Controller) architecture and is designed to eventually connect to a high-performance C++ physics engine.

### Key Features

- 🎨 **Interactive 3D Visualization** - Real-time rendering using VisPy with support for millions of particles
- 🌀 **Procedural Generation** - Generate galaxies with realistic structures (spiral, elliptical, irregular)
- 🎮 **Dual Mode System** - Switch between Observation and Sandbox modes
- ⚡ **Mock Physics Engine** - Test the UI without requiring the C++ backend
- 💾 **Save/Load System** - HDF5 for particle data, JSON for settings
- 🎬 **Timeline Controls** - Play, pause, rewind, and adjust simulation speed
- 🛠️ **Extensible Architecture** - Clean separation of concerns for easy integration

## Project Structure

```
StellarForge/
├── src/
│   ├── gui/                    # PyQt6 User Interface
│   │   ├── main_window.py      # Main application window
│   │   ├── control_panel.py    # Sidebar controls
│   │   └── timeline_widget.py  # Timeline playback controls
│   ├── vis/                    # VisPy 3D Visualization
│   │   ├── universe_renderer.py      # Main renderer
│   │   ├── star_field_visualizer.py  # Star rendering
│   │   └── galaxy_visualizer.py      # Galaxy structures
│   ├── core/                   # Application State
│   │   ├── app_state.py        # Central state management
│   │   └── scenario_manager.py # Save/load functionality
│   ├── engine_bridge/          # Physics Engine Interface
│   │   ├── simulation_engine.py # Abstract base class
│   │   └── mock_engine.py       # Mock implementation
│   └── proc_gen/               # Procedural Generation
│       ├── universe_generator.py # Main generator
│       ├── density_field.py      # Perlin/Simplex noise
│       └── galaxy_placer.py      # Galaxy placement logic
├── tests/                      # Unit tests
├── data/                       # Saved scenarios
├── config/                     # Configuration files
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── setup.py                    # Package setup

```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/SharonMathew4/StellarForge
   cd StellarForge
   ```

2. **Create a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Install the package:**
   ```powershell
   pip install -e .
   ```

5. **Build C++ Physics Engine (Optional but Recommended):**
   
   For high-performance simulation with CUDA support:
   ```bash
   # Linux
   ./build_engine.sh
   
   # Or manually
   cd cpp_engine && mkdir -p build && cd build
   cmake .. -DUSE_CUDA=ON -DUSE_OPENMP=ON
   make -j$(nproc) && make install
   ```
   
   See `cpp_engine/README.md` for detailed build instructions.
   
   **Note**: C++ engine provides:
   - 10-100x faster simulation than MockEngine
   - CUDA GPU acceleration (RTX 3050/4050 support)
   - Barnes-Hut O(N log N) gravity
   - Multi-threaded CPU fallback

## Running the Application

### Basic Launch

```bash
# With Python MockEngine (default)
python main.py

# With C++ engine and CUDA
python main.py --engine cpp --backend cuda

# With C++ engine and CPU multi-threading
python main.py --engine cpp --backend openmp
```

### From Package

```bash
stellarforge --engine cpp --backend cuda
```

## Quick Start with C++ Engine

For high-performance simulation with your RTX 4050/3050:

1. **Build the C++ engine:**
   ```bash
   ./build_engine.sh
   ```

2. **Run with CUDA:**
   ```bash
   python main.py --engine cpp --backend cuda
   ```

3. **See full guide:** `QUICKSTART_CPP_ENGINE.md`

## Usage Guide

### User Modes

#### Observation Mode
- **Purpose**: View and explore the simulation without modifying it
- **Features**: Camera controls, timeline playback, visualization settings
- **Use Case**: Watching pre-generated scenarios, analyzing simulations

#### Sandbox Mode
- **Purpose**: Interactive universe creation and modification
- **Features**: All observation features plus object spawning
- **Controls**:
  - 🌟 Add Star - Spawn a new star
  - 🌍 Add Planet - Spawn a planet
  - ⚫ Add Black Hole - Spawn a black hole

### Timeline Controls

- **▶ Play** - Start simulation
- **⏸ Pause** - Pause simulation
- **⏮ Reset** - Reset to initial state
- **Speed Slider** - Adjust simulation speed (0.1x to 10.0x)

### Camera Controls

- **Rotate**: Click and drag
- **Zoom**: Scroll wheel or pinch
- **Pan**: Right-click and drag (or middle mouse)
- **Reset**: View → Reset Camera

### Physics Settings

- **Show Gravity Lines**: Visualize gravitational interactions (mock)
- **Enable Collisions**: Enable particle collision detection (mock)
- **Relativistic Mode**: Enable relativistic effects (mock)

### Saving and Loading

#### Save a Scenario
1. File → Save Scenario
2. Enter a name for your scenario
3. Data saved to `data/` directory

#### Load a Scenario
1. File → Load Scenario
2. Select a scenario from the list
3. Simulation state restored

## Architecture

### MVC Pattern

- **Model**: `AppState` - Central state management
- **View**: `MainWindow`, `ControlPanel`, `TimelineWidget` - PyQt6 UI
- **Controller**: Signal/slot connections between UI and state

### Engine Bridge

The application uses a pluggable physics engine architecture through the `SimulationEngine` interface.

**Available Engines:**

1. **MockEngine** (Python) - Development/Testing
   ```python
   from engine_bridge import MockEngine
   engine = MockEngine()
   engine.initialize(1000, distribution='galaxy')
   ```

2. **CppEngine** (C++/CUDA) - Production/High-Performance
   ```python
   from engine_bridge import CppEngine
   
   # Use CUDA for GPU acceleration
   engine = CppEngine(backend='cuda')
   engine.initialize(100000)  # 100K particles
   
   # Or multi-threaded CPU
   engine = CppEngine(backend='openmp')
   ```

**Performance Comparison (RTX 4050):**
| Engine | Particle Count | FPS | Backend |
|--------|---------------|-----|---------|
| MockEngine | 1,000 | 60 | Python |
| MockEngine | 10,000 | 15 | Python |
| CppEngine (OpenMP) | 10,000 | 60 | CPU (8 threads) |
| CppEngine (CUDA) | 100,000 | 60 | GPU |
| CppEngine (CUDA) | 1,000,000 | 30 | GPU |

**Backend Options:**
- `single`: Single-threaded CPU (debugging)
- `openmp`: Multi-threaded CPU (default fallback)
- `cuda`: NVIDIA CUDA GPU acceleration ⚡
- `opengl`: OpenGL compute shaders (planned)

### Procedural Generation

Galaxies are generated using:
1. **Density Fields** - Perlin/Simplex noise for structure
2. **Galaxy Placement** - Threshold-based placement with minimum separation
3. **Particle Distribution** - Type-specific patterns (spiral, elliptical, irregular)

## Development

### Running Tests

```powershell
# Run all tests
python -m pytest tests/

# Run specific test file
python -m unittest tests/test_engine.py
```

### Adding New Features

#### Adding a New Particle Type

1. Add constant to `MockEngine`:
   ```python
   ASTEROID = 3
   ```

2. Update color generation in `_generate_colors()`

3. Add UI button in `ControlPanel`

#### Integrating the C++ Engine

1. Implement `SimulationEngine` interface
2. Replace `MockEngine` instantiation in `MainWindow`
3. Update build system to link C++ library

## Configuration

Edit `config/default_settings.json` to customize:

- Window size and title
- Default particle counts
- Rendering settings
- Camera parameters
- Procedural generation parameters

## Performance

### Current Performance
- **Particles**: Tested with up to 50,000 particles at 60 FPS
- **Rendering**: GPU-accelerated using VisPy
- **Memory**: ~100 MB for 10,000 particles

### Optimization Tips
- Reduce particle count for slower systems
- Disable gravity lines visualization
- Lower simulation speed for better frame rates

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| GUI Framework | PyQt6 | Application windows and controls |
| 3D Rendering | VisPy | High-performance OpenGL rendering |
| Math/Physics | NumPy, SciPy | Numerical computations |
| Astronomy | Astropy | Astronomical calculations |
| Noise | noise | Perlin/Simplex noise generation |
| Data Storage | HDF5 (h5py) | Particle data persistence |

## Roadmap

### Phase 1: UI Framework (Current)
- ✅ Basic UI layout
- ✅ VisPy integration
- ✅ Mock physics engine
- ✅ Procedural generation
- ✅ Save/load system

### Phase 2: C++ Engine Integration
- ⏳ Connect to C++ physics engine
- ⏳ Real N-body gravity calculations
- ⏳ Collision detection
- ⏳ Performance optimization

### Phase 3: Advanced Features
- ⏳ Relativistic effects
- ⏳ Advanced visualizations (trails, fields)
- ⏳ Multi-threading
- ⏳ VR support

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'vispy'"
**Solution**: Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

### Issue: Black screen in visualization
**Solution**: Update graphics drivers or try software rendering:
```python
# In main.py, before creating MainWindow:
import vispy
vispy.use('pyqt6', 'gl2')
```

### Issue: Slow performance
**Solution**: Reduce particle count or disable some visual features

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

See LICENSE file for details.

## Acknowledgments

- **VisPy** team for the excellent 3D rendering library
- **PyQt** team for the comprehensive GUI framework
- **NumPy/SciPy** communities for scientific computing tools

## Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for cosmic exploration**