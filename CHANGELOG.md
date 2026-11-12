# Changelog

All notable changes. Versions follow [Semantic Versioning](https://semver.org/).

## [1.0.0-rc.2]

### Added
- 10 more skills, completing the 20-skill catalogue: `api-design-integration`, `angular-engineering`, `frontend-architecture`, `agentic-ai-architect`, `rag-engineering`, `ai-testing-evaluation`, `application-security`, `performance-engineering`, `aws-cloud-architecture`, `cicd-release-engineering`.
- Orchestrator delegation map updated to use the new specialists; sample briefs no longer say specialists are missing.

### Changed
- CI workflow moved to `docs/ci-workflow.example.yml` (no active workflow; token lacked `workflow` scope and per-push minutes are avoided by design).
- All skills and tooling versioned 1.0.0-rc.2.

### Known gaps (unchanged)
- No live platform tests; no scored real-world evaluations; new skills have no output-checker scripts yet.

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
- (resolved in rc.2) Remaining catalogue skills.
