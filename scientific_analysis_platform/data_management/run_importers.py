"""
Main script to run data importers for the Scientific Analysis Platform.

This script initializes the database connection and then invokes the
necessary importer classes to populate the database with sample or
actual data.

To run this:
1. Ensure your `POSTGRES_DB_URL` environment variable is set correctly
   to point to your PostGIS database.
   Example: export POSTGRES_DB_URL="postgresql://platform_user:platform_secret_password@localhost:5432/scientific_platform_dev"
2. Make sure the database and PostGIS extension are created (e.g., via `docker-compose up -d db_postgis`).
3. Run `python -m scientific_analysis_platform.data_management.models` (or just ensure init_db has been called once).
4. Execute this script from the project root directory (`scientific_analysis_platform`):
   `python -m scientific_analysis_platform.data_management.run_importers`
   Or, if `scientific_analysis_platform` is in PYTHONPATH:
   `python scientific_analysis_platform/data_management/run_importers.py`
"""

import os
import sys

# Adjust Python path to include the project root if running script directly
# This allows for imports like `from scientific_analysis_platform.data_management...`
# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Project root is two levels up from data_management/ (importers/ is not used here)
project_root = os.path.dirname(os.path.dirname(script_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from scientific_analysis_platform.data_management.models import SessionLocal, init_db, HydrologicalStation
from scientific_analysis_platform.data_management.importers.station_importer import StationCSVImporter
from scientific_analysis_platform.data_management.importers.geojson_importer import WetlandGeoJSONImporter
from scientific_analysis_platform.data_management.importers.station_reading_importer import StationReadingsCSVImporter

def main():
    print("--- Starting Data Import Process ---")

    # Initialize Database (creates tables if they don't exist)
    try:
        print("Initializing database schema...")
        init_db()
        print("Database schema initialized successfully.")
    except Exception as e:
        print(f"CRITICAL: Failed to initialize database: {e}")
        print("Ensure your database server (PostGIS) is running and accessible,")
        print("and the POSTGRES_DB_URL environment variable is correctly set.")
        import traceback
        traceback.print_exc()
        return # Stop if DB init fails

    db_session = SessionLocal()

    # Define paths to sample data relative to the project root
    # project_root is already calculated above.
    # Alternatively, if running from project root, sample_data_dir = "sample_data"
    sample_data_dir = os.path.join(project_root, "sample_data")

    print(f"Looking for sample data in: {sample_data_dir}")


    # 1. Import Hydrological Stations
    stations_csv_path = os.path.join(sample_data_dir, "stations.csv")
    print(f"\n--- Importing Hydrological Stations from: {stations_csv_path} ---")
    station_importer = StationCSVImporter(db_session=db_session, file_path=stations_csv_path)
    try:
        station_importer.import_data()
        print("Hydrological stations import finished.")
    except Exception as e:
        print(f"ERROR during station import: {e}")
        db_session.rollback() # Rollback on error for this importer
    else:
        db_session.commit() # Commit if successful

    # 2. Import Wetland Boundaries from GeoJSON
    wetlands_geojson_path = os.path.join(sample_data_dir, "wetland_boundary.geojson")
    print(f"\n--- Importing Wetland Boundaries from: {wetlands_geojson_path} ---")
    wetland_importer = WetlandGeoJSONImporter(db_session=db_session, file_path=wetlands_geojson_path)
    try:
        wetland_importer.import_data()
        print("Wetland boundaries import finished.")
    except Exception as e:
        print(f"ERROR during wetland import: {e}")
        db_session.rollback()
    else:
        db_session.commit()


    # 3. Import Time Series Readings for specific stations
    # Example for station STN001
    station_to_import_for = "STN001"
    station_readings_csv_path = os.path.join(sample_data_dir, f"station_{station_to_import_for}_readings.csv")

    # Check if the station exists before attempting to import readings
    station = db_session.query(HydrologicalStation).filter_by(station_id_code=station_to_import_for).first()
    if station:
        print(f"\n--- Importing Readings for Station: {station_to_import_for} from {station_readings_csv_path} ---")
        readings_importer = StationReadingsCSVImporter(
            db_session=db_session,
            file_path=station_readings_csv_path,
            station_id_code=station_to_import_for
        )
        try:
            readings_importer.import_data()
            print(f"Readings import for {station_to_import_for} finished.")
        except Exception as e:
            print(f"ERROR during readings import for {station_to_import_for}: {e}")
            db_session.rollback()
        else:
            db_session.commit()
    else:
        print(f"\nSkipping readings import for {station_to_import_for} as the station was not found in the database.")


    # Add more importers here as needed...

    db_session.close()
    print("\n--- Data Import Process Finished ---")

if __name__ == "__main__":
    # This allows running the script with `python scientific_analysis_platform/data_management/run_importers.py`
    # from the parent directory of `scientific_analysis_platform`
    # OR by `python -m scientific_analysis_platform.data_management.run_importers` from project root.

    # If run directly, ensure the project root is in sys.path for module resolution
    # The sys.path modification at the top handles this for when script is run directly.
    main()
