# Claude Code adapter

`kw-skills package --platform claude-code` produces `dist/claude-code/knowledgewala-ai-engineering-skills/` (plugin: `.claude-plugin/plugin.json`, `skills/<name>/`, LICENSE, NOTICE) and its zip, plus `per-skill/<name>-<ver>.zip` for copying into `.claude/skills/`.
Frontmatter is passed through unchanged (name, description, license, compatibility, metadata); no Claude-specific fields are added. Not live-tested.
