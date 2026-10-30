import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import SessionLocal
from app.models.models import Case

from app.security import create_access_token

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_headers():
    token = create_access_token({"sub": "user-student-01", "role": "student"})
    return {"Authorization": f"Bearer {token}"}

def test_all_patient_cases_seeded():
    db = SessionLocal()
    try:
        cases = db.query(Case).all()
        case_ids = {c.id for c in cases}
        
        expected_cases = {
            "CASE-FATIGUE-01",
            "CASE-FATIGUE-02",
            "CASE-B12-01",
            "CASE-B12-02",
            "CASE-THAL-01",
            "CASE-ACD-01",
            "CASE-REDALERT-01"
        }
        for ec in expected_cases:
            assert ec in case_ids, f"Expected case {ec} not found in database"
    finally:
        db.close()

def test_student_cases_endpoint_filters_correctly(auth_headers):
    res = client.get("/api/cases", headers=auth_headers)
    assert res.status_code == 200
    cases = res.json()
    case_ids = {c["id"] for c in cases}

    # Initial cases must be present
    assert "CASE-FATIGUE-01" in case_ids
    assert "CASE-B12-01" in case_ids
    assert "CASE-THAL-01" in case_ids
    assert "CASE-ACD-01" in case_ids
    assert "CASE-REDALERT-01" in case_ids

    # Reassessment cases must NOT be in initial listing for students
    assert "CASE-FATIGUE-02" not in case_ids
    assert "CASE-B12-02" not in case_ids

def test_paired_reassessment_case(auth_headers):
    # Verify CASE-B12-01 and CASE-B12-02 pairing
    db = SessionLocal()
    try:
        c1 = db.query(Case).filter(Case.id == "CASE-B12-01").first()
        c2 = db.query(Case).filter(Case.id == "CASE-B12-02").first()
        assert c1 is not None and c2 is not None
        assert c1.content.get("paired_case") == "CASE-B12-02"
        assert c2.case_role == "reassessment"
        assert c2.content.get("paired_case") == "CASE-B12-01"
    finally:
        db.close()

def test_case_student_view_sanitization(auth_headers):
    res = client.get("/api/cases/CASE-THAL-01", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "CASE-THAL-01"
    assert "rubric" not in data
    assert "misconception_rules" not in data
    # Options must NOT contain "correct" field in student view
    for opt in data.get("options", []):
        assert "correct" not in opt

def test_assistant_chat_unauthenticated():
    res = client.post("/api/assistant/chat", json={"message": "What is microcytosis?"})
    assert res.status_code == 401

def test_assistant_chat_authenticated(auth_headers):
    res = client.post("/api/assistant/chat", json={
        "message": "How do I differentiate iron deficiency from beta-thalassaemia trait?"
    }, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert len(data["reply"]) > 50
    assert "Mentzer" in data["reply"] or "Ferritin" in data["reply"] or "microcytosis" in data["reply"].lower()
    assert len(data.get("citations", [])) >= 1
    assert len(data.get("suggested_questions", [])) >= 1
    assert "disclaimer" in data
    assert "not medical advice" in data["disclaimer"].lower()

def test_assistant_chat_ferritin_topic(auth_headers):
    res = client.post("/api/assistant/chat", json={
        "message": "Why is serum ferritin elevated during inflammation?"
    }, headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    reply = data["reply"]
    assert "acute-phase" in reply.lower() or "hepcidin" in reply.lower() or "inflammation" in reply.lower()

def test_assistant_starter_prompts(auth_headers):
    res = client.get("/api/assistant/prompts", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    groups = data.get("groups", [])
    assert len(groups) >= 4
    categories = [g["category"] for g in groups]
    assert "Full Blood Count Basics" in categories
    assert "Microcytic Differentials" in categories
    assert "Ferritin & Inflammation" in categories
    assert "Macrocytosis & Megaloblastosis" in categories
