from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Parse and normalize database URL for PostgreSQL drivers (psycopg2 or psycopg)
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if db_url.startswith("postgresql://") and not any(driver in db_url for driver in ["+psycopg", "+asyncpg"]):
    try:
        import psycopg2
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    except ImportError:
        try:
            import psycopg
            db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
        except ImportError:
            pass

# In SQLite, check_same_thread=False is needed for multithreading
connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
