import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from app.db import SessionLocal, engine, Base
from app.models.models import Lesson, ReferenceChunk
from app.schemas.lesson import LessonModel
from app.config import settings

def seed_lessons(db=None):
    close_db = False
    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        close_db = True

    try:
        lessons_dir = settings.LESSONS_DIR
        if not lessons_dir.exists():
            print(f"Lessons directory {lessons_dir} does not exist.")
            return

        # Check existing reference chunk IDs in DB and filesystem
        ref_files = {f.stem for f in settings.REFERENCES_DIR.glob("*.md")}
        db_ref_ids = {r.id for r in db.query(ReferenceChunk.id).all()}
        all_known_refs = ref_files | db_ref_ids

        for l_file in sorted(lessons_dir.glob("*.yaml")):
            with open(l_file, "r", encoding="utf-8") as f:
                l_data = yaml.safe_load(f)
            if not l_data:
                continue

            l_id = l_data.get("id") or l_file.stem
            
            # If it is a new doctor-practice lesson (LESSON-0X), apply strict validation
            if l_id.startswith("LESSON-0"):
                # 1. Pydantic schema validation
                validated = LessonModel(**l_data)
                
                # 2. Check reference passages integrity
                for ref_id in validated.reference_ids:
                    if ref_id not in all_known_refs:
                        raise RuntimeError(f"Lesson {l_id} references missing reference passage: {ref_id}")

                # 3. Check unreviewed content setting
                if not settings.ALLOW_UNREVIEWED_CONTENT:
                    if validated.status == "draft" or not validated.reviewed_by:
                        raise RuntimeError(f"Lesson {l_id} has unreviewed content, but allow_unreviewed_content is false")

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

            # Compatibility content mapping
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

        db.commit()
        print("Successfully seeded and validated all lessons.")
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_lessons()
