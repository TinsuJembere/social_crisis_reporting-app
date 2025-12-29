# PowerShell setup script for Windows
Write-Host "Setting up Community Crisis Reporting Platform Backend..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "Virtual environment created successfully!" -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "`nCreating .env file from env.example..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host ".env file created! Please update SECRET_KEY in .env" -ForegroundColor Green
} else {
    Write-Host ".env file already exists" -ForegroundColor Yellow
}

# Create uploads directory
if (-not (Test-Path "uploads")) {
    Write-Host "`nCreating uploads directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "uploads" | Out-Null
    Write-Host "Uploads directory created!" -ForegroundColor Green
}

Write-Host "`nSetup complete! Next steps:" -ForegroundColor Green
Write-Host "1. Activate virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "2. Update .env file with your SECRET_KEY" -ForegroundColor Cyan
Write-Host "3. Run migrations: alembic revision --autogenerate -m 'Initial migration'" -ForegroundColor Cyan
Write-Host "4. Apply migrations: alembic upgrade head" -ForegroundColor Cyan
Write-Host "5. Run server: python run.py or uvicorn app.main:app --reload" -ForegroundColor Cyan

