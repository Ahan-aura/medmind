from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CaseListItem(BaseModel):
    id: str
    version: int
    learning_objective: str
    case_role: str
    title: str
    disclaimer: str

class StartAttemptRequest(BaseModel):
    case_id: str
    lang: str = "en"
    parent_attempt_id: Optional[str] = None

class StepRequest(BaseModel):
    node_id: str
    choice_id: str

class SubmitRequest(BaseModel):
    selected_answer: str
    reasoning_text: str = Field(..., max_length=2000)
    selected_evidence: List[str] = Field(..., max_length=20)
    confidence: int = Field(..., ge=0, le=100)

class CriterionResult(BaseModel):
    id: str
    description: str
    met: bool
    points: float

class SubmitResponse(BaseModel):
    attempt_id: str
    state: str
    score: float
    max_score: float
    is_correct: bool
    criteria: List[CriterionResult]
    misconceptions: List[str]
    recommended_lesson_id: Optional[str] = None

class AttemptResponse(BaseModel):
    id: str
    case_id: str
    parent_attempt_id: Optional[str] = None
    state: str
    current_node: str
    selected_answer: Optional[str] = None
    reasoning_text: Optional[str] = None
    selected_evidence: List[str] = []
    confidence: Optional[int] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    is_correct: Optional[bool] = None
    criteria_results: Optional[List[Dict[str, Any]]] = None
    misconception_tags: List[str] = []
    case_view: Dict[str, Any]
    current_node_data: Optional[Dict[str, Any]] = None
    steps_history: List[Dict[str, Any]] = []

class LessonCompleteRequest(BaseModel):
    answers: Dict[str, str]
