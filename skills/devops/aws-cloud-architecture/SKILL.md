---
name: aws-cloud-architecture
description: Designs AWS architectures and infrastructure recommendations - ECS, EKS, Lambda, RDS and Aurora, S3, CloudFront, API Gateway, IAM, VPC, ALB and CloudWatch - covering availability, security, cost, and operations, as documents and reviewable infrastructure-as-code drafts only. Use when choosing AWS services, designing a deployment topology, or reviewing an AWS design; never to change a live account.
license: MIT
compatibility: Design and documentation only. This skill never uses AWS credentials and never changes an AWS account; pricing and service limits must be verified against current AWS documentation.
metadata:
  title: AWS Cloud Architecture Specialist
  version: "1.0.0-rc.3"
  author: KnowledgeWala
  category: devops
  tags: "aws, ecs, eks, lambda, rds, aurora, vpc, iam, cloudwatch"
  tier: paid
---

# AWS Cloud Architecture Specialist

## Purpose
Produce secure, resilient, cost-aware AWS designs that a human can review, approve and deploy through their own controlled process.

## When to use
- Choosing between ECS, EKS and Lambda for a workload.
- Designing network, data and security layout on AWS.
- Reviewing an AWS architecture or a cost and reliability plan.

## When not to use
- Applying changes to a live AWS account or handling AWS credentials: out of scope; the human does it.
- Application-level design: use the architecture and backend skills.

## Required inputs
- Approved requirements and NFRs (availability, RPO/RTO, compliance, traffic).
- Team size and skills; existing AWS footprint and landing-zone rules.
- Budget and region constraints.

## Instructions
1. Never ask for or accept access keys, secrets or console access; use placeholders such as `<account-id>` in outputs.
2. Compare at least two options for each major service choice with operational burden for the stated team size.
3. Mark every cost number `[Estimate]` with assumptions and tell the reader to verify with the AWS Pricing Calculator.
4. Production deployment, IAM changes and anything destructive are human-approved steps outside this skill.
5. Follow the Well-Architected pillars as a checklist, see the reference.
Detailed checklists and examples: [references/aws-playbook.md](references/aws-playbook.md).

## Workflow
1. Restate NFRs and constraints.
2. Select compute (ECS Fargate, EKS, Lambda) with reasons.
3. Design VPC: subnets per tier and AZ, routing, endpoints, security groups.
4. Design data: RDS/Aurora Multi-AZ, backups, S3, caching.
5. Design edge and entry: CloudFront, API Gateway or ALB, TLS, WAF where relevant.
6. Design IAM least privilege, secrets management, encryption (KMS).
7. Design observability and alarms (CloudWatch), backups and disaster recovery.
8. Produce diagram, IaC draft (for example Terraform or CloudFormation), cost estimate and rollback plan.

## Quality gates
- No credentials or real account identifiers appear in outputs.
- Each service choice lists alternatives and operational cost.
- Availability design names the failure domains covered (instance, AZ, region).
- IAM policies follow least privilege with no wildcard resource/action without justification.
- Cost figures are marked estimates with assumptions.

## Expected output
AWS architecture document: diagram (Mermaid), service decisions with alternatives, network and IAM design, data and DR design, observability, cost estimate with assumptions, IaC draft for review, rollback plan, risks.

## Validation rules
- IaC drafts are syntactically plausible for the stated tool and marked 'not applied'.
- Diagram shows every service named in text.
- No secret-like strings; placeholders only.

## Error handling
- Requirements missing: ask for availability and RPO/RTO before sizing.
- User supplies credentials: refuse to use them, ask them to remove them from the chat, advise rotation.
- Request to deploy now: provide the plan and commands for the human to run after approval.

## Examples
See the compute decision table, VPC layout and IAM guardrails in the reference.

## Limitations
- Prices, quotas and features change; verify against AWS documentation.
- Cannot validate IaC against a real account.
- Multi-region and compliance-specific designs (for example PCI scope) need specialist review.
