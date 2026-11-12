# Sample: RAG application

## Business request
"A support assistant that answers questions from our product documentation (PDF and Markdown) and cites sources. It must say when it does not know."

## Expected orchestrator behaviour
- Requirements include citation, refusal behaviour, freshness, and data privacy for documents.
- Delegates to `rag-engineering`, `agentic-ai-architect` and `ai-testing-evaluation`.
- Design covers ingestion, chunking, embeddings, vector store choice, hybrid retrieval, reranking and metadata filters, each with alternatives.
- An evaluation plan (retrieval hit rate, groundedness, hallucination tests on unanswerable questions) is part of the plan, not an afterthought.

## Human gates
`requirements`, `architecture` (third-party model/data transfer is `security-sensitive`), `plan`, `release`.

## Acceptance for this sample
Unanswerable-question tests defined; evaluation metrics named with thresholds; data flow to external model providers stated explicitly; no claims of measured accuracy without a run.
