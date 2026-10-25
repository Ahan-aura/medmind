import ssl
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from app.config import settings

db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

if "sqlite" not in db_url:
    # Check driver availability: prefer pg8000 on Python 3.14 or if binary drivers fail
    use_pg8000 = False
    try:
        import psycopg
        if "+psycopg2" in db_url:
            db_url = db_url.replace("+psycopg2", "+psycopg")
        elif not any(driver in db_url for driver in ["+psycopg", "+asyncpg", "+pg8000"]):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    except (ImportError, Exception):
        try:
            import psycopg2
            if not any(driver in db_url for driver in ["+psycopg", "+asyncpg", "+pg8000"]):
                db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        except (ImportError, Exception):
            use_pg8000 = True

    # Fall back to pure-Python pg8000 (which works everywhere without C-extensions or libpq)
    if use_pg8000 or "+pg8000" in db_url or ("postgresql://" in db_url and not any(d in db_url for d in ["+psycopg", "+asyncpg"])):
        try:
            import pg8000
            for driver in ["+psycopg2", "+psycopg"]:
                db_url = db_url.replace(driver, "")
            if not db_url.startswith("postgresql+pg8000://"):
                db_url = db_url.replace("postgresql://", "postgresql+pg8000://", 1)

            # Strip incompatible query params (sslmode, channel_binding) for pg8000
            parsed = urlparse(db_url)
            qs = parse_qs(parsed.query)
            qs.pop('sslmode', None)
            qs.pop('channel_binding', None)
            clean_query = urlencode(qs, doseq=True)
            db_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, clean_query, parsed.fragment))

            # Provide SSL context for encrypted cloud database connection
            connect_args['ssl_context'] = ssl.create_default_context()
        except ImportError:
            pass

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
