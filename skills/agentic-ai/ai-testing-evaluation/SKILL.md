---
name: ai-testing-evaluation
description: Designs and runs evaluation for LLM applications - prompt tests, agent workflow evaluation, RAG evaluation, regression suites, hallucination tests, output validation, model comparison, and cost and latency measurement, reporting only measured results. Use when an LLM feature needs a test plan, when a prompt or model change needs regression checking, or when comparing models.
license: MIT
compatibility: Framework-neutral. Running evaluations requires access to the model under test; this skill never invents results.
metadata:
  title: AI Testing and Evaluation
  version: "1.0.0-rc.2"
  author: KnowledgeWala
  category: agentic-ai
  tags: "llm-evaluation, prompt-testing, regression, hallucination, rag-evaluation, agents"
  tier: paid
---

# AI Testing and Evaluation

## Purpose
Turn 'it seems to work' into measured, repeatable evidence for LLM features, and keep regressions out when prompts or models change.

## When to use
- Creating an evaluation plan or dataset for an LLM feature.
- Checking regressions after a prompt, model or retrieval change.
- Comparing models on quality, cost and latency.

## When not to use
- Designing the agent or RAG system itself: use `agentic-ai-architect` or `rag-engineering`.
- Conventional code tests: use `test-engineering`.

## Required inputs
- The behaviour to evaluate and what 'good' means.
- Representative inputs, ideally from real usage, and known failure cases.
- Access to run the system, or recorded outputs to analyse.

## Instructions
1. Define pass criteria before running anything; version the dataset.
2. Use deterministic checks where possible (schema, exact match, contains, tool called) and rubric or model-graded checks only with a calibrated, spot-checked grader.
3. Run multiple samples for stochastic outputs and report variance.
4. Report only numbers that came from an actual run, with model, prompt version, date and settings.
5. Treat evaluation data containing personal information as sensitive.
Detailed checklists and examples: [references/evaluation-playbook.md](references/evaluation-playbook.md).

## Workflow
1. Define tasks, risks and success criteria.
2. Build the dataset: typical, edge, adversarial and unanswerable cases.
3. Choose metrics and graders; calibrate any model grader against human labels.
4. Run baseline; record configuration.
5. Run candidates (prompt/model/retrieval variants) under the same conditions.
6. Compare with variance, cost and latency; review failures by category.
7. Store results and set regression thresholds for future changes.

## Quality gates
- Pass criteria and dataset are fixed before the run.
- Model-graded metrics are validated on a human-labelled sample.
- Results include n, variance, configuration and date.
- Adversarial and unanswerable cases are included.
- No result is reported that was not produced by a run.

## Expected output
Evaluation plan, versioned dataset description, run records (configuration and metrics), comparison table, failure analysis, regression thresholds and a verdict that states its confidence.

## Validation rules
- Every metric has a definition and a number of samples.
- Comparisons use identical inputs and settings.
- Cost and latency are measured, not estimated, or labelled as estimates.

## Error handling
- Cannot run the model: deliver the plan and mark results 'not run'.
- Dataset too small for a claim: report as exploratory with the sample size.
- Grader disagrees with humans: fix the rubric before trusting scores.

## Examples
See the dataset template, metric catalogue and regression rule in the reference.

## Limitations
- Model-graded evaluation is imperfect and can share model biases.
- Results are valid for the tested configuration and date only.
- Cannot establish safety in general from a finite test set.
