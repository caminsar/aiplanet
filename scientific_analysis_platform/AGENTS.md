# Agent Instructions for Scientific Analysis Platform Development

This document provides guidelines and instructions for AI agents contributing to the `Scientific Analysis Platform` project.

## Project Overview

The platform aims to support research on the Changjiang River Basin by integrating data management, model execution, visualization, a knowledge graph, and a research assistant. Familiarize yourself with the project goals and module structure outlined in `README.md`.

## General Guidelines

1.  **Understand the Plan**: Always refer to the current development plan and the specific step you are working on. Ask for clarification if the plan is ambiguous.
2.  **Modular Design**: Strive to maintain a modular design. Components within a module should be cohesive, and coupling between modules should be loose.
3.  **Code Comments and Docstrings**:
    *   Write clear and concise comments for complex logic.
    *   Add Python docstrings to all modules, classes, and functions, explaining their purpose, arguments, and return values. Use a consistent docstring format (e.g., Google style, reStructuredText).
4.  **Placeholder Usage**: When implementing skeleton frameworks or interfaces, clearly mark placeholders (e.g., using `# TODO:`, `NotImplementedError`, or descriptive comments like `# Placeholder for actual database interaction`).
5.  **Error Handling**: Implement basic error handling (e.g., `try-except` blocks) where appropriate, especially for I/O operations, API calls, or database interactions. Log errors or provide informative messages.
6.  **Dependencies**: If new dependencies are added, ensure they are justifiable and mention them for inclusion in `requirements.txt`.
7.  **Testing**: While full test development might be a separate step, keep testability in mind. Think about how your code could be tested. (Future: Specific testing guidelines will be added).
8.  **Security**: Be mindful of security best practices, especially for web application components (e.g., input validation to prevent injection attacks if handling user input directly). For now, primary focus is on functionality.

## Module-Specific Notes

*   **`app.py` (Flask Application)**:
    *   When adding new routes, consider organizing them into Blueprints if the number of routes grows significantly.
    *   Ensure template and static file paths are correctly configured.
*   **`data_management/`**:
    *   Database interactions (even simulated) should be encapsulated. The `DataRecord` model in `models.py` is central.
    *   `data_handlers.py` defines interfaces; future concrete implementations should handle specific file formats or database types.
*   **`model_integration/`**:
    *   The `ScientificModel` interface in `model_interface.py` is key. New models must implement this interface.
    *   `ModelManager` should handle the lifecycle (registration, setup, run, cleanup).
*   **`visualization/`**:
    *   Templates should be clean and well-structured.
    *   Static files (CSS, JS) should be organized. Aim for a consistent UI/UX.
*   **`ai_knowledge_graph/`**:
    *   The `graph_schema.py` is conceptual. Actual graph DB queries (e.g., Cypher for Neo4j) will be needed in `graph_builder.py` and `graph_querier.py`. Clearly mark where specific DB query language is needed.
    *   Simulated DB interactions are acceptable for now but should be clearly noted.
*   **`research_assistant/`**:
    *   `assistant_core.py` is the brain. Initial logic is rule-based; future work will involve NLP and LLM integration. Design for extensibility.

## Python Style and Conventions

*   Follow PEP 8 style guidelines for Python code.
*   Use meaningful variable and function names.
*   Aim for readability and maintainability.

## Communication

*   If you encounter persistent issues (like the initial Git sandbox problem), clearly communicate the problem and the steps taken.
*   When a plan step is completed, provide a concise summary of the actions taken.
*   If you need to deviate significantly from an approved plan, request user input.

---
*These instructions are subject to updates as the project evolves.*
