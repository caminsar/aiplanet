"""
embedding_service.py

Provides a service for generating text embeddings.
For the prototype, this will simulate embedding generation.
A real implementation would use a sentence-transformer model or an external API.
"""
import numpy as np # For generating random vectors for simulation
from typing import List

# Configuration (Conceptual - based on AI_ENGINE_STRATEGY.md)
SIMULATED_EMBEDDING_DIMENSION = 384 # Example dimension for 'all-MiniLM-L6-v2'
USE_SIMULATED_EMBEDDINGS = True # Set to False to attempt real model loading (requires library)

# Placeholder for actual model loading if USE_SIMULATED_EMBEDDINGS is False
# from sentence_transformers import SentenceTransformer # Would be imported if not simulating

class EmbeddingService:
    """
    A service to convert text into dense vector embeddings.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the EmbeddingService.

        :param model_name: The name of the sentence-transformer model to use.
                           (Currently ignored if USE_SIMULATED_EMBEDDINGS is True).
        """
        self.model_name = model_name
        self.model = None
        self.simulated_dimension = SIMULATED_EMBEDDING_DIMENSION

        if USE_SIMULATED_EMBEDDINGS:
            print(f"[EmbeddingService INFO] Using SIMULATED embeddings of dimension {self.simulated_dimension}.")
        else:
            print(f"[EmbeddingService INFO] Attempting to load REAL embedding model: {self.model_name}")
            # try:
            #     self.model = SentenceTransformer(self.model_name)
            #     print(f"[EmbeddingService INFO] Successfully loaded model '{self.model_name}'.")
            #     # Get actual dimension from the loaded model
            #     # test_emb = self.model.encode(["test sentence"])
            #     # self.simulated_dimension = test_emb.shape[1]
            #     # print(f"[EmbeddingService INFO] Model embedding dimension: {self.simulated_dimension}")
            # except Exception as e:
            #     print(f"[EmbeddingService ERROR] Failed to load SentenceTransformer model '{self.model_name}': {e}")
            #     print("[EmbeddingService INFO] Falling back to SIMULATED embeddings.")
            #     USE_SIMULATED_EMBEDDINGS = True # Force simulation on error
            print(f"[EmbeddingService WARNING] Real model loading is commented out. Falling back to SIMULATED embeddings.")
            # Ensure USE_SIMULATED_EMBEDDINGS is true if model loading part is commented out.
            # This global modification is tricky; better to handle it via an instance variable.
            self.use_simulation_fallback = True


    def get_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding for a single piece of text.

        :param text: The input text.
        :return: A list of floats representing the embedding.
        """
        if not text.strip():
            # print("[EmbeddingService WARN] Received empty text for embedding, returning zero vector.")
            return [0.0] * self.simulated_dimension

        # Check if we should use simulation (either globally or as fallback)
        should_simulate = USE_SIMULATED_EMBEDDINGS or getattr(self, 'use_simulation_fallback', False)

        if not should_simulate and self.model:
            # Real embedding generation (conceptual, requires SentenceTransformer)
            # embedding = self.model.encode([text])[0] # Encode returns a list of embeddings
            # return embedding.tolist()
            pass # This path is currently not active due to commented out model loading

        # Simulated embedding: return a random vector of the configured dimension
        # For consistency in testing, one might use a fixed seed for np.random,
        # or generate a hash-based pseudo-random vector if determinism per text is needed.
        # For now, just random.
        np.random.seed(sum(ord(c) for c in text[:10])) # Simple seed based on text for some determinism
        sim_embedding = np.random.rand(self.simulated_dimension).astype(np.float32)
        # Normalize (optional, but good practice for cosine similarity)
        norm = np.linalg.norm(sim_embedding)
        if norm > 0:
            sim_embedding = sim_embedding / norm
        # print(f"[EmbeddingService DEBUG] Generated simulated embedding for text (first 10 chars): '{text[:10]}...'")
        return sim_embedding.tolist()

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts.

        :param texts: A list of input texts.
        :return: A list of embeddings (each embedding is a list of floats).
        """
        # print(f"[EmbeddingService INFO] Generating embeddings for {len(texts)} texts.")
        # This could be optimized for real models (batch processing).
        # For simulation, just call get_embedding for each.
        return [self.get_embedding(text) for text in texts]

if __name__ == "__main__":
    print("--- Testing Embedding Service ---")

    service = EmbeddingService()

    print("\n1. Testing with single texts (simulated):")
    text1 = "This is a test sentence for the Yangtze River project."
    emb1 = service.get_embedding(text1)
    print(f"  Embedding for text1 (first 5 dims): {emb1[:5]}... (Total dims: {len(emb1)})")

    text2 = "Another sentence about wetlands and hydrology."
    emb2 = service.get_embedding(text2)
    print(f"  Embedding for text2 (first 5 dims): {emb2[:5]}... (Total dims: {len(emb2)})")

    text3_empty = " "
    emb3_empty = service.get_embedding(text3_empty)
    print(f"  Embedding for empty text (first 5 dims): {emb3_empty[:5]}... (Total dims: {len(emb3_empty)})")


    print("\n2. Testing with a list of texts (simulated):")
    texts_list = [
        "Water quality is important.",
        "Sediment load affects river morphology.",
        text1 # Re-use text1
    ]
    embeddings_list = service.get_embeddings(texts_list)
    print(f"  Generated {len(embeddings_list)} embeddings.")
    for i, emb in enumerate(embeddings_list):
        print(f"  Embedding for texts_list[{i}] (first 5 dims): {emb[:5]}... (Total dims: {len(emb)})")

    # Simple check for determinism if seeded (as done in get_embedding)
    emb1_again = service.get_embedding(text1)
    if emb1 == emb1_again:
        print("\n  Deterministic check: PASSED (embeddings for same text are identical due to seeding).")
    else:
        print("\n  Deterministic check: FAILED (embeddings for same text differ). This might be ok if randomness is intended.")

    # Example of what would happen if real model loading was attempted (and failed)
    # print("\n3. Simulating attempt to load real model (conceptual):")
    # service_real_attempt = EmbeddingService(model_name="non_existent_hf_model_or_no_library")
    # # This would print warnings and fall back to simulated, as per current logic.
    # emb_real_attempt = service_real_attempt.get_embedding("Test with fallback.")
    # print(f"  Embedding from real-attempt service (first 5 dims): {emb_real_attempt[:5]}...")


    print("\n--- Embedding Service Test Finished ---")
