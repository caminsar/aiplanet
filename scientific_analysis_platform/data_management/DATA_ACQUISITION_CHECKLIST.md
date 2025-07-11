# Data Acquisition Checklist for Changjiang River Middle Reach Study

This document outlines the key datasets required for the research project: "Water-Sediment Dynamics, Hydrological Connectivity, Wetlands, and Aquatic Ecosystem Status and Evolution in the Middle Reaches of the Yangtze River." It also specifies potential sources, formats, and desired resolutions.

## I. Hydro-Meteorological Data

1.  **River Hydrology (Mainstream & Key Tributaries - e.g., Han, Xiang, Zi, Yuan, Li rivers, Dongting Lake system):**
    *   **Parameters:** Water level, discharge (flow rate), sediment concentration, sediment load, flow velocity.
    *   **Temporal Resolution:** Daily or higher (hourly if available, especially for flood events). Historical records as far back as possible.
    *   **Spatial Resolution:** Key hydrological stations (e.g., Yichang, Shashi, Hankou, Luoshan, Datong, Dongting Lake outlets - Chenglingji).
    *   **Potential Sources:** Changjiang Water Resources Commission (CWRC), Ministry of Water Resources (MWR) yearbooks, local hydrological bureaus, published research.
    *   **Formats:** CSV, Excel, text files, specific hydrological data formats.
    *   **Notes:** Prioritize long-term, continuous datasets. Metadata for station location (lat/lon/elevation), measurement methods, and data quality flags are crucial.

2.  **Meteorological Data:**
    *   **Parameters:** Precipitation (daily, hourly), air temperature (min/max/mean), evaporation, wind speed & direction, solar radiation, humidity.
    *   **Temporal Resolution:** Daily or higher.
    *   **Spatial Resolution:** Weather stations covering the middle Yangtze basin and key sub-catchments. Gridded datasets (e.g., from CMA, TRMM, GPM, ERA5) can supplement station data.
    *   **Potential Sources:** China Meteorological Administration (CMA), provincial meteorological bureaus, global reanalysis products (ECMWF, NOAA), research datasets.
    *   **Formats:** CSV, Excel, NetCDF, GRIB.

3.  **Reservoir/Dam Operations Data:**
    *   **Parameters:** Inflow, outflow, water level, storage volume, operational rules/schedules for major dams (e.g., Three Gorges Dam, Gezhouba, Danjiangkou).
    *   **Temporal Resolution:** Daily or higher.
    *   **Potential Sources:** CWRC, dam operation authorities, research publications.
    *   **Formats:** CSV, Excel, specific operational logs.

## II. Geospatial Data

1.  **Digital Elevation Model (DEM):**
    *   **Parameters:** Elevation, slope, aspect.
    *   **Spatial Resolution:** 30m or better (e.g., SRTM, ASTER GDEM, ALOS PALSAR DEM, national DEM products). Higher resolution for specific study areas (e.g., river channels, wetlands - potentially from LiDAR or drone surveys if available).
    *   **Potential Sources:** USGS EarthExplorer, JAXA, National Geomatics Center of China, research projects.
    *   **Formats:** GeoTIFF, IMG.

2.  **River Network and Catchment Boundaries:**
    *   **Parameters:** Streamlines, river order, sub-catchment delineations.
    *   **Potential Sources:** HydroSHEDS, national hydrological datasets, manual digitization from high-resolution imagery based on DEMs.
    *   **Formats:** Shapefile, GeoJSON, GDB.

3.  **Land Use/Land Cover (LULC):**
    *   **Parameters:** LULC classes (e.g., forest, agriculture, urban, water, wetland).
    *   **Temporal Resolution:** Multi-temporal snapshots (e.g., every 5-10 years, or annually if possible for recent periods) to assess changes.
    *   **Spatial Resolution:** 30m or better (e.g., Landsat-derived products, Sentinel-derived products, GlobeLand30, FROM-GLC).
    *   **Potential Sources:** CAS (Resource and Environment Science and Data Center), NASA, ESA, academic institutions.
    *   **Formats:** GeoTIFF, Shapefile.

4.  **Soil Data:**
    *   **Parameters:** Soil type, texture, organic matter content, hydraulic properties.
    *   **Potential Sources:** Harmonized World Soil Database (HWSD), SoilGrids, national soil survey data.
    *   **Formats:** GeoTIFF, Shapefile, specific soil database formats.

5.  **Wetland Extent and Type:**
    *   **Parameters:** Wetland boundaries, classification (e.g., lacustrine, palustrine, riverine), vegetation types within wetlands.
    *   **Temporal Resolution:** Multi-temporal for tracking changes (e.g., Landsat era to present).
    *   **Spatial Resolution:** 30m or better.
    *   **Potential Sources:** Remote sensing imagery analysis (Landsat, Sentinel, Gaofen), national wetland surveys, research publications.
    *   **Formats:** Shapefile, GeoJSON, GeoTIFF (for classified raster).

## III. Water Quality and Ecology Data

1.  **Water Quality Data:**
    *   **Parameters:** Temperature, pH, Dissolved Oxygen (DO), Total Suspended Solids (TSS), Turbidity, Conductivity, Nutrients (Total Nitrogen - TN, Total Phosphorus - TP, Ammonia, Nitrate, Nitrite), Chlorophyll-a, Chemical Oxygen Demand (COD), Biochemical Oxygen Demand (BOD), heavy metals, organic pollutants (if available).
    *   **Temporal Resolution:** Monthly, seasonal, or campaign-based. Continuous monitoring data if available for specific sites.
    *   **Spatial Resolution:** Key river sections, lake monitoring points, pollutant discharge points.
    *   **Potential Sources:** Ministry of Ecology and Environment (MEE), local environmental protection bureaus, research cruises/monitoring projects.
    *   **Formats:** CSV, Excel.

2.  **Sediment Quality Data:**
    *   **Parameters:** Grain size distribution, nutrient content, organic matter, heavy metal concentrations, pollutant levels in bed sediments.
    *   **Temporal Resolution:** Campaign-based, or pre/post specific events (e.g., dam construction).
    *   **Spatial Resolution:** Representative locations in riverbeds, lakebeds, floodplains.
    *   **Potential Sources:** Research projects, environmental impact assessments.
    *   **Formats:** CSV, Excel.

3.  **Aquatic Ecology Data:**
    *   **Parameters:**
        *   Phytoplankton (species composition, biomass, primary productivity).
        *   Zooplankton (species composition, biomass).
        *   Benthic invertebrates (species composition, density, biomass).
        *   Fish (species composition, abundance, biomass, distribution, information on endangered species like Finless Porpoise, Sturgeon).
        *   Aquatic vegetation (species, distribution, coverage, biomass - particularly for wetlands).
    *   **Temporal Resolution:** Seasonal, annual, or specific survey periods.
    *   **Spatial Resolution:** Representative habitats, transects, monitoring sites.
    *   **Potential Sources:** Research institutions (e.g., Institute of Hydrobiology CAS), fisheries departments, ecological survey reports, long-term ecological research stations.
    *   **Formats:** CSV, Excel, species occurrence databases.

## IV. Socio-Economic Data (Optional, for driving factor analysis)

1.  **Population Data:** Density, distribution.
2.  **Economic Indicators:** GDP, agricultural output, industrial output by sector.
3.  **Water Use Data:** Agricultural, industrial, domestic water consumption.
4.  **Infrastructure Data:** Location of major hydraulic structures, ports, cities.
    *   **Potential Sources:** National Bureau of Statistics, local government yearbooks, research datasets.
    *   **Formats:** CSV, Excel, Shapefile.

## V. Research Literature & Reports

*   **Content:** Peer-reviewed papers, technical reports, theses, environmental impact assessments relevant to the study area and topics.
*   **Potential Sources:** Web of Science, Scopus, CNKI, institutional repositories, government portals.
*   **Formats:** PDF, DOCX (text extraction will be needed). Metadata (authors, title, abstract, keywords, DOI) in CSV, RIS, BibTeX.

---
**General Note:** For all datasets, comprehensive metadata is essential. This includes data collection methods, processing steps, quality assurance/quality control (QA/QC) procedures, coordinate systems, units, and contact information for data providers. Priority should be given to officially published or validated datasets.
