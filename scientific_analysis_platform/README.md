# Scientific Analysis Platform for Changjiang River Basin Studies

This project aims to develop a comprehensive scientific analysis platform to support research on the "Water-Sediment Dynamics, Hydrological Connectivity, Wetlands, and Aquatic Ecosystem Status and Evolution in the Middle Reaches of the Yangtze River."

The platform integrates data management, model integration, visualization analysis, an AI-enhanced Evolution Knowledge Graph (EKG), and a Deep Research Assistant.

## Project Goal

To provide an advanced analytical environment that empowers researchers to:
- Manage and access diverse spatio-temporal datasets using a PostGIS enabled database.
- Integrate and run various scientific models (hydrological, ecological, etc.) via conceptual wrapper interfaces.
- Visualize complex data and model outputs interactively (maps, charts, graphs).
- Explore system-level evolution patterns and relationships through an **Evolution Knowledge Graph (EKG)** featuring a lightweight JSON-file backend and a basic frontend visualizer.
- Leverage an AI **Deep Research Assistant** with Natural Language Query (NLQ) capabilities (prototype using RAG with simulated components), automated literature summarization (simulated), data-driven hypothesis generation (simulated), and scenario interpretation assistance (simulated).

## Modules

The platform is structured into the following core modules:

1.  **Core (`core/`)**: (Currently minimal)
2.  **Data Management (`data_management/`)**:
    -   `models.py`: SQLAlchemy models for PostGIS (GeoAlchemy2).
    -   `api_routes.py`: Backend APIs for data query.
    -   `importers/`: Scripts for data import (stations, wetlands, readings).
    -   `spatial_analysis.py`: Conceptual placeholders for spatio-temporal analysis.
    -   `data_fusion.py`: Conceptual interface for data fusion.
    -   `DATA_ACQUISITION_CHECKLIST.md`, `DATA_STANDARDIZATION_GUIDE.md`.
3.  **Model Integration (`model_integration/`)**:
    -   `model_interface.py`: `ScientificModel` ABC.
    -   `model_manager.py`: Model lifecycle management.
    -   `models/`: Conceptual wrappers for MaxEnt, SWAT, VIC.
4.  **Visualization (`visualization/`)**:
    -   `routes.py`: Flask Blueprint for web pages.
    -   `templates/`: HTML templates (Leaflet for maps, Chart.js for charts, Vis.js for EKG).
        - `ekg_visualizer.html`: Basic visualizer for the EKG.
        - `scenario_simulator.html`: UI placeholder for scenario simulation.
    -   `static/`: CSS and JavaScript.
5.  **AI Knowledge Graph (`ai_knowledge_graph/`)**: The **Evolution Knowledge Graph (EKG)**.
    -   `graph_schema.py`: Extended schema for evolutionary aspects (TemporalEvents, EntityStates).
    -   `lightweight_graph_store.py`: Implements a JSON file-based graph data store.
    -   `graph_builder.py`, `graph_querier.py`: Adapted to use the `LightweightGraphStore`.
    -   `api_routes_ekg.py`: Backend APIs for interacting with the EKG.
    -   `data/evolution_graph_data.json`: Default persistence file for the EKG, pre-populated with sample evolution data.
6.  **Research Assistant (`research_assistant/`)**: AI-powered assistant.
    -   `assistant_core.py`: Core logic with RAG pipeline, and (simulated) literature summary, hypothesis generation, and scenario interpretation features.
    -   `document_processor.py`, `embedding_service.py`, `vector_store.py`: (Simulated) RAG components.
    -   `hypothesis_generator.py`: (Simulated) Data-driven hypothesis generation.
    -   `AI_ENGINE_STRATEGY.md`: LLM and RAG integration strategy.
    -   `sample_data/literature/`: Sample text files for RAG processing by the Research Assistant.
7.  **Application (`app.py`)**: Main Flask application, registers all blueprints.
8.  **Sample Data (`sample_data/`)**:
    - CSV, GeoJSON for PostGIS DB import.
    - `literature/`: Sample text files for RAG processing by the Research Assistant.
9.  **Tests (`tests/`)**:
    - Basic unit tests for `LightweightGraphStore` and `StationCSVImporter`.
    - `TESTING_PLAN.md`: Outlines overall testing strategy.
10. **Deployment & Documentation:**
    - `docker-compose.yml`: For PostGIS and (planned) application deployment.
    - `Dockerfile`: For containerizing the Flask application (to be completed).
    - `PERFORMANCE_OPTIMIZATION_STRATEGY.md`: Conceptual notes on optimization.
    - `CASE_STUDY_DONGTING_LAKE.md`, `DONGTING_CASE_STUDY_WALKTHROUGH.md`: Conceptual application.
    - `ACADEMIC_PAPER_OUTLINE.md`, `USER_MANUAL_DRAFT.md`, `LAUNCH_PLAN.md`, `TRAINING_MATERIALS_OUTLINE.md`: Planning and dissemination documents.


## Getting Started

Follow these steps to set up and run the platform locally:

### Prerequisites

*   **Python**: Version 3.9 or higher.
*   **Docker & Docker Compose**: For running the PostGIS database and potentially the application.
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

(Instructions for `docker-compose up -d db_postgis` remain the same - see `docker-compose.yml` for details on default credentials or using a `.env` file.)

### 4. Set Environment Variable for Database URL

(Instructions for setting `POSTGRES_DB_URL` remain the same.)
Example (defaults): `export POSTGRES_DB_URL="postgresql://platform_user:platform_secret_password@localhost:5432/scientific_platform_dev"`

### 5. Initialize Database Schema and EKG Store

*   **Initialize PostGIS Database Schema:**
    ```bash
    python -m scientific_analysis_platform.data_management.models
    ```
*   **EKG Data:** The `data/evolution_graph_data.json` file is pre-populated with sample data. The EKG APIs will use this file. The `scientific_analysis_platform/data` directory is created by `app.py` if it doesn't exist.

### 6. Import Initial Sample Data into PostGIS

```bash
python -m scientific_analysis_platform.data_management.run_importers
```

### 7. Run the Flask Application

```bash
python app.py
```
The application should now be running, typically at `http://localhost:5000`.

### 8. Access and Explore the Platform

Open your web browser and navigate to `http://localhost:5000`. Key features to explore:
*   **Data Catalog (`/view/catalog`):** Discover available data types.
*   **Interactive Map (`/view/map`):** View hydrological station locations.
*   **Data Charts (`/view/chart`):** Plot time series data for stations.
*   **EKG Visualizer (`/view/ekg`):** Load and view the sample Evolution Knowledge Graph.
*   **Scenario Simulator (`/view/scenario-simulator`):** Input conceptual scenario parameters and get placeholder outputs and (simulated) AI interpretations.
*   **Research Assistant (`/assistant`):**
    *   Ask general questions (e.g., "What is this platform about?" - uses RAG on README).
    *   Request literature summaries (e.g., "summarize literature on wetland changes in Dongting Lake").
    *   Ask for hypothesis generation (e.g., "generate hypothesis for: Dongting Lake wetland area has decreased significantly.").
*   **APIs:** Explore backend data APIs (e.g., `/api/data/stations`) and EKG APIs (e.g., `/api/ekg/graph_sample`).

### (Optional) Dockerized Application Deployment

A `Dockerfile` and an extended `docker-compose.yml` (with the `web_app` service) are planned for containerizing the Flask application. See comments within `docker-compose.yml` for future instructions.

### Stopping Services

*   To stop the Flask app: `Ctrl+C` in the terminal where it's running.
*   To stop the PostGIS container: `docker-compose down` (from the `scientific_analysis_platform` directory).
*   To stop and remove the PostGIS data volume: `docker-compose down -v`.

## Current Status

This prototype demonstrates an integrated platform with:
- A PostGIS backend for structured spatio-temporal data, with sample importers.
- RESTful APIs for data access.
- A frontend with data catalog, map (Leaflet), and chart (Chart.js) visualizations.
- An **Evolution Knowledge Graph (EKG)** module with:
    - An extended schema for temporal events and entity states.
    - A lightweight JSON file-based backend.
    - APIs for basic EKG interaction.
    - A frontend visualizer (Vis.js) for sample graph data.
- A **Deep Research Assistant** with (simulated/mocked) AI capabilities:
    - RAG-based NLQ using project documents and sample literature.
    - Automated literature summarization.
    - Data-driven hypothesis generation.
    - AI-assisted interpretation of (placeholder) scenario simulation results.
- Conceptual placeholders for advanced spatio-temporal analysis and mechanistic model integration (MaxEnt, SWAT, VIC).
- Initial unit tests, testing plan, and strategies for performance optimization and deployment.
- Comprehensive documentation including this README, user manual draft, and conceptual academic/dissemination outlines.

The platform provides a solid foundation for future development, particularly in replacing simulated AI components with real services, fully implementing model integrations, and populating the EKG with real-world evolutionary data.

## Contributing (Placeholder)
(Details to be added)

---

*This README provides setup instructions for the current prototype. It will be updated as the project progresses.*
