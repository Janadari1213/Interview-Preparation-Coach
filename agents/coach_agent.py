"""Coach Agent — Evaluates candidate answers using two-step draft and self-critique reflection."""

import re
from protocol.messages import CoachRequest, CoachResponse
from models.openrouter_client import call_openrouter


def parse_score(llm_output: str, fallback_score: int = 7) -> int:
    """Extract integer score out of 10 from LLM response text."""
    score_match = re.search(r'SCORE:\s*(\d+)', llm_output, re.IGNORECASE)
    if not score_match:
        score_match = re.search(r'(\d+)\s*/\s*10', llm_output)
    if score_match:
        try:
            val = int(score_match.group(1))
            return max(0, min(10, val))
        except ValueError:
            pass
    return fallback_score


def parse_feedback(llm_output: str) -> str:
    """Extract feedback text from LLM response."""
    feedback_match = re.search(r'FEEDBACK:\s*(.+)', llm_output, re.IGNORECASE | re.DOTALL)
    if feedback_match:
        return feedback_match.group(1).strip()
    return llm_output.strip()


def evaluate(request: CoachRequest) -> CoachResponse:
    """Evaluate candidate answer using draft evaluation followed by self-critique reflection.
    
    Args:
        request: CoachRequest containing question, correct_answer, and user_answer.
        
    Returns:
        CoachResponse with score (0-10), max_score (10), and detailed feedback.
    """
    q = request.question
    ref_ans = request.correct_answer
    user_ans = request.user_answer

    # Step 1: Draft Evaluation
    draft_system = (
        "You are an expert technical interview coach. Evaluate the candidate's answer against the reference answer. "
        "Focus on whether key concepts are present rather than exact wording matches. "
        "Output format strictly:\n"
        "SCORE: <number between 0 and 10>\n"
        "FEEDBACK: <2-3 constructive feedback sentences>"
    )
    draft_prompt = (
        f"Question: {q}\n"
        f"Reference Answer: {ref_ans}\n"
        f"Candidate Answer: {user_ans}"
    )

    draft_output = call_openrouter(prompt=draft_prompt, system=draft_system)
    draft_score = parse_score(draft_output, fallback_score=7)

    # Step 2: Self-Critique Reflection Step
    critique_system = (
        "You are a Senior Evaluation Reviewer. Critique your own initial draft evaluation for fairness. "
        "Reflect on whether you penalized different wording for correct concepts, or were overly harsh/generous. "
        "Output your final revised evaluation strictly as:\n"
        "FINAL_SCORE: <number between 0 and 10>\n"
        "FINAL_FEEDBACK: <revised, highly encouraging and specific feedback>"
    )
    critique_prompt = (
        f"Original Question: {q}\n"
        f"Reference Answer: {ref_ans}\n"
        f"Candidate Answer: {user_ans}\n"
        f"Draft Score: {draft_score}/10\n"
        f"Draft Evaluation Output:\n{draft_output}"
    )

    final_output = call_openrouter(prompt=critique_prompt, system=critique_system)
    
    if final_output and not final_output.startswith("[OpenRouter Error]"):
        score_match = re.search(r'FINAL_SCORE:\s*(\d+)', final_output, re.IGNORECASE)
        final_score = int(score_match.group(1)) if score_match else parse_score(final_output, fallback_score=draft_score)
        
        feedback_match = re.search(r'FINAL_FEEDBACK:\s*(.+)', final_output, re.IGNORECASE | re.DOTALL)
        final_feedback = feedback_match.group(1).strip() if feedback_match else parse_feedback(final_output)
    else:
        final_score = draft_score
        final_feedback = parse_feedback(draft_output)

    return CoachResponse(
        score=final_score,
        max_score=10,
        feedback=final_feedback
    )
