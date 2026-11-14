# Compatibility matrix

Evidence levels: **spec** = conforms to a published spec; **doc** = layout matches the vendor's documentation; **structural** = our automated check of the generated package passes; **live** = an assistant was actually run and discovered/used the skill. **No platform is at `live` yet.**

| Platform | Mechanism we target | Evidence | Structural check | Live-tested | Known gaps |
|---|---|---|---|---|---|
| Generic Agent Skills | `<name>/SKILL.md` + `scripts/ references/ assets/` | spec (agentskills.io) | pass | no | Per-agent support for `allowed-tools` and scripts varies; we don't use `allowed-tools` |
| Claude Code | `.claude/skills/<name>/` or plugin (`.claude-plugin/plugin.json` + `skills/`) | doc + same layout as the existing KnowledgeWala plugin | pass | no | Plugin not installed in a live session here |
| GitHub Copilot | `.github/skills/<name>/SKILL.md`, `.github/copilot-instructions.md` | doc (GitHub Docs: About Agent Skills); VS Code stable rollout stated as in progress | pass | no | Availability depends on the user's Copilot surface and plan |
| Cursor | `.cursor/rules/<name>.mdc` (frontmatter `description`, `alwaysApply: false`) + files in `.cursor/skills/<name>/` | rules: doc-level knowledge; native `.cursor/skills`: **unverified** (secondary sources only) | pass | no | Rule body is the whole SKILL.md; no progressive disclosure; `scripts/` execution depends on the agent |
| OpenAI Codex | `.agents/skills/<name>/SKILL.md` (repo-level, scanned from CWD up to repo root; also `$HOME/.agents/skills`); optional `AGENTS.md` | doc (OpenAI Codex docs: build-skills, agents-md, checked 2026-11-14) | pass, plus a discovery **simulation** | no (Codex not installed here) | Extra frontmatter fields (license, compatibility, metadata) not confirmed as tolerated; initial skills list has a context budget (about 2% of the window), the 20 skills total 7,982 chars of name+description (checked, must stay under the documented 8,000-char fallback), but small windows may still shorten or omit some; `allowed-tools` not used (Codex declares tool needs in `agents/openai.yaml`, not generated) |
| Agensi | Open SKILL.md zip; manual creator upload | homepage only | pass (same as generic) | no | Submission rules and security-scan criteria not public; no publishing API found |

## Feature support caveats
- **Progressive disclosure** (metadata first, body on activation, resources on demand) is a feature of Agent Skills clients. Cursor rules and Copilot instruction files load differently; large skills cost more context there.
- **Scripts:** `validate-output.py`, `check-findings.py` and `sdlc_state.py` require the assistant to run Python. Where it cannot, skills degrade to instruction-only; the orchestrator must say gate enforcement was unavailable.
- We do not claim one SKILL.md behaves identically across platforms.

## How to move a platform to `live`
1. Install the package per INSTALLATION.md on a clean project.
2. Ask: "What skills do you have for code review?" Record whether it names `code-review`.
3. Run test case CR-1 from `skills/quality/code-review/tests/test-cases.md`; save the transcript.
4. Run the orchestrator on `examples/spring-boot-payment-api`; check gates and script execution.
5. Update this table with date, tool version, and result in the same commit as the transcripts.

Re-run structural checks any time: `kw-skills compatibility`.
