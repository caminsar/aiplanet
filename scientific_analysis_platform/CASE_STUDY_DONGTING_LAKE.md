# Application Demonstration: Dongting Lake Case Study

## 1. Introduction

This document outlines a conceptual case study focusing on the Dongting Lake region, a critical wetland system in the middle reaches of the Yangtze River. The purpose of this case study is to demonstrate the integrated capabilities of the Scientific Analysis Platform in addressing typical research questions related to wetland evolution, hydrological changes, and potential drivers.

Given the current prototype stage of the platform, many analytical steps and AI outputs will be conceptual or based on simulated/mocked functionalities.

## 2. Case Study Objectives

This case study aims to:

1.  **Demonstrate Data Exploration and Visualization:** Showcase how a researcher can use the platform to find, view, and initially analyze data relevant to Dongting Lake (e.g., station locations, wetland boundaries, sample literature).
2.  **Illustrate Evolution Knowledge Graph (EKG) Utility:** Show how the EKG can be used to represent and query information about changes in Dongting Lake (e.g., wetland area over time) and related events (e.g., upstream dam construction).
3.  **Highlight AI Research Assistant Capabilities:** Demonstrate how the assistant can support research through:
    *   Natural Language Queries (NLQ) for information retrieval (from simulated RAG context).
    *   Automated literature summarization for specific topics related to Dongting Lake.
    *   Data-driven hypothesis generation based on conceptual observations about the lake.
    *   Interpretation of (placeholder) scenario simulation results relevant to Dongting Lake management.

## 3. Specific Research Questions (Conceptual Focus)

For this demonstration, we will focus on two interconnected conceptual research questions:

**RQ1: How has the area of a specific wetland patch in Dongting Lake (e.g., "WL001 - East Dongting Sample Patch") evolved over time, what major events might be associated with these changes according to the EKG, and what does existing literature (within the platform's RAG context) suggest about drivers of Dongting Lake wetland changes?**

*   **Platform Features to Use:**
    *   Data Catalog (to identify relevant data sources).
    *   EKG Visualizer (to explore WL001, its states, and connected events).
    *   EKG API (conceptually, how one might query detailed state changes).
    *   Research Assistant (NLQ for general info, literature summary for "Dongting Lake wetland changes" or "impact of TGD on Dongting Lake").

**RQ2: Based on an observation of "significant reduction in WL001 area between year X and year Y coinciding with upstream dam operations", what potential research hypotheses can be generated? Furthermore, if a scenario of "sustained reduced inflow due to upstream regulation" is simulated, what are the (AI-interpreted) potential implications?**

*   **Platform Features to Use:**
    *   Research Assistant (Hypothesis Generation feature with the observation as input).
    *   Scenario Simulator (UI to input the conceptual scenario).
    *   Research Assistant (AI Interpretation of the (placeholder) simulated output).

## 4. Data Requirements (Utilizing Existing Sample Data & EKG Enhancements)

*   **PostGIS Database:**
    *   `HydrologicalStation` data (from `stations.csv`).
    *   `WetlandArea` data (from `wetland_boundary.geojson`, specifically `WL001`).
*   **Evolution Knowledge Graph (`data/evolution_graph_data.json`):**
    *   Ensure `WL001` (East Dongting Sample Patch) exists as an entity node.
    *   Add at least two `EntityStateNode` instances for `WL001` representing its state (e.g., area) at different timestamps (e.g., Year 2000, Year 2010).
    *   Add a `TemporalEventNode` representing a significant event (e.g., "UpstreamDamActivity_TGD_FullOperation_2009").
    *   Link these nodes appropriately (e.g., `WL001 -HAS_STATE-> State_2000`, `State_2000 -TRANSITIONS_TO_STATE-> State_2010`, `State_2010 -INFLUENCED_BY_EVENT-> UpstreamDamActivity_TGD_FullOperation_2009`).
*   **Research Assistant RAG Context:**
    *   `README.md` (for general platform queries).
    *   `sample_data/literature/paper2_summary_wetlands.txt` (specifically relevant to Dongting Lake wetland changes).
    *   Other sample literature files for broader context.

## 5. Expected Outcomes (Conceptual)

*   A documented walkthrough (`DONGTING_CASE_STUDY_WALKTHROUGH.md`) detailing the steps taken to address RQ1 and RQ2 using the platform.
*   Demonstration of how different platform modules can be used in an integrated manner.
*   Illustration of the potential of AI-assisted features, even in their current simulated/mocked state.
*   Identification of areas for future development to better support such case studies (e.g., more sophisticated EKG queries, real model integration for scenario simulation, actual LLM integration).

This case study will serve as a proof-of-concept for the platform's utility and guide further refinement.
