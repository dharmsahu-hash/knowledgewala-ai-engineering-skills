"""Structural validation of canonical skills.

This is *structural* validation only. Passing it says nothing about whether a
skill produces good engineering output (see docs/QUALITY_MODEL.md).
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, asdict
from pathlib import Path

from . import frontmatter

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$")
MAX_NAME, MAX_DESC, MAX_COMPAT, MAX_BODY_LINES, MAX_BODY_TOKENS = 64, 1024, 500, 500, 5000
REQUIRED_META = ("version", "author", "category", "tags")
REQUIRED_SECTIONS = (
    "purpose", "when to use", "when not to use", "required inputs", "instructions",
    "workflow", "quality gates", "expected output", "validation rules",
    "error handling", "examples", "limitations",
)
REQUIRED_FILES = ("README.md", "tests/test-cases.md")

SECRET_PATTERNS = {
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private key block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "API-style secret": re.compile(r"\bsk-[A-Za-z0-9]{20,}"),
    "Slack token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "hardcoded credential": re.compile(
        r"(?i)\b(api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*['\"][^'\"\s<>{}$]{12,}['\"]"),
}
UNSAFE_MD = [
    (re.compile(r"(?i)(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba)?sh"), "pipe-to-shell install"),
    (re.compile(r"(?i)\brm\s+-rf\s+(/|~|\*)"), "recursive delete of broad path"),
    (re.compile(r"(?i)invoke-expression|\biex\s*\("), "Invoke-Expression"),
    (re.compile(r"(?i)chmod\s+(-R\s+)?777"), "world-writable permissions"),
]
NEGATION = re.compile(r"(?i)\b(never|do not|don't|must not|avoid|forbid\w*|prohibit\w*|no)\b")
BAD_IMPORTS = {"socket", "urllib", "requests", "http", "ftplib", "smtplib", "subprocess", "ctypes", "telnetlib"}
BAD_CALLS = {"eval", "exec", "os.system", "shutil.rmtree", "os.popen"}
TEXT_EXT = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".ps1", ".mdc", ".toml", ".csv", ""}


@dataclass
class Finding:
    code: str
    severity: str  # error | warning
    message: str
    path: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def estimate_tokens(text: str) -> int:
    return len(text) // 4  # coarse heuristic, documented as such


def _fence_stripped(text: str) -> str:
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        out.append("" if fenced else line)
    return "\n".join(out)


def check_links(md_path: Path, text: str) -> list[Finding]:
    res = []
    for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", _fence_stripped(text)):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        rel = target.split("#")[0]
        if rel and not (md_path.parent / rel).exists():
            res.append(Finding("V010", "error", f"broken relative link: {target}", str(md_path)))
    return res


def check_script(py: Path) -> list[Finding]:
    res = []
    try:
        tree = ast.parse(py.read_text(encoding="utf-8"))
    except SyntaxError as e:
        return [Finding("V013", "error", f"script does not compile: {e}", str(py))]
    for node in ast.walk(tree):
        mods = []
        if isinstance(node, ast.Import):
            mods = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods = [node.module.split(".")[0]]
        for m in mods:
            if m in BAD_IMPORTS:
                res.append(Finding("V013", "error", f"script imports restricted module '{m}'", str(py)))
        if isinstance(node, ast.Call):
            f = node.func
            name = f.id if isinstance(f, ast.Name) else (
                f"{f.value.id}.{f.attr}" if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) else "")
            if name in BAD_CALLS:
                res.append(Finding("V013", "error", f"script calls restricted function '{name}'", str(py)))
    return res


def validate_skill(skill_dir: Path) -> list[Finding]:
    f: list[Finding] = []
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return [Finding("V001", "error", "SKILL.md missing", str(skill_dir))]
    text = md.read_text(encoding="utf-8")
    fm, body, errs = frontmatter.parse(text)
    f += [Finding("V002", "error", e, str(md)) for e in errs]

    name = fm.get("name")
    if not isinstance(name, str) or not name:
        f.append(Finding("V003", "error", "frontmatter 'name' is required", str(md)))
    else:
        if len(name) > MAX_NAME or not NAME_RE.match(name):
            f.append(Finding("V003", "error", f"invalid name '{name}' (lowercase a-z, 0-9, single hyphens, max 64)", str(md)))
        if name != skill_dir.name:
            f.append(Finding("V003", "error", f"name '{name}' must match directory '{skill_dir.name}'", str(md)))

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        f.append(Finding("V004", "error", "frontmatter 'description' is required", str(md)))
    else:
        if len(desc) > MAX_DESC:
            f.append(Finding("V004", "error", f"description is {len(desc)} chars (max {MAX_DESC})", str(md)))
        if "use when" not in desc.lower():
            f.append(Finding("V004", "warning", "description should state when to use the skill ('Use when ...')", str(md)))

    if not fm.get("license"):
        f.append(Finding("V005", "error", "'license' is required by KnowledgeWala policy", str(md)))
    comp = fm.get("compatibility")
    if comp is not None and (not isinstance(comp, str) or not comp or len(comp) > MAX_COMPAT):
        f.append(Finding("V007", "error", f"'compatibility' must be a 1-{MAX_COMPAT} char string", str(md)))
    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        f.append(Finding("V006", "error", "'metadata' map is required", str(md)))
    else:
        for k in REQUIRED_META:
            if not meta.get(k):
                f.append(Finding("V006", "error", f"metadata.{k} is required", str(md)))
        if meta.get("version") and not SEMVER_RE.match(meta["version"]):
            f.append(Finding("V006", "error", f"metadata.version '{meta['version']}' is not semver", str(md)))
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    for k in set(fm) - allowed:
        f.append(Finding("V002", "error", f"unknown frontmatter field '{k}' (not in the Agent Skills spec)", str(md)))

    lines = body.count("\n") + 1
    if lines > MAX_BODY_LINES:
        f.append(Finding("V008", "error", f"SKILL.md body has {lines} lines (max {MAX_BODY_LINES})", str(md)))
    if estimate_tokens(body) > MAX_BODY_TOKENS:
        f.append(Finding("V008", "warning", f"SKILL.md body ~{estimate_tokens(body)} tokens (recommended < {MAX_BODY_TOKENS})", str(md)))

    heads = [h.lower() for h in re.findall(r"(?m)^##\s+(.+?)\s*$", _fence_stripped(body))]
    for sec in REQUIRED_SECTIONS:
        if not any(sec in h for h in heads):
            f.append(Finding("V009", "error", f"missing required section '{sec}'", str(md)))

    for rel in REQUIRED_FILES:
        if not (skill_dir / rel).is_file():
            f.append(Finding("V014", "error", f"missing required file {rel}", str(skill_dir)))

    for p in sorted(skill_dir.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or p.suffix.lower() not in TEXT_EXT:
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        for label, rx in SECRET_PATTERNS.items():
            if rx.search(t):
                f.append(Finding("V011", "error", f"possible secret ({label})", str(p)))
        if p.suffix == ".md":
            f += check_links(p, t)
            for i, line in enumerate(t.split("\n"), 1):
                for rx, label in UNSAFE_MD:
                    if rx.search(line) and not NEGATION.search(line):
                        f.append(Finding("V012", "warning", f"line {i}: {label} (review; add a 'never/do not' framing if it is a warning)", str(p)))
        if p.suffix == ".py" and "scripts" in p.relative_to(skill_dir).parts:
            f += check_script(p)
        if p.suffix in (".sh", ".ps1") and "scripts" in p.relative_to(skill_dir).parts:
            f.append(Finding("V013", "warning", "non-Python script requires manual security review", str(p)))
    return f


def summarize(results: dict[str, list[Finding]]) -> dict:
    return {
        "skills": len(results),
        "errors": sum(1 for v in results.values() for x in v if x.severity == "error"),
        "warnings": sum(1 for v in results.values() for x in v if x.severity == "warning"),
        "passed": sorted(k for k, v in results.items() if not any(x.severity == "error" for x in v)),
        "failed": sorted(k for k, v in results.items() if any(x.severity == "error" for x in v)),
    }
