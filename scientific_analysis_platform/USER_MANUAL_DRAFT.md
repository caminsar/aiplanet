# Scientific Analysis Platform - User Manual (Draft)

## 1. Introduction

Welcome to the User Manual for the Scientific Analysis Platform! This platform is designed to assist researchers in studying complex river basin systems, with a particular focus on the Yangtze River. It provides integrated tools for data management, visualization, exploring system evolution, and leveraging AI-powered research assistance.

This manual guides you through the main features and how to use them. As the platform is currently a prototype, some advanced analytical and AI features are simulated or conceptual.

**Target Audience:** Environmental researchers, hydrologists, ecologists, geographers, and data scientists.

## 2. Getting Started

Before using the platform, ensure it has been set up correctly by following the instructions in the main `README.md` file. This typically involves:
1.  Cloning the repository.
2.  Setting up a Python virtual environment and installing dependencies.
3.  Running the PostGIS database using Docker.
4.  Setting the `POSTGRES_DB_URL` environment variable.
5.  Initializing the database schema (`python -m scientific_analysis_platform.data_management.models`).
6.  Importing sample data (`python -m scientific_analysis_platform.data_management.run_importers`).
7.  Running the Flask application (`python app.py`).

Once the application is running (usually at `http://localhost:5000`), you can access it via your web browser.

## 3. Navigating the Platform

The platform features a main navigation bar providing access to its core sections:

*   **Home:** The main welcome page.
*   **Visualization Hub:** A central point for accessing different visualization tools.
*   **Data Catalog:** Browse available datasets and data types.
*   **Interactive Map:** Visualize geospatial data like station locations.
*   **Data Charts:** View time-series data and other graphical representations.
*   **EKG Visualizer:** Explore the Evolution Knowledge Graph.
*   **Scenario Simulator:** (Conceptual) Define scenarios and see placeholder outputs.
*   **Research Assistant:** Interact with the AI assistant for queries and tasks.

## 4. Exploring Data

### 4.1. Data Catalog (`/view/catalog`)
*   **Purpose:** Discover the types of data available within the platform.
*   **How to Use:**
    1.  Navigate to the "Data Catalog" page.
    2.  View the list of data resources, including descriptions, links to their raw API endpoints, and links to relevant UI visualization pages.
    3.  See quick statistics like the number of hydrological stations or wetland areas loaded.

### 4.2. Interactive Map (`/view/map`)
*   **Purpose:** Visualize geospatial data. Currently, it displays hydrological station locations.
*   **How to Use:**
    1.  Navigate to the "Interactive Map" page.
    2.  An OpenStreetMap base layer will load, centered on the approximate Middle Yangtze region.
    3.  Markers representing hydrological stations (from sample data) will be displayed.
    4.  Click on a station marker to view a popup with basic information (ID, name, river, etc.).
    5.  Use standard map controls to pan and zoom.
*   **Future Enhancements:** Displaying wetland polygons, overlaying raster data, more interactive querying.

### 4.3. Data Charts (`/view/chart`)
*   **Purpose:** Visualize time-series data, such as readings from hydrological stations.
*   **How to Use:**
    1.  Navigate to the "Data Charts" page.
    2.  Use the "Select Station" dropdown to choose a hydrological station (populated from the API).
    3.  Use the "Select Parameter" dropdown (e.g., "WaterLevel", "FlowRate").
    4.  The chart will automatically update to display the time series for the selected station and parameter, based on the (sample) data in the database.
    5.  Hover over the chart to see specific data points.
*   **Future Enhancements:** Date range selection, plotting multiple parameters or stations, chart customization.

## 5. Exploring System Evolution (EKG Visualizer)

### 5.1. EKG Visualizer (`/view/ekg`)
*   **Purpose:** Visualize the Evolution Knowledge Graph (EKG), which represents entities, their states over time, significant events, and their interrelationships.
*   **How to Use:**
    1.  Navigate to the "EKG Visualizer" page.
    2.  Click the "Load/Refresh Graph Sample" button.
    3.  A sample graph (from `data/evolution_graph_data.json`) will be rendered using Vis.js.
        *   Nodes represent entities (e.g., `Wetland`), their states (`EntityState`), or temporal events (`TemporalEvent`).
        *   Edges represent relationships (e.g., `HAS_STATE`, `TRANSITIONS_TO_STATE`, `INFLUENCED_BY_EVENT`).
    4.  Hover over nodes or edges to see a tooltip with their ID, type, and properties.
    5.  Use mouse to pan, zoom, and drag nodes to explore the graph structure.
*   **Note:** The EKG backend is currently a lightweight JSON file store. Data is pre-populated for demonstration. APIs exist to add more data conceptually.

## 6. Using the Deep Research Assistant (`/assistant`)

The Research Assistant provides (currently simulated/mocked) AI-powered support.

### 6.1. Natural Language Querying (NLQ)
*   **Purpose:** Ask questions in natural language about the platform or topics covered by its RAG context (currently `README.md` and sample literature files).
*   **How to Use:**
    1.  Navigate to the "Research Assistant" page.
    2.  Type your question in the query box (e.g., "What is this platform about?", "Tell me about the EKG module.").
    3.  Click "Submit Query".
    4.  The assistant's response (generated via a simulated RAG pipeline and mocked LLM call) will appear. Debug info may show retrieved context snippets.

### 6.2. Automated Literature Summarization
*   **Purpose:** Get a brief (mocked) summary of literature related to a specific topic, based on the sample literature files processed by RAG.
*   **How to Use:**
    1.  On the "Research Assistant" page, type a query like:
        *   "summarize literature on sediment load in Yangtze River"
        *   "literature summary for wetland changes in Dongting Lake"
    2.  Submit the query.
    3.  The assistant will provide a (mocked) summary based on relevant snippets it found.

### 6.3. Data-Driven Hypothesis Generation
*   **Purpose:** Generate (mocked) plausible research hypotheses based on a textual observation you provide.
*   **How to Use:**
    1.  On the "Research Assistant" page, type a query like:
        *   "generate hypothesis for: Water level at Yichang station has increased by 10% in the last 5 years while sediment load decreased."
        *   "hypothesize about: Remote sensing analysis indicates progressive wetland shrinkage around Dongting Lake since the year 2000."
        *   You can also ask for a specific number: "generate 2 hypotheses for: [your observation]"
    2.  Submit the query.
    3.  The assistant will return one or more (mocked) hypotheses.

### 6.4. Scenario Interpretation (via Scenario Simulator)
*   **Purpose:** Get a (mocked) AI interpretation of results from the Scenario Simulator.
*   **How to Use:**
    1.  First, go to the "Scenario Simulator" page (`/view/scenario-simulator`).
    2.  Define scenario parameters and click "Run Simulation (Conceptual)".
    3.  Once the placeholder "Simulated Model Output" is displayed, click the "Interpret Results with AI (Conceptual)" button.
    4.  This will send the scenario description and output to the Research Assistant, and the interpretation will be displayed on the Scenario Simulator page.

## 7. Scenario Simulation (`/view/scenario-simulator`)

*   **Purpose:** (Conceptual) To define hypothetical scenarios, see placeholder simulated outputs, and get AI-assisted interpretations.
*   **How to Use:**
    1.  Navigate to the "Scenario Simulator" page.
    2.  Fill in the form with parameters for your scenario (e.g., change in rainfall, dam outflow).
    3.  Click "Run Simulation (Conceptual)".
        *   The "Scenario Input Summary" and "Simulated Model Output" (which is a placeholder based on simple rules) will be displayed.
    4.  Click "Interpret Results with AI (Conceptual)" to get a (mocked) textual interpretation from the Research Assistant based on the inputs and placeholder outputs.
*   **Note:** Actual model execution is not integrated in this prototype. The simulation output is a placeholder.

## 8. Troubleshooting & Support (Conceptual)

*   **Problem:** Page not loading or API errors.
    *   **Solution:** Ensure the Flask app is running. Check the terminal for error messages. Verify the PostGIS Docker container is running and accessible, and `POSTGRES_DB_URL` is correctly set.
*   **Problem:** EKG visualizer not showing graph.
    *   **Solution:** Click "Load/Refresh Graph Sample". Check browser console for JavaScript errors. Ensure `data/evolution_graph_data.json` exists and is valid JSON.
*   **Problem:** AI Assistant gives generic or unhelpful answers.
    *   **Solution:** Remember that AI features are currently simulated/mocked. The RAG context is limited to `README.md` and a few sample literature files. For best results with current mocks, frame queries related to these documents.

For further support, consult the project `README.md` or contact the development team (conceptual).

---
This user manual draft provides a basic guide. It will be expanded as the platform's features mature and real analytical capabilities are implemented.
