# Dongting Lake Case Study: Platform Walkthrough

This document provides a step-by-step conceptual walkthrough of how the Scientific Analysis Platform can be used to address the research questions defined in `CASE_STUDY_DONGTING_LAKE.md`.

**Assumptions:**
*   The platform is running locally (`http://localhost:5000`).
*   PostGIS database is populated with sample data (stations, wetlands).
*   The EKG JSON file (`data/evolution_graph_data.json`) is populated with relevant Dongting Lake data (WL001 states, TGD event).
*   The Research Assistant's RAG pipeline has processed `README.md` and sample literature files (including `paper2_summary_wetlands.txt`).
*   AI features (LLM calls for RAG, hypothesis generation, scenario interpretation) are simulated/mocked.

## Research Question 1: How has the area of a specific wetland patch in Dongting Lake (e.g., "WL001 - East Dongting Sample Patch") evolved over time, what major events might be associated with these changes according to the EKG, and what does existing literature (within the platform's RAG context) suggest about drivers of Dongting Lake wetland changes?

**Step 1: Explore Available Data (Data Catalog)**

1.  **Action:** Navigate to the "Data Catalog" page (`/view/catalog`).
2.  **Observation:**
    *   The catalog lists "Hydrological Stations", "Wetland Areas", and "Evolution Knowledge Graph (EKG)" as available data resources.
    *   It shows a count for stations and wetlands, confirming data is loaded.
    *   Each entry provides a description, a link to its API endpoint, and a link to a relevant UI view.
3.  **Inference:** The platform has data related to wetlands and an EKG that might contain evolutionary information.

**Step 2: Visualize Wetland Area on Map (Conceptual - if detailed geometry was focus)**

1.  **Action:** From the Data Catalog, click the "View in UI" link for "Wetland Areas," which would typically lead to the map page (`/view/map`).
2.  **Observation (Current Map Functionality):** The current map page primarily shows station locations. To see wetland boundaries, the map page would need enhancement to fetch and render polygon data from the `/api/data/wetlands` GeoJSON endpoint.
3.  **Conceptual Next Step (if map was enhanced):** User would see wetland polygons, including "WL001 - East Dongting Sample Patch". They could click on it to get basic properties. This step highlights a future enhancement for the map view.

**Step 3: Explore Wetland Evolution in EKG Visualizer**

1.  **Action:** Navigate to the "EKG Visualizer" page (`/view/ekg`). Click "Load/Refresh Graph Sample".
2.  **Observation:**
    *   The graph displays nodes and edges from `evolution_graph_data.json`.
    *   User can visually identify the node `WL001` (Type: Wetland).
    *   User can see `EntityStateNode` instances (e.g., `WL001_State_2000`, `WL001_State_2010`) connected to `WL001` via `HAS_STATE` edges.
    *   Hovering over `WL001_State_2000` might show properties like `{"area_sqkm": 150.0, "state_timestamp": "2000-06-15..."}`.
    *   Hovering over `WL001_State_2010` might show `{"area_sqkm": 120.0, "state_timestamp": "2005-07-20..."}`.
    *   A `TRANSITIONS_TO_STATE` edge connects `WL001_State_2000` to `WL001_State_2010`.
    *   The `TGD_Ops_2009` (TemporalEvent) node is visible.
    *   An `INFLUENCED_BY_EVENT` edge connects `WL001_State_2010` to `TGD_Ops_2009`, with properties like `{"impact_description": "Reduced sediment input..."}`.
3.  **Inference from EKG:**
    *   The area of WL001 decreased from 150 sqkm (2000) to 120 sqkm (2010).
    *   The TGD full operation in 2009 is recorded as an event that influenced the state of WL001 in 2010.

**Step 4: Query Research Assistant for Literature Summary**

1.  **Action:** Navigate to the "Research Assistant" page (`/assistant`).
2.  **Input Query:** Type "summarize literature on wetland changes in Dongting Lake" and submit.
3.  **Observation (Simulated Assistant Response):**
    *   The assistant responds with something like: "Studies on Dongting Lake indicate wetland area changes due to reclamation and hydrological alterations. Literature suggests dam construction significantly impacts sediment load in the Yangtze. (Simulated Literature Summary from LLM)"
    *   The debug info might show snippets from `paper2_summary_wetlands.txt` were retrieved by RAG.
4.  **Input Query 2:** Type "What does literature say about TGD impact on Dongting Lake wetlands?"
5.  **Observation (Simulated Assistant Response):**
    *   A similar summary, potentially highlighting "Reduced sediment input post-TGD" from `paper2_summary_wetlands.txt`.
6.  **Inference:** The assistant (based on its RAG context from sample literature) corroborates that dam construction (like TGD) and land reclamation are known drivers of wetland changes in Dongting Lake.

**Answer to RQ1 (Conceptual):**
The EKG visually and structurally shows that the "East Dongting Sample Patch (WL001)" decreased in area from 150 sqkm in 2000 to 120 sqkm in 2010. This change is linked in the EKG to the influence of the "Three Gorges Dam Full Operation" event in 2009. The Research Assistant, by summarizing (simulated) relevant literature snippets, further suggests that upstream dam construction (affecting sediment and water regimes) and land reclamation are recognized drivers of wetland changes in the Dongting Lake area.

## Research Question 2: Based on an observation of "significant reduction in WL001 area between year X and year Y coinciding with upstream dam operations", what potential research hypotheses can be generated? Furthermore, if a scenario of "sustained reduced inflow due to upstream regulation" is simulated, what are the (AI-interpreted) potential implications?

**Step 1: Generate Hypotheses with Research Assistant**

1.  **Action:** Navigate to the "Research Assistant" page (`/assistant`).
2.  **Input Query:** Type "generate hypothesis for: The area of Dongting Lake wetland WL001 significantly reduced between 2000 and 2010, coinciding with the full operation of the Three Gorges Dam in 2009."
3.  **Observation (Simulated Assistant Response):**
    *   The assistant responds with hypotheses like:
        *   "Hypothesis 1 (mocked): The reduction in WL001 area is primarily driven by decreased sediment deposition from the Yangtze River due to sediment trapping by the Three Gorges Dam, leading to enhanced local erosion or subsidence."
        *   "Hypothesis 2 (mocked): Altered hydrological regimes (e.g., changes in flood pulse duration and magnitude) post-TGD operation are the main cause for the observed wetland shrinkage in WL001."
4.  **Inference:** The assistant provides plausible (though mocked) starting points for further research based on the observation.

**Step 2: Simulate Scenario and Get AI Interpretation**

1.  **Action:** Navigate to the "Scenario Simulator" page (`/view/scenario-simulator`).
2.  **Input Scenario Parameters:**
    *   Scenario Name: "Reduced Inflow Impact on Dongting WL001"
    *   Rainfall Change (%): 0 (to isolate inflow impact)
    *   Dam Outflow Adjustment (m³/s): -5000 (simulating a significant reduction in inflow to Dongting from upstream)
    *   Land Use Change Type: None
    *   Additional Scenario Description: "Simulate impact of sustained 5000 m³/s reduction in Yangtze inflow towards Dongting Lake on wetland WL001 area over a 5-year period."
3.  **Action:** Click "Run Simulation (Conceptual)".
4.  **Observation (Placeholder Output):**
    *   Scenario Input Summary: Displays the parameters entered.
    *   Simulated Model Output: Shows something like: `{"affected_area": "Dongting Lake WL001", "primary_impact_parameter": "Wetland Area", "change_magnitude_percent": -15, "secondary_impact": "Potential increase in drought stress for peripheral vegetation.", "confidence": "Conceptual Simulation - Low", "dam_impact_note": "Dam outflow adjustment of -5000 m³/s considered."}`
5.  **Action:** Click "Interpret Results with AI (Conceptual)".
6.  **Observation (Simulated Assistant Response):**
    *   The AI Interpretation text area updates with a response like: "Interpreting Scenario (mocked): Parameters '{\"name\":\"Reduced Inflow Impact on Dongting WL001\", ... \"damOutflowAdjustmentM3s\":-5000,...}' led to output '{\"affected_area\":\"Dongting Lake WL001\", ... \"change_magnitude_percent\":-15,...}'. A sustained reduction of 5000 m³/s in inflow, as simulated, would likely lead to a significant (e.g., 15%) decrease in the WL001 wetland area. This could exacerbate drought stress, reduce habitat availability for aquatic species, and diminish the flood retention capacity of this wetland portion. Further detailed hydrodynamic and ecological modeling is recommended to validate these potential implications. (Simulated AI Interpretation)"
7.  **Inference:** The platform provides a (conceptual) end-to-end workflow from defining a scenario, seeing a placeholder simulated outcome, and getting an AI-generated (mocked) interpretation of potential consequences.

**Answer to RQ2 (Conceptual):**
Based on the observation of WL001 area reduction coinciding with TGD operation, the Research Assistant generated hypotheses pointing towards sediment trapping and altered hydrological regimes as primary drivers. Simulating a "sustained reduced inflow" scenario (placeholder simulation) and using the AI interpretation feature (mocked) suggested potential outcomes like further wetland area reduction and increased drought stress, highlighting areas for more detailed modeling or policy consideration.

## 6. Conclusion of Case Study Walkthrough

This conceptual walkthrough demonstrates how the Scientific Analysis Platform, even in its current prototype stage with many simulated components, can guide a researcher through a workflow involving data discovery, EKG exploration, literature review assistance, hypothesis generation, and scenario impact interpretation. It highlights the potential of integrating these diverse tools to support complex environmental research in areas like Dongting Lake. Future development will focus on replacing simulated components with real analytical engines and AI models.
