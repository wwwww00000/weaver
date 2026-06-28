---
project: weaver
status: active
updated: 2026-06-29
wiki: ../../../wiki/projects/weaver.md
review_cadence: weekly
tags:
  - project-status
  - active
  - knowledge-management
  - agentic-workflows
---

<!-- weaver:project-status-card v1 -->

# Weaver Status

## Current Focus

Personal knowledge-system project for source triage, compiled wiki synthesis,
status surfaces, provenance, and future context compilation. Current center is
making the repo usable as the durable state layer for projects, weekly review,
and agent-assisted synthesis.

## Recent Changes

- Weaver was promoted from a Genesis child page to a top-level project hub.
- Project status cards were added as the live project-state layer.
- Initial Obsidian and ChatGPT ingest, artifact generation, QMD inventory, and
  first synthesis pass are complete.

## Decisions

- Treat Weaver as a peer of Genesis, not a Genesis subproject.
- Keep deterministic source ingestion and provenance separate from
  human-directed or agent-directed synthesis.
- Use markdown, git history, task templates, source maps, and status cards as
  the repeatability layer before adding heavier automation.
- Do not rewrite historical generated manifests only to reflect a later project
  promotion.
- Remove stale project-overview maintenance pressure from weekly notes; project
  cards and hubs should own current project state.

## Next Actions

- Decide how repo-native weekly notes should interact with project status
  cards and the Obsidian vault.
- Trial the current Weaver/status-card workflow for a few weeks before deciding
  whether to move periodic notes fully into the repo and Neovim.
- Prototype the smallest useful context-compiler loop over one project.
- Tighten frontmatter and project/status-card conventions after a few live
  review cycles.
- Keep project-promotion mechanics documented and repeatable.

## Open Questions

- What exact material should live in weekly notes versus project status cards?
- What should replace Obsidian's periodic-notes calendar view if the workflow
  moves into Neovim?
- Which context items must be loaded deterministically, and which should be
  retrieved by agent judgment?
- Should semantic tags remain a convention first, or become parser-backed
  extraction handles?
- What should the first Weaver tool beyond triage and inventory generation do?

## Blocked Or Waiting

- Waiting on design decisions about weekly-note integration, context compiler
  scope, and how much automation should exist before repeated manual review
  exposes stable task shapes.

## Promote To Wiki

- Stable weekly-note and status-card workflow decisions.
- Context-compiler object model and minimal prototype design.
- Project promotion, demotion, and boundary conventions that survive use.
- Validation rules for frontmatter, links, status cards, and source maps.

## Links

- [Weaver wiki](../../../wiki/projects/weaver.md)
- [Genesis status](genesis.md)
- [Chronicle status](chronicle.md)
- [Project dashboard](../dashboard.md)
