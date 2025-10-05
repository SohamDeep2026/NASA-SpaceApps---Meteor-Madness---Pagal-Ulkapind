import pandas as pd
import numpy as np
import requests
import json
from astropy import units as u
from astropy.time import Time
from astropy import constants as const
from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit
from poliastro.twobody.angles import M_to_E, E_to_nu
from poliastro.frames import Planes
from poliastro.plotting import OrbitPlotter3D
from poliastro.maneuver import Maneuver
import plotly.graph_objects as go
import plotly

class KineticImpactorCalculator:
    """Class to handle kinetic impactor calculations and visualizations"""
    
    def __init__(self):
        self.asteroid_data = None
        self.original_orbit = None
        self.final_orbit = None
    
    def fetch_asteroid_data(self, spk_id, api_key='DEMO_KEY'):
        """Fetch asteroid data from NASA API"""
        url = f'https://api.nasa.gov/neo/rest/v1/neo/{spk_id}?api_key={api_key}'
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.asteroid_data = response.json()
            return self.asteroid_data
        except requests.exceptions.RequestException as e:
            print(f'Error fetching data: {e}')
            return None
    
    def calculate_orbital_elements(self, data):
        """Extract and calculate orbital elements from API data"""
        # Extract orbital parameters
        a = float(data['orbital_data']['semi_major_axis']) * u.AU
        ecc = float(data['orbital_data']['eccentricity']) * u.one
        inc = float(data['orbital_data']['inclination']) * u.deg
        raan = float(data['orbital_data']['ascending_node_longitude']) * u.deg
        argp = float(data['orbital_data']['perihelion_argument']) * u.deg
        ma = float(data['orbital_data']['mean_anomaly']) * u.deg
        epo = Time(float(data['orbital_data']['epoch_osculation']), format='jd', scale='tdb')
        
        # Convert mean anomaly to true anomaly
        ea = M_to_E(ma, ecc)
        nu = E_to_nu(ea, ecc)
        
        # Create orbit object
        orbit = Orbit.from_classical(
            attractor=Sun,
            a=a, ecc=ecc, inc=inc, raan=raan, argp=argp, nu=nu,
            epoch=epo, plane=Planes.EARTH_ECLIPTIC
        )
        
        return orbit
    
    def calculate_asteroid_properties(self, data):
        """Calculate asteroid diameter and mass"""
        # Calculate average diameter
        diam_max = float(data['estimated_diameter']['meters']['estimated_diameter_max'])
        diam_min = float(data['estimated_diameter']['meters']['estimated_diameter_min'])
        diameter = (diam_max + diam_min) / 2 * u.m
        
        return diameter
    
    def calculate_impact(self, data, direction_mode, craft_mass, craft_vel, ast_density, beta):
        """Calculate the kinetic impact effects"""
        # Get orbital elements
        self.original_orbit = self.calculate_orbital_elements(data)
        
        # Calculate asteroid properties
        diameter = self.calculate_asteroid_properties(data)
        ast_mass = (4/3) * np.pi * (diameter / 2) ** 3 * (ast_density * u.kg / u.m**3)
        
        # Get position and velocity vectors
        r_ast, v_ast = self.original_orbit.rv()
        v_hat = v_ast / np.linalg.norm(v_ast)
        r_hat = r_ast / np.linalg.norm(r_ast)
        
        # Calculate delta-v based on direction mode
        craft_mass_u = craft_mass * u.kg
        craft_vel_u = craft_vel * u.m / u.s
        
        if direction_mode == '1':  # Along velocity
            dv = ((beta * craft_mass_u * craft_vel_u) / ast_mass) * v_hat
        elif direction_mode == '2':  # Against velocity
            dv = -((beta * craft_mass_u * craft_vel_u) / ast_mass) * v_hat
        else:  # Radial direction
            dv = ((beta * craft_mass_u * craft_vel_u) / ast_mass) * r_hat
        
        # Apply maneuver
        maneuver = Maneuver.impulse(dv)
        self.final_orbit = self.original_orbit.apply_maneuver(maneuver)
        
        # Calculate orbital changes
        orbital_changes = self.calculate_orbital_changes()
        
        return {
            'diameter': float(diameter.to(u.m).value),
            'mass': float(ast_mass.to(u.kg).value),
            'delta_v': [float(x) for x in dv.to(u.m/u.s).value],  # Convert to list
            'delta_v_magnitude': float(np.linalg.norm(dv.to(u.m/u.s).value)),
            'orbital_changes': orbital_changes,
            'original_orbit': self.original_orbit,
            'final_orbit': self.final_orbit
        }
    
    def calculate_orbital_changes(self):
        """Calculate changes in orbital elements"""
        orig_elements = {
            'semi_major_axis': float(self.original_orbit.a.to(u.AU).value),
            'eccentricity': float(self.original_orbit.ecc.value),
            'inclination': float(self.original_orbit.inc.to(u.deg).value),
            'period': float(self.original_orbit.period.to(u.day).value)
        }
        
        final_elements = {
            'semi_major_axis': float(self.final_orbit.a.to(u.AU).value),
            'eccentricity': float(self.final_orbit.ecc.value),
            'inclination': float(self.final_orbit.inc.to(u.deg).value),
            'period': float(self.final_orbit.period.to(u.day).value)
        }
        
        changes = {}
        for key in orig_elements:
            change_val = final_elements[key] - orig_elements[key]
            percent_change = (change_val / orig_elements[key]) * 100 if orig_elements[key] != 0 else 0
            
            changes[key] = {
                'original': orig_elements[key],
                'final': final_elements[key],
                'change': change_val,
                'percent_change': percent_change
            }
        
        return changes
    
    def create_orbit_plot(self, results):
        """Create 3D orbit visualization using Plotly"""
        try:
            # Sample points along both orbits
            times = np.linspace(0, float(results['original_orbit'].period.to(u.day).value), 100) * u.day
            
            # Original orbit points
            orig_positions = []
            for t in times:
                pos = results['original_orbit'].propagate(t).r
                orig_positions.append([
                    float(pos[0].to(u.km).value), 
                    float(pos[1].to(u.km).value), 
                    float(pos[2].to(u.km).value)
                ])
            
            orig_positions = np.array(orig_positions)
            
            # Final orbit points
            final_positions = []
            for t in times:
                pos = results['final_orbit'].propagate(t).r
                final_positions.append([
                    float(pos[0].to(u.km).value), 
                    float(pos[1].to(u.km).value), 
                    float(pos[2].to(u.km).value)
                ])
            
            final_positions = np.array(final_positions)
            
            # Create 3D plot
            fig = go.Figure()
            
            # Add Sun at origin
            fig.add_trace(go.Scatter3d(
                x=[0], y=[0], z=[0],
                mode='markers',
                marker=dict(size=10, color='yellow'),
                name='Sun'
            ))
            
            # Original orbit
            fig.add_trace(go.Scatter3d(
                x=orig_positions[:, 0].tolist(),
                y=orig_positions[:, 1].tolist(),
                z=orig_positions[:, 2].tolist(),
                mode='lines',
                line=dict(color='red', width=4),
                name='Original Orbit'
            ))
            
            # Final orbit
            fig.add_trace(go.Scatter3d(
                x=final_positions[:, 0].tolist(),
                y=final_positions[:, 1].tolist(),
                z=final_positions[:, 2].tolist(),
                mode='lines',
                line=dict(color='green', width=4),
                name='Modified Orbit'
            ))
            
            fig.update_layout(
                title='Kinetic Impactor Effect on Asteroid Orbit',
                scene=dict(
                    xaxis_title='X (km)',
                    yaxis_title='Y (km)',
                    zaxis_title='Z (km)',
                    aspectmode='cube'
                ),
                showlegend=True
            )
            
            return plotly.io.to_json(fig)
            
        except Exception as e:
            print(f"Error creating plot: {e}")
            return "{}"