import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from app.config import settings
from app.schemas.feedback import Feedback, Citation

_fallback_cache: Optional[Dict[str, Any]] = None

def get_fallback_data() -> Dict[str, Any]:
    global _fallback_cache
    if _fallback_cache is None:
        file_path = settings.FALLBACK_FILE
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                _fallback_cache = yaml.safe_load(f) or {}
        else:
            _fallback_cache = {}
    return _fallback_cache

def load_fallback_feedback(case: Dict[str, Any], result: Dict[str, Any]) -> Feedback:
    data = get_fallback_data()
    fallback_key = case.get('fallback_feedback_key', 'FB-IDA-01')
    case_fallbacks = data.get(fallback_key, {})
    
    misconceptions = result.get('misconceptions', [])
    fb_dict = None
    
    # Try finding matching misconception fallback
    for mc in misconceptions:
        if mc in case_fallbacks:
            fb_dict = case_fallbacks[mc]
            break
            
    if not fb_dict:
        fb_dict = case_fallbacks.get('default')
        
    if not fb_dict:
        # Ultimate fail-safe default
        fb_dict = {
            "what_you_got_right": ["Engaged with the clinical case and submitted structured reasoning."],
            "what_needs_work": ["Review laboratory reference ranges and connect morphological red cell indices with specific etiologies."],
            "why_it_matters": "Careful appraisal of indices prevents diagnostic oversight.",
            "evidence_links": [
                {
                    "ref_id": case.get('allowed_references', ['REF-IDA-001'])[0],
                    "supports": "Clinical practice guidelines for interpreting haematological laboratory investigations."
                }
            ],
            "reflection_prompt": "Consider how your confidence level matched your evidence selection.",
            "next_step": "Proceed to the targeted review module.",
            "uncertainty_note": "Educational simulation only. Not for clinical treatment."
        }
        
    return Feedback(
        what_you_got_right=fb_dict.get("what_you_got_right", []),
        what_needs_work=fb_dict.get("what_needs_work", []),
        why_it_matters=fb_dict.get("why_it_matters", ""),
        evidence_links=[Citation(**c) for c in fb_dict.get("evidence_links", [])],
        reflection_prompt=fb_dict.get("reflection_prompt", ""),
        next_step=fb_dict.get("next_step", ""),
        uncertainty_note=fb_dict.get("uncertainty_note", "Educational simulation only.")
    )
