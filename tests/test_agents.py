"""End-to-end test suite for agent flow and orchestrator interaction."""

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.orchestrator import InterviewOrchestrator


def test_end_to_end_agent_flow():
    """Execute end-to-end multi-agent interview cycle."""
    print("==========================================================")
    print("           END-TO-END AGENT ORCHESTRATION TEST            ")
    print("==========================================================")

    # 1. Instantiate Orchestrator
    orchestrator = InterviewOrchestrator()

    # 2. Start Panel
    panel_name = "practice_questions"
    print(f"\n[1] Starting Panel: '{panel_name}'...")
    question_res = orchestrator.start_panel(panel_name)

    print("\n--- Question Response Message ---")
    print(f"Topic:    {question_res.topic}")
    print(f"Question:\n{question_res.question}")
    print("---------------------------------")

    # 3. Submit Sample (Deliberately Imperfect) Candidate Answer
    sample_user_answer = (
        "Polymorphism means having many forms. In code, it means we can call a function "
        "and different objects execute it differently based on their class definition."
    )
    print(f"\n[2] Submitting Candidate Answer:\n\"{sample_user_answer}\"")

    coach_res = orchestrator.submit_answer(sample_user_answer)

    print("\n--- Coach Response Message ---")
    print(f"Score:    {coach_res.score} / {coach_res.max_score}")
    print(f"Feedback: {coach_res.feedback}")
    print("------------------------------")

    # 4. Get Summary Statistics
    summary = orchestrator.get_summary()
    print("\n--- Session Summary Statistics ---")
    print(f"Questions Asked: {summary['questions_asked']}")
    print(f"Total Score:     {summary['running_score']}")
    print(f"Average Score:   {summary['average_score']}")
    print("==========================================================\n")


if __name__ == "__main__":
    test_end_to_end_agent_flow()
