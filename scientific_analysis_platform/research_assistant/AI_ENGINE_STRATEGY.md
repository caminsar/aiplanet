# AI Engine and Natural Language Query (NLQ) Strategy

This document outlines the strategy for integrating an AI engine, primarily focusing on Large Language Models (LLMs) and Retrieval Augmented Generation (RAG), to enable Natural Language Query (NLQ) capabilities within the Scientific Analysis Platform.

## 1. Core Objective for NLQ

The primary goal is to allow users to ask questions in natural language about the data, models, and potentially the scientific knowledge contained within or accessible by the platform. For example:
- "What was the average water level at Yichang station in January 2023?"
- "Show me studies related to sediment transport changes after the Three Gorges Dam construction."
- "What environmental factors are most commonly associated with wetland degradation in the Dongting Lake area based on available literature?"

## 2. LLM Selection and Deployment Strategy (Prototype Phase)

Given the constraints of typical development environments (especially sandboxed ones) and the complexity of self-hosting large LLMs, the strategy for the initial prototype phase will be:

*   **Chosen Approach: External LLM API**
    *   **Rationale:** This approach offers access to state-of-the-art models without the significant overhead of local deployment, fine-tuning, and resource management (GPU, memory). It allows focusing on the RAG pipeline and NLQ logic.
    *   **Nominated Service (Example):** OpenAI's GPT series (e.g., GPT-3.5-turbo, GPT-4) via their API. Other alternatives include Anthropic's Claude or Google's Gemini. The specific choice can be made based on availability, cost, and performance for the types of queries anticipated.
    *   **API Key Management:** API keys will need to be managed securely (e.g., via environment variables, not committed to the repository).
    *   **Mocking:** If live API access is unavailable or costly during development/testing, API calls will be mocked to simulate LLM responses.

*   **Alternative (Considered but Deferred for Prototype): Local Open-Source LLM**
    *   **Examples:** Models from Hugging Face (e.g., Llama variants, Mistral, smaller fine-tuned models for Q&A).
    *   **Challenges:** Requires significant computational resources (GPU often necessary for good performance), setup complexity, and potentially fine-tuning for domain-specific accuracy. This is less feasible for a rapidly developed prototype in a constrained environment.
    *   **Future Consideration:** Could be explored for a production system for cost control, data privacy, or offline capabilities.

## 3. Retrieval Augmented Generation (RAG) Framework

To ground LLM responses in factual data from the platform (documents, database content, model metadata), a RAG framework will be implemented.

*   **A. Document Processing:**
    *   **Document Loaders:** Components to load text content from various sources (e.g., PDFs of research papers, Markdown files like `README.md`, text extracted from database records).
        *   *Module:* `research_assistant/document_processor.py`
    *   **Text Chunking:** Strategies to split large documents into smaller, manageable chunks suitable for embedding and retrieval.
        *   *Method:* Recursive character text splitting, semantic chunking (future).
        *   *Module:* `research_assistant/document_processor.py`

*   **B. Embedding Service:**
    *   **Purpose:** To convert text chunks and user queries into dense vector representations (embeddings).
    *   **Nominated Model (Example):** `all-MiniLM-L6-v2` from the `sentence-transformers` library (Hugging Face). This is a good general-purpose model, relatively small and efficient. Other models can be evaluated later.
    *   **Implementation:** A service class that loads the model and provides an embedding function.
        *   *Module:* `research_assistant/embedding_service.py`
    *   **Simulation for Prototype:** If running the actual sentence-transformer model is too heavy for the sandbox or initial tests, this service will return fixed-size random vectors, clearly marked as a simulation.

*   **C. Vector Store:**
    *   **Purpose:** To store the embeddings of document chunks and allow efficient similarity searches.
    *   **Nominated Approach (Conceptual for Prototype):** FAISS (Facebook AI Similarity Search) in-memory index. It's efficient and can be used locally.
        *   *Alternatives for larger scale:* PostgreSQL with `pgvector`, dedicated vector databases (Pinecone, Weaviate, Milvus, ChromaDB).
    *   **Implementation:** A class abstracting the vector store operations (add documents/embeddings, similarity search).
        *   *Module:* `research_assistant/vector_store.py`
    *   **Simulation for Prototype:** The `SimpleVectorStore` will store embeddings and texts in Python lists and perform a naive (e.g., first-k) similarity search if actual FAISS integration is too complex for the initial step.

*   **D. Retriever:**
    *   The retriever component uses the query embedding to search the vector store for the most relevant document chunks (the "context"). This is part of the `assistant_core.py` logic.

*   **E. Generator (LLM):**
    *   The LLM (selected in section 2) takes the original user query and the retrieved context chunks to generate a final, grounded answer. This interaction is managed by `assistant_core.py`.

## 4. NLQ Module Workflow (Conceptual)

The `ResearchAssistant` in `assistant_core.py` will orchestrate the NLQ process:

1.  User submits a natural language query.
2.  The query is processed:
    *   (Optional initial step) Keyword-based routing or simple intent detection. If it's a very specific command (e.g., "list stations"), it might bypass full RAG+LLM.
    *   For complex queries:
        a.  The user query is converted into an embedding using the `EmbeddingService`.
        b.  The `SimpleVectorStore` (or its equivalent) is queried with the embedding to find relevant document chunks.
        c.  A prompt is constructed containing the retrieved context and the original user query.
        d.  This prompt is sent to the chosen LLM (External API, mocked if necessary).
        e.  The LLM's response is received.
3.  The response is returned to the user.

## 5. Initial Data Sources for RAG

For the prototype, the RAG system will be tested with text content from:
*   Project documentation files (e.g., `README.md`, `DATA_ACQUISITION_CHECKLIST.md`).
*   (Future) Summaries or extracted text from sample research papers.
*   (Future) Metadata from the platform's database (e.g., descriptions of datasets, models).

## 6. Future Enhancements

*   **Hybrid Search:** Combining keyword search with semantic search.
*   **Query Transformation:** Using an LLM to refine user queries or break them into sub-queries.
*   **Agentic Behavior:** Allowing the LLM to interact with platform APIs (e.g., to fetch live data from the database based on the query).
*   **Fine-tuning:** Potentially fine-tuning smaller open-source LLMs or embedding models on domain-specific corpora.
*   **More Sophisticated Vector Stores:** Integration with `pgvector` or dedicated vector DBs.
*   **Evaluation Framework:** Metrics for NLQ performance (relevance, accuracy, factuality).

This strategy focuses on establishing a foundational, albeit simulated, RAG pipeline to demonstrate the potential of NLQ within the platform.
