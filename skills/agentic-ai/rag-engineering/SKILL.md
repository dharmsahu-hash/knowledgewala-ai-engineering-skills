---
name: rag-engineering
description: Designs and reviews retrieval-augmented generation systems - document ingestion, chunking, embedding and vector store selection, retrieval strategies, hybrid search, reranking, metadata filtering, evaluation and hallucination reduction. Use when building a question-answering or search assistant over private documents, or diagnosing poor retrieval or ungrounded answers.
license: MIT
compatibility: Works in any Agent Skills capable assistant. Vendor and library choices must be checked against current documentation.
metadata:
  title: RAG Engineering Specialist
  version: "1.0.0-rc.3"
  author: KnowledgeWala
  category: agentic-ai
  tags: "rag, retrieval, embeddings, vector-search, chunking, evaluation"
  tier: paid
---

# RAG Engineering Specialist

## Purpose
Build RAG systems whose answers are grounded, cited and measurable, and fix retrieval problems with evidence rather than guesses.

## When to use
- Designing a RAG pipeline over documents.
- Diagnosing wrong, missing or ungrounded answers.
- Choosing chunking, embedding, store or reranking strategies.

## When not to use
- Agent orchestration and tools: use `agentic-ai-architect`.
- Building the broader evaluation harness: use `ai-testing-evaluation`.

## Required inputs
- Document types, volume, update frequency and sensitivity.
- Question types and quality expectations (citations, refusal).
- Hosting, privacy and budget constraints.

## Instructions
1. Establish an evaluation set of real questions before tuning anything.
2. Change one pipeline stage at a time and re-measure.
3. Require citations and an explicit 'cannot answer from the sources' behaviour.
4. State where document content is sent (embedding and model providers) and get approval for third-party transfer of sensitive data.
Detailed checklists and examples: [references/rag-playbook.md](references/rag-playbook.md).

## Workflow
1. Characterise documents and questions.
2. Design ingestion: parsing, cleaning, metadata, deduplication, versioning.
3. Choose chunking and embedding with reasons and alternatives.
4. Select the vector store and retrieval strategy (dense, sparse, hybrid, filters).
5. Add reranking and context assembly with token budgets.
6. Design generation prompts with citation and refusal rules.
7. Evaluate retrieval and answers; iterate on the weakest stage.

## Quality gates
- Evaluation set exists with expected sources for each question.
- Retrieval is measured separately from generation.
- Unanswerable questions are tested and refused correctly.
- Data flow to external providers is documented and approved.
- No accuracy claim without a recorded run.

## Expected output
RAG design document: ingestion, chunking, embedding and store decisions with alternatives, retrieval and reranking design, prompt rules, evaluation plan and results (if run), privacy notes, risks.

## Validation rules
- Metrics are named with formulas (recall@k, MRR, groundedness) and thresholds.
- Each design choice cites a requirement or measured result.
- No real documents or personal data in examples.

## Error handling
- No evaluation set: create one with the user before tuning; do not tune blind.
- Sensitive documents and external providers: stop and request approval.
- Conflicting freshness and cost needs: present options and ask.

## Examples
See the diagnosis table and metric definitions in the reference.

## Limitations
- Cannot measure retrieval quality without the user's documents and questions.
- Embedding model rankings change; verify against current benchmarks on your data.
- Does not guarantee elimination of hallucination.
