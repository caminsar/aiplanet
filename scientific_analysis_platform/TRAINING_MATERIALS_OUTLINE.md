# Training Materials Outline - Scientific Analysis Platform

This document outlines the structure and content for training materials designed to help users effectively utilize the Scientific Analysis Platform. Materials could take the form of presentations, written guides, video tutorials, or interactive workshops.

---

**Target Audience:** Researchers, students, and data analysts in environmental science, hydrology, ecology, and related fields focusing on river basin studies, particularly the Yangtze River.

**Overall Goal of Training:** Enable users to independently use the platform for their research tasks, from data exploration to (conceptual) advanced analysis and knowledge discovery.

---

## Module 1: Introduction to the Scientific Analysis Platform

*   **1.1. Welcome and Overview**
    *   Purpose and vision of the platform.
    *   Key benefits for researchers studying complex river systems.
    *   High-level architecture and core modules (Data Management, Model Integration, Visualization, EKG, Research Assistant).
*   **1.2. Getting Started**
    *   Accessing the platform (URL, login - if applicable).
    *   Quick tour of the main user interface and navigation.
    *   Reference to `README.md` and `USER_MANUAL.md` for setup and detailed guidance.
*   **1.3. Core Concepts**
    *   Spatio-temporal data in the context of the platform.
    *   Introduction to the Evolution Knowledge Graph (EKG) concept.
    *   Overview of AI-assisted features and their (current simulated) capabilities.

## Module 2: Data Exploration and Management

*   **2.1. The Data Catalog**
    *   Navigating the catalog (`/view/catalog`).
    *   Understanding listed data types, descriptions, and API links.
    *   How to identify relevant datasets for a research question.
*   **2.2. Using the Interactive Map (`/view/map`)**
    *   Viewing station locations and basic information.
    *   Map navigation (pan, zoom).
    *   (Future: Adding layers, querying features).
*   **2.3. Working with Data Charts (`/view/chart`)**
    *   Selecting stations and parameters.
    *   Interpreting time-series visualizations.
    *   (Future: Customizing charts, exporting data/images).
*   **2.4. Accessing Data via APIs (For Advanced Users)**
    *   Brief overview of the Data APIs (`/api/data/*`).
    *   Example API calls using tools like `curl` or Postman (or Python `requests`).
    *   Understanding JSON and GeoJSON responses.
*   **2.5. (Conceptual) Data Import and Standardization**
    *   Briefly touch upon the `DATA_STANDARDIZATION_GUIDE.md`.
    *   Overview of how new data (conceptually) gets into the platform.

## Module 3: Exploring System Evolution with the EKG

*   **3.1. Introduction to the Evolution Knowledge Graph (EKG)**
    *   What it represents: entities, states, events, relationships over time.
    *   Key node and relationship types (from `graph_schema.py`).
*   **3.2. Using the EKG Visualizer (`/view/ekg`)**
    *   Loading and navigating the sample graph.
    *   Understanding node/edge representations and tooltips.
    *   Identifying entities, their states, and associated events.
    *   Tracing simple evolutionary paths visually (conceptual).
*   **3.3. Querying the EKG via APIs (For Advanced Users/Developers)**
    *   Overview of EKG APIs (`/api/ekg/*`).
    *   Examples of querying nodes, edges, and (conceptual) evolution paths.
*   **3.4. (Conceptual) Contributing to the EKG**
    *   How new events, states, or relationships might be added (via APIs).

## Module 4: Leveraging the AI Deep Research Assistant (`/assistant`)

*   **4.1. Introduction to the AI Assistant**
    *   Capabilities: NLQ, literature summary, hypothesis generation, scenario interpretation.
    *   Understanding its current RAG-based (simulated) functionality and knowledge sources (README, sample literature).
*   **4.2. Natural Language Querying (NLQ)**
    *   Formulating effective questions.
    *   Examples: "What is this platform?", "Tell me about EKG data."
    *   Interpreting responses, confidence scores, and debug information.
*   **4.3. Automated Literature Summarization**
    *   How to request summaries (e.g., "summarize literature on [topic]").
    *   Understanding the (simulated) output based on provided sample texts.
    *   Limitations of the current prototype.
*   **4.4. Data-Driven Hypothesis Generation**
    *   Providing clear textual observations.
    *   Example queries: "generate hypothesis for: [observation]".
    *   Interpreting the (mocked) generated hypotheses as starting points.
*   **4.5. AI-Assisted Scenario Interpretation**
    *   Using the Scenario Simulator UI (`/view/scenario-simulator`).
    *   How the "Interpret Results with AI" button works (conceptually).
    *   Understanding the (mocked) AI interpretation of placeholder simulation outputs.

## Module 5: (Conceptual) Scenario Simulation and Model Integration

*   **5.1. Using the Scenario Simulator UI (`/view/scenario-simulator`)**
    *   Defining scenario parameters.
    *   Understanding the placeholder "Simulated Model Output."
    *   (Reiteration) Using AI for interpretation.
*   **5.2. Overview of Integrated Models (Conceptual)**
    *   Brief introduction to MaxEnt, SWAT, VIC and their purpose.
    *   How they are (conceptually) wrapped and managed by `ModelManager`.
    *   (Future: How to configure and run these models via the platform).

## Module 6: Dongting Lake Case Study Application

*   **6.1. Revisiting the Case Study (`CASE_STUDY_DONGTING_LAKE.md`)**
*   **6.2. Hands-on Walkthrough (Guided Exercise)**
    *   Step-by-step execution of the tasks outlined in `DONGTING_CASE_STUDY_WALKTHROUGH.md`.
    *   Encourage users to try variations of queries and explore different features.
*   **6.3. Discussion and Q&A**

## Module 7: Summary and Future Directions

*   **7.1. Recap of Platform Capabilities.**
*   **7.2. Current Limitations and Known Issues (of the prototype).**
*   **7.3. Roadmap for Future Development.**
*   **7.4. How to Get Help and Provide Feedback.**

---

**Delivery Format Ideas:**
*   Series of short video tutorials for each module/feature.
*   Interactive Jupyter Notebooks for API usage examples.
*   Live webinar/workshop sessions.
*   A comprehensive written guide (expanded from `USER_MANUAL_DRAFT.md`).

**Prerequisites for Attendees/Users:**
*   Basic understanding of environmental science concepts.
*   Familiarity with web browser usage.
*   (For advanced API usage) Basic understanding of REST APIs and JSON.
