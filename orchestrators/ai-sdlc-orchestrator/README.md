# ai-sdlc-orchestrator

Flagship skill: runs the 16-stage lifecycle with enforced order, evidence and human approval gates.

- Entry point: [SKILL.md](SKILL.md); stages and delegation: `references/stages.md`
- Gate tool: `python scripts/sdlc_state.py --help` (tested by the repository's pytest suite)
- Sample projects: `examples/` at the repository root
- Test scenarios: `tests/test-cases.md`
- Status: structurally and functionally (gate tool) tested. End-to-end quality with a real assistant: not yet evaluated.
