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

def test_cases_list_requires_auth_and_filters_initial():
    # Unauthenticated returns 401
    unauth = client.get("/api/cases")
    assert unauth.status_code == 401

    # Student login
    login_res = client.post("/api/auth/login", json={
        "email": "student@medmind.ai",
        "password": "student123"
    })
    token = login_res.json()["access_token"]
    res = client.get("/api/cases", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    cases = res.json()
    ids = [c["id"] for c in cases]
    assert "CASE-FATIGUE-01" in ids
    assert "CASE-B12-01" in ids
    # Reassessment case excluded for student case list
    assert "CASE-FATIGUE-02" not in ids

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

def test_path_traversal_blocked():
    for p in ['/%2e%2e/%2e%2e/backend/app/config.py', '/..%2f..%2frun_app.py']:
        r = client.get(p)
        assert 'import os' not in r.text and 'JWT_SECRET' not in r.text

def test_unknown_api_route_is_404():
    assert client.get('/api/doesnotexist').status_code == 404

def test_register_cannot_escalate_role():
    # Attempting to register as 'admin' must ignore client role and create 'student'
    reg_res = client.post("/api/auth/register", json={
        "email": "hacker@testmedmind.edu",
        "password": "validPassword123",
        "display_name": "Test Attacker",
        "role": "admin"
    })
    assert reg_res.status_code == 200
    reg_data = reg_res.json()
    assert reg_data["user"]["role"] == "student"
    
    # Token must be rejected when attempting teacher endpoints
    token = reg_data["access_token"]
    teacher_res = client.get("/api/teacher/cohorts/cohort-med-2026-alpha/summary", headers={"Authorization": f"Bearer {token}"})
    assert teacher_res.status_code == 403

def test_register_short_password_returns_422():
    res = client.post("/api/auth/register", json={
        "email": "shortpw@testmedmind.edu",
        "password": "1",
        "display_name": "Short Pw"
    })
    assert res.status_code == 422

def test_token_signed_with_old_public_secret_returns_401():
    import jwt
    from datetime import datetime, timezone, timedelta
    old_secret = "medmind-super-secure-jwt-secret-key-yukthi-2026"
    forged_token = jwt.encode(
        {"sub": "fake-user-id", "role": "admin", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        old_secret,
        algorithm="HS256"
    )
    res = client.get("/api/progress/me", headers={"Authorization": f"Bearer {forged_token}"})
    assert res.status_code == 401

def test_startup_without_jwt_secret_raises_error(monkeypatch):
    import os
    monkeypatch.setenv("JWT_SECRET", "short")
    insecure = {"", "change-me", "medmind-super-secure-jwt-secret-key-yukthi-2026"}
    sec = os.getenv("JWT_SECRET", "")
    with pytest.raises(RuntimeError):
        if sec in insecure or len(sec) < 32:
            raise RuntimeError("Set JWT_SECRET to a random string of at least 32 characters.")

def test_ownership_student_b_cannot_read_student_a_attempt():
    # Student A creates attempt
    login_a = client.post("/api/auth/login", json={"email": "student@medmind.ai", "password": "student123"}).json()
    token_a = login_a["access_token"]
    att = client.post("/api/attempts", json={"case_id": "CASE-FATIGUE-01"}, headers={"Authorization": f"Bearer {token_a}"}).json()
    attempt_id = att["attempt_id"]

    # Student B registers and tries to read Student A's attempt -> must 404 (not 403)
    login_b = client.post("/api/auth/register", json={
        "email": "studentb@medmind.ai",
        "password": "validPassword123",
        "display_name": "Student B"
    }).json()
    token_b = login_b["access_token"]
    res = client.get(f"/api/attempts/{attempt_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert res.status_code == 404

def test_ownership_teacher_x_cannot_read_teacher_y_cohort():
    # Register teacher Y
    from app.db import SessionLocal
    from app.models.models import User, Cohort
    from app.security import hash_password

    with SessionLocal() as db:
        teacher_y = User(email="teachery@medmind.ai", display_name="Teacher Y", role="teacher", password_hash=hash_password("teacherPassword123"))
        db.add(teacher_y)
        cohort_y = Cohort(name="Cohort Y", teacher_id=teacher_y.id)
        db.add(cohort_y)
        db.commit()
        cohort_y_id = cohort_y.id

    # Dr. Sharma (Teacher X) tries to access Cohort Y summary -> 403
    login_x = client.post("/api/auth/login", json={"email": "dr.sharma@medmind.ai", "password": "teacher123"}).json()
    token_x = login_x["access_token"]
    res = client.get(f"/api/teacher/cohorts/{cohort_y_id}/summary", headers={"Authorization": f"Bearer {token_x}"})
    assert res.status_code == 403

def test_attempt_integrity_junk_answer_returns_422():
    login = client.post("/api/auth/login", json={"email": "student@medmind.ai", "password": "student123"}).json()
    token = login["access_token"]
    att = client.post("/api/attempts", json={"case_id": "CASE-FATIGUE-01"}, headers={"Authorization": f"Bearer {token}"}).json()
    attempt_id = att["attempt_id"]

    # Junk answer option
    res = client.post(f"/api/attempts/{attempt_id}/submit", json={
        "selected_answer": "Z_JUNK",
        "reasoning_text": "Random reasoning",
        "selected_evidence": ["mcv"],
        "confidence": 60
    }, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 422

def test_attempt_integrity_wrong_node_step_returns_409():
    login = client.post("/api/auth/login", json={"email": "student@medmind.ai", "password": "student123"}).json()
    token = login["access_token"]
    att = client.post("/api/attempts", json={"case_id": "CASE-FATIGUE-01"}, headers={"Authorization": f"Bearer {token}"}).json()
    attempt_id = att["attempt_id"]

    # Current node is n_review, attempt to step from n_decide -> 409
    res = client.post(f"/api/attempts/{attempt_id}/step", json={
        "node_id": "n_decide",
        "choice_id": "continue"
    }, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 409

def test_parent_attempt_cross_user_rejected():
    login_a = client.post("/api/auth/login", json={"email": "student@medmind.ai", "password": "student123"}).json()
    token_a = login_a["access_token"]
    att_a = client.post("/api/attempts", json={"case_id": "CASE-FATIGUE-01"}, headers={"Authorization": f"Bearer {token_a}"}).json()

    # Student B tries to use Student A's attempt as parent -> 400
    login_b = client.post("/api/auth/login", json={"email": "studentb@medmind.ai", "password": "validPassword123"}).json()
    token_b = login_b["access_token"]
    res = client.post("/api/attempts", json={
        "case_id": "CASE-FATIGUE-02",
        "parent_attempt_id": att_a["attempt_id"]
    }, headers={"Authorization": f"Bearer {token_b}"})
    assert res.status_code == 400

def test_security_headers_present():
    res = client.get("/api/health")
    assert res.headers.get("X-Content-Type-Options") == "nosniff"
    assert res.headers.get("Referrer-Policy") == "no-referrer"
    assert "default-src" in res.headers.get("Content-Security-Policy", "")

def test_rate_limit_login_returns_429():
    statuses = []
    for _ in range(12):
        r = client.post("/api/auth/login", json={"email": "ratelimit@medmind.ai", "password": "wrongpassword"})
        statuses.append(r.status_code)
    assert 429 in statuses






