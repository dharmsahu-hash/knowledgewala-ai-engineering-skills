# Security

## Reporting
Report vulnerabilities privately through GitHub's "Report a vulnerability" (Security tab) on this repository. Do not open public issues for exploitable problems. We aim to acknowledge within 7 days; this is a best-effort commitment, not an SLA.

## Security model
Skills are instructions plus optional small scripts, and are treated as **potentially untrusted code** when they come from anywhere else (including marketplaces).

| Control | Where enforced |
|---|---|
| No hardcoded secrets in any skill file | Validator V011 (patterns for cloud keys, tokens, private keys, credential assignments); repo-wide test |
| Scripts cannot use network, subprocess, `eval`/`exec`, `os.system`, recursive delete | Validator V013 (AST check); non-Python scripts raise a manual-review warning |
| Unsafe instructions (pipe-to-shell, broad `rm -rf`, `chmod 777`, `Invoke-Expression`) | Validator V012 warning unless framed as a prohibition |
| Tooling makes no network calls, no telemetry, uploads no source code | By design; zero dependencies; review `tooling/` |
| No automatic destructive actions, deploys or approvals | Skill rules; orchestrator script refuses AI-named approvers and blocks on pending flags |
| Human approval for architecture, destructive DB, security-sensitive, secrets, production deploy, scope change | Orchestrator gates and flags |
| Reproducible artifacts with checksums | Deterministic zips, `SHA256SUMS` |
| Manual workflows only in CI | `workflow_dispatch` only (tested) |

## Consuming third-party skills
Never run a downloaded skill's scripts without reading them. Extract archives into an empty directory, inspect `SKILL.md` and `scripts/`, and run any Python with `python -I` inside a sandbox or container without network access.

## Known limits
- The validator uses pattern matching; it will miss obfuscated secrets or malicious logic. It reduces risk and does not prove safety.
- The orchestrator cannot verify that an approval really came from a human; it only rejects obvious non-human names and records who approved.
- A security review of this repository by an independent party has **not** been performed. The self-review is in [docs/SECURITY_REVIEW.md](docs/SECURITY_REVIEW.md).
