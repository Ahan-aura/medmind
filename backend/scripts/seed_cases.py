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
            display_name="Demo Faculty (placeholder)",
            role="teacher",
            preferred_lang="en",
            cohort_id=cohort_id
        )
        db.add(teacher)
        db.commit()
        cohort.teacher_id = teacher.id
        db.commit()
    else:
        teacher.display_name = "Demo Faculty (placeholder)"
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
            
            # Reviewed status dynamically extracted from case YAML
            case.reviewed_by = c_data.get("reviewed_by")
            reviewed_at_raw = c_data.get("reviewed_at")
            if reviewed_at_raw:
                if isinstance(reviewed_at_raw, datetime):
                    case.reviewed_at = reviewed_at_raw
                else:
                    try:
                        case.reviewed_at = datetime.fromisoformat(str(reviewed_at_raw))
                    except Exception:
                        case.reviewed_at = datetime.now(timezone.utc)
            else:
                case.reviewed_at = None
            case.is_published = bool(case.reviewed_by)
        db.commit()
        print("Seeded Cases.")

    db.close()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_cases_and_data()
