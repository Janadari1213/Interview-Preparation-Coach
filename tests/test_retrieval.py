"""Retrieval evaluation script for 5 sample queries across KB collections."""

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from kb.retriever import retrieve


def test_retrieval_evaluation():
    """Evaluate retrieval performance across 5 benchmark questions."""
    eval_queries = [
        {
            "query": "What is polymorphism?",
            "collection": "technical_qa",
            "difficulty": None
        },
        {
            "query": "How does TCP differ from UDP?",
            "collection": "technical_qa",
            "difficulty": None
        },
        {
            "query": "How should I structure a behavioral answer?",
            "collection": "interview_tips",
            "difficulty": None
        },
        {
            "query": "What's a common mistake candidates make?",
            "collection": "interview_tips",
            "difficulty": None
        },
        {
            "query": "How do I message someone on LinkedIn for networking?",
            "collection": "networking_advice",
            "difficulty": None
        }
    ]

    print("==========================================================")
    print("           KB RETRIEVAL EVALUATION TEST SUITE             ")
    print("==========================================================")

    for idx, item in enumerate(eval_queries, 1):
        query = item["query"]
        coll = item["collection"]
        diff = item["difficulty"]

        results = retrieve(collection_name=coll, query=query, top_k=1, difficulty=diff)

        print(f"\n[{idx}] Query: '{query}'")
        print(f"    Collection: {coll}")
        
        if results:
            top_result = results[0]
            raw_text = top_result["text"].replace("\n", " ")
            truncated_text = (raw_text[:147] + "...") if len(raw_text) > 150 else raw_text
            score = top_result["score"]
            meta = top_result.get("metadata", {})

            print(f"    Similarity Score: {score}")
            print(f"    Source: {meta.get('source', 'N/A')} | Topic: {meta.get('topic', 'N/A')}")
            print(f"    Top Chunk: \"{truncated_text}\"")
        else:
            print("    [!] No result retrieved.")

    print("\n==========================================================")


if __name__ == "__main__":
    test_retrieval_evaluation()
