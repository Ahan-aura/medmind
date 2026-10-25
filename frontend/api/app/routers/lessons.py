from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import Lesson
from app.security import get_current_user

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/{lesson_id}")
def get_lesson(
    lesson_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
        
    return {
        "id": lesson.id,
        "title": lesson.title,
        "content": lesson.content,
        "practice_questions": lesson.practice_questions
    }
