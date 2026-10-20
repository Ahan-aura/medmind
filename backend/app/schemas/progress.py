from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ObjectiveProgress(BaseModel):
    learning_objective: str
    initial_score: Optional[float] = None
    initial_max: Optional[float] = None
    reassessment_score: Optional[float] = None
    reassessment_max: Optional[float] = None
    delta: Optional[float] = None
    criteria_newly_met: List[str] = []
    initial_attempt_id: Optional[str] = None
    reassessment_attempt_id: Optional[str] = None

class CalibrationPoint(BaseModel):
    confidence_bin: int  # 20, 40, 60, 80, 100
    accuracy: float
    count: int

class MisconceptionItem(BaseModel):
    id: str
    name: str
    times_seen: int
    last_seen_at: Optional[str] = None

class LearnerProgressResponse(BaseModel):
    user_id: str
    display_name: str
    objectives: List[ObjectiveProgress]
    calibration: List[CalibrationPoint]
    calibration_summary: Dict[str, int]  # {'overconfident': x, 'underconfident': y, 'calibrated': z}
    misconceptions: List[MisconceptionItem]

class TeacherSummaryResponse(BaseModel):
    cohort_id: str
    cohort_name: str
    student_count: int
    has_synthetic_data: bool = False
    objective_averages: List[Dict[str, Any]]
    top_misconceptions: List[Dict[str, Any]]
    calibration_matrix: List[Dict[str, Any]]
