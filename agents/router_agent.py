"""Router Agent — Maps user panel & query to target knowledge collection and difficulty."""

from protocol.messages import RouterRequest, RouterResponse
from models.groq_client import call_groq


def route(request: RouterRequest) -> RouterResponse:
    """Determine target Chroma collection and difficulty rating for a given panel request.
    
    Args:
        request: RouterRequest containing panel name, optional user query, and role.
        
    Returns:
        RouterResponse containing kb_collection, difficulty, and routing reasoning.
    """
    panel = request.panel.lower() if request.panel else ""

    # Direct panel mapping
    if "practice" in panel or "question" in panel:
        target_collection = "technical_qa"
    elif "face" in panel or "technique" in panel or "how_to" in panel:
        target_collection = "interview_tips"
    elif "connect" in panel or "expert" in panel or "networking" in panel:
        target_collection = "networking_advice"
    else:
        target_collection = "technical_qa"

    # For technical_qa, call Groq to decide dynamic difficulty rating
    if target_collection == "technical_qa":
        system_prompt = (
            "You are a Router Agent for an Interview Preparation system. "
            "Determine the target difficulty level ('easy', 'medium', or 'hard') "
            "for an interview question. Respond strictly in JSON format: "
            '{"difficulty": "easy"|"medium"|"hard", "reasoning": "brief explanation"}'
        )
        user_prompt = f"Panel: {request.panel}, Query: {request.user_query or 'General practice'}, Role: {request.role or 'Software Engineer'}"
        
        try:
            llm_res = call_groq(prompt=user_prompt, system=system_prompt)
            if "easy" in llm_res.lower():
                diff = "easy"
            elif "hard" in llm_res.lower():
                diff = "hard"
            else:
                diff = "medium"
            reason = f"LLM Routing: {llm_res}"
        except Exception:
            diff = "medium"
            reason = "Fallback default routing"
    else:
        diff = None
        reason = f"Direct panel route to '{target_collection}'"

    return RouterResponse(
        kb_collection=target_collection,
        difficulty=diff,
        reasoning=reason
    )
