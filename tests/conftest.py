import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tooling"))

GOOD_SKILL = """---
name: demo-skill
description: Does a demo thing. Use when testing the validator.
license: MIT
metadata:
  version: "1.0.0"
  author: Test
  category: demo
  tags: "a, b"
---

# Demo
## Purpose
x
## When to use
x
## When not to use
x
## Required inputs
x
## Instructions
x
## Workflow
x
## Quality gates
x
## Expected output
x
## Validation rules
x
## Error handling
x
## Examples
x
## Limitations
x
"""


@pytest.fixture
def repo_root() -> Path:
    return ROOT


@pytest.fixture
def make_skill(tmp_path):
    def _make(name="demo-skill", text=GOOD_SKILL, extras=True) -> Path:
        d = tmp_path / "skills" / "demo" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(text.replace("demo-skill", name), encoding="utf-8")
        if extras:
            (d / "README.md").write_text("# r\n", encoding="utf-8")
            (d / "tests").mkdir()
            (d / "tests" / "test-cases.md").write_text("# t\n", encoding="utf-8")
        return d
    return _make


@pytest.fixture
def repo_copy(tmp_path):
    """Writable copy of the real repo content (skills, orchestrators, schemas, CHANGELOG)."""
    dst = tmp_path / "repo"
    ign = shutil.ignore_patterns("__pycache__", "dist", ".git", "releases")
    for d in ("skills", "orchestrators", "schemas", "evals"):
        shutil.copytree(ROOT / d, dst / d, ignore=ign)
    for f in ("CHANGELOG.md", "LICENSE", "NOTICE.md"):
        if (ROOT / f).exists():
            shutil.copyfile(ROOT / f, dst / f)
    (dst / "docs").mkdir()
    return dst
