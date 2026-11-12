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


def test_compat_detects_missing_skill_md(repo_root, tmp_path):
    packager.package(repo_root, ["github-copilot"], dist=tmp_path)
    victim = next((tmp_path / "github-copilot" / "workspace" / ".github" / "skills").glob("*/SKILL.md"))
    victim.unlink()
    errs = compatibility.check_platform("github-copilot", tmp_path, [victim.parent.name])
    assert any("SKILL.md missing" in e for e in errs)
