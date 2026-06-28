---
project: foundation
status: incubating
updated: 2026-06-29
wiki: ../../../wiki/projects/foundation.md
review_cadence: as-needed
tags:
  - project-status
  - incubating
  - learning
  - math
  - physics
  - ai
---

<!-- weaver:project-status-card v1 -->

# Foundation Status

## Current Focus

Incubating source-grounded learning environment for math and physics textbooks:
parse textbook PDFs, preserve page/block provenance, propose concept and block
tags, support human review, and make study state resumable.

## Recent Changes

- Foundation seed note was ingested through the repo-native notes pipeline.
- Foundation was synthesized as a top-level project hub distinct from
  Revelation, Weaver, and Genesis.

## Decisions

- Treat Foundation as its own project rather than a Revelation page.
- Revelation owns the study path and learned math/physics content.
- Foundation owns the textbook-ingestion, concept-indexing, review, and
  source-grounded tutoring substrate.
- Start with Docling, but normalize parser output into a project-owned IR.

## Next Actions

- Pick one Revelation textbook chapter for the first dogfood pass.
- Run Docling and inspect output quality before designing too much schema.
- Define the first block/section JSONL shape.
- Generate one Markdown review artifact for proposed tags.

## Open Questions

- What is the right block granularity for math and physics sources?
- Should the first review UI be plain Markdown, TUI, web, or editor-native?
- How should confusions, exercises, and session notes link back to source
  passages?
- What smallest interaction would make a real study session easier to resume?

## Blocked Or Waiting

- Waiting on selection of the first textbook chapter and a decision to begin
  an implementation pass.

## Promote To Wiki

- First parsed chapter review.
- Normalized document IR.
- Accepted tag ontology revisions.
- Study-session and confusion-ledger examples.

## Links

- [Foundation wiki](../../../wiki/projects/foundation.md)
- [Revelation status](revelation.md)
- [Weaver status](weaver.md)
- [Genesis status](genesis.md)
- [Project dashboard](../dashboard.md)
