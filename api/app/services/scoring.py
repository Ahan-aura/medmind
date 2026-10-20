from typing import Dict, Any, List

def score_attempt(
    case: Dict[str, Any],
    answer: str,
    evidence: List[str],
    reasoning: str,
    confidence: int
) -> Dict[str, Any]:
    options = case.get('options', [])
    correct_opt = next((o for o in options if o.get('correct')), None)
    correct_id = correct_opt['id'] if correct_opt else None
    is_correct = (answer == correct_id)
    
    text = reasoning.lower() if reasoning else ""
    evidence_set = set(evidence) if evidence else set()
    
    rubric = case.get('rubric', {})
    criteria = rubric.get('criteria', [])
    results = []
    total_score = 0.0
    
    for c in criteria:
        chk = c.get('check', {})
        chk_type = chk.get('type')
        met = False
        
        if chk_type == 'answer_is':
            met = (answer == chk.get('value'))
        elif chk_type == 'evidence_includes':
            required_ids = chk.get('ids', [])
            met = all(i in evidence_set for i in required_ids)
        elif chk_type == 'keywords_any':
            groups = chk.get('groups', [])
            # Must have at least one keyword match from each group
            met = all(any(k.lower() in text for k in group) for group in groups)
            
        pts = float(c.get('points', 0)) if met else 0.0
        total_score += pts
        results.append({
            'id': c.get('id'),
            'description': c.get('description'),
            'met': met,
            'points': pts
        })
        
    misconceptions = detect_misconceptions(case, answer, evidence_set, confidence, is_correct)
    
    return {
        'score': total_score,
        'max_score': float(rubric.get('max_score', 10.0)),
        'is_correct': is_correct,
        'criteria': results,
        'misconceptions': misconceptions
    }

def detect_misconceptions(
    case: Dict[str, Any],
    answer: str,
    evidence_set: set,
    confidence: int,
    is_correct: bool
) -> List[str]:
    tags = []
    rules = case.get('misconception_rules', [])
    for rule in rules:
        r_id = rule.get('id')
        w = rule.get('when', {})
        
        fired = False
        if 'answer_in' in w and answer in w['answer_in']:
            fired = True
        elif 'evidence_missing' in w and any(i not in evidence_set for i in w['evidence_missing']):
            fired = True
        elif 'confidence_gte' in w:
            cond_conf = confidence >= w['confidence_gte']
            cond_corr = (is_correct == w.get('is_correct', False))
            if cond_conf and cond_corr:
                fired = True
                
        if fired and r_id not in tags:
            tags.append(r_id)
            
    return tags
