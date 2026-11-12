# Contributing

Thanks for helping. Quality over quantity: one excellent, tested skill beats five average ones.

1. Read [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md).
2. Open an issue before large changes (new skill, new platform adapter).
3. Branch from `main`; keep changes focused.
4. Run the gate locally: `scripts/check.ps1` or `scripts/check.sh`. All must pass.
5. A new or changed skill needs: valid frontmatter, all 12 body sections, `tests/test-cases.md`, a `CHANGELOG.md` entry, and honest limitations.
6. Never add secrets, real customer data, hidden network calls, telemetry, or scripts that delete data or run shell commands.
7. Do not claim a platform "works" or a skill is "production-ready" without recorded evidence; use the status vocabulary in [QUALITY_MODEL](docs/QUALITY_MODEL.md).

## Pull request checklist
- [ ] `kw-skills validate` clean
- [ ] `pytest` passes (paste the summary line)
- [ ] `kw-skills docs --check` passes
- [ ] Docs and changelog updated
- [ ] No secrets or personal data

By contributing you agree your work is released under the MIT License.
