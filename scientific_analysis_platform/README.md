# Scientific Analysis Platform for Changjiang River Basin Studies

This project aims to develop a comprehensive scientific analysis platform to support research on the "Water-Sediment Dynamics, Hydrological Connectivity, Wetlands, and Aquatic Ecosystem Status and Evolution in the Middle Reaches of the Yangtze River."

The platform integrates data management, model integration, visualization analysis, AI-enhanced system evolution knowledge graphs, and a deep research assistant.

## Project Goal

To provide an advanced analytical environment that empowers researchers to:
- Manage and access diverse spatio-temporal datasets using a PostGIS enabled database.
- Integrate and run various scientific models (hydrological, ecological, etc.) via wrapper interfaces.
- Visualize complex data and model outputs interactively (maps, charts).
- Explore system-level evolution patterns and relationships through an **Evolution Knowledge Graph (EKG)** with a lightweight backend and basic frontend visualizer.
- Leverage an AI **Deep Research Assistant** with Natural Language Query (NLQ) capabilities (prototype using RAG with simulated components), automated literature summarization (simulated), data-driven hypothesis generation (simulated), and scenario interpretation assistance (simulated).

## Modules

The platform is structured into the following core modules:

1.  **Core (`core/`)**: (Currently minimal)
2.  **Data Management (`data_management/`)**:
    -   `models.py`: SQLAlchemy models for PostGIS (GeoAlchemy2).
    -   `api_routes.py`: Backend APIs for data query.
    -   `importers/`: Scripts for data import.
    -   `spatial_analysis.py`: Conceptual spatio-temporal analysis functions.
    -   `data_fusion.py`: Conceptual data fusion interface.
    -   `DATA_ACQUISITION_CHECKLIST.md`, `DATA_STANDARDIZATION_GUIDE.md`.
3.  **Model Integration (`model_integration/`)**:
    -   `model_interface.py`: `ScientificModel` ABC.
    -   `model_manager.py`: Model lifecycle management.
    -   `models/`: Conceptual wrappers for MaxEnt, SWAT, VIC.
4.  **Visualization (`visualization/`)**:
    -   `routes.py`: Flask Blueprint for web pages.
    -   `templates/`: HTML templates (Leaflet, Chart.js, Vis.js for EKG).
        - `ekg_visualizer.html`: Basic visualizer for the EKG.
        - `scenario_simulator.html`: UI placeholder for scenario simulation.
    -   `static/`: CSS and JavaScript.
5.  **AI Knowledge Graph (`ai_knowledge_graph/`)**: The **Evolution Knowledge Graph (EKG)**.
    -   `graph_schema.py`: Extended schema for evolutionary aspects (TemporalEvents, EntityStates).
    -   `lightweight_graph_store.py`: Implements a JSON file-based graph data store.
    -   `graph_builder.py`, `graph_querier.py`: Adapted to use the `LightweightGraphStore`.
    -   `api_routes_ekg.py`: Backend APIs for interacting with the EKG (CRUD for nodes/edges, sample graph).
    -   `data/evolution_graph_data.json`: Default persistence file for the EKG.
6.  **Research Assistant (`research_assistant/`)**: AI-powered assistant.
    -   `assistant_core.py`: Core logic with RAG pipeline, and (simulated) literature summary, hypothesis generation, and scenario interpretation features.
    -   `document_processor.py`, `embedding_service.py`, `vector_store.py`: (Simulated) RAG components.
    -   `hypothesis_generator.py`: (Simulated) Data-driven hypothesis generation.
    -   `AI_ENGINE_STRATEGY.md`: LLM and RAG integration strategy.
    -   `sample_data/literature/`: Sample text files for RAG literature processing.
7.  **Application (`app.py`)**: Main Flask application.
8.  **Sample Data (`sample_data/`)**: CSV, GeoJSON for DB import, and literature text files.
9.  **Tests (`tests/`)**: (To be developed)

## Getting Started
...(Instructions remain largely the same as before, just need to ensure `data` directory is mentioned or created by `app.py`)...

### 5. Initialize Database Schema and EKG Store
...
```bash
python -m scientific_analysis_platform.data_management.models
# (The EKG JSON file will be created/loaded automatically by the EKG API/services when first accessed)
# (The data/ directory is created by app.py if it doesn't exist)
```
...

### 8. Access the Platform
... You should see:
*   ...
*   EKG Visualizer (`/view/ekg`) - click "Load/Refresh Graph Sample" to see a basic graph.
*   Scenario Simulator (`/view/scenario-simulator`) - UI placeholder.
*   Research Assistant (`/assistant`) - try:
    *   "What is this platform about?" (RAG from README)
    *   "summarize literature on sediment load" (RAG from sample literature)
    *   "generate hypothesis for: Wetland area in Dongting has decreased by 20%." (Simulated hypothesis)
    *   Use Scenario Simulator UI then "Interpret Results with AI".
*   EKG APIs (e.g., `/api/ekg/graph_sample`, `/api/ekg/health`).

## Current Status

The platform prototype now includes:
- Dockerized PostGIS, SQLAlchemy/GeoAlchemy2 schema, data importers, and data APIs.
- Frontend visualizations for maps (Leaflet), charts (Chart.js).
- **Evolution Knowledge Graph (EKG)**:
    - Extended schema for temporal events and entity states.
    - Lightweight JSON file-based backend for graph data storage.
    - APIs for basic EKG node/edge manipulation and data retrieval.
    - Basic frontend visualizer using Vis.js to display a sample EKG.
- **Deep Research Assistant** enhancements (features are simulated/conceptual):
    - RAG pipeline extended to include sample literature texts.
    - Automated literature summarization based on RAG.
    - Data-driven hypothesis generation based on textual observations.
    - Scenario simulation UI placeholder.
    - AI-driven interpretation of (placeholder) scenario simulation results.
- Conceptual placeholders for advanced spatio-temporal analysis and mechanistic model wrappers (MaxEnt, SWAT, VIC).

Next steps involve moving from conceptual/simulated AI features to real implementations, fleshing out the EKG with actual data, and further developing analytical capabilities.
...

---

*This README provides setup instructions for the current prototype. It will be updated as the project progresses.*
