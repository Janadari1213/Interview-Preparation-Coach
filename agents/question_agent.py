"""Question/Content Agent — ReAct pattern retrieve-vs-generate with role awareness."""

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


def get_content(request: QuestionRequest) -> QuestionResponse:
    """Retrieve content chunk for role and apply ReAct pattern to judge and optionally rephrase.
    
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

    # 2. ReAct Step: Call Groq to evaluate if chunk needs rewriting
    react_system = (
        "You are a ReAct Content Evaluation Agent. "
        "Analyze the retrieved text chunk and decide if it is clear to present directly to a user, "
        "or if it needs light rewriting for clarity into a natural question format. "
        "Respond strictly with either 'DECISION: AS_IS' or 'DECISION: REWRITE'."
    )
    react_prompt = f"Retrieved Chunk:\n{chunk_text}"
    react_decision = call_groq(prompt=react_prompt, system=react_system)

    should_rewrite = "REWRITE" in react_decision.upper()

    # 3. Execution step: If rewrite requested, rephrase with OpenRouter while keeping correct_answer intact
    if should_rewrite and not react_decision.startswith("[Groq Error]"):
        rewrite_system = (
            "You are a Question Formatting Assistant. "
            "Rephrase the following retrieved interview prompt into a natural, clear question or scenario. "
            "Do NOT change the underlying technical core concept or answer requirements."
        )
        question_text = call_openrouter(prompt=f"Text: {chunk_text}", system=rewrite_system)
        if question_text.startswith("[OpenRouter Error]"):
            question_text = chunk_text
    else:
        question_text = chunk_text

    return QuestionResponse(
        question=question_text,
        correct_answer=correct_answer,
        topic=topic
    )
