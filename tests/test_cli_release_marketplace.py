import json
import subprocess
import sys

import pytest

from kw_skills import cli, docsgen, evals, marketplace, release


@pytest.fixture(autouse=True)
def _root(monkeypatch, repo_root):
    monkeypatch.setenv("KW_SKILLS_ROOT", str(repo_root))


def test_list_json(capsys):
    assert cli.main(["list", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert len(rows) == 10 and {"name", "version", "category"} <= set(rows[0])


def test_global_flags_before_subcommand(capsys):
    assert cli.main(["--json", "list"]) == 0
    assert isinstance(json.loads(capsys.readouterr().out), list)


def test_validate_all_and_one(capsys):
    assert cli.main(["validate"]) == 0
    assert "10 skill(s): 0 error(s)" in capsys.readouterr().out
    assert cli.main(["validate", "code-review", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["summary"]["skills"] == 1 and data["summary"]["errors"] == 0


def test_validate_unknown_skill(capsys):
    assert cli.main(["validate", "nope"]) == 2


def test_version(capsys):
    with pytest.raises(SystemExit) as e:
        cli.main(["--version"])
    assert e.value.code == 0 and "kw-skills" in capsys.readouterr().out


def test_package_unknown_skill_error(capsys, tmp_path):
    assert cli.main(["package", "--platform", "generic", "--skill", "zzz", "--out", str(tmp_path)]) == 2


def test_package_platform_alias_generic_agent(tmp_path):
    assert cli.main(["package", "--platform", "generic-agent", "--skill", "code-review", "--out", str(tmp_path)]) == 0


def test_compat_cli():
    assert cli.main(["compatibility", "--platform", "claude-code"]) == 0


def test_docs_catalogue_is_current():
    assert docsgen.check(__import__("pathlib").Path(__import__("os").environ["KW_SKILLS_ROOT"]))


def test_module_entrypoint_runs(repo_root):
    r = subprocess.run([sys.executable, "-m", "kw_skills", "--version"], cwd=repo_root, capture_output=True, text=True,
                       env={**__import__("os").environ, "PYTHONPATH": str(repo_root / "tooling")})
    assert r.returncode == 0 and "kw-skills" in r.stdout


def test_release_build_history_rollback(repo_copy):
    (repo_copy / "CHANGELOG.md").write_text("# Changelog\n\n## [9.9.9]\n- test\n", encoding="utf-8")
    r = release.build_release(repo_copy, "9.9.9")
    out = repo_copy / "dist" / "release-9.9.9"
    assert (out / "SHA256SUMS").is_file() and (out / "RELEASE_NOTES.md").is_file() and r["published"] is False
    with pytest.raises(ValueError):
        release.build_release(repo_copy, "9.9.9")
    release.rollback(repo_copy, "9.9.9")
    assert not out.exists() and release.load_history(repo_copy)[-1]["status"] == "rolled_back"


def test_release_requires_changelog_and_semver(repo_copy):
    with pytest.raises(ValueError):
        release.build_release(repo_copy, "not-semver")
    with pytest.raises(ValueError):
        release.build_release(repo_copy, "8.8.8")


def test_release_blocked_by_validation_error(repo_copy):
    (repo_copy / "CHANGELOG.md").write_text("## [1.0.0]\n- x\n", encoding="utf-8")
    (repo_copy / "skills/quality/code-review/README.md").unlink()
    with pytest.raises(ValueError):
        release.build_release(repo_copy, "1.0.0")


def test_marketplace_prepare_and_report(repo_copy):
    r = marketplace.prepare(repo_copy)
    assert r["listings"] == 10 and r["packages"] == 10
    rep = marketplace.report(repo_copy)
    assert rep["submission_assets_ready"] and rep["evaluated_in_real_world"] == 0
    assert any("accepts Agensi creator terms" in g.lower() or "accepted" in g.lower() for g in rep["pending_human_gates"])
    text = (repo_copy / "marketplace/agensi/listings/ai-sdlc-orchestrator.md").read_text(encoding="utf-8")
    assert "NOT approved" in text and "Nothing here has been published" in text


def test_eval_scoring(tmp_path, repo_root):
    rubric = repo_root / "evals/rubrics/payment-api.json"
    sc = tmp_path / "s.json"
    crit = json.loads(rubric.read_text(encoding="utf-8"))["criteria"]
    sc.write_text(json.dumps({"evaluator": "tester", "run_date": "2026-01-01",
                              "scores": {c["id"]: {"score": 5, "rationale": "r"} for c in crit}}), encoding="utf-8")
    assert evals.score(rubric, sc)["total"] == 50.0
    bad = json.loads(sc.read_text(encoding="utf-8"))
    bad["scores"][crit[0]["id"]]["rationale"] = ""
    sc.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError):
        evals.score(rubric, sc)
