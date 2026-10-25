from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import User
from app.schemas.progress import TeacherSummaryResponse
from app.security import require_teacher
from app.services.analytics import get_cohort_summary

router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.get("/cohorts/{cohort_id}/summary", response_model=TeacherSummaryResponse)
def get_cohort_analytics(
    cohort_id: str,
    teacher: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    data = get_cohort_summary(db, cohort_id)
    return TeacherSummaryResponse(**data)
