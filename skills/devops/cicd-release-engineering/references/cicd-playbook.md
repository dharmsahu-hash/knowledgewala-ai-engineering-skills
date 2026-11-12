# CI/CD playbook

## Stage template
1. **Build**: reproducible, cached dependencies, pinned toolchain.
2. **Test**: unit, then integration; fail fast; publish reports.
3. **Scan**: dependency audit, secret scan, static analysis; failures block.
4. **Package**: versioned artifact or container image; checksum or digest recorded.
5. **Deploy staging**: automatic.
6. **Verify**: smoke tests and health checks.
7. **Approve**: manual gate for production by a named role.
8. **Deploy production**: strategy below; automatic rollback on failed health checks.

## Deployment strategies
| Strategy | Use when | Rollback |
|---|---|---|
| Rolling | Stateless, backward-compatible releases | Redeploy previous version |
| Blue/green | Need instant switch and rollback | Switch traffic back |
| Canary | Risky change, good metrics | Stop and route back to stable |
Database changes ship expand-and-contract so old and new versions both work; destructive steps are a separate approved release.

## Container checklist
Minimal base image pinned by digest, multi-stage build, non-root user, no secrets baked in, read-only filesystem where possible, health check, vulnerability scan.

## Environment configuration
Same artifact in every environment; configuration injected per environment; secrets from a secret store; a table lists each variable, its owner and where it is set.

## Rollback checklist
Previous artifact retained; rollback command documented and rehearsed; data compatibility confirmed; communication plan; post-rollback verification query or smoke test.

## Cost-aware triggering
When CI minutes are limited, run pipelines manually or on merge to the main branch only, and keep a local pre-commit check script as the first gate.

## Supply chain
Pin actions and images, least-privilege tokens for CI, protected branches, required reviews, signed or checksummed artifacts, review third-party actions before use.
