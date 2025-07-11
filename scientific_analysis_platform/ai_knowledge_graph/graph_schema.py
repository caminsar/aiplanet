"""
graph_schema.py

Defines the conceptual schema for the AI-enhanced System Evolution Knowledge Graph
for the Changjiang River Basin study. This includes node types and relationship types.
This is a conceptual representation and will guide the implementation with a graph database (e.g., Neo4j, JanusGraph).
"""

from enum import Enum
from typing import List, Dict, Any

# --- Node Labels / Types ---
class NodeType(Enum):
    """Defines the types of nodes in the knowledge graph."""
    STUDY_AREA = "StudyArea"              # e.g., "Yangtze River Middle Reach", "Dongting Lake"
    HYDROLOGICAL_STATION = "HydrologicalStation" # e.g., "Yichang Station", "Datong Station"
    METEOROLOGICAL_STATION = "MeteorologicalStation"
    WETLAND = "Wetland"                   # e.g., "East Dongting Wetland"
    RIVER_SECTION = "RiverSection"        # A specific reach or segment of the river
    DAM_PROJECT = "DamProject"            # e.g., "Three Gorges Dam"
    WATER_SAMPLE = "WaterSample"          # A specific water sample taken
    SEDIMENT_SAMPLE = "SedimentSample"    # A specific sediment sample
    ECOLOGICAL_SPECIES = "EcologicalSpecies" # e.g., "Finless Porpoise", "Reed"
    POLLUTANT = "Pollutant"               # e.g., "Total Phosphorus", "Heavy Metals"
    RESEARCH_PAPER = "ResearchPaper"      # Scientific literature
    AUTHOR = "Author"                     # Author of a research paper
    INSTITUTION = "Institution"           # Research institution
    MODEL_RUN = "ModelRun"                # An instance of a model execution from the platform
    EVENT = "Event"                       # Significant occurrences, e.g., "Flood Event 1998", "Drought 2011"
    POLICY = "Policy"                     # e.g., "Yangtze River Protection Law"
    OBSERVED_PHENOMENON = "ObservedPhenomenon" # e.g., "Algal Bloom", "Bank Erosion"
    DATA_PARAMETER = "DataParameter"      # e.g., "Water Level", "Sediment Concentration", "Flow Velocity"

    def __str__(self):
        return self.value

# --- Relationship Types / Edge Labels ---
class RelationshipType(Enum):
    """Defines the types of relationships (edges) between nodes."""
    # Spatial relationships
    LOCATED_IN = "LOCATED_IN"             # (HydrologicalStation) -[LOCATED_IN]-> (StudyArea)
    ADJACENT_TO = "ADJACENT_TO"           # (Wetland) -[ADJACENT_TO]-> (RiverSection)
    UPSTREAM_OF = "UPSTREAM_OF"           # (RiverSectionA) -[UPSTREAM_OF]-> (RiverSectionB)
    PART_OF = "PART_OF"                   # (Dongting Lake) -[PART_OF]-> (Yangtze River Middle Reach Study Area)

    # Temporal relationships / Evolution
    PRECEDES_EVENT = "PRECEDES_EVENT"     # (EventA) -[PRECEDES_EVENT]-> (EventB)
    FOLLOWS_EVENT = "FOLLOWS_EVENT"       # (EventB) -[FOLLOWS_EVENT]-> (EventA)
    OVERLAPS_WITH = "OVERLAPS_WITH"       # (PhenomenonA) -[OVERLAPS_WITH]-> (PhenomenonB) during a time period
    HAS_STATE_AT_TIME = "HAS_STATE_AT_TIME" # (Wetland) -[HAS_STATE_AT_TIME {time: '2000', area: '1500km^2'}]-> (Wetland) (could be self-loop with properties)

    # Influence / Causal relationships (often inferred or stated in literature)
    INFLUENCES = "INFLUENCES"             # (DamProject) -[INFLUENCES {effect: 'reduced sediment'}]-> (RiverSection)
    CAUSES = "CAUSES"                     # (PollutantDischarge) -[CAUSES]-> (AlgalBloom)
    CORRELATED_WITH = "CORRELATED_WITH"   # (Rainfall) -[CORRELATED_WITH {coefficient: 0.8}]-> (RiverFlow)
    MITIGATES = "MITIGATES"               # (Policy) -[MITIGATES]-> (Pollutant)
    EXACERBATES = "EXACERBATES"           # (LandUseChange) -[EXACERBATES]-> (SoilErosion)

    # Data & Measurement relationships
    MEASURES_PARAMETER = "MEASURES_PARAMETER" # (HydrologicalStation) -[MEASURES_PARAMETER]-> (DataParameter)
    HAS_OBSERVATION = "HAS_OBSERVATION"   # (WaterSample) -[HAS_OBSERVATION {value: 7.5, unit: 'pH'}]-> (DataParameter)
                                          # (HydrologicalStation) -[HAS_OBSERVATION {time: '...', value: ..., parameter: 'Flow'}]-> (HydrologicalStation)
    COLLECTED_AT = "COLLECTED_AT"         # (WaterSample) -[COLLECTED_AT]-> (LocationNode or specific coordinates)
    DERIVED_FROM = "DERIVED_FROM"         # (ModelRunOutput) -[DERIVED_FROM]-> (ModelRun)

    # Research & Provenance relationships
    AUTHORED_BY = "AUTHORED_BY"           # (ResearchPaper) -[AUTHORED_BY]-> (Author)
    AFFILIATED_WITH = "AFFILIATED_WITH"   # (Author) -[AFFILIATED_WITH]-> (Institution)
    CITES = "CITES"                       # (ResearchPaperA) -[CITES]-> (ResearchPaperB)
    DISCUSSES_TOPIC = "DISCUSSES_TOPIC"   # (ResearchPaper) -[DISCUSSES_TOPIC]-> (Wetland / Pollutant / etc.)
    PRODUCED_BY_MODEL = "PRODUCED_BY_MODEL" # (Dataset) -[PRODUCED_BY_MODEL]-> (ModelRun)

    # Ecological relationships
    HABITAT_OF = "HABITAT_OF"             # (Wetland) -[HABITAT_OF]-> (EcologicalSpecies)
    PREYS_ON = "PREYS_ON"                 # (SpeciesA) -[PREYS_ON]-> (SpeciesB)
    COMPETES_WITH = "COMPETES_WITH"       # (SpeciesA) -[COMPETES_WITH]-> (SpeciesB)

    # General relationships
    HAS_PROPERTY = "HAS_PROPERTY"         # (Node) -[HAS_PROPERTY {name: 'area', value: '100km^2'}]-> (Node)
    TYPE_OF = "TYPE_OF"                   # (SpecificDam) -[TYPE_OF]-> (DamProject) (less common if using labels well)
    MENTIONS = "MENTIONS"                 # (ResearchPaper) -[MENTIONS]-> (DamProject)

    def __str__(self):
        return self.value

# --- Node Properties (Common examples) ---
# These are not exhaustive but give an idea of attributes nodes might have.
# Actual properties will be stored directly on nodes in the graph database.

NODE_PROPERTIES_EXAMPLES: Dict[NodeType, List[str]] = {
    NodeType.STUDY_AREA: ["name", "description", "total_area_km2", "geojson_boundary"],
    NodeType.HYDROLOGICAL_STATION: ["station_id", "name", "latitude", "longitude", "river_name", "established_date"],
    NodeType.WETLAND: ["name", "type", "area_km2_timeseries", "dominant_vegetation", "geojson_boundary"],
    NodeType.DAM_PROJECT: ["name", "completion_date", "capacity_m3", "purpose", "height_m"],
    NodeType.RESEARCH_PAPER: ["doi", "title", "abstract", "publication_date", "journal"],
    NodeType.EVENT: ["event_type", "start_date", "end_date", "description", "magnitude", "affected_areas"],
    NodeType.DATA_PARAMETER: ["parameter_name", "description", "unit_of_measure", "domain"]
}

# --- Relationship Properties (Common examples) ---
# Properties that can exist on edges.

RELATIONSHIP_PROPERTIES_EXAMPLES: Dict[RelationshipType, List[str]] = {
    RelationshipType.LOCATED_IN: ["description"],
    RelationshipType.INFLUENCES: ["effect_description", "strength_qualitative", "time_lag_observed", "supporting_evidence_doi"],
    RelationshipType.CORRELATED_WITH: ["correlation_coefficient", "p_value", "time_period_of_correlation"],
    RelationshipType.HAS_OBSERVATION: ["value", "unit", "timestamp", "quality_flag", "sensor_id"],
    RelationshipType.CITES: ["citation_context_snippet"]
}


if __name__ == '__main__':
    print("Knowledge Graph Schema (Conceptual)")
    print("\n--- Node Types ---")
    for nt in NodeType:
        print(f"- {nt.value}")
        if nt in NODE_PROPERTIES_EXAMPLES:
            print(f"  Common Properties: {', '.join(NODE_PROPERTIES_EXAMPLES[nt])}")

    print("\n--- Relationship Types ---")
    for rt in RelationshipType:
        print(f"- {rt.value}")
        if rt in RELATIONSHIP_PROPERTIES_EXAMPLES:
            print(f"  Common Properties: {', '.join(RELATIONSHIP_PROPERTIES_EXAMPLES[rt])}")

    # Example of how one might think about a connection:
    print("\n--- Example Connection ---")
    example_node_1 = {"label": NodeType.DAM_PROJECT, "properties": {"name": "Three Gorges Dam"}}
    example_node_2 = {"label": NodeType.RIVER_SECTION, "properties": {"name": "Yichang-Datong Reach"}}
    example_relationship = {
        "type": RelationshipType.INFLUENCES,
        "properties": {
            "effect_description": "Significant reduction in sediment transport",
            "time_lag_observed": "Observed post-2003",
            "supporting_evidence_doi": "10.1000/somejournal.xxxx"
        }
    }
    print(f"Node 1: {example_node_1['label'].value} (Name: {example_node_1['properties']['name']})")
    print(f"Node 2: {example_node_2['label'].value} (Name: {example_node_2['properties']['name']})")
    print(f"Relationship: {example_relationship['type'].value}")
    print(f"  Properties: {example_relationship['properties']}")
