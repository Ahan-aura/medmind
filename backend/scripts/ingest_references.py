import os
import yaml
from pathlib import Path
import sys

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal, engine, Base
from app.models.models import ReferenceChunk
from app.config import settings

def parse_markdown_with_frontmatter(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            metadata = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()
            return metadata, body
            
    return {}, content.strip()

def ingest_references():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    ref_dir = settings.REFERENCES_DIR
    if not ref_dir.exists():
        print(f"Directory {ref_dir} does not exist.")
        return

    md_files = list(ref_dir.glob("*.md"))
    print(f"Found {len(md_files)} reference files to ingest.")
    
    count = 0
    for file_path in md_files:
        meta, text = parse_markdown_with_frontmatter(file_path)
        ref_id = meta.get("id") or file_path.stem
        
        chunk = db.query(ReferenceChunk).filter(ReferenceChunk.id == ref_id).first()
        if not chunk:
            chunk = ReferenceChunk(id=ref_id)
            db.add(chunk)
            
        chunk.source_title = meta.get("source_title", "Clinical Reference")
        chunk.source_url = meta.get("source_url")
        chunk.section = meta.get("section", "General")
        chunk.text = text
        chunk.lang = meta.get("lang", "en")
        chunk.tags = meta.get("tags", [])
        chunk.reviewed = bool(meta.get("reviewed", False))
        count += 1
        
    db.commit()
    db.close()
    print(f"Successfully ingested {count} reference chunks into database.")

if __name__ == "__main__":
    ingest_references()
