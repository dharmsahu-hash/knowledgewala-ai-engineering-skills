"""Repository-level checks: required docs, examples, licence, no secrets, schema consistency."""
import json
import re

from kw_skills import validator

REQUIRED_DOCS = ["README.md", "ARCHITECTURE.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSE", "CHANGELOG.md", "ROADMAP.md",
                 "INSTALLATION.md", "USER_GUIDE.md", "DEVELOPER_GUIDE.md", "MARKETPLACE_GUIDE.md", "NOTICE.md"]
EXAMPLES = ["spring-boot-payment-api", "angular-frontend", "mysql-database-design", "aws-deployment", "rag-application", "multi-agent-application"]


def test_required_docs_exist_and_nonempty(repo_root):
    for d in REQUIRED_DOCS:
        assert (repo_root / d).is_file() and (repo_root / d).stat().st_size > 200, d


def test_examples_have_brief_with_expected_flow(repo_root):
    for e in EXAMPLES:
        t = (repo_root / "examples" / e / "brief.md").read_text(encoding="utf-8")
        for h in ("## Business request", "## Expected orchestrator behaviour", "## Human gates", "## Acceptance for this sample"):
            assert h in t, (e, h)


def test_licence_is_mit_and_attributes_existing_project(repo_root):
    assert "MIT License" in (repo_root / "LICENSE").read_text(encoding="utf-8")
    assert "knowledgewala-agentic-sdlc" in (repo_root / "NOTICE.md").read_text(encoding="utf-8")


def test_schema_limits_match_validator(repo_root):
    s = json.loads((repo_root / "schemas/skill-frontmatter.schema.json").read_text(encoding="utf-8"))
    p = s["properties"]
    assert p["name"]["maxLength"] == validator.MAX_NAME
    assert p["description"]["maxLength"] == validator.MAX_DESC
    assert p["compatibility"]["maxLength"] == validator.MAX_COMPAT
    assert set(s["required"]) == {"name", "description", "license", "metadata"}


def test_no_secrets_anywhere_in_tracked_text(repo_root):
    skip = {".git", "dist", "__pycache__", ".pytest_cache", "node_modules"}
    for p in repo_root.rglob("*"):
        if not p.is_file() or set(p.parts) & skip or p.suffix not in {".md", ".py", ".json", ".yml", ".yaml", ".toml", ".ps1", ".sh"}:
            continue
        if "tests" in p.relative_to(repo_root).parts and p.name.startswith("test_"):
            continue  # tests contain intentionally fake tokens
        t = p.read_text(encoding="utf-8", errors="replace")
        for label, rx in validator.SECRET_PATTERNS.items():
            assert not rx.search(t), (p, label)


def test_workflows_are_manual_only(repo_root):
    for w in (repo_root / ".github/workflows").glob("*.yml"):
        t = w.read_text(encoding="utf-8")
        assert "workflow_dispatch" in t and not re.search(r"(?m)^\s*(push|pull_request|schedule):", t), w.name


def test_initial_ten_skills_present(repo_root):
    from kw_skills import discover_skills
    names = {s.name for s in discover_skills(repo_root)}
    assert names == {"requirement-analysis", "solution-architecture", "hld-generator", "lld-generator", "java-engineering",
                     "spring-boot-engineering", "database-engineering", "code-review", "test-engineering", "ai-sdlc-orchestrator"}
