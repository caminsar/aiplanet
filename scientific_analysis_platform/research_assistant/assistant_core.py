"""
assistant_core.py

Core logic for the Deep Research Assistant.
Integrates RAG components for Natural Language Querying (NLQ)
and conceptual features like literature summary, hypothesis generation, and scenario interpretation.
"""

import os
import re # For keyword parsing
import json # For parsing structured query parts
from typing import Dict, Any, Optional, List

# RAG Components (Simulated/Mocked for now)
from .document_processor import load_text_from_file, chunk_text
from .embedding_service import EmbeddingService
from .vector_store import SimpleVectorStore
from .hypothesis_generator import generate_hypotheses_from_observation

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_LITERATURE_PATH = os.path.join(PROJECT_ROOT, "sample_data", "literature")


class ResearchAssistant:
    """
    Research assistant with keyword responses, RAG NLQ, literature summary,
    hypothesis generation, and (simulated) scenario interpretation.
    """

    def __init__(self, kg_querier: Optional[Any] = None, document_store_path: Optional[str] = None, load_readme: bool = True):
        self.kg_querier = kg_querier
        self.embedding_service = EmbeddingService()
        self.vector_store = SimpleVectorStore(embedding_dimension=self.embedding_service.simulated_dimension)

        print("[ResearchAssistant INFO] Initialized with EmbeddingService and SimpleVectorStore.")
        self._initialize_document_store(document_store_path, load_readme=load_readme)
        if self.kg_querier:
            print("  - Knowledge Graph Querier is connected (simulated).")

    def _initialize_document_store(self, primary_doc_path: Optional[str], load_readme: bool = True):
        # (Same as before - ensures documents are loaded)
        files_to_process = []
        if load_readme:
            readme_path = os.path.join(PROJECT_ROOT, "README.md")
            if os.path.exists(readme_path): files_to_process.append(readme_path)
            else: print(f"[ResearchAssistant WARN] README.md not found at {readme_path}.")
        literature_path = primary_doc_path if primary_doc_path else DEFAULT_LITERATURE_PATH
        if os.path.exists(literature_path):
            if os.path.isfile(literature_path):
                if literature_path not in files_to_process: files_to_process.append(literature_path)
            elif os.path.isdir(literature_path):
                for filename in os.listdir(literature_path):
                    if filename.endswith(".txt"):
                        file_path = os.path.join(literature_path, filename)
                        if file_path not in files_to_process: files_to_process.append(file_path)
        else: print(f"[ResearchAssistant WARN] Literature path {literature_path} does not exist.")
        if not files_to_process: return
        all_chunks = []
        for file_path in files_to_process:
            text_content = load_text_from_file(file_path)
            if not text_content: continue
            chunk_s = 500 if "literature" in file_path.lower() else 700
            chunk_o = 100 if "literature" in file_path.lower() else 150
            chunks = chunk_text(text_content, chunk_size=chunk_s, chunk_overlap=chunk_o)
            if chunks: all_chunks.extend(chunks)
        if not all_chunks: return
        chunk_embeddings = self.embedding_service.get_embeddings(all_chunks)
        self.vector_store.add_documents(all_chunks, chunk_embeddings)
        print(f"[ResearchAssistant INFO] Document store initialized with {self.vector_store.get_document_count()} total chunks for RAG.")


    def _mock_llm_call(self, prompt_type: str, query_or_observation: str, context_chunks: Optional[List[str]] = None, scenario_params_str: Optional[str]=None, sim_output_str: Optional[str]=None) -> Any:
        """Simulates LLM call. `prompt_type` can be 'rag_query', 'literature_summary', 'hypothesis_generation', or 'scenario_interpretation'."""
        print(f"\n[ResearchAssistant DEBUG] Mock LLM Call (Type: {prompt_type}):")
        context_str_lower = " ".join(context_chunks if context_chunks else []).lower()
        input_lower = query_or_observation.lower()

        if prompt_type == "literature_summary":
            # ... (same logic as before)
            if not context_chunks: return f"No relevant literature snippets found for '{query_or_observation}'. (Mocked LLM)"
            summary_parts = []
            if "sediment" in input_lower and "sediment" in context_str_lower:
                summary_parts.append("Literature suggests dam construction significantly impacts sediment load in the Yangtze.")
            if "wetland" in input_lower and ("dongting" in context_str_lower or "wetland" in context_str_lower):
                summary_parts.append("Studies on Dongting Lake indicate wetland area changes due to reclamation and hydrological alterations.")
            if "water quality" in input_lower and ("nutrient" in context_str_lower or "pollution" in context_str_lower):
                summary_parts.append("Nutrient pollution (N, P) is a concern for Middle Yangtze water quality.")
            if not summary_parts: return f"Found literature snippets for '{query_or_observation}', but content seems diverse. (Mocked LLM for summary)"
            return " ".join(summary_parts) + " (Simulated Literature Summary from LLM)"

        elif prompt_type == "hypothesis_generation":
            # This is handled by hypothesis_generator's own mock. This path is more for a generic LLM call.
            return generate_hypotheses_from_observation(query_or_observation, num_hypotheses=1)

        elif prompt_type == "scenario_interpretation":
            interpretation = f"Interpreting Scenario (mocked): Parameters '{scenario_params_str}' led to output '{sim_output_str}'. "
            if scenario_params_str and "-20" in scenario_params_str and "rainfall" in scenario_params_str: # Example check
                interpretation += "A 20% reduction in rainfall, as simulated, would likely lead to reduced streamflow and potential drought stress on wetlands, consistent with the simulated output. Further analysis of specific model outputs is needed."
            else:
                interpretation += "The simulated changes suggest potential impacts on X and Y, requiring careful consideration for decision-making."
            return interpretation + " (Simulated AI Interpretation)"

        # Default RAG query handling
        if "yangtze river" in input_lower or "changjiang" in input_lower:
            if "yangtze river" in context_str_lower or "changjiang" in context_str_lower:
                 return "Based on the provided documents, the Yangtze River (Changjiang) is a significant area of study. (Simulated LLM/RAG)"
        elif "platform" in input_lower and "modules" in input_lower:
            if "modules" in context_str_lower:
                return "The platform comprises several modules including Data Management, etc. (Simulated LLM/RAG)"

        if context_chunks:
            return f"Context found: '{context_chunks[0][:70]}...'. For your query '{query_or_observation}', specific details require a more advanced LLM. (Simulated)"
        return f"No specific context found for '{query_or_observation}'. My knowledge is limited. (Simulated LLM - no context)"


    def query_llm_with_rag(self, user_query: str) -> Dict[str, Any]:
        # ... (same as before)
        print(f"[ResearchAssistant RAG] Processing query: '{user_query}'")
        query_embedding = self.embedding_service.get_embedding(user_query)
        relevant_chunks_with_scores = self.vector_store.similarity_search(query_embedding, top_k=3)
        retrieved_texts = [text for text, score in relevant_chunks_with_scores]
        llm_answer = self._mock_llm_call(prompt_type="rag_query", query_or_observation=user_query, context_chunks=retrieved_texts)
        confidence = 0.70 if retrieved_texts else 0.30
        return {"query": user_query, "answer": llm_answer, "confidence": confidence,
                "source": "RAG Pipeline (Simulated LLM)",
                "debug_info": {"rag_context_chunks_count": len(retrieved_texts), "rag_context_preview": [chunk[:100]+"..." for chunk in retrieved_texts]}}

    def generate_literature_summary(self, topic: str, num_snippets: int = 3) -> Dict[str, Any]:
        # ... (same as before)
        print(f"[ResearchAssistant LitSum] Generating summary for topic: '{topic}'")
        topic_embedding = self.embedding_service.get_embedding(topic)
        relevant_chunks_with_scores = self.vector_store.similarity_search(topic_embedding, top_k=num_snippets)
        retrieved_texts = [text for text, score in relevant_chunks_with_scores]
        if not retrieved_texts:
            return {"query": topic, "answer": f"No literature snippets found for '{topic}'.", "confidence": 0.1,
                    "source": "Literature Summary (No Data)", "debug_info": {"retrieved_snippets_count": 0}}
        summary = self._mock_llm_call(prompt_type="literature_summary", query_or_observation=topic, context_chunks=retrieved_texts)
        return {"query": topic, "answer": summary, "confidence": 0.6,
                "source": "Automated Literature Summary (Simulated LLM)",
                "debug_info": {"retrieved_snippets_count": len(retrieved_texts), "snippets_preview": [chunk[:100]+"..." for chunk in retrieved_texts]}}

    def trigger_hypothesis_generation(self, observation_text: str, num_hypotheses: int = 1) -> Dict[str, Any]:
        # ... (same as before)
        print(f"[ResearchAssistant HypoGen] Triggering hypothesis generation for: '{observation_text}'")
        try:
            hypotheses = generate_hypotheses_from_observation(observation_text, num_hypotheses)
            answer_text = "\n".join([f"- {h}" for h in hypotheses]) if hypotheses else "No hypotheses were generated (mocked)."
            return {"query": observation_text, "answer": answer_text, "confidence": 0.5,
                    "source": "Hypothesis Generation (Simulated LLM)",
                    "debug_info": {"num_hypotheses_requested": num_hypotheses, "num_generated": len(hypotheses)}}
        except ValueError as ve:
             return {"query": observation_text, "answer": f"Error in hypothesis generation input: {ve}", "confidence": 0.1,
                    "source": "Hypothesis Generation (Input Error)"}

    def interpret_simulation_result(self, scenario_description: str, simulated_output_text: str) -> Dict[str, Any]:
        """Generates a (mocked) AI interpretation of scenario simulation results."""
        print(f"[ResearchAssistant ScnInterpret] Interpreting scenario: '{scenario_description}' with output: '{simulated_output_text}'")

        # This mocked call doesn't use RAG context for interpretation, just the input strings.
        interpretation = self._mock_llm_call(
            prompt_type="scenario_interpretation",
            query_or_observation=scenario_description, # Pass scenario_desc as main query/topic
            scenario_params_str=scenario_description, # Specific params for the mock
            sim_output_str=simulated_output_text
        )
        return {
            "query": f"Interpretation for scenario: {scenario_description}",
            "answer": interpretation,
            "confidence": 0.55, # Simulated confidence
            "source": "Scenario Interpretation (Simulated AI)",
            "debug_info": {"scenario": scenario_description, "sim_output": simulated_output_text}
        }

    def process_query(self, query_text: str) -> Dict[str, Any]:
        print(f"[ResearchAssistant INFO] Received query: \"{query_text}\"")
        query_lower = query_text.lower()

        if "hello" in query_lower or "hi" in query_lower:
            return {"query": query_text, "answer": "Hello! Ask me about the platform, request a literature summary, hypothesis, or scenario interpretation.",
                    "confidence": 0.9, "source": "Keyword Match", "debug_info": "Keyword matched."}

        lit_summary_match = re.match(r"^(?:summarize literature on|literature summary for|review literature about)\s+(.+)$", query_text, re.IGNORECASE)
        if lit_summary_match:
            topic = lit_summary_match.group(1).strip()
            return self.generate_literature_summary(topic)

        hypothesis_match = re.match(r"^(?:generate hypothesis for|hypothesize about|formulate hypothesis for):\s*(.+)$", query_text, re.IGNORECASE)
        if hypothesis_match:
            observation = hypothesis_match.group(1).strip()
            num_hypo_match = re.search(r"generate\s+(\d+)\s+hypotheses? for:", query_lower)
            num_to_generate = int(num_hypo_match.group(1)) if num_hypo_match else 1
            return self.trigger_hypothesis_generation(observation, num_hypotheses=num_to_generate)

        # Keyword for scenario interpretation
        # Example query: "interpret scenario: {"name":"Test Scenario..."} with output: {"affected_area":"Middle Yangtze..."}"
        scenario_interpret_match = re.match(r"^interpret scenario:\s*(.+?)\s*with output:\s*(.+)$", query_text, re.IGNORECASE | re.DOTALL)
        if scenario_interpret_match:
            scenario_desc_str = scenario_interpret_match.group(1).strip()
            sim_output_str = scenario_interpret_match.group(2).strip()
            # Potentially parse these strings if they are JSON, but for mock, pass as is.
            return self.interpret_simulation_result(scenario_desc_str, sim_output_str)

        print(f"[ResearchAssistant INFO] No specific command match for '{query_text}'. Proceeding with RAG-based NLQ.")
        return self.query_llm_with_rag(query_text)


if __name__ == '__main__':
    print("--- Testing Research Assistant with RAG, LitSum, HypoGen & Scenario Interpretation (Simulated) ---")

    assistant = ResearchAssistant(document_store_path=DEFAULT_LITERATURE_PATH, load_readme=True)

    print(f"\n[Test INFO] RAG store initialized with {assistant.vector_store.get_document_count()} chunks.")

    queries = [
        "Hello assistant",
        "What is this platform about?",
        "summarize literature on sediment load in Yangtze River",
        "generate hypothesis for: Water level at Yichang station has shown a slight increasing trend.",
        'interpret scenario: {"name":"Test Scenario - Rainfall Reduction", "rainfallChangePercent":-20} with output: {"affected_area":"Middle Yangtze", "change_magnitude_percent":-16.0}',
        "What is the capital of France?"
    ]

    for q_text in queries:
        print(f"\n--- User Query: \"{q_text}\" ---")
        result = assistant.process_query(q_text)
        print(f"  Assistant Answer: {result.get('answer')}")
        if result.get('debug_info'):
             debug_info_str = str(result.get('debug_info'))
             print(f"  Debug Info: {debug_info_str[:300]}{'...' if len(debug_info_str) > 300 else ''}")

    print("\n--- Research Assistant Full Test Finished ---")
