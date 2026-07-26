"""Ingestion script: Reads KB markdown files, parses into chunks by '## ' headings,
embeds using sentence-transformers/all-MiniLM-L6-v2, and stores into 3 Chroma collections.
"""

import re
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions


def parse_markdown_chunks(file_path: Path) -> list[dict]:
    """Parse a markdown file into chunks split by '## ' headings."""
    content = file_path.read_text(encoding="utf-8")
    filename = file_path.name
    
    # Split content on lines starting with '## '
    raw_sections = re.split(r'(?:\r?\n|^)(?=## )', content)
    chunks = []

    for sec in raw_sections:
        sec_str = sec.strip()
        if not sec_str:
            continue
        
        # Ensure it starts with ## 
        if not sec_str.startswith("## "):
            sec_str = "## " + sec_str

        # Extract topic if present
        topic_match = re.search(r'\*\*Topic:\*\*\s*(.+)', sec_str, re.IGNORECASE)
        if topic_match:
            topic = topic_match.group(1).strip()
        else:
            # Fallback topic from filename
            topic = file_path.stem.replace("_questions", "").replace("_", " ").title()

        # Extract difficulty if present (technical_qa)
        diff_match = re.search(r'\*\*Difficulty:\*\*\s*(easy|medium|hard)', sec_str, re.IGNORECASE)
        if diff_match:
            difficulty = diff_match.group(1).lower().strip()
        else:
            difficulty = "medium"

        metadata = {
            "topic": topic,
            "difficulty": difficulty,
            "source": filename
        }

        chunks.append({
            "text": sec_str,
            "metadata": metadata
        })

    return chunks


def ingest():
    """Ingest markdown files from kb/documents/ into Chroma collections."""
    kb_dir = Path(__file__).parent
    docs_dir = kb_dir / "documents"
    chroma_db_dir = kb_dir / "chroma_db"

    # Initialize Chroma persistent client
    client = chromadb.PersistentClient(path=str(chroma_db_dir))
    
    # Embedding function
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collections = ["technical_qa", "interview_tips", "networking_advice"]
    summary = {}

    for collection_name in collections:
        subfolder = docs_dir / collection_name
        if not subfolder.exists():
            print(f"Warning: subfolder {subfolder} does not exist.")
            continue

        # Reset collection if exists for clean ingestion
        try:
            client.delete_collection(name=collection_name)
        except Exception:
            pass

        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_func
        )

        all_chunks = []
        md_files = list(subfolder.glob("*.md"))
        for md_file in md_files:
            file_chunks = parse_markdown_chunks(md_file)
            all_chunks.extend(file_chunks)

        if all_chunks:
            ids = [f"{collection_name}_{i}" for i in range(len(all_chunks))]
            documents = [c["text"] for c in all_chunks]
            metadatas = [c["metadata"] for c in all_chunks]

            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

        summary[collection_name] = len(all_chunks)

    print("\n--- Ingestion Summary ---")
    for coll_name, count in summary.items():
        print(f"Collection '{coll_name}': {count} chunks loaded.")
    print("-------------------------\n")


if __name__ == "__main__":
    ingest()
