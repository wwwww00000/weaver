# Foundation

Status: idea / parked
Area: LLM-aided learning, textbook ingestion, personal knowledge systems
Related projects: Revelation, Weaver, Genesis
Initial parser choice: Docling

## Summary

Foundation is a proposed project for turning math and physics textbooks into structured, source-linked learning environments. It is Revelation-adjacent, but should be its own project: Revelation is the study project itself, while Foundation is the software substrate that makes long-running self-study easier to resume, navigate, and deepen.

The initial use case is personal undergraduate-to-early-graduate-level self-study in mathematics and physics. The system should ingest textbook PDFs, parse them into a durable intermediate representation, tag their conceptual structure, and support LLM-aided interactions such as “jump to definition,” “explain this derivation gap,” “resume where I left off,” and “show me related explanations across multiple texts.”

The long-term vision is not merely “chat with a PDF.” The goal is a stateful learning system that preserves context across study sessions, links concepts across books, remembers confusions and progress, and acts as a source-grounded tutor.

## Motivation

My current mode of casual amateur study suffers from cold restarts. I can make progress through a textbook, but when I return after days or weeks, I often lose the local context: what I had understood, what confused me, what I intended to review, and why the current section mattered.

LLMs could help with this, but only if the system keeps durable state. Ordinary chat sessions are too transient, and ordinary PDF readers do not understand concepts, dependencies, or personal study history. Foundation should bridge that gap.

The core motivation is to make studying technical subjects feel less like repeatedly restarting from a cold PDF and more like continuing an accumulating intellectual journey.

## Initial Scope

Foundation should start with math and physics textbooks, especially quantum mechanics and related mathematical background. The first technical target should be a single textbook chapter, parsed and tagged well enough to support a small number of useful interactions.

The initial parser should be Docling. Other PDF parsing tools may be compared later, but the first pass should avoid spending too much time on parser evaluation. The system should be designed so that Docling output is normalized into our own schema rather than becoming the permanent internal format.

## Core Idea

A textbook PDF should be transformed into a structured intermediate representation:

```text
PDF
  -> parsed pages and blocks
  -> normalized document IR
  -> section outline
  -> block-level tags
  -> concept tags
  -> relation graph
  -> reviewable human steering artifacts
  -> searchable source-linked learning environment
```

The system should preserve provenance throughout. Every tag, concept, summary, and explanation should be linked back to a page, section, block, or equation.

This provenance requirement is important. For math and physics study, a hallucinated concept map is much less useful than a modest, incomplete map with reliable anchors into the source text.

## Document Representation

The normalized IR should include at least:

```text
Document
  metadata:
    title
    author
    edition
    source_path
    file_hash
    parser_version

  pages:
    page_id
    page_number
    rendered_image_path
    raw_text
    blocks

  sections:
    section_id
    title
    section_path
    page_range
    block_ids

  blocks:
    block_id
    page_number
    section_id
    block_type
    text
    markdown
    bbox
    source_parser
    parse_confidence

  tags:
    block_id
    tag_type
    tag_value
    evidence_span
    status: proposed / accepted / rejected / edited

  concepts:
    concept_id
    canonical_name
    aliases
    first_seen
    definitions
    related_blocks

  relations:
    source_id
    relation_type
    target_id
    evidence
```

The first implementation can use JSONL files and SQLite. Fancy graph databases should not be necessary at the beginning.

## Tag Ontology

The initial tag ontology should support math/physics learning rather than generic document search.

Block-level tags:

```text
definition
theorem
lemma
postulate
proof
derivation
worked_example
exercise
notation_setup
physical_interpretation
mathematical_interpretation
motivation
warning
common_confusion
summary
historical_note
```

Physics-specific tags:

```text
limiting_case
classical_limit
symmetry_argument
conservation_law
measurement_interpretation
approximation
idealization
dimensional_analysis
experimental_connection
```

Personal learning tags:

```text
core
optional
advanced
confusing
reread
prerequisite_gap
good_for_flashcard
good_for_concept_map
exercise_recommended
```

Relation tags:

```text
introduces
uses
depends_on
motivates
contrasts_with
generalizes
special_case_of
derives
example_of
applies_to
```

The tag ontology should remain editable. The system should learn from user corrections rather than assume that the first proposed ontology is final.

## Human-in-the-Loop Steering

The first useful version should be interactive. Instead of silently building a concept graph, Foundation should generate a review artifact for each chapter or section.

Example review item:

```markdown
## Page 87 — Section 3.2 Operators

> An observable is represented by a Hermitian operator...

Suggested tags:
- block_type: definition
- concepts: observable, Hermitian operator, eigenvalue
- relations:
  - introduces: observable
  - depends_on: linear operator
  - depends_on: inner product

Actions:
- [ ] accept
- [ ] reject
- [ ] mark as confusing
- [ ] add to flashcards
- [ ] link to previous note: 
- [ ] rename concept: Hermitian operator -> self-adjoint operator
```

This review flow is important because the ideal interaction is not obvious yet. The project should discover the right UX by letting me steer the tags, concepts, and learning state manually at first.

## Key Interactions to Enable

### Resume Study State

The system should make it easy to continue after time away.

Example:

```text
You last studied Shankar Section 3.2.

You understood:
- observables as operators
- the motivation for Hermitian operators

You were confused by:
- why Hermitian operators have real eigenvalues
- how the adjoint is being used in the derivation

Suggested next action:
- review the adjoint definition
- work through the finite-dimensional matrix example
- then continue to the spectral decomposition discussion
```

### Jump to Definition

While reading a passage, I should be able to jump to:

```text
first definition
formal definition
informal explanation
worked example
prior use
future use
same concept in another textbook
```

This should work across multiple books, not only within one PDF.

### Derivation Gap Debugger

The system should help with moments where a textbook omits too many intermediate steps.

Example queries:

```text
How does line 3 follow from line 2?
What theorem is being used here?
Expand the algebraic steps.
Show the finite-dimensional matrix version.
Show the same argument in Dirac notation.
What prerequisite am I missing?
```

The answer should be source-grounded and should identify the hidden move rather than merely paraphrase the passage.

### Cross-Text Triangulation

The system should connect explanations across several texts.

Example:

```text
Find another textbook that explains this idea more slowly.
Compare Shankar and Hall on observables.
Show the intuitive explanation before the rigorous one.
Show the rigorous version after the physics version.
```

This is one of the key benefits of turning several PDFs into a shared concept-indexed library.

### Confusion Ledger

Confusions should be first-class objects.

```text
confusion_id
source passage
question asked
suspected prerequisite
status: open / partially resolved / resolved
resolution note
related concepts
date first encountered
date last reviewed
```

Useful interactions:

```text
Show my open confusions in quantum mechanics.
Which confusions block the most future material?
Turn this confusion into a review card.
Explain this again using a different route.
```

### Personal Prerequisite Graph

Foundation should eventually model not just the textbook’s concept graph but my personal learning frontier.

It should know which concepts are:

```text
known
seen but shaky
currently blocking progress
upcoming
safe to ignore for now
```

This enables explanations like:

```text
Explain this using only finite-dimensional linear algebra.
Do not use measure theory.
Use the matrix version first, then the Hilbert space version.
```

### Study Session Memory

Each session should produce a durable learning trace.

```text
Session: 2026-06-29
Topic: Hermitian operators and observables
Sources:
- Shankar Ch. 3
- Hall Ch. 2

Progress:
- Read Shankar 3.1–3.2
- Resolved confusion about Hermitian matrices having real eigenvalues
- Marked spectral theorem as a prerequisite gap
- Created two review prompts
- Next action: attempt exercise on commutators
```

This is the mechanism that kills cold restarts.

## MVP

The first MVP should be deliberately small.

Target:

```text
One chapter of one textbook
Docling parse
normalized block JSONL
section outline
proposed tags
editable review markdown
SQLite/FTS search
basic source-grounded Q&A
session note generation
```

Possible first commands:

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

## Technology Stack

Initial stack:

```text
Language:
- Python

PDF parsing:
- Docling

PDF rendering / page images:
- PyMuPDF or pypdfium2

Storage:
- JSONL for raw artifacts
- SQLite for normalized records
- SQLite FTS5 for text search

LLM layer:
- hosted frontier model initially for quality
- local model later for cheap classification/tagging

Embeddings:
- optional in v1
- add local or hosted embeddings after FTS baseline

Review UX:
- Markdown review files first
- later Textual, Streamlit, or Obsidian integration

Exports:
- Obsidian-compatible Markdown
- source-linked notes
```

The implementation should stay boring at first. Avoid heavy RAG frameworks until the custom data model and learning interactions are clearer.

## Design Principles

1. **Provenance first**
   Every concept, tag, summary, and answer should point back to source spans.

2. **Human steering first**
   The initial system should expose proposed structure for review rather than pretend to fully understand the textbook.

3. **Parser-agnostic IR**
   Start with Docling, but normalize into our own schema.

4. **Learning state is first-class**
   The system should remember study sessions, confusions, progress, and intended next steps.

5. **Cross-text from the start**
   Even if the first MVP uses one book, the schema should support multiple books and cross-text concept linking.

6. **Local-first where practical**
   The system should be able to run locally for parsing, storage, search, and eventually tagging. Hosted LLMs can be used initially for quality.

7. **Do not over-automate too early**
   The project should discover the ideal interaction loop through review artifacts and personal use.

## Open Questions

* What is the right granularity for blocks: paragraph, equation, theorem, proof-step, or semantic chunk?
* Should the review artifact be Markdown, a TUI, a small web UI, or Obsidian-native?
* How much of the concept graph should be user-curated versus LLM-proposed?
* How should the system represent notation differences across books?
* How should confusions, exercises, and session notes be linked to source passages?
* Should this become part of Weaver, or remain a separate tool that exports into the LLM wiki?
* What is the smallest interaction that would make the system immediately useful during actual study?

## Near-Term Next Steps

1. Pick one textbook chapter from Revelation.
2. Run Docling on the chapter.
3. Inspect the raw output quality.
4. Define the first normalized block schema.
5. Generate a simple section outline.
6. Ask an LLM to propose tags for a small subset.
7. Create a Markdown review document.
8. Manually review the tags.
9. Save corrections as structured data.
10. Build a tiny `ask` command over accepted blocks and tags.

## Long-Term Vision

Foundation could become a personal learning environment for technical subjects. It would combine source-grounded textbook navigation, LLM tutoring, persistent study memory, concept graphs, exercise recommendation, and cross-text triangulation.

The mature version should make technical self-study feel less like reading isolated PDFs and more like working inside a living, navigable, personalized map of the subject.
