# Sample: MySQL database design

## Business request
"Design the database for an exam platform: students, exams, questions, attempts and answers. Attempts table will reach 50 million rows. Existing `results` table must be migrated to the new model."

## Expected orchestrator behaviour
- Delegates to `database-engineering`; asks for MySQL version and query list.
- Produces ER diagram, DDL, justified indexes, expand-and-contract migration with rollback.
- Partitioning or archiving considered with trade-offs, not assumed.

## Human gates
`requirements`, `architecture`, `destructive-db` flag for dropping or rewriting `results`, `plan`, `release`. No SQL is run against any database.

## Acceptance for this sample
Every index tied to a query; migration steps each have a verification query and rollback; destructive step blocked until a human resolves the flag.
