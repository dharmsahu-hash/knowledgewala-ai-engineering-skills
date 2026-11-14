# Architecture

One canonical source, many generated outputs. Everything generated is reproducible and disposable; only `skills/` and `orchestrators/` are authoritative.

## Product architecture

```mermaid
flowchart TB
  subgraph Source[A. Canonical repository]
    S[skills/**/SKILL.md]:::src
    O[orchestrators/ai-sdlc-orchestrator]:::src
  end
  subgraph Tooling[tooling/kw_skills - Python stdlib only]
    V[B. Validator] --> P[C. Packager adapters]
    P --> C[D. Compatibility checks]
    D[E. Docs generator]
    R[F. Release manager]
    M[G. Marketplace preparation]
    E[Evals scorer]
  end
  S & O --> V
  P --> OUT[(dist/ per platform)]
  R --> OUT
  M --> AG[marketplace/agensi - manual upload]
  classDef src fill:#e8f1ff,stroke:#2b6cb0;
```

Layer to module map: A `skills/`, `orchestrators/` · B `validator.py` · C `packager.py` · D `compatibility.py` · E `docsgen.py` · F `release.py` · G `marketplace.py` · evaluation `evals.py` · CLI `cli.py`.
The brief proposed `tooling/validator|packager|...` directories; one flat package was chosen instead because the layers share the parser and finding types, and a single zero-dependency package is simpler to install and test.

## Skill execution lifecycle

```mermaid
sequenceDiagram
  participant H as Human
  participant A as Assistant
  participant G as sdlc_state.py
  participant S as Specialist skill
  H->>A: business request
  A->>G: init
  loop stages 1..16
    A->>S: delegate with approved artifacts
    S-->>A: output + evidence
    A->>G: complete stage --evidence
    G-->>A: refuse if order, evidence, approval or flag missing
  end
  A->>H: stop at gate / flag
  H->>A: approval in chat
  A->>G: approve gate --by <human name>
```

Progressive disclosure: only `name` and `description` are loaded at startup; `SKILL.md` on activation; `references/`, `templates/`, `scripts/` only when needed.

## Packaging workflow

```mermaid
flowchart LR
  A[validate] -->|errors block| X((stop))
  A --> B[package per platform]
  B --> C[deterministic zips + sha256]
  C --> D[compatibility checks on output]
  D --> E[release: SHA256SUMS + notes + history]
```

## Platform compatibility

```mermaid
flowchart LR
  C[canonical SKILL.md] --> G[generic: skill folder zips]
  C --> CC[Claude Code: plugin + .claude/skills]
  C --> CU[Cursor: .cursor/rules .mdc + resources]
  C --> GH[Copilot: .github/skills + instructions]
  C --> CX[Codex: .agents/skills + AGENTS.md snippet]
  C --> AG[Agensi: SKILL.md zips, manual upload]
```

Adapters never edit the canonical skill; they copy, wrap or rewrite paths. Evidence level per platform is in [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md).

## Marketplace release process

```mermaid
flowchart LR
  P[marketplace prepare agensi] --> R[marketplace report]
  R --> H1{{Owner approves release}}
  H1 --> H2{{Owner verified as creator, accepts terms}}
  H2 --> H3{{Owner sets prices}}
  H3 --> U[Owner uploads via Agensi dashboard]
  U --> SC[Agensi security scan]
```
Diamond-shaped steps are human gates; the tool performs none of them.

## Key decisions

| Decision | Reason |
|---|---|
| Stdlib-only Python, custom frontmatter parser | No dependency supply-chain risk; frontmatter subset is strict and errors loudly |
| Gate logic in a script | Models skip steps; code does not |
| Zero network in tooling | Marketplace and platform uploads are human actions; satisfies "no hidden telemetry" |
| Deterministic zips | Reproducible checksums for release and rollback |
| No database or web UI | No requirement justifies one yet; Skill Explorer is a roadmap phase |
| Honest compatibility levels | `structural` vs `live-tested`, never merged |
