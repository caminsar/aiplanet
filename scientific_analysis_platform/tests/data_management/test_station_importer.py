import unittest
import os
import csv
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adjust path to import from the main project directory
test_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root_for_test = os.path.dirname(os.path.dirname(test_file_dir))
if project_root_for_test not in sys.path:
    sys.path.insert(0, project_root_for_test)

from scientific_analysis_platform.data_management.models import Base, HydrologicalStation
from scientific_analysis_platform.data_management.importers.station_importer import StationCSVImporter
from geoalchemy2.shape import to_shape # To inspect geometry

class TestStationCSVImporter(unittest.TestCase):

    def setUp(self):
        """Set up an in-memory SQLite database for testing."""
        # Using SQLite for importer unit tests is simpler than requiring PostGIS,
        # but means we can't fully test PostGIS-specific geometry functions.
        # We can mock the geometry part or test it in integration tests.
        # For now, we'll test the CSV parsing and basic object creation.
        # GeoAlchemy2 can work with SpatiaLite (SQLite extension) but needs setup.
        # For simplicity, let's assume location is stored as WKT text if not PostGIS,
        # or mock the from_shape part.

        # Let's use in-memory SQLite and mock from_shape for this unit test.
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()

        # Create a dummy CSV file for testing
        self.test_csv_file = "temp_test_stations.csv"
        with open(self.test_csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["station_id_code", "name", "latitude", "longitude", "river_name", "elevation_m", "operator"])
            writer.writerow(["STN001", "Test Station Alpha", "30.5", "114.3", "Yangtze", "50.0", "TestOpA"])
            writer.writerow(["STN002", "Test Station Beta", "31.2", "121.5", "Huangpu", "5.0", "TestOpB"])
            writer.writerow(["STN003_INVALID_LAT", "Test Station Gamma", "INVALID", "120.0", "Qiantang", "10.0", "TestOpC"])


    def tearDown(self):
        """Clean up database session and test file."""
        self.db_session.close()
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)
        # Base.metadata.drop_all(self.engine) # If tables needed to be dropped for each test

    def test_import_stations_successfully(self):
        """Test successful import of valid station data."""
        importer = StationCSVImporter(db_session=self.db_session, file_path=self.test_csv_file)

        # Mock from_shape to avoid PostGIS/SpatiaLite dependency in this specific unit test
        # If testing with actual PostGIS, this mock wouldn't be needed.
        original_from_shape = importer.from_shape # Keep original if needed
        importer.from_shape = lambda shapely_geom, srid: f"POINT({shapely_geom.x} {shapely_geom.y})" # Mock returns WKT like string

        importer.import_data()

        stations = self.db_session.query(HydrologicalStation).all()
        self.assertEqual(len(stations), 2) # STN003 should be skipped

        station1 = self.db_session.query(HydrologicalStation).filter_by(station_id_code="STN001").first()
        self.assertIsNotNone(station1)
        self.assertEqual(station1.name, "Test Station Alpha")
        self.assertEqual(station1.river_name, "Yangtze")
        self.assertEqual(station1.elevation_m, 50.0)
        # For mocked geometry:
        self.assertEqual(station1.location, "POINT(114.3 30.5)")

        # Restore from_shape if it was part of the class, not instance
        # setattr(StationCSVImporter, 'from_shape', original_from_shape) # if it was a class attribute
        # Or if instance attribute: importer.from_shape = original_from_shape
        # (Better to mock via unittest.patch if from_shape is imported directly in the module)

    def test_skip_invalid_row(self):
        """Test that rows with data conversion errors are skipped."""
        importer = StationCSVImporter(db_session=self.db_session, file_path=self.test_csv_file)
        importer.from_shape = lambda shapely_geom, srid: f"POINT({shapely_geom.x} {shapely_geom.y})" # Mock

        importer.import_data() # This will log a warning for STN003_INVALID_LAT

        station_gamma = self.db_session.query(HydrologicalStation).filter_by(station_id_code="STN003_INVALID_LAT").first()
        self.assertIsNone(station_gamma)

        # Ensure the valid ones are still imported
        self.assertEqual(self.db_session.query(HydrologicalStation).count(), 2)

    def test_update_existing_station(self):
        """Test that existing stations are updated."""
        # Initial import
        importer1 = StationCSVImporter(db_session=self.db_session, file_path=self.test_csv_file)
        importer1.from_shape = lambda shapely_geom, srid: f"POINT({shapely_geom.x} {shapely_geom.y})" # Mock
        importer1.import_data()

        # Create a new CSV with updated data for STN001
        updated_csv_file = "temp_updated_stations.csv"
        with open(updated_csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["station_id_code", "name", "latitude", "longitude", "river_name", "elevation_m", "operator"])
            writer.writerow(["STN001", "Test Station Alpha UPDATED", "30.6", "114.4", "Yangtze Updated", "55.0", "TestOpA_New"])

        importer2 = StationCSVImporter(db_session=self.db_session, file_path=updated_csv_file)
        importer2.from_shape = lambda shapely_geom, srid: f"POINT({shapely_geom.x} {shapely_geom.y})" # Mock
        importer2.import_data()

        updated_station1 = self.db_session.query(HydrologicalStation).filter_by(station_id_code="STN001").first()
        self.assertIsNotNone(updated_station1)
        self.assertEqual(updated_station1.name, "Test Station Alpha UPDATED")
        self.assertEqual(updated_station1.elevation_m, 55.0)
        self.assertEqual(updated_station1.location, "POINT(114.4 30.6)")

        # Ensure total count hasn't increased (just update)
        self.assertEqual(self.db_session.query(HydrologicalStation).count(), 2)

        if os.path.exists(updated_csv_file):
            os.remove(updated_csv_file)

if __name__ == '__main__':
    # This setup is a bit more involved due to path adjustments needed for direct script run
    # Typically, you'd run tests via `python -m unittest discover tests` from project root.

    # Ensure the module's from_shape is correctly mocked if this file is run directly
    # This is tricky. `unittest.mock.patch` is the robust way.
    # For this example, the mock is assigned to the instance inside the test methods.

    print("Running tests for StationCSVImporter...")
    print(f"Project root for test (added to sys.path): {project_root_for_test}")
    print(f"Current sys.path: {sys.path[:3]}...") # Print first few paths

    # Verify module import
    try:
        from scientific_analysis_platform.data_management.importers.station_importer import StationCSVImporter
        print("Successfully imported StationCSVImporter for direct run.")
    except ImportError as e:
        print(f"Failed to import StationCSVImporter for direct run: {e}")
        print("Ensure PYTHONPATH is set correctly or run tests via 'python -m unittest discover'.")
        sys.exit(1)

    unittest.main()
