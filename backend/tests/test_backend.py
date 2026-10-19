import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import yaml

from app.services.case_engine import student_view, take_step, require_state
from app.services.scoring import score_attempt
from app.services.tutor import is_valid_feedback
from app.schemas.feedback import Feedback, Citation

@pytest.fixture
def sample_case():
    case_path = Path(__file__).resolve().parent.parent / "content" / "cases" / "CASE-FATIGUE-01.yaml"
    with open(case_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def test_student_view_hides_answer_key(sample_case):
    view = student_view(sample_case)
    assert 'rubric' not in view
    assert 'misconception_rules' not in view
    assert 'allowed_references' not in view
    assert 'fallback_feedback_key' not in view
    assert all('correct' not in o for o in view['options'])
    assert len(view['options']) == len(sample_case['options'])

def test_full_marks_scoring(sample_case):
    result = score_attempt(
        case=sample_case,
        answer='A',
        evidence=['mcv', 'ferritin', 'rdw'],
        reasoning='Microcytic hypochromic cells with low ferritin due to blood loss and dietary factors.',
        confidence=80
    )
    assert result['score'] == 10.0
    assert result['is_correct'] is True
    assert len(result['misconceptions']) == 0

def test_misconception_detection(sample_case):
    # Student chose B (B12 deficiency) with high confidence 90% and missed ferritin
    result = score_attempt(
        case=sample_case,
        answer='B',
        evidence=['hb'],
        reasoning='Patient is feeling tired and weak.',
        confidence=90
    )
    assert result['is_correct'] is False
    assert 'MC-MACRO-MICRO-CONFUSED' in result['misconceptions']
    assert 'MC-IGNORES-INDICES' in result['misconceptions']
    assert 'MC-FERRITIN-MISSED' in result['misconceptions']
    assert 'MC-OVERCONFIDENT' in result['misconceptions']

def test_branching_step(sample_case):
    next_node_id, flags, next_node = take_step(sample_case, "n_review", "more_info")
    assert next_node_id == "n_smear"
    assert next_node is not None
    assert "reveal" in next_node or "text" in next_node

def test_state_machine_enforcement():
    # step allowed in STARTED
    require_state("STARTED", "step")
    require_state("STARTED", "submit")
    
    # submit NOT allowed in SUBMITTED
    with pytest.raises(Exception):
        require_state("SUBMITTED", "submit")

def test_tutor_validation_rejects_hallucinated_citations(sample_case):
    fb = Feedback(
        what_you_got_right=["Good work"],
        what_needs_work=["Check indices"],
        why_it_matters="Pathophysiology matters",
        evidence_links=[Citation(ref_id="REF-FAKE-999", supports="Invented citation")],
        reflection_prompt="Reflect on confidence",
        next_step="Lesson",
        uncertainty_note="Educational note"
    )
    allowed = {"REF-IDA-001", "REF-IDA-002"}
    assert not is_valid_feedback(fb, allowed, sample_case, [])
