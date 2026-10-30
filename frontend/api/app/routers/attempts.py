from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.limiter import limiter

from app.db import get_db
from app.models.models import (
    Attempt, AttemptStep, Case, FeedbackRecord,
    LearnerMisconception, Misconception, User, Cohort
)
from app.schemas.case import (
    StartAttemptRequest, StepRequest, SubmitRequest,
    SubmitResponse, AttemptResponse, LessonCompleteRequest
)
from app.schemas.feedback import FeedbackResponse
from app.security import get_current_user
from app.services.case_engine import require_state, student_view, take_step
from app.services.scoring import score_attempt
from app.services.misconceptions import get_recommended_lesson, MISCONCEPTIONS_REGISTRY
from app.services.rag import retrieve_references
from app.services.tutor import generate_feedback

router = APIRouter(prefix="/attempts", tags=["attempts"])

def get_user_attempt(attempt_id: str, user: User, db: Session) -> Attempt:
    attempt = db.query(Attempt).filter(Attempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.user_id == user.id or user.role == "admin":
        return attempt
    if user.role == "teacher":
        owner = db.query(User).filter(User.id == attempt.user_id).first()
        cohort = db.query(Cohort).filter(Cohort.id == owner.cohort_id).first() if owner and owner.cohort_id else None
        if cohort and cohort.teacher_id == user.id:
            return attempt
    raise HTTPException(status_code=404, detail="Attempt not found")

@router.post("", response_model=Dict[str, Any])
@router.post("/", response_model=Dict[str, Any], include_in_schema=False)
def start_attempt(
    req: StartAttemptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(Case.id == req.case_id, Case.is_published == True).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found or not published")

    if req.parent_attempt_id:
        parent = db.query(Attempt).filter(Attempt.id == req.parent_attempt_id).first()
        if not parent or parent.user_id != current_user.id:
            raise HTTPException(status_code=400, detail="Parent attempt does not belong to the current user or does not exist")
        parent_case = db.query(Case).filter(Case.id == parent.case_id).first()
        paired = parent_case.content.get('paired_case') if parent_case and parent_case.content else None
        if not paired or paired != req.case_id:
            raise HTTPException(status_code=400, detail="Case is not the paired reassessment case for this parent attempt")
        existing_reassessment = db.query(Attempt).filter(Attempt.parent_attempt_id == req.parent_attempt_id).first()
        if existing_reassessment:
            raise HTTPException(status_code=409, detail="Reassessment attempt already exists for this parent attempt")
        
    start_node = case.content.get('branching', {}).get('start', 'n_review')
    
    attempt = Attempt(
        user_id=current_user.id,
        case_id=case.id,
        parent_attempt_id=req.parent_attempt_id,
        state="STARTED",
        current_node=start_node,
        lang=req.lang or current_user.preferred_lang or "en"
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    return {
        "attempt_id": attempt.id,
        "case_id": case.id,
        "state": attempt.state,
        "current_node": attempt.current_node,
        "case_view": student_view(case.content)
    }

@router.get("/{attempt_id}", response_model=AttemptResponse)
def get_attempt(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = get_user_attempt(attempt_id, current_user, db)
    case = db.query(Case).filter(Case.id == attempt.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    # Get current node info from case
    nodes = case.content.get('branching', {}).get('nodes', [])
    current_node_data = next((n for n in nodes if n['id'] == attempt.current_node), None)
    
    steps = db.query(AttemptStep).filter(AttemptStep.attempt_id == attempt.id).order_by(AttemptStep.id.asc()).all()
    steps_history = [{"node_id": s.node_id, "choice_id": s.choice_id} for s in steps]
    
    return AttemptResponse(
        id=attempt.id,
        case_id=attempt.case_id,
        parent_attempt_id=attempt.parent_attempt_id,
        state=attempt.state,
        current_node=attempt.current_node,
        selected_answer=attempt.selected_answer,
        reasoning_text=attempt.reasoning_text,
        selected_evidence=attempt.selected_evidence or [],
        confidence=attempt.confidence,
        score=attempt.score,
        max_score=attempt.max_score,
        is_correct=attempt.is_correct,
        criteria_results=attempt.criteria_results,
        misconception_tags=attempt.misconception_tags or [],
        case_view=student_view(case.content),
        current_node_data=current_node_data,
        steps_history=steps_history
    )

@router.post("/{attempt_id}/step")
def record_step(
    attempt_id: str,
    req: StepRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = get_user_attempt(attempt_id, current_user, db)
    require_state(attempt.state, 'step')

    if req.node_id != attempt.current_node:
        raise HTTPException(
            status_code=409,
            detail=f"Requested node '{req.node_id}' does not match current attempt node '{attempt.current_node}'"
        )
    
    case = db.query(Case).filter(Case.id == attempt.case_id).first()
    next_node_id, flags, next_node = take_step(case.content, req.node_id, req.choice_id)
    
    # Save step history
    step = AttemptStep(attempt_id=attempt.id, node_id=req.node_id, choice_id=req.choice_id)
    db.add(step)
    
    attempt.current_node = next_node_id
    db.commit()
    
    return {
        "current_node": next_node_id,
        "flags": flags,
        "node_data": next_node
    }

@router.post("/{attempt_id}/submit", response_model=SubmitResponse)
def submit_decision(
    attempt_id: str,
    req: SubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = get_user_attempt(attempt_id, current_user, db)
    require_state(attempt.state, 'submit')
    
    case = db.query(Case).filter(Case.id == attempt.case_id).first()
    case_content = case.content or {}

    valid_answers = {o['id'] for o in case_content.get('options', [])}
    valid_evidence = set(case_content.get('evidence_ids') or [l['id'] for l in case_content.get('labs', [])])
    
    if req.selected_answer not in valid_answers:
        raise HTTPException(status_code=422, detail="Unknown answer option")
    if not set(req.selected_evidence) <= valid_evidence:
        raise HTTPException(status_code=422, detail="Unknown evidence item")
    
    # Score attempt deterministically
    scoring_result = score_attempt(
        case=case.content,
        answer=req.selected_answer,
        evidence=req.selected_evidence,
        reasoning=req.reasoning_text,
        confidence=req.confidence
    )
    
    # Update attempt state & fields
    attempt.selected_answer = req.selected_answer
    attempt.selected_evidence = req.selected_evidence
    attempt.reasoning_text = req.reasoning_text
    attempt.confidence = req.confidence
    attempt.is_correct = scoring_result['is_correct']
    attempt.score = scoring_result['score']
    attempt.max_score = scoring_result['max_score']
    attempt.criteria_results = scoring_result['criteria']
    attempt.misconception_tags = scoring_result['misconceptions']
    attempt.state = "SUBMITTED"
    attempt.submitted_at = datetime.now(timezone.utc)
    
    # Upsert learner misconceptions in tracking table
    for tag in scoring_result['misconceptions']:
        # Ensure tag exists in misconceptions table
        m_entry = db.query(Misconception).filter(Misconception.id == tag).first()
        if not m_entry:
            m_info = MISCONCEPTIONS_REGISTRY.get(tag, {})
            m_entry = Misconception(
                id=tag,
                name=m_info.get("name", tag),
                description=m_info.get("description", tag),
                lesson_id=m_info.get("lesson_id")
            )
            db.add(m_entry)
            db.commit()
            
        lm = db.query(LearnerMisconception).filter(
            LearnerMisconception.user_id == current_user.id,
            LearnerMisconception.misconception_id == tag
        ).first()
        if lm:
            lm.times_seen += 1
            lm.last_seen_at = datetime.now(timezone.utc)
        else:
            lm = LearnerMisconception(
                user_id=current_user.id,
                misconception_id=tag,
                times_seen=1,
                last_seen_at=datetime.now(timezone.utc)
            )
            db.add(lm)
            
    db.commit()
    
    rec_lesson = get_recommended_lesson(scoring_result['misconceptions'], case.learning_objective)
    
    return SubmitResponse(
        attempt_id=attempt.id,
        state=attempt.state,
        score=attempt.score,
        max_score=attempt.max_score,
        is_correct=attempt.is_correct,
        criteria=scoring_result['criteria'],
        misconceptions=scoring_result['misconceptions'],
        recommended_lesson_id=rec_lesson
    )

@router.post("/{attempt_id}/feedback", response_model=FeedbackResponse)
@limiter.limit("20/hour")
def get_or_generate_feedback(
    request: Request,
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = get_user_attempt(attempt_id, current_user, db)
    
    # If feedback was already generated, return stored feedback record
    existing_fb = db.query(FeedbackRecord).filter(FeedbackRecord.attempt_id == attempt.id).first()
    if existing_fb:
        return FeedbackResponse(
            id=existing_fb.id,
            attempt_id=existing_fb.attempt_id,
            source=existing_fb.source,
            payload=existing_fb.payload,
            citations_valid=existing_fb.citations_valid,
            fallback_reason=existing_fb.fallback_reason,
            model=existing_fb.model,
            latency_ms=existing_fb.latency_ms
        )
        
    require_state(attempt.state, 'feedback')
    case = db.query(Case).filter(Case.id == attempt.case_id).first()
    
    # 1. Reference retrieval
    missed_crit = [
        c['description'] for c in (attempt.criteria_results or []) if not c.get('met')
    ]
    passages = retrieve_references(
        db=db,
        case=case.content,
        missed_criteria=missed_crit,
        tags=attempt.misconception_tags or []
    )
    
    # Check jumped_early flag from step history
    steps = db.query(AttemptStep).filter(AttemptStep.attempt_id == attempt.id).all()
    jumped_early = False
    nodes = case.content.get('branching', {}).get('nodes', [])
    for s in steps:
        node = next((n for n in nodes if n.get('id') == s.node_id), None)
        if node:
            choice = next((c for c in node.get('choices', []) if c.get('id') == s.choice_id), None)
            if choice and 'jumped_early' in choice.get('flags', []):
                jumped_early = True
                break

    # 2. Tutor generation
    submission_dict = {
        'selected_answer': attempt.selected_answer,
        'selected_evidence': attempt.selected_evidence,
        'reasoning_text': attempt.reasoning_text,
        'confidence': attempt.confidence,
        'lang': current_user.preferred_lang or 'en',
        'jumped_early': jumped_early
    }
    scoring_result = {
        'score': attempt.score,
        'max_score': attempt.max_score,
        'is_correct': attempt.is_correct,
        'criteria': attempt.criteria_results,
        'misconceptions': attempt.misconception_tags
    }
    
    fb, source, latency_ms, model_name, citations_valid, fallback_reason = generate_feedback(
        case=case.content,
        submission=submission_dict,
        result=scoring_result,
        passages=passages
    )
    
    # 3. Save feedback record and transition state to FEEDBACK_READY
    fb_record = FeedbackRecord(
        attempt_id=attempt.id,
        source=source,
        payload=fb.model_dump(),
        citations_valid=citations_valid,
        fallback_reason=fallback_reason,
        model=model_name,
        latency_ms=latency_ms
    )
    db.add(fb_record)
    if attempt.parent_attempt_id:
        attempt.state = "COMPLETED"
        attempt.completed_at = datetime.now(timezone.utc)
    else:
        attempt.state = "FEEDBACK_READY"
    db.commit()
    db.refresh(fb_record)
    
    return FeedbackResponse(
        id=fb_record.id,
        attempt_id=fb_record.attempt_id,
        source=fb_record.source,
        payload=fb,
        citations_valid=fb_record.citations_valid,
        fallback_reason=fb_record.fallback_reason,
        model=fb_record.model,
        latency_ms=fb_record.latency_ms
    )

@router.post("/{attempt_id}/lesson-complete")
def complete_lesson(
    attempt_id: str,
    req: LessonCompleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = get_user_attempt(attempt_id, current_user, db)
    require_state(attempt.state, 'lesson')
    
    attempt.state = "LESSON_DONE"
    db.commit()
    return {"status": "ok", "state": attempt.state}

@router.post("/{attempt_id}/reassess")
def start_reassessment(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    parent_attempt = get_user_attempt(attempt_id, current_user, db)
    require_state(parent_attempt.state, 'reassess')

    existing = db.query(Attempt).filter(Attempt.parent_attempt_id == parent_attempt.id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Reassessment attempt already exists for this parent attempt")
    
    parent_case = db.query(Case).filter(Case.id == parent_attempt.case_id).first()
    paired_case_id = parent_case.content.get('paired_case')
    if not paired_case_id:
        raise HTTPException(status_code=400, detail="No paired reassessment case found for this case")
        
    paired_case = db.query(Case).filter(Case.id == paired_case_id).first()
    if not paired_case:
        raise HTTPException(status_code=404, detail="Paired case not found in database")
        
    start_node = paired_case.content.get('branching', {}).get('start', 'n_review')
    
    # Create new attempt linked by parent_attempt_id
    reassess_attempt = Attempt(
        user_id=current_user.id,
        case_id=paired_case.id,
        parent_attempt_id=parent_attempt.id,
        state="STARTED",
        current_node=start_node,
        lang=parent_attempt.lang
    )
    db.add(reassess_attempt)
    db.commit()
    db.refresh(reassess_attempt)
    
    return {
        "attempt_id": reassess_attempt.id,
        "case_id": paired_case.id,
        "parent_attempt_id": parent_attempt.id,
        "state": reassess_attempt.state
    }
