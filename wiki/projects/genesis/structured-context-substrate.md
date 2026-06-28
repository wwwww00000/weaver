---
title: Structured Context As A Portable LLM Substrate
status: draft
page_type: research-thread
projects:
  - genesis
  - weaver
categories:
  - ai
  - context-management
  - agentic-workflows
  - knowledge-management
source_bundles:
  - genesis/context-management
  - genesis/agent-harnesses
  - genesis/structured-memory
  - weaver/context-management
  - weaver/structured-memory
source_inventory: ops/clusters/2026-06-29/source-inventory.qmd
parent: projects/genesis
related:
  - projects/genesis/agentic-tooling
  - projects/genesis/reasoning-models-and-tool-use
  - projects/weaver
created: 2026-06-29
updated: 2026-06-29
---

# Structured Context As A Portable LLM Substrate

The structured-context thread asks whether LLM workflows should treat chat
transcripts as event logs while keeping durable project state in portable,
inspectable artifacts: claims, decisions, todos, affordance cards, code notes,
experiment summaries, and task-specific context packs.

The practical problem is cold-start friction. Useful state is scattered across
long chats, generated summaries, memory features, and local files. A better
workflow would let ChatGPT, Codex, Claude Code, local models, and future agent
harnesses all load the same structured state through a textual interface.

## Core Thesis

Text should remain the universal serialization layer, but not necessarily the
conceptual layer. The durable state should be typed, inspectable, and
rewritable:

```text
chat transcript = event log
markdown/code/artifacts = durable state
semantic tags = portable structure
QMD-like search = retrieval substrate
graph overlay = relationship substrate
affordance cards = usage-attraction layer
controller = context routing and memory hygiene
LLM = reasoning and generation engine
```

This keeps the system provider-agnostic. The artifacts stay in markdown and
git, while each model or harness receives a rendered context pack appropriate
to the task.

## Context Packs

A context pack is a task-specific mounted working set. Instead of starting a
session from a blank prompt or a pasted history, a command such as:

```bash
ctx open --project genesis --task "think about structured context and affordance fields"
```

would assemble the relevant current focus, decisions, claims, affordances, open
questions, source pointers, and known constraints. The output can be XML,
Markdown, YAML, or a hybrid, as long as it is readable by both humans and
models.

The goal is not to hide state behind an opaque agent. The goal is to give the
session the right state at the right abstraction level, with enough pointers to
reload details when needed.

## Session Close And State Deltas

The matching operation is session close:

```bash
ctx close --project genesis transcript.md
```

Close should propose durable updates rather than silently mutate memory:

- new claims worth keeping;
- decisions made during the session;
- todos that should survive;
- open questions;
- superseded claims;
- affordance updates;
- handoff summaries.

The proposed state delta should be human-reviewed. Memory hygiene is central:
not every fluent thought deserves promotion into durable project state.

## Affordance Cards

Affordance cards describe when an artifact wants to be used. Ordinary
documentation says what something is; an affordance card says when it should be
loaded, when it should be avoided, what invariants it preserves, and how it can
fail.

For code, an affordance card can sit beside a module and record:

- when to use the module;
- when not to use it;
- invariants the caller should preserve;
- common failure modes;
- example commands;
- design rationale that should shape future edits.

The retrieval goal is not only lexical similarity. A context compiler should
retrieve artifacts whose usage conditions match the current task.

## Relationship To Weaver

Weaver is the immediate dogfood substrate. Its triage, artifacts, wiki pages,
status cards, and synthesis playbooks already demonstrate the preferred shape:
durable markdown state, explicit provenance, git diffs, and reviewable
promotion from raw trace into modules.

Structured context extends Weaver from wiki compilation toward live context
compilation. A future Weaver context compiler could use typed project pages,
status cards, source maps, process docs, and affordance cards to assemble
task-specific packs for agents.

## Relationship To Genesis

Genesis owns the broader build and AI-systems question. Structured context is a
Genesis research/build thread because it touches agent harnesses, recursive
context access, controller policies, retrieval routing, and possibly future
model/runtime primitives.

The near-term version should remain high-level and textual. Lower-level ideas
such as memory tokens, context-operation vocabularies, pointer tokens, and
activation-level retrieval should be treated as north-star speculation until a
sidecar workflow proves which primitives are actually useful.

## Evaluation Shape

Do not start with an abstract benchmark. Start with dogfooding:

- can `ctx open` reduce cold starts in Weaver and Genesis sessions;
- can affordance cards help an agent choose the right module or process doc;
- does session close preserve decisions without polluting memory;
- does retrieval show restraint instead of mounting every vaguely related
  artifact;
- do future edits preserve invariants more reliably when affordance cards are
  present.

Small fixture tasks can measure retrieval precision, affordance activation,
invariant preservation, handoff usefulness, duplication avoidance, and memory
hygiene.

## Open Questions

- What is the smallest useful semantic tag vocabulary?
- Should XML tags, Markdown sections, or YAML frontmatter be the primary
  structure?
- How much should the system write automatically versus propose for review?
- How should uncertainty, provenance, and superseded claims be represented?
- When does a graph overlay provide value beyond typed markdown search?
- What would make this useful enough to integrate into the actual Weaver
  harness?

## Source Map

- [Structured Context inbox note](../../../ops/artifacts/notes/structured-context.md)
- [source inventory](../../../ops/clusters/2026-06-29/source-inventory.qmd)
