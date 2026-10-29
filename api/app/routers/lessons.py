from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from app.db import get_db
from app.models.models import Lesson, LessonProgress, ReferenceChunk, LearnerMisconception, Attempt
from app.schemas.lesson import (
    LessonListItem, LessonDetailResponse, SanitizedQuestion, SanitizedOption,
    QuizSubmissionRequest, QuizResultResponse, QuestionResult
)
from app.security import get_current_user
from app.config import settings
from app.limiter import limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/lessons", tags=["lessons"])

def get_user_lesson_limiter_key(request: Request) -> str:
    lesson_id = request.path_params.get("lesson_id", "")
    auth = request.headers.get("authorization", "")
    ip = get_remote_address(request)
    return f"{auth}:{ip}:{lesson_id}"

@router.get("", response_model=List[LessonListItem])
@router.get("/", response_model=List[LessonListItem], include_in_schema=False)
def list_lessons(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Lesson)
    if not settings.ALLOW_UNREVIEWED_CONTENT:
        query = query.filter(
            Lesson.status != "draft",
            Lesson.reviewed_by.isnot(None)
        )
    
    lessons = query.all()
    # Order lessons: LESSON-01 to LESSON-08 first, then legacy
    lessons = sorted(lessons, key=lambda l: (0 if l.id.startswith("LESSON-0") else 1, l.id))

    # User progress
    progress_map = {
        p.lesson_id: p
        for p in db.query(LessonProgress).filter(LessonProgress.user_id == current_user.id).all()
    }

    # User's recent triggered misconceptions
    learner_misc_ids = {
        lm.misconception_id
        for lm in db.query(LearnerMisconception).filter(LearnerMisconception.user_id == current_user.id).all()
    }
    recent_attempts = db.query(Attempt).filter(
        Attempt.user_id == current_user.id
    ).order_by(Attempt.created_at.desc()).limit(5).all()
    for att in recent_attempts:
        if att.misconception_tags:
            for tag in att.misconception_tags:
                learner_misc_ids.add(tag)

    results = []
    for l in lessons:
        prog = progress_map.get(l.id)
        best_score = prog.best_score if prog else None
        completed = (best_score is not None and best_score >= 2)
        
        target_miscs = l.targets_misconceptions or []
        is_recommended = bool(
            not completed and any(m in learner_misc_ids for m in target_miscs)
        )

        results.append(LessonListItem(
            id=l.id,
            title=l.title,
            objective_id=l.objective_id,
            status=l.status or "draft",
            estimated_minutes=l.estimated_minutes or 8,
            difficulty=l.difficulty or 1,
            completed=completed,
            best_score=best_score,
            recommended=is_recommended,
            targets_misconceptions=target_miscs
        ))

    return results

@router.get("/{lesson_id}")
def get_lesson(
    lesson_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if not settings.ALLOW_UNREVIEWED_CONTENT:
        if lesson.status == "draft" or not lesson.reviewed_by:
            raise HTTPException(status_code=403, detail="Unreviewed draft lessons are disabled in this environment")

    raw = lesson.raw_data or {}
    questions_source = raw.get("quick_check") or lesson.practice_questions or []

    # Sanitize questions: strip correct and rationale
    sanitized_questions = []
    for q in questions_source:
        opts = [
            SanitizedOption(id=opt.get("id"), text=opt.get("text", ""))
            for opt in q.get("options", [])
        ]
        sanitized_questions.append(SanitizedQuestion(
            id=q.get("id", ""),
            prompt=q.get("prompt") or q.get("question", ""),
            options=opts,
            reference_id=q.get("reference_id")
        ))

    # Collect reference chunks
    ref_ids = set(raw.get("reference_ids", []))
    for kp in raw.get("key_points", []):
        for r in kp.get("refs", []):
            ref_ids.add(r)
    for q in questions_source:
        if q.get("reference_id"):
            ref_ids.add(q.get("reference_id"))

    references_map = {}
    if ref_ids:
        chunks = db.query(ReferenceChunk).filter(ReferenceChunk.id.in_(ref_ids)).all()
        for chunk in chunks:
            references_map[chunk.id] = {
                "id": chunk.id,
                "title": getattr(chunk, "section", None) or chunk.source_title,
                "source_title": chunk.source_title,
                "source_url": chunk.source_url,
                "text": chunk.text,
                "key_facts": getattr(chunk, "tags", []) or []
            }

    # Progress
    prog = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()

    best_score = prog.best_score if prog else None
    completed = (best_score is not None and best_score >= 2)
    attempts = prog.attempts if prog else 0

    return {
        "id": lesson.id,
        "title": lesson.title,
        "objective_id": lesson.objective_id,
        "status": lesson.status or "draft",
        "reviewed_by": lesson.reviewed_by,
        "reviewed_at": lesson.reviewed_at.isoformat() if lesson.reviewed_at else None,
        "estimated_minutes": lesson.estimated_minutes or 8,
        "difficulty": lesson.difficulty or 1,
        "targets_misconceptions": lesson.targets_misconceptions or [],
        "prerequisites": lesson.prerequisites or [],
        "learning_outcomes": raw.get("learning_outcomes", []),
        "key_points": raw.get("key_points", []),
        "worked_example": raw.get("worked_example"),
        "common_pitfalls": raw.get("common_pitfalls", []),
        "clinical_pearl": raw.get("clinical_pearl", ""),
        "quick_check": [q.dict() for q in sanitized_questions],
        "reference_ids": list(ref_ids),
        "further_reading": raw.get("further_reading", []),
        "references": references_map,
        "completed": completed,
        "best_score": best_score,
        "attempts": attempts,
        # Legacy compatibility
        "content": lesson.content,
        "practice_questions": [q.dict() for q in sanitized_questions]
    }

@router.post("/{lesson_id}/quiz", response_model=QuizResultResponse)
@limiter.limit("3/hour", key_func=get_user_lesson_limiter_key)
def submit_quiz(
    request: Request,
    lesson_id: str,
    submission: QuizSubmissionRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    raw = lesson.raw_data or {}
    questions_source = raw.get("quick_check") or lesson.practice_questions or []
    if not questions_source:
        raise HTTPException(status_code=400, detail="Lesson has no quiz questions")

    answers = submission.answers or {}
    results = {}
    score = 0

    # Validate that every question has a valid answer
    for q in questions_source:
        q_id = q.get("id")
        if q_id not in answers:
            raise HTTPException(status_code=422, detail=f"Missing answer for question {q_id}")
        
        valid_options = {opt.get("id") for opt in q.get("options", [])}
        chosen = answers[q_id]
        if chosen not in valid_options:
            raise HTTPException(status_code=422, detail=f"Invalid option '{chosen}' for question {q_id}")

        correct = q.get("correct")
        if not correct:
            for opt in q.get("options", []):
                if opt.get("correct"):
                    correct = opt.get("id")

        is_correct = (chosen == correct)
        if is_correct:
            score += 1

        results[q_id] = QuestionResult(
            question_id=q_id,
            chosen=chosen,
            correct=correct or "",
            is_correct=is_correct,
            rationale=q.get("rationale") or q.get("explanation", ""),
            reference_id=q.get("reference_id")
        )

    max_score = len(questions_source)
    passed = (score >= 2)

    # Upsert lesson progress
    prog = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()

    now = datetime.now(timezone.utc)
    if not prog:
        prog = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            best_score=score,
            attempts=1,
            completed_at=now if passed else None,
            last_seen_at=now
        )
        db.add(prog)
    else:
        prog.attempts += 1
        prog.best_score = max(prog.best_score or 0, score)
        if passed and not prog.completed_at:
            prog.completed_at = now
        prog.last_seen_at = now

    db.commit()
    db.refresh(prog)

    return QuizResultResponse(
        score=score,
        max_score=max_score,
        passed=passed,
        best_score=prog.best_score,
        attempts=prog.attempts,
        results=results
    )
