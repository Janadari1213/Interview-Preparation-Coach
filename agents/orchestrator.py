"""Orchestrator Agent — Manages interview session state and coordinates sub-agents."""

from typing import Dict, Any, List
from protocol.messages import (
    RouterRequest,
    QuestionRequest,
    QuestionResponse,
    CoachRequest,
    CoachResponse
)
from agents import router_agent
from agents import question_agent
from agents import coach_agent


class InterviewOrchestrator:
    """Session state orchestrator for the Interview Preparation Coach system."""

    def __init__(self):
        self.running_score: int = 0
        self.questions_asked: int = 0
        self.current_panel: str = None
        self.current_question: str = None
        self.current_correct_answer: str = None
        self.history: List[Dict[str, Any]] = []

    def start_panel(self, panel_name: str) -> QuestionResponse:
        """Start or switch panel, route query, and fetch appropriate question content.
        
        Args:
            panel_name: Name of interview panel ('practice_questions', 'how_to_face_interview', 'connect_with_experts').
            
        Returns:
            QuestionResponse dataclass containing question, correct_answer, and topic.
        """
        self.current_panel = panel_name
        
        # 1. Delegate to Router Agent
        router_req = RouterRequest(panel=panel_name)
        router_res = router_agent.route(router_req)

        # 2. Delegate to Question Agent
        q_req = QuestionRequest(
            type="get_content",
            collection=router_res.kb_collection,
            difficulty=router_res.difficulty
        )
        q_res = question_agent.get_content(q_req)

        # Update current state
        self.current_question = q_res.question
        self.current_correct_answer = q_res.correct_answer

        return q_res

    def submit_answer(self, user_answer_text: str) -> CoachResponse:
        """Evaluate candidate answer for current question using Coach Agent.
        
        Args:
            user_answer_text: Candidate's submitted text answer.
            
        Returns:
            CoachResponse dataclass containing score, max_score, and feedback.
        """
        if not self.current_question or not self.current_correct_answer:
            raise ValueError("No active question to answer. Please call start_panel() first.")

        # Delegate to Coach Agent
        coach_req = CoachRequest(
            question=self.current_question,
            correct_answer=self.current_correct_answer,
            user_answer=user_answer_text
        )
        coach_res = coach_agent.evaluate(coach_req)

        # Update session tracking statistics
        self.running_score += coach_res.score
        self.questions_asked += 1

        self.history.append({
            "panel": self.current_panel,
            "question": self.current_question,
            "correct_answer": self.current_correct_answer,
            "user_answer": user_answer_text,
            "score": coach_res.score,
            "max_score": coach_res.max_score,
            "feedback": coach_res.feedback
        })

        return coach_res

    def get_summary(self) -> Dict[str, Any]:
        """Return cumulative summary statistics for the interview session."""
        avg_score = (self.running_score / self.questions_asked) if self.questions_asked > 0 else 0.0
        return {
            "running_score": self.running_score,
            "questions_asked": self.questions_asked,
            "average_score": round(avg_score, 2),
            "history": self.history
        }
