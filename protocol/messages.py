"""Protocol messages module — Typed dataclasses for agent-to-agent communication."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class RouterRequest:
    """Request sent to Router Agent to determine target collection and difficulty."""
    panel: str
    user_query: Optional[str] = None
    role: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "panel": self.panel,
            "user_query": self.user_query,
            "role": self.role
        }


@dataclass
class RouterResponse:
    """Response returned from Router Agent."""
    kb_collection: str
    difficulty: Optional[str] = None
    reasoning: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kb_collection": self.kb_collection,
            "difficulty": self.difficulty,
            "reasoning": self.reasoning
        }


@dataclass
class QuestionRequest:
    """Request sent to Question Agent to retrieve or generate question content."""
    type: str  # 'get_content' or 'generate'
    collection: str
    difficulty: Optional[str] = None
    role: Optional[str] = None
    topic: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "collection": self.collection,
            "difficulty": self.difficulty,
            "role": self.role,
            "topic": self.topic
        }


@dataclass
class QuestionResponse:
    """Response returned from Question Agent containing question prompt and reference answer."""
    question: str
    correct_answer: str
    topic: str
    source_file: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "correct_answer": self.correct_answer,
            "topic": self.topic,
            "source_file": self.source_file
        }


@dataclass
class UserAnswer:
    """Container for candidate's submitted answer text."""
    user_answer_text: str

    def to_dict(self) -> Dict[str, Any]:
        return {"user_answer_text": self.user_answer_text}


@dataclass
class CoachRequest:
    """Request sent to Coach Agent to evaluate user answer against reference answer."""
    question: str
    correct_answer: str
    user_answer: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "correct_answer": self.correct_answer,
            "user_answer": self.user_answer
        }


@dataclass
class CoachResponse:
    """Response returned from Coach Agent containing score out of 10 and qualitative feedback."""
    score: int
    max_score: int = 10
    feedback: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "max_score": self.max_score,
            "feedback": self.feedback
        }
