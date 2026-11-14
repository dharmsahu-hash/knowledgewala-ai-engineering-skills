# Compatibility report (listing support)

Summary of [docs/COMPATIBILITY.md](../../docs/COMPATIBILITY.md) as of 1.0.0-rc.3.

- All twenty skills pass the structural checks for generic, Claude Code, GitHub Copilot, Cursor, Codex and Agensi packages (`kw-skills compatibility`).
- **No live discovery or execution test has been performed on any platform.** Do not describe the skills as "tested on Cursor/Copilot/Claude Code" in the listing until the manual checklist in docs/COMPATIBILITY.md is completed.
- OpenAI Codex: layout verified from OpenAI docs; discovery simulated, not live-tested.
- Cursor: rule wrapper is the targeted mechanism; native skills directory support is unverified.
- Agensi: format is the open SKILL.md standard; its scan criteria and submission rules were not publicly documented where we looked; verify in the creator dashboard.
- Skills with scripts need an assistant that can run Python; otherwise they degrade to instructions only.
