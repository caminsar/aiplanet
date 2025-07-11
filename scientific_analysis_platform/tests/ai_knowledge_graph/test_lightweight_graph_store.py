import unittest
import os
import json
import sys

# Adjust path to import from the main project directory
# Assuming this test file is in tests/ai_knowledge_graph/
# and LightweightGraphStore is in ai_knowledge_graph/
# Correct path adjustment to reach 'scientific_analysis_platform' root
# then import 'scientific_analysis_platform.ai_knowledge_graph.lightweight_graph_store'

# Get the absolute path of the current test file
test_file_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to the 'tests' directory, then one more to 'scientific_analysis_platform' (project root for imports)
project_root_for_test = os.path.dirname(os.path.dirname(test_file_dir))

if project_root_for_test not in sys.path:
    sys.path.insert(0, project_root_for_test)

from scientific_analysis_platform.ai_knowledge_graph.lightweight_graph_store import LightweightGraphStore
from scientific_analysis_platform.ai_knowledge_graph.graph_schema import NodeType, RelationshipType


class TestLightweightGraphStore(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test graph file before each test."""
        self.test_graph_file = "temp_test_graph_for_unittest.json"
        # Ensure no old test file exists
        if os.path.exists(self.test_graph_file):
            os.remove(self.test_graph_file)
        self.store = LightweightGraphStore(filepath=self.test_graph_file)

    def tearDown(self):
        """Clean up the temporary test graph file after each test."""
        if os.path.exists(self.test_graph_file):
            os.remove(self.test_graph_file)

    def test_add_and_get_node(self):
        """Test adding a new node and retrieving it."""
        node_id = "test_node_1"
        node_type = NodeType.TEMPORAL_EVENT.value # Use enum value (string)
        properties = {"name": "Test Event", "date": "2024-01-01"}

        added_node = self.store.add_node(node_id, node_type, properties)
        self.assertIsNotNone(added_node)
        self.assertEqual(added_node["id"], node_id)
        self.assertEqual(added_node["type"], node_type)
        self.assertEqual(added_node["properties"], properties)

        retrieved_node = self.store.get_node(node_id)
        self.assertEqual(retrieved_node, added_node)

        self.assertEqual(len(self.store.nodes), 1)

    def test_update_node_properties(self):
        """Test updating an existing node's properties."""
        node_id = "update_node"
        self.store.add_node(node_id, NodeType.ENTITY_STATE.value, {"status": "initial"})

        updated_props = {"status": "updated", "value": 10}
        # Type can also be updated by add_node if desired, test that too
        updated_type = NodeType.OBSERVED_PHENOMENON.value
        self.store.add_node(node_id, updated_type, updated_props)

        updated_node = self.store.get_node(node_id)
        self.assertEqual(updated_node["properties"]["status"], "updated")
        self.assertEqual(updated_node["properties"]["value"], 10)
        self.assertEqual(updated_node["type"], updated_type)

    def test_add_and_get_edge(self):
        """Test adding a new edge and retrieving it."""
        self.store.add_node("src_node", "SourceType", {})
        self.store.add_node("tgt_node", "TargetType", {})

        edge_id = "test_edge_1"
        edge_type = RelationshipType.INFLUENCES.value
        properties = {"strength": "high"}

        added_edge = self.store.add_edge(edge_id, "src_node", "tgt_node", edge_type, properties)
        self.assertIsNotNone(added_edge)
        self.assertEqual(added_edge["id"], edge_id)
        self.assertEqual(added_edge["source_id"], "src_node")
        self.assertEqual(added_edge["target_id"], "tgt_node")
        self.assertEqual(added_edge["type"], edge_type)
        self.assertEqual(added_edge["properties"], properties)

        retrieved_edge = self.store.get_edge(edge_id)
        self.assertEqual(retrieved_edge, added_edge)
        self.assertEqual(len(self.store.edges), 1)

    def test_add_edge_with_nonexistent_nodes(self):
        """Test adding an edge where source or target node does not exist."""
        edge = self.store.add_edge("e_fail", "no_src", "no_tgt", "FAILS")
        self.assertIsNone(edge)
        self.assertEqual(len(self.store.edges), 0)

    def test_save_and_load_json(self):
        """Test saving the graph to JSON and reloading it."""
        self.store.add_node("n1", "TypeA", {"prop1": "val1"})
        self.store.add_node("n2", "TypeB", {"prop2": "val2"})
        self.store.add_edge("e1", "n1", "n2", "LINKS_TO", {"weight": 1.0})

        save_success = self.store.save_to_json()
        self.assertTrue(save_success)
        self.assertTrue(os.path.exists(self.test_graph_file))

        # Create a new store instance to load from the file
        reloaded_store = LightweightGraphStore(filepath=self.test_graph_file)
        self.assertEqual(len(reloaded_store.nodes), 2)
        self.assertEqual(len(reloaded_store.edges), 1)

        reloaded_n1 = reloaded_store.get_node("n1")
        self.assertIsNotNone(reloaded_n1)
        self.assertEqual(reloaded_n1["properties"]["prop1"], "val1")

        reloaded_e1 = reloaded_store.get_edge("e1")
        self.assertIsNotNone(reloaded_e1)
        self.assertEqual(reloaded_e1["properties"]["weight"], 1.0)

        # Test adjacency list is rebuilt correctly
        self.assertIn("e1", reloaded_store.adj["out"].get("n1", []))
        self.assertIn("e1", reloaded_store.adj["in"].get("n2", []))


    def test_get_neighbors(self):
        """Test retrieving neighbors of a node."""
        self.store.add_node("center_node", "Center", {})
        self.store.add_node("out_neighbor1", "Out", {})
        self.store.add_node("in_neighbor1", "In", {})
        self.store.add_node("unconnected_node", "Other", {})

        self.store.add_edge("e_out1", "center_node", "out_neighbor1", "POINTS_TO")
        self.store.add_edge("e_in1", "in_neighbor1", "center_node", "POINTS_TO")

        # Test outgoing
        outgoing_neighbors = self.store.get_neighbors("center_node", direction="outgoing")
        self.assertEqual(len(outgoing_neighbors), 1)
        self.assertEqual(outgoing_neighbors[0]["id"], "out_neighbor1")

        # Test incoming
        incoming_neighbors = self.store.get_neighbors("center_node", direction="incoming")
        self.assertEqual(len(incoming_neighbors), 1)
        self.assertEqual(incoming_neighbors[0]["id"], "in_neighbor1")

        # Test all
        all_neighbors = self.store.get_neighbors("center_node", direction="all")
        self.assertEqual(len(all_neighbors), 2) # Order might vary, check IDs
        neighbor_ids = {n["id"] for n in all_neighbors}
        self.assertIn("out_neighbor1", neighbor_ids)
        self.assertIn("in_neighbor1", neighbor_ids)

    def test_get_incident_edges(self):
        """Test retrieving incident edges of a node."""
        self.store.add_node("n_a", "A", {})
        self.store.add_node("n_b", "B", {})
        self.store.add_node("n_c", "C", {})

        self.store.add_edge("e_ab", "n_a", "n_b", "CONNECTS")
        self.store.add_edge("e_ca", "n_c", "n_a", "CONNECTS")

        edges_n_a_all = self.store.get_incident_edges("n_a", direction="all")
        self.assertEqual(len(edges_n_a_all), 2)
        edge_ids_n_a = {e["id"] for e in edges_n_a_all}
        self.assertIn("e_ab", edge_ids_n_a)
        self.assertIn("e_ca", edge_ids_n_a)

        edges_n_a_out = self.store.get_incident_edges("n_a", direction="outgoing")
        self.assertEqual(len(edges_n_a_out), 1)
        self.assertEqual(edges_n_a_out[0]["id"], "e_ab")

        edges_n_a_in = self.store.get_incident_edges("n_a", direction="incoming")
        self.assertEqual(len(edges_n_a_in), 1)
        self.assertEqual(edges_n_a_in[0]["id"], "e_ca")

if __name__ == '__main__':
    unittest.main()
