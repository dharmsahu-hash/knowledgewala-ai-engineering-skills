# Changelog

All notable changes. Versions follow [Semantic Versioning](https://semver.org/).

## [1.0.0-rc.1]

First release candidate. Not published; human approval required before public release.

### Added
- 10 skills: `requirement-analysis`, `solution-architecture`, `hld-generator`, `lld-generator`, `java-engineering`, `spring-boot-engineering`, `database-engineering`, `code-review`, `test-engineering`, and the flagship `ai-sdlc-orchestrator`.
- `kw-skills` CLI: `list`, `validate`, `package`, `compatibility`, `docs`, `release`, `marketplace prepare|report`, `eval score`, with `--json`, `--verbose`, `--version`.
- Validator (Agent Skills spec + KnowledgeWala policy + secret/unsafe-script checks), packager adapters (generic, Claude Code, Cursor, GitHub Copilot, Agensi), compatibility checks, release management with checksums, history and rollback.
- Script-enforced lifecycle gates (`sdlc_state.py`): stage order, evidence, human approvals, blocking flags.
- Evaluation rubric and scorer; six sample project briefs.
- Documentation set, Agensi submission package (manual), security policy.

### Known gaps
- No live test on Claude Code, Cursor, Copilot or Agensi; Cursor native skills directory unverified.
- Real-world quality evaluation of skills not yet performed.
- Specialist skills 7, 9-11, 13, 14, 16-20 of the catalogue are roadmap items.
