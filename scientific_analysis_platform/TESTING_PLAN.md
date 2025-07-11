# Scientific Analysis Platform - Testing Plan

## 1. Introduction

This document outlines the testing strategy for the Scientific Analysis Platform. The goal is to ensure the platform's reliability, functionality, usability, and performance (conceptually for some aspects given sandbox limitations). This plan covers various types of testing, tools, environments, and key areas of focus.

## 2. Scope of Testing

Testing will cover the following major components and functionalities:

*   **Data Management Module:**
    *   Database schema integrity (PostGIS).
    *   Data import scripts (sample data).
    *   Backend APIs for data querying (`/api/data/*`).
*   **Model Integration Module:**
    *   Model registration and management (`ModelManager`).
    *   Conceptual model wrapper execution (simulated runs of MaxEnt, SWAT, VIC).
*   **Visualization Module:**
    *   Frontend display of maps (Leaflet), charts (Chart.js), and EKG (Vis.js).
    *   Interaction with backend APIs to fetch data for visualization.
    *   User interface for Data Catalog, EKG visualizer, Scenario Simulator.
*   **AI Knowledge Graph (EKG) Module:**
    *   Lightweight graph store (JSON persistence via `LightweightGraphStore`).
    *   Backend APIs for EKG node/edge manipulation and querying (`/api/ekg/*`).
*   **Research Assistant Module:**
    *   Keyword-based responses.
    *   RAG pipeline (simulated embeddings, vector store, LLM calls).
    *   Literature summarization (simulated).
    *   Hypothesis generation (simulated).
    *   Scenario interpretation (simulated).
    *   Backend API for assistant queries (`/api/assistant/*`).
*   **Application Core:**
    *   Flask application setup, routing, Blueprints.
    *   Docker deployment (`docker-compose.yml`, `Dockerfile`).

## 3. Types of Testing

### 3.1. Unit Testing
*   **Objective:** Verify individual components (functions, classes, methods) work as expected in isolation.
*   **Scope:** Focus on backend Python code.
    *   Critical functions in data importers (e.g., CSV parsing, geometry creation).
    *   Logic within `LightweightGraphStore` (add/get nodes/edges, save/load JSON).
    *   Core helper functions in `assistant_core.py` (e.g., query parsing, if separated).
    *   API endpoint logic (request parsing, response formatting - can be part of integration tests too).
*   **Tools (Conceptual):** Python's `unittest` or `pytest` framework.
*   **Execution:** Primarily automated, run frequently during development.

### 3.2. Integration Testing
*   **Objective:** Verify interactions between different components or modules.
*   **Scope:**
    *   API endpoints interacting with the database (PostGIS via SQLAlchemy, EKG via `LightweightGraphStore`).
    *   Frontend components fetching data from backend APIs.
    *   Research Assistant core logic calling its sub-modules (document processor, embedding service, vector store - all simulated).
    *   Data importers writing to the database.
*   **Tools (Conceptual):** `pytest` with Flask test client, `requests` library for API testing. Manual testing for initial phases.
*   **Execution:** Automated where possible, run after unit tests pass.

### 3.3. End-to-End (E2E) / User Acceptance Testing (UAT)
*   **Objective:** Validate complete workflows from a user's perspective to ensure the platform meets requirements.
*   **Scope:** Key user scenarios:
    1.  Setting up the platform (Docker, DB init, data import).
    2.  Accessing the Data Catalog and understanding available data.
    3.  Visualizing station data on the map.
    4.  Visualizing time series data on charts.
    5.  Interacting with the EKG visualizer (loading sample graph).
    6.  Querying the Research Assistant (simple NLQ, literature summary, hypothesis generation, scenario interpretation).
    7.  Using the Scenario Simulator UI.
*   **Tools (Conceptual):** Manual walkthroughs based on test cases. For automation: Selenium, Cypress, or Playwright (beyond current sandbox capabilities).
*   **Execution:** Primarily manual for this project phase, based on UAT scenarios derived from the `DONGTING_CASE_STUDY_WALKTHROUGH.md`.

### 3.4. Performance Testing (Conceptual)
*   **Objective:** Evaluate platform responsiveness and resource usage under expected load (conceptual).
*   **Scope (Conceptual KPIs):**
    *   API response times for key data queries (e.g., `/api/data/stations`, `/api/ekg/graph_sample`).
    *   Page load times for main visualization pages.
    *   Data import script execution time for sample datasets.
    *   EKG query speed for `LightweightGraphStore` (for a defined sample graph size).
*   **Tools (Conceptual):** Load testing tools (e.g., Locust, JMeter) for APIs. Browser developer tools for frontend. Python `cProfile` for backend script profiling.
*   **Execution:** Conceptual for this phase; focus on identifying bottlenecks through observation and code review. Real performance testing requires a dedicated environment.

### 3.5. Usability Testing (Informal)
*   **Objective:** Assess ease of use and intuitiveness of the UI.
*   **Scope:** Navigation, clarity of information, form inputs, visualization interactions.
*   **Execution:** Informal review during development and UAT walkthroughs.

## 4. Test Environment

*   **Local Development:** Developers' machines with Python, Docker Desktop, PostGIS (via Docker), and necessary environment variables set. This is the primary environment for unit and most integration tests.
*   **Staging Environment (Conceptual):** A shared environment mimicking production more closely. Would be used for UAT and performance tests.
*   **Production Environment (Conceptual):** The live deployed platform.

For this project phase, testing will primarily occur in the local development environment.

## 5. Test Execution and Reporting

*   **Unit Tests:** Stored in `tests/` subdirectories within relevant modules. Run using `python -m unittest discover -s module_path/tests`.
*   **Integration Tests:** (Conceptual) Could be part of the `tests/` structure or run as separate scripts.
*   **UAT Scenarios:** Documented in `DONGTING_CASE_STUDY_WALKTHROUGH.md` and potentially a separate UAT checklist.
*   **Bug Tracking (Conceptual):** Use GitHub Issues for tracking identified bugs, improvements, and test failures.
*   **Test Summary Report (Conceptual):** A brief summary of test activities, pass/fail rates for automated tests, and major issues found from UAT would be created at the end of a testing cycle.

## 6. Key Areas of Focus for Testing

*   **Data Integrity:** Correctness of data imported and retrieved from PostGIS and EKG store.
*   **API Functionality:** All API endpoints work as specified (request/response formats, status codes, error handling).
*   **Frontend-Backend Integration:** Data fetched from APIs is correctly displayed in visualizations. User inputs are correctly sent to APIs.
*   **Research Assistant Logic:** Keyword triggers work. (Simulated) RAG pipeline fetches context and (mocked) LLM calls produce expected types of responses.
*   **EKG Functionality:** Node/edge creation via API, persistence in JSON, and sample graph loading in the visualizer.
*   **Setup and Deployment:** `README.md` instructions for setting up the environment and running the application are accurate and lead to a working instance. Docker setup is functional.

## 7. Test Data Management

*   Sample datasets in `sample_data/` will be used for initial data import testing.
*   Specific small test files (e.g., minimal CSVs, JSON snippets) can be created within `tests/fixtures/` for unit tests.
*   The EKG JSON file (`data/evolution_graph_data.json`) will be pre-populated with a small graph for EKG API and visualizer testing.

This testing plan provides a framework. Specific test cases will be derived from requirements, user stories (implicit in the feature requests), and the case study walkthrough.
