"""
Test script to verify the vector index works correctly.
This will load the index and perform a few sample queries.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def test_vector_index():
    """
    Test the created vector index by loading it and performing similarity searches.
    """
    # Initialize the same embedding model used for creating the index
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Load the vector store
    vector_store = FAISS.load_local(
        "./vector_store", 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    print("Vector index loaded successfully!")
    print(f"Number of vectors in index: {vector_store.index.ntotal}")
    
    # Perform a few sample queries
    test_queries = [
        "Who is the main villain?",  # Query for a character
        "Tell me about the spaceship technology",  # Query for technology
        "What happened in the last battle?"  # Query for an event
    ]
    
    print("\nPerforming sample queries:")
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: '{query}'")
        
        # Find similar documents
        docs = vector_store.similarity_search(query, k=3)
        
        print(f"Top {len(docs)} similar document(s):")
        for j, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            print(f"  {j}. From: {source}")
            print(f"     Preview: {content_preview}")
            print()


if __name__ == "__main__":
    test_vector_index()