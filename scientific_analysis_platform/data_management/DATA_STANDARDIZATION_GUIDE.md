# Data Standardization Guide for Scientific Analysis Platform

This guide outlines the procedures and conventions for standardizing data collected for the Changjiang River Middle Reach study. Standardization is crucial for ensuring data quality, interoperability, and compatibility with the platform's data management, modeling, and analysis modules.

## I. General Principles

1.  **Uniform Data Model:** All processed data should ideally conform to the core data models defined in the platform (e.g., `DataRecord` and specialized tables in `data_management/models.py`), including consistent naming for common attributes (e.g., `timestamp`, `latitude`, `longitude`, `parameter_name`, `value`, `unit`).
2.  **Comprehensive Metadata:** Each dataset and data point (where applicable) must be accompanied by comprehensive metadata. This includes provenance (source, collection methods), processing history, quality flags, spatial reference systems, temporal resolution, units of measurement, and parameter definitions.
3.  **Controlled Vocabularies/Ontologies:** Where possible, use controlled vocabularies or ontologies for parameter names, units, species names, LULC classes, etc., to ensure consistency and facilitate semantic queries. (e.g., CF Conventions for climate/forecast data, BODC parameter codes, WoRMS for species).
4.  **Data Quality Assurance:** Implement QA/QC checks during the standardization process (e.g., range checks, outlier detection, consistency checks). Document any quality issues.
5.  **Version Control:** Standardized datasets should be versioned, especially if they undergo updates or re-processing.

## II. Standardization Workflow

The general workflow for standardizing a raw dataset involves the following steps:

1.  **Data Ingestion & Initial Inspection:**
    *   Receive or download raw data.
    *   Inspect the data format, structure, and content.
    *   Review any accompanying metadata or documentation.
    *   Identify potential issues (e.g., inconsistent formatting, missing data, unclear units).

2.  **Format Conversion (if necessary):**
    *   Convert proprietary or uncommon formats to standard, open formats (e.g., CSV, GeoJSON, NetCDF, GeoTIFF).
    *   **Tools:** GDAL/OGR, Pandas, xarray, custom scripts.

3.  **Structural Reformatting:**
    *   **Tabular Data (CSV, Excel):**
        *   Ensure consistent column headers. Standardize column names (e.g., `date_time` to `timestamp`, `station_id` to `station_identifier`).
        *   Handle merged cells, multiple header rows, or footnotes appropriately.
        *   Reshape data if necessary (e.g., from wide to long format or vice-versa) to fit the target database schema.
    *   **Spatial Data (Shapefiles, GeoJSON, Rasters):**
        *   Verify geometry validity.
        *   Ensure attribute tables have consistent field names.

4.  **Data Cleaning & Preprocessing:**
    *   **Missing Values:**
        *   Identify missing data (e.g., `NaN`, `None`, `-9999`).
        *   Adopt a consistent representation for missing values in the standardized dataset (e.g., `NULL` in databases, `NaN` in Pandas).
        *   Document the strategy for handling missing values (e.g., removal, imputation with justification).
    *   **Outlier Detection & Handling:**
        *   Apply domain-specific rules or statistical methods to detect outliers.
        *   Document outliers and the strategy for handling them (e.g., flagging, correction if erroneous, removal with justification).
    *   **Date/Time Standardization:**
        *   Convert all date and time information to a standard format (e.g., ISO 8601: `YYYY-MM-DDTHH:MM:SSZ` or `YYYY-MM-DD HH:MM:SS`).
        *   Ensure consistent timezone handling (preferably UTC for storage, with timezone information stored as metadata if original data was local).
    *   **Text & Categorical Data:**
        *   Normalize text (e.g., case consistency, remove leading/trailing whitespace).
        *   Map categorical values to a controlled vocabulary (e.g., "forest" vs "Forestland" -> "Forest").
        *   Handle special characters and encoding issues (ensure UTF-8 where possible).

5.  **Unit Conversion:**
    *   Identify units for all numerical parameters.
    *   Convert all values to a predefined standard unit for each parameter type (e.g., all temperature data to Celsius, all flow rates to m³/s, all lengths/areas to SI units).
    *   Document original units and conversion factors.

6.  **Spatial Data Standardization:**
    *   **Coordinate Reference System (CRS):**
        *   Identify the CRS of all spatial data.
        *   Reproject all spatial data to a consistent project-wide CRS (e.g., WGS 84 - EPSG:4326 for general use, or a projected CRS like UTM for specific regional analysis if distortion is a concern). Document the chosen standard CRS.
    *   **Geometric Operations (if needed):**
        *   Simplify or generalize geometries if necessary for performance, with documented tolerances.
        *   Ensure topological correctness for vector data (e.g., no self-intersections in polygons).
    *   **Raster Data:**
        *   Align raster grids (common origin and resolution) if datasets are to be used together in cell-by-cell operations.
        *   Standardize NoData values.

7.  **Metadata Generation & Association:**
    *   Create comprehensive metadata for the standardized dataset. This should include:
        *   **Identification:** Title, abstract, keywords.
        *   **Provenance:** Original source, collection method, processing steps applied during standardization, version.
        *   **Spatial Details:** Geographic extent, CRS.
        *   **Temporal Details:** Time period covered, temporal resolution.
        *   **Data Quality:** Accuracy assessments, completeness, logical consistency, known issues.
        *   **Parameter Information:** For each parameter, its name, definition, standard unit, and original unit.
    *   Store metadata in a structured format (e.g., JSON, XML, or dedicated metadata tables in the database) and link it to the data. Adhere to standards like ISO 19115 or Dublin Core where feasible.

8.  **Loading into Platform Database:**
    *   Use importer scripts (see `DATA_ACQUISITION_CHECKLIST.md` and future importer modules) to load the standardized data and its metadata into the PostGIS database, conforming to the platform's schema.
    *   Perform validation checks during and after loading to ensure data integrity.

## III. Specific Data Type Considerations

*   **Time Series Data:**
    *   Ensure regular time steps where expected. Flag or interpolate irregular steps with caution and documentation.
    *   Clearly define whether observations are instantaneous, averages, or accumulations over a time period.
*   **Remote Sensing Imagery:**
    *   Specify processing levels (e.g., L1, L2).
    *   Document atmospheric corrections, radiometric calibrations, and geometric corrections applied.
*   **Model Outputs:**
    *   Standardize output formats (e.g., NetCDF for gridded data, CSV for time series).
    *   Include metadata about the model run (model name, version, input parameters, run date).

## IV. Tools and Technologies (Examples)

*   **Scripting:** Python (with Pandas, GeoPandas, NumPy, xarray, SciPy).
*   **Spatial Data Processing:** GDAL/OGR, QGIS, ArcGIS, PostGIS functions.
*   **Database:** PostgreSQL with PostGIS.
*   **Version Control:** Git (for scripts and potentially small reference datasets), DVC (for large datasets).

## V. Documentation and Review

*   Maintain a log for each dataset detailing the standardization steps performed, decisions made, and any issues encountered.
*   Standardized datasets should be reviewed by at least one other team member or domain expert before being finalized for platform integration.

---
This guide provides a general framework. Specific standardization protocols may need to be developed for particularly complex or unique datasets.
