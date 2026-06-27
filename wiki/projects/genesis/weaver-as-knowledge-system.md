---
title: Weaver As A Knowledge System
status: draft
page_type: concept
projects:
  - genesis
categories:
  - ai
  - knowledge-management
  - notes
  - agentic-workflows
source_bundles:
  - genesis/personal
  - genesis/tech
  - unassigned/ai
  - unassigned/cognitive
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/genesis
related:
  - projects/genesis
  - projects/genesis/agentic-tooling
created: 2026-06-28
updated: 2026-06-28
---

# Weaver As A Knowledge System

Weaver is the Genesis subproject for turning messy personal knowledge sources
into a maintained, compiled wiki.

The central problem is not raw storage. Obsidian notes, weekly notes, idea
dumps, project todos, and ChatGPT conversations already store plenty of text.
The failure mode is that capture and reference collapse into the same space:
conversation streams remain too sequential, daily notes accumulate low-signal
state, and durable ideas are not promoted into pages that future agents or
humans can reliably reload.

## Working Model

Weaver should be a layered system:

- Raw sources are copied and kept auditable.
- Triage artifacts record human import decisions with stable source IDs.
- Intermediate artifacts point back to copied notes or transcripts.
- The compiled wiki holds project hubs, concept pages, method pages, open
  questions, and source maps.
- Process docs and task templates make future synthesis repeatable.

The important design constraint is that markdown remains the durable source of
truth. Python code should produce manifests, triage documents, validation
reports, task envelopes, and other explicit artifacts. It should not hide the
knowledge state in a database or vector index before the markdown workflow has
proven itself.

## Context Compiler

The long-term Weaver idea is a context compiler rather than a bigger chat
transcript.

A task should begin from a deliberately assembled working set: current goal,
pinned constraints, relevant project pages, retrieved modules, summaries of
prior episodes, and reloadable pointers to source artifacts. The agent can ask
for more material, but the system should not treat every prior token as equally
important context.

Useful memory object types:

- `frame`: current task, scope, inputs, constraints, and status;
- `module`: durable concept, method, project, or procedure page;
- `summary`: compressed episode or source bundle;
- `decision`: accepted design choice with source support;
- `open_question`: unresolved issue worth preserving;
- `artifact`: generated output, report, copied source, or manifest;
- `index`: navigational page that decides what to load next.

This makes compaction a promotion problem. Raw traces can be summarized into
episodes, episodes can promote durable findings into modules, and modules can
roll up into hubs. The point is not to preserve every interaction; it is to
preserve the information that should shape future work.

## Current V0

The current implementation is deliberately narrower:

- deterministic triage for Obsidian and ChatGPT sources;
- applied artifacts with source IDs and copied raw references;
- source inventory and clustering outputs for synthesis queues;
- a wiki synthesis playbook and task template;
- human-directed agent synthesis into draft wiki pages.

That is enough to test the first claim: a compiled wiki with explicit source
maps should be more useful than raw vault search or rereading old ChatGPT
threads.

## Synthesis Role

Weaver pages should not read like source summaries. The source wrappers and raw
transcripts remain available for audit. The wiki layer should distill:

- stable project definitions;
- durable methods and ideas;
- current hypotheses;
- unresolved questions;
- links between projects and reusable concepts.

When the agent is involved, its work should appear as git diffs against markdown
files, not as hidden state. Task templates and playbooks are part of the system
because they keep the synthesis behavior repeatable across future sessions and
delegated agents.

## Open Questions

- What is the first concrete context-compiler prototype: QMD-backed retrieval,
  explicit task frames, or an agent tool for module loading?
- How should modules advertise when they are relevant to a task?
- Which information should be pinned deterministically, and which should be
  retrieved through agent judgment?
- How do we measure compaction mistakes, such as forgotten constraints or
  summaries that omit details later needed for synthesis?

## Source Map

- [LLM Wiki Project Planning](../../../ops/artifacts/chatgpt/6a379f1a-a974-83ec-901a-a9c6f958030c.md)
- [weaver note](../../../ops/artifacts/obsidian/weaver.md)
- [genesis overview](../../../ops/artifacts/obsidian/genesis.md)
- [Context Management in LLMs](../../../ops/artifacts/chatgpt/69acf566-8c94-839f-9dc5-9e4931ab63ba.md)
- [LLM Note-taking Tools](../../../ops/artifacts/chatgpt/67e29c1d-88f4-8009-b717-e92513a6543e.md)
- [source inventory](../../../ops/clusters/2026-06-24/source-inventory.qmd)
