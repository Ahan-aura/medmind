from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.models import Case
from app.schemas.case import CaseListItem
from app.services.case_engine import student_view
from app.security import get_current_user

router = APIRouter(prefix="/cases", tags=["cases"])

@router.get("", response_model=List[CaseListItem])
@router.get("/", response_model=List[CaseListItem], include_in_schema=False)
def list_cases(db: Session = Depends(get_db)):
    cases = db.query(Case).filter(Case.is_published == True).all()
    items = []
    for c in cases:
        content = c.content or {}
        items.append(CaseListItem(
            id=c.id,
            version=c.version,
            learning_objective=c.learning_objective,
            case_role=c.case_role,
            title=c.title,
            disclaimer=content.get('disclaimer', "Educational simulation only. Not medical advice.")
        ))
    return items

@router.get("/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    c = db.query(Case).filter(Case.id == case_id, Case.is_published == True).first()
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    return student_view(c.content)
