#!/bin/bash

################################################################################
#                                                                              #
#               StellarForge Universal GPU-Aware Launcher                      #
#                                                                              #
#   Automatically detects NVIDIA GPU, checks system status, and launches       #
#   the application with optimal GPU acceleration. Handles errors gracefully.  #
#                                                                              #
################################################################################

# Color codes for beautiful terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Utility functions
print_header() {
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║                 StellarForge - Cosmic Simulation                ║${NC}"
    echo -e "${BOLD}${CYAN}║            GPU-Accelerated N-Body Physics Engine                ║${NC}"
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

# Error handling
cleanup_on_error() {
    echo ""
    print_error "StellarForge encountered an issue"
    echo ""
    print_info "Troubleshooting tips:"
    echo "  1. Ensure virtual environment is set up: ./install.sh"
    echo "  2. Check CUDA installation: nvidia-smi"
    echo "  3. Verify C++ engine built: ls -la src/engine_bridge/*.so"
    echo ""
    exit 1
}

trap cleanup_on_error ERR

# Start
print_header

# Check project directory
print_status "Validating project structure..."
if [ ! -f "main.py" ]; then
    print_error "main.py not found. Are you in the StellarForge directory?"
    exit 1
fi
print_success "Project structure valid"
echo ""

# Check virtual environment
print_section "Virtual Environment Setup"
if [ ! -d ".venv" ]; then
    print_warning "Virtual environment not found"
    print_status "Creating virtual environment..."
    python3 -m venv .venv || {
        print_error "Failed to create virtual environment"
        exit 1
    }
    print_success "Virtual environment created"
else
    print_success "Virtual environment found"
fi

print_status "Activating virtual environment..."
source .venv/bin/activate || {
    print_error "Failed to activate virtual environment"
    exit 1
}
print_success "Virtual environment activated"
echo ""

# GPU Detection
print_section "GPU Detection & Status"

GPU_DETECTED=0
GPU_NAME=""
GPU_MEMORY=""
GPU_DRIVER=""
CUDA_VERSION=""
CUDA_BACKEND="openmp"  # Fallback

# Try to detect NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    print_status "nvidia-smi found - querying GPU..."
    
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -n1)
    GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -n1)
    GPU_DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits 2>/dev/null | head -n1)
    CUDA_VERSION=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader,nounits 2>/dev/null | head -n1)
    
    if [ -n "$GPU_NAME" ]; then
        GPU_DETECTED=1
        CUDA_BACKEND="cuda"
        
        print_success "NVIDIA GPU Detected"
        echo -e "  ${CYAN}GPU Model:${NC}        $GPU_NAME"
        echo -e "  ${CYAN}GPU Memory:${NC}       ${GPU_MEMORY}MB"
        echo -e "  ${CYAN}Driver Version:${NC}   $GPU_DRIVER"
        echo -e "  ${CYAN}Compute Capability:${NC} $CUDA_VERSION"
    else
        print_warning "nvidia-smi failed to detect GPU"
    fi
else
    print_warning "nvidia-smi not found in PATH"
fi

if [ $GPU_DETECTED -eq 0 ]; then
    print_warning "No NVIDIA GPU detected or nvidia-smi unavailable"
    print_info "System will use OpenMP (CPU multi-threading)"
    CUDA_BACKEND="openmp"
fi
echo ""

# Check Dependencies
print_section "Dependency Check"

print_status "Checking Python packages..."
MISSING_PACKAGES=0

# Check core packages
for package in PyQt6 vispy numpy scipy; do
    python3 -c "import $package" 2>/dev/null && \
        print_success "$package installed" || \
        { print_warning "$package missing - will attempt to install"; MISSING_PACKAGES=1; }
done
echo ""

if [ $MISSING_PACKAGES -eq 1 ]; then
    print_status "Installing missing packages..."
    pip install -q PyQt6 vispy numpy scipy h5py trimesh 2>/dev/null || \
        print_warning "Some packages may not have installed properly"
    print_success "Package installation complete"
    echo ""
fi

# Check C++ Engine
print_section "C++ Physics Engine"

if ls src/engine_bridge/*.so &>/dev/null; then
    print_success "C++ engine compiled (.so module found)"
    COMPILED_BACKEND="cpp"
else
    print_warning "C++ engine not compiled"
    print_info "Building C++ engine (this may take a minute)..."
    
    if [ -f "build_engine.sh" ]; then
        bash build_engine.sh > /tmp/stellarforge_build.log 2>&1 && \
            print_success "C++ engine built successfully" || \
            { print_warning "C++ engine build failed (see /tmp/stellarforge_build.log)"; COMPILED_BACKEND="mock"; }
    else
        print_warning "build_engine.sh not found"
        COMPILED_BACKEND="mock"
    fi
fi
echo ""

# Summary and Launch
print_section "Launch Configuration"

echo -e "  ${CYAN}Engine:${NC}            $COMPILED_BACKEND"
echo -e "  ${CYAN}Backend:${NC}           $CUDA_BACKEND"
if [ $GPU_DETECTED -eq 1 ]; then
    echo -e "  ${CYAN}GPU:${NC}               $GPU_NAME"
fi
echo ""

# Prepare launch command
if [ "$COMPILED_BACKEND" = "cpp" ]; then
    LAUNCH_CMD="python3 main.py --engine cpp --backend $CUDA_BACKEND"
else
    LAUNCH_CMD="python3 main.py --engine mock --backend openmp"
fi

# Set CUDA env vars if GPU detected
if [ $GPU_DETECTED -eq 1 ]; then
    export CUDA_VISIBLE_DEVICES=0
    export CUDA_LAUNCH_BLOCKING=0
    print_status "GPU acceleration enabled"
else
    print_status "Using CPU multi-threading (OpenMP)"
fi
echo ""

# Final preparation
print_section "System Information"

# Get detailed system info
PYTHON_VERSION=$(python3 --version 2>&1)
OS_NAME=$(uname -s)
OS_RELEASE=$(cat /etc/os-release 2>/dev/null | grep "^NAME=" | cut -d'"' -f2 || echo "Unknown")
KERNEL_VERSION=$(uname -r)
CPU_MODEL=$(lscpu 2>/dev/null | grep "Model name:" | cut -d':' -f2 | xargs || echo "Unknown")
CPU_CORES=$(nproc)
TOTAL_RAM=$(free -h 2>/dev/null | awk '/^Mem:/ {print $2}' || echo "Unknown")

echo -e "  ${CYAN}System:${NC}"
echo -e "    OS:                 $OS_RELEASE"
echo -e "    Kernel:             $KERNEL_VERSION"
echo ""

echo -e "  ${CYAN}CPU:${NC}"
echo -e "    Model:              $CPU_MODEL"
echo -e "    Cores:              $CPU_CORES"
echo -e "    Total RAM:          $TOTAL_RAM"
echo ""

if [ $GPU_DETECTED -eq 1 ]; then
    echo -e "  ${CYAN}GPU:${NC}"
    echo -e "    Model:              $GPU_NAME"
    echo -e "    Memory:             ${GPU_MEMORY}MB"
    echo -e "    Driver:             $GPU_DRIVER"
    echo -e "    Compute Cap:        $CUDA_VERSION"
    echo ""
else
    echo -e "  ${CYAN}GPU:${NC}"
    echo -e "    Status:             No NVIDIA GPU detected (CPU-only mode)"
    echo ""
fi

echo -e "  ${CYAN}Software:${NC}"
echo -e "    Python:             $PYTHON_VERSION"
echo ""

print_status "Launching StellarForge..."
echo ""

# Launch with error handling
$LAUNCH_CMD || {
    print_error "Application crashed"
    print_info "Exit code: $?"
    print_info "Check the output above for error details"
    exit 1
}

# Post-execution summary
echo ""
print_success "StellarForge closed successfully"
echo ""
