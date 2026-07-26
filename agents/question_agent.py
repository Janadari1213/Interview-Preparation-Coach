"""Question/Content Agent — ReAct pattern retrieve-vs-generate with role awareness and ultra-fast caching."""

import re
import random
from protocol.messages import QuestionRequest, QuestionResponse
from kb.retriever import retrieve
from models.groq_client import call_groq
from models.openrouter_client import call_openrouter


def extract_correct_answer(chunk_text: str) -> str:
    """Extract reference answer string from markdown Q&A chunk."""
    match = re.search(r'\*\*A:\*\*\s*(.+)', chunk_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return chunk_text.strip()


def extract_question_prompt(chunk_text: str) -> str:
    """Extract clean question prompt string without leaking reference answer or metadata tags."""
    # 1. Try finding **Q:** prompt string
    q_match = re.search(r'\*\*Q:\*\*\s*(.*?)(?=\*\*A:\*\*|$)', chunk_text, re.DOTALL)
    if q_match and q_match.group(1).strip():
        return q_match.group(1).strip()
    
    # 2. Try finding ## Q: header line
    header_match = re.search(r'##\s*Q:\s*(.*?)(?=\*\*Topic|\*\*Role|\*\*Difficulty|\*\*A:|$)', chunk_text, re.DOTALL)
    if header_match and header_match.group(1).strip():
        return header_match.group(1).strip()

    # 3. Fallback: remove **A:** section and metadata lines
    cleaned = re.sub(r'\*\*A:\*\*.*$', '', chunk_text, flags=re.DOTALL)
    cleaned = re.sub(r'\*\*(Topic|Role|Difficulty):\*\*.*$', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^##\s*', '', cleaned, flags=re.MULTILINE)
    return cleaned.strip()


def get_content(request: QuestionRequest) -> QuestionResponse:
    """Retrieve content chunk for role and apply fast-path or ReAct pattern.
    
    Args:
        request: QuestionRequest specifying collection, difficulty, and role.
        
    Returns:
        QuestionResponse containing question, correct_answer, and topic.
    """
    coll = request.collection
    diff = request.difficulty
    role = request.role

    # 1. Retrieve top matching chunks from Knowledge Base for role
    query = f"{role} interview question" if role else "interview question"
    retrieved_items = retrieve(collection_name=coll, query=query, top_k=5, difficulty=diff, role=role)
    
    if not retrieved_items:
        retrieved_items = retrieve(collection_name=coll, query=query, top_k=5, role=role)

    if not retrieved_items:
        return QuestionResponse(
            question=f"What are your primary technical skills and key responsibilities as a {role or 'Candidate'}?",
            correct_answer="Candidate should outline relevant technical skills, framework knowledge, and problem-solving experience.",
            topic="General"
        )

    # Random selection among matching top-5 items to vary questions across requests
    top_item = random.choice(retrieved_items)
    chunk_text = top_item["text"]
    topic = top_item.get("metadata", {}).get("topic", "General")
    correct_answer = extract_correct_answer(chunk_text)
    clean_question = extract_question_prompt(chunk_text)

    # FAST PATH: If clean_question is already a valid formatted question prompt, return immediately for sub-second speed!
    if clean_question and len(clean_question) >= 10 and not clean_question.startswith("["):
        return QuestionResponse(
            question=clean_question,
            correct_answer=correct_answer,
            topic=topic
        )

    # Fallback ReAct Step if chunk is raw or unformatted
    react_system = (
        "You are a ReAct Content Evaluation Agent. "
        "Analyze the retrieved text chunk and decide if it is clear to present directly to a user, "
        "or if it needs light rewriting for clarity into a natural question format. "
        "Respond strictly with either 'DECISION: AS_IS' or 'DECISION: REWRITE'."
    )
    react_prompt = f"Retrieved Chunk:\n{clean_question}"
    react_decision = call_groq(prompt=react_prompt, system=react_system)

    should_rewrite = "REWRITE" in react_decision.upper()

    if should_rewrite and not react_decision.startswith("[Groq Error]"):
        rewrite_system = (
            "You are a Question Formatting Assistant. "
            "Rephrase the following retrieved interview prompt into a natural, clear question or scenario. "
            "Do NOT change the underlying technical core concept or answer requirements."
        )
        question_text = call_openrouter(prompt=f"Text: {clean_question}", system=rewrite_system)
        if question_text.startswith("[OpenRouter Error]"):
            question_text = clean_question
    else:
        question_text = clean_question

    return QuestionResponse(
        question=question_text,
        correct_answer=correct_answer,
        topic=topic
    )
