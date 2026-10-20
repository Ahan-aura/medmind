from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Attempt, Case, LearnerMisconception, Misconception, User

def get_learner_progress(db: Session, user: User) -> Dict[str, Any]:
    # 1. Fetch completed or submitted attempts for this learner
    attempts = db.query(Attempt).filter(
        Attempt.user_id == user.id,
        Attempt.score != None
    ).order_by(Attempt.started_at.asc()).all()
    
    # Map by case_id
    attempts_by_case = {}
    for a in attempts:
        attempts_by_case[a.case_id] = a
        
    # Map pairs by learning_objective
    cases = db.query(Case).all()
    case_map = {c.id: c for c in cases}
    
    objectives_dict: Dict[str, Dict[str, Any]] = {}
    for c in cases:
        lo = c.learning_objective
        if lo not in objectives_dict:
            objectives_dict[lo] = {
                "learning_objective": lo,
                "initial_score": None,
                "initial_max": None,
                "reassessment_score": None,
                "reassessment_max": None,
                "delta": None,
                "criteria_newly_met": [],
                "initial_attempt_id": None,
                "reassessment_attempt_id": None
            }
            
        att = attempts_by_case.get(c.id)
        if att:
            if c.case_role == 'initial':
                objectives_dict[lo]["initial_score"] = att.score
                objectives_dict[lo]["initial_max"] = att.max_score
                objectives_dict[lo]["initial_attempt_id"] = att.id
                objectives_dict[lo]["_init_crit"] = att.criteria_results or []
            elif c.case_role == 'reassessment':
                objectives_dict[lo]["reassessment_score"] = att.score
                objectives_dict[lo]["reassessment_max"] = att.max_score
                objectives_dict[lo]["reassessment_attempt_id"] = att.id
                objectives_dict[lo]["_reassess_crit"] = att.criteria_results or []

    # Calculate delta and newly met criteria
    objectives_list = []
    for lo, data in objectives_dict.items():
        if data["initial_score"] is not None and data["reassessment_score"] is not None:
            data["delta"] = round(data["reassessment_score"] - data["initial_score"], 1)
            init_met = {c.get("id") for c in data.get("_init_crit", []) if c.get("met")}
            reassess_met = [c.get("description", c.get("id")) for c in data.get("_reassess_crit", []) if c.get("met") and c.get("id") not in init_met]
            data["criteria_newly_met"] = reassess_met
        data.pop("_init_crit", None)
        data.pop("_reassess_crit", None)
        objectives_list.append(data)

    # 2. Calibration calculation
    bins = {20: [], 40: [], 60: [], 80: [], 100: []}
    calib_summary = {"overconfident": 0, "underconfident": 0, "calibrated": 0}
    
    for a in attempts:
        conf = a.confidence
        corr = a.is_correct
        if conf is not None and corr is not None:
            # find closest bin
            closest_bin = min(bins.keys(), key=lambda b: abs(b - conf))
            bins[closest_bin].append(1.0 if corr else 0.0)
            
            if conf >= 80 and not corr:
                calib_summary["overconfident"] += 1
            elif conf <= 40 and corr:
                calib_summary["underconfident"] += 1
            else:
                calib_summary["calibrated"] += 1

    calibration_points = []
    for b_val in [20, 40, 60, 80, 100]:
        acc_list = bins[b_val]
        accuracy = (sum(acc_list) / len(acc_list) * 100.0) if acc_list else 0.0
        calibration_points.append({
            "confidence_bin": b_val,
            "accuracy": round(accuracy, 1),
            "count": len(acc_list)
        })

    # 3. Misconceptions
    misconceptions_db = db.query(LearnerMisconception, Misconception).join(
        Misconception, LearnerMisconception.misconception_id == Misconception.id
    ).filter(LearnerMisconception.user_id == user.id).all()
    
    misconception_items = []
    for lm, m in misconceptions_db:
        misconception_items.append({
            "id": m.id,
            "name": m.name,
            "times_seen": lm.times_seen,
            "last_seen_at": lm.last_seen_at.isoformat() if lm.last_seen_at else None
        })

    return {
        "user_id": user.id,
        "display_name": user.display_name,
        "objectives": objectives_list,
        "calibration": calibration_points,
        "calibration_summary": calib_summary,
        "misconceptions": misconception_items
    }

def get_cohort_summary(db: Session, cohort_id: str) -> Dict[str, Any]:
    # Get students in cohort
    students = db.query(User).filter(User.cohort_id == cohort_id).all()
    student_ids = [s.id for s in students]
    student_count = len(students)
    has_synthetic_data = any(bool(getattr(s, 'is_synthetic', False)) for s in students)
    
    # 1. Objective averages
    # Initial vs Reassessment average
    cases = db.query(Case).all()
    obj_stats: Dict[str, Dict[str, Any]] = {}
    
    for c in cases:
        lo = c.learning_objective
        if lo not in obj_stats:
            obj_stats[lo] = {
                "learning_objective": lo,
                "initial_total": 0.0,
                "initial_count": 0,
                "reassessment_total": 0.0,
                "reassessment_count": 0
            }
            
        attempts = db.query(Attempt).filter(
            Attempt.case_id == c.id,
            Attempt.user_id.in_(student_ids),
            Attempt.score != None
        ).all()
        
        for a in attempts:
            if a.max_score and a.max_score > 0:
                pct = (a.score / a.max_score) * 100.0
                if c.case_role == 'initial':
                    obj_stats[lo]["initial_total"] += pct
                    obj_stats[lo]["initial_count"] += 1
                else:
                    obj_stats[lo]["reassessment_total"] += pct
                    obj_stats[lo]["reassessment_count"] += 1

    obj_averages = []
    for lo, s in obj_stats.items():
        avg_init = round(s["initial_total"] / s["initial_count"], 1) if s["initial_count"] > 0 else 0.0
        avg_re = round(s["reassessment_total"] / s["reassessment_count"], 1) if s["reassessment_count"] > 0 else 0.0
        obj_averages.append({
            "learning_objective": lo,
            "avg_initial_score": avg_init,
            "avg_reassessment_score": avg_re,
            "delta": round(avg_re - avg_init, 1),
            "learner_count": max(s["initial_count"], s["reassessment_count"])
        })

    # 2. Top misconceptions in cohort
    top_mc_rows = db.query(
        Misconception.name,
        func.count(LearnerMisconception.user_id).label("student_count")
    ).join(
        LearnerMisconception, Misconception.id == LearnerMisconception.misconception_id
    ).filter(
        LearnerMisconception.user_id.in_(student_ids)
    ).group_by(
        Misconception.name
    ).order_by(
        func.count(LearnerMisconception.user_id).desc()
    ).limit(5).all()

    top_misconceptions = [
        {"name": row[0], "students": row[1]} for row in top_mc_rows
    ]

    # 3. Calibration matrix across cohort
    bins = {20: [], 40: [], 60: [], 80: [], 100: []}
    cohort_attempts = db.query(Attempt).filter(
        Attempt.user_id.in_(student_ids),
        Attempt.confidence != None,
        Attempt.is_correct != None
    ).all()
    
    for a in cohort_attempts:
        closest_bin = min(bins.keys(), key=lambda b: abs(b - a.confidence))
        bins[closest_bin].append(1.0 if a.is_correct else 0.0)
        
    calib_matrix = []
    for b_val in [20, 40, 60, 80, 100]:
        acc_list = bins[b_val]
        acc = (sum(acc_list) / len(acc_list) * 100.0) if acc_list else 0.0
        calib_matrix.append({
            "confidence_bin": b_val,
            "accuracy": round(acc, 1),
            "total_attempts": len(acc_list)
        })

    return {
        "cohort_id": cohort_id,
        "cohort_name": "Class 2026 - Clinical Medicine Cohort Alpha",
        "student_count": student_count,
        "has_synthetic_data": has_synthetic_data,
        "objective_averages": obj_averages,
        "top_misconceptions": top_misconceptions,
        "calibration_matrix": calib_matrix
    }
