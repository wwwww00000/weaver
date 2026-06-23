# Weaver State And Next Steps

Date: 2026-06-21

This note supersedes the initial `HANDOFF.md` as the current working state for
the Weaver repo.

## Current State

Weaver is a git-backed personal knowledge tooling repo. The near-term goal is to
turn existing knowledge sources into explicit, reviewable intermediate artifacts
before any synthesis into a wiki.

Implemented so far:

- Python package `weaver` initialized with `uv`.
- Typer CLI exposed as `weaver`.
- `weaver triage obsidian` scans the default Obsidian vault at
  `/mnt/c/Users/limwe/Documents/obsidian`.
- Default Obsidian scanning ignores `.obsidian/`, `.trash/`, `.git/`,
  `node_modules/`, `assets/`, `attachments/`, `daily/`, and `weekly/`.
- Obsidian triage renders editable Markdown with decisions, comments, and
  category labels.
- YAML frontmatter tags and Obsidian inline tags are extracted.
- Completed initial Obsidian triage snapshot committed at
  `ops/triage/snapshots/obsidian-triage-2026-06-21-initial.md`.
- `weaver triage apply` parses completed triage docs, validates exactly one
  checked decision per item, copies selected source notes, and creates
  intermediate artifacts.

Generated local artifacts from the first Obsidian pass:

- Live triage document: `ops/triage/obsidian.md`
- Manifest: `ops/manifests/obsidian.csv`
- Copied selected notes: `raw/obsidian/`
- Intermediate artifacts: `ops/artifacts/obsidian/`
- Artifact index: `ops/artifacts/obsidian/index.md`

The first apply pass selected 116 of 151 Obsidian notes:

- `include`: 77
- `extract-insights`: 39
- skipped, deferred, or excluded: 35

The most recent weekly context note, `weekly/2026-W25.md`, was manually added to
the generated Obsidian source/artifact set because it contains current project
context that was intentionally excluded from bulk triage.

## Project Context

Project names and descriptions are captured in:

- `ops/context/projects.md`
- `ops/context/project-glossary.yaml`
- `ops/context/chatgpt-project-glossary.yaml`

Project names are a separate axis from category labels. Downstream synthesis
should infer project identity from file paths, titles, links, explicit comments,
ChatGPT project IDs, and the project glossaries. Category labels should remain
topical or conceptual.

Important project code names:

- `obelisk`: old crypto trading project; archive-mode.
- `p12n`: active crypto trading project with a machine learning focus.
- `accretion`: personal finance and wealth accumulation.
- `whetstone`: cognition improvement.
- `chronicle`: morning pages, journaling, creative writing, mindfulness, and meditation.
- `conjuration`: imagination building, creativity, and drawing.
- `revelation`: math and physics learning.
- `genesis`: building things, exercising agency, AI-adjacent work, and AI research.

## ChatGPT Triage Next

The ChatGPT export is available. Stage the extracted export locally under:

```text
raw/exports/chatgpt/2026-06-23/
```

This path is ignored by git because `raw/` may contain private source material.

Implemented deterministic ChatGPT triage:

```bash
weaver triage chatgpt /path/to/export.zip --out ops/triage/chatgpt.md
```

The command should accept:

- an export ZIP,
- an extracted export directory,
- or a direct `conversations.json`.

The triage output should use the same decision model as Obsidian and should
produce a manifest. After manual review, `weaver triage apply-chatgpt` handles
ChatGPT triage artifacts under `raw/chatgpt/` and `ops/artifacts/chatgpt/`.

## Synthesis Direction

After ChatGPT triage and apply, the next stage should consume both artifact sets:

- `ops/artifacts/obsidian/`
- `ops/artifacts/chatgpt/`

The path of least resistance is to let Codex perform the first synthesis pass,
possibly with subagents, using explicit task envelopes generated from the
artifact indexes. This keeps the workflow coupled to the coding-agent layer for
now, but avoids prematurely building an API-backed orchestration system.

The synthesis pass should be intelligent rather than a mechanical import:

- combine overlapping artifacts,
- rewrite rough notes into durable wiki pages,
- recategorize sparse or noisy labels,
- infer project labels where useful,
- preserve source links back to raw copied notes and conversation artifacts,
- avoid importing sensitive or skipped material,
- distinguish project pages from category pages,
- create cross-links when a note is both project-specific and conceptually reusable.

Recommended first synthesis target:

1. Generate a synthesis plan from artifact indexes and project glossary.
2. Group artifacts into candidate project clusters and category clusters.
3. Produce draft wiki pages under `wiki/drafts/`.
4. Keep provenance blocks linking back to artifacts and copied sources.
5. Review drafts before promoting anything to stable `wiki/` pages.

## Open Design Questions

- Whether synthesis should be primarily Codex-driven, `codex exec` task-envelope
  driven, or API-driven.
- Whether to make project inference deterministic before synthesis, or leave it
  to the intelligent synthesis pass.
- Whether category pages should be generated first, project pages first, or both
  in parallel.
- How aggressively to rewrite personal notes versus preserving source phrasing.

For now, keep deterministic tooling explicit and inspectable. Use agentic
synthesis only after the source artifacts are clear and reviewable.
