# SECURITY & DATA INTEGRITY POLICY: MEDMIND AI

This document details how secrets are managed, how administrative/faculty accounts are provisioned, and what data within the system is synthetic.

---

## 1. Secrets Management

### Critical Secrets:
* **`JWT_SECRET`**:
  - Used by `app/security.py` to sign and verify HS256 authentication tokens.
  - **Generation**: Generate a secure 256-bit random key before deploying to production:
    ```bash
    openssl rand -hex 32
    ```
  - **Storage**: Place in your `.env` file for local development. In production (Render, Railway, Fly.io), set it as an encrypted environment variable. **Never commit `.env` or secrets to version control.**

* **`ANTHROPIC_API_KEY`**:
  - Optional. Used by `app/services/tutor.py` to generate live clinical explanations using Anthropic Claude.
  - If omitted or empty, the platform automatically operates in safe fallback mode, returning pre-reviewed, deterministic clinical guidance with zero external network requests.
  - Set as an encrypted environment variable in your production host.

* **`DATABASE_URL`**:
  - Connection string for SQLite or managed PostgreSQL.
  - When deploying to production on Render or Railway, use the provided internal database connection URL with SSL enabled (`sslmode=require`).

---

## 2. Faculty & Teacher Account Provisioning

### Password Hashing:
* All passwords are hashed using **Argon2id** (`argon2-cffi`) with secure time and memory cost parameters. Plaintext passwords are never stored.

### Seeded Demo Accounts:
The system includes two pre-seeded demonstration accounts for local evaluation:
* **Student Learner**: `student@medmind.ai` (Password: `student123`)
* **Demo Faculty (placeholder)**: `dr.sharma@medmind.ai` (Password: `teacher123`)

### Provisioning New Faculty Accounts in Production:
To prevent unauthorized users from creating educator accounts with access to class-wide cohort analytics:
1. Public registration via `/api/auth/register` automatically assigns the default role `"student"`.
2. To promote a user to `"teacher"` or `"admin"`, an administrator must update the user record directly via database CLI or an administrative script:
   ```python
   from app.db import SessionLocal
   from app.models.models import User

   db = SessionLocal()
   user = db.query(User).filter(User.email == "faculty@medschool.edu").first()
   if user:
       user.role = "teacher"
       user.display_name = "Prof. Jane Doe"
       db.commit()
   db.close()
   ```
3. Assign the teacher's `id` to the corresponding `Cohort.teacher_id` to grant access to the cohort analytics dashboard.

---

## 3. Synthetic Data Disclosure & Medical Simulation Scope

### Educational Scope:
* **MEDMIND AI is an educational simulation platform** designed exclusively for training medical, nursing, and healthcare students in clinical diagnostic reasoning.
* **NOT A CLINICAL DIAGNOSTIC TOOL**: The platform must never be used for real patient diagnosis, treatment planning, medication dosing, or clinical decision support.

### Synthetic Data Details:
1. **Patient Cases & Laboratory Values**:
   - Cases `CASE-FATIGUE-01` (Alex), `CASE-FATIGUE-02` (Jordan), and `CASE-B12-01` (Morgan) are fictional clinical vignettes created solely for educational practice.
   - All haematological laboratory panels (haemoglobin, MCV, RDW, ferritin, vitamin B12) are synthetically constructed to illustrate specific pathophysiological patterns (e.g. microcytic hypochromic anaemia vs beta-thalassaemia trait).
2. **Reviewer & Author Metadata**:
   - Case metadata specifies `"Curriculum Team (Educational Draft)"` or placeholder designations. No claims of review by licensed physicians or medical institutions are made.
3. **Cohort Peer Analytics**:
   - The five peer learners (`priya.nair@medmind.ai`, `rohan.v@medmind.ai`, `siddharth@medmind.ai`, `ananya.roy@medmind.ai`, `vikram.s@medmind.ai`) and their attempts are synthetic.
   - They are seeded strictly via `python scripts/seed_demo_data.py --demo`.
   - Each synthetic user has `is_synthetic = True` in the database.
   - Whenever synthetic users are included in cohort aggregates, the faculty analytics dashboard explicitly displays a **"Synthetic Demo Data"** badge to inform educators.

---

## 4. Reporting Security Vulnerabilities

If you discover a security vulnerability in MEDMIND AI, please contact the maintainers or open a confidential security advisory on GitHub. Do not file public issues for active security vulnerabilities.
