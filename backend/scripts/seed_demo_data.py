import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal, engine, Base
from app.models.models import (
    User, Cohort, LearnerMisconception, Attempt
)
from app.security import hash_password

def seed_synthetic_demo_data(force: bool = False):
    if not force:
        parser = argparse.ArgumentParser(description="Seed synthetic demo peer data for MEDMIND AI")
        parser.add_argument(
            "--demo",
            action="store_true",
            required=True,
            help="Flag required to confirm seeding synthetic demo data."
        )
        args = parser.parse_args()

        if not args.demo:
            print("Error: --demo flag is required to seed synthetic data.")
            sys.exit(1)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    cohort_id = "cohort-med-2026-alpha"
    cohort = db.query(Cohort).filter(Cohort.id == cohort_id).first()
    if not cohort:
        cohort = Cohort(
            id=cohort_id,
            name="Class 2026 - Clinical Medicine Cohort Alpha"
        )
        db.add(cohort)
        db.commit()

    # Synthetic demo peer students
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
                cohort_id=cohort_id,
                is_synthetic=True
            )
            db.add(u)
            db.commit()
            db.refresh(u)
        else:
            u.is_synthetic = True
            db.commit()

        # Record learner misconception
        lm = db.query(LearnerMisconception).filter(
            LearnerMisconception.user_id == u.id,
            LearnerMisconception.misconception_id == p["mc"]
        ).first()
        if not lm:
            lm = LearnerMisconception(
                user_id=u.id,
                misconception_id=p["mc"],
                times_seen=2,
                last_seen_at=datetime.now(timezone.utc)
            )
            db.add(lm)
            db.commit()

        # Initial attempt
        a1 = db.query(Attempt).filter(
            Attempt.user_id == u.id,
            Attempt.case_id == "CASE-FATIGUE-01"
        ).first()
        if not a1:
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
        a2 = db.query(Attempt).filter(
            Attempt.user_id == u.id,
            Attempt.case_id == "CASE-FATIGUE-02"
        ).first()
        if not a2:
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
    print("Synthetic demo data seeded successfully with --demo flag.")

if __name__ == "__main__":
    seed_synthetic_demo_data()
