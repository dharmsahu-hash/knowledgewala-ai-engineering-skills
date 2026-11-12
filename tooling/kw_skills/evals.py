"""Skill evaluation scoring (real-world quality layer).

A human or a recorded evaluation run supplies per-criterion scores (0-10) with
a written rationale; this module validates them against a rubric and computes
a weighted score out of 100. It does not call any model: scores must come from
an actual evaluation, never be invented.
"""
from __future__ import annotations

import json
from pathlib import Path


def score(rubric_path: Path, scores_path: Path) -> dict:
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    scores = json.loads(scores_path.read_text(encoding="utf-8"))
    crit = {c["id"]: c for c in rubric["criteria"]}
    total_w = sum(c["weight"] for c in crit.values())
    if total_w != 100:
        raise ValueError(f"rubric weights must sum to 100 (got {total_w})")
    rows, errs = [], []
    for cid, c in crit.items():
        s = scores.get("scores", {}).get(cid)
        if not s:
            errs.append(f"missing score for '{cid}'")
            continue
        v = s.get("score")
        if not isinstance(v, (int, float)) or not 0 <= v <= 10:
            errs.append(f"'{cid}': score must be 0-10")
            continue
        if not str(s.get("rationale", "")).strip():
            errs.append(f"'{cid}': rationale is required")
            continue
        rows.append({"id": cid, "weight": c["weight"], "score": v, "points": round(v / 10 * c["weight"], 1), "rationale": s["rationale"]})
    if errs:
        raise ValueError("; ".join(errs))
    if not scores.get("evaluator") or not scores.get("run_date"):
        raise ValueError("scores file needs 'evaluator' and 'run_date' (who actually ran the evaluation, and when)")
    return {"rubric": rubric["name"], "total": round(sum(r["points"] for r in rows), 1), "out_of": 100, "criteria": rows,
            "evaluator": scores["evaluator"], "run_date": scores["run_date"]}
