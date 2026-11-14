import zipfile

import pytest

from kw_skills import compatibility, packager


def test_all_platforms_package(repo_root, tmp_path):
    res = packager.package(repo_root, list(packager.PLATFORMS), dist=tmp_path)
    assert set(res) == set(packager.PLATFORMS)
    assert all(v for v in res.values())


def test_checksums_reproducible(repo_root, tmp_path):
    a = packager.package(repo_root, ["generic"], dist=tmp_path / "a")
    b = packager.package(repo_root, ["generic"], dist=tmp_path / "b")
    assert [x["sha256"] for x in a["generic"]] == [x["sha256"] for x in b["generic"]]


def test_unknown_platform_and_skill(repo_root, tmp_path):
    with pytest.raises(ValueError):
        packager.package(repo_root, ["nope"], dist=tmp_path)
    with pytest.raises(ValueError):
        packager.package(repo_root, ["generic"], only=["missing-skill"], dist=tmp_path)


def test_generic_zip_layout_excludes_tests(repo_root, tmp_path):
    packager.package(repo_root, ["generic"], only=["code-review"], dist=tmp_path)
    z = next((tmp_path / "generic").glob("code-review-*.zip"))
    names = zipfile.ZipFile(z).namelist()
    assert "code-review/SKILL.md" in names and not any("/tests/" in n for n in names)
    assert "code-review/scripts/check-findings.py" in names


def test_cursor_rule_has_rewritten_links(repo_root, tmp_path):
    packager.package(repo_root, ["cursor"], only=["requirement-analysis"], dist=tmp_path)
    rule = (tmp_path / "cursor" / "workspace" / ".cursor" / "rules" / "requirement-analysis.mdc").read_text(encoding="utf-8")
    assert rule.startswith("---\ndescription:") and "alwaysApply: false" in rule
    assert ".cursor/skills/requirement-analysis/templates/requirement-document.md" in rule


def test_claude_plugin_manifest(repo_root, tmp_path):
    import json
    packager.package(repo_root, ["claude-code"], dist=tmp_path)
    m = json.loads((tmp_path / "claude-code" / packager.PRODUCT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert m["name"] == packager.PRODUCT and m["license"] == "MIT"


def test_compatibility_all_structural_pass(repo_root):
    res = compatibility.run(repo_root, list(compatibility.MATRIX))
    failed = {k: v["errors"] for k, v in res.items() if not v["passed"]}
    assert not failed, failed
    assert all(v["live_tested"] is False and v["level"] == "structural" for v in res.values())


def test_codex_layout_and_discovery_simulation(repo_root, tmp_path):
    packager.package(repo_root, ["codex"], dist=tmp_path)
    ws = tmp_path / "codex" / "workspace"
    assert (ws / ".agents/skills/ai-sdlc-orchestrator/SKILL.md").is_file()
    assert (ws / ".agents/skills/ai-sdlc-orchestrator/scripts/sdlc_state.py").is_file()
    assert not list(ws.rglob("tests"))  # fixtures excluded from distribution
    expected = [s.name for s in __import__("kw_skills").discover_skills(repo_root)]
    assert compatibility.simulate_codex_discovery(ws, expected) == []


def test_codex_simulation_catches_missing_and_duplicate(repo_root, tmp_path):
    packager.package(repo_root, ["codex"], dist=tmp_path)
    ws = tmp_path / "codex" / "workspace"
    (ws / ".agents/skills/code-review/SKILL.md").unlink()
    errs = compatibility.simulate_codex_discovery(ws, ["code-review"])
    assert any("not discovered" in e for e in errs) or any("lacks" in e for e in errs)
    # duplicate name in a nested .agents/skills (Codex does not merge same-named skills)
    nested = ws / "deep" / ".agents" / "skills" / "requirement-analysis"
    nested.mkdir(parents=True)
    (nested / "SKILL.md").write_text("---\nname: requirement-analysis\ndescription: dup. Use when testing.\n---\n", encoding="utf-8")
    assert any("duplicate" in e for e in compatibility.simulate_codex_discovery(ws, []))


def test_codex_agents_snippet_within_cap(repo_root, tmp_path):
    packager.package(repo_root, ["codex"], dist=tmp_path)
    assert (tmp_path / "codex/workspace/AGENTS-kw-skills-snippet.md").stat().st_size < 32 * 1024


def test_compat_detects_missing_skill_md(repo_root, tmp_path):
    packager.package(repo_root, ["github-copilot"], dist=tmp_path)
    victim = next((tmp_path / "github-copilot" / "workspace" / ".github" / "skills").glob("*/SKILL.md"))
    victim.unlink()
    errs = compatibility.check_platform("github-copilot", tmp_path, [victim.parent.name])
    assert any("SKILL.md missing" in e for e in errs)


def test_codex_install_and_run_orchestrator_end_to_end(repo_root, tmp_path):
    """Install the Codex package into a fresh repo and run the installed gate script from its installed path."""
    import subprocess, sys, zipfile
    packager.package(repo_root, ["codex"], dist=tmp_path / "d")
    z = next((tmp_path / "d" / "codex").glob("*.zip"))
    proj = tmp_path / "proj"
    zipfile.ZipFile(z).extractall(proj)
    script = proj / ".agents/skills/ai-sdlc-orchestrator/scripts/sdlc_state.py"
    state = proj / "state.json"
    run = lambda *a: subprocess.run([sys.executable, "-I", str(script), "--state", str(state), *a], capture_output=True, text=True)
    assert run("init", "--project", "demo").returncode == 0
    assert run("complete", "hld", "--evidence", "tried to skip stages ahead").returncode == 1   # order enforced
    assert run("approve", "requirements", "--by", "codex").returncode == 1                       # AI cannot approve
    assert run("complete", "requirement-analysis", "--evidence", "produced docs/sdlc/requirements.md").returncode == 0
    out = run("status")
    assert out.returncode == 0 and "requirement-approval" in out.stdout
    check = proj / ".agents/skills/code-review/scripts/check-findings.py"
    bad = proj / "review.md"
    bad.write_text("no findings format here\n", encoding="utf-8")
    assert subprocess.run([sys.executable, "-I", str(check), str(bad)], capture_output=True, text=True).returncode == 1
