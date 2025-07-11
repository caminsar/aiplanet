import json
from sqlalchemy.orm import Session
from shapely.geometry import shape
from geoalchemy2.shape import from_shape

from .base_importer import BaseImporter
from ..models import WetlandArea # Adjust import path as necessary

class WetlandGeoJSONImporter(BaseImporter):
    """
    Importer for wetland area data from a GeoJSON file.
    Expected GeoJSON properties: wetland_id_code, name, type, description (matching WetlandArea model)
    """

    def __init__(self, db_session: Session, file_path: str):
        super().__init__(db_session, file_path)

    def import_data(self):
        self.log_message(f"Starting import of wetland GeoJSON data from: {self.file_path}")
        if not self._file_exists():
            self.log_message(f"File not found: {self.file_path}", level="ERROR")
            return

        try:
            with open(self.file_path, mode='r', encoding='utf-8') as f:
                geojson_data = json.load(f)

            if geojson_data.get("type") != "FeatureCollection":
                self.log_message("GeoJSON is not a FeatureCollection. Skipping.", level="ERROR")
                return

            wetlands_added = 0
            wetlands_updated = 0

            for feature in geojson_data.get("features", []):
                try:
                    properties = feature.get("properties", {})
                    geometry_dict = feature.get("geometry")

                    if not properties or not geometry_dict:
                        self.log_message(f"Skipping feature due to missing properties or geometry: {feature.get('id', 'N/A')}", level="WARN")
                        continue

                    wetland_id_code = properties.get('wetland_id_code')
                    name = properties.get('name')
                    wetland_type = properties.get('type')
                    description = properties.get('description')

                    if not name: # Name is mandatory in our model
                        self.log_message(f"Skipping feature due to missing 'name' property: {properties}", level="WARN")
                        continue

                    # Convert GeoJSON geometry dict to Shapely object, then to GeoAlchemy2 element
                    shapely_geom = shape(geometry_dict)
                    # Ensure it's MultiPolygon as per model, or handle conversion if necessary
                    # For simplicity, we assume the GeoJSON provides compatible geometry types (Polygon or MultiPolygon)
                    # If it's a Polygon, from_shape might handle it, or you might need to wrap it.
                    # The WetlandArea model expects MULTIPOLYGON. If GeoJSON has Polygon, it needs to be wrapped.
                    if shapely_geom.geom_type == 'Polygon':
                        from shapely.geometry import MultiPolygon
                        shapely_geom = MultiPolygon([shapely_geom])

                    boundary_geom = from_shape(shapely_geom, srid=4326) # SRID from GeoJSON usually WGS84

                    # Check if wetland already exists (e.g., by wetland_id_code if available and unique, or by name)
                    # Using wetland_id_code if present and unique, otherwise name could be an alternative.
                    # For this example, let's assume wetland_id_code is the primary business key for existence check.
                    existing_wetland = None
                    if wetland_id_code:
                        existing_wetland = self.db_session.query(WetlandArea).filter_by(wetland_id_code=wetland_id_code).first()

                    if not existing_wetland and name: # Fallback to name if no ID code, or for initial check
                         existing_wetland_by_name = self.db_session.query(WetlandArea).filter_by(name=name).first()
                         if existing_wetland_by_name and not wetland_id_code: # Only use name if no code was given
                             existing_wetland = existing_wetland_by_name


                    if existing_wetland:
                        existing_wetland.name = name # Update name if it changed
                        existing_wetland.boundary = boundary_geom
                        existing_wetland.type = wetland_type
                        existing_wetland.description = description
                        # existing_wetland.area_sqkm = shapely_geom.area # Optional: calculate and store area
                        self.log_message(f"Updating wetland: {existing_wetland.wetland_id_code or name}")
                        wetlands_updated += 1
                    else:
                        new_wetland = WetlandArea(
                            wetland_id_code=wetland_id_code,
                            name=name,
                            boundary=boundary_geom,
                            type=wetland_type,
                            description=description
                            # area_sqkm=shapely_geom.area # Optional
                        )
                        self.db_session.add(new_wetland)
                        self.log_message(f"Adding new wetland: {wetland_id_code or name}")
                        wetlands_added += 1

                except Exception as e:
                    self.log_message(f"Error processing GeoJSON feature {properties.get('name', 'N/A')}: {e}", level="ERROR")
                    self.db_session.rollback()
                    continue

            self.db_session.commit()
            self.log_message(f"Wetland GeoJSON import completed. Added: {wetlands_added}, Updated: {wetlands_updated} wetlands.")

        except FileNotFoundError:
            self.log_message(f"File not found: {self.file_path}", level="ERROR")
        except json.JSONDecodeError as jde:
            self.log_message(f"Error decoding GeoJSON file {self.file_path}: {jde}", level="CRITICAL")
        except Exception as e:
            self.db_session.rollback()
            self.log_message(f"An error occurred during GeoJSON import: {e}", level="CRITICAL")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    from scientific_analysis_platform.data_management.models import SessionLocal, init_db
    import os

    print("Directly running WetlandGeoJSONImporter example...")
    try:
        init_db()
    except Exception as e:
        print(f"Failed to initialize database for importer test: {e}")
        print("Ensure your database server is running and accessible, and POSTGRES_DB_URL is correctly set.")
        exit(1)

    db_session = SessionLocal()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file_path = os.path.join(current_dir, '..', '..', 'sample_data', 'wetland_boundary.geojson')
    sample_file_path = os.path.normpath(sample_file_path)

    if not os.path.exists(sample_file_path):
        print(f"Error: Sample file not found at {sample_file_path}")
    else:
        print(f"Found sample file at: {sample_file_path}")
        importer = WetlandGeoJSONImporter(db_session=db_session, file_path=sample_file_path)
        try:
            importer.import_data()
            print("Wetland GeoJSON import process finished.")
        except Exception as e:
            print(f"An error occurred while running the importer: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db_session.close()
            print("Database session closed.")
