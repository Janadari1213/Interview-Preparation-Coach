"""Retriever module: Queries Chroma DB collections and returns top matching chunks with metadata.
Includes auto-ingestion on missing DB directory and in-memory singleton caching for lightning-fast performance.
"""

from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

_CHROMA_CLIENT = None
_EMBEDDING_FUNC = None


def _get_client_and_embedding(chroma_db_dir: Path):
    """Singleton getter for PersistentClient and SentenceTransformer embedding function."""
    global _CHROMA_CLIENT, _EMBEDDING_FUNC

    if not chroma_db_dir.exists():
        print(f"[Auto-Ingest] Chroma DB directory not found at {chroma_db_dir}. Triggering auto-ingestion...")
        try:
            from kb import ingest
            ingest.ingest()
        except Exception as e:
            print(f"[Auto-Ingest Failure]: {e}")

    if _CHROMA_CLIENT is None:
        _CHROMA_CLIENT = chromadb.PersistentClient(path=str(chroma_db_dir))
    if _EMBEDDING_FUNC is None:
        _EMBEDDING_FUNC = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    return _CHROMA_CLIENT, _EMBEDDING_FUNC


def retrieve(collection_name: str, query: str, top_k: int = 1, difficulty: str = None, role: str = None) -> list[dict]:
    """Retrieve top-k matching documents from a Chroma DB collection safely and rapidly.
    
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

    try:
        client, embedding_func = _get_client_and_embedding(chroma_db_dir)
        collection = client.get_collection(
            name=collection_name,
            embedding_function=embedding_func
        )
    except Exception as e:
        print(f"[Retriever Warning] Collection '{collection_name}' access failed: {e}")
        # Try re-ingesting and re-fetching
        try:
            from kb import ingest
            ingest.ingest()
            client, embedding_func = _get_client_and_embedding(chroma_db_dir)
            collection = client.get_collection(
                name=collection_name,
                embedding_function=embedding_func
            )
        except Exception as e2:
            print(f"[Retriever Error]: {e2}")
            return []

    total_count = collection.count()
    if total_count == 0:
        return []

    safe_k = min(top_k, total_count)

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

    results = None
    # Tier 1: Try with full filter and safe_k
    try:
        results = collection.query(
            query_texts=[query],
            n_results=safe_k,
            where=where_filter
        )
    except Exception:
        results = None

    # Tier 2: Try with full filter and n_results=1
    if not results or not results.get("documents") or not results["documents"][0]:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=1,
                where=where_filter
            )
        except Exception:
            results = None

    # Tier 3: Try with role-only filter and n_results=1
    if not results or not results.get("documents") or not results["documents"][0]:
        fallback_where = {"role": role} if role and collection_name == "technical_qa" else None
        try:
            results = collection.query(
                query_texts=[query],
                n_results=1,
                where=fallback_where
            )
        except Exception:
            results = None

    # Tier 4: Ultimate fallback without any filter
    if not results or not results.get("documents") or not results["documents"][0]:
        try:
            results = collection.query(
                query_texts=[query],
                n_results=1
            )
        except Exception:
            return []

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
