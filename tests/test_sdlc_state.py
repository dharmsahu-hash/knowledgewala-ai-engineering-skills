import importlib.util
from pathlib import Path

import pytest

P = Path(__file__).resolve().parents[1] / "orchestrators" / "ai-sdlc-orchestrator" / "scripts" / "sdlc_state.py"
spec = importlib.util.spec_from_file_location("sdlc_state", P)
sdlc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sdlc)


@pytest.fixture
def run(tmp_path):
    state = str(tmp_path / "s.json")

    def _run(*args):
        return sdlc.main(["--state", state, *args])
    _run("init", "--project", "demo")
    return _run


EV = "produced docs/sdlc/requirements.md"


def test_init_does_not_overwrite(run):
    assert run("init", "--project", "again") == 1


def test_cannot_skip_stage(run):
    assert run("complete", "hld", "--evidence", EV) == 1


def test_evidence_required(run):
    assert run("complete", "requirement-analysis") == 1
    assert run("complete", "requirement-analysis", "--evidence", "short") == 1
    assert run("complete", "requirement-analysis", "--evidence", EV) == 0


def test_gate_needs_human_approval(run):
    run("complete", "requirement-analysis", "--evidence", EV)
    assert run("complete", "requirement-approval", "--evidence", EV) == 1
    assert run("approve", "requirements", "--by", "Claude") == 1
    assert run("approve", "requirements", "--by", "") == 1
    assert run("approve", "requirements", "--by", "Dharm") == 0
    assert run("complete", "requirement-approval", "--evidence", EV) == 0


def test_flag_blocks_until_human_resolves(run):
    run("flag", "destructive-db", "--reason", "drop legacy table")
    assert run("complete", "requirement-analysis", "--evidence", EV) == 1
    assert run("resolve", "1", "--decision", "approve", "--by", "assistant") == 1
    assert run("resolve", "1", "--decision", "reject", "--by", "Dharm") == 0
    assert run("complete", "requirement-analysis", "--evidence", EV) == 0


def test_unknown_inputs_refused(run):
    assert run("complete", "nope", "--evidence", EV) == 1
    assert run("approve", "nope", "--by", "Dharm") == 1
    assert run("flag", "nope", "--reason", "x") == 1


def test_double_complete_refused(run):
    run("complete", "requirement-analysis", "--evidence", EV)
    assert run("complete", "requirement-analysis", "--evidence", EV) == 1


def test_full_lifecycle(run):
    run("approve", "requirements", "--by", "Dharm")
    run("approve", "architecture", "--by", "Dharm")
    run("approve", "plan", "--by", "Dharm")
    run("approve", "release", "--by", "Dharm")
    for s in sdlc.STAGE_IDS:
        assert run("complete", s, "--evidence", f"evidence for {s}") == 0, s
    assert run("status") == 0
    assert len(sdlc.STAGES) == 16


def test_missing_state_file_exits(tmp_path):
    with pytest.raises(SystemExit):
        sdlc.main(["--state", str(tmp_path / "none.json"), "status"])
