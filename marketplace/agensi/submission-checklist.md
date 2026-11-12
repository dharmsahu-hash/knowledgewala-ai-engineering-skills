# Submission checklist

Tool-verifiable (run and record results):
- [ ] `kw-skills validate` has 0 errors
- [ ] `pytest` passes
- [ ] `kw-skills compatibility` passes
- [ ] `kw-skills marketplace prepare agensi` then `report` shows assets ready
- [ ] `packages/SHA256SUMS` matches the files to upload
- [ ] Secret scan clean (included in validate)

Owner-only (not performed by any tool):
- [ ] Approve public release of this version
- [ ] Agensi creator verification completed
- [ ] Agensi creator terms read and accepted by the owner
- [ ] Final prices set (see pricing-recommendation.md)
- [ ] Real screenshots captured in `screenshots/` (terminal run of `kw-skills validate`, orchestrator status, example output)
- [ ] Listings reviewed; any claim not backed by evidence removed
- [ ] Licence terms for marketplace copy decided (MIT repository versus Agensi no-export terms)
- [ ] Packages uploaded; Agensi security-scan result and requested permissions reviewed
- [ ] Release recorded as published in `releases/history.json`
- [ ] At least one platform live-tested, and `docs/COMPATIBILITY.md` updated (recommended before launch)
