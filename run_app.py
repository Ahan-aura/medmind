import os
import sys
import webbrowser
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"

def main():
    print("=" * 70)
    print("   MEDMIND AI 2.0 | Clinical Reasoning Practice Simulator")
    print("   Deterministic Evaluation Core + Grounded Evidence AI Tutor")
    print("=" * 70)

    # 1. Ensure sys.path includes backend
    sys.path.insert(0, str(BACKEND_DIR))

    # Auto-generate secure JWT_SECRET if unset for safe local prototyping
    import secrets
    if os.getenv("JWT_SECRET", "") in {"", "change-me", "medmind-super-secure-jwt-secret-key-yukthi-2026"} or len(os.getenv("JWT_SECRET", "")) < 32:
        os.environ["JWT_SECRET"] = secrets.token_urlsafe(48)

    # 2. Check and seed database if needed
    db_file = BACKEND_DIR / "medmind.db"
    if not db_file.exists():
        print("\n[*] Initializing database, seeds, and verified references...")
        from scripts.ingest_references import ingest_references
        from scripts.seed_cases import seed_cases_and_data
        ingest_references()
        seed_cases_and_data()

    # 3. Print access information
    print("\n[+] Server starting on http://127.0.0.1:8000")
    print("[+] Interactive Swagger Docs: http://127.0.0.1:8000/docs")
    print("[+] Pre-seeded Demo Accounts:")
    print("    - Student: student@medmind.ai  /  student123")
    print("    - Faculty: dr.sharma@medmind.ai / teacher123")
    print("[+] Press Ctrl+C to stop the server at any time.\n")

    # 4. Open browser in a separate thread after 1.5s
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000")

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    # 5. Run uvicorn
    import uvicorn
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    main()
