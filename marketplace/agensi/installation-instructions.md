# Installation instructions (listing text)

## Through Agensi
Follow Agensi's own instructions to connect your agent; its homepage states skills are delivered through an MCP connector rather than downloaded. Confirm the current steps in your Agensi account, since they are not reproduced here.

## Open-source route (always available)
1. Clone `https://github.com/dharmsahu-hash/knowledgewala-ai-engineering-skills` (once public) or unzip a release archive.
2. Verify checksums against `SHA256SUMS`.
3. Copy a skill folder to your assistant's skills directory:
   - Claude Code: `~/.claude/skills/<skill>/` or `<project>/.claude/skills/<skill>/`
   - GitHub Copilot: `<repo>/.github/skills/<skill>/`
   - Cursor: use `kw-skills package --platform cursor` and unzip at the project root
4. Optional tooling: `pip install -e .` then `kw-skills list`.
5. Ask your assistant to use the skill by name.

Requirements: Python 3.10+ only for skills with scripts (`requirement-analysis`, `code-review`, `ai-sdlc-orchestrator`).
