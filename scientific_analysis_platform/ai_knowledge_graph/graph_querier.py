"""
graph_querier.py

Provides classes for querying the AI-enhanced System Evolution Knowledge Graph
using the LightweightGraphStore.
"""
import os
from .graph_schema import NodeType, RelationshipType # Assuming schema is in the same directory
from .graph_builder import GraphDBConnector # Reusing the connector from graph_builder
from .lightweight_graph_store import GraphNode, GraphEdge # For type hinting
from typing import Dict, Any, List, Optional, Union

PROJECT_ROOT_EKG_QUERIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_GRAPH_DATA_PATH_QUERIER = os.path.join(PROJECT_ROOT_EKG_QUERIER, "data", "evolution_graph_data.json")


class KnowledgeGraphQuerier:
    """
    Provides methods to query and retrieve information from the knowledge graph
    via the LightweightGraphStore.
    """
    def __init__(self, connector: GraphDBConnector):
        self.connector = connector
        self.graph_store = self.connector.get_store()
        print("KnowledgeGraphQuerier initialized with LightweightGraphStore.")

    def get_node_by_id(self, node_id: str) -> Optional[GraphNode]:
        """Retrieves a single node by its ID."""
        return self.graph_store.get_node(node_id)

    def find_nodes_by_property(self, property_name: str, property_value: Any, node_type_filter: Optional[Union[NodeType, str]] = None) -> List[GraphNode]:
        """
        Finds nodes that have a specific property with a specific value.
        Optionally filters by node type.
        """
        results = []
        type_filter_str = node_type_filter.value if isinstance(node_type_filter, NodeType) else node_type_filter

        for node in self.graph_store.get_all_nodes():
            if type_filter_str and node.get("type") != type_filter_str:
                continue
            if node.get("properties", {}).get(property_name) == property_value:
                results.append(node)
        return results

    def get_neighbors_of_node(self, node_id: str, direction: str = "all", relationship_type_filter: Optional[Union[RelationshipType, str]] = None) -> List[GraphNode]:
        """
        Finds neighbor nodes of a given node, optionally filtering by relationship type.
        """
        rel_type_filter_str = relationship_type_filter.value if isinstance(relationship_type_filter, RelationshipType) else relationship_type_filter

        # This is a simplified version. LightweightGraphStore.get_neighbors itself doesn't filter by edge type.
        # So, we need to get incident edges first, filter them, then get the actual neighbor nodes.

        neighbor_nodes = []
        seen_neighbor_ids = set()

        incident_edges = self.graph_store.get_incident_edges(node_id, direction=direction)

        for edge in incident_edges:
            if rel_type_filter_str and edge.get("type") != rel_type_filter_str:
                continue

            if direction == "outgoing" or (direction == "all" and edge["source_id"] == node_id) :
                neighbor_id = edge["target_id"]
                if neighbor_id not in seen_neighbor_ids:
                    neighbor_node = self.graph_store.get_node(neighbor_id)
                    if neighbor_node:
                        neighbor_nodes.append(neighbor_node)
                        seen_neighbor_ids.add(neighbor_id)

            if direction == "incoming" or (direction == "all" and edge["target_id"] == node_id):
                neighbor_id = edge["source_id"]
                if neighbor_id not in seen_neighbor_ids: # Avoid adding if already added via outgoing (for 'all')
                    neighbor_node = self.graph_store.get_node(neighbor_id)
                    if neighbor_node:
                        neighbor_nodes.append(neighbor_node)
                        seen_neighbor_ids.add(neighbor_id)
        return neighbor_nodes

    def get_all_graph_data(self) -> Dict[str, List[Any]]:
        """Returns all nodes and edges, suitable for frontend visualization."""
        return {
            "nodes": self.graph_store.get_all_nodes(),
            "edges": self.graph_store.get_all_edges()
        }

    def get_entity_evolution_path(self, entity_node_id: str) -> List[Union[GraphNode, GraphEdge]]:
        """
        (Conceptual) Traces states or connected events for a given entity node.
        For LightweightGraphStore, this would involve graph traversal logic.
        Example: Find all ENTITY_STATE nodes linked from entity_node_id via HAS_STATE,
                 then find TRANSITIONS_TO_STATE between these states,
                 and also find TEMPORAL_EVENT nodes linked via INFLUENCED_BY_EVENT.

        This is a simplified version focusing on state transitions.
        """
        path_elements: List[Union[GraphNode, GraphEdge]] = []
        entity_node = self.graph_store.get_node(entity_node_id)
        if not entity_node:
            return []

        path_elements.append(entity_node)

        # Find initial states
        current_states: List[GraphNode] = []
        for edge in self.graph_store.get_incident_edges(entity_node_id, direction="outgoing"):
            if edge["type"] == RelationshipType.HAS_STATE.value:
                state_node = self.graph_store.get_node(edge["target_id"])
                if state_node:
                    current_states.append(state_node)
                    path_elements.append(edge)
                    path_elements.append(state_node)

        # Sort states by timestamp (assuming 'state_timestamp' in properties)
        current_states.sort(key=lambda s: s.get("properties", {}).get("state_timestamp", ""))

        # Follow TRANSITIONS_TO_STATE (this is a very basic traversal, not handling branches well)
        processed_states = set()

        # This loop structure is just one way; a proper traversal (DFS/BFS) would be better.
        # For now, let's just show the states linked to the entity and any transitions between them.

        all_states_of_entity = {s["id"]: s for s in current_states} # For quick lookup

        for state_id in list(all_states_of_entity.keys()): # Iterate over a copy if modifying inside
            if state_id in processed_states:
                continue
            # processed_states.add(state_id) # Not strictly needed for this simplified version

            for edge in self.graph_store.get_incident_edges(state_id, direction="outgoing"):
                if edge["type"] == RelationshipType.TRANSITIONS_TO_STATE.value:
                    next_state_node = self.graph_store.get_node(edge["target_id"])
                    if next_state_node and next_state_node["id"] in all_states_of_entity : # Ensure it's a state of the same entity
                        if edge not in path_elements: path_elements.append(edge)
                        # The next_state_node itself is already in path_elements if it was an initial state.
                        # If it wasn't (e.g. state only reachable via transition), add it. This logic is getting complex for simple path.
                        # For now, this simplified path primarily gets the entity and its direct states + transitions between those direct states.

            # Also find events influencing this state
            for edge in self.graph_store.get_incident_edges(state_id, direction="outgoing"): # Assuming (State)-[INFLUENCED_BY_EVENT]->(Event)
                 if edge["type"] == RelationshipType.INFLUENCED_BY_EVENT.value: # This was defined other way around in schema, let's adjust
                      event_node = self.graph_store.get_node(edge["target_id"])
                      if event_node and event_node not in path_elements : path_elements.append(event_node)
                      if edge not in path_elements: path_elements.append(edge)

            # If schema is (State) <-[INFLUENCED_BY_EVENT]- (Event), then direction="incoming"
            for edge in self.graph_store.get_incident_edges(state_id, direction="incoming"):
                 if edge["type"] == RelationshipType.INFLUENCED_BY_EVENT.value: # If (Event)-[INFLUENCED_BY_EVENT]->(State)
                      # This means my schema definition of INFLUENCED_BY_EVENT might be ambiguous or used inconsistently.
                      # Let's assume for schema: (EntityState) -[INFLUENCED_BY_EVENT {impact}]-> (TemporalEvent)
                      # This means the above outgoing check is correct.
                      pass


        # Remove duplicates while preserving order (simple way for list of dicts)
        # This is not efficient but works for small lists.
        # A better way is to add to set of IDs as processing and only add to list if ID not seen.
        final_path_elements = []
        seen_ids = set()
        for el in path_elements:
            el_id = el.get("id")
            if el_id not in seen_ids:
                final_path_elements.append(el)
                seen_ids.add(el_id)

        return final_path_elements


if __name__ == '__main__':
    print("Knowledge Graph Querier with LightweightGraphStore")

    # Ensure data directory and a test graph file exist for querier to load
    data_dir = os.path.join(PROJECT_ROOT_EKG_QUERIER, "data")
    os.makedirs(data_dir, exist_ok=True)
    test_graph_file_querier = os.path.join(data_dir, "querier_test_graph.json")

    # Create a dummy graph file for testing the querier
    # (Normally this would be created by the builder)
    sample_graph_data = {
        "nodes": [
            {"id": "W01", "type": "Wetland", "properties": {"name": "Dongting Lake"}},
            {"id": "S_W01_2000", "type": "EntityState", "properties": {"entity_ref_id": "W01", "state_timestamp": "2000-01-01", "state_data_json": {"area": 500}}},
            {"id": "S_W01_2005", "type": "EntityState", "properties": {"entity_ref_id": "W01", "state_timestamp": "2005-01-01", "state_data_json": {"area": 450}}},
            {"id": "EVT_Flood02", "type": "TemporalEvent", "properties": {"event_type": "Flood", "year": 2002}}
        ],
        "edges": [
            {"id": "e_ws1", "source_id": "W01", "target_id": "S_W01_2000", "type": "HAS_STATE", "properties": {}},
            {"id": "e_ws2", "source_id": "W01", "target_id": "S_W01_2005", "type": "HAS_STATE", "properties": {}},
            {"id": "e_s1s2", "source_id": "S_W01_2000", "target_id": "S_W01_2005", "type": "TRANSITIONS_TO_STATE", "properties": {"reason": "Drought"}},
            {"id": "e_s2evt", "source_id": "S_W01_2005", "target_id": "EVT_Flood02", "type": "INFLUENCED_BY_EVENT", "properties": {"impact": "Area slightly recovered"}}
        ]
    }
    import json
    with open(test_graph_file_querier, 'w') as f:
        json.dump(sample_graph_data, f, indent=2)

    print(f"\n--- Querier Example using Lightweight Store (File: {test_graph_file_querier}) ---")
    connector = None
    try:
        connector = GraphDBConnector(graph_store_filepath=test_graph_file_querier)
        querier = KnowledgeGraphQuerier(connector)

        print("\n1. Get Node by ID:")
        node = querier.get_node_by_id("S_W01_2000")
        print(f"  Node S_W01_2000: {node}")

        print("\n2. Find Nodes by Property:")
        wetlands = querier.find_nodes_by_property("name", "Dongting Lake", node_type_filter=NodeType.WETLAND)
        print(f"  Wetlands named 'Dongting Lake': {wetlands}")

        flood_events = querier.find_nodes_by_property("year", 2002, node_type_filter="TemporalEvent") # Using string for type
        print(f"  Flood events in 2002: {flood_events}")


        print("\n3. Get Neighbors of Node:")
        neighbors_of_s_w01_2000 = querier.get_neighbors_of_node("S_W01_2000", direction="all")
        print(f"  Neighbors of S_W01_2000 (all): {neighbors_of_s_w01_2000}")

        # Filter neighbors by relationship type
        source_of_s_w01_2000_via_has_state = querier.get_neighbors_of_node("S_W01_2000", direction="incoming", relationship_type_filter=RelationshipType.HAS_STATE)
        print(f"  Source of S_W01_2000 via HAS_STATE: {source_of_s_w01_2000_via_has_state}")


        print("\n4. Get All Graph Data (for visualization):")
        all_data = querier.get_all_graph_data()
        print(f"  Total nodes: {len(all_data['nodes'])}, Total edges: {len(all_data['edges'])}")
        # print(f"  Sample node: {all_data['nodes'][0] if all_data['nodes'] else 'None'}")
        # print(f"  Sample edge: {all_data['edges'][0] if all_data['edges'] else 'None'}")

        print("\n5. Get Entity Evolution Path (Conceptual):")
        evolution_path_w01 = querier.get_entity_evolution_path("W01")
        print(f"  Evolution path for W01 (length {len(evolution_path_w01)}):")
        for elem in evolution_path_w01:
            print(f"    - ID: {elem['id']}, Type: {elem['type']}")


    except Exception as e:
        print(f"An error occurred in the querier example: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if connector: # Connector doesn't have a close that saves for querier, builder does.
            pass
        if os.path.exists(test_graph_file_querier):
            os.remove(test_graph_file_querier) # Clean up test file
        print("\nQuerier example finished.")
