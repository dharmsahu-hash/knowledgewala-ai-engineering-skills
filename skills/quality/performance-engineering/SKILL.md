---
name: performance-engineering
description: Diagnoses and improves application performance from measurements - CPU, memory, database and query efficiency, API latency, throughput, concurrency, caching and resource utilisation - with baseline, change and re-measurement for every claim. Use when an endpoint or job is slow, capacity is in question, or a performance requirement must be verified.
license: MIT
compatibility: Works in any Agent Skills capable assistant. Measurements require running the system; load tests need an approved non-production environment.
metadata:
  title: Performance Engineering Specialist
  version: "1.0.0-rc.3"
  author: KnowledgeWala
  category: quality
  tags: "performance, profiling, latency, throughput, caching, concurrency"
  tier: paid
---

# Performance Engineering Specialist

## Purpose
Make systems faster by finding the actual bottleneck and proving each improvement, instead of optimising by intuition.

## When to use
- A slow endpoint, query, page or job needs diagnosis.
- A latency or throughput requirement must be verified.
- Capacity or resource usage is a concern.

## When not to use
- Pure SQL tuning with plans: start with `database-engineering`.
- Load testing production systems: not without explicit approval and a safe plan.

## Required inputs
- The performance requirement (for example p95 under 300 ms at 200 requests/second).
- A reproducible scenario and the environment it runs in.
- Existing metrics, traces, profiles or logs.

## Instructions
1. Measure first. Without a baseline, every suggestion is labelled `[Hypothesis]`.
2. Change one thing at a time and re-measure under the same conditions.
3. Report the slowest stage (the bottleneck), not a list of everything that could be faster.
4. Never run load against production or third-party systems without explicit approval.
5. Quote only numbers from real runs, with tool, environment and date.
Detailed checklists and examples: [references/performance-playbook.md](references/performance-playbook.md).

## Workflow
1. Restate the requirement and define the metric (percentile, throughput, resource).
2. Reproduce the problem and record a baseline with variance.
3. Locate the bottleneck with traces, profiler or query plans.
4. Form a hypothesis, make one change, re-measure.
5. Check side effects (correctness, memory, tail latency, other endpoints).
6. Repeat until the requirement is met or the limit is understood.
7. Write findings and regression guards (performance test, budget, alert).

## Quality gates
- Baseline and after numbers use the same scenario and environment.
- Improvement exceeds measurement noise.
- Correctness tests still pass.
- No unmeasured optimisation is left in the change.
- Load tests ran only in an approved environment.

## Expected output
Performance report: requirement, method, baseline, bottleneck evidence, changes with before/after numbers, remaining risks, regression guards.

## Validation rules
- Each claim cites a measurement or is tagged `[Hypothesis]`.
- Percentiles are reported, not only averages.
- Scenario is reproducible from the report.

## Error handling
- No ability to run or measure: deliver a measurement plan; mark results not run.
- Result inside noise: report no significant change.
- Optimisation breaks tests: revert it and report.

## Examples
See the bottleneck table and experiment log template in the reference.

## Limitations
- Results hold for the measured environment and data size.
- Cannot predict production behaviour from a laptop run without stating the gap.
- Micro-benchmarks can mislead; prefer end-to-end scenarios.
