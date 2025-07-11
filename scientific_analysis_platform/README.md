# Scientific Analysis Platform for Changjiang River Basin Studies

This project aims to develop a comprehensive scientific analysis platform to support research on the "Water-Sediment Dynamics, Hydrological Connectivity, Wetlands, and Aquatic Ecosystem Status and Evolution in the Middle Reaches of the Yangtze River."

The platform integrates data management, model integration, visualization analysis, AI-enhanced system evolution knowledge graphs, and a deep research assistant.

## Project Goal

To provide an advanced analytical environment that empowers researchers to:
- Manage and access diverse spatio-temporal datasets using a PostGIS enabled database.
- Integrate and run various scientific models (hydrological, ecological, etc.).
- Visualize complex data and model outputs interactively (maps, charts).
- Explore system-level evolution patterns and relationships through an AI-driven knowledge graph.
- Leverage an AI research assistant for querying information, literature review, and report generation.

## Modules

The platform is structured into the following core modules:

1.  **Core (`core/`)**: Contains shared utilities, configurations, and base classes. (Currently minimal)
2.  **Data Management (`data_management/`)**: Handles ingestion, storage, processing, and querying of data.
    -   `models.py`: SQLAlchemy models for the PostGIS database schema (using GeoAlchemy2).
    -   `api_routes.py`: Flask Blueprint for data-related backend APIs.
    -   `importers/`: Scripts to import data from various sources (e.g., CSV, GeoJSON) into the database.
    -   `DATA_ACQUISITION_CHECKLIST.md`: Lists required datasets and their characteristics.
    -   `DATA_STANDARDIZATION_GUIDE.md`: Outlines data standardization procedures.
3.  **Model Integration (`model_integration/`)**: Facilitates integration and management of scientific models. (Skeleton)
    -   `model_interface.py`: Defines the `ScientificModel` abstract base class.
    -   `model_manager.py`: Manages model lifecycle.
4.  **Visualization (`visualization/`)**: Provides tools for interactive web-based visualization.
    -   `routes.py`: Flask Blueprint for visualization-related web pages (Data Catalog, Map, Charts).
    -   `templates/`: HTML templates (using Leaflet.js for maps, Chart.js for charts).
    -   `static/`: CSS and JavaScript files.
5.  **AI Knowledge Graph (`ai_knowledge_graph/`)**: For building and querying an AI-enhanced knowledge graph. (Skeleton)
    -   `graph_schema.py`: Conceptual schema definition.
    -   `graph_builder.py`, `graph_querier.py`: Placeholder classes.
6.  **Research Assistant (`research_assistant/`)**: AI-powered assistant. (Basic placeholder)
    -   `assistant_core.py`: Core logic.
7.  **Application (`app.py`)**: The main Flask web application entry point, routing, and initialization.
8.  **Sample Data (`sample_data/`)**: Contains sample CSV and GeoJSON files for initial data import.
9.  **Tests (`tests/`)**: For unit and integration tests. (To be developed)

## Getting Started

Follow these steps to set up and run the platform locally:

### Prerequisites

*   **Python**: Version 3.9 or higher.
*   **Docker & Docker Compose**: For running the PostGIS database.
*   **Git**: For cloning the repository.

### 1. Clone the Repository

```bash
git clone https://github.com/caminsar/aiplanet.git
cd aiplanet/scientific_analysis_platform
# (or your specific path to the scientific_analysis_platform directory)
```

### 2. Set Up Python Environment

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure and Run PostGIS Database using Docker

The platform uses a PostGIS database. A `docker-compose.yml` file is provided for easy setup.

*   **(Optional) Create a `.env` file:** In the `scientific_analysis_platform` directory, you can create a `.env` file to customize database credentials or port. If not provided, defaults will be used.
    Example `.env` content:
    ```env
    POSTGRES_USER=my_custom_user
    POSTGRES_PASSWORD=my_strong_password
    POSTGRES_DB=my_platform_db
    POSTGRES_PORT=5433
    ```
    If you set `POSTGRES_PORT` here, ensure it matches the port used in `POSTGRES_DB_URL` later.

*   **Start the PostGIS service:**
    ```bash
    docker-compose up -d db_postgis
    ```
    This will download the PostGIS image (if not already present) and start the database container in detached mode. The data will be persisted in a Docker volume named `postgis_data`.

### 4. Set Environment Variable for Database URL

The Flask application needs to know how to connect to the PostGIS database. Set the `POSTGRES_DB_URL` environment variable.

*   If you used default settings in `docker-compose.yml` and did not create a `.env` file, the default connection URL is:
    ```bash
    export POSTGRES_DB_URL="postgresql://platform_user:platform_secret_password@localhost:5432/scientific_platform_dev"
    ```
*   If you customized using a `.env` file (e.g., user `my_custom_user`, password `my_strong_password`, db `my_platform_db`, and port `5433`):
    ```bash
    export POSTGRES_DB_URL="postgresql://my_custom_user:my_strong_password@localhost:5433/my_platform_db"
    ```
    *(On Windows, use `set POSTGRES_DB_URL="..."` for Command Prompt or `$env:POSTGRES_DB_URL = "..."` for PowerShell)*

### 5. Initialize Database Schema

Once the PostGIS container is running and the `POSTGRES_DB_URL` is set, initialize the database schema (create tables):

```bash
python -m scientific_analysis_platform.data_management.models
```
You should see output indicating successful connection and table creation, including a PostGIS version check.

### 6. Import Initial Sample Data

Run the provided script to populate the database with sample datasets:

```bash
python -m scientific_analysis_platform.data_management.run_importers
```
This will import data from the `sample_data/` directory.

### 7. Run the Flask Application

```bash
python app.py
```
The application should now be running, typically at `http://localhost:5000` (or `http://0.0.0.0:5000`).

### 8. Access the Platform

Open your web browser and navigate to `http://localhost:5000`. You should see:
*   The homepage.
*   Visualization Hub (`/view/`).
*   Interactive Map (`/view/map`) showing station locations.
*   Data Charts (`/view/chart`) allowing selection of stations and parameters.
*   Data Catalog (`/view/catalog`) listing available data types.
*   Research Assistant (`/assistant`).
*   Data APIs (e.g., `/api/data/stations`, `/api/data/wetlands`).

### Stopping the Database

To stop the PostGIS container:
```bash
docker-compose down
```
To stop and remove the data volume (all data will be lost):
```bash
docker-compose down -v
```

## Current Status

The project has a foundational skeleton with:
- Dockerized PostGIS setup.
- Defined database schema using SQLAlchemy and GeoAlchemy2.
- Sample data importers.
- Backend APIs for accessing station and wetland data.
- Frontend prototypes for data catalog, map visualization (Leaflet), and chart visualization (Chart.js).
- Basic Research Assistant placeholder.

Next steps will involve further development of each module, adding more complex features, and refining the existing ones.

## Contributing (Placeholder)

(Contribution guidelines will be added here.)

---

*This README provides setup instructions for the current prototype. It will be updated as the project progresses.*
