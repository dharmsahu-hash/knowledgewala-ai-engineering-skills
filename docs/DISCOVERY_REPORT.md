# Phase 0 Discovery Report

Date: 2026-11-12. Scope: inspect the existing KnowledgeWala Agentic SDLC repository, the official Agent Skills specification, Agensi, and platform skill mechanisms; produce a gap analysis. The existing repository was **read only**; nothing in it was modified.

## 1. Existing repository: `knowledgewala-agentic-sdlc` v1.3.0

| Item | Finding |
|---|---|
| Licence | MIT, copyright 2026 KnowledgeWala. `NOTICE.md` states brand is not licensed, requires licence text and markers on redistribution, and disclaims affiliation with Anthropic and Atlassian |
| Packaging | Claude Code plugin (`.claude-plugin/plugin.json`, `marketplace.json`), installer (`install/kw_install.py`, `.ps1`, `.sh`), zip releases in `dist/` with sha256 |
| Content | 1 skill (`dev-workflow`, an orchestrator command), 15 subagents in `agents/`, guardrail and observability scripts (`scripts/kw_policy.py`, `block_destructive.py`, `kw_trace.py`, `kw_report.py`) |
| Tests | 5 test modules (agents, guardrail, installer, observability, policy); 26 tests at v1.3.0 |
| Docs | README, CHANGELOG, `docs/EVIDENCE.md`, `EXAMPLE.md`, `RELEASING.md`, `TOKEN-OPTIMIZATION.md` |
| Nature | A Claude Code workflow product: slash command + subagents + hooks. Not an Agent Skills collection |

## 2. Reuse versus independent implementation

| Existing component | Decision | Reason |
|---|---|---|
| Stage model and gates (G1-G4, bounded 3-round fix loop) | **Reuse the ideas**, reimplement | Same discipline, but new product uses a 16-stage model and a script-enforced state file usable on any platform |
| `requirement-analyst`, `solution-architect`, `code-reviewer`, `unit-test-agent` | **Rewrite as standalone skills** | Subagent files use Claude-only frontmatter (`tools`, `model`, `disallowedTools`); skills must follow the open spec |
| Attribution marker convention | **Adopt** (provenance in NOTICE) | Keeps ownership and licence trail clear |
| Release process (zip + sha256, `RELEASING.md`) | **Reuse the approach** | Implemented in `kw_skills.release` for every platform |
| Guardrail hooks, Jira poller, observability scripts, installer, `dev-workflow` command | **Stay exclusive to the original project** | Claude Code specific, hook-based, or Jira-coupled |
| `deploy-planner`, `deployment-devops-agent`, `ops-monitor`, `ticket-analyst` | **Not ported in v1** | Roadmap: CI/CD and AWS skills |

No source text was copied verbatim; new skills are written for the open format. Licence for the new product is MIT, same owner, with `NOTICE.md` crediting the original project as the conceptual predecessor.

## 3. Agent Skills specification (agentskills.io/specification, fetched 2026-11-12)

- Required frontmatter: `name` (max 64, lowercase/digits/single hyphens, must match directory), `description` (max 1024). Optional: `license`, `compatibility` (max 500), `metadata` (string map), `allowed-tools` (experimental).
- Layout: `SKILL.md` plus optional `scripts/`, `references/`, `assets/`. SKILL.md under 500 lines; body under about 5000 tokens recommended; references one level deep.
- Consequence: the 13 required sections requested in the brief live in the **body**, not frontmatter; version, author, category, tags go in `metadata`; KnowledgeWala additionally *requires* `license` and `metadata` (policy, not spec). No undocumented frontmatter fields are used; the validator rejects them.

## 4. Platform mechanisms

| Platform | Mechanism | Confidence |
|---|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md`, or plugin with `.claude-plugin/plugin.json` and `skills/` | High (matches existing KnowledgeWala plugin) |
| GitHub Copilot | `.github/skills/<name>/SKILL.md` for the cloud agent, CLI and VS Code agent mode; `.github/copilot-instructions.md` for repo guidance | Medium-high (GitHub Docs); VS Code stable rollout noted as in progress |
| Cursor | `.cursor/rules/*.mdc` is the established mechanism. A native `.cursor/skills/` directory appears only in secondary sources | **Unverified** for native skills; adapter ships a rule wrapper plus resources |
| Generic | agentskills.io open format | High |

Not live-tested on any platform (no accounts or installations driven in this session). See `docs/COMPATIBILITY.md`.

## 5. Agensi (agensi.io homepage, fetched 2026-11-12)

Found: SKILL.md open standard; creators are verified before selling; creators keep 70% (30% platform fee); payouts via Stripe or USDC through Zoneless; money-back guarantee on paid skills; every version scanned (8-point scan), permissions shown on listings; buyers consume through an MCP connector and may not copy/export skills; free and paid skills reviewed alike.
**Not found:** submission steps, SKILL.md requirements specific to Agensi, any public publishing API or CLI, versioning rules, licensing terms for creators beyond the above.
Consequence: **no automated publishing is implemented.** The tool prepares listings and zip packages for manual upload; every commercial or legal step is a human gate. Detailed docs may exist behind creator login: owner should confirm before submission.

## 6. Gap analysis

| Gap | Resolution in this repo |
|---|---|
| No cross-platform packaging | `kw_skills.packager` adapters |
| No skill validation beyond ad-hoc tests | `kw_skills.validator` (spec + policy + security checks) |
| No marketplace preparation | `kw_skills.marketplace` |
| No evaluation of skill output quality | `evals/` rubric + scorer; **real runs still to do** |
| Specialist skills for Angular, AWS, agentic AI, RAG, security, performance, CI/CD | Roadmap (v1 ships 10 skills, quality over quantity) |
| Live testing on Claude Code, Cursor, Copilot, Agensi | Manual checklist in `docs/COMPATIBILITY.md` |

## 7. Recommendations (adopted)
Ship 10 skills first; build the flagship orchestrator with script-enforced gates; keep Agensi manual; freemium tiers proposed (needs approval); GitHub is canonical source.
