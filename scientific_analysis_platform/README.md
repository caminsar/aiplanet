# Scientific Analysis Platform for Changjiang River Basin Studies

This project aims to develop a comprehensive scientific analysis platform to support research on the "Water-Sediment Dynamics, Hydrological Connectivity, Wetlands, and Aquatic Ecosystem Status and Evolution in the Middle Reaches of the Yangtze River."

The platform integrates data management, model integration, visualization analysis, AI-enhanced system evolution knowledge graphs, and a deep research assistant.

## Project Goal

To provide an advanced analytical environment that empowers researchers to:
- Manage and access diverse spatio-temporal datasets.
- Integrate and run various scientific models (hydrological, ecological, etc.).
- Visualize complex data and model outputs interactively.
- Explore system-level evolution patterns and relationships through an AI-driven knowledge graph.
- Leverage an AI research assistant for querying information, literature review, and report generation.

## Modules

The platform is structured into the following core modules:

1.  **Core (`core/`)**: Contains shared utilities, configurations, and base classes used across the platform.
2.  **Data Management (`data_management/`)**: Handles ingestion, storage, processing, and querying of multi-source heterogeneous data (hydrological, meteorological, geographical, ecological).
    -   `models.py`: SQLAlchemy models for database schema.
    -   `data_handlers.py`: Interfaces for data sources, importers, and exporters.
3.  **Model Integration (`model_integration/`)**: Facilitates the integration, configuration, execution, and management of various scientific models.
    -   `model_interface.py`: Defines the `ScientificModel` abstract base class and related data structures for model parameters, inputs, and outputs.
    -   `model_manager.py`: Manages the lifecycle of registered models.
4.  **Visualization (`visualization/`)**: Provides tools for interactive visualization of data and model results, including maps and charts.
    -   `templates/`: HTML templates for web pages.
    -   `static/`: CSS and JavaScript files.
5.  **AI Knowledge Graph (`ai_knowledge_graph/`)**: Focuses on building and querying an AI-enhanced knowledge graph representing system components, relationships, and their evolution over time.
    -   `graph_schema.py`: Defines the conceptual schema (node types, relationship types) for the knowledge graph.
    -   `graph_builder.py`: Placeholder for logic to construct the graph.
    -   `graph_querier.py`: Placeholder for logic to query the graph.
6.  **Research Assistant (`research_assistant/`)**: An AI-powered assistant to help researchers with queries, literature searches, and other tasks.
    -   `assistant_core.py`: Core logic for the research assistant.
7.  **Application (`app.py`)**: The main Flask web application entry point, routing, and initialization.
8.  **Tests (`tests/`)**: Contains unit tests, integration tests, etc. (To be developed).

## Getting Started (Placeholder)

(Detailed setup instructions will be added here, including dependencies, database setup, and how to run the application.)

1.  Clone the repository: `git clone https://github.com/caminsar/aiplanet.git`
2.  Navigate to the `scientific_analysis_platform` directory: `cd aiplanet/scientific_analysis_platform` (or wherever it's cloned relative to this README).
3.  Install dependencies: `pip install -r requirements.txt` (requirements.txt to be created)
4.  Configure database settings (details TBD).
5.  Run the Flask application: `python app.py`
6.  Access the platform via a web browser, typically at `http://localhost:5000`.

## Current Status

The project is in the initial development phase. Core module skeletons and basic functionalities are being established.

## Contributing (Placeholder)

(Contribution guidelines will be added here.)

---

*This README is a preliminary version and will be updated as the project progresses.*
