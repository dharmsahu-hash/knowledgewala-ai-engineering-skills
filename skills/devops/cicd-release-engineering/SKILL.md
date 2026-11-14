---
name: cicd-release-engineering
description: Designs build, test and release pipelines - automated testing, artifact management, containerisation, deployment strategies, rollback plans, environment configuration, release validation and infrastructure as code - with approval gates before production. Use when creating or reviewing a CI/CD pipeline, planning a release or rollback, or hardening how software reaches production.
license: MIT
compatibility: Tool-neutral (GitHub Actions, GitLab CI, Jenkins, others). Pipelines are produced as drafts for review; this skill never triggers a deployment.
metadata:
  title: CI/CD and Release Engineering
  version: "1.0.0-rc.3"
  author: KnowledgeWala
  category: devops
  tags: "cicd, pipelines, containers, deployment-strategies, rollback, iac, release"
  tier: paid
---

# CI/CD and Release Engineering

## Purpose
Make releases repeatable, tested, reversible and approved, without automatic production changes.

## When to use
- Creating or reviewing a CI/CD pipeline.
- Planning a release strategy and rollback.
- Containerising an application for delivery.

## When not to use
- Triggering or performing production deployments: humans do that after approval.
- Cloud topology design: use `aws-cloud-architecture`.

## Required inputs
- Repository layout, build tools and test commands (inspect them).
- Target environments and who approves promotion.
- Constraints: CI minutes budget, compliance, release cadence.

## Instructions
1. Inspect how the project builds and tests today and automate that, not an imagined setup.
2. Pipelines never contain secrets; reference the CI secret store by name.
3. Production deployment requires a manual approval step and a documented rollback; the pipeline must not deploy production on push by default.
4. Respect cost constraints: prefer manual or scheduled triggers when the owner has said CI minutes matter.
5. Pin third-party actions/images to versions or digests and note supply-chain risk.
Detailed checklists and examples: [references/cicd-playbook.md](references/cicd-playbook.md).

## Workflow
1. Inventory build, test, lint and security steps.
2. Define stages: build, test, scan, package, publish artifact, deploy to staging, verify, approve, deploy production.
3. Containerise with a minimal, non-root image and a reproducible build.
4. Choose deployment strategy (rolling, blue/green, canary) with health checks.
5. Define environment configuration and secrets handling per environment.
6. Write the rollback and release-validation plan.
7. Draft the pipeline files and a release checklist for review.

## Quality gates
- Every stage has a defined failure behaviour and the pipeline stops on failure.
- No secrets in pipeline files, images or logs.
- Production step needs manual approval and a tested rollback path.
- Artifacts are versioned, immutable and checksummed.
- Release validation (smoke tests) is defined for each environment.

## Expected output
Pipeline draft files, release and rollback runbook, environment configuration table, deployment strategy decision with rationale, risks.

## Validation rules
- Pipeline syntax is valid for the stated CI tool (checked with its linter when available, else marked unchecked).
- Third-party actions and base images are pinned.
- Rollback steps are concrete commands or procedures, each with a verification step.

## Error handling
- Unknown build/test commands: inspect the repo or ask; do not guess.
- Request for auto-deploy to production on merge: explain the risk and propose approval-gated promotion.
- Secrets requested for the pipeline: reference the secret store names only.

## Examples
See the stage template, strategy table and rollback checklist in the reference.

## Limitations
- Cannot run pipelines on the user's CI; drafts are unexecuted unless the user runs them.
- Tool-specific syntax varies by version; verify with the tool's documentation.
- Does not manage infrastructure state or credentials.
