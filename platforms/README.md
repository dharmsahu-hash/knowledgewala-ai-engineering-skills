# Platform adapters

Adapter code lives in `tooling/kw_skills/packager.py` (one `build_<platform>` function each); this folder documents what each adapter produces. The canonical skills are never edited by an adapter.

| Folder | Output | Notes |
|---|---|---|
| [claude-code](claude-code/README.md) | plugin bundle + per-skill zips | `.claude-plugin/plugin.json`, `skills/` |
| [cursor](cursor/README.md) | `.cursor/rules/*.mdc` + `.cursor/skills/` | native skills dir unverified |
| [github-copilot](github-copilot/README.md) | `.github/skills/` + `copilot-instructions.md` | |
| [generic-agent](generic-agent/README.md) | per-skill zips | Agent Skills spec; also used for Agensi |

Evidence levels: [docs/COMPATIBILITY.md](../docs/COMPATIBILITY.md).
