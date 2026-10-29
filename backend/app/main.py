import sys
import os
from pathlib import Path

# Bootstrap sys.path for direct serverless function execution on Vercel
_main_dir = Path(__file__).resolve().parent
for _candidate in [
    str(_main_dir.parent),                 # directory containing 'app' (e.g. .../api or .../backend)
    str(_main_dir.parent.parent),          # repo root
    "/var/task",
    "/var/task/api",
    "/var/task/backend",
    "/var/task/frontend/api",
]:
    if _candidate not in sys.path and (os.path.exists(_candidate) or _candidate.startswith("/var")):
        sys.path.insert(0, _candidate)

from fastapi import FastAPI, Request, HTTPException
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

# Ensure database tables exist safely and default data is seeded
try:
    Base.metadata.create_all(bind=engine)
    from app.services.seed import ensure_seeded
    ensure_seeded()
except Exception as e:
    logger.warning("Startup database table check/seed deferred/non-fatal: %s", e)

app = FastAPI(
    title="MEDMIND AI 2.0",
    description="Deterministic Simulation Core + Grounded Evidence AI Tutor API for Clinical Reasoning Practice",
    version="2.0.0",
    redirect_slashes=False
)

class VercelForwardedUriMiddleware:
    """
    On Vercel serverless, proxy rewrites (e.g. /api/cases/(.*) -> /api/cases)
    pass the original requested path in x-matched-path or x-forwarded-uri.
    This middleware synchronizes scope['path'] to the true requested endpoint.
    """
    def __init__(self, app_instance):
        self.app = app_instance

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope.get("headers", [])}
            original_path = (
                headers.get("x-matched-path")
                or headers.get("x-forwarded-uri")
                or headers.get("x-original-uri")
            )
            if original_path:
                clean_path = original_path.split("?")[0]
                current_path = scope.get("path", "")
                if clean_path and clean_path != current_path:
                    scope["path"] = clean_path
        await self.app(scope, receive, send)

app.add_middleware(VercelForwardedUriMiddleware)

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.limiter import limiter

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Response security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:;"
    return response

# CORS Middleware (strict origins, allow_credentials=False for bearer auth)
allowed_origins = [settings.FRONTEND_ORIGIN]
if os.getenv("ENVIRONMENT", "development") == "development":
    allowed_origins.extend(["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "http://127.0.0.1:8000"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(set(allowed_origins)),
    allow_credentials=False,
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

@app.get("/api/debug-routes")
@app.get("/debug-routes")
def debug_routes(request: Request):
    return {
        "status": "ok",
        "url_path": request.url.path,
        "scope_path": request.scope.get("path"),
        "headers": {k: v for k, v in request.headers.items() if k.lower() not in ("authorization", "cookie")},
        "routes": [f"{getattr(r, 'methods', '')} {getattr(r, 'path', '')}" for r in app.routes]
    }

# Entrypoint root routes
@app.get("/api")
@app.get("/api/")
@app.get("/api/index")
@app.get("/index")
@app.get("/")
def root():
    return {
        "message": "MEDMIND AI 2.0 API is active. Visit /docs for the interactive Swagger documentation.",
        "health": "/api/health"
    }

# Check if frontend production dist exists to serve as unified SPA in local dev
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists() and not os.getenv("VERCEL"):
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_spa(full_path: str):
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(404, "Not found")
        index = FRONTEND_DIST / "index.html"
        if not index.is_file():
            raise HTTPException(404, "Frontend not built")
        candidate = (FRONTEND_DIST / full_path).resolve()
        if candidate.is_file() and candidate.is_relative_to(FRONTEND_DIST):
            return FileResponse(candidate)
        return FileResponse(index)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
