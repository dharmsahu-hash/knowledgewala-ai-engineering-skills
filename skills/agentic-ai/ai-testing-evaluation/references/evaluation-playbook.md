# Evaluation playbook

## Dataset record
| id | input | expected (or rubric) | category | source | sensitivity |
|---|---|---|---|---|---|
Categories: typical, edge, adversarial (injection, jailbreak), unanswerable, regression-from-bug. Version the file; never edit cases silently.

## Metric catalogue
- Exact/contains/regex/schema checks (deterministic).
- Tool-call correctness (right tool, right arguments).
- Rubric score (1-5 per criterion) by human or calibrated model grader.
- RAG: recall@k, groundedness, citation correctness, refusal accuracy.
- System: latency p50/p95, tokens, cost per task.

## Grader calibration
Label 30-50 cases by hand, compare grader agreement (for example Cohen's kappa or simple agreement), fix the rubric until agreement is acceptable, then spot-check periodically.

## Variance
For non-deterministic output run n samples per case (n of at least 3), report mean and spread; do not compare single runs.

## Model comparison table
| Model | Quality (metric, n) | p95 latency | Cost per 1k tasks | Notes |
|---|---|---|---|---|
Same dataset, prompt, temperature and retrieval for every row; record versions and dates.

## Regression rule
A change ships only if no category drops more than the agreed threshold versus the stored baseline and adversarial pass rate does not fall. Failures are reviewed, then either fixed or the threshold change is approved by a human.

## Hallucination tests
Unanswerable questions, questions with false premises, requests for citations to non-existent sources; expected behaviour is refusal or correction, with citation checks against the provided sources.
