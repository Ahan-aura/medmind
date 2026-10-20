# MEDMIND AI Backend Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pinned dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY . .

EXPOSE 8000

ENV PORT=8000
ENV HOST=0.0.0.0

# Ingest verified reference passages, verify seed data, then launch uvicorn
CMD ["sh", "-c", "python scripts/ingest_references.py && python scripts/seed_cases.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
