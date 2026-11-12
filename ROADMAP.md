# Roadmap

Legend: done = implemented and tested here; planned = not started.

## Phase status
| Phase | Status |
|---|---|
| 0 Discovery | done ([report](docs/DISCOVERY_REPORT.md)) |
| 1 Foundation (schema, validator, packager, CLI, tests) | done |
| 2 Initial 10 skills, then remaining 10 catalogue skills | done (structural + functional validated); all 20 skills shipped as rc.2 |
| 3 Multi-platform packaging | done structurally; live platform testing **planned** |
| 4 Testing and evaluation | partial: automated tests done; sample briefs written; scored real-assistant runs **planned** |
| 5 Marketplace preparation | done for manual submission; screenshots, prices, submission **owner action** |
| 6 Release | candidate built locally; public release **needs owner approval** |

## Next (in priority order)
1. Run the six sample briefs with a real assistant on Claude Code, record transcripts and scores in `evals/results/` (turns "not evaluated" into evidence).
2. Live-test installation and discovery on Claude Code, GitHub Copilot, Cursor; update the compatibility matrix.
3. Confirm Agensi submission requirements with the owner's creator account; capture real screenshots.
4. Depth over breadth: add scripts/checkers to the skills that lack them (security findings checker, API linter), then iterate on weaknesses found in real runs.
5. Optional MCP distribution if Agensi or users require it.
6. Skill Explorer web UI (separate repository/phase; only if adoption justifies it).

## Commercial proposal (needs owner approval; not Agensi-confirmed)
Free: requirement-analysis, code-review, test-engineering. Paid: architecture, design, backend skills. Premium: orchestrator. Bundle: full collection. Enterprise: contact KnowledgeWala. Prioritise adoption and feedback over revenue.
