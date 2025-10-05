from flask import Flask, render_template, request, jsonify
import requests
import numpy as np
import json
from utils.calculations import KineticImpactorCalculator
from plotly import graph_objects as go
import plotly

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with input form"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_impact():
    """Handle kinetic impactor calculations"""
    try:
        # Get form data
        spk_id = request.form.get('spk_id')
        api_key = request.form.get('api_key', 'DEMO_KEY')
        direction_mode = request.form.get('direction_mode')
        craft_mass = float(request.form.get('craft_mass'))
        craft_vel = float(request.form.get('craft_vel'))
        ast_density = float(request.form.get('ast_density'))
        beta = float(request.form.get('beta'))
        
        # Initialize calculator
        calculator = KineticImpactorCalculator()
        
        # Fetch asteroid data
        asteroid_data = calculator.fetch_asteroid_data(spk_id, api_key)
        if not asteroid_data:
            return jsonify({'error': 'Failed to fetch asteroid data'}), 400
            
        # Calculate impact effects
        results = calculator.calculate_impact(
            asteroid_data, direction_mode, craft_mass, 
            craft_vel, ast_density, beta
        )
        
        # Generate 3D plot
        plot_json = calculator.create_orbit_plot(results)
        
        # Prepare response data (ensure all values are JSON serializable)
        response_data = {
            'success': True,
            'asteroid_name': asteroid_data.get('name', 'Unknown'),
            'diameter': float(results['diameter']),
            'mass': float(results['mass']),
            'delta_v': results['delta_v'],  # Already converted to list
            'delta_v_magnitude': float(results['delta_v_magnitude']),
            'plot': plot_json,
            'orbital_changes': results['orbital_changes']  # Already converted to floats
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in calculate_impact: {e}")
        return jsonify({'error': f'Calculation error: {str(e)}'}), 500

@app.route('/results')
def results():
    """Results display page"""
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)