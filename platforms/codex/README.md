# OpenAI Codex adapter

`kw-skills package --platform codex` produces a workspace zip with `.agents/skills/<name>/` (full skills, tests excluded) and `AGENTS-kw-skills-snippet.md` (to merge into your own `AGENTS.md`, never overwrites one).
Layout follows OpenAI Codex docs (checked 2026-11-14): repo-level `.agents/skills` scanned from the working directory up to the repo root, user-level `$HOME/.agents/skills`. Only `name` and `description` are documented as required; our extra fields (`license`, `compatibility`, `metadata`) are unconfirmed as tolerated. Codex budgets the initial skills list (about 2% of the context window), so large sets may be trimmed. Verified by structure plus a discovery simulation; not live-tested.
