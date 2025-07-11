"""
graph_schema.py

Defines the conceptual schema for the AI-enhanced System Evolution Knowledge Graph (EKG)
for the Changjiang River Basin study. This includes node types and relationship types,
with a focus on representing evolutionary aspects.
"""

from enum import Enum
from typing import List, Dict, Any

# --- Node Labels / Types ---
class NodeType(Enum):
    """Defines the types of nodes in the knowledge graph."""
    # Existing types (can be reused as "entities" that have states or are involved in events)
    STUDY_AREA = "StudyArea"
    HYDROLOGICAL_STATION = "HydrologicalStation"
    METEOROLOGICAL_STATION = "MeteorologicalStation"
    WETLAND = "Wetland"
    RIVER_SECTION = "RiverSection"
    DAM_PROJECT = "DamProject"
    ECOLOGICAL_SPECIES = "EcologicalSpecies"
    POLLUTANT = "Pollutant"
    RESEARCH_PAPER = "ResearchPaper"
    AUTHOR = "Author"
    INSTITUTION = "Institution"
    MODEL_RUN_INSTANCE = "ModelRunInstance" # Renamed from ModelRun for clarity
    POLICY_MEASURE = "PolicyMeasure"        # Renamed from Policy for clarity
    OBSERVED_PHENOMENON = "ObservedPhenomenon"
    DATA_PARAMETER = "DataParameter"

    # New types for evolution tracking
    TEMPORAL_EVENT = "TemporalEvent" # Significant occurrences, e.g., "Flood 1998", "Policy Implementation 2005"
                                     # Properties: event_type, start_date, end_date, description, magnitude, affected_entities_ref (list of IDs)

    ENTITY_STATE = "EntityState"     # Represents the state of an entity (e.g., Wetland, RiverSection) at a specific time.
                                     # Properties: entity_ref (ID of the main entity node), state_timestamp, state_data_json (dict of properties like area, water_level, species_count)

    def __str__(self):
        return self.value

# --- Relationship Types / Edge Labels ---
class RelationshipType(Enum):
    """Defines the types of relationships (edges) between nodes."""
    # General relationships (can apply to entities)
    LOCATED_IN = "LOCATED_IN"
    ADJACENT_TO = "ADJACENT_TO"
    UPSTREAM_OF = "UPSTREAM_OF"
    PART_OF = "PART_OF"
    INFLUENCES = "INFLUENCES" # General influence, can have properties like 'effect_description', 'strength'
    CORRELATED_WITH = "CORRELATED_WITH"
    MENTIONS = "MENTIONS" # (ResearchPaper) -[MENTIONS]-> (Entity/Event)
    AUTHORED_BY = "AUTHORED_BY"
    AFFILIATED_WITH = "AFFILIATED_WITH"
    CITES = "CITES"
    DISCUSSES_TOPIC = "DISCUSSES_TOPIC"
    PRODUCED_BY_MODEL = "PRODUCED_BY_MODEL" # (Dataset/State) -[PRODUCED_BY_MODEL]-> (ModelRunInstance)
    MEASURES_PARAMETER_AT = "MEASURES_PARAMETER_AT" # (Station) -[MEASURES_PARAMETER_AT]-> (DataParameter) (Location implied by station)


    # Relationships for evolution and events
    HAS_STATE = "HAS_STATE"                 # (Entity e.g., Wetland) -[HAS_STATE]-> (EntityState)
                                            # This links an entity to its various states over time.

    TRANSITIONS_TO_STATE = "TRANSITIONS_TO_STATE" # (EntityState_T1) -[TRANSITIONS_TO_STATE {reason: 'seasonal change'}]-> (EntityState_T2)
                                                  # Represents direct evolution of an entity's state.

    CAUSED_EVENT = "CAUSED_EVENT"           # (Entity e.g., DamProject, or another TemporalEvent) -[CAUSED_EVENT]-> (TemporalEvent e.g., "Reduced Flow Event")
                                            # Can also be (PolicyMeasure) -[CAUSED_EVENT]-> (TemporalEvent "PolicyEnforcement")

    INFLUENCED_BY_EVENT = "INFLUENCED_BY_EVENT" # (EntityState or Entity) -[INFLUENCED_BY_EVENT {impact_description: 'area reduced'}]-> (TemporalEvent)
                                                # Shows how an event affected an entity or its state.

    PRECEDES_EVENT = "PRECEDES_EVENT"       # (TemporalEvent_A) -[PRECEDES_EVENT]-> (TemporalEvent_B)
    COOCCURS_WITH_EVENT = "COOCCURS_WITH_EVENT" # (TemporalEvent_A) -[COOCCURS_WITH_EVENT]-> (TemporalEvent_B)

    ASSOCIATED_WITH_PHENOMENON = "ASSOCIATED_WITH_PHENOMENON" # (EntityState or TemporalEvent) -[ASSOCIATED_WITH_PHENOMENON]-> (ObservedPhenomenon)

    HAS_OBSERVATION_AT_STATE = "HAS_OBSERVATION_AT_STATE" # (EntityState) -[HAS_OBSERVATION_AT_STATE {param, value, unit}]-> (DataParameter)
                                                         # Links specific measurements to a state.

    def __str__(self):
        return self.value

# --- Node Properties Examples (Illustrative for new types) ---
# For existing types, refer to previous definitions.
# These are conceptual and would be stored as dicts in the lightweight graph.
NODE_PROPERTIES_EXAMPLES_NEW: Dict[NodeType, List[str]] = {
    NodeType.TEMPORAL_EVENT: ["event_id", "event_type", "start_date", "end_date", "description", "magnitude", "affected_entities_ref_json", "data_source"],
    NodeType.ENTITY_STATE: ["state_id", "entity_ref_id", "entity_type_str", "state_timestamp", "state_data_json", "source_of_state_data"]
    # entity_ref_id points to the ID of the main entity node (e.g., a Wetland node's ID)
    # entity_type_str stores the NodeType of the referenced entity (e.g., "Wetland")
    # state_data_json stores a dict of properties like {"area_sqkm": 100, "dominant_species": "Phragmites"}
}

# --- Relationship Properties Examples (Illustrative for new types) ---
RELATIONSHIP_PROPERTIES_EXAMPLES_NEW: Dict[RelationshipType, List[str]] = {
    RelationshipType.INFLUENCED_BY_EVENT: ["impact_description", "impact_magnitude_qualitative", "confidence_score"],
    RelationshipType.TRANSITIONS_TO_STATE: ["transition_reason", "duration_of_transition", "triggering_event_ref_id"],
    RelationshipType.HAS_OBSERVATION_AT_STATE: ["parameter_name", "value_numeric", "value_text", "unit", "measurement_method"]
}


if __name__ == '__main__':
    print("Knowledge Graph Schema (Conceptual - Extended for Evolution)")

    print("\n--- All Node Types ---")
    for nt in NodeType:
        print(f"- {nt.value}")
        if nt in NODE_PROPERTIES_EXAMPLES_NEW:
            print(f"  Common New Properties: {', '.join(NODE_PROPERTIES_EXAMPLES_NEW[nt])}")

    print("\n--- All Relationship Types ---")
    for rt in RelationshipType:
        print(f"- {rt.value}")
        if rt in RELATIONSHIP_PROPERTIES_EXAMPLES_NEW:
            print(f"  Common New Properties: {', '.join(RELATIONSHIP_PROPERTIES_EXAMPLES_NEW[rt])}")

    # Example of evolution representation:
    print("\n--- Example Evolution Representation ---")
    wetland_entity = {"id": "WL001", "type": NodeType.WETLAND, "properties": {"name": "East Dongting Sample Patch"}}

    state1 = {
        "id": "WL001_State1", "type": NodeType.ENTITY_STATE,
        "properties": {
            "entity_ref_id": "WL001", "entity_type_str": "Wetland",
            "state_timestamp": "2000-06-15T00:00:00Z",
            "state_data_json": {"area_sqkm": 150.0, "vegetation_cover": 0.8}
        }
    }
    state2 = {
        "id": "WL001_State2", "type": NodeType.ENTITY_STATE,
        "properties": {
            "entity_ref_id": "WL001", "entity_type_str": "Wetland",
            "state_timestamp": "2005-07-20T00:00:00Z",
            "state_data_json": {"area_sqkm": 120.0, "vegetation_cover": 0.65}
        }
    }
    flood_event = {
        "id": "EVT001", "type": NodeType.TEMPORAL_EVENT,
        "properties": {
            "event_type": "MajorFlood", "start_date": "2005-07-01T00:00:00Z", "end_date": "2005-07-15T00:00:00Z",
            "description": "Summer flood affecting Dongting Lake area.", "magnitude": "High"
        }
    }

    print(f"Entity: {wetland_entity['properties']['name']} ({wetland_entity['type'].value})")
    print(f"  State 1 ({state1['type'].value}): Time {state1['properties']['state_timestamp']}, Area {state1['properties']['state_data_json']['area_sqkm']}")
    print(f"  State 2 ({state2['type'].value}): Time {state2['properties']['state_timestamp']}, Area {state2['properties']['state_data_json']['area_sqkm']}")
    print(f"Event ({flood_event['type'].value}): {flood_event['properties']['event_type']} starting {flood_event['properties']['start_date']}")

    print("\nRelationships:")
    print(f"  ({wetland_entity['id']}) -[{RelationshipType.HAS_STATE.value}]-> ({state1['id']})")
    print(f"  ({wetland_entity['id']}) -[{RelationshipType.HAS_STATE.value}]-> ({state2['id']})")
    print(f"  ({state1['id']}) -[{RelationshipType.TRANSITIONS_TO_STATE.value} {{reason: 'Post-flood impact'}]-> ({state2['id']})")
    print(f"  ({state2['id']}) -[{RelationshipType.INFLUENCED_BY_EVENT.value} {{impact_description: 'Area reduction due to flood scouring'}}]-> ({flood_event['id']})")
    print(f"  ({flood_event['id']}) -[{RelationshipType.PRECEDES_EVENT.value}]-> (AnotherEventID) (conceptually)")
