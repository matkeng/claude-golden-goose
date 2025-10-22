#!/bin/bash
# Setup script for Conda environment

echo "Setting up Claude Golden Goose with Conda..."

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda is required but not installed. Please install Anaconda or Miniconda."
    exit 1
fi

# Create conda environment
echo "Creating conda environment..."
conda create -n claude-golden-goose python=3.10 -y

# Activate conda environment
echo "Activating conda environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate claude-golden-goose

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your API keys and configuration."
fi

echo ""
echo "Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  conda activate claude-golden-goose"
echo ""
echo "To start the Django project setup, run:"
echo "  python manage.py migrate"
echo "  python manage.py createsuperuser"
echo "  python manage.py runserver"
