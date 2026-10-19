# MEDMIND AI 2.0 (YUKTHI 26)
### Adaptive Clinical Reasoning Practice Simulator for Medical & Nursing Students
**Learn smarter. Detect earlier. Practice safer.**

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python%203.12-blue.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%7C%20Vite%20%7C%20Tailwind-teal.svg)](https://react.dev/)
[![Tests](https://img.shields.io/badge/Tests-10%2F10%20Passing-emerald.svg)](https://pytest.org/)
[![Safety](https://img.shields.io/badge/Clinical%20Scope-Educational%20Simulation%20Only-amber.svg)](#educational-safety-principles)

---

## 1. Executive Summary

**MEDMIND AI** addresses a fundamental challenge in medical education: students frequently memorize laboratory definitions from textbooks but struggle when translating patient history and laboratory panels into cohesive clinical reasoning.

Unlike open-ended chatbots that hallucinate diagnoses or alter grading standards, **MEDMIND AI enforces a strict architectural boundary**:
1. **Deterministic Core**: Case facts, allowed diagnostic choices, branching nodes, scoring rubrics, and answer keys reside strictly in validated Python application code and database records. The LLM never grades or alters case facts.
2. **Grounded AI Explanation Layer**: When explaining reasoning gaps, the AI tutor is constrained to verified clinical guidelines (e.g., British Society of Haematology, WHO), with automated schema validation and citation checking that rejects hallucinated references or measurements.
3. **The Complete Adaptive Loop**:
   $$\text{Fictional Case} \longrightarrow \text{Decision \& Evidence} \longrightarrow \text{Grounded Tutor Feedback} \longrightarrow \text{Targeted Concept Module} \longrightarrow \text{New-Case Reassessment} \longrightarrow \text{Progress Analytics}$$

---

## 2. System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  BROWSER: React + Vite + Tailwind (Student UI, Faculty UI)    │
└──────────────────────────────┬───────────────────────────────┘
                               │ HTTPS / REST (JWT Bearer Token)
┌──────────────────────────────▼───────────────────────────────┐
│  FASTAPI BACKEND (Python 3.12)                               │
│  ┌─────────┐ ┌─────────────┐ ┌────────────┐ ┌──────────────┐ │
│  │ Auth    │ │ Case Engine │ │ Scoring +  │ │ Analytics    │ │
│  │ (JWT)   │ │ (State      │ │ Misconcep- │ │ (Progress,   │ │
│  │         │ │  Machine)   │ │ tion Rules │ │  Teacher)    │ │
│  └─────────┘ └─────────────┘ └────────────┘ └──────────────┘ │
│  ┌──────────────────────┐   ┌──────────────────────────────┐ │
│  │ RAG Retrieval        │──▶│ AI Tutor Service             │ │
│  │ Tag-overlap + Semantic│  │ Prompt → LLM → Validation    │ │
│  │ Ranking              │   │ & Fallback Protection        │ │
│  └──────────┬───────────┘   └──────────────┬───────────────┘ │
└─────────────┼──────────────────────────────┼─────────────────┘
              │                              │
┌─────────────▼─────────────┐    ┌───────────▼─────────────────┐
│ SQLite / PostgreSQL       │    │ LLM API                     │
│ Users, Cases, Attempts,   │    │ Anthropic / Gemini /        │
│ Feedback, References      │    │ Pre-reviewed Fallback       │
└───────────────────────────┘    └─────────────────────────────┘
```

---

## 3. The 6 Core Clinical Features

1. **Clinical Reasoning Copilot**: Compels learners to justify diagnostic selections using specific laboratory indices and clinical history clues.
2. **Evidence-Linked Reasoning**: Clickable laboratory panel linking findings (e.g. low MCV, depleted ferritin) directly to diagnostic criteria.
3. **Misconception-to-Mastery**: Automated rule-based detection of recurring reasoning traps (`MC-MACRO-MICRO-CONFUSED`, `MC-FERRITIN-MISSED`, `MC-IGNORES-INDICES`), triggering targeted micro-lessons.
4. **Confidence Calibration**: Discrete 5-tier confidence tracking (20%, 40%, 60%, 80%, 100%) alerting learners to dangerous overconfidence gaps (e.g., high confidence on incorrect diagnoses).
5. **Branching Investigation Simulation**: Allows learners to request auxiliary tests (e.g. peripheral blood smear or haemoglobin electrophoresis) before committing to a decision.
6. **English + Telugu Bilingual Support**: Dynamic language toggle with faculty-reviewed medical terminology preserved in standard brackets.

---

## 4. Repository Structure

```
medmind-ai/
├── README.md                          # Project documentation and architectural blueprint
├── run_app.py                         # 1-click launcher for the entire platform
├── docker-compose.yml                 # PostgreSQL + pgvector configuration
├── .env.example                       # Environment variable templates
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI application & SPA static router
│   │   ├── config.py                  # Environment settings
│   │   ├── db.py                      # SQLAlchemy engine & session management
│   │   ├── security.py                # Argon2 password hashing & JWT handling
│   │   ├── models/models.py           # Relational database schema
│   │   ├── schemas/                   # Pydantic v2 validation contracts
│   │   ├── routers/                   # REST endpoints (auth, cases, attempts, teacher)
│   │   └── services/
│   │       ├── case_engine.py         # State machine & student view sanitization
│   │       ├── scoring.py             # Deterministic rubric scoring engine
│   │       ├── misconceptions.py      # Diagnostic error catalog & mapper
│   │       ├── rag.py                 # Guideline retrieval with tag-overlap ranking
│   │       ├── tutor.py               # Grounded tutor with citation validation
│   │       ├── fallback.py            # Pre-reviewed faculty feedback loader
│   │       └── analytics.py           # Calibration and cohort analytics
│   ├── content/
│   │   ├── cases/                     # CASE-FATIGUE-01, CASE-FATIGUE-02, CASE-B12-01
│   │   ├── references/                # Reviewed clinical guideline passages (.md)
│   │   ├── lessons/                   # Targeted misconception micro-lessons (.yaml)
│   │   └── fallback_feedback.yaml     # Reviewed deterministic fallback responses
│   ├── scripts/
│   │   ├── seed_cases.py              # Seeds cases, lessons, and demo cohort data
│   │   └── ingest_references.py       # Ingests and tags guideline references
│   └── tests/
│       ├── test_backend.py            # Unit tests (scoring, state machine, citations)
│       └── test_api_endpoints.py      # Integration tests (complete student & teacher flow)
└── frontend/
    ├── package.json                   # React 18, Vite, Tailwind CSS, Lucide, Recharts
    ├── vite.config.ts                 # Dev server with reverse proxy
    ├── index.html                     # HTML shell with Inter & Noto Sans Telugu
    └── src/
        ├── api/client.ts              # Typed API communication layer
        ├── types/index.ts             # TypeScript interfaces
        ├── i18n/                      # Bilingual English/Telugu dictionary & context
        ├── components/                # Modular UI components (LabTable, DecisionForm, etc.)
        └── pages/                     # Complete application screens
```

---

## 5. Quickstart & Running Locally

### Option A: 1-Click Launch (Recommended)
Run the automated runner from the project root. It will initialize the database, verify seeds, start the server, and automatically open your default browser:

```powershell
python medmind-ai/run_app.py
```

Then visit: **`http://127.0.0.1:8000`**

### Pre-Seeded Demo Accounts:
* **Student Learner**: `student@medmind.ai` / `student123`
* **Clinical Faculty**: `dr.sharma@medmind.ai` / `teacher123`

---

### Option B: Separate Development Servers

**1. Backend Server:**
```powershell
cd medmind-ai/backend
python -m uvicorn app.main:app --reload --port 8000
```
Interactive API Documentation is available at: **`http://127.0.0.1:8000/docs`**

**2. Frontend Dev Server:**
```powershell
cd medmind-ai/frontend
npm run dev
```
Accessible at: **`http://localhost:5173`**

---

## 6. Running the Test Suite

Execute the comprehensive automated test suite with pytest:

```powershell
pytest medmind-ai/backend/tests
```

**Test Coverage Highlights:**
* `test_student_view_hides_answer_key`: Verifies answer keys and rubrics are stripped before submission.
* `test_full_marks_scoring`: Validates accurate scoring of criteria without LLM variance.
* `test_misconception_detection`: Validates triggering of `MC-MACRO-MICRO-CONFUSED` and `MC-OVERCONFIDENT`.
* `test_tutor_validation_rejects_hallucinated_citations`: Guarantees hallucinated citation IDs are blocked.
* `test_student_complete_flow`: End-to-end integration test from login to reassessment.

---

## 7. 4-Minute Presentation Walkthrough Script

| Time | Stage | Action & Key Narrative |
| :--- | :--- | :--- |
| **0:00–0:30** | **Problem & Login** | Explain that medical students need a safe environment to practice reasoning from labs. Click **Quick Demo: Student (Alex Mercer)** to sign in. |
| **0:30–1:15** | **Patient & Labs** | Open *Persistent Fatigue in a Young Adult*. Inspect Alex's history (fatigue, menorrhagia, vegetarian diet) and CBC panel. Click *Request Peripheral Smear* to reveal microcytic hypochromic cells. |
| **1:15–2:00** | **Reasoning & Confidence** | In the Decision Form, choose **Iron-Deficiency Anaemia**. Check **MCV, Ferritin, and RDW** in the evidence checklist. Rate diagnostic confidence at **80%**. Click *Submit*. |
| **2:00–2:45** | **Tutor & References** | Review instant rubric scoring (10/10). Examine AI Tutor feedback showing **Grounded Evidence Cards** (e.g. *REF-IDA-001*). Expand the reference card to demonstrate zero hallucination. |
| **2:45–3:30** | **Targeted Lesson & Transfer** | Click *Proceed to Targeted Lesson* to review red cell indices and answer the formative check question. Proceed to the paired reassessment case (*Jordan - Microcytic Indices with Preserved Iron Stores*) to test concept transfer. |
| **3:30–4:00** | **Progress & Faculty View** | View the **Transfer Comparison Screen** demonstrating score gain (+3.0 delta). Switch to **Faculty Dashboard** (`dr.sharma@medmind.ai`) to show cohort-wide misconception clustering and confidence calibration. |

---

## 8. Educational Safety Principles

> **IMPORTANT DISCLAIMER**
> MEDMIND AI is an **educational simulation platform** designed exclusively for medical and nursing student training.
> * All clinical cases, patient profiles, and laboratory values are synthetic and illustrative.
> * It is **NOT** a medical diagnostic tool and must never be utilized for real patient diagnosis, treatment planning, or emergency triage.
> * The deterministic architecture ensures AI models cannot alter educational scoring or clinical case facts.
