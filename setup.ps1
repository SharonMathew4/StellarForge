# StellarForge Complete Setup Script for Windows 10/11
# This script handles complete setup: system detection, dependency installation, and GPU optimization
# Run: powershell -ExecutionPolicy Bypass -File setup.ps1

# Set error action
$ErrorActionPreference = "Stop"

# ============================================================================
# COLOR FUNCTIONS
# ============================================================================
function Write-Header {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║         StellarForge - Complete Windows Setup                  ║" -ForegroundColor Cyan
    Write-Host "║      GPU-Accelerated N-Body Physics & 3D Visualization         ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Status {
    param([string]$Message)
    Write-Host "→ $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Cyan
}

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host "  $Title" -ForegroundColor Magenta
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
    Write-Host ""
}

# ============================================================================
# START
# ============================================================================
Write-Header

# ============================================================================
# SYSTEM INFORMATION
# ============================================================================
Write-Section "System Information Detection"

Write-Status "Gathering system specifications..."

try {
    # OS Info
    $OSInfo = Get-ComputerInfo -ErrorAction SilentlyContinue
    $OSName = $OSInfo.OsName
    $OSVersion = $OSInfo.OsVersion
    $OSArch = $OSInfo.OsArchitecture
    
    Write-Host "  OS Name:              $OSName" -ForegroundColor Cyan
    Write-Host "  OS Version:           $OSVersion" -ForegroundColor Cyan
    Write-Host "  Architecture:         $OSArch" -ForegroundColor Cyan
    Write-Host ""
    
    # CPU Info
    Write-Status "CPU Information:"
    $CPUInfo = Get-CimInstance -ClassName Win32_Processor -ErrorAction SilentlyContinue
    $CPUName = $CPUInfo.Name
    $CPUCores = $CPUInfo.NumberOfCores
    $CPUThreads = $CPUInfo.NumberOfLogicalProcessors
    
    Write-Host "  Model:                $CPUName" -ForegroundColor Cyan
    Write-Host "  Physical Cores:       $CPUCores" -ForegroundColor Cyan
    Write-Host "  Logical Processors:   $CPUThreads" -ForegroundColor Cyan
    Write-Host ""
    
    # RAM Info
    Write-Status "Memory Information:"
    $RAMInfo = Get-CimInstance -ClassName Win32_ComputerSystem -ErrorAction SilentlyContinue
    $TotalRAM = [math]::Round($RAMInfo.TotalPhysicalMemory / 1GB, 2)
    $OSMemory = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction SilentlyContinue
    $FreeRAM = [math]::Round($OSMemory.FreePhysicalMemory / 1MB, 2)
    
    Write-Host "  Total RAM:            ${TotalRAM}GB" -ForegroundColor Cyan
    Write-Host "  Available RAM:        ${FreeRAM}MB" -ForegroundColor Cyan
    Write-Host ""
    
    # GPU Detection
    Write-Status "GPU Detection:"
    $GPU = Get-CimInstance -ClassName Win32_VideoController -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "NVIDIA|GeForce|RTX|GTX|Tesla|Quadro" }
    
    if ($GPU) {
        Write-Host "  GPU Found:            $($GPU.Name)" -ForegroundColor Green
        if ($GPU.AdapterRAM) {
            $GPUMemoryGB = [math]::Round($GPU.AdapterRAM / 1GB, 2)
            Write-Host "  GPU Memory:           ${GPUMemoryGB}GB" -ForegroundColor Green
        }
        $GPUDetected = $true
    } else {
        Write-Warning "No NVIDIA GPU detected (CPU-only mode available)"
        $GPUDetected = $false
    }
    Write-Host ""
    
} catch {
    Write-Warning "Could not retrieve all system information"
}

# ============================================================================
# PREREQUISITE CHECKS
# ============================================================================
Write-Section "Prerequisite Checks"

Write-Status "Checking Python..."
try {
    $PythonVersion = python --version 2>&1
    Write-Success "Python installed: $PythonVersion"
} catch {
    Write-Error "Python not found in PATH"
    Write-Info "Download from: https://www.python.org/downloads/"
    Write-Info "Make sure to enable 'Add Python to PATH' during installation"
    exit 1
}
Write-Host ""

Write-Status "Checking Git..."
try {
    $GitVersion = git --version 2>&1
    Write-Success "Git installed: $GitVersion"
} catch {
    Write-Warning "Git not found (optional)"
}
Write-Host ""

Write-Status "Checking CMake..."
$CMakeFound = $false
try {
    $CMakeVersion = cmake --version 2>&1 | Select-Object -First 1
    Write-Success "CMake installed: $CMakeVersion"
    $CMakeFound = $true
} catch {
    Write-Warning "CMake not found (optional - needed for C++ engine)"
}
Write-Host ""

Write-Status "Checking NVIDIA CUDA..."
try {
    $CUDAVersion = nvcc --version 2>&1 | Select-String "release" | Select-Object -First 1
    Write-Success "CUDA Toolkit installed: $CUDAVersion"
} catch {
    if ($GPUDetected) {
        Write-Warning "CUDA Toolkit not found - GPU acceleration unavailable"
        Write-Info "Download from: https://developer.nvidia.com/cuda-downloads"
    } else {
        Write-Info "CUDA not needed (no GPU detected)"
    }
}
Write-Host ""

# ============================================================================
# VIRTUAL ENVIRONMENT
# ============================================================================
Write-Section "Virtual Environment Setup"

if (Test-Path "venv") {
    Write-Success "Virtual environment already exists"
} else {
    Write-Status "Creating virtual environment..."
    python -m venv venv
    Write-Success "Virtual environment created"
}
Write-Host ""

Write-Status "Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"
Write-Success "Virtual environment activated"
Write-Host ""

# ============================================================================
# DEPENDENCIES
# ============================================================================
Write-Section "Installing Python Dependencies"

Write-Status "Upgrading pip..."
python -m pip install --upgrade pip -q
Write-Success "pip upgraded"
Write-Host ""

$Dependencies = @(
    "PyQt6>=6.6.0",
    "vispy>=0.14.0",
    "numpy>=1.24.0",
    "scipy>=1.11.0",
    "h5py>=3.10.0",
    "trimesh>=4.0.0",
    "pillow>=10.0.0",
    "noise>=1.2.2"
)

foreach ($dep in $Dependencies) {
    Write-Status "Installing: $dep"
    pip install $dep -q
    Write-Success "$dep installed"
}
Write-Host ""

# ============================================================================
# COMPLETION
# ============================================================================
Write-Section "Setup Complete!"

Write-Success "StellarForge is ready!"
Write-Host ""

Write-Host "System Configuration:" -ForegroundColor Green
Write-Host "  CPU:                  $CPUName ($CPUCores cores)" -ForegroundColor Cyan
Write-Host "  RAM:                  ${TotalRAM}GB" -ForegroundColor Cyan
Write-Host "  GPU:                  $(if ($GPUDetected) { "$($GPU.Name)" } else { 'No NVIDIA GPU' })" -ForegroundColor Cyan
Write-Host "  Python:               $PythonVersion" -ForegroundColor Cyan
Write-Host ""

Write-Host "To Launch StellarForge:" -ForegroundColor Green
Write-Host "  python main.py --engine mock --backend openmp" -ForegroundColor Yellow
if ($GPUDetected) {
    Write-Host "  python main.py --engine cpp --backend cuda" -ForegroundColor Yellow
}
Write-Host ""

Write-Success "Enjoy your cosmic simulation!"
Write-Host ""
