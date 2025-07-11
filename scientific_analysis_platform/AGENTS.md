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
    *   When implementing skeleton frameworks, interfaces, or conceptual components (like the RAG pipeline, model wrappers, EKG features), clearly mark placeholders (e.g., using `# TODO:`, `NotImplementedError`, or descriptive comments like `# Placeholder for actual database interaction`, `# Simulated LLM call`).
    *   Ensure docstrings and comments explicitly state when a component is a conceptual placeholder or uses simulated/mocked behavior, and briefly outline what a real implementation would entail. This is crucial for AI-driven features.
5.  **Error Handling**: Implement basic error handling (e.g., `try-except` blocks) where appropriate, especially for I/O operations, API calls, or database interactions. Log errors or provide informative messages.
6.  **Dependencies**: If new dependencies are added, ensure they are justifiable and add them to `requirements.txt` with appropriate version pinning (e.g., `library>=1.0,<2.0`). Note any client-side library CDNs in relevant HTML files.
7.  **Testing**: While full test development might be a separate step, keep testability in mind. Think about how your code could be tested. (Future: Specific testing guidelines will be added).
8.  **Security**: Be mindful of security best practices, especially for web application components. For now, primary focus is on functionality.
9.  **Configuration**: Use environment variables for sensitive or environment-specific configurations (e.g., `POSTGRES_DB_URL`, API keys). Refer to `docker-compose.yml` and `README.md` for examples. Data file paths (like for EKG JSON) should be configurable or clearly documented.

## Module-Specific Notes

*   **`app.py` (Flask Application)**:
    *   Organize routes into Blueprints. The app factory pattern (`create_app`) is used.
    *   Ensure creation of necessary directories (like `data/` for EKG JSON) on startup if they might not exist.
*   **`data_management/`**:
    *   Database models in `models.py` use SQLAlchemy/GeoAlchemy2 for PostGIS.
    *   `spatial_analysis.py` and `data_fusion.py` remain conceptual.
*   **`model_integration/`**:
    *   Wrappers in `models/` are conceptual.
*   **`visualization/`**:
    *   Templates use client-side JavaScript (Leaflet, Chart.js, Vis.js). Ensure CDNs are correctly linked or local static assets are properly served.
    *   UI-supporting APIs within the visualization blueprint should be minimal and clearly justified.
*   **`ai_knowledge_graph/`**:
    *   The EKG is now implemented with a `LightweightGraphStore` using JSON file persistence (e.g., `data/evolution_graph_data.json`). This is a basic implementation; future work might involve a proper graph database.
    *   `graph_schema.py` has been extended for evolutionary aspects.
    *   APIs in `api_routes_ekg.py` interact with this lightweight store.
*   **`research_assistant/`**:
    *   Core RAG components (`EmbeddingService`, `VectorStore`) and LLM interactions in `assistant_core.py` (including literature summary, hypothesis generation, scenario interpretation) are **heavily simulated/mocked**.
    *   Future development must focus on replacing these mocks with real model/API calls.
    *   The `AI_ENGINE_STRATEGY.md` document outlines the intended path for real implementations.

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
