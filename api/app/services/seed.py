from app.schemas.lesson import LessonModel
from app.models.models import ReferenceChunk
import os
import yaml
import logging
from pathlib import Path
from datetime import datetime, timezone

from app.db import SessionLocal, engine, Base
from app.models.models import (
    User, Cohort, Case, Lesson, Misconception
)
from app.security import hash_password
from app.config import settings
from app.services.misconceptions import MISCONCEPTIONS_REGISTRY

logger = logging.getLogger("medmind.seed")

def ensure_seeded():
    """Ensure database has basic tables, users, cases, lessons, and misconceptions."""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.warning("create_all deferred: %s", e)
        return

    db = SessionLocal()
    try:
        # 1. Cohort
        cohort_id = "cohort-med-2026-alpha"
        cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
        if not cohort:
            cohort = Cohort(
                id=cohort_id,
                name="Class 2026 - Clinical Medicine Cohort Alpha"
            )
            db.add(cohort)
            db.commit()

        # 2. Default Users (Student, Teacher, and Mullick Ahan)
        users_to_seed = [
            ("user-student-01", "student@medmind.ai", "student123", "Alex Mercer (Student)", "student"),
            ("user-teacher-01", "dr.sharma@medmind.ai", "teacher123", "Demo Faculty (placeholder)", "teacher"),
            ("user-ahan-01", "mullickahan@gmail.com", "student123", "Ahan Mullick", "student")
        ]
        for uid, email, pwd, name, role in users_to_seed:
            u = db.query(User).filter(User.email == email.lower()).first()
            if not u:
                u = User(
                    id=uid,
                    email=email.lower(),
                    password_hash=hash_password(pwd),
                    display_name=name,
                    role=role,
                    preferred_lang="en",
                    cohort_id=cohort_id
                )
                db.add(u)
                db.commit()

        # 3. Misconceptions
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
        db.commit()

        # 4. Lessons
        lessons_dir = settings.LESSONS_DIR
        if lessons_dir.exists():
            for l_file in lessons_dir.glob("*.yaml"):
                try:
                    with open(l_file, "r", encoding="utf-8") as f:
                        l_data = yaml.safe_load(f)
                    if not l_data:
                        continue
                    l_id = l_data.get("id") or l_file.stem
                    if l_id.startswith("LESSON-0"):
                        validated = LessonModel(**l_data)
                    lesson = db.query(Lesson).filter(Lesson.id == l_id).first()
                    if not lesson:
                        lesson = Lesson(id=l_id)
                        db.add(lesson)
                    lesson.title = l_data.get("title", l_id)
                    lesson.objective_id = l_data.get("objective_id")
                    lesson.status = l_data.get("status", "draft")
                    lesson.reviewed_by = l_data.get("reviewed_by")
                    lesson.difficulty = l_data.get("difficulty", 1)
                    lesson.estimated_minutes = l_data.get("estimated_minutes", 8)
                    lesson.targets_misconceptions = l_data.get("targets_misconceptions", [])
                    lesson.prerequisites = l_data.get("prerequisites", [])
                    lesson.raw_data = l_data
                    if "content" in l_data:
                        lesson.content = l_data["content"]
                    else:
                        lesson.content = {
                            "overview": l_data.get("worked_example", {}).get("vignette", ""),
                            "key_principles": [
                                {"title": f"{i+1}. Point", "explanation": kp.get("point", "")}
                                for i, kp in enumerate(l_data.get("key_points", []))
                            ],
                            "clinical_pearl": l_data.get("clinical_pearl", "")
                        }
                    if "practice_questions" in l_data:
                        lesson.practice_questions = l_data["practice_questions"]
                    else:
                        lesson.practice_questions = l_data.get("quick_check", [])
                except Exception as ex:
                    logger.warning("Error seeding lesson %s: %s", l_file, ex)
            db.commit()

        # 5. Cases
        cases_dir = settings.CASES_DIR
        if cases_dir.exists():
            for c_file in cases_dir.glob("*.yaml"):
                try:
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
                except Exception as ex:
                    logger.warning("Error seeding case %s: %s", c_file, ex)
            db.commit()

    except Exception as e:
        logger.warning("Database ensure_seeded non-fatal: %s", e)
    finally:
        db.close()
