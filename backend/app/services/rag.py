"""
Curated reference retrieval (tag + keyword ranking over reviewed passages).
Restricts passages strictly to verified references mapped to the active case.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import ReferenceChunk

def retrieve_references(
    db: Session,
    case: Dict[str, Any],
    missed_criteria: List[str],
    tags: List[str],
    k: int = 4
) -> List[ReferenceChunk]:
    """
    Curated reference retrieval (tag + keyword ranking over reviewed passages).
    Filters exclusively for reviewed passages belonging to the case's allowed_references,
    then ranks by tag overlap and keyword occurrences.
    """
    allowed_ids = case.get('allowed_references', [])
    if not allowed_ids:
        return []
    
    # Query approved chunks restricted strictly to allowed_references for this case
    query = db.query(ReferenceChunk).filter(
        ReferenceChunk.reviewed == True,
        ReferenceChunk.id.in_(allowed_ids)
    )
    all_chunks = query.all()
    
    # Curated ranking: Tag overlap score + keyword match score over reviewed passages
    search_keywords = set()
    for tag in tags:
        search_keywords.update(tag.lower().replace("mc-", "").replace("-", " ").split())
    for crit in missed_criteria:
        search_keywords.update(crit.lower().split())
    if case.get('title'):
        search_keywords.update(case['title'].lower().split())
        
    tag_set = set(t.lower() for t in tags)
    
    def score_chunk(chunk: ReferenceChunk) -> float:
        chunk_tags = set(t.lower() for t in (chunk.tags or []))
        tag_overlap = len(chunk_tags.intersection(tag_set))
        
        text_lower = (chunk.text + " " + chunk.source_title + " " + (chunk.section or "")).lower()
        keyword_hits = sum(1 for kw in search_keywords if len(kw) > 3 and kw in text_lower)
        
        # Priority weighting: tag overlap prioritized, followed by keyword hits
        return tag_overlap * 10.0 + keyword_hits * 1.0

    scored = sorted(all_chunks, key=score_chunk, reverse=True)
    return scored[:k]
