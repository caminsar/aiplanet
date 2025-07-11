"""
graph_builder.py

Provides classes for constructing the AI-enhanced System Evolution Knowledge Graph.
This version uses the LightweightGraphStore for data persistence.
"""
import os
from .graph_schema import NodeType, RelationshipType # Assuming schema is in the same directory
from .lightweight_graph_store import LightweightGraphStore, GraphNode, GraphEdge # Import the new store
from typing import Dict, Any, Optional, Union
import uuid # For generating unique IDs if not provided

# Path to the project root to locate the data directory
PROJECT_ROOT_EKG_BUILDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_GRAPH_DATA_PATH = os.path.join(PROJECT_ROOT_EKG_BUILDER, "data", "evolution_graph_data.json")


class GraphDBConnector:
    """
    Connector class that now interfaces with LightweightGraphStore.
    The concept of URI, user, password is less relevant here but kept for potential future
    switch to a real graph DB with minimal interface changes.
    """
    def __init__(self, graph_store_filepath: str = DEFAULT_GRAPH_DATA_PATH):
        """
        Initializes the connector with a LightweightGraphStore.
        :param graph_store_filepath: Path to the JSON file for the graph store.
        """
        self.filepath = graph_store_filepath
        self.graph_store = LightweightGraphStore(filepath=self.filepath)
        # _driver attribute can now represent the store itself for compatibility with old logic if any
        self._driver = self.graph_store
        print(f"GraphDBConnector initialized with LightweightGraphStore using file: {self.filepath}")

    def connect(self):
        """For LightweightGraphStore, connection is implicit on init (file load)."""
        print("LightweightGraphStore is file-based; 'connection' established on initialization.")
        if not self._driver: # Should not happen if __init__ is correct
            self.graph_store = LightweightGraphStore(filepath=self.filepath)
            self._driver = self.graph_store
        return True

    def close(self):
        """Saves the graph data to file on close."""
        print("Closing GraphDBConnector: saving graph data...")
        if self.graph_store:
            self.graph_store.save_to_json()
        self._driver = None # Clear the reference
        print("Graph data saved.")

    def get_store(self) -> LightweightGraphStore:
        """Provides direct access to the graph store instance."""
        if not self._driver:
            self.connect() # Re-initialize if closed
        return self.graph_store


class KnowledgeGraphBuilder:
    """
    Provides methods to add and update elements in the knowledge graph
    using the LightweightGraphStore.
    """
    def __init__(self, connector: GraphDBConnector):
        self.connector = connector
        self.graph_store = self.connector.get_store() # Get the actual store instance
        print("KnowledgeGraphBuilder initialized with LightweightGraphStore.")

    def add_node(self, node_id: str, node_type: Union[NodeType, str], properties: Optional[Dict[str, Any]] = None) -> Optional[GraphNode]:
        """
        Adds or updates a node in the graph.

        :param node_id: Unique ID for the node.
        :param node_type: The type of the node (from graph_schema.NodeType or as string).
        :param properties: A dictionary of node properties.
        :return: The added or updated node dictionary, or None on failure.
        """
        type_str = node_type.value if isinstance(node_type, NodeType) else str(node_type)
        return self.graph_store.add_node(node_id, type_str, properties)

    def add_relationship(self,
                         edge_id: str,
                         from_node_id: str,
                         to_node_id: str,
                         relationship_type: Union[RelationshipType, str],
                         rel_properties: Optional[Dict[str, Any]] = None) -> Optional[GraphEdge]:
        """
        Adds or updates a relationship (edge) between two existing nodes.

        :param edge_id: Unique ID for the edge. If None, a UUID will be generated.
        :param from_node_id: ID of the source node.
        :param to_node_id: ID of the target node.
        :param relationship_type: The type of relationship (from graph_schema.RelationshipType or as string).
        :param rel_properties: Optional properties for the relationship itself.
        :return: The added or updated edge dictionary, or None on failure.
        """
        type_str = relationship_type.value if isinstance(relationship_type, RelationshipType) else str(relationship_type)

        # Auto-generate edge_id if not provided or empty
        current_edge_id = edge_id if edge_id else str(uuid.uuid4())

        return self.graph_store.add_edge(current_edge_id, from_node_id, to_node_id, type_str, rel_properties)

    def save_graph(self):
        """Persists the graph to its file."""
        self.graph_store.save_to_json()


if __name__ == '__main__':
    print("Knowledge Graph Builder with LightweightGraphStore")

    # Ensure the data directory exists for the default JSON file path
    data_dir = os.path.join(PROJECT_ROOT_EKG_BUILDER, "data")
    os.makedirs(data_dir, exist_ok=True)
    test_graph_file = os.path.join(data_dir, "builder_test_graph.json")
    if os.path.exists(test_graph_file): os.remove(test_graph_file)


    print(f"\n--- Builder Example using Lightweight Store (File: {test_graph_file}) ---")
    connector = None # Define in outer scope for finally block
    try:
        connector = GraphDBConnector(graph_store_filepath=test_graph_file)
        builder = KnowledgeGraphBuilder(connector)

        # Add some nodes
        builder.add_node("station_YIC", NodeType.HYDROLOGICAL_STATION, {"name": "Yichang Station", "river": "Yangtze"})
        builder.add_node("event_Flood98", NodeType.TEMPORAL_EVENT, {"event_type": "MajorFlood", "year": 1998, "description": "1998 Yangtze Flood"})
        builder.add_node("state_YIC_preFlood", NodeType.ENTITY_STATE, {"entity_ref_id": "station_YIC", "state_timestamp": "1998-06-01", "data_json": {"status": "normal"}})
        builder.add_node("state_YIC_postFlood", NodeType.ENTITY_STATE, {"entity_ref_id": "station_YIC", "state_timestamp": "1998-09-01", "data_json": {"status": "affected", "damage_level": 3}})

        print("\nNodes after adding:")
        for node_id in ["station_YIC", "event_Flood98", "state_YIC_preFlood", "state_YIC_postFlood"]:
             print(builder.graph_store.get_node(node_id))

        # Add relationships
        edge1_id = str(uuid.uuid4()) # Example of generating ID if needed by API layer
        builder.add_relationship(edge1_id, "station_YIC", "state_YIC_preFlood", RelationshipType.HAS_STATE)

        builder.add_relationship(str(uuid.uuid4()), "station_YIC", "state_YIC_postFlood", RelationshipType.HAS_STATE)

        builder.add_relationship(str(uuid.uuid4()),
                                 "state_YIC_preFlood", "state_YIC_postFlood",
                                 RelationshipType.TRANSITIONS_TO_STATE,
                                 {"trigger_event_ref_id": "event_Flood98"})

        builder.add_relationship(str(uuid.uuid4()),
                                 "state_YIC_postFlood", "event_Flood98",
                                 RelationshipType.INFLUENCED_BY_EVENT,
                                 {"impact_description": "Station operations disrupted."})

        print("\nEdges after adding:")
        for edge in builder.graph_store.get_all_edges():
            print(edge)

        # The graph is saved when the connector is closed (or explicitly via builder.save_graph())
        # builder.save_graph() # Explicit save

    except Exception as e:
        print(f"An error occurred in the builder example: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if connector:
            connector.close() # This will save the graph
        if os.path.exists(test_graph_file):
            print(f"\nTest graph saved to {test_graph_file}. Please inspect or remove it.")
            # os.remove(test_graph_file) # Optionally clean up test file

        print("\nBuilder example finished.")
