from fastapi import HTTPException
from typing import Dict, Any, Tuple, List

ALLOWED = {
    'STARTED': {'step', 'submit'},
    'SUBMITTED': {'feedback'},
    'FEEDBACK_READY': {'lesson', 'reassess'},
    'LESSON_DONE': {'reassess'},
    'COMPLETED': set(),
}

def require_state(attempt_state: str, action: str):
    allowed_actions = ALLOWED.get(attempt_state, set())
    if action not in allowed_actions:
        raise HTTPException(
            status_code=409,
            detail=f"Action '{action}' is not allowed in current attempt state '{attempt_state}'"
        )

HIDDEN_FIELDS = {'rubric', 'misconception_rules', 'fallback_feedback_key', 'allowed_references'}

def student_view(case_data: Dict[str, Any]) -> Dict[str, Any]:
    """Strips answer key, rubric, and internal configuration so learner cannot inspect them."""
    view = {k: v for k, v in case_data.items() if k not in HIDDEN_FIELDS}
    if 'options' in view:
        view['options'] = [{'id': o['id'], 'text': o['text']} for o in view['options']]
    return view

def take_step(case_data: Dict[str, Any], current_node_id: str, choice_id: str) -> Tuple[str, List[str], Dict[str, Any]]:
    branching = case_data.get('branching', {})
    nodes = branching.get('nodes', [])
    node = next((n for n in nodes if n['id'] == current_node_id), None)
    if node is None:
        raise HTTPException(status_code=400, detail=f"Node '{current_node_id}' not found in case branching")
    
    choices = node.get('choices', [])
    choice = next((c for c in choices if c['id'] == choice_id), None)
    if choice is None:
        raise HTTPException(status_code=400, detail=f"Choice '{choice_id}' is not valid for node '{current_node_id}'")
    
    next_node_id = choice['next']
    flags = choice.get('flags', [])
    
    next_node = next((n for n in nodes if n['id'] == next_node_id), None)
    return next_node_id, flags, next_node
