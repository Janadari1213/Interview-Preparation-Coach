"""Router Agent — Decides KB collection and target difficulty level based on interview panel."""

import re
from protocol.messages import RouterRequest, RouterResponse
from models.groq_client import call_groq


def route(request: RouterRequest) -> RouterResponse:
    """Route interview request to appropriate collection and difficulty level.
    
    Args:
        request: RouterRequest containing the target panel name.
        
    Returns:
        RouterResponse with kb_collection and difficulty.
    """
    panel = request.panel.lower().strip()
    
    # Deterministic base collection mapping fallback
    panel_map = {
        "practice_questions": "technical_qa",
        "how_to_face_interview": "interview_tips",
        "connect_with_experts": "networking_advice"
    }
    fallback_collection = panel_map.get(panel, "technical_qa")
    fallback_difficulty = "medium"

    system_prompt = (
        "You are a Router Agent for an Interview Preparation system. "
        "Based on the panel name, select the KB collection and difficulty level. "
        "Collections: 'technical_qa', 'interview_tips', 'networking_advice'. "
        "Difficulties: 'easy', 'medium', 'hard' (difficulty is primary for technical_qa). "
        "Format output strictly as JSON or key-value: COLLECTION=<name>, DIFFICULTY=<level>"
    )
    user_prompt = f"Panel Name: '{panel}'. Base collection hint: '{fallback_collection}'."

    llm_output = call_groq(prompt=user_prompt, system=system_prompt)

    # Defensive parsing of LLM response
    collection = fallback_collection
    difficulty = fallback_difficulty

    if llm_output and not llm_output.startswith("[Groq Error]"):
        # Match COLLECTION
        coll_match = re.search(r'COLLECTION\s*=\s*(technical_qa|interview_tips|networking_advice)', llm_output, re.IGNORECASE)
        if coll_match:
            collection = coll_match.group(1).lower()

        # Match DIFFICULTY
        diff_match = re.search(r'DIFFICULTY\s*=\s*(easy|medium|hard)', llm_output, re.IGNORECASE)
        if diff_match:
            difficulty = diff_match.group(1).lower()

    return RouterResponse(
        kb_collection=collection,
        difficulty=difficulty
    )
