# Frontend architecture checklists

## State ownership
| Kind | Owner | Mechanism |
|---|---|---|
| Server data | Data-access layer | Cached queries with explicit invalidation |
| UI state | Component | Local state / signals |
| Form state | Form | Framework form model |
| Navigation state | Router | URL (shareable, bookmarkable) |
| Cross-feature state | Store (only when needed) | Single store per domain |

## Structure
Feature folders own routes, components and data access; a shared kit holds design-system components with no business logic; dependency direction is feature -> shared, never feature -> feature.

## Design system
Tokens (colour, spacing, type, radius, motion) as the only source; components documented with states and a11y notes; visual regression for the kit.

## Errors and loading
Skeleton or spinner after a short delay; empty states with next action; retry for transient failures; global handler for unexpected errors with a correlation id; never show raw server errors.

## Security
CSP, output encoding by default (no raw HTML injection), dependency audit in the pipeline, tokens off URLs and logs, third-party scripts reviewed, authorisation always re-checked on the server.

## Performance budget template
Largest Contentful Paint under 2.5 s on a mid-range mobile profile; initial JS under an agreed KB gzip; interaction latency under 200 ms. Replace with measured targets once baselines exist.

## Testing
Unit for logic, component tests for states, a few end-to-end journeys, accessibility checks in CI, visual regression for the design system.
