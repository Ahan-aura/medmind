import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'medmind.db'}")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "medmind-super-secure-jwt-secret-key-yukthi-2026")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    
    # LLM Settings: Anthropic Claude is the designated provider
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "")  # Must be set explicitly, e.g. claude-3-5-sonnet-20241022
    TUTOR_TIMEOUT_SECONDS: int = int(os.getenv("TUTOR_TIMEOUT_SECONDS", "20"))
    TUTOR_MODE: str = os.getenv("TUTOR_MODE", "auto")  # auto, cached, fallback
    
    # Content paths
    CONTENT_DIR: Path = BASE_DIR / "content"
    CASES_DIR: Path = CONTENT_DIR / "cases"
    REFERENCES_DIR: Path = CONTENT_DIR / "references"
    LESSONS_DIR: Path = CONTENT_DIR / "lessons"
    FALLBACK_FILE: Path = CONTENT_DIR / "fallback_feedback.yaml"

    def get_tutor_mode(self) -> str:
        if self.TUTOR_MODE == "cached":
            return "cached"
        if self.TUTOR_MODE == "fallback":
            return "fallback"
        # auto mode: live only if both key and model are present
        if self.ANTHROPIC_API_KEY and self.LLM_MODEL:
            return "live"
        return "fallback"

settings = Settings()
