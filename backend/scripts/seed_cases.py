import os
import yaml
from pathlib import Path
import sys
from datetime import datetime, timezone

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal, engine, Base
from app.models.models import (
    User, Cohort, Case, Lesson, Misconception,
    LearnerMisconception, Attempt, FeedbackRecord
)
from app.security import hash_password
from app.config import settings
from app.services.misconceptions import MISCONCEPTIONS_REGISTRY

def seed_cases_and_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 1. Seed Cohort
    cohort_id = "cohort-med-2026-alpha"
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        cohort = Cohort(
            id=cohort_id,
            name="Class 2026 - Clinical Medicine Cohort Alpha"
        )
        db.add(cohort)
        db.commit()
    print("Seeded Cohort.")

    # 2. Seed Default Accounts
    # Demo Teacher
    teacher_email = "dr.sharma@medmind.ai"
    teacher = db.query(User).filter(User.email == teacher_email).first()
    if not teacher:
        teacher = User(
            id="user-teacher-01",
            email=teacher_email,
            password_hash=hash_password("teacher123"),
            display_name="Dr. Aarti Sharma, MD",
            role="teacher",
            preferred_lang="en",
            cohort_id=cohort_id
        )
        db.add(teacher)
        db.commit()
        cohort.teacher_id = teacher.id
        db.commit()
    print("Seeded Demo Teacher:", teacher_email)

    # Demo Student
    student_email = "student@medmind.ai"
    student = db.query(User).filter(User.email == student_email).first()
    if not student:
        student = User(
            id="user-student-01",
            email=student_email,
            password_hash=hash_password("student123"),
            display_name="Alex Mercer (Student)",
            role="student",
            preferred_lang="en",
            cohort_id=cohort_id
        )
        db.add(student)
        db.commit()
    print("Seeded Demo Student:", student_email)

    # 3. Seed Misconceptions
    for m_id, m_data in MISCONCEPTIONS_REGISTRY.items():
        m = db.query(Misconception).filter(Misconception.id == m_id).first()
        if not m:
            m = Misconception(
                id=m_id,
                name=m_data["name"],
                description=m_data["description"],
                lesson_id=m_data.get("lesson_id")
            )
            db.add(m)
        else:
            m.name = m_data["name"]
            m.description = m_data["description"]
            m.lesson_id = m_data.get("lesson_id")
    db.commit()
    print("Seeded Misconceptions.")

    # 4. Seed Lessons
    lessons_dir = settings.LESSONS_DIR
    if lessons_dir.exists():
        for l_file in lessons_dir.glob("*.yaml"):
            with open(l_file, "r", encoding="utf-8") as f:
                l_data = yaml.safe_load(f)
            if not l_data:
                continue
            l_id = l_data.get("id") or l_file.stem
            lesson = db.query(Lesson).filter(Lesson.id == l_id).first()
            if not lesson:
                lesson = Lesson(id=l_id)
                db.add(lesson)
            lesson.title = l_data.get("title", l_id)
            lesson.content = l_data.get("content", {})
            lesson.practice_questions = l_data.get("practice_questions", [])
        db.commit()
        print("Seeded Lessons.")

    # 5. Seed Cases
    cases_dir = settings.CASES_DIR
    if cases_dir.exists():
        for c_file in cases_dir.glob("*.yaml"):
            with open(c_file, "r", encoding="utf-8") as f:
                c_data = yaml.safe_load(f)
            if not c_data:
                continue
            c_id = c_data.get("id") or c_file.stem
            case = db.query(Case).filter(Case.id == c_id).first()
            if not case:
                case = Case(id=c_id)
                db.add(case)
            case.version = c_data.get("version", 1)
            case.learning_objective = c_data.get("learning_objective", "LO-GENERAL")
            case.case_role = c_data.get("case_role", "initial")
            case.title = c_data.get("title", c_id)
            case.content = c_data
            case.reviewed_by = "Dr. M. K. Rao, MD (Haematology)"
            case.reviewed_at = datetime.now(timezone.utc)
            case.is_published = True
        db.commit()
        print("Seeded Cases.")

    # 6. Seed Cohort Sample Students & Attempts for compelling Teacher Analytics
    cohort_peer_samples = [
        {"name": "Priya Nair", "email": "priya.nair@medmind.ai", "init_score": 4.0, "re_score": 8.0, "mc": "MC-IGNORES-INDICES", "conf": 80, "corr_init": False},
        {"name": "Rohan Verma", "email": "rohan.v@medmind.ai", "init_score": 3.0, "re_score": 7.0, "mc": "MC-FERRITIN-MISSED", "conf": 90, "corr_init": False},
        {"name": "Siddharth Das", "email": "siddharth@medmind.ai", "init_score": 6.0, "re_score": 9.0, "mc": "MC-IGNORES-RDW", "conf": 60, "corr_init": True},
        {"name": "Ananya Roy", "email": "ananya.roy@medmind.ai", "init_score": 5.0, "re_score": 8.0, "mc": "MC-FERRITIN-MISSED", "conf": 80, "corr_init": False},
        {"name": "Vikram Sethi", "email": "vikram.s@medmind.ai", "init_score": 4.0, "re_score": 8.0, "mc": "MC-MACRO-MICRO-CONFUSED", "conf": 100, "corr_init": False},
    ]

    for p in cohort_peer_samples:
        u = db.query(User).filter(User.email == p["email"]).first()
        if not u:
            u = User(
                email=p["email"],
                password_hash=hash_password("peer123"),
                display_name=p["name"],
                role="student",
                preferred_lang="en",
                cohort_id=cohort_id
            )
            db.add(u)
            db.commit()
            db.refresh(u)

            # Record learner misconception
            lm = LearnerMisconception(
                user_id=u.id,
                misconception_id=p["mc"],
                times_seen=2,
                last_seen_at=datetime.now(timezone.utc)
            )
            db.add(lm)

            # Initial attempt
            a1 = Attempt(
                user_id=u.id,
                case_id="CASE-FATIGUE-01",
                state="COMPLETED",
                selected_answer="B" if not p["corr_init"] else "A",
                reasoning_text="Clinical interpretation of patient fatigue and initial symptoms.",
                selected_evidence=["hb", "mcv"],
                confidence=p["conf"],
                is_correct=p["corr_init"],
                score=p["init_score"],
                max_score=10.0,
                criteria_results=[
                    {"id": "C1", "description": "Selects interpretation", "met": p["corr_init"], "points": 3.0 if p["corr_init"] else 0.0},
                    {"id": "C2", "description": "Uses low MCV", "met": True, "points": 2.0},
                    {"id": "C3", "description": "Uses low ferritin", "met": False, "points": 0.0},
                ],
                misconception_tags=[p["mc"]],
                started_at=datetime.now(timezone.utc),
                submitted_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc)
            )
            db.add(a1)
            db.commit()
            db.refresh(a1)

            # Reassessment attempt
            a2 = Attempt(
                user_id=u.id,
                case_id="CASE-FATIGUE-02",
                parent_attempt_id=a1.id,
                state="COMPLETED",
                selected_answer="A",
                reasoning_text="Identified preserved ferritin and normal RDW pointing to beta-thalassaemia trait.",
                selected_evidence=["ferritin", "rdw", "mcv"],
                confidence=80,
                is_correct=True,
                score=p["re_score"],
                max_score=10.0,
                criteria_results=[
                    {"id": "C1", "description": "Selects Beta-thalassaemia", "met": True, "points": 3.0},
                    {"id": "C2", "description": "Identifies normal ferritin", "met": True, "points": 2.0},
                    {"id": "C3", "description": "Recognises normal RDW", "met": True, "points": 2.0},
                ],
                misconception_tags=[],
                started_at=datetime.now(timezone.utc),
                submitted_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc)
            )
            db.add(a2)
            db.commit()

    db.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_cases_and_data()
