# System Technical Flowchart

This document provides a technical flowchart for the Scientific Analysis Platform, described using Mermaid syntax. It illustrates the high-level architecture and key process flows.

---

## 1. Overall System Architecture

This diagram shows the main components of the platform and how they are organized.

```mermaid
graph TD
    subgraph User Interface (Frontend)
        A1[Web Browser]
    end

    subgraph Backend (Flask Application)
        B1[Flask App / WSGI Server]
        B2[Visualization Routes]
        B3[Data API (Blueprint)]
        B4[EKG API (Blueprint)]
        B5[Assistant API (Blueprint)]
    end

    subgraph Core Logic & Services
        C1[Data Management Module]
        C2[Model Integration Module]
        C3[AI Knowledge Graph (EKG) Module]
        C4[Research Assistant Module]
    end

    subgraph Data & Persistence Layer
        D1[PostGIS Database]
        D2[EKG Store (JSON File)]
        D3[Model Files & Outputs]
        D4[RAG Document Store (Files)]
    end

    %% Connections
    A1 -- HTTPS --> B1
    B1 -- Routes to --> B2
    B1 -- Routes to --> B3
    B1 -- Routes to --> B4
    B1 -- Routes to --> B5

    B2 -- Renders HTML/JS/CSS --> A1
    B2 -- Fetches Data via --> B3
    B2 -- Fetches Graph Data via --> B4

    B3 -- Uses --> C1
    B4 -- Uses --> C3
    B5 -- Uses --> C4

    C1 -- Interacts with --> D1
    C2 -- Interacts with (conceptual) --> D3
    C3 -- Interacts with --> D2
    C4 -- Interacts with --> C3 & D4

    style User Interface fill:#d4edda,stroke:#155724
    style Backend fill:#cce5ff,stroke:#004085
    style Core Logic & Services fill:#fff3cd,stroke:#856404
    style Data & Persistence Layer fill:#f8d7da,stroke:#721c24
```

**Description:**
*   The **User** interacts with the platform via a **Web Browser**.
*   The **Backend** is a **Flask Application** that serves all requests. It's organized into **Blueprints** for different functionalities: Visualization web pages, Data APIs, EKG APIs, and Assistant APIs.
*   The API/Route layer communicates with the **Core Logic & Services** layer, where each module encapsulates specific business logic.
*   The **Core Logic** modules interact with the **Data & Persistence Layer** to store and retrieve data. This includes a **PostGIS Database** for structured spatio-temporal data, a **JSON file** for the EKG, and file-based storage for model files and RAG documents.

---

## 2. Data Ingestion and Management Flow

This diagram illustrates the process of getting raw data into the platform's queryable database.

```mermaid
graph LR
    subgraph Raw Data Sources
        DS1[CSV/Excel Files]
        DS2[Shapefiles/GeoJSON]
        DS3[NetCDF/GRIB (Future)]
    end

    subgraph Data Management Module
        IMP[Importer Scripts<br>(e.g., station_importer.py)]
        MOD[SQLAlchemy Models<br>(models.py)]
        DB_SESS[Database Session]
    end

    subgraph PostGIS Database
        TBL[Tables: stations, wetlands, readings, etc.]
    end

    %% Connections
    DS1 --> IMP
    DS2 --> IMP
    DS3 -.-> IMP

    IMP -- Uses --> MOD
    IMP -- Gets Session --> DB_SESS
    DB_SESS -- Writes to --> TBL

    style Raw Data Sources fill:#f8d7da,stroke:#721c24
    style Data Management Module fill:#fff3cd,stroke:#856404
```

**Description:**
1.  **Raw Data Sources** (e.g., CSV, GeoJSON) are identified.
2.  An **Importer Script** specific to the data format is executed (e.g., via `run_importers.py`).
3.  The importer script uses the **SQLAlchemy Models** to structure the data.
4.  It obtains a **Database Session** and uses it to write the structured data into the appropriate **Tables** in the **PostGIS Database**.

---

## 3. Research Assistant (RAG/NLQ) Flow (Simulated)

This diagram shows the steps involved when a user submits a natural language query to the Research Assistant.

```mermaid
graph TD
    A[User Query<br>e.g., "summarize literature on sediment"] --> B{Process Query in Assistant Core}

    B -- Keyword Match? --> C{Is it a direct command?<br>e.g., "hello"}
    C -- Yes --> D[Return Canned Response]
    C -- No --> E{Start RAG Pipeline}

    E --> F[1. Get Embedding for Query<br>(EmbeddingService - Simulated)]
    F --> G[2. Similarity Search in Vector Store<br>(SimpleVectorStore - Simulated)]
    G --> H[3. Retrieve Top-K Relevant Text Chunks<br>(e.g., from Literature/README)]
    H --> I[4. Construct Prompt with Context + Query]
    I --> J[5. Send to LLM for Answer Generation<br>(Mocked LLM Call)]
    J --> K[6. Receive Generated Answer]
    K --> L[Format Final Response]

    D --> L
    L --> Z[Return Response to User]

    subgraph RAG Context Storage
        R1[Document Files<br>(e.g., literature/*.txt)] --> R2{Load & Chunk<br>(DocumentProcessor)}
        R2 --> R3{Get Embeddings<br>(EmbeddingService)}
        R3 --> R4{Store Chunks & Embeddings<br>(SimpleVectorStore)}
    end

    G -- Searches in --> R4

    style RAG Context Storage fill:#e2e3e5,stroke:#383d41
```

**Description:**
*   **Offline/Initialization (RAG Context Storage):** Documents are loaded, chunked, converted to (simulated) embeddings, and stored in the (simulated) vector store.
*   **Online/Query Time:**
    1.  A user's query enters the `process_query` method.
    2.  A check for simple keywords (e.g., "hello") is performed first.
    3.  If no keyword matches, the RAG pipeline is initiated.
    4.  The user's query is converted to a (simulated) vector embedding.
    5.  This embedding is used to search the vector store for the most similar text chunks.
    6.  These retrieved chunks are combined with the original query to form a detailed prompt.
    7.  The prompt is sent to a (mocked) LLM.
    8.  The LLM's generated answer is received, formatted, and returned to the user.

---
This provides a comprehensive overview of the system's technical architecture and key operational flows.
