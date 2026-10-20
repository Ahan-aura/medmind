import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.db import Base

def gen_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="student")  # 'student', 'teacher', 'admin'
    preferred_lang = Column(String(10), nullable=False, default="en")
    cohort_id = Column(String(36), nullable=True)
    is_synthetic = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    attempts = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")

class Cohort(Base):
    __tablename__ = "cohorts"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(255), nullable=False)
    teacher_id = Column(String(36), ForeignKey("users.id"), nullable=True)

class Case(Base):
    __tablename__ = "cases"

    id = Column(String(100), primary_key=True)  # e.g. CASE-FATIGUE-01
    version = Column(Integer, default=1)
    learning_objective = Column(String(100), nullable=False, index=True)
    case_role = Column(String(50), nullable=False)  # 'initial', 'reassessment'
    title = Column(String(255), nullable=False)
    content = Column(JSON, nullable=False)
    reviewed_by = Column(String(255), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    is_published = Column(Boolean, default=False)

    attempts = relationship("Attempt", back_populates="case")

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    case_id = Column(String(100), ForeignKey("cases.id"), nullable=False, index=True)
    parent_attempt_id = Column(String(36), ForeignKey("attempts.id"), nullable=True)
    
    state = Column(String(50), nullable=False, default="STARTED")  # STARTED, SUBMITTED, FEEDBACK_READY, LESSON_DONE, COMPLETED
    current_node = Column(String(100), default="n_review")
    selected_answer = Column(String(50), nullable=True)
    reasoning_text = Column(Text, nullable=True)
    selected_evidence = Column(JSON, default=list)  # list of lab/history string ids
    confidence = Column(Integer, nullable=True)  # 20, 40, 60, 80, 100
    
    is_correct = Column(Boolean, nullable=True)
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    criteria_results = Column(JSON, nullable=True)
    misconception_tags = Column(JSON, default=list)
    lang = Column(String(10), default="en")
    
    started_at = Column(DateTime(timezone=True), default=utc_now)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="attempts")
    case = relationship("Case", back_populates="attempts")
    steps = relationship("AttemptStep", back_populates="attempt", cascade="all, delete-orphan")
    feedback = relationship("FeedbackRecord", back_populates="attempt", uselist=False, cascade="all, delete-orphan")

class AttemptStep(Base):
    __tablename__ = "attempt_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    attempt_id = Column(String(36), ForeignKey("attempts.id"), nullable=False)
    node_id = Column(String(100), nullable=False)
    choice_id = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    attempt = relationship("Attempt", back_populates="steps")

class FeedbackRecord(Base):
    __tablename__ = "feedback"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    attempt_id = Column(String(36), ForeignKey("attempts.id"), unique=True, nullable=False)
    source = Column(String(50), nullable=False)  # 'llm' or 'fallback'
    payload = Column(JSON, nullable=False)
    citations_valid = Column(Boolean, nullable=True, default=None)
    fallback_reason = Column(String(255), nullable=True)
    model = Column(String(100), nullable=True)
    latency_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    attempt = relationship("Attempt", back_populates="feedback")

class Misconception(Base):
    __tablename__ = "misconceptions"

    id = Column(String(100), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    lesson_id = Column(String(100), nullable=True)

class LearnerMisconception(Base):
    __tablename__ = "learner_misconceptions"

    user_id = Column(String(36), ForeignKey("users.id"), primary_key=True)
    misconception_id = Column(String(100), ForeignKey("misconceptions.id"), primary_key=True)
    times_seen = Column(Integer, default=1)
    last_seen_at = Column(DateTime(timezone=True), default=utc_now)

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(100), primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(JSON, nullable=False)
    practice_questions = Column(JSON, nullable=False)

class ReferenceChunk(Base):
    __tablename__ = "reference_chunks"

    id = Column(String(100), primary_key=True)
    source_title = Column(String(255), nullable=False)
    source_url = Column(String(500), nullable=True)
    section = Column(String(255), nullable=True)
    text = Column(Text, nullable=False)
    lang = Column(String(10), default="en")
    tags = Column(JSON, default=list)
    reviewed = Column(Boolean, default=False)
