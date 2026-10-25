from pydantic import BaseModel, Field
from typing import List, Optional

class Citation(BaseModel):
    ref_id: str
    supports: str

class Feedback(BaseModel):
    what_you_got_right: List[str]
    what_needs_work: List[str]
    why_it_matters: str
    evidence_links: List[Citation] = Field(min_length=1)
    reflection_prompt: str
    next_step: str
    uncertainty_note: str

class FeedbackResponse(BaseModel):
    id: str
    attempt_id: str
    source: str  # 'llm' or 'fallback'
    payload: Feedback
    citations_valid: Optional[bool] = None
    fallback_reason: Optional[str] = None
    model: Optional[str] = None
    latency_ms: Optional[int] = None
