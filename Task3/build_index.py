"""
Script to create a vector index from the knowledge base using embeddings.
This will create a FAISS index for the RAG bot to use for semantic search.
"""

import os
from pathlib import Path
import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def create_vector_index():
    """
    Creates a vector index from the knowledge base documents.
    """
    
    # Path to knowledge base
    knowledge_base_path = "../Task2/knowledge_base"
    
    # Check if knowledge base exists
    if not os.path.exists(knowledge_base_path):
        raise FileNotFoundError(f"Knowledge base not found at {knowledge_base_path}")
    
    # Initialize the embedding model
    # Using all-MiniLM-L6-v2 which is lightweight but effective for most tasks
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}  # Using CPU since we're using faiss-cpu
    )
    
    # Text splitter to chunk documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Splitting into chunks of ~500 characters
        chunk_overlap=50,  # Overlap to maintain context between chunks
        length_function=len,
    )
    
    # Read all text files from knowledge base
    documents = []
    for file_path in Path(knowledge_base_path).glob("**/*.txt"):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Create a document with metadata about the source
            doc = {
                "content": content,
                "metadata": {"source": str(file_path)}
            }
            documents.append(doc)
    
    print(f"Loaded {len(documents)} documents from knowledge base.")
    
    # Split documents into chunks
    texts = []
    metadatas = []
    
    for doc in documents:
        content = doc["content"]
        metadata = doc["metadata"]
        
        # Split the content into chunks
        chunks = text_splitter.split_text(content)
        
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append(metadata)
    
    print(f"Created {len(texts)} text chunks.")
    
    # Create the vector store using FAISS
    print("Creating FAISS index...")
    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )
    
    # Save the vector store locally
    vector_store.save_local("./vector_store")
    
    print("Vector index created and saved successfully!")
    print(f"Index contains {len(texts)} text chunks.")
    print(f"Embedding model used: all-MiniLM-L6-v2")
    print(f"Chunk size: 500 characters with 50 character overlap")
    
    return vector_store


if __name__ == "__main__":
    create_vector_index()