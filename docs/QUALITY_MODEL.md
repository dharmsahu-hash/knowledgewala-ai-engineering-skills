# Quality model

A skill passing Markdown validation is not a skill that produces good engineering. Four separate layers, never merged:

| Layer | Question | How | Status today |
|---|---|---|---|
| 1 Structural | Is it well-formed and safe to ship? | `kw-skills validate` (spec, policy, links, secrets, script safety) | 10/10 skills pass |
| 2 Functional | Do the executable parts work? | pytest: CLI, packagers, gate script (`sdlc_state.py`), output checkers | passing (see test results in the delivery report) |
| 3 Platform compatibility | Does each platform load it? | `kw-skills compatibility` (structural) plus manual live checklist | structural pass; live: none |
| 4 Real-world quality | Does it produce good engineering outcomes? | Run on sample briefs; score with a rubric | **0 evaluations recorded** |

## Production-ready definition
A skill may be called production-ready only when layers 1-3 pass **and** layer 4 has at least three recorded runs on different briefs with a score of 80+ out of 100 from an evaluator who is not the skill's author, plus the live platform check on at least one platform. None qualifies yet; all skills are `release candidate`.

## Scoring
Rubrics live in `evals/rubrics/`. Example: payment API (correctness 20, architecture 10, idempotency 15, transactions 10, security 15, error handling 8, unit testing 10, performance 5, documentation 7). Evaluator gives 0-10 per criterion with rationale; `kw-skills eval score` validates completeness and computes /100. Scores without rationale, evaluator or date are rejected. Accepted results are stored as `evals/results/<skill>.json`; `marketplace report` counts them.

## Token efficiency
`SKILL.md` bodies are capped at 500 lines (error) and about 5000 tokens (warning, estimated as characters/4, a coarse heuristic). Details live in `references/` and are loaded on demand. Measured token counts with a real tokenizer have not been collected.

## Reliability and consistency
Planned: repeat each sample three times and compare gate behaviour and findings. Not yet done.
