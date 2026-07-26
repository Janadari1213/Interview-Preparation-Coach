"""Retriever module: Queries Chroma DB collections and returns top matching chunks with metadata."""

from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions


def retrieve(collection_name: str, query: str, top_k: int = 1, difficulty: str = None) -> list[dict]:
    """Retrieve top-k matching documents from a Chroma DB collection.
    
    Args:
        collection_name: Name of Chroma collection ('technical_qa', 'interview_tips', 'networking_advice').
        query: Search query text.
        top_k: Number of results to return.
        difficulty: Optional difficulty filter ('easy', 'medium', 'hard').
        
    Returns:
        List of dicts containing 'text', 'metadata', and 'score' / 'similarity'.
    """
    kb_dir = Path(__file__).parent
    chroma_db_dir = kb_dir / "chroma_db"

    if not chroma_db_dir.exists():
        raise FileNotFoundError(f"Chroma DB directory not found at {chroma_db_dir}. Please run kb/ingest.py first.")

    client = chromadb.PersistentClient(path=str(chroma_db_dir))
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    try:
        collection = client.get_collection(
            name=collection_name,
            embedding_function=embedding_func
        )
    except Exception as e:
        raise ValueError(f"Collection '{collection_name}' not found: {e}")

    # Build filter if difficulty provided
    where_filter = None
    if difficulty and collection_name == "technical_qa":
        where_filter = {"difficulty": difficulty.lower()}

    # Execute query
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter
    )

    retrieved = []
    if results and results.get("documents") and results["documents"][0]:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
        distances = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

        for doc, meta, dist in zip(docs, metas, distances):
            # Compute cosine / distance similarity score (1 - distance for cosine/normalized distance)
            sim_score = max(0.0, 1.0 - float(dist)) if dist is not None else 1.0
            retrieved.append({
                "text": doc,
                "metadata": meta,
                "score": round(sim_score, 4),
                "similarity": round(sim_score, 4)
            })

    return retrieved
