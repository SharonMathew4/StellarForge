#!/bin/bash

# StellarForge Installation Script for Linux/Unix
# This script sets up a Python virtual environment and installs all dependencies

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================"
echo -e "  StellarForge Installation"
echo -e "========================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo -e "${YELLOW}  Please install Python 3.10 or higher${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}✗ Python $PYTHON_VERSION found, but Python $REQUIRED_VERSION or higher is required${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}  Virtual environment already exists${NC}"
    read -p "  Do you want to recreate it? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment recreated${NC}"
    else
        echo -e "${GRAY}  Using existing virtual environment${NC}"
    fi
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to create virtual environment${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

echo ""

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to activate virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ pip upgraded successfully${NC}"
else
    echo -e "${YELLOW}! pip upgrade had issues (non-critical)${NC}"
fi
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
echo -e "${GRAY}  This may take a few minutes...${NC}"
echo ""

# Package list
packages=(
    "PyQt6>=6.6.0"
    "vispy>=0.14.0"
    "numpy>=1.24.0"
    "scipy>=1.11.0"
    "astropy>=5.3.0"
    "noise>=1.2.2"
    "mesa>=2.1.0"
    "h5py>=3.10.0"
    "pyopengl>=3.1.6"
    "pillow>=10.0.0"
)

failed=()

for package in "${packages[@]}"; do
    packageName="${package%%>=*}"
    echo -e "  Installing ${packageName}..."
    pip install "$package" --quiet
    if [ $? -ne 0 ]; then
        failed+=("$packageName")
    fi
done

echo ""

if [ ${#failed[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All dependencies installed successfully${NC}"
else
    echo -e "${YELLOW}! Some packages failed to install:${NC}"
    for pkg in "${failed[@]}"; do
        echo -e "${RED}  - $pkg${NC}"
    done
    echo ""
    echo -e "${YELLOW}You can try installing them manually:${NC}"
    echo -e "${GRAY}  pip install -r requirements.txt${NC}"
fi

echo ""

# Verify installation
echo -e "${YELLOW}Verifying installation...${NC}"
VERIFY_SCRIPT="
try:
    import PyQt6
    import vispy
    import numpy
    import scipy
    import astropy
    import noise
    import h5py
    print('SUCCESS')
except ImportError as e:
    print(f'FAILED: {e}')
"

result=$(python3 -c "$VERIFY_SCRIPT")
if [ "$result" = "SUCCESS" ]; then
    echo -e "${GREEN}✓ Installation verified${NC}"
else
    echo -e "${RED}✗ Verification failed: $result${NC}"
    echo -e "${YELLOW}  Some packages may not be installed correctly.${NC}"
fi

echo ""

# Create data directories
echo -e "${YELLOW}Creating data directories...${NC}"
directories=("data" "config")
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✓ Created $dir/${NC}"
    else
        echo -e "${GREEN}✓ $dir/ already exists${NC}"
    fi
done

echo ""

# Installation complete
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${YELLOW}To run StellarForge:${NC}"
echo -e "${GRAY}  1. Make sure virtual environment is activated:${NC}"
echo -e "${WHITE}     source venv/bin/activate${NC}"
echo ""
echo -e "${GRAY}  2. Run the application:${NC}"
echo -e "${WHITE}     python main.py${NC}"
echo ""
echo -e "${GRAY}  Or use the launch script:${NC}"
echo -e "${WHITE}     ./launch.sh${NC}"
echo ""
echo -e "${GRAY}For more information, see:${NC}"
echo -e "${WHITE}  - README.md (full documentation)${NC}"
echo -e "${WHITE}  - docs/QUICKSTART.md (quick start guide)${NC}"
echo -e "${WHITE}  - docs/ARCHITECTURE.md (architecture overview)${NC}"
echo ""
echo -e "${CYAN}Happy cosmic exploration! 🌌${NC}"
echo ""
