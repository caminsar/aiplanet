"""
lightweight_graph_store.py

Provides a simple file-based (JSON) storage and retrieval mechanism
for graph data (nodes and edges). This serves as a lightweight alternative
to a full graph database for early-stage EKG development.
"""
import json
import os
from typing import List, Dict, Any, Optional, Union

# Define a type alias for Node and Edge for clarity
GraphNode = Dict[str, Any] # Expected keys: "id", "type" (NodeType as str), "properties" (dict)
GraphEdge = Dict[str, Any] # Expected keys: "id", "source_id", "target_id", "type" (RelationshipType as str), "properties" (dict)

class LightweightGraphStore:
    """
    Manages graph data (nodes and edges) stored in lists and persisted to a JSON file.
    """
    def __init__(self, filepath: str = "evolution_graph_data.json"):
        """
        Initializes the graph store.

        :param filepath: Path to the JSON file where graph data will be stored.
                         If the file exists, data will be loaded from it.
        """
        self.filepath = filepath
        self.nodes: Dict[str, GraphNode] = {} # Store nodes by ID for quick lookup
        self.edges: Dict[str, GraphEdge] = {} # Store edges by ID for quick lookup
        # For relationships involving a node, we might need to build indexes on the fly or store them separately
        self.adj: Dict[str, Dict[str, List[str]]] = {"out": {}, "in": {}} # Adjacency list: node_id -> {"out": [edge_ids], "in": [edge_ids]}

        self._load_from_json()
        print(f"[LightweightGraphStore INFO] Initialized. Loaded {len(self.nodes)} nodes and {len(self.edges)} edges from {self.filepath}")

    def _rebuild_adj(self):
        """Rebuilds the adjacency list from the current edges."""
        self.adj = {"out": {}, "in": {}}
        for edge_id, edge in self.edges.items():
            source_id = edge.get("source_id")
            target_id = edge.get("target_id")
            if source_id:
                self.adj["out"].setdefault(source_id, []).append(edge_id)
            if target_id:
                self.adj["in"].setdefault(target_id, []).append(edge_id)

    def add_node(self, node_id: str, node_type: str, properties: Optional[Dict[str, Any]] = None) -> Optional[GraphNode]:
        """Adds a node to the graph. If node_id exists, it updates properties."""
        if not node_id or not node_type:
            print("[LightweightGraphStore ERROR] Node ID and type are required.")
            return None

        props = properties if properties else {}
        if node_id in self.nodes:
            self.log_message(f"Node '{node_id}' already exists. Updating properties.")
            self.nodes[node_id]["properties"].update(props) # Simple merge, might need smarter update logic
            self.nodes[node_id]["type"] = node_type # Allow type update too
        else:
            self.nodes[node_id] = {"id": node_id, "type": node_type, "properties": props}
            # Initialize adjacency for the new node
            self.adj["out"].setdefault(node_id, [])
            self.adj["in"].setdefault(node_id, [])
            self.log_message(f"Added node: {node_id} (Type: {node_type})")
        return self.nodes[node_id]

    def add_edge(self, edge_id: str, source_id: str, target_id: str, edge_type: str, properties: Optional[Dict[str, Any]] = None) -> Optional[GraphEdge]:
        """Adds an edge to the graph. If edge_id exists, it updates properties."""
        if not all([edge_id, source_id, target_id, edge_type]):
            print("[LightweightGraphStore ERROR] Edge ID, source ID, target ID, and type are required.")
            return None
        if source_id not in self.nodes or target_id not in self.nodes:
            print(f"[LightweightGraphStore ERROR] Source node '{source_id}' or target node '{target_id}' not found.")
            return None

        props = properties if properties else {}
        if edge_id in self.edges:
            self.log_message(f"Edge '{edge_id}' already exists. Updating properties.")
            # Ensure source/target/type are not changed for existing edge to maintain consistency with adj list
            if (self.edges[edge_id]["source_id"] != source_id or
                self.edges[edge_id]["target_id"] != target_id or
                self.edges[edge_id]["type"] != edge_type):
                print(f"[LightweightGraphStore ERROR] Cannot change source/target/type of existing edge '{edge_id}'. Create new edge.")
                return None
            self.edges[edge_id]["properties"].update(props)
        else:
            self.edges[edge_id] = {"id": edge_id, "source_id": source_id, "target_id": target_id, "type": edge_type, "properties": props}
            # Update adjacency list
            self.adj["out"].setdefault(source_id, []).append(edge_id)
            self.adj["in"].setdefault(target_id, []).append(edge_id)
            self.log_message(f"Added edge: {edge_id} ({source_id} -[{edge_type}]-> {target_id})")
        return self.edges[edge_id]

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self.nodes.get(node_id)

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        return self.edges.get(edge_id)

    def get_neighbors(self, node_id: str, direction: str = "all") -> List[GraphNode]:
        """Gets neighbor nodes of a given node."""
        if node_id not in self.nodes:
            return []

        neighbor_nodes: List[GraphNode] = []
        seen_neighbor_ids = set()

        if direction in ["all", "outgoing"]:
            for edge_id in self.adj["out"].get(node_id, []):
                edge = self.edges[edge_id]
                neighbor_id = edge["target_id"]
                if neighbor_id not in seen_neighbor_ids and neighbor_id in self.nodes:
                    neighbor_nodes.append(self.nodes[neighbor_id])
                    seen_neighbor_ids.add(neighbor_id)

        if direction in ["all", "incoming"]:
            for edge_id in self.adj["in"].get(node_id, []):
                edge = self.edges[edge_id]
                neighbor_id = edge["source_id"]
                if neighbor_id not in seen_neighbor_ids and neighbor_id in self.nodes:
                    neighbor_nodes.append(self.nodes[neighbor_id])
                    seen_neighbor_ids.add(neighbor_id)
        return neighbor_nodes

    def get_incident_edges(self, node_id: str, direction: str = "all") -> List[GraphEdge]:
        """Gets edges connected to a given node."""
        if node_id not in self.nodes:
            return []

        incident_edges: List[GraphEdge] = []
        if direction in ["all", "outgoing"]:
            for edge_id in self.adj["out"].get(node_id, []):
                incident_edges.append(self.edges[edge_id])

        if direction in ["all", "incoming"]:
            # Avoid duplicates if an edge was already added (e.g. self-loop or if "all" and already processed as outgoing)
            # A simple way is to use a set of edge_ids if "all"
            edge_ids_added = {e["id"] for e in incident_edges} if direction == "all" else set()
            for edge_id in self.adj["in"].get(node_id, []):
                if edge_id not in edge_ids_added:
                    incident_edges.append(self.edges[edge_id])
                    if direction == "all": edge_ids_added.add(edge_id)
        return incident_edges

    def get_all_nodes(self) -> List[GraphNode]:
        return list(self.nodes.values())

    def get_all_edges(self) -> List[GraphEdge]:
        return list(self.edges.values())

    def save_to_json(self, custom_filepath: Optional[str] = None) -> bool:
        """Saves the current graph (nodes and edges) to the JSON file."""
        filepath_to_save = custom_filepath if custom_filepath else self.filepath
        self.log_message(f"Saving graph to {filepath_to_save}...")
        try:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(filepath_to_save), exist_ok=True)
            graph_data = {
                "nodes": list(self.nodes.values()), # Convert dict_values to list for JSON
                "edges": list(self.edges.values())
            }
            with open(filepath_to_save, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)
            self.log_message(f"Graph successfully saved. Nodes: {len(self.nodes)}, Edges: {len(self.edges)}")
            return True
        except IOError as e:
            self.log_message(f"Error saving graph to {filepath_to_save}: {e}", level="ERROR")
            return False

    def _load_from_json(self) -> bool:
        """Loads graph data from the JSON file upon initialization."""
        if not os.path.exists(self.filepath):
            self.log_message(f"File {self.filepath} not found. Starting with an empty graph.", level="WARN")
            return False

        self.log_message(f"Loading graph from {self.filepath}...")
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                graph_data = json.load(f)

            loaded_nodes = graph_data.get("nodes", [])
            loaded_edges = graph_data.get("edges", [])

            self.nodes = {node["id"]: node for node in loaded_nodes}
            self.edges = {edge["id"]: edge for edge in loaded_edges}
            self._rebuild_adj() # Rebuild adjacency list based on loaded edges

            self.log_message(f"Graph loaded. Nodes: {len(self.nodes)}, Edges: {len(self.edges)}")
            return True
        except (IOError, json.JSONDecodeError) as e:
            self.log_message(f"Error loading graph from {self.filepath}: {e}. Starting with an empty graph.", level="ERROR")
            self.nodes = {}
            self.edges = {}
            self.adj = {"out": {}, "in": {}}
            return False

    def log_message(self, message: str, level: str = "INFO"):
        import datetime
        print(f"{datetime.datetime.now().isoformat()} [{level}] [LightweightGraphStore] {message}")


if __name__ == '__main__':
    print("--- Testing LightweightGraphStore ---")
    test_file = "temp_test_graph_data.json"
    if os.path.exists(test_file): os.remove(test_file) # Clean start

    store = LightweightGraphStore(filepath=test_file)
    print(f"Initial store: Nodes={len(store.nodes)}, Edges={len(store.edges)}")

    # Add nodes
    store.add_node("n1", "EntityTypeA", {"name": "Node 1", "value": 100})
    store.add_node("n2", "EntityTypeB", {"name": "Node 2", "value": 200})
    store.add_node("n3", "EntityTypeA", {"name": "Node 3", "description": "Another node"})

    # Add edges
    store.add_edge("e1", "n1", "n2", "RELATES_TO", {"weight": 0.5})
    store.add_edge("e2", "n2", "n3", "INFLUENCES", {"strength": "high"})
    store.add_edge("e3", "n1", "n3", "RELATES_TO", {"notes": "indirect relation"})

    # Test updates
    store.add_node("n1", "EntityTypeA_Updated", {"value": 150, "new_prop": "updated"}) # Update n1
    store.add_edge("e1", "n1", "n2", "RELATES_TO", {"weight": 0.75, "status": "revised"}) # Update e1

    print(f"\nAfter additions/updates: Nodes={len(store.nodes)}, Edges={len(store.edges)}")
    print("Node n1:", store.get_node("n1"))
    print("Edge e1:", store.get_edge("e1"))

    print("\nNeighbors of n1:", store.get_neighbors("n1"))
    print("Outgoing edges from n1:", [e["id"] for e in store.get_incident_edges("n1", direction="outgoing")])
    print("Incoming edges to n3:", [e["id"] for e in store.get_incident_edges("n3", direction="incoming")])

    # Save and reload
    store.save_to_json()
    store_reloaded = LightweightGraphStore(filepath=test_file)
    print(f"\nReloaded store: Nodes={len(store_reloaded.nodes)}, Edges={len(store_reloaded.edges)}")
    print("Reloaded Node n1:", store_reloaded.get_node("n1"))
    assert store_reloaded.get_node("n1")["properties"]["value"] == 150
    assert store_reloaded.get_edge("e1")["properties"]["weight"] == 0.75
    print("Reloaded neighbors of n1:", store_reloaded.get_neighbors("n1"))


    # Test bad edge
    store.add_edge("e_bad", "n1", "non_existent_node", "FAILS")

    if os.path.exists(test_file): os.remove(test_file)
    print("\n--- LightweightGraphStore Test Finished ---")
