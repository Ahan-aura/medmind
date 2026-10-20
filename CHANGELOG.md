# CHANGELOG: MEDMIND AI Audit & Remediation

All fixes, modifications, and accompanying test verifications implemented as part of the system integrity and reliability audit.

---

## Section 3: Client, Simulator & Demo Mode Integrity

### Fixes:
1. **Strict Demo Mode Gating (`frontend/src/api/client.ts`)**:
   - The mock simulator runs **ONLY** when `VITE_DEMO_MODE === 'true'`.
   - Never falls back to mock simulation on HTTP 4xx, 5xx, or standard API errors; real error responses are surfaced to the user.
   - If the network is completely unreachable (connection refused, server down), throws `BackendUnavailableError`.
2. **Backend Unavailable Screen (`frontend/src/pages/LoginPage.tsx`)**:
   - Dedicated UI screen displayed upon network failure explaining that the backend is unreachable, with a live retry button.
3. **Persistent Simulation Banner (`frontend/src/components/DisclaimerBanner.tsx`)**:
   - When running in demo mode, renders a persistent amber warning banner across all screens:
     `"SIMULATION MODE: no server, sample data, scores are not real."`
4. **Restricted Mock Credentials & Sample Labels (`frontend/src/pages/LoginPage.tsx`, `ProgressPage.tsx`, `TeacherPage.tsx`)**:
   - Demo mode accepts only documented demo credentials (`student@medmind.ai` / `student123`, `dr.sharma@medmind.ai` / `teacher123`).
   - Mock educator analytics and progress statistics explicitly labeled "Sample Data".
5. **Vercel Routing Fix (`vercel.json`, `frontend/vercel.json`)**:
   - Configured route rewrites to proxy `/api/(.*)` to `https://<BACKEND_URL>/api/$1` first, followed by SPA fallback `/(.*)` to `/index.html`.

### Automated Verification & Tests:
- `backend/tests/test_api_endpoints.py::test_login_invalid_credentials_returns_401`: Verifies that invalid login credentials return HTTP 401 with real error details without falling back to mock login.
- Verified frontend build passes (`npm run build`).

---

## Section 4: Fake Data and Unearned Claims

### Fixes:
1. **Dynamic Case Review Status (`backend/scripts/seed_cases.py`, `backend/content/cases/*.yaml`)**:
   - Removed hard-coded `reviewed_by = "Dr. M. K. Rao..."` and `reviewed_at = now()`.
   - `reviewed_by` and `reviewed_at` are read dynamically from each case YAML (defaulting to null).
   - `is_published` is evaluated as `bool(case.reviewed_by)`.
   - Defaulted `ReferenceChunk.reviewed` attribute to `False` in schema and ingestion pipeline.
2. **Isolation of Synthetic Peer Cohort (`backend/scripts/seed_demo_data.py`)**:
   - Moved the 5 synthetic peer students (Priya Nair, Rohan Verma, Siddharth Das, Ananya Roy, Vikram Sethi) and their attempts out of `seed_cases.py` into a separate script: `backend/scripts/seed_demo_data.py`.
   - Script enforces the `--demo` confirmation flag to run.
   - Added `is_synthetic = Column(Boolean, default=False)` to `User` model.
   - Teacher dashboard shows "Synthetic demo data" badge whenever synthetic users are included in cohort aggregates.
3. **Renamed Demo Faculty**:
   - Renamed faculty display name to `"Demo Faculty (placeholder)"` across seeds, translation dictionaries, and login views.
4. **Softened Claims in Documentation & UI (`README.md`, `translations.ts`, `DemoWalkthroughBar.tsx`)**:
   - Replaced unearned claims ("zero hallucination", "guarantees", "faculty-reviewed", "semantic ranking") with precise technical descriptions ("strict citation validation", "curated reference guidelines", "tag + keyword ranking").
   - Replaced static "Tests 10/10" badge with live GitHub Actions CI badge.
   - Corrected command paths in README from `medmind-ai/backend` to `backend`.

### Automated Verification & Tests:
- `backend/tests/test_backend.py::test_reference_chunk_reviewed_default_false`: Asserts default for `ReferenceChunk.reviewed` is `False`.
- `backend/tests/test_backend.py::test_case_is_published_requires_reviewed_by`: Asserts `is_published` requires `reviewed_by`.
- `backend/tests/test_backend.py::test_synthetic_user_flag`: Validates `is_synthetic` flag behavior on User model.

---

## Section 5: AI Tutor Robustness & Security

### Fixes:
1. **Single Provider Selection & Configuration (`backend/app/config.py`, `main.py`)**:
   - Selected Anthropic Claude as single provider; removed Gemini integration.
   - Removed default `LLM_MODEL=gemini-1.5-flash`; `LLM_MODEL` must be set explicitly.
   - On startup, logs effective tutor mode (`live`, `cached`, `fallback`) and logs warning if `ANTHROPIC_API_KEY` is present but `LLM_MODEL` is missing.
2. **Proper `TUTOR_MODE` Implementation (`backend/app/services/tutor.py`)**:
   - `auto`: Live LLM if both API key and model identifier are configured; otherwise safe deterministic fallback.
   - `cached` / `fallback`: Deterministic curated guidance loader.
3. **Strict Number Validation (`backend/app/services/tutor.py::validate_feedback`)**:
   - Rejects feedback containing ANY number not present in the case history, lab panels, scoring rubric, or retrieved passages.
   - Removed `len(n) > 3` loophole and blanket 0-100 allowance.
   - Allows only small counting digits 0–10.
4. **Retry Once with Fallback Reason (`backend/app/services/tutor.py`, `backend/app/routers/attempts.py`)**:
   - If initial LLM output fails citation or number validation, retries once with validation feedback.
   - If second attempt fails or on timeout/network exception, falls back immediately to curated guidance and stores `fallback_reason` on the `FeedbackRecord`.
   - `citations_valid`: Null for fallback responses; boolean for live validated LLM responses.
5. **Prompt Injection Defense (`backend/app/services/tutor.py::build_tutor_prompt`)**:
   - Student reasoning text is sanitized (angle brackets `<` and `>` escaped as `&lt;` and `&gt;`) and JSON-encoded as a string value.
   - Prevents student input from breaking out of or closing XML tags like `</student_submission>`.
   - Includes learner `lang` and `jumped_early` investigation flag from step history.

### Automated Verification & Tests:
- `test_tutor_validation_rejects_fake_ref_id`: Validates rejection of non-approved reference IDs.
- `test_tutor_validation_rejects_invented_value_7_2`: Validates rejection of hallucinated lab numbers (e.g. 7.2).
- `test_tutor_timeout_fallback_with_reason`: Validates timeout handling, fallback transition, and `fallback_reason` recording.
- `test_tutor_prompt_injection_cannot_close_tag`: Validates tag escaping and verifies prompt contains exactly 1 closing tag.

---

## Section 6: Retrieval Honesty

### Fixes:
1. **Accurate Retrieval Terminology (`backend/app/services/rag.py`, `README.md`, `.env.example`, `docker-compose.yml`)**:
   - Replaced all claims of "semantic search", "vector database", or "pgvector" with "curated reference retrieval (tag + keyword ranking over reviewed passages)".
   - Swapped `pgvector/pgvector:pg16` in `docker-compose.yml` for standard `postgres:16-alpine`.
   - Documented exact ranking mechanics: tag overlap (10.0 weight) + keyword occurrence (1.0 weight) over approved passages restricted to the active case.

### Automated Verification & Tests:
- `backend/tests/test_backend.py::test_curated_reference_retrieval_ranking`: Tests that retrieval ranks approved passages matching missed criteria and misconception tags without vector dependencies.

---

## Section 7: Dependencies, Test Isolation & Deployment

### Fixes:
1. **Pinned Dependencies (`backend/requirements.txt`)**:
   - Added pinned dependency manifest: `fastapi==0.137.2`, `uvicorn[standard]==0.49.0`, `sqlalchemy==2.1.5`, `psycopg[binary]==3.2.5`, `pydantic==2.13.4`, `email-validator==2.2.0`, `pyyaml==6.0.2`, `pyjwt==2.15.1`, `argon2-cffi==25.1.0`, `anthropic==0.49.0`, `slowapi==0.1.9`, `pytest==9.1.1`, `httpx==0.28.1`.
2. **Isolated Test Database Fixture (`backend/tests/conftest.py`)**:
   - Created session-scoped autouse fixture that provisions a temporary SQLite database, seeds reference passages, cases, and demo peers, and overrides `get_db`.
   - Guarantees `pytest` runs and passes on a clean clone without requiring existing database artifacts.
3. **Containerization (`backend/Dockerfile`)**:
   - Created lightweight Python 3.12-slim Dockerfile with automated startup ingestion and seeding.
4. **Continuous Integration (`.github/workflows/ci.yml`)**:
   - Added GitHub Actions workflow running backend pytest on Python 3.12 and frontend build (`npm run build`) on Node.js 20 on every push/PR.
5. **Database Normalization & Deployment Documentation (`backend/app/db.py`, `README.md`)**:
   - Added automatic URI normalization in `db.py` to convert `postgres://` / `postgresql://` to `postgresql+psycopg://` for Render and Railway deployments.
   - Added complete deployment guide in `README.md` covering Render/Railway (backend + PostgreSQL) and Vercel (frontend).
6. **Live DB Health Check (`backend/app/main.py`)**:
   - `/api/health` executes `SELECT 1` on the active database session and returns actual connection status.

### Automated Verification & Tests:
- `backend/tests/test_api_endpoints.py::test_health_endpoint`: Validates `/api/health` returns status `ok` and live database connectivity.
- Full test suite: 19 passing tests with 0 failures.
