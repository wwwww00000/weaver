# Wiki Hub Todo

This is the working queue for turning triaged source artifacts into curated wiki
hub pages and child pages.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Current Baseline

- Obelisk has been split into a project hub plus child pages.
- Commit: `722a68d Split Obelisk wiki into child pages`
- P12n now has a project hub plus six child pages, and Quant has a topic hub
  plus seven method pages.
- Genesis now has a project hub plus child pages for Weaver, agentic tooling,
  and AI research.
- Commit: `d4f0d31 Synthesize Genesis wiki hub`
- Chronicle and Whetstone now have paired project hubs plus child pages for
  pages/life OS, think tags, cadence, and felt sense.
- Commit: `9fbee08 Synthesize Chronicle and Whetstone wiki hubs`
- Conjuration now has a project hub plus child pages for visualization,
  constructive drawing, and sourcebook worldwork.
- Commit: `d9c552c Synthesize Conjuration wiki hub`
- Revelation now has a project hub plus child pages for the quantum mechanics
  spine, emergence/reverse physics, and active learning.
- Commit: `86caf7d Synthesize Revelation wiki hub`
- Accretion now has a project hub plus child pages for balance/portfolio
  policy, structured products, options selling, and finance tooling.
- Commit: `a347211 Synthesize Accretion wiki hub`
- The initial named project hub pass is complete. Remaining synthesis work is
  mostly queue mining from `unassigned/*` bundles into existing pages or new
  topic candidates.
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

- [x] Build the `chronicle` and `whetstone` hubs as a paired pass.
  - Keep the boundary explicit:
    - `chronicle`: morning pages, journaling, mindfulness, meditation,
      creative writing
    - `whetstone`: cognition improvement, metacognition, learning, problem
      solving
  - Mine `chronicle/cognitive`, `whetstone/cognitive`,
    `unassigned/cognitive`, `unassigned/personal`, and `unassigned/writing`.
  - Added paired project hubs:
    - [Chronicle](../../wiki/projects/chronicle.md)
    - [Whetstone](../../wiki/projects/whetstone.md)
  - Added child pages:
    - [Morning Pages And Life OS](../../wiki/projects/chronicle/morning-pages-and-life-os.md)
    - [Think Tags And Metacognition](../../wiki/projects/whetstone/think-tags-and-metacognition.md)
    - [Cadence And Mental Pages](../../wiki/projects/whetstone/cadence-and-mental-pages.md)
    - [Felt Sense And Modes](../../wiki/projects/whetstone/felt-sense-and-modes.md)
  - Remaining work: mine larger `unassigned/cognitive`, `unassigned/personal`,
    and `unassigned/writing` queues for reusable topic pages after the
    remaining project hubs exist.

- [x] Build the `conjuration` hub.
  - Focus on imagination, creativity, drawing, visual practice, and creative
    confidence.
  - Mine `unassigned/drawing`, `unassigned/creativity`, `unassigned/art`, and
    relevant `unassigned/writing`.
  - Added a project hub:
    - [Conjuration](../../wiki/projects/conjuration.md)
  - Added child pages:
    - [Visualization And Imagination Training](../../wiki/projects/conjuration/visualization-and-imagination-training.md)
    - [Constructive Drawing Practice](../../wiki/projects/conjuration/constructive-drawing-practice.md)
    - [Sourcebook Worldwork](../../wiki/projects/conjuration/sourcebook-worldwork.md)
  - Remaining work: review whether the large unassigned drawing/art queues
    should become a separate drawing topic hub or stay under Conjuration.

- [x] Build the `accretion` hub.
  - Focus on personal finance, wealth accumulation, structured products,
    options, and personal balance-sheet thinking.
  - Mine `accretion/finance`, `unassigned/finance`, and relevant
    `unassigned/personal`.
  - Added a project hub:
    - [Accretion](../../wiki/projects/accretion.md)
  - Added child pages:
    - [Balance And Portfolio Policy](../../wiki/projects/accretion/balance-and-portfolio-policy.md)
    - [Structured Products And Autocallables](../../wiki/projects/accretion/structured-products-and-autocallables.md)
    - [Option Selling And Volatility Risk](../../wiki/projects/accretion/options-selling-and-volatility-risk.md)
    - [Finance Tooling And Data](../../wiki/projects/accretion/finance-tooling-and-data.md)
  - Remaining work: write the actual investment policy statement and decide
    which finance tooling ideas belong in Accretion versus Genesis.

- [x] Build the `revelation` hub.
  - Focus on math and physics learning, intuition building, and bridges to
    quantitative modeling.
  - Mine `revelation/math`, `revelation/physics`, `unassigned/math`, and
    `unassigned/physics`.
  - Added a project hub:
    - [Revelation](../../wiki/projects/revelation.md)
  - Added child pages:
    - [Quantum Mechanics Spine](../../wiki/projects/revelation/quantum-mechanics-spine.md)
    - [Emergence And Reverse Physics](../../wiki/projects/revelation/emergence-and-reverse-physics.md)
    - [Active Learning For Math And Physics](../../wiki/projects/revelation/active-learning-for-math-and-physics.md)
  - Remaining work: review whether the broader unassigned math queue belongs
    mostly under quant, Revelation, or standalone math topic pages.

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

## Unassigned Mining Passes

- [ ] Route and mine `unassigned/quant`.
  - Initial routing plan:
    [unassigned-mining-plan.md](unassigned-mining-plan.md)
  - Preferred first page-deepening candidates:
    - [x] [Adaptive Filters And EMA](../../wiki/topics/quant/adaptive-filters-and-ema.md)
    - [x] [Temporal Evidence](../../wiki/topics/quant/temporal-evidence.md)
    - [x] [Temporal Returns Experiments](../../wiki/projects/p12n/temporal-returns-experiments.md)
      and [Structured Return Models](../../wiki/topics/quant/structured-return-models.md)
    - [x] [Regression Stability And Validation](../../wiki/topics/quant/regression-stability-and-validation.md)
      and [Generalization And Regularization](../../wiki/topics/quant/generalization-and-regularization.md)
- [ ] Route and mine `unassigned/ai`.
- [ ] Route and mine `unassigned/cognitive`.
- [ ] Route and mine `unassigned/personal`.
- [ ] Route and mine `unassigned/writing`.
- [ ] Route and mine `unassigned/math`.
- [ ] Route and mine `unassigned/drawing`.
