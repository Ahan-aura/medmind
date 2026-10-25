import sys
import os
import traceback
from pathlib import Path

# Add possible paths to sys.path
api_dir = Path(__file__).resolve().parent
root_dir = api_dir.parent
backend_dir = root_dir / "backend"

for candidate in [
    str(api_dir),
    str(backend_dir),
    str(root_dir),
    "/var/task",
    "/var/task/backend",
    "/var/task/api",
    "/var/task/frontend/api"
]:
    if candidate not in sys.path and (os.path.exists(candidate) or candidate.startswith("/var")):
        sys.path.insert(0, candidate)

try:
    from app.main import app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    err_str = str(e)
    tb_str = traceback.format_exc()

    app = FastAPI(title="MedMind Startup Diagnostics")

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def startup_error_catcher(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "MedMind Backend Serverless Startup Failed",
                "exception": err_str,
                "traceback": tb_str,
                "sys_path": sys.path[:8],
                "cwd": os.getcwd()
            }
        )
