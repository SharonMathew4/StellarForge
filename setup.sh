#!/bin/bash

################################################################################
#                                                                              #
#        StellarForge Complete Setup Script for Linux/Unix/macOS              #
#                                                                              #
#   Comprehensive setup: system detection, dependency installation, GPU       #
#   detection, and environment configuration for optimal performance          #
#                                                                              #
################################################################################

set -e

# ============================================================================
# COLOR CODES
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
print_header() {
    echo ""
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║         StellarForge - Complete Setup for Linux/Unix            ║${NC}"
    echo -e "${BOLD}${CYAN}║      GPU-Accelerated N-Body Physics & 3D Visualization         ║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${BLUE}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${CYAN}ℹ${NC} $1"
}

print_section() {
    echo ""
    echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${MAGENTA}  $1${NC}"
    echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# ============================================================================
# START
# ============================================================================
print_header

# ============================================================================
# SYSTEM INFORMATION
# ============================================================================
print_section "System Information Detection"

print_status "Gathering system specifications..."

# OS Info
OS_NAME=$(uname -s)
OS_RELEASE=""
DISTRO=""

case "$OS_NAME" in
    Linux)
        if [ -f /etc/os-release ]; then
            DISTRO=$(grep "^NAME=" /etc/os-release | cut -d'"' -f2)
        elif [ -f /etc/lsb-release ]; then
            DISTRO=$(grep DISTRIB_DESCRIPTION /etc/lsb-release | cut -d'=' -f2 | cut -d'"' -f2)
        fi
        ;;
    Darwin)
        DISTRO=$(sw_vers -productName)
        ;;
esac

KERNEL_VERSION=$(uname -r)
echo -e "  ${CYAN}OS:${NC}                  $DISTRO"
echo -e "  ${CYAN}Kernel:${NC}              $KERNEL_VERSION"
echo -e "  ${CYAN}Architecture:${NC}         $(uname -m)"
echo ""

# CPU Info
print_status "CPU Information:"
if command -v lscpu &> /dev/null; then
    CPU_MODEL=$(lscpu | grep "Model name:" | cut -d':' -f2 | xargs)
    CPU_CORES=$(nproc)
else
    CPU_MODEL=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "Unknown")
    CPU_CORES=$(sysctl -n hw.ncpu 2>/dev/null || echo "Unknown")
fi
echo -e "  ${CYAN}Model:${NC}                $CPU_MODEL"
echo -e "  ${CYAN}Cores:${NC}                $CPU_CORES"
echo ""

# RAM Info
print_status "Memory Information:"
if command -v free &> /dev/null; then
    TOTAL_RAM=$(free -h | awk '/^Mem:/ {print $2}')
    FREE_RAM=$(free -h | awk '/^Mem:/ {print $7}')
else
    TOTAL_RAM=$(sysctl -n hw.memsize | awk '{printf "%.1fGi", $1 / 1024 / 1024 / 1024}')
    FREE_RAM="Unknown"
fi
echo -e "  ${CYAN}Total RAM:${NC}            $TOTAL_RAM"
echo -e "  ${CYAN}Available RAM:${NC}        $FREE_RAM"
echo ""

# GPU Detection
print_status "GPU Detection:"
GPU_DETECTED=0
GPU_NAME=""

if command -v nvidia-smi &> /dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -n1)
    GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -n1)
    GPU_DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits 2>/dev/null | head -n1)
    
    if [ -n "$GPU_NAME" ]; then
        GPU_DETECTED=1
        print_success "NVIDIA GPU Detected"
        echo -e "  ${CYAN}GPU Model:${NC}            $GPU_NAME"
        echo -e "  ${CYAN}GPU Memory:${NC}           ${GPU_MEMORY}MB"
        echo -e "  ${CYAN}Driver Version:${NC}       $GPU_DRIVER"
    else
        print_warning "nvidia-smi found but no GPU detected"
    fi
else
    print_warning "nvidia-smi not found (GPU acceleration unavailable)"
    print_info "Install NVIDIA CUDA Toolkit for GPU support"
fi
echo ""

# ============================================================================
# PREREQUISITE CHECKS
# ============================================================================
print_section "Prerequisite Checks"

print_status "Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found"
    print_info "Install Python 3.10+: sudo apt install python3.10 python3.10-venv"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION installed"
echo ""

print_status "Checking pip..."
if ! python3 -m pip &> /dev/null; then
    print_warning "pip not found, installing..."
    python3 -m ensurepip --default-pip
fi
print_success "pip installed"
echo ""

print_status "Checking git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    print_success "$GIT_VERSION"
else
    print_warning "Git not found (optional)"
fi
echo ""

print_status "Checking CMake..."
if command -v cmake &> /dev/null; then
    CMAKE_VERSION=$(cmake --version | head -n1)
    print_success "$CMAKE_VERSION"
else
    print_warning "CMake not found (optional for C++ engine)"
fi
echo ""

if [ $GPU_DETECTED -eq 1 ]; then
    print_status "Checking CUDA..."
    if command -v nvcc &> /dev/null; then
        CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $5}' | cut -d',' -f1)
        print_success "CUDA Toolkit $CUDA_VERSION installed"
    else
        print_warning "CUDA Toolkit not found (GPU acceleration unavailable)"
        print_info "Download from: https://developer.nvidia.com/cuda-downloads"
    fi
    echo ""
fi

# ============================================================================
# VIRTUAL ENVIRONMENT
# ============================================================================
print_section "Virtual Environment Setup"

if [ -d ".venv" ]; then
    print_success "Virtual environment found"
else
    print_status "Creating virtual environment..."
    python3 -m venv .venv
    print_success "Virtual environment created"
fi

print_status "Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated"
echo ""

# ============================================================================
# DEPENDENCIES
# ============================================================================
print_section "Installing Python Dependencies"

print_status "Upgrading pip..."
pip install --upgrade pip -q
print_success "pip upgraded"
echo ""

PACKAGES=(
    "PyQt6>=6.6.0"
    "vispy>=0.14.0"
    "numpy>=1.24.0"
    "scipy>=1.11.0"
    "h5py>=3.10.0"
    "trimesh>=4.0.0"
    "pillow>=10.0.0"
    "noise>=1.2.2"
)

for package in "${PACKAGES[@]}"; do
    print_status "Installing: $package"
    pip install "$package" -q
    print_success "$package installed"
done
echo ""

# ============================================================================
# COMPLETION
# ============================================================================
print_section "Setup Complete!"

print_success "StellarForge is ready to run!"
echo ""

echo -e "${BOLD}${GREEN}System Configuration:${NC}"
echo -e "  ${CYAN}OS:${NC}                    $DISTRO"
echo -e "  ${CYAN}CPU:${NC}                   $CPU_MODEL ($CPU_CORES cores)"
echo -e "  ${CYAN}RAM:${NC}                   $TOTAL_RAM"
if [ $GPU_DETECTED -eq 1 ]; then
    echo -e "  ${CYAN}GPU:${NC}                   $GPU_NAME"
fi
echo -e "  ${CYAN}Python:${NC}                $PYTHON_VERSION"
echo ""

echo -e "${BOLD}${GREEN}To Launch StellarForge:${NC}"
echo -e "  source .venv/bin/activate"
if [ $GPU_DETECTED -eq 1 ]; then
    echo -e "  python3 main.py --engine cpp --backend cuda"
else
    echo -e "  python3 main.py --engine mock --backend openmp"
fi
echo ""

echo -e "${BOLD}${GREEN}Or use the universal launcher:${NC}"
echo -e "  ./launch.sh"
echo ""

print_success "Enjoy your cosmic simulation!"
echo ""
