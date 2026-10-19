from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import User
from app.schemas.progress import LearnerProgressResponse
from app.security import get_current_user
from app.services.analytics import get_learner_progress

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("/me", response_model=LearnerProgressResponse)
def get_my_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    data = get_learner_progress(db, current_user)
    return LearnerProgressResponse(**data)
