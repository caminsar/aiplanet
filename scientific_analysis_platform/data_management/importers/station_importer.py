import csv
from sqlalchemy.orm import Session
from shapely.geometry import Point
from geoalchemy2.shape import from_shape

from .base_importer import BaseImporter
# Adjust the import path based on the actual location of models.py relative to this file
# Assuming importers are in data_management/importers and models is in data_management/
from ..models import HydrologicalStation  # Relative import if models.py is one level up

class StationCSVImporter(BaseImporter):
    """
    Importer for hydrological station data from a CSV file.
    Expected CSV format: station_id_code,name,latitude,longitude,river_name,elevation_m,operator
    """

    def __init__(self, db_session: Session, file_path: str):
        super().__init__(db_session, file_path)

    def import_data(self):
        self.log_message(f"Starting import of station data from: {self.file_path}")
        if not self._file_exists():
            self.log_message(f"File not found: {self.file_path}", level="ERROR")
            return

        try:
            with open(self.file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                stations_added = 0
                stations_updated = 0

                for row in reader:
                    try:
                        station_id_code = row['station_id_code']
                        name = row['name']
                        latitude = float(row['latitude'])
                        longitude = float(row['longitude'])
                        river_name = row.get('river_name') # Use .get for optional fields
                        elevation_m = float(row['elevation_m']) if row.get('elevation_m') else None
                        operator = row.get('operator')

                        # Create Shapely Point for location
                        location_point = Point(longitude, latitude)
                        # Convert to GeoAlchemy2 geometry element
                        location_geom = from_shape(location_point, srid=4326)

                        # Check if station already exists
                        existing_station = self.db_session.query(HydrologicalStation).filter_by(station_id_code=station_id_code).first()

                        if existing_station:
                            # Update existing station
                            existing_station.name = name
                            existing_station.location = location_geom
                            existing_station.river_name = river_name
                            existing_station.elevation_m = elevation_m
                            existing_station.operator = operator
                            # existing_station.updated_at = datetime.datetime.utcnow() # If model has this field
                            self.log_message(f"Updating station: {station_id_code} - {name}")
                            stations_updated += 1
                        else:
                            # Create new station
                            new_station = HydrologicalStation(
                                station_id_code=station_id_code,
                                name=name,
                                location=location_geom,
                                river_name=river_name,
                                elevation_m=elevation_m,
                                operator=operator
                            )
                            self.db_session.add(new_station)
                            self.log_message(f"Adding new station: {station_id_code} - {name}")
                            stations_added += 1

                    except ValueError as ve:
                        self.log_message(f"Skipping row due to data conversion error: {row} - {ve}", level="WARN")
                        continue # Skip to next row
                    except Exception as e:
                        self.log_message(f"Error processing row {row}: {e}", level="ERROR")
                        self.db_session.rollback() # Rollback this specific row's attempt if part of a larger transaction logic
                        continue


                self.db_session.commit()
                self.log_message(f"Station data import completed. Added: {stations_added}, Updated: {stations_updated} stations.")

        except FileNotFoundError:
            self.log_message(f"File not found: {self.file_path}", level="ERROR")
        except Exception as e:
            self.db_session.rollback()
            self.log_message(f"An error occurred during CSV import: {e}", level="CRITICAL")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    # This is an example of how to run the importer directly.
    # You would need to set up a database session.
    # Ensure your POSTGRES_DB_URL is set in environment variables.

    from scientific_analysis_platform.data_management.models import SessionLocal, init_db

    print("Directly running StationCSVImporter example...")
    # Initialize DB (create tables if they don't exist)
    # This should point to your PostGIS DB if POSTGRES_DB_URL is set
    try:
        init_db()
    except Exception as e:
        print(f"Failed to initialize database for importer test: {e}")
        print("Ensure your database server is running and accessible, and POSTGRES_DB_URL is correctly set.")
        exit(1)

    db_session = SessionLocal()

    # Path to the sample CSV file - adjust if your script is run from a different directory
    # Assuming this script is in scientific_analysis_platform/data_management/importers/
    # and sample_data is in scientific_analysis_platform/sample_data/
    import os
    # Construct path relative to this script's location to find sample_data
    # __file__ is data_management/importers/station_importer.py
    # We need to go up two levels to scientific_analysis_platform, then to sample_data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file_path = os.path.join(current_dir, '..', '..', 'sample_data', 'stations.csv')
    sample_file_path = os.path.normpath(sample_file_path) # Normalize path (e.g. /a/b/../c -> /a/c)


    if not os.path.exists(sample_file_path):
        print(f"Error: Sample file not found at {sample_file_path}")
        print(f"Current script directory: {current_dir}")
    else:
        print(f"Found sample file at: {sample_file_path}")
        importer = StationCSVImporter(db_session=db_session, file_path=sample_file_path)
        try:
            importer.import_data()
            print("Station import process finished.")
        except Exception as e:
            print(f"An error occurred while running the importer: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db_session.close()
            print("Database session closed.")
