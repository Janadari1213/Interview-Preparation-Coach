"""Shared message schemas for agent-to-agent communication."""

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class RouterRequest:
    panel: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RouterResponse:
    kb_collection: str
    difficulty: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QuestionRequest:
    type: str
    collection: str
    difficulty: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QuestionResponse:
    question: str
    correct_answer: str
    topic: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserAnswer:
    type: str
    text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CoachRequest:
    question: str
    correct_answer: str
    user_answer: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CoachResponse:
    score: int
    max_score: int
    feedback: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
