from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Define the base for declarative models
Base = declarative_base()

# Example Data Record Model
class DataRecord(Base):
    __tablename__ = 'data_records'

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String(255), index=True) # e.g., 'Hydrological Station X', 'Meteorological Sensor Y'
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    location_latitude = Column(Float, nullable=True)
    location_longitude = Column(Float, nullable=True)
    parameter_name = Column(String(255), index=True) # e.g., 'Water Level', 'Temperature', 'Sediment Concentration'
    parameter_value = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True) # e.g., 'm', '°C', 'mg/L'
    raw_data = Column(Text, nullable=True) # For storing raw text or JSON if needed
    metadata_json = Column(Text, nullable=True) # For additional metadata as JSON

    def __repr__(self):
        return f"<DataRecord(id={self.id}, source='{self.source_name}', parameter='{self.parameter_name}', value={self.parameter_value})>"

# --- Database Setup (Example using SQLite in memory) ---
# In a real application, this would be configured to point to a persistent database like PostgreSQL/PostGIS.
DATABASE_URL = "sqlite:///:memory:" # Example, replace with actual DB URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    # This is for demonstration/testing purposes if you run this file directly.
    print("Initializing in-memory database and creating tables...")
    init_db()
    print("Database initialized. Tables (like 'data_records') should be created.")

    # Example usage (optional, for testing)
    # db_session = SessionLocal()
    # new_record = DataRecord(
    #     source_name="Test Station",
    #     parameter_name="Water Level",
    #     parameter_value=10.5,
    #     unit="m",
    #     location_latitude=30.5,
    #     location_longitude=114.3
    # )
    # db_session.add(new_record)
    # db_session.commit()
    # print(f"Added new record: {new_record}")
    #
    # retrieved_record = db_session.query(DataRecord).first()
    # print(f"Retrieved record: {retrieved_record}")
    # db_session.close()
