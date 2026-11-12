# Developer guide

## Setup
```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"     # Windows: .\.venv\Scripts\python -m pip install -e ".[dev]"
sh scripts/check.sh                                            # Windows: powershell -File scripts/check.ps1
```

## Layout
```
skills/<category>/<skill-name>/   canonical skills (name == directory)
orchestrators/ai-sdlc-orchestrator/
tooling/kw_skills/                validator, packager, compatibility, docsgen, release, marketplace, evals, cli
schemas/                          frontmatter JSON Schema (documentation of the validator's rules)
evals/rubrics|results/            quality rubrics and recorded scores
examples/                         six sample briefs
marketplace/agensi/               generated listings/packages + manual guides
platforms/<name>/README.md        adapter notes (code lives in packager.py)
tests/                            pytest suite
```

## Adding a skill
1. `skills/<category>/<name>/` with `SKILL.md`, `README.md`, `tests/test-cases.md`, plus `references/`, `templates/`, `scripts/` as needed.
2. Frontmatter: `name`, `description` (what + "Use when ..."), `license: MIT`, `metadata` (`version`, `author`, `category`, `tags`, optional `title`, `tier`). No other top-level fields.
3. Body must contain these `##` sections: Purpose, When to use, When not to use, Required inputs, Instructions, Workflow, Quality gates, Expected output, Validation rules, Error handling, Examples, Limitations. Keep under 500 lines and about 5000 tokens; move detail to `references/`.
4. Scripts: Python stdlib only, read-only on inputs, no network, no `subprocess`/`os.system`/`eval`/`exec`/`rmtree` (validator enforces).
5. `kw-skills validate <name>`, then `kw-skills docs`, update `tests/test_repo_governance.py` expected set and `CHANGELOG.md`, then `scripts/check.*`.

## Adding a platform adapter
Add a `build_<platform>` function in `packager.py` returning archive paths, register it in `BUILDERS`/`PLATFORMS`, add a `MATRIX` entry (mechanism, docs evidence, `live_tested: False`) and structural checks in `compatibility.check_platform`, and a test. State the evidence honestly; never mark `live_tested` true without a recorded manual run.

## Release
1. Update `CHANGELOG.md` with a `## [x.y.z]` section, `__version__` in `tooling/kw_skills/__init__.py`, `pyproject.toml`, and skill `metadata.version`s.
2. `kw-skills release --version x.y.z` builds `dist/release-x.y.z/` (zips, `SHA256SUMS`, `RELEASE_NOTES.md`) and records history. `release history`, `release rollback --version x.y.z` available.
3. Tagging, GitHub release and marketplace upload are **manual and need owner approval**.

## Design rules
Deterministic outputs; zero runtime dependencies; no network in tooling; every check has a test; honest status labels (structural / functional / compatibility / real-world).
