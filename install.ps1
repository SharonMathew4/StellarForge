# StellarForge Installation Script for Windows PowerShell
# This script automates the installation process

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  StellarForge Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
            Write-Host "✗ Python 3.10+ required. Please upgrade Python." -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10+." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if virtual environment exists
Write-Host "Setting up virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "  Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = ".\venv\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    try {
        & $activateScript
        Write-Host "✓ Virtual environment activated" -ForegroundColor Green
    } catch {
        Write-Host "! Could not activate automatically. You may need to run:" -ForegroundColor Yellow
        Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Gray
        Write-Host "  Then run this script again." -ForegroundColor Gray
        exit 1
    }
} else {
    Write-Host "✗ Activation script not found" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ pip upgraded" -ForegroundColor Green
} else {
    Write-Host "! pip upgrade failed, continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray

$packages = @(
    "PyQt6>=6.6.0",
    "vispy>=0.14.0",
    "numpy>=1.24.0",
    "scipy>=1.11.0",
    "astropy>=5.3.0",
    "noise>=1.2.2",
    "mesa>=2.1.0",
    "h5py>=3.10.0",
    "pyopengl>=3.1.6",
    "pillow>=10.0.0"
)

$failed = @()
foreach ($package in $packages) {
    $packageName = $package.Split(">=")[0]
    Write-Host "  Installing $packageName..." -ForegroundColor Gray
    pip install $package --quiet
    if ($LASTEXITCODE -ne 0) {
        $failed += $packageName
    }
}

Write-Host ""

if ($failed.Count -eq 0) {
    Write-Host "✓ All dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "! Some packages failed to install:" -ForegroundColor Yellow
    foreach ($pkg in $failed) {
        Write-Host "  - $pkg" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "You can try installing them manually:" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Gray
}

Write-Host ""

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
$verifyScript = @"
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
"@

$result = python -c $verifyScript
if ($result -eq "SUCCESS") {
    Write-Host "✓ Installation verified" -ForegroundColor Green
} else {
    Write-Host "✗ Verification failed: $result" -ForegroundColor Red
    Write-Host "  Some packages may not be installed correctly." -ForegroundColor Yellow
}

Write-Host ""

# Create data directories if they don't exist
Write-Host "Creating data directories..." -ForegroundColor Yellow
$directories = @("data", "config")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created $dir/" -ForegroundColor Green
    } else {
        Write-Host "✓ $dir/ already exists" -ForegroundColor Green
    }
}

Write-Host ""

# Installation complete
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run StellarForge:" -ForegroundColor Yellow
Write-Host "  1. Make sure virtual environment is activated:" -ForegroundColor Gray
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "  2. Run the application:" -ForegroundColor Gray
Write-Host "     python main.py" -ForegroundColor White
Write-Host ""
Write-Host "  Or use the quick start script:" -ForegroundColor Gray
Write-Host "     python run.py --demo" -ForegroundColor White
Write-Host ""
Write-Host "For CUDA/GPU backend:" -ForegroundColor Gray
Write-Host "  - Install NVIDIA CUDA Toolkit 11.8" -ForegroundColor White
Write-Host "  - Build the C++ engine (see docs/QUICKSTART.md)" -ForegroundColor White
Write-Host "" 
Write-Host "For more information, see:" -ForegroundColor Gray
Write-Host "  - README.md (full documentation)" -ForegroundColor White
Write-Host "  - QUICKSTART.md (quick start guide)" -ForegroundColor White
Write-Host "  - ARCHITECTURE.md (architecture overview)" -ForegroundColor White
Write-Host ""
Write-Host "Happy cosmic exploration! 🌌" -ForegroundColor Cyan
Write-Host ""
