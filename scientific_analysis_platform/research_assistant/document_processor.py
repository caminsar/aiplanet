"""
document_processor.py

Handles loading text from documents and chunking it for the RAG framework.
"""
import os
from typing import List

def load_text_from_file(filepath: str) -> str:
    """
    Loads text content from a specified file.
    Simulated: For now, this is a very basic text file reader.
    In a real scenario, this would handle various formats (PDF, DOCX, etc.)
    using libraries like PyPDF2, python-docx, Unstructured.io, etc.
    """
    print(f"[DocProcessor] Attempting to load text from: {filepath}")
    if not os.path.exists(filepath):
        print(f"[DocProcessor ERROR] File not found: {filepath}")
        return ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"[DocProcessor] Successfully loaded {len(content)} characters from {filepath}")
        return content
    except Exception as e:
        print(f"[DocProcessor ERROR] Failed to read file {filepath}: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Splits a long text into smaller chunks with some overlap.
    This is a simple character-based chunking strategy. More advanced strategies
    (e.g., sentence splitting, recursive character splitting, semantic chunking)
    would be used in a production system (e.g., using LangChain's text_splitters).

    :param text: The input text to be chunked.
    :param chunk_size: The desired maximum size of each chunk (in characters).
    :param chunk_overlap: The number of characters to overlap between consecutive chunks.
    :return: A list of text chunks.
    """
    print(f"[DocProcessor] Chunking text of length {len(text)} into chunks of size ~{chunk_size} with overlap ~{chunk_overlap}")
    if not text:
        return []

    chunks: List[str] = []
    start_index = 0
    text_length = len(text)

    while start_index < text_length:
        end_index = min(start_index + chunk_size, text_length)
        chunks.append(text[start_index:end_index])

        # Move start_index for the next chunk
        # If we are at the end, no need to advance with overlap
        if end_index == text_length:
            break

        start_index += (chunk_size - chunk_overlap)
        # Ensure start_index does not go beyond a point where a meaningful chunk can be made
        if start_index >= text_length: # Should ideally not happen if chunk_overlap < chunk_size
             break


    print(f"[DocProcessor] Produced {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    print("--- Testing Document Processor ---")

    # Create a dummy test file
    dummy_file_content = """This is the first sentence of a long document. It talks about various important topics.
Second sentence continues the discussion. We need to ensure that chunking works as expected.
The overlap should help maintain context between chunks. This is sentence three.
Sentence four provides more details. And sentence five wraps up this paragraph.

Another paragraph starts here. This is sentence six. Sentence seven is also here.
This document will be used for testing the document loading and chunking functionality
of the RAG pipeline's document processor. The goal is to break this down.
Final sentence for good measure.
"""
    dummy_filepath = "temp_test_doc.txt"
    with open(dummy_filepath, "w", encoding="utf-8") as f:
        f.write(dummy_file_content)

    # Test load_text_from_file
    print("\n1. Testing load_text_from_file:")
    loaded_content = load_text_from_file(dummy_filepath)
    if loaded_content:
        print(f"  Successfully loaded content (first 50 chars): '{loaded_content[:50]}...'")
    else:
        print("  Failed to load content.")

    loaded_content_nonexistent = load_text_from_file("nonexistent_file.txt")
    print(f"  Attempt to load non-existent file returned length: {len(loaded_content_nonexistent)}")


    # Test chunk_text
    print("\n2. Testing chunk_text:")
    if loaded_content:
        test_chunk_size = 100
        test_chunk_overlap = 20
        chunks = chunk_text(loaded_content, chunk_size=test_chunk_size, chunk_overlap=test_chunk_overlap)
        print(f"  Original length: {len(loaded_content)}, Number of chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"  Chunk {i+1} (length {len(chunk)}): '{chunk[:70]}...'")
            if i > 0: # Check overlap
                prev_chunk_end = chunks[i-1][-(test_chunk_overlap + 10):] # Approx end of prev
                current_chunk_start = chunk[:(test_chunk_overlap + 10)] # Approx start of current
                print(f"    Overlap check: Prev end snippet: '...{prev_chunk_end[-test_chunk_overlap:]}', Curr start snippet: '{current_chunk_start[:test_chunk_overlap]}'")


    # Test with empty text
    print("\n3. Testing chunk_text with empty input:")
    empty_chunks = chunk_text("")
    print(f"  Chunks from empty text: {empty_chunks} (Count: {len(empty_chunks)})")

    # Clean up dummy file
    if os.path.exists(dummy_filepath):
        os.remove(dummy_filepath)

    print("\n--- Document Processor Test Finished ---")
