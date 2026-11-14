"""Compatibility testing: structural checks on generated packages.

Honesty rule: these checks prove the package has the layout each platform's
documentation describes. They do NOT prove a live assistant discovered or
followed a skill; that needs a manual run (see docs/COMPATIBILITY.md).
"""
from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

from . import discover_skills, frontmatter
from .packager import PRODUCT, package

# Evidence level for each platform's documented mechanism.
MATRIX = {
    "claude-code": {"mechanism": "skills dir (.claude/skills/<name>/SKILL.md) or plugin (.claude-plugin/plugin.json + skills/)",
                    "docs": "verified against Claude Code docs and the existing KnowledgeWala plugin layout", "live_tested": False},
    "github-copilot": {"mechanism": ".github/skills/<name>/SKILL.md (Copilot cloud agent, CLI, VS Code agent mode) + .github/copilot-instructions.md",
                       "docs": "documented by GitHub Docs (About Agent Skills); VS Code stable support noted as rolling out", "live_tested": False},
    "cursor": {"mechanism": ".cursor/rules/<name>.mdc (long-standing rules mechanism) + resources in .cursor/skills/<name>/",
               "docs": "rules: documented. Native .cursor/skills: only secondary sources found, treat as UNVERIFIED", "live_tested": False},
    "codex": {"mechanism": ".agents/skills/<name>/SKILL.md (repo-level, scanned from CWD up to repo root; user-level $HOME/.agents/skills) + AGENTS.md snippet",
              "docs": "documented by OpenAI Codex docs (build-skills, agents-md), checked 2026-11-14; extra frontmatter fields (license, compatibility, metadata) not confirmed as tolerated; Codex was not installed here", "live_tested": False},
    "generic": {"mechanism": "agentskills.io open format: <name>/SKILL.md with optional scripts/ references/ assets/",
                "docs": "verified against agentskills.io/specification", "live_tested": False},
    "agensi": {"mechanism": "open SKILL.md format; creator submission through Agensi dashboard (manual)",
               "docs": "agensi.io homepage only; submission steps and SKILL.md rules not publicly documented there; no publishing API found", "live_tested": False},
}


def _check_skill_dir(d: Path, name: str, errs: list[str]) -> None:
    md = d / "SKILL.md"
    if not md.is_file():
        errs.append(f"{name}: SKILL.md missing in package")
        return
    fm, _, e = frontmatter.parse(md.read_text(encoding="utf-8"))
    errs += [f"{name}: {x}" for x in e]
    if fm.get("name") != d.name:
        errs.append(f"{name}: frontmatter name != directory {d.name}")


def simulate_codex_discovery(workspace: Path, expected: list[str], start: str = "deep/nested/dir") -> list[str]:
    """SIMULATION of the documented Codex scan (not the real client): walk from a nested CWD up to the
    repo root reading every .agents/skills/*/SKILL.md, require name+description, flag duplicate names."""
    errs: list[str] = []
    cwd = workspace / start
    cwd.mkdir(parents=True, exist_ok=True)
    seen: dict[str, int] = {}
    budget_chars = 0
    for d in [cwd, *cwd.parents]:
        base = d / ".agents" / "skills"
        if base.is_dir():
            for md in sorted(base.glob("*/SKILL.md")):
                fm, _, e = frontmatter.parse(md.read_text(encoding="utf-8"))
                if e or not fm.get("name") or not fm.get("description"):
                    errs.append(f"codex: {md.parent.name} lacks readable name/description")
                    continue
                seen[fm["name"]] = seen.get(fm["name"], 0) + 1
                budget_chars += len(fm["name"]) + len(fm["description"])
        if d == workspace:
            break
    dups = [n for n, c in seen.items() if c > 1]
    if dups:
        errs.append(f"codex: duplicate skill names {dups}")
    missing = set(expected) - set(seen)
    if missing:
        errs.append(f"codex: skills not discovered: {sorted(missing)}")
    SIMULATION_STATS["codex_description_chars"] = budget_chars
    if budget_chars > 8000:  # documented fallback budget when the context window is unknown
        errs.append(f"codex: name+description text is {budget_chars} chars, above the 8000-char fallback budget for the skills list")
    return errs


SIMULATION_STATS: dict[str, int] = {}


def check_platform(plat: str, work: Path, expected: list[str]) -> list[str]:
    errs: list[str] = []
    out = work / plat
    zips = sorted(out.rglob("*.zip"))
    if not zips:
        return [f"{plat}: no archives produced"]
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            if zf.testzip():
                errs.append(f"{plat}: corrupt archive {z.name}")
            names = zf.namelist()
            if any(n.startswith(("/", "..")) or ".." in n.split("/") for n in names):
                errs.append(f"{plat}: unsafe path in {z.name}")
            if any("/tests/" in "/" + n for n in names):
                errs.append(f"{plat}: test fixtures leaked into {z.name}")
            if plat in ("generic", "agensi") or "per-skill" in z.parts:
                if not any(n.endswith("/SKILL.md") and n.count("/") == 1 for n in names):
                    errs.append(f"{plat}: {z.name} lacks <name>/SKILL.md")
    if plat == "claude-code":
        root = out / PRODUCT
        if not (root / ".claude-plugin" / "plugin.json").is_file():
            errs.append("claude-code: plugin.json missing")
        for n in expected:
            _check_skill_dir(root / "skills" / n, f"claude-code/{n}", errs)
    if plat == "cursor":
        for n in expected:
            rule = out / "workspace" / ".cursor" / "rules" / f"{n}.mdc"
            if not rule.is_file():
                errs.append(f"cursor: rule missing for {n}")
                continue
            t = rule.read_text(encoding="utf-8")
            if not t.startswith("---\ndescription:") or "alwaysApply:" not in t:
                errs.append(f"cursor: {n}.mdc frontmatter malformed")
            for ref in __import__("re").findall(r"\.cursor/skills/[\w./\-]+", t):
                if not (out / "workspace" / ref).exists():
                    errs.append(f"cursor: {n}.mdc references missing file {ref}")
    if plat == "codex":
        errs += simulate_codex_discovery(out / "workspace", expected)
        snip = out / "workspace" / "AGENTS-kw-skills-snippet.md"
        if not snip.is_file() or snip.stat().st_size > 32 * 1024:
            errs.append("codex: AGENTS snippet missing or larger than Codex's default 32 KiB project-doc cap")
    if plat == "github-copilot":
        if not (out / "workspace" / ".github" / "copilot-instructions.md").is_file():
            errs.append("github-copilot: copilot-instructions.md missing")
        for n in expected:
            _check_skill_dir(out / "workspace" / ".github" / "skills" / n, f"github-copilot/{n}", errs)
    return errs


def run(root: Path, platforms: list[str]) -> dict:
    expected = [s.name for s in discover_skills(root)]
    results = {}
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        package(root, platforms, dist=work)
        for p in platforms:
            errs = check_platform(p, work, expected)
            results[p] = {"passed": not errs, "errors": errs, "skills_checked": len(expected),
                          "level": "structural", **{k: MATRIX[p][k] for k in ("mechanism", "docs", "live_tested")}}
            if p == "codex":
                n = SIMULATION_STATS.get("codex_description_chars", 0)
                results[p]["skill_list_chars"] = n
                results[p]["note"] = (f"skill name+description text totals {n} chars; Codex budgets the initial skills list at about 2% of the "
                                      "context window, so on small windows some descriptions may be shortened or skills omitted")
    return results
