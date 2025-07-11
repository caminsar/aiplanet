"""
vector_store.py

Provides a simple in-memory vector store for the RAG framework.
For the prototype, this will simulate storing and searching embeddings.
A real implementation would use a library like FAISS, pgvector, or a dedicated vector DB.
"""

from typing import List, Tuple, Dict, Any
import numpy as np # For basic vector operations in simulation

# Configuration (Conceptual)
USE_SIMULATED_VECTOR_STORE = True
# If False, one might try to integrate FAISS or similar, which is complex for sandbox.

# Placeholder for actual FAISS index if not simulating
# import faiss # Would be imported if not simulating

class SimpleVectorStore:
    """
    A very simple in-memory vector store for prototyping RAG.
    It stores texts and their corresponding embeddings (simulated or real).
    Similarity search is also simulated.
    """

    def __init__(self, embedding_dimension: int):
        """
        Initializes the SimpleVectorStore.
        :param embedding_dimension: The dimension of the embeddings it will store.
        """
        self.embedding_dimension = embedding_dimension
        self.stored_texts: List[str] = []
        self.stored_embeddings: List[np.ndarray] = [] # Store as numpy arrays for easier math

        self.index = None # Placeholder for a real index (e.g., FAISS index)

        if USE_SIMULATED_VECTOR_STORE:
            print(f"[VectorStore INFO] Using SIMULATED in-memory vector store (list-based).")
        else:
            # Conceptual: Initialize FAISS index
            # try:
            #     self.index = faiss.IndexFlatL2(self.embedding_dimension) # L2 distance index
            #     # Or: self.index = faiss.IndexFlatIP(self.embedding_dimension) # Inner product for cosine similarity if embeddings are normalized
            #     print(f"[VectorStore INFO] Initialized FAISS IndexFlatL2 with dimension {self.embedding_dimension}.")
            # except Exception as e:
            #     print(f"[VectorStore ERROR] Failed to initialize FAISS index: {e}. Falling back to simulation.")
            #     USE_SIMULATED_VECTOR_STORE = True # Force simulation
            print(f"[VectorStore WARNING] Real FAISS index initialization is commented out. Using SIMULATED store.")
            self.use_simulation_fallback = True # Ensure simulation

        print(f"[VectorStore INFO] Initialized with embedding dimension: {self.embedding_dimension}")

    def add_documents(self, texts: List[str], embeddings: List[List[float]]):
        """
        Adds documents (texts and their embeddings) to the store.

        :param texts: A list of original text chunks.
        :param embeddings: A list of corresponding embeddings (as lists of floats).
        """
        if len(texts) != len(embeddings):
            raise ValueError("Number of texts and embeddings must be the same.")
        if not texts:
            print("[VectorStore WARN] No documents provided to add.")
            return

        print(f"[VectorStore INFO] Adding {len(texts)} documents to the store.")

        # Convert list of floats to numpy arrays for internal storage/processing
        np_embeddings = [np.array(emb, dtype=np.float32) for emb in embeddings]

        # Validate embedding dimensions
        for i, emb_np in enumerate(np_embeddings):
            if emb_np.shape[0] != self.embedding_dimension:
                raise ValueError(f"Embedding for text {i} has dimension {emb_np.shape[0]}, expected {self.embedding_dimension}.")

        should_simulate = USE_SIMULATED_VECTOR_STORE or getattr(self, 'use_simulation_fallback', False)

        if not should_simulate and self.index is not None:
            # Real FAISS usage (conceptual)
            # self.index.add(np.array(np_embeddings))
            # self.stored_texts.extend(texts) # Still need to store texts separately for retrieval
            pass # Path not active
        else:
            # Simulated: just append to lists
            self.stored_texts.extend(texts)
            self.stored_embeddings.extend(np_embeddings)

        print(f"[VectorStore INFO] Store now contains {len(self.stored_texts)} documents.")

    def similarity_search(self, query_embedding: List[float], top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Performs a similarity search for a given query embedding.

        :param query_embedding: The embedding of the query text (as a list of floats).
        :param top_k: The number of most similar documents to return.
        :return: A list of tuples, where each tuple is (document_text, similarity_score).
                 For simulation, score might be arbitrary or based on simple distance.
        """
        if not self.stored_texts:
            print("[VectorStore WARN] No documents in store to search.")
            return []

        print(f"[VectorStore INFO] Performing similarity search for top {top_k} results.")
        query_emb_np = np.array(query_embedding, dtype=np.float32)
        if query_emb_np.shape[0] != self.embedding_dimension:
            raise ValueError(f"Query embedding has dimension {query_emb_np.shape[0]}, expected {self.embedding_dimension}.")

        should_simulate = USE_SIMULATED_VECTOR_STORE or getattr(self, 'use_simulation_fallback', False)

        results: List[Tuple[str, float]] = []

        if not should_simulate and self.index is not None:
            # Real FAISS usage (conceptual)
            # distances, indices = self.index.search(np.array([query_emb_np]), top_k)
            # # distances are L2 squared by default with IndexFlatL2. Convert to similarity score if needed.
            # # For cosine similarity with IndexFlatIP, results are inner products.
            # for i in range(len(indices[0])):
            #     idx = indices[0][i]
            #     dist = distances[0][i]
            #     # Example: simple inverse of distance as score, or 1 - normalized_L2_dist
            #     score = 1.0 / (1.0 + dist) if dist >= 0 else 1.0
            #     results.append((self.stored_texts[idx], float(score)))
            pass # Path not active
        else:
            # Simulated similarity search:
            # Calculate cosine similarity (assuming embeddings are normalized) or Euclidean distance.
            # For simplicity, let's use Euclidean distance and then invert it for a "score".
            # Or, even simpler for a pure placeholder: return the first top_k items.

            if not self.stored_embeddings: # Should be caught by earlier check too
                return []

            # Calculate Euclidean distances to all stored embeddings
            distances = []
            for i, emb in enumerate(self.stored_embeddings):
                dist = np.linalg.norm(query_emb_np - emb)
                distances.append((dist, i)) # Store distance and original index

            # Sort by distance (ascending)
            distances.sort(key=lambda x: x[0])

            # Get top_k results
            for i in range(min(top_k, len(distances))):
                dist, original_idx = distances[i]
                # Convert distance to a pseudo-similarity score (0 to 1, higher is better)
                # This is arbitrary for simulation; real scores depend on the metric.
                similarity_score = 1.0 / (1.0 + dist)
                results.append((self.stored_texts[original_idx], float(similarity_score)))
                # print(f"[VectorStore DEBUG] Match: '{self.stored_texts[original_idx][:30]}...' (Dist: {dist:.4f}, Score: {similarity_score:.4f})")

        print(f"[VectorStore INFO] Similarity search found {len(results)} results.")
        return results

    def get_document_count(self) -> int:
        return len(self.stored_texts)

if __name__ == "__main__":
    print("--- Testing Simple Vector Store ---")

    # Assume embedding dimension from a service (e.g., EmbeddingService's simulated dim)
    test_embedding_dim = 384 # Must match what EmbeddingService produces

    store = SimpleVectorStore(embedding_dimension=test_embedding_dim)

    print("\n1. Testing add_documents (simulated):")
    sample_texts = [
        "The Yangtze River is the longest river in Asia.",
        "Wetlands are important ecosystems for biodiversity.",
        "Hydrological models help predict water flow.",
        "Data management is key for scientific research."
    ]
    # Simulate embeddings (random vectors)
    np.random.seed(42) # For reproducible random embeddings
    sample_embeddings_np = [np.random.rand(test_embedding_dim).astype(np.float32) for _ in sample_texts]
    # Normalize them (as cosine similarity often expects normalized vectors)
    sample_embeddings_np = [emb / np.linalg.norm(emb) if np.linalg.norm(emb) > 0 else emb for emb in sample_embeddings_np]
    sample_embeddings_list_float = [emb.tolist() for emb in sample_embeddings_np]

    store.add_documents(sample_texts, sample_embeddings_list_float)
    print(f"  Store document count: {store.get_document_count()}")

    # Test adding more documents
    more_texts = ["Climate change impacts water resources significantly."]
    more_embeddings_np = [np.random.rand(test_embedding_dim).astype(np.float32)]
    more_embeddings_np = [emb / np.linalg.norm(emb) if np.linalg.norm(emb) > 0 else emb for emb in more_embeddings_np]
    store.add_documents(more_texts, [e.tolist() for e in more_embeddings_np])
    print(f"  Store document count after adding more: {store.get_document_count()}")


    print("\n2. Testing similarity_search (simulated):")
    # Simulate a query embedding (e.g., for "information about rivers")
    # For a meaningful test, this query embedding should be somewhat similar to one of the stored ones.
    # Let's make it very similar to the first document's embedding + some noise.
    query_vector_np = sample_embeddings_np[0] + (np.random.rand(test_embedding_dim).astype(np.float32) * 0.1)
    query_vector_np = query_vector_np / np.linalg.norm(query_vector_np) # Normalize

    search_results = store.similarity_search(query_vector_np.tolist(), top_k=2)
    print(f"  Search results for query (expected to be close to first doc):")
    for text, score in search_results:
        print(f"    - Score: {score:.4f}, Text: '{text}'")

    # Test search with an empty store (after recreating it)
    empty_store = SimpleVectorStore(embedding_dimension=test_embedding_dim)
    empty_results = empty_store.similarity_search(query_vector_np.tolist(), top_k=2)
    print(f"\n  Search results from empty store: {empty_results} (Count: {len(empty_results)})")

    # Test dimension mismatch
    print("\n3. Testing dimension mismatch error:")
    try:
        wrong_dim_emb = np.random.rand(test_embedding_dim + 1).tolist()
        store.similarity_search(wrong_dim_emb)
    except ValueError as e:
        print(f"  Caught expected error: {e}")

    try:
        store.add_documents(["text with wrong emb dim"], [wrong_dim_emb])
    except ValueError as e:
        print(f"  Caught expected error during add_documents: {e}")


    print("\n--- Simple Vector Store Test Finished ---")
