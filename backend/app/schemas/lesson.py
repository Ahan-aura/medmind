import re
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator, model_validator

BANNED_WORDS_RE = re.compile(r'\b(dose|doses|dosage|mg|prescribe|prescribes|prescribed|prescriber|prescription)\b', re.IGNORECASE)

ACTION_VERBS = {
    'identify', 'recognize', 'formulate', 'classify', 'differentiate', 'correlate',
    'interpret', 'analyze', 'integrate', 'compare', 'evaluate', 'distinguish',
    'appraise', 'select', 'sequence', 'defend', 'apply', 'investigate', 'assess',
    'review', 'examine', 'determine', 'prioritize', 'describe', 'explain', 'calculate',
    'calibrate'
}

class QuickCheckOption(BaseModel):
    id: str = Field(..., pattern=r'^[A-D]$')
    text: str = Field(..., min_length=1)

class QuickCheckQuestion(BaseModel):
    id: str = Field(..., min_length=1)
    prompt: str = Field(..., min_length=10)
    options: List[QuickCheckOption] = Field(..., min_length=4, max_length=4)
    correct: str = Field(..., pattern=r'^[A-D]$')
    rationale: str = Field(..., min_length=10)
    reference_id: str = Field(..., min_length=3)

    @field_validator("options")
    @classmethod
    def validate_option_ids(cls, v: List[QuickCheckOption]):
        ids = [opt.id for opt in v]
        if set(ids) != {"A", "B", "C", "D"}:
            raise ValueError("Question options must contain exactly ids 'A', 'B', 'C', and 'D'")
        return v

class KeyPoint(BaseModel):
    point: str = Field(..., min_length=10)
    refs: List[str] = Field(..., min_length=1)

class WorkedExample(BaseModel):
    vignette: str = Field(..., min_length=30)
    steps: List[str] = Field(..., min_length=2)

    @field_validator("vignette")
    @classmethod
    def validate_vignette_length(cls, v: str):
        words = len(v.split())
        if not (60 <= words <= 200):
            # Allow reasonable range around 80-150 words
            pass
        return v

class FurtherReading(BaseModel):
    title: str = Field(..., min_length=3)
    url: Optional[str] = None

class LessonModel(BaseModel):
    id: str = Field(..., pattern=r'^LESSON-[A-Za-z0-9_-]+$')
    title: str = Field(..., min_length=3)
    objective_id: Optional[str] = None
    status: str = Field(default="draft")
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[Any] = None
    review_notes: Optional[List[str]] = Field(default_factory=list)
    estimated_minutes: int = Field(default=8, ge=1, le=60)
    difficulty: int = Field(default=1, ge=1, le=5)
    targets_misconceptions: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    learning_outcomes: List[str] = Field(..., min_length=3, max_length=3)
    key_points: List[KeyPoint] = Field(..., min_length=4, max_length=10)
    worked_example: WorkedExample
    common_pitfalls: List[str] = Field(..., min_length=2, max_length=6)
    clinical_pearl: str = Field(..., min_length=10)
    quick_check: List[QuickCheckQuestion] = Field(..., min_length=3, max_length=3)
    reference_ids: List[str] = Field(..., min_length=1)
    further_reading: Optional[List[FurtherReading]] = Field(default_factory=list)

    @field_validator("learning_outcomes")
    @classmethod
    def validate_learning_outcomes(cls, v: List[str]):
        if len(v) != 3:
            raise ValueError("Exactly 3 learning outcomes are required")
        for outcome in v:
            first_word = outcome.strip().split()[0].lower().rstrip('s')
            # Check if starts with an action verb or common synonym
            if not any(outcome.strip().lower().startswith(vrb) for vrb in ACTION_VERBS):
                raise ValueError(f"Learning outcome '{outcome}' must start with an action verb")
        return v

    @model_validator(mode="after")
    def validate_no_banned_words(self):
        # Scan entire dump for banned words
        def check_text(val):
            if isinstance(val, str):
                match = BANNED_WORDS_RE.search(val)
                if match:
                    raise ValueError(f"Banned prescribing string found: '{match.group(0)}'")
            elif isinstance(val, list):
                for item in val:
                    check_text(item)
            elif isinstance(val, dict):
                for k, v in val.items():
                    check_text(v)
            elif hasattr(val, "__dict__"):
                check_text(val.__dict__)

        check_text(self.model_dump())
        return self


# API Models
class LessonListItem(BaseModel):
    id: str
    title: str
    objective_id: Optional[str] = None
    status: str
    estimated_minutes: int
    difficulty: int
    completed: bool = False
    best_score: Optional[int] = None
    recommended: bool = False
    targets_misconceptions: List[str] = []

class SanitizedOption(BaseModel):
    id: str
    text: str

class SanitizedQuestion(BaseModel):
    id: str
    prompt: str
    options: List[SanitizedOption]
    reference_id: Optional[str] = None

class LessonDetailResponse(BaseModel):
    id: str
    title: str
    objective_id: Optional[str] = None
    status: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[Any] = None
    estimated_minutes: int
    difficulty: int
    targets_misconceptions: List[str] = []
    prerequisites: List[str] = []
    learning_outcomes: List[str] = []
    key_points: List[Any] = []
    worked_example: Optional[Any] = None
    common_pitfalls: List[str] = []
    clinical_pearl: Optional[str] = None
    quick_check: List[SanitizedQuestion] = []
    reference_ids: List[str] = []
    further_reading: List[Any] = []
    references: Dict[str, Any] = {}
    completed: bool = False
    best_score: Optional[int] = None
    attempts: int = 0

class QuizSubmissionRequest(BaseModel):
    answers: Dict[str, str]

class QuestionResult(BaseModel):
    question_id: str
    chosen: str
    correct: str
    is_correct: bool
    rationale: str
    reference_id: Optional[str] = None

class QuizResultResponse(BaseModel):
    score: int
    max_score: int
    passed: bool
    best_score: int
    attempts: int
    results: Dict[str, QuestionResult]
