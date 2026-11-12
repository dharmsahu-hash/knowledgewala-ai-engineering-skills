"""KnowledgeWala AI Engineering Skills tooling (standard library only)."""
from __future__ import annotations

from pathlib import Path

__version__ = "1.0.0-rc.1"

SKILL_ROOTS = ("skills", "orchestrators")


def find_root(start: Path | None = None) -> Path:
    """Locate the repository root (contains skills/ and schemas/)."""
    import os

    env = os.environ.get("KW_SKILLS_ROOT")
    if env:
        return Path(env).resolve()
    candidates = [Path(start or Path.cwd()).resolve(), Path(__file__).resolve().parents[2]]
    for base in candidates:
        for p in [base, *base.parents]:
            if (p / "skills").is_dir() and (p / "schemas").is_dir():
                return p
    raise SystemExit("error: cannot find repository root (set KW_SKILLS_ROOT or run inside the repo)")


def discover_skills(root: Path) -> list[Path]:
    """Every directory below skills/ or orchestrators/ that contains SKILL.md, sorted by name."""
    found: list[Path] = []
    for r in SKILL_ROOTS:
        base = root / r
        if base.is_dir():
            found += [p.parent for p in base.rglob("SKILL.md")]
    return sorted(found, key=lambda p: p.name)
