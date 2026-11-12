#!/usr/bin/env python3
"""Structural check of a code-review document. Reads one file; no network, no writes.

Usage: python check-findings.py review.md
Exit code 0 = structure OK, 1 = problems found, 2 = usage error.
"""
import re
import sys
from pathlib import Path

SEVERITIES = {"Critical", "High", "Medium", "Low"}
FIELDS = ["Status", "Evidence", "Explanation", "Impact", "Remediation"]
HEAD = re.compile(r"(?m)^###\s+(F-\d+)\s+\[(\w+)\]\s+(\S+?:\d+)\s*$")


def check(text: str) -> list[str]:
    problems = []
    heads = list(HEAD.finditer(text))
    all_heads = re.findall(r"(?m)^###\s+F-\d+.*$", text)
    if len(all_heads) != len(heads):
        problems.append("a finding heading does not match '### F-n [Severity] path:line'")
    blocking = False
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        block = text[m.end():end]
        fid, sev = m.group(1), m.group(2)
        if sev not in SEVERITIES:
            problems.append(f"{fid}: invalid severity '{sev}'")
        for f in FIELDS:
            if not re.search(rf"\*\*{f}:\*\*\s*\S", block):
                problems.append(f"{fid}: missing field {f}")
        st = re.search(r"\*\*Status:\*\*\s*(\w+)", block)
        if st and st.group(1) not in ("Confirmed", "Potential"):
            problems.append(f"{fid}: Status must be Confirmed or Potential")
        if st and st.group(1) == "Confirmed" and sev in ("Critical", "High"):
            blocking = True
    v = re.search(r"\*\*Verdict:\s*(APPROVED WITH SUGGESTIONS|APPROVED|BLOCKED)\*\*", text)
    if not v:
        problems.append("missing '**Verdict: ...**' line")
    elif blocking and v.group(1) != "BLOCKED":
        problems.append("a Confirmed Critical/High finding exists but verdict is not BLOCKED")
    if not re.search(r"(?im)^#+\s*review limits", text):
        problems.append("missing 'Review limits' section")
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
