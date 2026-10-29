import argparse
import getpass
import sys
from pathlib import Path

# Ensure backend in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.db import SessionLocal
from app.models.models import User
from app.security import hash_password

def main():
    p = argparse.ArgumentParser(description="Create a teacher account with admin/faculty privileges")
    p.add_argument('--email', required=True, help="Teacher email address")
    p.add_argument('--name', required=True, help="Teacher display name")
    a = p.parse_args()

    pw = getpass.getpass('Password (min 12 chars): ')
    assert len(pw) >= 12, "Password must be at least 12 characters"

    with SessionLocal() as db:
        existing = db.query(User).filter(User.email == a.email.lower()).first()
        if existing:
            print(f"Error: User with email {a.email} already exists.")
            sys.exit(1)
        db.add(User(email=a.email.lower(), display_name=a.name, role='teacher', password_hash=hash_password(pw)))
        db.commit()
    print(f"[+] Successfully created teacher account for {a.email}")

if __name__ == "__main__":
    main()
