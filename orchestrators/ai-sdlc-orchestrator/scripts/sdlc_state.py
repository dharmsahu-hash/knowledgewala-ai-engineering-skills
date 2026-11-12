#!/usr/bin/env python3
"""Lifecycle state and gate enforcement for the AI SDLC Orchestrator.

Keeps a small JSON file (default .kw-sdlc/state.json) so stage order and human
approvals are enforced by code rather than by the model's good intentions.
Local file only: no network, no subprocess, no deletion.

Commands: init, status, complete, approve, flag, resolve, risk
Exit codes: 0 ok, 1 refused by a rule, 2 usage/IO error.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# (id, specialist skill, gate that must be approved before the stage can complete)
STAGES = [
    ("requirement-analysis", "requirement-analysis", None),
    ("requirement-approval", "human", "requirements"),
    ("architecture-design", "solution-architecture", "architecture"),
    ("hld", "hld-generator", None),
    ("lld", "lld-generator", None),
    ("implementation-planning", "ai-sdlc-orchestrator", "plan"),
    ("task-decomposition", "ai-sdlc-orchestrator", None),
    ("specialist-delegation", "java-engineering|spring-boot-engineering|database-engineering", None),
    ("code-generation", "java-engineering|spring-boot-engineering", None),
    ("unit-tests", "test-engineering", None),
    ("integration-tests", "test-engineering", None),
    ("security-assessment", "security specialist or code-review", None),
    ("code-review", "code-review", None),
    ("defect-resolution", "specialist skills", None),
    ("release-readiness", "ai-sdlc-orchestrator", "release"),
    ("documentation", "ai-sdlc-orchestrator", None),
]
STAGE_IDS = [s[0] for s in STAGES]
GATES = {"requirements", "architecture", "plan", "release"}
FLAG_KINDS = {"major-architecture", "destructive-db", "security-sensitive", "production-deploy", "secrets", "scope-change"}
NOT_HUMAN = {"claude", "ai", "assistant", "agent", "model", "orchestrator", "llm", "bot"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"error: {path} not found; run 'init' first")
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, st: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(st, indent=2) + "\n", encoding="utf-8")


def refuse(msg: str) -> int:
    print(f"REFUSED: {msg}", file=sys.stderr)
    return 1


def human(name: str) -> str | None:
    name = (name or "").strip()
    if len(name) < 2 or name.lower() in NOT_HUMAN:
        return None
    return name


def cmd_init(a, p):
    if p.exists():
        return refuse(f"{p} already exists; refusing to overwrite")
    st = {"project": a.project, "created": now(), "stages": {s: {"status": "pending"} for s in STAGE_IDS},
          "approvals": {}, "flags": [], "risks": [], "history": []}
    save(p, st)
    print(f"initialised {p} with {len(STAGE_IDS)} stages")
    return 0


def cmd_status(a, p):
    st = load(p)
    if a.json:
        print(json.dumps(st, indent=2))
        return 0
    print(f"project: {st['project']}")
    for s, skill, gate in STAGES:
        e = st["stages"][s]
        g = f"  [gate: {gate} {'approved' if gate in st['approvals'] else 'NOT approved'}]" if gate else ""
        print(f"  {e['status']:<9} {s:<24} -> {skill}{g}")
    pend = [f for f in st["flags"] if f["status"] == "pending"]
    print(f"pending approvals: {len(pend)}" + "".join(f"\n  - #{f['id']} {f['kind']}: {f['reason']}" for f in pend))
    print(f"open risks: {sum(1 for r in st['risks'] if r['status'] == 'open')}")
    return 0


def cmd_complete(a, p):
    st = load(p)
    if a.stage not in STAGE_IDS:
        return refuse(f"unknown stage '{a.stage}'. Stages: {', '.join(STAGE_IDS)}")
    if st["stages"][a.stage]["status"] == "complete":
        return refuse(f"stage '{a.stage}' is already complete")
    idx = STAGE_IDS.index(a.stage)
    for prev in STAGE_IDS[:idx]:
        if st["stages"][prev]["status"] != "complete":
            return refuse(f"stage '{prev}' must be complete before '{a.stage}' (stages cannot be skipped)")
    pend = [f for f in st["flags"] if f["status"] == "pending"]
    if pend:
        return refuse(f"{len(pend)} pending human approval(s) block progress, e.g. #{pend[0]['id']} {pend[0]['kind']}")
    if len((a.evidence or "").strip()) < 10:
        return refuse("--evidence is required (what was produced or which command ran with what result)")
    gate = STAGES[idx][2]
    if gate and gate not in st["approvals"]:
        return refuse(f"gate '{gate}' needs human approval first: approve {gate} --by <human name>")
    st["stages"][a.stage] = {"status": "complete", "evidence": a.evidence.strip(), "at": now()}
    st["history"].append({"at": now(), "event": "complete", "stage": a.stage})
    save(p, st)
    print(f"completed {a.stage}")
    return 0


def cmd_approve(a, p):
    st = load(p)
    if a.gate not in GATES:
        return refuse(f"unknown gate '{a.gate}'. Gates: {', '.join(sorted(GATES))}")
    who = human(a.by)
    if not who:
        return refuse("--by must be the name of the human approver; an AI cannot approve a gate")
    st["approvals"][a.gate] = {"by": who, "note": a.note or "", "at": now()}
    st["history"].append({"at": now(), "event": "approve", "gate": a.gate, "by": who})
    save(p, st)
    print(f"gate '{a.gate}' approved by {who}")
    return 0


def cmd_flag(a, p):
    st = load(p)
    if a.kind not in FLAG_KINDS:
        return refuse(f"unknown kind '{a.kind}'. Kinds: {', '.join(sorted(FLAG_KINDS))}")
    fid = len(st["flags"]) + 1
    st["flags"].append({"id": fid, "kind": a.kind, "reason": a.reason, "status": "pending", "at": now()})
    st["history"].append({"at": now(), "event": "flag", "id": fid, "kind": a.kind})
    save(p, st)
    print(f"flag #{fid} ({a.kind}) raised; work is blocked until a human resolves it")
    return 0


def cmd_resolve(a, p):
    st = load(p)
    who = human(a.by)
    if not who:
        return refuse("--by must be the name of the human decision-maker; an AI cannot resolve a flag")
    hit = [f for f in st["flags"] if f["id"] == a.id and f["status"] == "pending"]
    if not hit:
        return refuse(f"no pending flag #{a.id}")
    hit[0].update(status="approved" if a.decision == "approve" else "rejected", by=who, resolved_at=now())
    st["history"].append({"at": now(), "event": "resolve", "id": a.id, "decision": a.decision, "by": who})
    save(p, st)
    print(f"flag #{a.id} {hit[0]['status']} by {who}")
    return 0


def cmd_risk(a, p):
    st = load(p)
    st["risks"].append({"id": len(st["risks"]) + 1, "text": a.text, "status": "open", "at": now()})
    save(p, st)
    print(f"risk #{len(st['risks'])} recorded")
    return 0


def build() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", default=".kw-sdlc/state.json")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("--project", required=True); s.set_defaults(fn=cmd_init)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    s = sub.add_parser("complete"); s.add_argument("stage"); s.add_argument("--evidence", default=""); s.set_defaults(fn=cmd_complete)
    s = sub.add_parser("approve"); s.add_argument("gate"); s.add_argument("--by", default=""); s.add_argument("--note"); s.set_defaults(fn=cmd_approve)
    s = sub.add_parser("flag"); s.add_argument("kind"); s.add_argument("--reason", required=True); s.set_defaults(fn=cmd_flag)
    s = sub.add_parser("resolve"); s.add_argument("id", type=int); s.add_argument("--decision", choices=["approve", "reject"], required=True); s.add_argument("--by", default=""); s.set_defaults(fn=cmd_resolve)
    s = sub.add_parser("risk"); s.add_argument("text"); s.set_defaults(fn=cmd_risk)
    return ap


def main(argv=None) -> int:
    a = build().parse_args(argv)
    try:
        return a.fn(a, Path(a.state))
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
