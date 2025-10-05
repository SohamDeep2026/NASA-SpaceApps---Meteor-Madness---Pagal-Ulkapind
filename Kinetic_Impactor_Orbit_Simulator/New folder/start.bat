@echo off
echo 🚀 Starting Kinetic Impactor Simulator...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the Flask application
echo Starting Flask application...
echo 🌐 Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server

python app.py
pause
