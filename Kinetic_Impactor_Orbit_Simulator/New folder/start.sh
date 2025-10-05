#!/bin/bash

# Kinetic Impactor Simulator Startup Script

echo "🚀 Starting Kinetic Impactor Simulator..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the Flask application
echo "Starting Flask application..."
echo "🌐 Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"

python app.py
