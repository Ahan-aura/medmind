import sys
from pathlib import Path

_api_dir = Path(__file__).resolve().parent.parent
for _p in [str(_api_dir), str(_api_dir.parent), "/var/task", "/var/task/api", "/var/task/frontend/api"]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from app.main import app
