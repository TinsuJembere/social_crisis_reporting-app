#!/bin/bash
# Bash setup script for macOS/Linux
echo "Setting up Community Crisis Reporting Platform Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from env.example..."
    cp env.example .env
    echo ".env file created! Please update SECRET_KEY in .env"
else
    echo ".env file already exists"
fi

# Create uploads directory
if [ ! -d "uploads" ]; then
    echo ""
    echo "Creating uploads directory..."
    mkdir uploads
    echo "Uploads directory created!"
fi

echo ""
echo "Setup complete! Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Update .env file with your SECRET_KEY"
echo "3. Run migrations: alembic revision --autogenerate -m 'Initial migration'"
echo "4. Apply migrations: alembic upgrade head"
echo "5. Run server: python run.py or uvicorn app.main:app --reload"

