from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session, joinedload # For eager loading relationships
from geoalchemy2.shape import to_shape # To convert PostGIS geometry to Shapely objects
import datetime

# Assuming models.py and SessionLocal are accessible from this path
# Adjust if your project structure or how you manage sessions is different
from .models import SessionLocal, HydrologicalStation, TimeSeriesReading, WetlandArea

data_api_bp = Blueprint('data_api', __name__, url_prefix='/api/data')

def get_db_session():
    """Helper to get a DB session."""
    return SessionLocal()

@data_api_bp.route('/stations', methods=['GET'])
def list_stations():
    """
    List all hydrological stations.
    Returns basic info: id, station_id_code, name, river_name, and WKT location.
    """
    db: Session = get_db_session()
    try:
        stations = db.query(HydrologicalStation).options(joinedload(HydrologicalStation.readings).load_only(TimeSeriesReading.id)).all() # Example of loading only count or specific fields

        result = []
        for station in stations:
            location_wkt = to_shape(station.location).wkt if station.location else None
            result.append({
                "id": station.id,
                "station_id_code": station.station_id_code,
                "name": station.name,
                "river_name": station.river_name,
                "location_wkt": location_wkt, # Well-Known Text representation of geometry
                "latitude": to_shape(station.location).y if station.location else None,
                "longitude": to_shape(station.location).x if station.location else None,
                "elevation_m": station.elevation_m,
                "operator": station.operator,
                "readings_count": db.query(TimeSeriesReading).filter(TimeSeriesReading.station_id == station.id).count() # Efficient count
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@data_api_bp.route('/stations/<string:station_id_code>/details', methods=['GET'])
def get_station_details(station_id_code: str):
    """Get detailed information for a specific station by its code."""
    db: Session = get_db_session()
    try:
        station = db.query(HydrologicalStation).filter(HydrologicalStation.station_id_code == station_id_code).first()
        if not station:
            return jsonify({"error": "Station not found"}), 404

        location_wkt = to_shape(station.location).wkt if station.location else None
        return jsonify({
            "id": station.id,
            "station_id_code": station.station_id_code,
            "name": station.name,
            "river_name": station.river_name,
            "basin_name": station.basin_name,
            "location_wkt": location_wkt,
            "latitude": to_shape(station.location).y if station.location else None,
            "longitude": to_shape(station.location).x if station.location else None,
            "elevation_m": station.elevation_m,
            "established_date": station.established_date.isoformat() if station.established_date else None,
            "operator": station.operator,
            "remarks": station.remarks
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@data_api_bp.route('/stations/<string:station_id_code>/readings', methods=['GET'])
def get_station_readings(station_id_code: str):
    """
    Get time series readings for a specific station.
    Supports time range filtering via query parameters `start_time` and `end_time` (ISO format).
    Supports parameter filtering via `parameter_name`.
    """
    db: Session = get_db_session()
    try:
        station = db.query(HydrologicalStation).filter(HydrologicalStation.station_id_code == station_id_code).first()
        if not station:
            return jsonify({"error": "Station not found"}), 404

        query = db.query(TimeSeriesReading).filter(TimeSeriesReading.station_id == station.id)

        start_time_str = request.args.get('start_time')
        end_time_str = request.args.get('end_time')
        parameter_name_filter = request.args.get('parameter_name')

        if start_time_str:
            try:
                start_time = datetime.datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
                query = query.filter(TimeSeriesReading.timestamp >= start_time)
            except ValueError:
                return jsonify({"error": "Invalid start_time format. Use ISO 8601."}), 400

        if end_time_str:
            try:
                end_time = datetime.datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))
                query = query.filter(TimeSeriesReading.timestamp <= end_time)
            except ValueError:
                return jsonify({"error": "Invalid end_time format. Use ISO 8601."}), 400

        if parameter_name_filter:
            query = query.filter(TimeSeriesReading.parameter_name == parameter_name_filter)

        query = query.order_by(TimeSeriesReading.timestamp.asc()) # Default order

        # Add pagination later if needed
        readings = query.all()

        result = [{
            "id": reading.id,
            "timestamp": reading.timestamp.isoformat(),
            "parameter_name": reading.parameter_name,
            "value": reading.value,
            "unit": reading.unit,
            "quality_flag": reading.quality_flag
        } for reading in readings]

        return jsonify({
            "station_id_code": station.station_id_code,
            "station_name": station.name,
            "readings": result
        })
    except Exception as e:
        # import traceback; traceback.print_exc() # For debugging
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@data_api_bp.route('/wetlands', methods=['GET'])
def list_wetlands():
    """
    List all wetland areas.
    Returns basic info including GeoJSON representation of their boundary.
    """
    db: Session = get_db_session()
    try:
        wetlands = db.query(WetlandArea).all()
        result_features = []
        for wetland in wetlands:
            shapely_geom = to_shape(wetland.boundary) if wetland.boundary else None
            feature = {
                "type": "Feature",
                "properties": {
                    "id": wetland.id,
                    "wetland_id_code": wetland.wetland_id_code,
                    "name": wetland.name,
                    "type": wetland.type,
                    "area_sqkm": wetland.area_sqkm,
                    "description": wetland.description
                },
                # GeoJSON geometry format
                "geometry": shapely_geom.__geo_interface__ if shapely_geom else None
            }
            result_features.append(feature)

        return jsonify({
            "type": "FeatureCollection",
            "features": result_features
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@data_api_bp.route('/wetlands/<string:wetland_id_code_or_name>/details', methods=['GET'])
def get_wetland_details(wetland_id_code_or_name: str):
    """Get detailed information for a specific wetland by its code or name."""
    db: Session = get_db_session()
    try:
        wetland = db.query(WetlandArea).filter(
            (WetlandArea.wetland_id_code == wetland_id_code_or_name) |
            (WetlandArea.name == wetland_id_code_or_name)
        ).first()

        if not wetland:
            return jsonify({"error": "Wetland not found"}), 404

        shapely_geom = to_shape(wetland.boundary) if wetland.boundary else None
        return jsonify({
            "type": "Feature",
            "properties": {
                "id": wetland.id,
                "wetland_id_code": wetland.wetland_id_code,
                "name": wetland.name,
                "type": wetland.type,
                "area_sqkm": wetland.area_sqkm,
                "description": wetland.description
            },
            "geometry": shapely_geom.__geo_interface__ if shapely_geom else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Example of a simple health check for the API blueprint
@data_api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Data API is running."})
