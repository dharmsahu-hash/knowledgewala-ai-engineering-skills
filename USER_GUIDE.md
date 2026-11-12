# User guide

## The idea
Don't ask an assistant to "build X". Ask it to run X through the lifecycle, and approve at the gates.

## Run a project with the orchestrator
1. Install the skills (see [INSTALLATION](INSTALLATION.md)).
2. Say: *"Use ai-sdlc-orchestrator for this project: <business request>."*
3. The assistant initialises `.kw-sdlc/state.json`, runs requirement analysis and asks clarification questions. Answer them.
4. Review `docs/sdlc/requirements.md`. Say *"requirements approved"* and give your name; the assistant records it. It cannot approve for you.
5. Repeat for architecture, plan and release gates.
6. When the assistant raises a flag (destructive database change, security-sensitive change, secrets, production deploy, scope change) decide explicitly. Nothing proceeds until you do.
7. Read the closing report: completed stages, evidence, open risks, and what was **not** verified.

Check progress any time: `python orchestrators/ai-sdlc-orchestrator/scripts/sdlc_state.py status` (or ask the assistant to run it).

## Use a single skill
Each skill works alone, for example:
- *"Use code-review on this diff."* returns findings with severity, `path:line`, impact, remediation, and a verdict.
- *"Use database-engineering to tune this query (EXPLAIN attached)."*
- *"Use requirement-analysis on this ticket."* then validate: `python skills/architecture/requirement-analysis/scripts/validate-output.py out.md`.

## Rules the skills follow
- Inference is labelled; unknowns become questions.
- Tests are reported only if run, with the real command and output.
- Destructive and security-sensitive actions need your explicit approval.
- No credentials are requested or stored; examples use placeholders.

## CLI cheat sheet
| Command | Purpose |
|---|---|
| `kw-skills list` | Show skills, versions, categories |
| `kw-skills validate [skill]` | Structural validation |
| `kw-skills package [--platform p] [--skill s]` | Build packages (`--json` for machine output) |
| `kw-skills compatibility` | Structural platform checks |
| `kw-skills docs [--check]` | Regenerate or verify the catalogue |
| `kw-skills release [history\|rollback --version V]` | Local release artifacts |
| `kw-skills marketplace prepare agensi` / `report` | Submission assets and readiness |
| `kw-skills eval score <rubric> <scores>` | Weighted score from a recorded evaluation |

Exit codes: 0 success, 1 check failed, 2 usage or input error.

## Scoring a skill run
Run the skill on a sample brief, evaluate the result against `evals/rubrics/payment-api.json` (0-10 per criterion with rationale), save as JSON with `evaluator` and `run_date`, then `kw-skills eval score evals/rubrics/payment-api.json my-scores.json`. Save accepted results in `evals/results/<skill>.json`.
