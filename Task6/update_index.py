"""
Script to update the vector index with new or changed documents.
This script finds new or changed documents in the docs folder,
splits them into chunks, generates embeddings, updates the FAISS index,
and logs the process.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import hashlib


def setup_logging():
    """Setup logging configuration."""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    return logging.getLogger(__name__)


def get_file_hash(filepath):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def load_existing_hashes(index_dir="./vector_store"):
    """Load hashes of previously processed files."""
    hash_file = os.path.join(index_dir, "file_hashes.json")
    if os.path.exists(hash_file):
        with open(hash_file, 'r') as f:
            return json.load(f)
    return {}


def save_hashes(hashes, index_dir="./vector_store"):
    """Save hashes of processed files."""
    os.makedirs(index_dir, exist_ok=True)
    hash_file = os.path.join(index_dir, "file_hashes.json")
    with open(hash_file, 'w') as f:
        json.dump(hashes, f)


def find_new_or_changed_files(docs_dir="../Task6/docs", index_dir="./vector_store"):
    """Find new or changed files in the docs directory."""
    existing_hashes = load_existing_hashes(index_dir)
    logger = logging.getLogger(__name__)
    logger.info(f"Loaded existing hashes: {len(existing_hashes)} entries")

    new_or_changed_files = []

    for file_path in Path(docs_dir).glob("**/*.txt"):
        file_hash = get_file_hash(file_path)
        logger.info(f"Checking file: {file_path}, hash: {file_hash}")
        if str(file_path) not in existing_hashes or existing_hashes[str(file_path)] != file_hash:
            logger.info(f"File changed or new: {file_path}")
            new_or_changed_files.append(file_path)
            existing_hashes[str(file_path)] = file_hash
        else:
            logger.info(f"File unchanged: {file_path}")

    save_hashes(existing_hashes, index_dir)
    return new_or_changed_files


def update_vector_index():
    """
    Updates the vector index with new or changed documents.
    """
    logger = setup_logging()
    start_time = datetime.now()
    
    logger.info(f"Starting index update at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Path to docs folder
    docs_path = "../Task6/docs"
    index_path = "./vector_store"
    
    # Check if docs folder exists
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"Docs folder not found at {docs_path}")

    # Initialize the embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    # Text splitter to chunk documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    
    # Find new or changed files
    new_files = find_new_or_changed_files(docs_path, index_path)
    
    if not new_files:
        logger.info("No new or changed files found. Exiting.")
        end_time = datetime.now()
        logger.info(f"Index update completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("Total processing time: {}".format(end_time - start_time))
        return
    
    logger.info(f"Found {len(new_files)} new or changed files: {[str(f) for f in new_files]}")
    
    # Prepare to store new chunks
    new_texts = []
    new_metadatas = []
    
    # Process new files
    for file_path in new_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Create a document with metadata about the source
            doc = {
                "content": content,
                "metadata": {"source": str(file_path)}
            }
            
            # Split the content into chunks
            chunks = text_splitter.split_text(content)
            
            for chunk in chunks:
                new_texts.append(chunk)
                new_metadatas.append({"source": str(file_path)})
        
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            continue
    
    # Load the existing vector store if it exists
    if os.path.exists(index_path):
        vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        logger.info(f"Loaded existing vector store from {index_path}")
        
        # Add new vectors to the existing index
        if new_texts:
            vector_store.add_texts(new_texts, new_metadatas)
            logger.info(f"Added {len(new_texts)} new chunks to the existing index")
    else:
        # Create a new index if none exists
        if new_texts:
            vector_store = FAISS.from_texts(
                texts=new_texts,
                embedding=embeddings,
                metadatas=new_metadatas
            )
            logger.info(f"Created new vector store with {len(new_texts)} chunks")
        else:
            logger.info("No new chunks to add and no existing index found.")
            return
    
    # Save the updated vector store
    vector_store.save_local(index_path)
    
    # Log final statistics
    index_size = len(vector_store.docstore._dict)
    end_time = datetime.now()
    
    logger.info(f"Index update completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Number of new chunks added: {len(new_texts)}")
    logger.info(f"Final index size: {index_size} chunks")
    logger.info("Total processing time: {}".format(end_time - start_time))


if __name__ == "__main__":
    update_vector_index()