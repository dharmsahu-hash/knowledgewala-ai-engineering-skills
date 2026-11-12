"""Release management: semver, notes, checksums, artifacts, history, rollback.

Releases are built locally into dist/release-<version>/. Nothing is uploaded or
tagged remotely; publishing is a separate, human-approved step.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from . import __version__, discover_skills
from .packager import PLATFORMS, package, sha256
from .validator import SEMVER_RE, validate_skill


def history_path(root: Path) -> Path:
    return root / "releases" / "history.json"


def load_history(root: Path) -> list[dict]:
    p = history_path(root)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else []


def release_notes(root: Path, version: str) -> str:
    cl = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").is_file() else ""
    m = re.search(rf"(?ms)^##\s+\[?{re.escape(version)}\]?[^\n]*\n(.*?)(?=^##\s|\Z)", cl)
    if not m:
        raise ValueError(f"CHANGELOG.md has no section for version {version}")
    return f"# Release {version}\n\n{m.group(1).strip()}\n"


def build_release(root: Path, version: str | None = None) -> dict:
    version = version or __version__
    if not SEMVER_RE.match(version):
        raise ValueError(f"'{version}' is not a semantic version")
    if any(h["version"] == version and h["status"] == "built" for h in load_history(root)):
        raise ValueError(f"version {version} already built; bump the version or roll it back first")
    bad = {s.name: [f.message for f in validate_skill(s) if f.severity == "error"] for s in discover_skills(root)}
    bad = {k: v for k, v in bad.items() if v}
    if bad:
        raise ValueError(f"validation errors block release: {sorted(bad)}")
    notes = release_notes(root, version)
    out = root / "dist" / f"release-{version}"
    if out.exists():
        shutil.rmtree(out)
    pk = package(root, list(PLATFORMS), dist=out)
    (out / "RELEASE_NOTES.md").write_text(notes, encoding="utf-8")
    files = sorted(p for p in out.rglob("*.zip"))
    (out / "SHA256SUMS").write_text("".join(f"{sha256(p)}  {p.relative_to(out).as_posix()}\n" for p in files), encoding="utf-8")
    entry = {"version": version, "status": "built", "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "artifacts": len(files), "published": False}
    hist = load_history(root) + [entry]
    history_path(root).parent.mkdir(parents=True, exist_ok=True)
    history_path(root).write_text(json.dumps(hist, indent=2) + "\n", encoding="utf-8")
    return {**entry, "dir": str(out), "platforms": pk}


def rollback(root: Path, version: str) -> dict:
    hist = load_history(root)
    hit = [h for h in hist if h["version"] == version and h["status"] == "built"]
    if not hit:
        raise ValueError(f"no built release {version} in history")
    if hit[-1].get("published"):
        raise ValueError("release is marked published; withdraw it from the marketplace manually first")
    shutil.rmtree(root / "dist" / f"release-{version}", ignore_errors=True)
    hit[-1]["status"] = "rolled_back"
    hit[-1]["rolled_back_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    history_path(root).write_text(json.dumps(hist, indent=2) + "\n", encoding="utf-8")
    return hit[-1]
