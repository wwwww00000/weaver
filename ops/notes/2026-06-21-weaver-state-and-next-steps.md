# Weaver State And Next Steps

Date: 2026-06-21
Updated: 2026-06-28

This note supersedes the initial `HANDOFF.md` as the current working state for
the Weaver repo.

## Current State

The initial bulk ingest and synthesis pass is complete.

Weaver now contains deterministic tooling for triaging personal knowledge
sources, copied source artifacts for review, a generated source inventory, and
a first curated wiki synthesized from Obsidian notes and ChatGPT conversations.

The active mode is no longer "ingest more source material." The active mode is:

- review synthesized wiki pages;
- correct emphasis, naming, and boundaries;
- flesh out pages just-in-time as projects become active;
- discuss design questions for making the workflow more repeatable;
- run a new triage/import cycle only when new source material arrives.

## Deterministic Tooling

Implemented tooling lives in the Python package `weaver`, exposed through a
Typer CLI.

Core commands are documented in [README.md](../../README.md):

- `weaver triage obsidian`
- `weaver triage apply`
- `weaver triage chatgpt`
- `weaver triage apply-chatgpt`
- `weaver cluster qmd`

The Obsidian command defaults to the local vault at
`/mnt/c/Users/limwe/Documents/obsidian` and skips low-signal bulk directories
such as `daily/` and `weekly/` by default. The most recent weekly context note,
`weekly/2026-W25.md`, was manually added because it contained active project
context that was intentionally excluded from bulk triage.

## Source Ingestion

Obsidian ingestion is complete for the initial pass.

Important outputs:

- triage document: `ops/triage/obsidian.md`
- triage snapshot: `ops/triage/snapshots/obsidian-triage-2026-06-21-initial.md`
- manifest: `ops/manifests/obsidian.csv`
- copied selected notes: `raw/obsidian/`
- intermediate artifacts: `ops/artifacts/obsidian/`

ChatGPT ingestion is complete for the initial pass.

Important outputs:

- split triage documents under `ops/triage/`
- manifest: `ops/manifests/chatgpt.csv`
- copied selected JSON and transcripts: `raw/chatgpt/`
- intermediate artifacts: `ops/artifacts/chatgpt/`

The deterministic inventory workbench was generated from both artifact sets:

- `ops/clusters/2026-06-24/source-inventory.qmd`
- `ops/clusters/2026-06-24/manifest.csv`

## Project Context

Project names and descriptions are captured in:

- `ops/context/projects.md`
- `ops/context/project-glossary.yaml`
- `ops/context/chatgpt-project-glossary.yaml`

Project names are a separate axis from category labels. Category labels were
useful for source retrieval and initial bundle formation, but downstream wiki
organization now relies on project glossaries, source paths, titles, project
IDs, and synthesis judgment.

Important project code names:

- `obelisk`: old crypto trading project; archive-mode.
- `p12n`: active crypto trading project with a machine-learning focus.
- `accretion`: personal finance and wealth accumulation.
- `whetstone`: cognition improvement.
- `chronicle`: morning pages, journaling, creative writing, mindfulness, and
  meditation.
- `conjuration`: imagination building, creativity, and drawing.
- `revelation`: math and physics learning.
- `genesis`: building things, exercising agency, AI-adjacent work, and AI
  research.

## Synthesis State

The first intelligent synthesis pass has been performed by Codex against the
triaged artifacts and generated source inventory.

The named project hub pass is complete:

- [Obelisk](../../wiki/projects/obelisk.md)
- [P12n](../../wiki/projects/p12n.md)
- [Accretion](../../wiki/projects/accretion.md)
- [Whetstone](../../wiki/projects/whetstone.md)
- [Chronicle](../../wiki/projects/chronicle.md)
- [Conjuration](../../wiki/projects/conjuration.md)
- [Revelation](../../wiki/projects/revelation.md)
- [Genesis](../../wiki/projects/genesis.md)

Major topic hubs and supporting pages now exist under:

- [Quant](../../wiki/topics/quant.md)
- [Personal](../../wiki/topics/personal.md)
- [Poker](../../wiki/topics/poker.md)
- [Reading Notes And Books](../../wiki/topics/reading-and-books.md)
- [Music Practice And Tools](../../wiki/topics/music.md)

The major `unassigned/*` mining queues have been routed and mined:

- `unassigned/quant`
- `unassigned/ai`
- `unassigned/cognitive`
- `unassigned/personal`
- `unassigned/writing`
- `unassigned/math`
- `unassigned/drawing`
- residual queues such as `book`, `idea`, `creativity`, `poker`, `art`,
  `physics`, `machine learning`, `music`, `finance`, `travel`, and the small
  reference-only tail.

The current synthesis audit trail is:

- `ops/synthesis/wiki-hub-todo.md`
- `ops/synthesis/residual-unassigned-mining-plan.md`
- the per-queue mining plans in `ops/synthesis/`
- `ops/process/wiki-synthesis-playbook.md`
- `ops/process/wiki-synthesis-task-template.md`

## Current Workflow

The source wrappers and raw transcripts remain the provenance layer. The wiki
is the curated layer. Future work should preserve that separation.

Use this workflow for new material:

1. Run deterministic triage.
2. Review triage Markdown manually.
3. Apply selected sources into raw copies and artifacts.
4. Regenerate the QMD inventory.
5. Use the synthesis playbook and task template for any agent-assisted pass.
6. Commit each coherent synthesis or review pass.

Use this workflow for existing wiki material:

1. Pick a page or active project.
2. Read the page and its source map.
3. Pull raw artifacts only where more context is needed.
4. Correct, deepen, split, or cross-link the page.
5. Keep provenance compact and local.
6. Commit the review/fleshing pass.

## Open Design Questions

The next discussion should focus on workflow design rather than more bulk
ingestion.

Important questions:

- How much of the synthesis process should stay Codex-thread-driven versus be
  reified as task templates, skills, subagents, or SDK-driven jobs?
- Should project/page review be lazy and just-in-time, or should there be a
  second systematic review pass over the whole wiki?
- What metadata should be standardized in wiki YAML frontmatter before the
  corpus grows further?
- Should semantic tags remain lightweight conventions, or become parser-backed
  objects that tools can use?
- How should new Obsidian notes and future ChatGPT exports be incrementally
  triaged without redoing the whole synthesis pass?
- What should count as "done" for a page: source coverage, conceptual
  coherence, actionability, or project usefulness?

For now, keep deterministic tooling explicit and inspectable. Use agentic
synthesis and review as a controlled markdown-editing workflow with clear
source provenance and git commits.
