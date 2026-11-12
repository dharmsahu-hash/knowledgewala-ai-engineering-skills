# Marketplace guide (Agensi)

## What is known (agensi.io homepage, 2026-11-12)
SKILL.md open standard; verified creators; 70/30 revenue split; Stripe or USDC payouts; money-back guarantee on paid skills; every version security-scanned with permissions shown; buyers use skills via an MCP connector and cannot export them. Not publicly documented there: submission steps, Agensi-specific SKILL.md rules, versioning, publishing API. **No API or automated upload is implemented or assumed.**

## Prepare
```bash
kw-skills validate
kw-skills marketplace prepare agensi      # listings -> marketplace/agensi/listings, zips -> marketplace/agensi/packages
kw-skills marketplace report
```
`prepare` refuses to run if any skill has validation errors, and never contacts a network.

## Human steps (owner only)
1. Approve public release of the version.
2. Complete Agensi creator verification and read the creator terms there (the tool never accepts terms).
3. Review each generated listing; replace the "pricing proposal" with real prices.
4. Capture real screenshots into `marketplace/agensi/screenshots/` (none are fabricated).
5. Upload `packages/<skill>-<version>.zip` in the Agensi dashboard; check the security-scan result and requested permissions.
6. Verify checksums in `packages/SHA256SUMS` match what was uploaded.
7. Record the submission in `releases/history.json` (`published: true`) only after it is live.

## Distribution policy
GitHub is the canonical source; KnowledgeWala hosts the docs; Agensi and other marketplaces are channels, never the only access path. Because Agensi delivers skills through its connector, check whether its terms conflict with the MIT licence of this repository before listing the same content, and decide licence terms for the marketplace copy.

Details and checklist: `marketplace/agensi/`.
