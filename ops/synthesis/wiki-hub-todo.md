# Wiki Hub Todo

This is the working queue for turning triaged source artifacts into curated wiki
hub pages and child pages.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Current Baseline

- Obelisk has been split into a project hub plus child pages.
- Commit: `722a68d Split Obelisk wiki into child pages`
- P12n now has a project hub plus six child pages, and Quant has a topic hub
  plus seven method pages.
- Keep future passes source-grounded, but do not let raw source references dominate
  the page shape. The output should read like synthesized wiki material.

## Prioritization

The largest raw bundles are mostly `unassigned/*`. Treat those as mining queues,
not as durable wiki hubs. Prefer real project hubs first, then pull relevant
unassigned material into those pages or into concept pages.

For the next pass, keep `p12n` and `quant` slightly disjoint:

- `p12n` is the active applied machine-learning-to-trading project, with a
  crypto focus and current threads in the spirit of modern sequence models.
- `quant` is a broader methods/archive layer for ideas applicable to
  quantitative trading, especially regression regularization, cross validation,
  time series, tabular models, and some deep learning.

Project-scale queues from the current inventory:

| Priority | Hub | Artifact Count | Largest Feeds |
| --- | --- | ---: | --- |
| 1 | `p12n` | 80 | `p12n/quant`, `p12n/ai`, `unassigned/quant`, `unassigned/math`, `unassigned/ai` |
| 2 | `genesis` | 40 | `genesis/ai`, `genesis/tech`, `unassigned/ai` |
| 3 | `chronicle` | 14 | `chronicle/cognitive`, `unassigned/personal`, `unassigned/writing` |
| 4 | `whetstone` | 13 | `whetstone/cognitive`, `unassigned/cognitive` |
| 5 | `accretion` | 9 | `accretion/finance`, `unassigned/finance` |
| 6 | `revelation` | 6 | `revelation/math`, `revelation/physics`, `unassigned/math`, `unassigned/physics` |
| 7 | `conjuration` | 4 | `unassigned/drawing`, `unassigned/creativity`, `unassigned/art`, `unassigned/writing` |

Largest unassigned mining queues:

| Queue | Artifact Count | Likely Destinations |
| --- | ---: | --- |
| `unassigned/quant` | 92 | `p12n`, quant concepts, possibly Obelisk follow-ups |
| `unassigned/cognitive` | 54 | `whetstone`, `chronicle`, cognition concept pages |
| `unassigned/personal` | 46 | `chronicle`, `accretion`, life operations pages |
| `unassigned/ai` | 34 | `genesis`, `p12n`, AI research/tooling pages |
| `unassigned/writing` | 28 | `chronicle`, `conjuration`, writing concept pages |
| `unassigned/math` | 27 | `revelation`, `p12n`, math concept pages |
| `unassigned/drawing` | 22 | `conjuration`, drawing concept pages |

## Next Hub Passes

- [x] Draft the `p12n` hub and initial quant method split.
  - Added a p12n project hub with child pages for temporal returns, n-linear
    returns models, sequence-model analogies, feature transforms, execution and
    policy, and experiment infrastructure.
  - Added a quant topic hub with method pages for temporal evidence, adaptive
    filters, structured return models, tabular nonlinearities, regression
    stability, optimization/computation, and generalization/regularization.
  - Remaining work: deepen individual pages after source-specific review and
    connect future implementation artifacts back into the wiki.

- [x] Build the `genesis` hub.
  - Likely child pages:
    - [AI research map](../../wiki/projects/genesis/ai-research-map.md)
    - [agentic tools and coding workflows](../../wiki/projects/genesis/agentic-tooling.md)
    - [Weaver as a knowledge-work system](../../wiki/projects/genesis/weaver-as-knowledge-system.md)
    - ARC-AGI, reinforcement learning, and neurosymbolic experiments are
      currently grouped under the AI research map.
    - building, agency, and taste formation remains a possible later child
      page if more source material is pulled in.
  - Mine `genesis/ai`, `genesis/tech`, `genesis/math`, and `unassigned/ai`.
  - Remaining work: review whether `unassigned/ai` should produce additional
    topic pages for context management, reasoning-model training, or
    notebook-agent workflows.

- [ ] Build the `chronicle` and `whetstone` hubs as a paired pass.
  - Keep the boundary explicit:
    - `chronicle`: morning pages, journaling, mindfulness, meditation,
      creative writing
    - `whetstone`: cognition improvement, metacognition, learning, problem
      solving
  - Mine `chronicle/cognitive`, `whetstone/cognitive`,
    `unassigned/cognitive`, `unassigned/personal`, and `unassigned/writing`.

- [ ] Build the `conjuration` hub.
  - Focus on imagination, creativity, drawing, visual practice, and creative
    confidence.
  - Mine `unassigned/drawing`, `unassigned/creativity`, `unassigned/art`, and
    relevant `unassigned/writing`.

- [ ] Build the `accretion` hub.
  - Focus on personal finance, wealth accumulation, structured products,
    options, and personal balance-sheet thinking.
  - Mine `accretion/finance`, `unassigned/finance`, and relevant
    `unassigned/personal`.

- [ ] Build the `revelation` hub.
  - Focus on math and physics learning, intuition building, and bridges to
    quantitative modeling.
  - Mine `revelation/math`, `revelation/physics`, `unassigned/math`, and
    `unassigned/physics`.

## Per-Hub Checklist

- [ ] Read the project glossary entry before writing.
- [ ] Review the project-specific bundle and the relevant unassigned mining
  queues.
- [ ] Draft the hub page with YAML metadata.
- [ ] Split into child pages early if the hub becomes long.
- [ ] Keep raw source references compact and local to the claims they support.
- [ ] Update [wiki/index.md](../../wiki/index.md).
- [ ] Run `git diff --check`.
- [ ] Commit after each coherent hub or project pass.
