# StellarForge Windows Quickstart (Windows 10/11)

Technical, command-focused setup for Windows 10/11. Use PowerShell or Windows Terminal. All commands assume the project root is `C:\Users\<you>\StellarForge`.

## Prerequisites

- Windows 10/11 (64-bit)
- Python 3.10+ in PATH (`py -3.10 --version`)
- Git
- CMake 3.20+ (for C++ engine build)
- Visual Studio 2022 (or Build Tools) with Desktop C++ workload
- Optional GPU path: NVIDIA CUDA Toolkit 11.8+ and an RTX GPU (see install steps below)

### Install CUDA Toolkit 11.8 (required for `--backend cuda`)
1) Download: https://developer.nvidia.com/cuda-downloads
2) Select: Windows → x86_64 → Windows 10/11 → exe (network) → CUDA Toolkit 11.8
3) Install with defaults (driver + toolkit). Restart if prompted.
4) Verify in a new PowerShell:
```powershell
nvcc --version
```
If `nvcc` is not found, re-open terminal or add `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin` to PATH.

## 1) Clone the repository
```powershell
cd $HOME\source  # choose any workspace
git clone https://github.com/SharonMathew4/StellarForge.git
cd StellarForge
```

## 2) Create and activate a virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you hit execution-policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 3) Install Python dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Sanity check:
```powershell
python - << 'EOF'
import PyQt6, vispy, numpy
print('PyQt6:', PyQt6.__version__)
print('VisPy:', vispy.__version__)
print('NumPy:', numpy.__version__)
EOF
```

## 4) (Optional) Build the C++ physics engine

### Option A: CPU/OpenMP build
```powershell
build_engine.bat
```

### Option B: CUDA build (GPU acceleration)
Requirements: CUDA Toolkit 11.8+, NVIDIA driver, RTX-class GPU.
```powershell
build_with_cuda.bat
```

### Option C: Manual CMake (fine-grained)
```powershell
cd cpp_engine
mkdir build && cd build
cmake .. -DUSE_CUDA=ON -DUSE_OPENMP=ON -G "Visual Studio 17 2022"
cmake --build . --config Release
cd ..\..
```

After build, the Python extension `stellarforge_cpp_engine*.pyd` is placed in `src/engine_bridge/`.

Verify the binding loads:
```powershell
python - << 'EOF'
from engine_bridge import CppEngine
e = CppEngine(backend='cuda')
print('CppEngine backend:', e.get_backend())
EOF
```

## 5) Run StellarForge

### Mock (no C++ build required)
```powershell
python main.py
```

### C++ engine, CPU multi-threaded (OpenMP)
```powershell
python main.py --engine cpp --backend openmp
```

### C++ engine, CUDA GPU
```powershell
python main.py --engine cpp --backend cuda
```

## 6) Configuration knobs (edit `config/default_settings.json`)
- `window.width/height` — initial window size
- `simulation.default_particle_count` — starting particles
- `simulation.timestep` — integration step size
- `camera` block — initial camera position/zoom

## 7) Troubleshooting (Windows)
- **Python not found**: reopen terminal after installing Python; try `py -3.10 --version`.
- **Execution policy**: run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` once, then re-activate venv.
- **C++ build fails (CUDA)**: ensure CUDA Toolkit 11.8+ is installed and `nvcc --version` works; rebuild from a new `cpp_engine\build` directory.
- **Module not found: stellarforge_cpp_engine**: rebuild with `build_engine.bat` or `build_with_cuda.bat`; confirm `.pyd` exists in `src/engine_bridge`.
- **Black screen in VisPy**: update GPU drivers; as a fallback, set software GL in `main.py`:
	```python
	import vispy
	vispy.use('pyqt6', 'gl2')
	```
- **Slow performance**: reduce particle count, switch to CUDA backend, or lower simulation speed in UI.

## 8) Quick verification checklist
- `python main.py` launches (MockEngine)
- `python main.py --engine cpp --backend openmp` launches after CPU build
- `python main.py --engine cpp --backend cuda` launches after CUDA build
- `python verify_engine.py` reports success (optional script)

## 9) Useful one-liners
```powershell
# Show available backends
python - << 'EOF'
from engine_bridge import MockEngine
try:
		from engine_bridge import CppEngine
		print('CppEngine available')
except ImportError:
		print('CppEngine missing')
EOF

# Measure step timing (requires C++ engine built)
python - << 'EOF'
import numpy as np
from engine_bridge import CppEngine
e = CppEngine(backend='openmp')
e.initialize(50000)
e.step(0.016)
print('Step OK')
EOF
```

This guide keeps Windows users on the fastest path to a working StellarForge installation with both CPU and CUDA backends.
