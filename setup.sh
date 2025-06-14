#!/bin/bash

# Ensure scripts are executable
chmod +x scripts/*.sh

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -e .

echo "Setup complete! Activate the virtual environment with:"
echo "source venv/bin/activate"
