"""
AI Knowledge Graph Module for the Scientific Analysis Platform.

This module contains components for defining, building, and querying
the AI-enhanced System Evolution Knowledge Graph related to the
Changjiang River Basin study.
"""

# Make key classes and enums available for easier import
from .graph_schema import NodeType, RelationshipType
from .graph_builder import GraphDBConnector, KnowledgeGraphBuilder
from .graph_querier import KnowledgeGraphQuerier

__all__ = [
    "NodeType",
    "RelationshipType",
    "GraphDBConnector",
    "KnowledgeGraphBuilder",
    "KnowledgeGraphQuerier"
]

print("AI Knowledge Graph module initialized.")
