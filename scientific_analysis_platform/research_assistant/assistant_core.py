"""
assistant_core.py

Core logic for the Deep Research Assistant.
Integrates RAG components for Natural Language Querying (NLQ).
"""

import os
from typing import Dict, Any, Optional, List

# RAG Components (Simulated/Mocked for now)
from .document_processor import load_text_from_file, chunk_text
from .embedding_service import EmbeddingService
from .vector_store import SimpleVectorStore

# Potential future imports (not used in this phase directly by assistant_core)
# from ..ai_knowledge_graph.graph_querier import KnowledgeGraphQuerier

# Path to the root of the project (scientific_analysis_platform)
# This assumes assistant_core.py is in scientific_analysis_platform/research_assistant/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class ResearchAssistant:
    """
    Research assistant with basic keyword responses and a (simulated) RAG pipeline for NLQ.
    """

    def __init__(self, kg_querier: Optional[Any] = None, document_store_path: Optional[str] = None):
        """
        Initializes the ResearchAssistant.

        :param kg_querier: (Future) An instance of KnowledgeGraphQuerier.
        :param document_store_path: Path to a directory or file to be used as the initial document store for RAG.
        """
        self.kg_querier = kg_querier # Not used in this phase

        # Initialize RAG components
        self.embedding_service = EmbeddingService() # Uses simulated embeddings by default
        self.vector_store = SimpleVectorStore(embedding_dimension=self.embedding_service.simulated_dimension)

        print("[ResearchAssistant INFO] Initialized with EmbeddingService and SimpleVectorStore.")

        # Load and process initial documents for RAG
        self._initialize_document_store(document_store_path)

        if self.kg_querier:
            print("  - Knowledge Graph Querier is connected (simulated).")


    def _initialize_document_store(self, doc_path: Optional[str]):
        """Loads and processes documents into the vector store."""
        # For prototype, let's try to load README.md as a sample document.
        if not doc_path:
            # Default to loading README.md from the project root
            doc_path = os.path.join(PROJECT_ROOT, "README.md")
            print(f"[ResearchAssistant INFO] No document path provided, defaulting to project README: {doc_path}")

        if not os.path.exists(doc_path):
            print(f"[ResearchAssistant WARN] Document for RAG not found at: {doc_path}. RAG will have no context.")
            return

        try:
            print(f"[ResearchAssistant INFO] Initializing RAG document store from: {doc_path}")
            # For now, assume doc_path is a single file.
            # A real system would handle directories, multiple files, different types.
            text_content = load_text_from_file(doc_path)
            if not text_content:
                print(f"[ResearchAssistant WARN] No content loaded from {doc_path}.")
                return

            chunks = chunk_text(text_content, chunk_size=500, chunk_overlap=100) # Smaller chunks for testing
            if not chunks:
                print(f"[ResearchAssistant WARN] No chunks generated from {doc_path}.")
                return

            print(f"[ResearchAssistant INFO] Generated {len(chunks)} chunks from {doc_path}.")

            # Get (simulated) embeddings for these chunks
            chunk_embeddings = self.embedding_service.get_embeddings(chunks)
            print(f"[ResearchAssistant INFO] Generated {len(chunk_embeddings)} embeddings for chunks.")

            # Add to vector store
            self.vector_store.add_documents(chunks, chunk_embeddings)
            print(f"[ResearchAssistant INFO] Document store initialized with {self.vector_store.get_document_count()} chunks for RAG.")

        except Exception as e:
            print(f"[ResearchAssistant ERROR] Failed to initialize document store for RAG: {e}")
            import traceback
            traceback.print_exc()


    def _mock_llm_call(self, prompt: str, context_chunks: List[str]) -> str:
        """
        Simulates a call to an LLM with the given prompt and context.
        This is a very basic mock for prototyping.
        """
        print(f"\n[ResearchAssistant DEBUG] Mock LLM Call:")
        print(f"  Prompt (first 100 chars): {prompt[:100]}...")
        # print(f"  Context Chunks ({len(context_chunks)}):")
        # for i, chunk in enumerate(context_chunks[:2]): # Print first 2 chunks
        #     print(f"    Chunk {i}: {chunk[:80]}...")

        # Simple logic: if keywords from context appear in prompt, give canned response.
        # This is NOT how a real LLM works but simulates context usage.
        query_part = prompt.split("Question:")[-1].split("Answer:")[0].strip().lower()

        # Convert context to lowercase string for searching
        context_str_lower = " ".join(context_chunks).lower()

        if "yangtze river" in query_part or "changjiang" in query_part:
            if "yangtze river" in context_str_lower or "changjiang" in context_str_lower :
                 return "Based on the provided documents, the Yangtze River (Changjiang) is a significant area of study for this platform, focusing on aspects like hydrology and ecology. (Simulated LLM response using RAG context)"
            return "The documents provided some context, but specific details about the Yangtze River query were not prominent. (Simulated LLM response)"
        elif "platform" in query_part and "modules" in query_part:
            if "modules" in context_str_lower:
                return "The platform comprises several modules including Data Management, Model Integration, and Visualization, as per the documents. (Simulated LLM response using RAG context)"
        elif "data" in query_part and "import" in query_part:
             if "importers" in context_str_lower or "sample_data" in context_str_lower:
                 return "The platform includes functionality for importing sample data, such as station and wetland information, using importer scripts. (Simulated LLM response using RAG context)"

        if context_chunks: # If any context was retrieved
            return f"I have some context from the documents: '{context_chunks[0][:100]}...'. However, I need more specific instructions or a more advanced LLM to answer your query '{query_part}' precisely. (Simulated LLM response)"
        else:
            return f"I could not find relevant information in my current document set to answer your query about '{query_part}'. My knowledge is limited to the documents I've processed. (Simulated LLM response - no context found)"


    def query_llm_with_rag(self, user_query: str) -> Dict[str, Any]:
        """
        Processes a user query using the RAG pipeline and a (mocked) LLM.
        """
        print(f"[ResearchAssistant RAG] Processing query: '{user_query}'")
        source_info = "RAG Pipeline (Simulated LLM)"

        # 1. Get embedding for the user query
        query_embedding = self.embedding_service.get_embedding(user_query)

        # 2. Perform similarity search in VectorStore
        #    top_k can be tuned.
        relevant_chunks = self.vector_store.similarity_search(query_embedding, top_k=2)
        retrieved_texts = [text for text, score in relevant_chunks] # Get just the text part

        if retrieved_texts:
            print(f"[ResearchAssistant RAG] Retrieved {len(retrieved_texts)} relevant chunks for context.")
            # for i, chunk_text_score in enumerate(relevant_chunks):
            #     print(f"  Chunk {i} (score {chunk_text_score[1]:.4f}): '{chunk_text_score[0][:100]}...'")
        else:
            print("[ResearchAssistant RAG] No relevant chunks found in vector store.")

        # 3. Construct the prompt for the LLM
        context_str = "\n\n".join(retrieved_texts)
        prompt = f"Based on the following context, please answer the question.\n\nContext:\n{context_str}\n\nQuestion: {user_query}\n\nAnswer:"

        # 4. (Mock) Call the LLM
        llm_answer = self._mock_llm_call(prompt, retrieved_texts)

        # Confidence is hard to simulate meaningfully here without a real LLM
        # For now, base it on whether context was found.
        confidence = 0.65 if retrieved_texts else 0.25

        return {
            "query": user_query,
            "answer": llm_answer,
            "confidence": confidence,
            "source": source_info,
            "debug_info": {
                "rag_context_chunks_count": len(retrieved_texts),
                "rag_context_preview": [chunk[:150] + "..." for chunk in retrieved_texts[:2]] # Preview of first 2 chunks
            }
        }

    def process_query(self, query_text: str) -> Dict[str, Any]:
        """
        Processes a user's query, trying keyword matching first, then falling back to RAG NLQ.
        """
        print(f"[ResearchAssistant INFO] Received query: \"{query_text}\"")

        # Simple keyword-based responses (priority)
        query_lower = query_text.lower()
        if "hello" in query_lower or "hi" in query_lower:
            return {
                "query": query_text,
                "answer": "Hello! I am the Research Assistant for the Scientific Analysis Platform. How can I help you today with RAG-based queries or specific commands?",
                "confidence": 0.9,
                "source": "Keyword Match",
                "debug_info": "Processed by basic keyword matching."
            }
        # Add more keyword triggers if specific non-NLQ commands are needed.
        # Example:
        # elif "list all stations" == query_lower:
        #     # Here you might call a specific function to query DB via self.data_querier (if available)
        #     return {"answer": "Fetching all stations... (Simulated DB call)", "source": "Direct Command"}

        # If no keyword match, proceed to RAG-based NLQ
        print(f"[ResearchAssistant INFO] No keyword match for '{query_text}'. Proceeding with RAG-based NLQ.")
        return self.query_llm_with_rag(query_text)


    # search_documents method is now effectively replaced by the RAG pipeline.
    # If direct document search without LLM processing is still needed, it could be kept.
    # For this phase, we focus on RAG.

if __name__ == '__main__':
    print("--- Testing Research Assistant with RAG (Simulated) ---")

    # The assistant will try to load PROJECT_ROOT/README.md by default
    # Ensure README.md exists at that location relative to this script, or provide a valid path.
    # If scientific_analysis_platform is the root, and this script is in research_assistant,
    # PROJECT_ROOT should correctly point to scientific_analysis_platform.

    # For local testing, you might want to specify an explicit path to a test document:
    # test_doc_path = os.path.join(PROJECT_ROOT, "README.md") # Or any other .txt or .md file
    # print(f"Attempting to use document for RAG: {test_doc_path}")
    # assistant = ResearchAssistant(document_store_path=test_doc_path)

    assistant = ResearchAssistant() # Uses default README.md

    print(f"\n[Test INFO] RAG store initialized with {assistant.vector_store.get_document_count()} chunks.")
    if assistant.vector_store.get_document_count() == 0:
        print("[Test WARN] RAG document store is empty. NLQ results will be poor.")
        print(f"  Make sure a document (e.g., README.md) exists at the expected path: {os.path.join(PROJECT_ROOT, 'README.md')}")


    queries = [
        "Hello assistant",
        "What is this platform about?", # Should use RAG from README
        "Tell me about the modules in this project.", # Should use RAG
        "How to run data importers?", # Should use RAG from README's Getting Started
        "What is the capital of France?" # General knowledge, RAG might not find context
    ]

    for q_text in queries:
        print(f"\n--- User Query: \"{q_text}\" ---")
        result = assistant.process_query(q_text)
        print(f"  Assistant Answer: {result.get('answer')}")
        print(f"  Confidence: {result.get('confidence')}")
        print(f"  Source: {result.get('source')}")
        if result.get('debug_info'):
            print(f"  Debug Info: {result.get('debug_info')}")

    print("\n--- Research Assistant RAG Test Finished ---")
