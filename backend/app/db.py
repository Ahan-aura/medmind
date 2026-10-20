from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from app.config import settings

# Parse and normalize database URL for PostgreSQL drivers (psycopg v3, psycopg2, or pg8000)
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Prefer psycopg (v3) over psycopg2 because psycopg doesn't rely on external C libpq.so on serverless
if "+psycopg2" in db_url:
    try:
        import psycopg
        db_url = db_url.replace("+psycopg2", "+psycopg")
    except ImportError:
        pass
elif db_url.startswith("postgresql://") and not any(driver in db_url for driver in ["+psycopg", "+asyncpg", "+pg8000"]):
    try:
        import psycopg
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    except ImportError:
        try:
            import psycopg2
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        except ImportError:
            pass

# In SQLite, check_same_thread=False is needed for multithreading
connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

engine_kwargs = {
    "echo": False,
    "connect_args": connect_args,
}

if "sqlite" not in db_url:
    # Use NullPool for serverless / pooled cloud PostgreSQL (e.g. Neon) to avoid stale socket reuse
    engine_kwargs["poolclass"] = NullPool

engine = create_engine(
    db_url,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
