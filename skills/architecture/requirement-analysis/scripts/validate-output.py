#!/usr/bin/env python3
"""Structural check of a requirements document. Reads one file; no network, no writes.

Usage: python validate-output.py requirements.md
Exit code 0 = structure OK, 1 = problems found, 2 = usage error.
"""
import re
import sys
from pathlib import Path

SECTIONS = ["Business Summary", "Stakeholders", "Functional Requirements", "Non-Functional Requirements",
            "User Stories and Acceptance Criteria", "Security and Compliance", "Assumption Register",
            "Risk Register", "Clarification Questions", "Traceability Matrix"]
WEAK = re.compile(r"\b(fast|quick|secure|user[- ]friendly|scalable|robust|easy)\b", re.I)


def check(text: str) -> list[str]:
    problems = []
    for s in SECTIONS:
        if not re.search(rf"(?im)^#+\s*{re.escape(s)}\s*$", text):
            problems.append(f"missing section: {s}")
    frs = set(re.findall(r"\*\*((?:FR|NFR)-\d+)\*\*", text))
    if not frs:
        problems.append("no FR-n / NFR-n requirements found")
    matrix = text.split("Traceability Matrix")[-1] if "Traceability Matrix" in text else ""
    for r in sorted(frs):
        if not re.search(rf"\b{r}\b", matrix):
            problems.append(f"{r} is not in the traceability matrix")
    for block in re.split(r"(?m)^#{2,4}\s*US-\d+", text)[1:]:
        story = block.split("\n## ")[0]
        if not re.search(r"\*\*AC-\d+\*\*", story):
            problems.append("a user story has no acceptance criteria")
    for m in re.finditer(r"\*\*(NFR-\d+)\*\*([^\n]*)", text):
        if WEAK.search(m.group(2)) and not re.search(r"\d", m.group(2)):
            problems.append(f"{m.group(1)} uses an unmeasurable word without a number")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"error: {path} not found", file=sys.stderr)
        return 2
    problems = check(path.read_text(encoding="utf-8"))
    for p in problems:
        print("PROBLEM:", p)
    print("OK (structure only)" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
