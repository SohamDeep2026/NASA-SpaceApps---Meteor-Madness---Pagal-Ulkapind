# Kinetic Impactor Simulator

A Flask web application that simulates the effects of kinetic impactor missions on asteroid orbits. This tool converts the original Jupyter notebook into an interactive web interface.

## Features

- 🚀 Interactive web interface for kinetic impactor simulations
- 📊 3D orbital visualizations using Plotly
- 🌌 Real asteroid data from NASA's Near Earth Object API
- 📈 Detailed orbital change analysis
- 💻 Responsive design for desktop and mobile

## Installation

1. **Clone or download this project**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **This code runs into some issues on newer versions of Python, It is recommended to use this on Python 3.10.11.**

## Usage

1. **Start the Flask application:**
   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Enter simulation parameters:**
   - **Asteroid SPK ID**: Unique identifier for the target asteroid (e.g., 2000433 for Eros)
   - **NASA API Key**: Use "DEMO_KEY" for testing or get a free API key from NASA (https://api.nasa.gov/)
   - **Impact Direction**: Choose whether to impact along velocity, against velocity, or radially
   - **Impactor Mass**: Mass of the kinetic impactor spacecraft in kg
   - **Impact Velocity**: Velocity of impact in m/s
   - **Asteroid Density**: Estimated density of the asteroid in kg/m³
   - **Momentum Enhancement Factor**: Beta parameter for momentum transfer efficiency

4. **View Results:**
   - Asteroid properties (diameter, mass)
   - Applied delta-V vector
   - Orbital element changes
   - Interactive 3D orbit visualization

## Example Asteroids

- **2000433** - Eros
- **2001627** - Ivar  
- **2001916** - Boreas
- **2002063** - Bacchus

## File Structure

```
kinetic_impactor/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Main form interface
│   └── results.html      # Results display page
├── static/
│   ├── css/
│   │   └── style.css     # Application styling
│   └── js/
│       └── app.js        # Frontend JavaScript
├── utils/
│   ├── __init__.py
│   └── calculations.py   # Orbital mechanics calculations
└── README.md             # This file
```

## API Dependencies

- **NASA Near Earth Object API**: Provides asteroid orbital data
- **Poliastro**: Python library for orbital mechanics calculations
- **Plotly**: Interactive 3D plotting library

## Technical Details

The application uses:
- **Flask** for the web framework
- **Astropy** for astronomical calculations and unit handling
- **Poliastro** for orbital mechanics and propagation
- **Plotly** for interactive 3D orbit visualizations
- **Bootstrap** for responsive UI components


