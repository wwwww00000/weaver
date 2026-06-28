---
title: Foundation
status: draft
page_type: project-hub
projects:
  - foundation
categories:
  - learning
  - math
  - physics
  - ai
  - knowledge-management
source_bundles:
  - foundation/foundation
  - revelation/foundation
  - genesis/foundation
  - weaver/foundation
source_inventory: ops/clusters/2026-06-29/source-inventory.qmd
related:
  - projects/revelation
  - projects/weaver
  - projects/genesis
  - projects/revelation/active-learning-for-math-and-physics
created: 2026-06-29
updated: 2026-06-29
---

# Foundation

Foundation is the proposed software substrate for source-grounded math and
physics study. It should help technical self-study resume across weeks by
turning textbooks into structured, source-linked learning environments with
concept tags, session memory, confusions, and LLM-aided navigation.

The project is Revelation-adjacent but distinct. Revelation owns the actual
math and physics learning path. Foundation owns the tooling that makes that
learning stateful: textbook parsing, provenance, concept indexing, review
artifacts, source-grounded tutoring, and cross-text triangulation.

## Working Model

The core pipeline is:

```text
PDF
  -> parsed pages and blocks
  -> normalized document IR
  -> section outline
  -> block-level tags
  -> concept tags and relations
  -> human review artifacts
  -> searchable learning environment
```

The important constraint is provenance. Every tag, concept, explanation,
summary, and answer should point back to a page, section, block, equation, or
evidence span. For technical learning, a modest map with reliable anchors is
better than a fluent but hallucinated concept graph.

The initial parser should be Docling, but Docling output should be normalized
into a project-owned intermediate representation. The first data stack can stay
boring: JSONL for parsed artifacts, SQLite for normalized records, and SQLite
FTS5 for search.

## Learning Objects

Foundation should make the following objects first-class:

- `document`: textbook metadata, source path, hash, parser version, pages, and
  sections;
- `block`: paragraph, equation, proof step, example, exercise, or semantic
  unit with page and bounding-box provenance;
- `tag`: proposed or accepted block-level classification such as definition,
  theorem, derivation, worked example, warning, or physical interpretation;
- `concept`: canonical name, aliases, definitions, first appearance, and
  related blocks;
- `relation`: introduces, uses, depends on, derives, generalizes, motivates,
  contrasts with, or applies to;
- `confusion`: source passage, question, suspected prerequisite, status,
  resolution note, and review dates;
- `study_session`: dated progress, sources used, confusions resolved, review
  prompts created, and next action.

These objects are not just metadata. They are the handles that make "resume
where I left off" and "explain the hidden step in this derivation" possible.

## Key Interactions

The first useful interactions should be narrow and study-facing:

- resume the last study state with understood material, open confusions, and
  next action;
- jump from a passage to first definition, formal definition, worked example,
  prior use, future use, or related explanation in another text;
- debug derivation gaps by identifying hidden algebra, theorem use, notation
  shifts, or missing prerequisites;
- triangulate concepts across textbooks, especially slow intuitive exposition
  versus formal treatment;
- maintain a confusion ledger and turn unresolved confusions into review cards
  or prerequisite tasks;
- track a personal prerequisite frontier: known, shaky, blocking, upcoming, or
  safe to ignore for now.

## MVP

The first MVP should be deliberately small:

1. Pick one Revelation textbook chapter.
2. Parse it with Docling.
3. Normalize pages, sections, and blocks into JSONL.
4. Generate a section outline.
5. Propose tags for a small subset.
6. Write an editable Markdown review document.
7. Apply accepted review decisions into structured data.
8. Add a tiny search or `ask` command over accepted blocks and tags.
9. Generate a study-session note with progress, confusions, and next action.

Possible command shape:

```bash
foundation ingest shankar.pdf --doc-id shankar_qm
foundation parse shankar_qm --parser docling --pages 1-40
foundation normalize shankar_qm
foundation propose-tags shankar_qm --chapter 1
foundation review shankar_qm --chapter 1 --output review.md
foundation apply-review shankar_qm review.md
foundation ask shankar_qm "Where are observables first defined?"
foundation resume shankar_qm
```

## Boundaries

Use [Revelation](revelation.md) for the study roadmap, exercise work,
conceptual physics questions, and durable math/physics explanations.
Foundation should support Revelation without becoming the place where the
learning itself is stored.

Use [Weaver](weaver.md) for general source ingestion, wiki synthesis,
provenance conventions, context compilation, and project-state surfaces.
Foundation can borrow Weaver's markdown review and provenance style, but its
domain model is textbook-specific and learning-specific.

Use [Genesis](genesis.md) when the work is mainly about building the tool,
agent harness choices, or broader LLM workflow design.

## Open Questions

- What is the right block granularity: paragraph, equation, theorem,
  proof-step, or semantic chunk?
- Should review start as Markdown, a TUI, a small web UI, or something
  editor-native?
- How much of the concept graph should be user-curated versus LLM-proposed?
- How should notation differences across books be represented?
- How should confusions, exercises, and session notes link to source passages?
- What is the smallest interaction that would be useful during an actual
  Revelation study session?

## Source Map

- [Foundation inbox note](../../ops/artifacts/notes/foundation.md)
- [source inventory](../../ops/clusters/2026-06-29/source-inventory.qmd)
