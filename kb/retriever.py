"""Retriever module: Queries Chroma DB collections and returns top matching chunks with metadata."""

from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions


def retrieve(collection_name: str, query: str, top_k: int = 1, difficulty: str = None, role: str = None) -> list[dict]:
    """Retrieve top-k matching documents from a Chroma DB collection.
    
    Args:
        collection_name: Name of Chroma collection ('technical_qa', 'interview_tips', 'networking_advice').
        query: Search query text.
        top_k: Number of results to return.
        difficulty: Optional difficulty filter ('easy', 'medium', 'hard').
        role: Optional role filter ('Software Engineer', 'Data Analyst', 'Product Manager', 'UX Designer').
        
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

    # Build filter if difficulty / role provided
    where_conditions = []
    if role and collection_name == "technical_qa":
        where_conditions.append({"role": role})
    if difficulty and collection_name == "technical_qa":
        where_conditions.append({"difficulty": difficulty.lower()})

    if len(where_conditions) == 1:
        where_filter = where_conditions[0]
    elif len(where_conditions) > 1:
        where_filter = {"$and": where_conditions}
    else:
        where_filter = None

    # Execute query
    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter
        )
    except Exception:
        # Fallback to role-only filter if difficulty combo yields zero or error
        fallback_where = {"role": role} if role and collection_name == "technical_qa" else None
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=fallback_where
        )

    retrieved = []
    if results and results.get("documents") and results["documents"][0]:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
        distances = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

        for doc, meta, dist in zip(docs, metas, distances):
            sim_score = max(0.0, 1.0 - float(dist)) if dist is not None else 1.0
            retrieved.append({
                "text": doc,
                "metadata": meta,
                "score": round(sim_score, 4),
                "similarity": round(sim_score, 4)
            })

    return retrieved
