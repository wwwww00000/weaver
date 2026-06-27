# Wiki Hub Todo

This is the working queue for turning triaged source artifacts into curated wiki
hub pages and child pages.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Current Baseline

- Obelisk has been split into a project hub plus child pages.
- Commit: `722a68d Split Obelisk wiki into child pages`
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

- [ ] Build the `p12n` hub.
  - Start with a hub page and decide child pages before writing too much.
  - Likely child pages:
    - temporal modeling and dynamic filters
    - sequence models and recurrent architectures
    - bilinear and N-linear models
    - validation, generalization, and leakage control
    - regression and forecasting workflows
    - feature engineering and experiment infrastructure
  - Mine `p12n/quant`, `p12n/ai`, `unassigned/quant`, `unassigned/math`,
    and `unassigned/ai`.

- [ ] Build the `genesis` hub.
  - Likely child pages:
    - AI research map
    - agentic tools and coding workflows
    - Weaver as a knowledge-work system
    - ARC-AGI, reinforcement learning, and neurosymbolic experiments
    - building, agency, and taste formation
  - Mine `genesis/ai`, `genesis/tech`, `genesis/math`, and `unassigned/ai`.

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
