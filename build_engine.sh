#!/bin/bash
# Build script for StellarForge C++ Engine on Linux

set -e  # Exit on error

echo "========================================="
echo "StellarForge C++ Engine Build Script"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"

# Check for CMake
if ! command -v cmake &> /dev/null; then
    echo -e "${RED}ERROR: CMake not found. Please install CMake 3.18+${NC}"
    exit 1
fi

# Check for g++
if ! command -v g++ &> /dev/null; then
    echo -e "${RED}ERROR: g++ not found. Please install a C++ compiler${NC}"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 not found${NC}"
    exit 1
fi

# Check for CUDA (optional)
USE_CUDA="ON"
if ! command -v nvcc &> /dev/null; then
    echo -e "${YELLOW}WARNING: CUDA not found. Building without CUDA support${NC}"
    USE_CUDA="OFF"
else
    echo -e "${GREEN}CUDA found: $(nvcc --version | head -n 1)${NC}"
fi

# Check for OpenMP (optional but recommended)
if g++ -fopenmp -x c++ -E - < /dev/null &> /dev/null; then
    echo -e "${GREEN}OpenMP support detected${NC}"
else
    echo -e "${YELLOW}WARNING: OpenMP not detected. Multi-threading may be limited${NC}"
fi

# Check for pybind11
echo -e "${YELLOW}Checking for pybind11...${NC}"
if python3 -c "import pybind11" 2>/dev/null; then
    echo -e "${GREEN}pybind11 found via Python${NC}"
else
    echo -e "${YELLOW}pybind11 not found in Python. Will use bundled version if available${NC}"
    
    # Check if we need to clone pybind11
    if [ ! -d "external/pybind11" ]; then
        echo -e "${YELLOW}Cloning pybind11...${NC}"
        mkdir -p external
        git clone --depth 1 --branch v2.11.1 https://github.com/pybind/pybind11.git external/pybind11
    fi
fi

# Navigate to cpp_engine directory
cd "$(dirname "$0")/cpp_engine"

# Create build directory
echo -e "${GREEN}Creating build directory...${NC}"
mkdir -p build
cd build

# Configure with CMake
echo -e "${GREEN}Configuring with CMake...${NC}"
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_CUDA=${USE_CUDA} \
    -DUSE_OPENMP=ON \
    -DUSE_OPENGL_COMPUTE=OFF \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# Build
echo -e "${GREEN}Building C++ engine...${NC}"
make -j$(nproc)

# Install Python module
echo -e "${GREEN}Installing Python module...${NC}"
make install

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Build completed successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"

# Test if module can be imported
cd ../..
if python3 -c "from src.engine_bridge import stellarforge_cpp_engine; print('Module imported successfully')" 2>/dev/null; then
    echo -e "${GREEN}✓ C++ engine module is importable${NC}"
else
    echo -e "${YELLOW}⚠ Module built but import test failed. You may need to adjust PYTHONPATH${NC}"
fi

echo ""
echo "To use the C++ engine in StellarForge:"
echo "  from engine_bridge import CppEngine"
echo "  engine = CppEngine(backend='cuda')  # or 'openmp', 'opengl'"
echo ""
echo "Backend options:"
echo "  - 'single': Single-threaded CPU"
echo "  - 'openmp': Multi-threaded CPU (fastest CPU option)"
if [ "$USE_CUDA" == "ON" ]; then
    echo "  - 'cuda': NVIDIA CUDA GPU acceleration"
fi
echo "  - 'opengl': OpenGL compute shaders (not yet implemented)"
