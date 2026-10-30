from typing import Dict, Any, Optional

MISCONCEPTIONS_REGISTRY: Dict[str, Dict[str, Any]] = {
    "MC-MICRO-DIFFERENTIAL": {
        "name": "Failure to Distinguish Thalassaemia Trait from Iron Deficiency",
        "description": "Learner did not utilize RDW, red blood cell count, or ferritin to differentiate globin chain synthesis defects from substrate starvation.",
        "lesson_id": "LESSON-04",
        "priority": 9
    },
    "MC-MACRO-CAUSE-MISSED": {
        "name": "Overlooking Underlying Etiology in Macrocytosis",
        "description": "Learner failed to evaluate blood smear characteristics or distinguish megaloblastic from non-megaloblastic causes.",
        "lesson_id": "LESSON-05",
        "priority": 8
    },
    "MC-WASTEFUL-TESTING": {
        "name": "Ordering Low-Yield or Indiscriminate Laboratory Testing",
        "description": "Learner requested excessive or low-value diagnostic panels before evaluating primary cell size morphology or basic indices.",
        "lesson_id": "LESSON-06",
        "priority": 7
    },
    "MC-PREMATURE-CLOSURE": {
        "name": "Premature Diagnostic Closure and Heuristic Anchoring",
        "description": "Learner accepted an initial diagnostic hunch without evaluating contradictory red cell indices or exploring dual pathology.",
        "lesson_id": "LESSON-07",
        "priority": 8
    },
    "MC-MISSED-DANGEROUS-ALTERNATIVE": {
        "name": "Halting at Symptom Level Without Investigating Underlying Etiology",
        "description": "Learner diagnosed iron deficiency but neglected red-flag clinical features or failed to escalate for occult blood loss.",
        "lesson_id": "LESSON-08",
        "priority": 10
    },
    "MC-MACRO-MICRO-CONFUSED": {
        "name": "Confusion Between Microcytic and Macrocytic Anaemias",
        "description": "Learner selected a macrocytic diagnosis (e.g. B12 deficiency) despite laboratory evidence of microcytosis (MCV < 80 fL).",
        "lesson_id": "LESSON-02",
        "priority": 10
    },
    "MC-IGNORES-INDICES": {
        "name": "Omission of Red Blood Cell Indices",
        "description": "Learner reached a diagnostic decision without incorporating MCV or RDW into their clinical evidence.",
        "lesson_id": "LESSON-01",
        "priority": 8
    },
    "MC-FERRITIN-MISSED": {
        "name": "Failure to Evaluate Body Iron Stores",
        "description": "Learner failed to evaluate serum ferritin, the key biomarker distinguishing iron deficiency from thalassaemia trait.",
        "lesson_id": "LESSON-03",
        "priority": 9
    },
    "MC-DEFAULT-TO-IDA": {
        "name": "Defaulting to Iron Deficiency Without Preserved Store Check",
        "description": "Learner assumed all microcytic anaemia is iron deficiency, overlooking normal ferritin and uniform cell size in thalassaemia.",
        "lesson_id": "LESSON-03",
        "priority": 9
    },
    "MC-IGNORES-RDW": {
        "name": "Overlooking Anisocytosis Index (RDW)",
        "description": "Learner did not utilize RDW to distinguish heterogeneous iron deficiency from uniform thalassaemic cells.",
        "lesson_id": "LESSON-01",
        "priority": 7
    },
    "MC-OVERCONFIDENT": {
        "name": "High Diagnostic Confidence with Flawed Reasoning",
        "description": "Learner reported 80%+ confidence while submitting an incorrect or inadequately supported interpretation.",
        "lesson_id": "LESSON-07",
        "priority": 6
    },
    "MC-FOLATE-B12-CONFUSED": {
        "name": "Conflation of Folate and Cobalamin Deficiencies",
        "description": "Learner diagnosed isolated folate deficiency despite marked sensory/neurological deficits and low cobalamin.",
        "lesson_id": "LESSON-02",
        "priority": 8
    },
    "MC-IGNORES-NEUROLOGICAL": {
        "name": "Overlooking Neurological Signs in Megaloblastosis",
        "description": "Learner did not link paresthesias and ataxia to subacute combined degeneration in Vitamin B12 deficiency.",
        "lesson_id": "LESSON-02",
        "priority": 7
    }
}

def get_recommended_lesson(tags: list, learning_objective: str) -> Optional[str]:
    if not tags:
        # Default lesson based on learning objective
        if "MICROCYTIC" in learning_objective:
            return "LESSON-MICROCYTIC-INDICES"
        return "LESSON-MACRO-VS-MICRO"
    
    # Sort tags by priority
    sorted_tags = sorted(
        tags,
        key=lambda t: MISCONCEPTIONS_REGISTRY.get(t, {}).get("priority", 0),
        reverse=True
    )
    for tag in sorted_tags:
        lesson_id = MISCONCEPTIONS_REGISTRY.get(tag, {}).get("lesson_id")
        if lesson_id:
            return lesson_id
            
    return "LESSON-MICROCYTIC-INDICES"
