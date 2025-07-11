from flask import Blueprint, jsonify, request, current_app
import uuid # For generating IDs if not provided by client for edges

# Assuming GraphDBConnector, KnowledgeGraphBuilder, KnowledgeGraphQuerier are accessible
# and configured to use LightweightGraphStore
from .graph_builder import GraphDBConnector, KnowledgeGraphBuilder
from .graph_querier import KnowledgeGraphQuerier
from .graph_schema import NodeType, RelationshipType # For type validation if needed

ekg_api_bp = Blueprint('ekg_api', __name__, url_prefix='/api/ekg')

# It's better to initialize connector (and thus store) once per app context or request context
# For simplicity in this phase, we might re-initialize per request or use a global if careful.
# A better approach is Flask app context or a dedicated service layer.
# Let's try a simplified approach: get a connector instance.
def get_ekg_services():
    """Helper to get EKG builder and querier instances."""
    # The connector will load/create the JSON file as per its logic
    # The filepath for the graph store is defined in graph_builder.DEFAULT_GRAPH_DATA_PATH
    connector = GraphDBConnector()
    builder = KnowledgeGraphBuilder(connector)
    querier = KnowledgeGraphQuerier(connector)
    return builder, querier, connector

@ekg_api_bp.route('/node', methods=['POST'])
def add_ekg_node():
    """
    Adds a generic node to the EKG.
    Expects JSON: {"id": "unique_node_id", "type": "NodeTypeString", "properties": {"key": "value"}}
    """
    data = request.get_json()
    if not data or not data.get("id") or not data.get("type"):
        return jsonify({"error": "Missing required fields: id, type"}), 400

    node_id = data["id"]
    node_type_str = data["type"]
    properties = data.get("properties", {})

    # Optional: Validate node_type_str against NodeType enum
    try:
        NodeType(node_type_str) # This will raise ValueError if not a valid NodeType
    except ValueError:
        return jsonify({"error": f"Invalid node type: {node_type_str}. Must be one of {[e.value for e in NodeType]}"}), 400

    builder, _, connector = get_ekg_services()
    try:
        node = builder.add_node(node_id, node_type_str, properties)
        if node:
            builder.save_graph() # Persist after successful add
            return jsonify({"message": "Node added/updated successfully", "node": node}), 201
        else:
            # add_node in LightweightGraphStore might return None if id/type missing, but we check above.
            # This path might not be easily reachable with current store add_node logic.
            return jsonify({"error": "Failed to add node, ID or Type might be invalid internally."}), 500
    except Exception as e:
        current_app.logger.error(f"Error adding EKG node: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connector: connector.close() # Ensures graph is saved by LightweightGraphStore's connector

@ekg_api_bp.route('/edge', methods=['POST'])
def add_ekg_edge():
    """
    Adds an edge to the EKG.
    Expects JSON: {"source_id": "...", "target_id": "...", "type": "RelationshipTypeString",
                   "properties": {...}, "id": "optional_edge_id"}
    """
    data = request.get_json()
    if not data or not data.get("source_id") or not data.get("target_id") or not data.get("type"):
        return jsonify({"error": "Missing required fields: source_id, target_id, type"}), 400

    edge_id = data.get("id") if data.get("id") else str(uuid.uuid4()) # Generate ID if not provided
    source_id = data["source_id"]
    target_id = data["target_id"]
    edge_type_str = data["type"]
    properties = data.get("properties", {})

    try:
        RelationshipType(edge_type_str) # Validate edge_type_str
    except ValueError:
        return jsonify({"error": f"Invalid edge type: {edge_type_str}. Must be one of { [e.value for e in RelationshipType]}"}), 400

    builder, querier, connector = get_ekg_services()
    try:
        # Check if source and target nodes exist
        if not querier.get_node_by_id(source_id) or not querier.get_node_by_id(target_id):
            return jsonify({"error": "Source or target node not found"}), 404

        edge = builder.add_relationship(edge_id, source_id, target_id, edge_type_str, properties)
        if edge:
            builder.save_graph() # Persist
            return jsonify({"message": "Edge added/updated successfully", "edge": edge}), 201
        else:
            # This path implies an issue within add_relationship like nodes not existing, already checked.
            return jsonify({"error": "Failed to add edge"}), 500
    except Exception as e:
        current_app.logger.error(f"Error adding EKG edge: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connector: connector.close()


@ekg_api_bp.route('/node/<node_id>', methods=['GET'])
def get_ekg_node_details(node_id: str):
    """Get details of a specific node by its ID."""
    _, querier, connector = get_ekg_services()
    try:
        node = querier.get_node_by_id(node_id)
        if node:
            return jsonify(node), 200
        else:
            return jsonify({"error": "Node not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Error getting EKG node {node_id}: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connector: connector.close() # Only reading, but store might have loaded. Close ensures no dangling file handles if store does more.

@ekg_api_bp.route('/node/<node_id>/evolution_path', methods=['GET'])
def get_ekg_node_evolution(node_id: str):
    """(Conceptual) Get evolution path related to a node."""
    _, querier, connector = get_ekg_services()
    try:
        # This is a conceptual method in querier, its output might be complex
        path_elements = querier.get_entity_evolution_path(node_id)
        if not path_elements and not querier.get_node_by_id(node_id): # Check if node itself DNE
            return jsonify({"error": f"Node {node_id} not found"}), 404

        return jsonify({"node_id": node_id, "evolution_path": path_elements}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting EKG node evolution for {node_id}: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connector: connector.close()


@ekg_api_bp.route('/graph_sample', methods=['GET'])
def get_ekg_graph_sample():
    """
    Returns a small, hardcoded sample graph subset for frontend visualization.
    In a real system, this might take parameters to define the subgraph.
    """
    _, querier, connector = get_ekg_services()
    try:
        # For now, let's return a small portion of the graph, e.g., first N nodes and their related edges.
        # Or, a predefined sample if the graph is empty.

        all_data = querier.get_all_graph_data()
        nodes = all_data.get("nodes", [])
        edges = all_data.get("edges", [])

        if not nodes: # If graph is empty, provide a very basic sample
            sample_nodes = [
                {"id": "sample_evt1", "type": "TemporalEvent", "properties": {"name": "Sample Event A (Graph Empty)", "date": "2023-01-01"}},
                {"id": "sample_state1", "type": "EntityState", "properties": {"name": "Sample State X (Graph Empty)", "value": 10}},
            ]
            sample_edges = [
                {"id": "s_e1", "source_id": "sample_evt1", "target_id": "sample_state1", "type": "INFLUENCES", "properties": {}}
            ]
            return jsonify({"nodes": sample_nodes, "edges": sample_edges}), 200

        # Limit sample size for now
        max_nodes_sample = 20
        max_edges_sample = 50

        sampled_nodes = nodes[:max_nodes_sample]
        sampled_node_ids = {n["id"] for n in sampled_nodes}

        # Filter edges to only include those connecting sampled nodes
        sampled_edges = [e for e in edges if e["source_id"] in sampled_node_ids and e["target_id"] in sampled_node_ids]
        sampled_edges = sampled_edges[:max_edges_sample]

        return jsonify({"nodes": sampled_nodes, "edges": sampled_edges}), 200

    except Exception as e:
        current_app.logger.error(f"Error getting EKG graph sample: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connector: connector.close()

# Health check for this blueprint
@ekg_api_bp.route('/health', methods=['GET'])
def ekg_health_check():
    return jsonify({"status": "healthy", "message": "EKG API is running (using LightweightGraphStore)."}), 200
