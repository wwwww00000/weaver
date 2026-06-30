# Weaver Workflow Todo

This is the working queue for turning the reviewed Weaver hub and structured
context idea into small, testable workflow prototypes.

## Current Frame

Weaver is reviewed as a project hub, but the next stage should stay exploratory.
The goal is not to build a full retrieval system yet. The goal is to discover
which context, tagging, and write-back interactions actually help future
sessions start faster and preserve better state.

Use these references first:

- [Weaver hub](../../wiki/projects/weaver.md)
- [Structured Context As A Portable LLM Substrate](../../wiki/projects/genesis/structured-context-substrate.md)
- [Weaver status card](../status/projects/weaver.md)
- [Wiki Synthesis Playbook](../process/wiki-synthesis-playbook.md)

## Todo Queue

- [ ] Hold a design conversation on semantic tagging and retrieval before
  adding code.
  - Working note:
    [Weaver Structure And Retrieval Design Note](weaver-structure-and-retrieval.md)
  - Decide the first object vocabulary: likely `claim`, `decision`, `todo`,
    `question`, `affordance`, `invariant`, `failure_mode`, `source`, and
    `state_delta`.
  - Compare frontmatter, Markdown headings, HTML comments, XML-style inline
    tags, and sidecar files.
  - Decide whether retrieval should operate over pages, sections, status cards,
    source artifacts, or hand-built context packs.
  - Define what good retrieval means: fewer cold starts, fewer forgotten
    constraints, better provenance, and less memory pollution.

- [ ] Build one or two manual context-pack prototypes.
  - Use real tasks rather than abstract examples.
  - Start with a small fixture set:
    [Weaver hub](../../wiki/projects/weaver.md),
    [Structured Context](../../wiki/projects/genesis/structured-context-substrate.md),
    [Weaver status](../status/projects/weaver.md), and one process doc.
  - Manually assemble the context pack before implementing any generator.
  - Record what was useful, missing, noisy, or stale.

- [ ] Prototype a ChatGPT-like wiki-context session in a fresh Codex thread.
  - Start a new Codex conversation in this repo rather than continuing a long
    historical thread.
  - Load context from files, not from prior chat memory.
  - Opening prompt should ask for design only, not implementation.
  - Initial files to read:
    [Weaver hub](../../wiki/projects/weaver.md),
    [Structured Context](../../wiki/projects/genesis/structured-context-substrate.md),
    [Weaver status](../status/projects/weaver.md), and
    [Wiki Synthesis Playbook](../process/wiki-synthesis-playbook.md).

- [ ] Define the first session-close artifact.
  - It should propose durable updates rather than silently mutate memory.
  - Candidate sections: claims, decisions, todos, open questions, superseded
    claims, source links, and follow-up prompts.
  - Keep the first version as Markdown for review.

- [ ] Only after manual prototypes feel useful, consider a small Weaver command
  for context packs.
  - Possible shape: `weaver context pack --project weaver --task "..."`
  - Keep the output as plain Markdown or XML-flavored Markdown.
  - Do not add vector search, databases, or automatic write-back in this first
    pass.

- [ ] Defer Codex SDK work until the interaction shape is clear.
  - Use the SDK when a program needs to create or continue Codex threads,
    integrate Codex into another app, or automate a repeatable harness.
  - Do not start there for the first design exploration.

## Open Questions

- What is the minimum context-pack schema that is useful without becoming a
  brittle template?
- Which Weaver pages are mandatory context and which should be retrieved?
- Should semantic tags be visible authoring syntax, invisible comments, or
  sidecar metadata?
- How should a future retrieval system rank affordance matches against lexical
  matches?
- What does a good session-close review workflow look like in Neovim?
