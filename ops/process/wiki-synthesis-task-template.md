# Wiki Synthesis Task Template

Use this template to start a new synthesis pass in a fresh agent context. The
agent should be able to complete the task without relying on any prior chat
session.

## Cold-Start Prompt

```text
You are working in the Weaver repository.

First read:
- AGENTS.md
- ops/process/wiki-synthesis-playbook.md
- ops/process/project-promotion-checklist.md
- ops/context/project-glossary.yaml
- ops/context/chatgpt-project-glossary.yaml
- ops/clusters/2026-06-24/source-inventory.qmd
- ops/clusters/2026-06-24/manifest.csv

Then perform the synthesis task below. Do not rely on previous session context.
Use repository files as the source of truth.
```

## Task Envelope

```text
Synthesis pass:
- Name:
- Date:
- Goal:

Primary target:
- Hub path:
- Page type:
- Status:

Source scope:
- Source inventory:
- Manifest:
- Source bundles:
- Required artifacts:
- Optional artifacts:
- Raw files to inspect only if needed:

Project and category context:
- Project glossary entries:
- ChatGPT project IDs:
- Boundary notes:

Expected output:
- Hub page:
- Child pages:
- Topic or method pages:
- Planning file updates:
- Index updates:

Constraints:
- Write distilled wiki prose, not a source summary.
- Keep hubs short and move reusable detail into child pages.
- Use YAML frontmatter from the playbook.
- Include compact `Source Map` sections.
- Prefer artifact links over raw links.
- Use raw transcripts or copied notes only when artifact wrappers are too thin.
- Preserve open questions separately from conclusions.
- Cross-link project pages and reusable method pages.
- Do not import skipped or sensitive material.
- Do not add LLM calls, vector indexes, databases, or automatic synthesis code.
- If the task promotes a concept or child page to a top-level project, follow
  `ops/process/project-promotion-checklist.md`.

Checks before completion:
- Run `git diff --check`.
- Run the wiki link checker.
- Run a trailing-whitespace scan for touched Markdown files.
- Report created and modified files.
- Commit only if explicitly requested.
```

## Fill-In Example

```text
Synthesis pass:
- Name: Genesis Hub Draft
- Date: 2026-06-27
- Goal: Create the first Genesis project hub and identify child pages for AI
  research, agentic tooling, and Weaver-as-system material.

Primary target:
- Hub path: wiki/projects/genesis.md
- Page type: project-hub
- Status: draft

Source scope:
- Source inventory: ops/clusters/2026-06-24/source-inventory.qmd
- Manifest: ops/clusters/2026-06-24/manifest.csv
- Source bundles:
  - genesis/ai
  - genesis/tech
  - genesis/math
  - unassigned/ai
- Required artifacts:
  - ops/artifacts/obsidian/genesis.md
  - ops/artifacts/chatgpt/6a379f1a-a974-83ec-901a-a9c6f958030c.md
- Optional artifacts:
  - ops/artifacts/chatgpt/index.md
- Raw files to inspect only if needed:
  - raw/chatgpt/transcripts/<conversation_id>.md

Project and category context:
- Project glossary entries:
  - genesis
- ChatGPT project IDs:
  - weaver-agentic-wiki-ai-ide
- Boundary notes:
  - Keep Genesis as building/agency/AI-adjacent project work.
  - Move reusable AI tooling methods into topic pages when they are not
    project-specific.

Expected output:
- Hub page: wiki/projects/genesis.md
- Child pages:
  - wiki/projects/genesis/agentic-tooling.md
- Related project pages:
  - wiki/projects/weaver.md
- Topic or method pages:
  - wiki/topics/ai-tools.md if the reusable material is large enough
- Planning file updates:
  - ops/synthesis/wiki-hub-todo.md
- Index updates:
  - wiki/index.md
```

## Agent Output Contract

The agent should finish with:

- a short summary of pages created or updated;
- any source bundles intentionally deferred;
- checks run and whether they passed;
- residual risks or open questions;
- commit hash, if a commit was requested.

Do not treat completion of the task as evidence that pages are `reviewed`.
Synthesis pages remain `status: draft` until a separate review pass checks
scope, source support, and omissions.
