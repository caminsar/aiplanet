# Agent Instructions for Scientific Analysis Platform Development

This document provides guidelines and instructions for AI agents contributing to the `Scientific Analysis Platform` project.

## Project Overview

The platform aims to support research on the Changjiang River Basin by integrating data management, model execution, visualization, a knowledge graph, and a research assistant. Familiarize yourself with the project goals and module structure outlined in `README.md`.

## General Guidelines

1.  **Understand the Plan**: Always refer to the current development plan and the specific step you are working on. Ask for clarification if the plan is ambiguous.
2.  **Modular Design**: Strive to maintain a modular design. Components within a module should be cohesive, and coupling between modules should be loose. Use Flask Blueprints for organizing routes for different features.
3.  **Code Comments and Docstrings**:
    *   Write clear and concise comments for complex logic.
    *   Add Python docstrings to all modules, classes, and functions, explaining their purpose, arguments, and return values. Use a consistent docstring format (e.g., Google style, reStructuredText).
4.  **Placeholder Usage & Conceptual Components**:
    *   When implementing skeleton frameworks, interfaces, or conceptual components (like the initial RAG pipeline or model wrappers), clearly mark placeholders (e.g., using `# TODO:`, `NotImplementedError`, or descriptive comments like `# Placeholder for actual database interaction`, `# Simulated LLM call`).
    *   Ensure docstrings and comments explicitly state when a component is a conceptual placeholder or uses simulated/mocked behavior, and briefly outline what a real implementation would entail.
5.  **Error Handling**: Implement basic error handling (e.g., `try-except` blocks) where appropriate, especially for I/O operations, API calls, or database interactions. Log errors or provide informative messages.
6.  **Dependencies**: If new dependencies are added, ensure they are justifiable and add them to `requirements.txt` with appropriate version pinning (e.g., `library>=1.0,<2.0`).
7.  **Testing**: While full test development might be a separate step, keep testability in mind. Think about how your code could be tested. (Future: Specific testing guidelines will be added).
8.  **Security**: Be mindful of security best practices, especially for web application components. For now, primary focus is on functionality.
9.  **Configuration**: Use environment variables for sensitive or environment-specific configurations (e.g., `POSTGRES_DB_URL`, API keys). Refer to `docker-compose.yml` and `README.md` for examples.

## Module-Specific Notes

*   **`app.py` (Flask Application)**:
    *   Organize routes into Blueprints (e.g., `data_api_bp`, `visualization_bp`).
    *   Use an app factory pattern (`create_app`) for better structure.
*   **`data_management/`**:
    *   Database models are defined in `models.py` using SQLAlchemy and GeoAlchemy2 for PostGIS.
    *   API routes for data are in `api_routes.py`.
    *   Importers in `importers/` should be robust enough for sample data and extendable.
    *   Modules like `spatial_analysis.py` and `data_fusion.py` are currently conceptual; their further development should focus on integrating established Python libraries (SciPy, GeoPandas, etc.).
*   **`model_integration/`**:
    *   The `ScientificModel` interface in `model_interface.py` is key.
    *   Wrappers in `models/` (e.g., `MaxEntModelWrapper`, `SWATModelWrapper`) are conceptual. Future work should detail how they would interact with actual model executables or libraries.
*   **`visualization/`**:
    *   Templates should be clean and use client-side JavaScript for interactivity (e.g., Leaflet, Chart.js).
    *   UI-supporting API endpoints can be part of the visualization Blueprint if they are solely for that UI component's needs (e.g., populating a dropdown).
*   **`ai_knowledge_graph/`**:
    *   Currently a conceptual skeleton. Development will require choosing a graph database technology and query language.
*   **`research_assistant/`**:
    *   `assistant_core.py` orchestrates the RAG pipeline.
    *   Components like `EmbeddingService`, `VectorStore`, and LLM interactions in `assistant_core.py` are currently **simulated/mocked**. Future tasks will involve replacing these with real implementations (e.g., using `sentence-transformers`, FAISS/pgvector, and an actual LLM API like OpenAI). Clearly document which parts are simulated.
    *   Refer to `AI_ENGINE_STRATEGY.md` for the planned approach.

## Python Style and Conventions

*   Follow PEP 8 style guidelines for Python code.
*   Use meaningful variable and function names.
*   Aim for readability and maintainability.

## Communication

*   If you encounter persistent issues, clearly communicate the problem and the steps taken.
*   When a plan step is completed, provide a concise summary of the actions taken.
*   If you need to deviate significantly from an approved plan, request user input.

---
*These instructions are subject to updates as the project evolves.*
