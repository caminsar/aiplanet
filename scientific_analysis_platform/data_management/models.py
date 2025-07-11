import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, text # Added text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base # updated import
from geoalchemy2 import Geometry, Geography # For PostGIS spatial types
from geoalchemy2.shape import from_shape # To convert shapely geometries
from shapely.geometry import Point # Example for creating point data

# Define the base for declarative models
Base = declarative_base()

# --- Core Spatial Object (Optional, for generic features) ---
class SpatialFeature(Base):
    __tablename__ = 'spatial_features'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    feature_type = Column(String(100), index=True) # e.g., 'HydrologicalStation', 'WetlandArea'
    description = Column(Text, nullable=True)
    # Using Geometry for projected data, Geography for lon/lat if distance calcs are frequent
    # SRID 4326 is WGS84 (lat/lon)
    geom = Column(Geometry(geometry_type='GEOMETRY', srid=4326, spatial_index=True), nullable=True)
    # For geography type: geom = Column(Geography(geometry_type='GEOMETRY', srid=4326, spatial_index=True), nullable=True)

    properties_json = Column(JSON, nullable=True) # For flexible additional properties
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<SpatialFeature(id={self.id}, name='{self.name}', type='{self.feature_type}')>"

# --- Specific Entity Models ---
class HydrologicalStation(Base):
    __tablename__ = 'hydrological_stations'
    id = Column(Integer, primary_key=True, index=True)
    station_id_code = Column(String(50), unique=True, nullable=False, index=True) # Official station code
    name = Column(String(255), nullable=False)
    river_name = Column(String(100), nullable=True)
    basin_name = Column(String(100), nullable=True)
    # Location using PostGIS Point geometry. SRID 4326 for WGS84 lat/lon.
    location = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True), nullable=False)
    elevation_m = Column(Float, nullable=True)
    established_date = Column(DateTime, nullable=True)
    operator = Column(String(255), nullable=True)
    remarks = Column(Text, nullable=True)

    # Relationship to time series readings
    readings = relationship("TimeSeriesReading", back_populates="station")

    def __repr__(self):
        return f"<HydrologicalStation(station_id_code='{self.station_id_code}', name='{self.name}')>"

class WetlandArea(Base):
    __tablename__ = 'wetland_areas'
    id = Column(Integer, primary_key=True, index=True)
    wetland_id_code = Column(String(50), unique=True, nullable=True, index=True) # Official ID if exists
    name = Column(String(255), nullable=False)
    # Boundary using PostGIS Polygon/MultiPolygon geometry
    boundary = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True), nullable=False)
    type = Column(String(100), nullable=True) # e.g., Lacustrine, Palustrine, Riverine
    area_sqkm = Column(Float, nullable=True) # Can be calculated from geometry too
    description = Column(Text, nullable=True)
    # Could have relationships to observed changes, species, etc.

    def __repr__(self):
        return f"<WetlandArea(name='{self.name}')>"

class EcologicalSamplePoint(Base):
    __tablename__ = 'ecological_sample_points'
    id = Column(Integer, primary_key=True, index=True)
    sample_id_code = Column(String(100), unique=True, nullable=False, index=True)
    project_name = Column(String(255), nullable=True)
    location = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True), nullable=False)
    sampling_date = Column(DateTime, nullable=False, index=True)
    sampler_type = Column(String(100)) # e.g., 'Water Sample', 'Sediment Core', 'Fish Net'
    depth_m = Column(Float, nullable=True)
    remarks = Column(Text, nullable=True)

    # Relationship to observations/measurements made at this sample point
    observations = relationship("Observation", back_populates="sample_point")

    def __repr__(self):
        return f"<EcologicalSamplePoint(sample_id_code='{self.sample_id_code}', date='{self.sampling_date}')>"

# --- Time Series Data Model (Generic) ---
# This replaces the previous more generic DataRecord for structured time series
class TimeSeriesReading(Base):
    __tablename__ = 'time_series_readings'
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to a station (e.g., HydrologicalStation, MeteorologicalStation)
    # This assumes a polymorphic association or separate tables for different station types if needed.
    # For simplicity, linking to HydrologicalStation here.
    station_id = Column(Integer, ForeignKey('hydrological_stations.id'), nullable=False, index=True)
    station = relationship("HydrologicalStation", back_populates="readings")

    timestamp = Column(DateTime, nullable=False, index=True)
    parameter_name = Column(String(100), nullable=False, index=True) # e.g., 'WaterLevel', 'FlowRate', 'SedimentConcentration'
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    quality_flag = Column(String(50), nullable=True) # e.g., 'Good', 'Suspect', 'Estimated'
    source_datasource_id = Column(String(100), nullable=True) # Identifier for the original data file or source

    def __repr__(self):
        return f"<TimeSeriesReading(station_id={self.station_id}, param='{self.parameter_name}', ts='{self.timestamp}', val={self.value})>"

# --- Observational Data (more generic, for ecological samples etc.) ---
class Observation(Base):
    __tablename__ = 'observations'
    id = Column(Integer, primary_key=True, index=True)

    sample_point_id = Column(Integer, ForeignKey('ecological_sample_points.id'), nullable=True, index=True)
    sample_point = relationship("EcologicalSamplePoint", back_populates="observations")

    # Could also link to a SpatialFeature directly if observation is not tied to a pre-defined sample point
    # spatial_feature_id = Column(Integer, ForeignKey('spatial_features.id'), nullable=True, index=True)

    timestamp = Column(DateTime, nullable=False, index=True) # Observation time if different from sample time
    parameter_name = Column(String(255), nullable=False, index=True) # e.g., 'SpeciesCount_FinlessPorpoise', 'TP_Concentration', 'pH'
    value_numeric = Column(Float, nullable=True)
    value_text = Column(Text, nullable=True) # For qualitative observations or species names
    unit = Column(String(50), nullable=True)
    method = Column(String(255), nullable=True) # Observation method
    remarks = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Observation(param='{self.parameter_name}', value_numeric={self.value_numeric}, value_text='{self.value_text}')>"


# --- Database Setup ---
# Default to SQLite in-memory for easy testing if POSTGRES_DB_URL is not set.
# For production/PostGIS, set the POSTGRES_DB_URL environment variable.
# Example: postgresql://user:password@host:port/database
DATABASE_URL = os.getenv("POSTGRES_DB_URL", "sqlite:///:memory:")

engine_args = {}
if DATABASE_URL.startswith("postgresql"):
    # Add connect_args for PostgreSQL if needed, e.g., SSL settings
    # engine_args['connect_args'] = {"sslmode": "prefer"}
    print(f"Configuring for PostgreSQL: {DATABASE_URL}")
else:
    print(f"Configuring for SQLite (in-memory): {DATABASE_URL}")


engine = create_engine(DATABASE_URL, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    print(f"Initializing database at {DATABASE_URL}...")
    try:
        # This will create tables for all classes that inherit from Base
        Base.metadata.create_all(bind=engine)
        print("Database tables created (or already exist).")

        # For PostGIS, ensure the PostGIS extension is enabled in your database.
        # This check can be done manually or via a DB session if permissions allow.
        if DATABASE_URL.startswith("postgresql"):
            with engine.connect() as connection:
                try:
                    result = connection.execute(text("SELECT postgis_version();")) # SQLAlchemy 2.x text import
                    # from sqlalchemy import text # Add this import at the top for SQLAlchemy 2.x
                    # For SQLAlchemy 1.x, it's just connection.execute("SELECT postgis_version();")
                    pg_version = result.scalar_one_or_none()
                    if pg_version:
                        print(f"PostGIS extension found: {pg_version}")
                    else:
                        print("Warning: PostGIS extension version could not be verified. Ensure it's enabled.")
                except Exception as e:
                    print(f"Warning: Could not verify PostGIS extension. Ensure it's enabled in the database '{engine.url.database}'. Error: {e}")
                finally:
                    connection.commit() # commit any transaction started by execute
                    # No close needed for connection from engine.connect() due to context manager

    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    # This is for demonstration/testing purposes if you run this file directly.
    # Remember to set POSTGRES_DB_URL environment variable if you want to test with PostgreSQL.
    # e.g., export POSTGRES_DB_URL="postgresql://youruser:yourpass@localhost:5432/yourdb"

    print(f"Running models.py directly. Target DB: {DATABASE_URL}")

    if "sqlite" in DATABASE_URL:
        print("Note: Spatial operations with GeoAlchemy2 might be limited or behave differently with SQLite (SpatiaLite).")
        print("Full functionality is expected with PostgreSQL/PostGIS.")

    init_db() # Create tables

    # Example usage (optional, for testing with the current DB engine)
    db_session = SessionLocal()
    try:
        # Create a sample Hydrological Station with a Point geometry
        # For PostGIS, WKT for a point: 'SRID=4326;POINT(lon lat)'
        # Using shapely Point and from_shape for easier construction
        station_location_shapely = Point(114.3, 30.5) # Example: Wuhan

        # Check if station already exists to avoid re-inserting if run multiple times
        existing_station = db_session.query(HydrologicalStation).filter_by(station_id_code="TEST001").first()
        if not existing_station:
            new_station = HydrologicalStation(
                station_id_code="TEST001",
                name="Test Hydrological Station Wuhan",
                river_name="Yangtze",
                location=from_shape(station_location_shapely, srid=4326), # Convert shapely to WKT/EWKB for GeoAlchemy
                elevation_m=23.0
            )
            db_session.add(new_station)
            db_session.commit()
            print(f"Added new station: {new_station.name} with ID {new_station.id}")

            # Add a sample reading for this station
            new_reading = TimeSeriesReading(
                station_id=new_station.id, # Link to the newly created station
                timestamp=datetime.datetime.now(datetime.timezone.utc),
                parameter_name="WaterLevel",
                value=15.5,
                unit="m",
                quality_flag="Good"
            )
            db_session.add(new_reading)
            db_session.commit()
            print(f"Added new reading for station {new_station.name}: {new_reading.parameter_name} = {new_reading.value} {new_reading.unit}")
        else:
            print(f"Station TEST001 already exists with ID {existing_station.id}.")
            # Query existing reading for this station
            existing_reading = db_session.query(TimeSeriesReading).filter_by(station_id=existing_station.id, parameter_name="WaterLevel").first()
            if existing_reading:
                 print(f"Existing reading for station {existing_station.name}: {existing_reading.parameter_name} = {existing_reading.value} {existing_reading.unit} at {existing_reading.timestamp}")


        retrieved_station = db_session.query(HydrologicalStation).filter_by(station_id_code="TEST001").first()
        if retrieved_station:
            print(f"Retrieved station: {retrieved_station.name}, Location: {retrieved_station.location}")
            # To get WKT from the geometry object:
            # from geoalchemy2.shape import to_shape
            # shapely_geom = to_shape(retrieved_station.location)
            # print(f"  Shapely geometry: {shapely_geom.wkt}")
            print(f"  Number of readings for this station: {len(retrieved_station.readings)}")
            for r in retrieved_station.readings:
                print(f"    - Reading: {r.parameter_name} = {r.value} {r.unit} at {r.timestamp}")

    except Exception as e:
        db_session.rollback()
        print(f"An error occurred during example usage: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()

    print("models.py script finished.")
