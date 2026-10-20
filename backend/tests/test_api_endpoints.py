import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_cases_list():
    res = client.get("/api/cases")
    assert res.status_code == 200
    cases = res.json()
    assert len(cases) >= 3
    ids = [c["id"] for c in cases]
    assert "CASE-FATIGUE-01" in ids
    assert "CASE-FATIGUE-02" in ids
    assert "CASE-B12-01" in ids

def test_login_invalid_credentials_returns_401():
    # Attempting to login with incorrect credentials must yield 401 and an error detail
    res = client.post("/api/auth/login", json={
        "email": "student@medmind.ai",
        "password": "wrongpassword"
    })
    assert res.status_code == 401
    assert "Invalid email or password" in res.json().get("detail", "")

def test_student_complete_flow():
    # 1. Login as demo student
    login_res = client.post("/api/auth/login", json={
        "email": "student@medmind.ai",
        "password": "student123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Start attempt
    start_res = client.post("/api/attempts", json={"case_id": "CASE-FATIGUE-01"}, headers=headers)
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]
    assert start_res.json()["state"] == "STARTED"

    # 3. Step forward in branching
    step_res = client.post(f"/api/attempts/{attempt_id}/step", json={
        "node_id": "n_review",
        "choice_id": "more_info"
    }, headers=headers)
    assert step_res.status_code == 200
    assert step_res.json()["current_node"] == "n_smear"

    # 4. Submit answer
    submit_res = client.post(f"/api/attempts/{attempt_id}/submit", json={
        "selected_answer": "A",
        "reasoning_text": "Patient has microcytic red cells with depleted ferritin indicating iron deficiency from menorrhagia.",
        "selected_evidence": ["mcv", "ferritin", "rdw"],
        "confidence": 80
    }, headers=headers)
    assert submit_res.status_code == 200
    submit_data = submit_res.json()
    assert submit_data["score"] == 10.0
    assert submit_data["is_correct"] is True
    assert submit_data["state"] == "SUBMITTED"

    # 5. Fetch feedback
    fb_res = client.post(f"/api/attempts/{attempt_id}/feedback", headers=headers)
    assert fb_res.status_code == 200
    fb_data = fb_res.json()
    assert fb_data["source"] == "fallback"
    assert fb_data["citations_valid"] is None  # Correct specification: null for fallback
    assert len(fb_data["payload"]["evidence_links"]) >= 1

    # 6. Check learner progress endpoint
    prog_res = client.get("/api/progress/me", headers=headers)
    assert prog_res.status_code == 200
    prog_data = prog_res.json()
    assert len(prog_data["objectives"]) >= 1

def test_teacher_analytics_access():
    # Login as teacher
    login_res = client.post("/api/auth/login", json={
        "email": "dr.sharma@medmind.ai",
        "password": "teacher123"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    summary_res = client.get("/api/teacher/cohorts/cohort-med-2026-alpha/summary", headers=headers)
    assert summary_res.status_code == 200
    data = summary_res.json()
    assert data["student_count"] >= 5
    assert len(data["objective_averages"]) >= 1
    assert len(data["top_misconceptions"]) >= 1
