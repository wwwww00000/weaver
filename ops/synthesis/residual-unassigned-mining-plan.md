# Residual Unassigned Mining Plan

Date: 2026-06-28

This is the routing layer for the small residual `unassigned/*` queues after
the major quant, AI, cognitive, personal, writing, math, and drawing passes.
It is meant to close the initial bulk sweep without pretending every small
queue deserves a large hub page.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Method

Treat residual queues as one of three things:

- standalone topic pages when a queue has a coherent practice or research
  surface and no existing destination;
- source-map closure when a queue has already been absorbed into a project
  page;
- reference-only or skip when the material is too small, low-signal, or better
  handled just-in-time.

The goal is completion of the initial pass, not exhaustive fleshing. Future
review can deepen individual pages when one becomes active again.

## Queue Routing

| Queue | Count | Destination | Status |
| --- | ---: | --- | --- |
| `unassigned/book` | 17 | [Reading Notes And Books](../../wiki/topics/reading-and-books.md) plus existing Chronicle/Whetstone pages | complete |
| `unassigned/idea` | 17 | Split across Genesis, Conjuration, Accretion, Poker, Music, and reference-only tail | complete |
| `unassigned/creativity` | 10 | Existing Conjuration pages | complete |
| `unassigned/poker` | 9 | [Poker](../../wiki/topics/poker.md) | complete |
| `unassigned/art` | 7 | Existing Conjuration pages, with art-tail source-map update | complete |
| `unassigned/physics` | 7 | Existing Revelation pages | complete |
| `unassigned/uncategorized` | 7 | Route individually; mostly already covered by Quant, Genesis, Whetstone, or reference-only | complete |
| `unassigned/machine learning` | 6 | [AI Research Map](../../wiki/projects/genesis/ai-research-map.md) backlog update | complete |
| `unassigned/music` | 6 | [Music Practice And Tools](../../wiki/topics/music.md) | complete |
| `unassigned/finance` | 5 | Existing Accretion pages | complete |
| `unassigned/travel` | 5 | [Travel And Environment Design](../../wiki/projects/chronicle/travel-and-environment-design.md) source-map closure | complete |
| `unassigned/tech` | 4 | Existing Genesis agentic-tooling/agency pages or reference-only tail | complete |
| `unassigned/data science` | 1 | Reference-only; no standalone page in initial pass | complete |
| `unassigned/hobby` | 1 | Reference-only; no standalone page in initial pass | complete |
| `unassigned/reading` | 1 | [Reading Notes And Books](../../wiki/topics/reading-and-books.md) | complete |

## Standalone Topic Pages

### Poker

`unassigned/poker` is coherent enough to keep as a topic. It combines:

- GTO interpretability and human-facing solver study;
- exploitative play against static or non-adaptive opponents;
- Bayesian opponent modelling and sparse-read preflop adaptation;
- continuous-strength and interval-structured toy river solvers;
- an implementation tail from the earlier GTO solver project.

Status: complete in [Poker](../../wiki/topics/poker.md).

### Reading And Books

`unassigned/book` is not one domain. It is a cross-project reading layer:
productivity systems, wholehearted living, creative recovery, learning mastery,
extended cognition, play, career capital, economics, and political economy.

Status: complete in
[Reading Notes And Books](../../wiki/topics/reading-and-books.md).

### Music

`unassigned/music` is small but coherent: voice technique, song practice,
QWERTY music-controller ideas, and DAW/synthesis exploration. It is too
specific for Conjuration and too lightweight for a project hub.

Status: complete in [Music Practice And Tools](../../wiki/topics/music.md).

## Existing Destination Closure

### Conjuration

`unassigned/creativity` and `unassigned/art` mostly landed in:

- [Visualization And Imagination Training](../../wiki/projects/conjuration/visualization-and-imagination-training.md)
- [Constructive Drawing Practice](../../wiki/projects/conjuration/constructive-drawing-practice.md)
- [Drawing Studio Stack And Projects](../../wiki/projects/conjuration/drawing-studio-stack-and-projects.md)
- [Sourcebook Worldwork](../../wiki/projects/conjuration/sourcebook-worldwork.md)

The residual art tail adds soft sketching mediums, concept-art seed notes, and
manga reference notes to the studio stack.

### Revelation

`unassigned/physics` is already represented by:

- [Quantum Mechanics Spine](../../wiki/projects/revelation/quantum-mechanics-spine.md)
- [Emergence And Reverse Physics](../../wiki/projects/revelation/emergence-and-reverse-physics.md)
- [Active Learning For Math And Physics](../../wiki/projects/revelation/active-learning-for-math-and-physics.md)

No new Revelation page is needed in the initial pass.

### Accretion

`unassigned/finance` is already represented by:

- [Finance Tooling And Data](../../wiki/projects/accretion/finance-tooling-and-data.md)
- [Options Selling And Volatility Risk](../../wiki/projects/accretion/options-selling-and-volatility-risk.md)
- [Structured Products And Autocallables](../../wiki/projects/accretion/structured-products-and-autocallables.md)

No new Accretion page is needed in the initial pass.

### Genesis

`unassigned/machine learning` is a backlog tail for the Genesis AI research
map. AGOP/RFM, interpretable deep learning, LAR internals, IRL-as-skill-learning,
and conference watch notes are useful as future experiment seeds, but not as
separate pages yet.

`unassigned/tech` is mostly already represented by agentic tooling, editor
substrates, and agency/building practice. Hardware, VS Code, and security notes
remain reference-only unless one becomes a build project.

### Chronicle

`unassigned/travel` is already represented by
[Travel And Environment Design](../../wiki/projects/chronicle/travel-and-environment-design.md).
Packing notes remain logistics references rather than wiki synthesis.

## Reference-Only Tail

The following residual sources are intentionally not promoted during this
initial pass:

- one-off hobby or data-science notes such as tennis and data visualization;
- isolated societal or military-strategy prompts with no current project home;
- low-context hardware, security, or editor notes unless they later become
  Genesis work;
- small idea fragments that already have a better home in Chronicle,
  Conjuration, Genesis, Accretion, Music, or Poker.

They remain available through the copied artifacts and manifest. Future review
should pull them just-in-time when a concrete page or project needs them.
