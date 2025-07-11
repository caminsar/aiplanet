from flask import Blueprint, render_template, current_app, jsonify
import requests # For making internal API calls to our own backend

visualization_bp = Blueprint(
    'visualization_bp',
    __name__,
    template_folder='templates', # Points to scientific_analysis_platform/visualization/templates
    static_folder='static',      # Points to scientific_analysis_platform/visualization/static
    url_prefix='/view'           # Optional: prefix for all routes in this blueprint e.g. /view/catalog
)

# Helper to get the base URL for internal API calls
def get_api_base_url():
    # This assumes the app is running on localhost:5000 for internal calls.
    # In a production/containerized setup, this might need to be more dynamic
    # or use service discovery. For development, this is usually fine.
    # Using current_app.config.get("SERVER_NAME") might also be an option if set.
    return "http://localhost:5000/api/data"


@visualization_bp.route('/')
def home():
    """Main page for the visualization section."""
    # This is the same as the existing /visualization route in app.py
    # We are migrating it here.
    return render_template('visualization_home.html', title='Visualization Hub')

@visualization_bp.route('/map')
def map_page():
    """Page for map placeholder - will be enhanced."""
    # This is the same as the existing /visualization/map_placeholder route
    return render_template('map_placeholder.html', title='Interactive Map')

@visualization_bp.route('/chart')
def chart_page():
    """Page for chart placeholder - will be enhanced."""
    # This is the same as the existing /visualization/chart_placeholder route
    return render_template('chart_placeholder.html', title='Data Charts')

@visualization_bp.route('/catalog')
def data_catalog_page():
    """Displays a catalog of available data types or datasets."""
    # For now, this will be a mix of hardcoded data and potentially
    # calls to simple API endpoints if we had one for "list_data_types".
    # Let's simulate fetching some data types.

    data_types = [
        {"name": "Hydrological Stations", "description": "Locations and metadata of hydrological monitoring stations.", "api_endpoint": f"{get_api_base_url()}/stations", "ui_view_url": "/view/map"}, # Link to our map view
        {"name": "Station Time Series Readings", "description": "Time series data (e.g., water level, flow rate) from stations.", "api_example": f"{get_api_base_url()}/stations/STN001/readings?parameter_name=WaterLevel", "ui_view_url": "/view/chart"},
        {"name": "Wetland Areas", "description": "Boundaries and characteristics of wetland areas.", "api_endpoint": f"{get_api_base_url()}/wetlands", "ui_view_url": "/view/map"},
        # Add more as APIs develop
    ]

    # Example: try to fetch live station count
    try:
        response = requests.get(f"{get_api_base_url()}/stations")
        response.raise_for_status() # Raise an exception for HTTP errors
        stations_data = response.json()
        station_count = len(stations_data) if isinstance(stations_data, list) else "N/A"
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Failed to fetch station count for catalog: {e}")
        station_count = "Error fetching"

    # Example: try to fetch live wetland count
    try:
        response = requests.get(f"{get_api_base_url()}/wetlands")
        response.raise_for_status()
        wetlands_data = response.json()
        wetland_count = len(wetlands_data.get("features", [])) if isinstance(wetlands_data, dict) else "N/A"
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Failed to fetch wetland count for catalog: {e}")
        wetland_count = "Error fetching"


    return render_template('data_catalog.html', title='Data Catalog',
                           data_types=data_types,
                           station_count=station_count,
                           wetland_count=wetland_count)


# API endpoint within visualization blueprint - just an example, typically APIs are separate
@visualization_bp.route('/api/available-stations-for-charting', methods=['GET'])
def available_stations_for_charting():
    """
    Provides a simplified list of stations suitable for populating a dropdown in the chart view.
    This is an example of a UI-supporting API endpoint.
    """
    try:
        # This makes an internal request to our own data API.
        # Ensure your Flask development server can handle concurrent requests or use appropriate session handling.
        # For production, consider direct DB access if this blueprint has its own session scope,
        # or ensure the API is robust.
        api_url = f"{get_api_base_url()}/stations"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        stations_raw = response.json()

        # Process for dropdown: { value: station_id_code, text: name }
        stations_for_dropdown = [
            {"id": s.get("station_id_code"), "name": s.get("name", "Unknown Station")}
            for s in stations_raw if s.get("station_id_code")
        ]
        return jsonify(stations_for_dropdown)
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching stations for charting dropdown: {e}")
        return jsonify({"error": "Could not fetch station list", "details": str(e)}), 500
    except Exception as e: # Catch any other unexpected errors
        current_app.logger.error(f"Unexpected error in available_stations_for_charting: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
