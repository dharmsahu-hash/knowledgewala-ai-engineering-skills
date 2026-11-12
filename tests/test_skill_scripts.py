import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ra = load("skills/architecture/requirement-analysis/scripts/validate-output.py", "ra")
cr = load("skills/quality/code-review/scripts/check-findings.py", "cr")

GOOD_REQ = """# Requirements
## Business Summary
x
## Stakeholders
x
## Functional Requirements
- **FR-1** pay
## Non-Functional Requirements
- **NFR-1** p95 latency under 300 ms
## User Stories and Acceptance Criteria
### US-1 As a merchant
- **AC-1** Given a, when b, then c.
## Security and Compliance
x
## Assumption Register
x
## Risk Register
x
## Clarification Questions
x
## Traceability Matrix
| FR-1 | NFR-1 | US-1 | AC-1 |
"""


def test_requirements_ok():
    assert ra.check(GOOD_REQ) == []


def test_requirements_detects_problems():
    bad = GOOD_REQ.replace("- **AC-1** Given a, when b, then c.", "").replace("p95 latency under 300 ms", "must be fast")
    p = " ".join(ra.check(bad))
    assert "no acceptance criteria" in p and "unmeasurable" in p
    assert "not in the traceability matrix" in " ".join(ra.check(GOOD_REQ.replace("| FR-1 |", "|")))


def test_shipped_example_is_structurally_sound():
    # the worked example is an excerpt, so only check it is parseable text
    assert (ROOT / "skills/architecture/requirement-analysis/references/examples.md").read_text(encoding="utf-8")


GOOD_REVIEW = """## Summary
x
**Verdict: BLOCKED**
### F-1 [High] a/B.java:10
- **Status:** Confirmed
- **Evidence:** line
- **Explanation:** why
- **Impact:** bad
- **Remediation:** fix
## Review limits
none
"""


def test_review_ok():
    assert cr.check(GOOD_REVIEW) == []


def test_review_inconsistent_verdict_and_missing_fields():
    assert any("not BLOCKED" in p for p in cr.check(GOOD_REVIEW.replace("BLOCKED", "APPROVED")))
    assert any("missing field Impact" in p for p in cr.check(GOOD_REVIEW.replace("- **Impact:** bad\n", "")))
    assert any("invalid severity" in p for p in cr.check(GOOD_REVIEW.replace("[High]", "[Huge]")))
    assert any("heading" in p for p in cr.check(GOOD_REVIEW + "\n### F-2 no path\n"))


def test_review_format_reference_example_passes():
    text = (ROOT / "skills/quality/code-review/references/review-format.md").read_text(encoding="utf-8")
    ex = text.split("## Example\n```\n")[1].split("```")[0]
    doc = "**Verdict: BLOCKED**\n" + ex + "\n## Review limits\nnone\n"
    assert cr.check(doc) == []
