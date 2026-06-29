---
title: Weaver
status: reviewed
page_type: project-hub
projects:
  - weaver
categories:
  - ai
  - knowledge-management
  - notes
  - agentic-workflows
source_bundles:
  - genesis/personal
  - genesis/tech
  - weaver/context-management
  - weaver/structured-memory
  - weaver/foundation
  - unassigned/ai
  - unassigned/cognitive
source_inventory: ops/clusters/2026-06-29/source-inventory.qmd
related:
  - projects/genesis
  - projects/genesis/structured-context-substrate
  - projects/foundation
  - projects/genesis/agentic-tooling
  - projects/whetstone/think-tags-and-metacognition
created: 2026-06-28
updated: 2026-06-29
---

# Weaver

Weaver is the top-level project for turning messy personal knowledge sources
into a maintained, compiled wiki and eventually a context compiler for future
human-agent work.

It started inside Genesis because it is also a buildable AI-adjacent system.
It is now a peer project: Genesis owns the broader building, agency, AI
research, and agentic tooling frame; Weaver owns the knowledge workflow,
compiled-memory model, source provenance, wiki synthesis process, and future
context-loading machinery.

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

## Compiled Modules, Not Conversations

The core interaction should eventually feel less like chatting into a transcript
and more like editing a knowledge base with an agent.

A conversation is useful as an ephemeral work surface, but it is a poor durable
object. It is sequential, noisy, and optimized for immediate back-and-forth
rather than future loading. Weaver should instead preserve a hierarchy of
description levels:

- raw trace: tool outputs, failed attempts, chat fragments, and local
  exploration;
- episode summary: what happened in one session or branch;
- module: reusable concept, procedure, decision, invariant, or open question;
- index: curated map that tells future humans and agents what to load.

Compaction is therefore not just shortening text. It is promotion. A session can
leave behind an episode summary plus pointers to raw evidence. Stable pieces can
be promoted into modules. Modules can be linked from project indexes, process
docs, or task templates. The raw transcript remains auditable, but the active
context should be compiled from the higher layers first.

This is the main difference between Weaver and an append-only chat log. The
question is not "what happened before?" but "which durable modules should shape
the next task?"

## Module Retrieval And Packing

Module retrieval should be agent-assisted, but not purely agent-decided.

The deterministic compiler should always include mandatory context:

- the current task frame;
- pinned constraints;
- project glossary entries;
- relevant process docs;
- recent decisions and open questions;
- any user-specified source artifacts.

The agent can then use retrieval tools to request additional modules by query,
link neighborhood, project, category, or source bundle. A QMD-style local search
backend is a plausible substrate because it can search markdown notes and expose
candidate modules without hiding provenance. Search alone is not the memory
policy, though. The compiler still decides what fits in the working set and what
stays as a reloadable pointer.

Useful memory operations:

```text
search_modules(query, scope, k)
open_module(id)
pin_module(id)
create_module(type, title, body, links)
update_module(id, patch)
push_frame(title, goal, inputs)
compact_frame(id)
archive_trace(frame_id)
reload_pointer(id)
link_modules(a, b)
```

The model should feel like it is manipulating a small context operating system,
not rummaging through a folder. But the operating system must remain visible in
markdown and git.

[Structured Context As A Portable LLM Substrate](genesis/structured-context-substrate.md)
is the sharper research thread for this idea. Weaver should treat it as a
design reference for context packs, session-close state deltas, affordance
cards, and memory hygiene, while keeping the first implementation grounded in
this repo's markdown artifacts.

## Semantic Notes As Interface

The semantic-notetaking source suggests a useful bridge between freeform
Chronicle-style pages and Weaver-style compilation: inline tags that mark
sentences or paragraphs without forcing the whole note into a rigid template.

Examples:

- `<idea>`: candidate seed;
- `<question>`: unresolved inquiry;
- `<next>`: smallest actionable step;
- `<experiment>`: thing to try and observe;
- `<tension>`: affective or conceptual knot;
- `<seed>`: capture only;
- `<develop>`: expand this now or during review.

These tags are not only labels. They are extraction handles. A morning page,
work note, or handwritten page can remain mostly stream of consciousness while
tagged fragments become easier to skim, lift into atomic notes, convert into
projects, or hand to an agent as structured context.

The strongest version is a semantic macro: a tag implies a next operation.

- `<distill>` produces a short summary.
- `<fork>` produces options and chooses one.
- `<prove>` asks for evidence, counterexample, or test.
- `<resolve>` produces a decision rule or next action.

This turns notation into a light interface for cognition and later tooling.
Weaver should preserve the markdown-first form, but the tags can eventually
become parser-friendly affordances for search, extraction, and agent commands.

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

The next implementable slice should still be small: a context compiler over one
project folder, using typed markdown notes, explicit task frames, QMD-style
retrieval, and selective write-back of summaries, decisions, modules, and open
questions. Code execution, subagents, and custom UI can wait until the memory
semantics are proven.

## Weekly And Editor Workflow Trial

The stale "projects overview" section in weekly notes is a signal that project
state should not be maintained by copy-pasting week to week. Project hubs and
status cards should own that state instead. Weekly notes can shrink toward
dated deltas, review prompts, and promotion queues that point back to current
project cards.

There is also growing momentum toward reducing or dropping Obsidian usage.
Most ordinary note and wiki work may be viable inside Neovim with markdown
rendering, repo-local search, git diffs, and lightweight project/status files.
`render-markdown.nvim` is a plausible rendering layer, with additional plugins
or small Weaver tools filling in navigation and review operations.

The main Obsidian feature still in active use is the periodic-notes calendar
view. Before replacing Obsidian, run the current Weaver workflow for a few
weeks and then review what remains missing: calendar navigation, weekly note
creation, backlinks, search, task capture, mobile capture, or visual browsing.

## Possible Tool Surface

The Weaver source note points beyond static compilation toward a headless or
TUI-friendly knowledge work surface:

- open and edit notes from a command-driven interface;
- route ChatGPT or agent outputs directly into note buffers;
- expose semantic tags, sentence ranges, and sections as addressable objects;
- use QMD-style search or summaries for retrieval without hiding provenance;
- connect notebook or Jupyter-like kernels when plots and experiments matter;
- promote repeated flows into typed commands rather than one-off chats.

This overlaps with Genesis because it is a buildable interface project. The
Weaver-specific requirement is that the interface be shaped by the markdown
knowledge model, not bolted on after the fact.

## Relationship To Genesis

In an AI-saturated workflow, raw generation and competent execution get cheaper.
Genesis still needs human taste and agency, while Weaver should make that taste
and agency easier to preserve across time.

Weaver can support taste by preserving comparative judgment: best examples,
why they work, what felt generic, and which principles survived review. It can
support agency by turning ambient ideas into small shipped artifacts, visible
decision logs, and reviewable next actions.

The knowledge system should therefore not only answer "what did I think?" It
should also answer:

- what did I choose to pursue;
- why did it seem worth pursuing;
- what artifact did it become;
- what feedback changed the direction;
- what should be copied, rejected, or deviated from next time.

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
- What minimum context-pack schema should be dogfooded on Genesis and Weaver
  sessions?
- Should semantic tags remain a human notation convention first, or become a
  parser-backed command surface?
- What are the exact promotion rules from raw trace to episode summary to
  module to index?
- Which context items must be loaded deterministically, and which should be
  agent-selected through retrieval?
- How should modules advertise when they are relevant to a task?
- Which information should be pinned deterministically, and which should be
  retrieved through agent judgment?
- How do we measure compaction mistakes, such as forgotten constraints or
  summaries that omit details later needed for synthesis?

## Source Map

- [LLM Wiki Project Planning](../../ops/artifacts/chatgpt/6a379f1a-a974-83ec-901a-a9c6f958030c.md)
- [Semantic Notetaking Systems](../../ops/artifacts/chatgpt/6985b8d3-8a14-839c-aa84-7f617c78ad3e.md)
- [weaver note](../../ops/artifacts/obsidian/weaver.md)
- [Taste and agency in AI](../../ops/artifacts/chatgpt/689b6e60-1688-8322-95a3-6848c2ab85c5.md)
- [genesis overview](../../ops/artifacts/obsidian/genesis.md)
- [Context Management in LLMs](../../ops/artifacts/chatgpt/69acf566-8c94-839f-9dc5-9e4931ab63ba.md)
- [LLM Note-taking Tools](../../ops/artifacts/chatgpt/67e29c1d-88f4-8009-b717-e92513a6543e.md)
- [Structured Context inbox note](../../ops/artifacts/notes/structured-context.md)
- [LLM Coding Workflows](../../ops/artifacts/chatgpt/6a31f45a-f0e0-83ec-8a47-08c0e09e206c.md)
- [source inventory](../../ops/clusters/2026-06-29/source-inventory.qmd)
