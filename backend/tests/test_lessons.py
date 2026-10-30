import pytest
import re
import yaml
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings
from app.schemas.lesson import LessonModel
from app.services.misconceptions import MISCONCEPTIONS_REGISTRY
from app.models.models import Misconception, ReferenceChunk, LessonProgress
from app.security import create_access_token
import app.db as db_module

BANNED_WORDS_RE = re.compile(r'\b(dose|doses|dosage|mg|prescribe|prescribes|prescribed|prescriber|prescription)\b', re.IGNORECASE)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    session = db_module.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def auth_headers():
    token = create_access_token({"sub": "user-student-01", "role": "student"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def fresh_user_headers():
    token = create_access_token({"sub": "user-rate-limit-test-01", "role": "student"})
    return {"Authorization": f"Bearer {token}"}

def test_schema_validation():
    """All 8 lesson YAMLs parse and pass Pydantic LessonModel validation."""
    lessons_dir = settings.LESSONS_DIR
    lesson_files = sorted(lessons_dir.glob("LESSON-0*.yaml"))
    assert len(lesson_files) == 8, f"Expected 8 doctor-practice lessons, found {len(lesson_files)}"

    for l_file in lesson_files:
        with open(l_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        model = LessonModel(**data)
        assert model.id == l_file.stem
        assert len(model.learning_outcomes) == 3
        assert 4 <= len(model.key_points) <= 10
        assert len(model.quick_check) == 3
        assert model.status == "draft"
        assert model.reviewed_by is None

def test_reference_integrity(db_session):
    """Every reference_id cited in any lesson exists in backend/content/references/ and database."""
    lessons_dir = settings.LESSONS_DIR
    ref_dir = settings.REFERENCES_DIR

    for l_file in lessons_dir.glob("LESSON-0*.yaml"):
        with open(l_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        # Check reference_ids list
        for ref_id in data.get("reference_ids", []):
            md_path = ref_dir / f"{ref_id}.md"
            assert md_path.exists(), f"Reference file {md_path} missing for lesson {data['id']}"

        # Check references in key points
        for kp in data.get("key_points", []):
            for ref_id in kp.get("refs", []):
                md_path = ref_dir / f"{ref_id}.md"
                assert md_path.exists(), f"Key point reference {ref_id} missing in {data['id']}"

        # Check references in quick check questions
        for q in data.get("quick_check", []):
            ref_id = q.get("reference_id")
            if ref_id:
                md_path = ref_dir / f"{ref_id}.md"
                assert md_path.exists(), f"Quick check reference {ref_id} missing in {data['id']}"

def test_misconception_mapping(db_session):
    """Every misconception cited in targets_misconceptions exists in the registry and database."""
    lessons_dir = settings.LESSONS_DIR
    for l_file in lessons_dir.glob("LESSON-0*.yaml"):
        with open(l_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        for misc_id in data.get("targets_misconceptions", []):
            assert misc_id in MISCONCEPTIONS_REGISTRY, f"Misconception {misc_id} in {data['id']} not in registry"
            db_m = db_session.query(Misconception).filter(Misconception.id == misc_id).first()
            assert db_m is not None, f"Misconception {misc_id} in {data['id']} not seeded into database"

def test_answer_distribution():
    """No single option letter (A, B, C, D) is correct for more than 40% of the 24 questions."""
    lessons_dir = settings.LESSONS_DIR
    counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    total_questions = 0

    for l_file in sorted(lessons_dir.glob("LESSON-0*.yaml")):
        with open(l_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for q in data.get("quick_check", []):
            correct = q.get("correct")
            assert correct in counts, f"Invalid correct option '{correct}' in {data['id']}"
            counts[correct] += 1
            total_questions += 1

    assert total_questions == 24, f"Expected 24 questions across 8 lessons, found {total_questions}"
    for opt, count in counts.items():
        percentage = (count / total_questions) * 100.0
        assert percentage <= 40.0, f"Option {opt} accounts for {percentage:.1f}% (> 40%) of correct answers"

def test_draft_visibility(client, auth_headers):
    """When allow_unreviewed_content is False, GET /api/lessons returns only reviewed lessons; when True, returns all."""
    # 1. When ALLOW_UNREVIEWED_CONTENT is True (default)
    orig_setting = settings.ALLOW_UNREVIEWED_CONTENT
    try:
        settings.ALLOW_UNREVIEWED_CONTENT = True
        res = client.get("/api/lessons", headers=auth_headers)
        assert res.status_code == 200
        lessons = res.json()
        lesson_ids = [l["id"] for l in lessons]
        assert "LESSON-01" in lesson_ids
        assert "LESSON-08" in lesson_ids
        assert len(lessons) >= 8

        # 2. When ALLOW_UNREVIEWED_CONTENT is False
        settings.ALLOW_UNREVIEWED_CONTENT = False
        res = client.get("/api/lessons", headers=auth_headers)
        assert res.status_code == 200
        reviewed_lessons = res.json()
        for l in reviewed_lessons:
            assert l["status"] != "draft"

        # Also GET /api/lessons/LESSON-01 returns 403 when unreviewed content disallowed
        res_detail = client.get("/api/lessons/LESSON-01", headers=auth_headers)
        assert res_detail.status_code == 403
    finally:
        settings.ALLOW_UNREVIEWED_CONTENT = orig_setting

def test_quiz_answer_confidentiality(client, auth_headers):
    """GET /api/lessons/{id} does not contain 'correct' or 'rationale' in question options or bodies."""
    res = client.get("/api/lessons/LESSON-01", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()

    assert "quick_check" in data
    assert len(data["quick_check"]) == 3
    for q in data["quick_check"]:
        assert "correct" not in q, f"Question {q.get('id')} leaked 'correct' answer key"
        assert "rationale" not in q, f"Question {q.get('id')} leaked 'rationale'"
        for opt in q.get("options", []):
            assert "correct" not in opt, f"Option {opt.get('id')} leaked 'correct' flag"

def test_quiz_scoring_and_progress(client, auth_headers, db_session):
    """Quiz scoring returns accurate score, rationale, and monotonically updates best_score."""
    # 1. Perfect submission: LESSON-01 answer key is Q1: A, Q2: B, Q3: C
    perfect_answers = {"Q1": "A", "Q2": "B", "Q3": "C"}
    res = client.post("/api/lessons/LESSON-01/quiz", json={"answers": perfect_answers}, headers=auth_headers)
    assert res.status_code == 200
    res_data = res.json()
    assert res_data["score"] == 3
    assert res_data["max_score"] == 3
    assert res_data["passed"] is True
    assert res_data["best_score"] == 3
    assert "results" in res_data
    assert res_data["results"]["Q1"]["is_correct"] is True
    assert len(res_data["results"]["Q1"]["rationale"]) > 0

    # 2. Incomplete submission returns 422
    incomplete_answers = {"Q1": "A", "Q2": "B"}
    res_inc = client.post("/api/lessons/LESSON-01/quiz", json={"answers": incomplete_answers}, headers=auth_headers)
    assert res_inc.status_code == 422

    # 3. Invalid option letter returns 422
    invalid_opt_answers = {"Q1": "A", "Q2": "B", "Q3": "Z"}
    res_inv = client.post("/api/lessons/LESSON-01/quiz", json={"answers": invalid_opt_answers}, headers=auth_headers)
    assert res_inv.status_code == 422

    # 4. Monotonic progression: submitting a lower score on a different lesson
    # LESSON-02 answers: Q1: D, Q2: A, Q3: B
    # First submit 2 correct (Q1: D, Q2: A, Q3: D) -> score = 2
    res_sub2 = client.post("/api/lessons/LESSON-02/quiz", json={"answers": {"Q1": "D", "Q2": "A", "Q3": "D"}}, headers=auth_headers)
    assert res_sub2.status_code == 200
    assert res_sub2.json()["score"] == 2
    assert res_sub2.json()["best_score"] == 2

    # Now submit 1 correct (Q1: D, Q2: B, Q3: D) -> score = 1
    res_sub1 = client.post("/api/lessons/LESSON-02/quiz", json={"answers": {"Q1": "D", "Q2": "B", "Q3": "D"}}, headers=auth_headers)
    assert res_sub1.status_code == 200
    assert res_sub1.json()["score"] == 1
    # best_score must NOT decrease
    assert res_sub1.json()["best_score"] == 2

def test_quiz_rate_limiting(client, auth_headers):
    """Submissions beyond 3 per hour on the same lesson return 429."""
    answers = {"Q1": "B", "Q2": "C", "Q3": "D"}  # LESSON-04 answers
    # Call 1, 2, 3 should succeed
    for i in range(3):
        res = client.post("/api/lessons/LESSON-04/quiz", json={"answers": answers}, headers=auth_headers)
        assert res.status_code == 200, f"Attempt {i+1} failed unexpectedly with status {res.status_code}"

    # Call 4 within the hour must be blocked with 429
    res_4 = client.post("/api/lessons/LESSON-04/quiz", json={"answers": answers}, headers=auth_headers)
    assert res_4.status_code == 429, f"Expected 429 RateLimitExceeded on 4th call, got {res_4.status_code}"

def test_no_banned_prescribing_words():
    """Assert no lesson YAML contains 'dose', 'mg', or 'prescribe' (case-insensitive)."""
    lessons_dir = settings.LESSONS_DIR
    for l_file in sorted(lessons_dir.glob("LESSON-0*.yaml")):
        with open(l_file, "r", encoding="utf-8") as f:
            content = f.read()

        matches = BANNED_WORDS_RE.findall(content)
        assert len(matches) == 0, f"File {l_file.name} contains banned prescribing strings: {matches}"
