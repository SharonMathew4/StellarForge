#!/bin/bash
# Build StellarForge C++ Engine with CUDA support
# Run this from a REGULAR terminal (not VS Code flatpak)

set -e

echo "========================================="
echo "Building StellarForge with CUDA Support"
echo "========================================="

# Add CUDA to PATH
export PATH=/usr/local/cuda-12.3/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.3/lib64:$LD_LIBRARY_PATH

# Verify CUDA
echo "Verifying CUDA installation..."
nvcc --version || { echo "ERROR: CUDA not found!"; exit 1; }

# Navigate to project
cd "$(dirname "$0")"
PROJECT_DIR="$(pwd)"

# Check for venv
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found! Run: python3 -m venv venv"
    exit 1
fi

# Use venv python directly
VENV_PYTHON="${PROJECT_DIR}/venv/bin/python3"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "ERROR: Python not found in venv!"
    exit 1
fi

echo "Using Python from venv..."
$VENV_PYTHON --version

# Verify numpy
$VENV_PYTHON -c "import numpy; print('NumPy version:', numpy.__version__)" || { 
    echo "ERROR: NumPy not found! Run: pip install numpy"; 
    exit 1; 
}

# Clean build directory
echo "Cleaning build directory..."
rm -rf cpp_engine/build

# Get Python paths
PYTHON_EXECUTABLE="$VENV_PYTHON"
PYTHON_VERSION=$($VENV_PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_INCLUDE_DIR=$($VENV_PYTHON -c "from sysconfig import get_path; print(get_path('include'))")
NUMPY_INCLUDE_DIR=$($VENV_PYTHON -c "import numpy; print(numpy.get_include())")

echo "Using Python: $PYTHON_EXECUTABLE"
echo "Python version: $PYTHON_VERSION"
echo "Python include: $PYTHON_INCLUDE_DIR"
echo "NumPy include: $NUMPY_INCLUDE_DIR"

# Build with CUDA enabled
echo "Building C++ engine with CUDA..."
cd cpp_engine
mkdir -p build
cd build

cmake .. -DUSE_CUDA=ON \
         -DCMAKE_CUDA_ARCHITECTURES="86;89" \
         -DCMAKE_BUILD_TYPE=Release \
         -DPython3_EXECUTABLE=$PYTHON_EXECUTABLE \
         -DPython3_INCLUDE_DIR=$PYTHON_INCLUDE_DIR \
         -DPython3_NumPy_INCLUDE_DIR=$NUMPY_INCLUDE_DIR

make -j$(nproc)
make install

echo ""
echo "========================================="
echo "✓ Build completed with CUDA support!"
echo "========================================="
echo ""
echo "To run StellarForge with CUDA:"
echo "  python main.py --engine cpp --backend cuda"
echo ""
