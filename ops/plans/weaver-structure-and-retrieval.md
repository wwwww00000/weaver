# Weaver Structure And Retrieval Design Note

Status: working conversation note
Started: 2026-07-01

This note is the editable surface for thinking through semantic structure,
retrieval, context packs, and future Weaver interaction design.

The method is deliberately "cognitive code editing": instead of letting the
discussion disappear into a chat transcript, we will iteratively edit this
file, classify ideas, preserve tensions, and promote stable conclusions into
the Weaver wiki only after they survive review.

## Current Frame

We are circling a hard problem that looks like "how to solve RAG" in miniature.
The goal is not to solve all of retrieval immediately. The goal is to slow down
and discover which structure is worth introducing before retrieval automation
exists.

The current bias:

- structure comes first;
- retrieval depends on structure;
- write-back and review matter as much as retrieval;
- the first experiments should be manual and inspectable;
- markdown remains the durable editing surface.

## Dimensions

### Structure

Structure is the easier part to see, but it creates big upfront decisions. The
main question is not "can we tag everything?" It is which distinctions are
stable enough to carry across future sessions without creating annotation
burden.

Candidate structure layers:

- page-level metadata in YAML frontmatter;
- predictable Markdown section headings;
- stable IDs for high-value objects;
- inline semantic tags for selected fragments;
- generated or hand-built context packs;
- session-close state deltas;
- possible sidecar metadata later.

### Retrieval

Retrieval should come after we understand the useful units of structure. The
danger is trying to invent a general RAG system before knowing what a good
answer should load.

Important retrieval questions:

- What is the retrieval unit: page, section, status card, source artifact,
  decision, affordance, or context pack?
- Which context should be mandatory and deterministic?
- Which context should be searched or agent-selected?
- How do we avoid over-retrieval and memory pollution?
- How do we preserve provenance without making every answer source-noisy?
- How do we measure whether a retrieved item was actually useful?

## Visions

### Cognitive IDE

The cognitive IDE idea is a strong attractor. The desired feeling is not a
traditional note app and not an ordinary chat window. It is closer to editing a
knowledge base with an agent that can see structure, propose state changes,
retrieve relevant modules, and leave reviewable diffs.

Possible extension: expand this into a separate note focused only on the
cognitive IDE interface, workflows, and editing primitives.

Questions:

- What are the primitives of a cognitive IDE: buffer, selection, object,
  command, retrieval, context pack, state delta?
- What should feel like ordinary text editing, and what should feel like an
  agent command?
- How much of this can be prototyped inside Neovim before a custom UI exists?

### Affordance Cards

Affordance cards remain promising but underspecified. The key intuition is that
ordinary notes say what something is, while affordance cards say when something
wants to be used.

An affordance card might record:

- when to use an artifact;
- when not to use it;
- invariants to preserve;
- failure modes;
- examples;
- related tools or pages;
- expected outputs.

The hard part is retrieval. A useful system should retrieve an artifact because
its usage conditions match the task, not merely because words overlap.

## Object Vocabulary Candidates

Start with a small vocabulary. These should be operationally useful, not merely
ontologically pleasing.

### Likely First Objects

- `decision`: accepted choice that should shape future work.
- `open_question`: unresolved issue worth preserving.
- `todo`: actionable next step.
- `invariant`: rule future agents should preserve.
- `affordance`: when a page, process, tool, or artifact wants to be used.
- `source`: provenance pointer.
- `state_delta`: proposed durable update after a session.

### Maybe Later

- `claim`: a knowledge assertion that may need evidence, confidence, or later
  reconciliation.
- `failure_mode`: recurring way a workflow or tool can go wrong.
- `example`: concrete demonstration of a concept or process.
- `episode`: compressed record of a session or work branch.
- `module`: durable concept, method, project, or procedure page.

Reason to defer `claim`: decisions, invariants, and open questions are more
directly useful for agent behavior. Claim extraction can become expensive and
argumentative before we know how it helps retrieval.

## Structural Carriers

### YAML Frontmatter

Best for page-level routing:

- project;
- status;
- page type;
- categories;
- source bundles;
- related pages;
- update dates.

Strengths:

- already used in the wiki;
- easy to parse;
- compatible with Obsidian-like tooling;
- low visual noise.

Limits:

- too coarse for decisions, questions, claims, and affordances inside a page.

### Markdown Sections

Best first choice for durable page-internal structure.

Candidate headings:

- `## Decisions`
- `## Open Questions`
- `## Invariants`
- `## Affordances`
- `## Failure Modes`
- `## Sources`
- `## Next Actions`

Strengths:

- human-readable;
- easy to edit in Neovim;
- easy enough to parse later;
- does not make pages look like machine output.

Limits:

- weak stable identity unless we add IDs;
- can drift if headings are informal.

### Invisible HTML Comments

Best for stable IDs on high-value objects.

Example:

```md
<!-- weaver:decision id="markdown-first-state" -->
- Keep markdown and git as the durable state layer.
```

Strengths:

- parseable;
- low rendered noise;
- can give stable handles to decisions, invariants, and questions.

Limits:

- editing gets fiddlier;
- overuse will make notes feel mechanically burdened.

### Visible XML-Style Tags

Best for generated context packs or session-close artifacts, not ordinary wiki
prose.

Example:

```xml
<decision id="start-with-manual-context-packs">
Start manually before building retrieval automation.
</decision>
```

Strengths:

- model-readable;
- clear typed boundaries;
- useful for context-pack serialization.

Limits:

- awkward inside normal Markdown notes;
- can make human writing feel artificial.

### Sidecar Metadata

Best later, if structure becomes too detailed for prose files.

Possible shape:

```text
wiki/projects/weaver.md
wiki/projects/weaver.meta.yaml
```

Strengths:

- keeps prose clean;
- allows stricter schemas.

Limits:

- synchronization burden;
- harder to review casually;
- worse for simple git-based reading.

## Retrieval Options

### Manual Context Packs

First step. Manually assemble the context a future session should load for a
real task.

Why:

- fastest way to learn what matters;
- no premature retrieval infrastructure;
- exposes missing object types and noisy context.

### Lexical Search

Use `rg`, headings, tags, frontmatter, and filenames.

Why:

- transparent;
- cheap;
- provenance-preserving;
- good baseline.

Limits:

- misses semantic matches;
- does not understand affordances.

### QMD Or SQLite FTS

Index pages and sections into searchable records.

Why:

- still local and inspectable;
- can search headings, projects, categories, and body text;
- can remain deterministic.

Limits:

- more tooling;
- requires deciding indexing units.

### Affordance-Based Retrieval

Retrieve artifacts based on when they want to be used.

Why:

- closer to actual agent usefulness than text similarity;
- can encode "use this process doc when the task is a synthesis pass."

Limits:

- requires authored affordance metadata;
- ranking is not obvious;
- may need manual examples before automation.

### Embeddings Or Vector Search

Defer.

Why:

- semantic recall may eventually help.

Reason to defer:

- opaque ranking;
- easy to over-retrieve;
- adds dependency and policy questions before we know the right units.

## First Manual Prototype Candidate

Task:

```text
Design the first Weaver context-pack and session-close workflow.
```

Manual context pack should include:

- task frame;
- mandatory context files;
- relevant decisions;
- invariants;
- open questions;
- affordances;
- source links;
- explicit non-goals.

Candidate source files:

- [Weaver hub](../../wiki/projects/weaver.md)
- [Structured Context As A Portable LLM Substrate](../../wiki/projects/genesis/structured-context-substrate.md)
- [Weaver status card](../status/projects/weaver.md)
- [Wiki Synthesis Playbook](../process/wiki-synthesis-playbook.md)
- [Weaver workflow plan](weaver-workflow-todo.md)

## Evaluation Criteria

A structure/retrieval experiment is useful if it:

- reduces cold-start friction;
- preserves decisions and constraints;
- avoids loading too much stale or generic context;
- makes source support auditable;
- produces better session-close updates;
- helps future agents preserve invariants;
- stays editable as ordinary Markdown.

## Tensions

- Structure helps retrieval, but too much structure makes writing unpleasant.
- Inline tags are powerful, but can pollute prose.
- Context packs should be model-readable, but the source of truth should remain
  human-readable.
- Affordance cards are appealing, but their retrieval semantics are still
  unclear.
- Retrieval is tempting, but write-back and memory hygiene may be the harder
  problems.

## Open Questions

- What is the minimum context-pack schema that feels useful?
- Which object types deserve stable IDs now?
- Should stable IDs live in comments, headings, or explicit bullet labels?
- Should affordance cards be sections inside pages or separate pages?
- Can a manual context pack reveal enough structure to avoid premature tooling?
- What does "retrieval success" mean for Weaver besides "the answer sounded
  good"?

## Next Edits

- Add user's additional intuitions and objections.
- Create one hand-built context pack in this file or a sibling file.
- Decide whether the cognitive IDE deserves its own planning note.
- Decide whether affordance cards should be prototyped as page sections or
  standalone cards.
