import csv
import datetime
from sqlalchemy.orm import Session
from dateutil import parser as dateutil_parser # For flexible date parsing

from .base_importer import BaseImporter
from ..models import HydrologicalStation, TimeSeriesReading # Adjust import path

class StationReadingsCSVImporter(BaseImporter):
    """
    Importer for time series readings for a specific hydrological station from a CSV file.
    Expected CSV format: timestamp,parameter_name,value,unit,quality_flag
    The station itself must already exist in the database.
    """

    def __init__(self, db_session: Session, file_path: str, station_id_code: str):
        super().__init__(db_session, file_path)
        self.station_id_code = station_id_code
        self.station = None # Will be fetched in import_data

    def import_data(self):
        self.log_message(f"Starting import of station readings for station '{self.station_id_code}' from: {self.file_path}")
        if not self._file_exists():
            self.log_message(f"File not found: {self.file_path}", level="ERROR")
            return

        # Fetch the station first
        self.station = self.db_session.query(HydrologicalStation).filter_by(station_id_code=self.station_id_code).first()
        if not self.station:
            self.log_message(f"Station with ID code '{self.station_id_code}' not found in database. Cannot import readings.", level="ERROR")
            return

        self.log_message(f"Found station: {self.station.name} (ID: {self.station.id})")

        try:
            with open(self.file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                readings_added = 0

                for row in reader:
                    try:
                        # Parse timestamp, trying to be flexible with ISO 8601 formats
                        timestamp_str = row['timestamp']
                        try:
                            timestamp = dateutil_parser.isoparse(timestamp_str)
                        except ValueError:
                            self.log_message(f"Could not parse timestamp '{timestamp_str}'. Attempting fallback. Row: {row}", level="WARN")
                            # Fallback or more robust parsing can be added here if needed
                            timestamp = dateutil_parser.parse(timestamp_str) # General parser

                        # Ensure timestamp is timezone-aware (UTC preferred)
                        if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
                            self.log_message(f"Timestamp '{timestamp_str}' is naive. Assuming UTC. Row: {row}", level="DEBUG")
                            timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)
                        else:
                            timestamp = timestamp.astimezone(datetime.timezone.utc) # Convert to UTC

                        parameter_name = row['parameter_name']
                        value = float(row['value'])
                        unit = row['unit']
                        quality_flag = row.get('quality_flag')

                        # Optional: Check if this specific reading already exists to prevent duplicates
                        # This depends on business logic (e.g., (station_id, timestamp, parameter_name) should be unique)
                        # For this example, we'll assume new readings are always added.
                        # existing_reading = self.db_session.query(TimeSeriesReading).filter_by(
                        #     station_id=self.station.id,
                        #     timestamp=timestamp,
                        #     parameter_name=parameter_name
                        # ).first()
                        # if existing_reading:
                        #     self.log_message(f"Reading already exists, skipping: {row}", level="DEBUG")
                        #     continue

                        new_reading = TimeSeriesReading(
                            station_id=self.station.id,
                            timestamp=timestamp,
                            parameter_name=parameter_name,
                            value=value,
                            unit=unit,
                            quality_flag=quality_flag
                        )
                        self.db_session.add(new_reading)
                        readings_added += 1

                        # Commit in batches for large files
                        if readings_added % 1000 == 0:
                            self.db_session.commit()
                            self.log_message(f"Committed batch of 1000 readings. Total added so far: {readings_added}")

                    except ValueError as ve:
                        self.log_message(f"Skipping row due to data conversion error: {row} - {ve}", level="WARN")
                        continue
                    except Exception as e:
                        self.log_message(f"Error processing row {row}: {e}", level="ERROR")
                        # Decide if rollback is needed here or if we just skip the row
                        continue

                self.db_session.commit() # Commit any remaining records
                self.log_message(f"Station readings import for '{self.station_id_code}' completed. Added: {readings_added} readings.")

        except FileNotFoundError:
            self.log_message(f"File not found: {self.file_path}", level="ERROR")
        except Exception as e:
            self.db_session.rollback()
            self.log_message(f"An error occurred during CSV import for station '{self.station_id_code}': {e}", level="CRITICAL")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    from scientific_analysis_platform.data_management.models import SessionLocal, init_db
    import os

    print("Directly running StationReadingsCSVImporter example...")
    try:
        init_db()
    except Exception as e:
        print(f"Failed to initialize database for importer test: {e}")
        print("Ensure your database server is running and accessible, and POSTGRES_DB_URL is correctly set.")
        exit(1)

    db_session = SessionLocal()

    # --- Import STN001 readings ---
    # First, ensure STN001 exists. If not, the StationCSVImporter should be run first.
    # For this test, we assume STN001 might have been added by StationCSVImporter's own __main__
    station_to_import_for = "STN001"
    station_check = db_session.query(HydrologicalStation).filter_by(station_id_code=station_to_import_for).first()
    if not station_check:
        print(f"Station {station_to_import_for} not found. Please import stations first (e.g., run station_importer.py).")
        # As a fallback for isolated testing, let's add it if models.py __main__ didn't run or was for different DB
        # This is not ideal for a real workflow but helps testing this script in isolation.
        print(f"Attempting to add station {station_to_import_for} for testing purposes...")
        from shapely.geometry import Point
        from geoalchemy2.shape import from_shape
        try:
            test_station_location = from_shape(Point(111.29, 30.70), srid=4326) # Yichang coords
            fallback_station = HydrologicalStation(station_id_code=station_to_import_for, name="Yichang (Fallback)", location=test_station_location)
            db_session.add(fallback_station)
            db_session.commit()
            print(f"Fallback station {station_to_import_for} added.")
        except Exception as e_stat:
            db_session.rollback()
            print(f"Could not add fallback station {station_to_import_for}: {e_stat}")
            db_session.close()
            exit(1)


    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file_path_stn001 = os.path.join(current_dir, '..', '..', 'sample_data', f'station_{station_to_import_for}_readings.csv')
    sample_file_path_stn001 = os.path.normpath(sample_file_path_stn001)

    if not os.path.exists(sample_file_path_stn001):
        print(f"Error: Sample file not found at {sample_file_path_stn001}")
    else:
        print(f"Found sample file for {station_to_import_for} at: {sample_file_path_stn001}")
        importer_stn001 = StationReadingsCSVImporter(db_session=db_session, file_path=sample_file_path_stn001, station_id_code=station_to_import_for)
        try:
            importer_stn001.import_data()
            print(f"Station {station_to_import_for} readings import process finished.")
        except Exception as e:
            print(f"An error occurred while running the importer for {station_to_import_for}: {e}")
            import traceback
            traceback.print_exc()

    db_session.close()
    print("Database session closed.")
