# Cursor adapter

`kw-skills package --platform cursor` produces a workspace zip with `.cursor/rules/<name>.mdc` (frontmatter `description`, `alwaysApply: false`, body from SKILL.md with resource paths rewritten to `.cursor/skills/<name>/...`) and the skill resources in `.cursor/skills/<name>/`.
The rules mechanism is the targeted one. Cursor's native `.cursor/skills` support is **unverified**; the folder is shipped so rule links resolve. Not live-tested.
