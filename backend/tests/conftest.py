import sys
import os
import tempfile
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

os.environ["JWT_SECRET"] = "test-secret-" + "x" * 40
os.environ["TUTOR_MODE"] = "fallback"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
import app.db as db_module
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Creates an isolated temporary SQLite database and seeds reference chunks,
    cases, lessons, and demo user accounts so tests pass reliably on a clean clone.
    """
    temp_dir = tempfile.mkdtemp()
    temp_db_path = os.path.join(temp_dir, "test_medmind_suite.db")
    test_db_url = f"sqlite:///{temp_db_path}"

    test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Create tables
    Base.metadata.create_all(bind=test_engine)

    # Patch database engine and SessionLocal for seed scripts
    orig_engine = db_module.engine
    orig_session = db_module.SessionLocal

    db_module.engine = test_engine
    db_module.SessionLocal = TestingSessionLocal

    import scripts.seed_cases as seed_cases_module
    import scripts.ingest_references as ingest_ref_module
    import scripts.seed_demo_data as seed_demo_module

    seed_cases_module.engine = test_engine
    seed_cases_module.SessionLocal = TestingSessionLocal
    ingest_ref_module.engine = test_engine
    ingest_ref_module.SessionLocal = TestingSessionLocal
    seed_demo_module.engine = test_engine
    seed_demo_module.SessionLocal = TestingSessionLocal

    # Seed reference passages, cases, and demo peers
    ingest_ref_module.ingest_references()
    seed_cases_module.seed_cases_and_data()
    seed_demo_module.seed_synthetic_demo_data(force=True)

    # Override get_db in FastAPI app
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal

    # Clean up
    app.dependency_overrides.clear()
    db_module.engine = orig_engine
    db_module.SessionLocal = orig_session

    try:
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
    except Exception:
        pass
