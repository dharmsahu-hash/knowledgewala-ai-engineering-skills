# Security self-review (1.0.0-rc.1, 2026-11-12)

Performed by the author's tooling and a manual read. **Not an independent audit.**

## Executed checks
| Check | Result |
|---|---|
| `kw-skills validate` over all 10 skills (secrets V011, unsafe markdown V012, script safety V013) | 0 errors, 0 warnings |
| Repo-wide secret-pattern test over all tracked text (`tests/test_repo_governance.py`) | pass |
| Grep of `tooling/` for network modules, `subprocess`, `os.system`, `eval`, `exec` | none used; only the validator's own deny-list and a function named `cmd_eval` match |
| Skill scripts (`validate-output.py`, `check-findings.py`, `sdlc_state.py`) AST-checked | read/write local files only; no network or process spawning |
| CI workflow triggers | `workflow_dispatch` only (tested) |
| Dependencies | runtime: none; dev: pytest |

## Manual review notes
- `shutil.rmtree` is used only inside `packager.py` (its own `dist/` staging folders) and `release.py` (`dist/release-<version>` for a version that exists in history, and rebuild of the same). Neither accepts arbitrary paths. The validator forbids `rmtree` in *skills*, not in tooling.
- `sdlc_state.py` never overwrites an existing state file on `init`, and rejects AI-like approver names. A determined user can still type any name; it records, it does not authenticate.
- Cursor adapter rewrites relative paths with a regex; output is checked for dangling references.

## Findings
| ID | Severity | Status | Description |
|---|---|---|---|
| S-1 | Low | Open (accepted) | Secret and unsafe-pattern detection is regex-based and can miss obfuscation; documented in SECURITY.md |
| S-2 | Low | Open (accepted) | Approvals are not authenticated; recorded only |
| S-3 | Info | Open | No independent review or third-party SAST run yet; recommended before public release |

No confirmed vulnerabilities found. This does not mean none exist.
