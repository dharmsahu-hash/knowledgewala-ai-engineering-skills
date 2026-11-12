# Stages, delegation and gates

| # | Stage | Delegate to | Output artifact | Gate |
|---|---|---|---|---|
| 1 | requirement-analysis | `requirement-analysis` | docs/sdlc/requirements.md | |
| 2 | requirement-approval | human | recorded approval | `requirements` |
| 3 | architecture-design | `solution-architecture` | docs/sdlc/architecture.md + ADRs | `architecture` |
| 4 | hld | `hld-generator` | docs/sdlc/hld.md | |
| 5 | lld | `lld-generator` | docs/sdlc/lld.md | |
| 6 | implementation-planning | orchestrator | docs/sdlc/plan.md | `plan` |
| 7 | task-decomposition | orchestrator | task list with AC ids | |
| 8 | specialist-delegation | java / spring-boot / database skills | per-task briefs | |
| 9 | code-generation | java / spring-boot skills | source | |
| 10 | unit-tests | `test-engineering` | tests + run output | |
| 11 | integration-tests | `test-engineering` | tests + run output | |
| 12 | security-assessment | security specialist if installed, else `code-review` security pass | findings | |
| 13 | code-review | `code-review` | docs/sdlc/review.md | |
| 14 | defect-resolution | specialist skills | fixes + rerun evidence | |
| 15 | release-readiness | orchestrator | docs/sdlc/release-readiness.md | `release` |
| 16 | documentation | orchestrator | README, API docs, changelog | |

## Flags (human decision required, raised before acting)
`major-architecture`, `destructive-db`, `security-sensitive`, `production-deploy`, `secrets`, `scope-change`.

## Walkthrough: payment API (abridged)
1. `init --project payments-api`.
2. Stage 1 yields FR/NFR with idempotency; Q-1 asks about PCI scope. Human answers; `complete requirement-analysis`.
3. Human says "requirements approved". Run `approve requirements --by "<their name>"` then `complete requirement-approval`.
4. Architecture picks a modular monolith (ADR-1). Payment design is security-sensitive: `flag security-sensitive`; human approves with `resolve 1 --decision approve --by ...`; then `approve architecture ...`.
5. HLD, LLD, plan (gate), tasks T1..T6 each mapped to AC ids.
6. Per task: implement, test, security, review (max 3 rounds). The reviewer returns BLOCKED once on a transaction-boundary finding; only that required change returns to the coder.
7. Release readiness lists: tests run (with output), security findings, unverified items, rollback plan. Human approves `release`. Deployment itself is performed by the human or an approved separate process.

## Delegation brief template
Goal; inputs (artifact paths); constraints; the AC ids covered; evidence required back; what NOT to touch.
