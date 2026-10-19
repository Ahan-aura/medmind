import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.db import engine, Base
from app.routers import auth, cases, attempts, lessons, progress, teacher

# Ensure all database tables exist
Base.metadata.create_all(bind=engine)

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

# Include Routers under /api
app.include_router(auth.router, prefix="/api")
app.include_router(cases.router, prefix="/api")
app.include_router(attempts.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "MEDMIND AI API",
        "version": "2.0.0",
        "tutor_mode": settings.TUTOR_MODE,
        "database": "connected"
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
