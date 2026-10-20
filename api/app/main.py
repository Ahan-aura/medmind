import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.db import engine, Base
from app.routers import auth, cases, attempts, lessons, progress, teacher

import logging
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db import get_db

logger = logging.getLogger("medmind")

# Log tutor mode on startup and check for configuration gaps
tutor_mode = settings.get_tutor_mode()
logger.info("MEDMIND AI starting up. Effective Tutor Mode: [%s] (Configured TUTOR_MODE: %s)", tutor_mode, settings.TUTOR_MODE)
if settings.ANTHROPIC_API_KEY and not settings.LLM_MODEL:
    logger.warning("WARNING: ANTHROPIC_API_KEY is configured but LLM_MODEL is not set. Tutor will operate in fallback mode.")

# Ensure database tables exist safely without breaking cold starts if DB is waking up
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.warning("Startup database table check deferred/non-fatal: %s", e)

app = FastAPI(
    title="MEDMIND AI 2.0",
    description="Deterministic Simulation Core + Grounded Evidence AI Tutor API for Clinical Reasoning Practice",
    version="2.0.0"
)

# CORS Middleware
origins = [
    settings.FRONTEND_ORIGIN,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api (for local dev and explicit /api proxy)
app.include_router(auth.router, prefix="/api")
app.include_router(cases.router, prefix="/api")
app.include_router(attempts.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")

# Also include Routers at root (in case serverless rewrites strip the /api prefix)
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(attempts.router)
app.include_router(lessons.router)
app.include_router(progress.router)
app.include_router(teacher.router)

@app.get("/api/health")
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"unhealthy: {e}"

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "service": "MEDMIND AI API",
        "version": "2.0.0",
        "tutor_mode": settings.get_tutor_mode(),
        "database": db_status
    }

# Check if frontend production dist exists to serve as unified SPA
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Do not capture API routes
        if full_path.startswith("api/"):
            return None
        file_candidate = FRONTEND_DIST / full_path
        if file_candidate.is_file():
            return FileResponse(file_candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
else:
    @app.get("/")
    def root():
        return {
            "message": "MEDMIND AI 2.0 API is active. Visit /docs for the interactive Swagger documentation.",
            "health": "/api/health"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
