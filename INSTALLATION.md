# Installation

Two parts: the **tooling** (`kw-skills`, optional) and the **skills** (what your assistant loads).

## 1. Tooling (Python 3.10+)

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .          # add ".[dev]" to run tests
.\.venv\Scripts\kw-skills --version
```
```bash
# Linux / macOS
python3 -m venv .venv && .venv/bin/pip install -e .
.venv/bin/kw-skills --version
```
Without installing: `PYTHONPATH=tooling python -m kw_skills --version` (PowerShell: `$env:PYTHONPATH="tooling"; python -m kw_skills --version`).

## 2. Skills into an assistant

Build packages first: `kw-skills package` (all platforms) or `--platform <name>`. Output goes to `dist/<platform>/`. Verify downloads with `dist/release-<version>/SHA256SUMS` when you build a release.

| Assistant | Steps | Verification level |
|---|---|---|
| **Claude Code** | Copy `dist/claude-code/per-skill/<skill>` folders (unzipped) into `~/.claude/skills/` or `<project>/.claude/skills/`. Or unzip the plugin bundle and load it as a plugin directory | Layout matches docs; not live-tested |
| **GitHub Copilot** | Unzip `dist/github-copilot/...zip` at the repository root; it creates `.github/skills/<skill>/` and `.github/copilot-instructions.md` | Layout matches GitHub Docs; not live-tested |
| **Cursor** | Unzip `dist/cursor/...zip` at the project root: rules in `.cursor/rules/*.mdc`, resources in `.cursor/skills/`. Rules are the verified mechanism; the skills folder holds referenced files | Rules documented; native skills dir **unverified**; not live-tested |
| **Other Agent Skills agents** | Copy a folder from `dist/generic/<skill>-<ver>.zip` to the agent's skills directory | Spec-conformant; per-agent behaviour unverified |
| **Agensi** | Manual creator submission by the owner: see [MARKETPLACE_GUIDE](MARKETPLACE_GUIDE.md) | Not submitted |

Quick check after install: ask the assistant "Which skills do you have for requirement analysis?" and confirm it names `requirement-analysis`. Report failures as issues; this is how compatibility moves from structural to live-tested.

## 3. Orchestrator prerequisites
The orchestrator's gate tool needs Python 3.10+ on the machine where the assistant runs commands. Without Python, the skill still works but gate enforcement falls back to instructions only; say so in the closing report.

## Troubleshooting
- `error: cannot find repository root`: run inside the clone or set `KW_SKILLS_ROOT`.
- Skill not discovered: check the folder name equals the `name:` field and `SKILL.md` is at the folder root.
- PowerShell blocks scripts: use `python -m kw_skills ...` instead of wrapper scripts.
