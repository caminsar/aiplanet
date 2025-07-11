from flask import Blueprint, render_template, current_app, jsonify
import requests # For making internal API calls to our own backend

visualization_bp = Blueprint(
    'visualization_bp',
    __name__,
    template_folder='templates', # Points to scientific_analysis_platform/visualization/templates
    static_folder='static',      # Points to scientific_analysis_platform/visualization/static
    url_prefix='/view'           # Optional: prefix for all routes in this blueprint e.g. /view/catalog
)

# Helper to get the base URL for internal API calls to the data API
def get_data_api_base_url():
    return "http://localhost:5000/api/data" # Assuming data_api_bp is at /api/data

# Helper to get the base URL for internal API calls to the EKG API
def get_ekg_api_base_url():
    return "http://localhost:5000/api/ekg" # Assuming ekg_api_bp is at /api/ekg


@visualization_bp.route('/')
def home():
    """Main page for the visualization section."""
    return render_template('visualization_home.html', title='Visualization Hub')

@visualization_bp.route('/map')
def map_page():
    """Page for map visualization."""
    return render_template('map_placeholder.html', title='Interactive Map')

@visualization_bp.route('/chart')
def chart_page():
    """Page for chart visualization."""
    return render_template('chart_placeholder.html', title='Data Charts')

@visualization_bp.route('/catalog')
def data_catalog_page():
    """Displays a catalog of available data types or datasets."""
    data_api_url = get_data_api_base_url()
    ekg_api_url = get_ekg_api_base_url()

    data_types = [
        {"name": "Hydrological Stations", "description": "Locations and metadata of hydrological monitoring stations.", "api_endpoint": f"{data_api_url}/stations", "ui_view_url": "visualization_bp.map_page"},
        {"name": "Station Time Series Readings", "description": "Time series data from stations.", "api_example": f"{data_api_url}/stations/STN001/readings?parameter_name=WaterLevel", "ui_view_url": "visualization_bp.chart_page"},
        {"name": "Wetland Areas", "description": "Boundaries and characteristics of wetland areas.", "api_endpoint": f"{data_api_url}/wetlands", "ui_view_url": "visualization_bp.map_page"},
        {"name": "Evolution Knowledge Graph (EKG)", "description": "Visualizer for the system evolution graph.", "api_endpoint": f"{ekg_api_url}/graph_sample", "ui_view_url": "visualization_bp.ekg_visualizer_page"},
        {"name": "Scenario Simulator", "description": "Tool for conceptual scenario simulation and AI-driven interpretation.", "api_endpoint": "N/A (UI Driven)", "ui_view_url": "visualization_bp.scenario_simulator_page"},
    ]

    station_count, wetland_count = "N/A", "N/A" # Defaults
    try:
        response_stations = requests.get(f"{data_api_url}/stations")
        response_stations.raise_for_status()
        stations_data = response_stations.json()
        station_count = len(stations_data) if isinstance(stations_data, list) else "Error"
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Failed to fetch station count for catalog: {e}")
        station_count = "Error fetching"

    try:
        response_wetlands = requests.get(f"{data_api_url}/wetlands")
        response_wetlands.raise_for_status()
        wetlands_data = response_wetlands.json()
        wetland_count = len(wetlands_data.get("features", [])) if isinstance(wetlands_data, dict) else "Error"
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Failed to fetch wetland count for catalog: {e}")
        wetland_count = "Error fetching"

    return render_template('data_catalog.html', title='Data Catalog',
                           data_types=data_types,
                           station_count=station_count,
                           wetland_count=wetland_count)

@visualization_bp.route('/ekg')
def ekg_visualizer_page():
    """Page for visualizing the Evolution Knowledge Graph."""
    return render_template('ekg_visualizer.html', title='EKG Visualizer')

@visualization_bp.route('/scenario-simulator')
def scenario_simulator_page():
    """Page for scenario simulation and decision support."""
    return render_template('scenario_simulator.html', title='Scenario Simulator')


# API endpoint within visualization blueprint - UI supporting API
@visualization_bp.route('/api/available-stations-for-charting', methods=['GET'])
def available_stations_for_charting():
    """
    Provides a simplified list of stations suitable for populating a dropdown in the chart view.
    """
    data_api_url = get_data_api_base_url()
    try:
        api_url = f"{data_api_url}/stations"
        response = requests.get(api_url)
        response.raise_for_status()
        stations_raw = response.json()

        stations_for_dropdown = [
            {"id": s.get("station_id_code"), "name": s.get("name", "Unknown Station")}
            for s in stations_raw if s.get("station_id_code")
        ]
        return jsonify(stations_for_dropdown)
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching stations for charting dropdown: {e}")
        return jsonify({"error": "Could not fetch station list", "details": str(e)}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in available_stations_for_charting: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
