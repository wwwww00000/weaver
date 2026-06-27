# P12n And Quant Categorization

Date: 2026-06-27

This is a working taxonomy for the large `p12n` and `quant` source cluster. It
should guide the next wiki synthesis pass before final pages are written.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Boundary

Keep `p12n` and `quant` as related but distinct axes.

- `p12n` is the active applied machine-learning-to-trading project, with a
  crypto focus and current threads around temporal returns, sequence-model-like
  architectures, feature transforms, execution policy, and experiment
  infrastructure.
- `quant` is the broader methods/archive layer for reusable ideas that apply to
  quantitative trading, especially regression regularization, cross-validation,
  time series, tabular models, optimization, adaptive filters, and some deep
  learning.

Rule of thumb:

- Put an artifact in the `p12n` synthesis path when it describes the current
  system, current experiments, crypto trading execution, project infrastructure,
  or an active model family being built for p12n.
- Put an artifact in the `quant` synthesis path when it explains a reusable
  method, diagnostic, mathematical trick, validation idea, or modeling pattern
  that can outlive the current p12n implementation.
- Dual-link material when a p12n-motivated discussion also produces a durable
  method. Do not force it into only one home.

The existing triage labels are useful for source retrieval, but they are too
coarse to be the final wiki organization.

## Page Strategy

The next synthesis pass should probably create a short `p12n` project hub plus
several child pages. It should not pour the entire `p12n/quant` bundle into a
single page.

Later, introduce a separate methods area, likely under `wiki/topics/quant.md` or
`wiki/methods/quant.md`. The current wiki only has `wiki/projects/`, so this can
wait until the first quant method page is ready.

Use this split:

- Project pages answer: what is happening in the named workstream?
- Quant method pages answer: what durable technique or idea can be reused across
  projects?

## P12n Project Categories

### Project State And Roadmap

Purpose: capture the live shape of the project, not every technical detail.

Likely page:

- `wiki/projects/p12n.md`

Core source feeds:

- [raw/obsidian/weekly/2026-W25.md](../../raw/obsidian/weekly/2026-W25.md)
- [raw/obsidian/p12n/overview.md](../../raw/obsidian/p12n/overview.md)
- [raw/obsidian/p12n/ml.md](../../raw/obsidian/p12n/ml.md)

Expected content:

- active crypto trading ML project
- current temporal returns experiments
- current split between streaming data/modeling, target model, execution, and
  infrastructure
- links to child pages for details

### Temporal Returns Experiments

Purpose: capture the empirical research thread around lagged returns and current
signal discovery.

Likely child page:

- `wiki/projects/p12n/temporal-returns-experiments.md`

Expected content:

- short-lag predictiveness
- demeaned longer-lag predictiveness
- round-minute effects from 5-second sampling
- temporal basis ideas
- greedy feature cliques and robustness selection
- cross-asset/self-lag experiments

Primary feeds:

- weekly 2026-W25 p12n section
- `Returns Model Design`
- p12n conversations about temporal model design, temporal regime descriptors,
  sparse-lag AR models, and temporal cross-validation

### N-Linear And Structured Returns Models

Purpose: capture the active model family for robust, expressive return
forecasting.

Likely child page:

- `wiki/projects/p12n/n-linear-returns-models.md`

Expected content:

- bilinear and n-linear returns models
- diagonal plus low-rank asset operators
- lag filters and temporal bases
- time-of-day gates
- linear-attention interpretation
- alternating least-squares and block-coordinate fitting
- additive residual-fitting view

Primary feeds:

- `Bilinear Model Generalization`
- `N-linear model fitting`
- `Solving for Beta`
- `Linear Attention Branch - Bilinear Model Generalization`
- weekly 2026-W25 p12n n-linear notes

### Sequence-Model Analogies

Purpose: capture the modern sequence-model spirit that informs p12n without
making p12n into a generic AI research hub.

Likely child page:

- `wiki/projects/p12n/sequence-model-analogies.md`

Expected content:

- recurrent state as fast parameters
- test-time regression and in-context learning analogies
- RNN/minGRU/S4/linear-attention perspectives
- adaptive filtering as a principled lens on memory, forgetting, and online
  update rules
- diagnostics for whether recurrent updates behave like optimizer steps

Primary feeds:

- `Adaptive Filtering in Sequence Models`
- `Benchmarking Recurrent State Updates`
- `Fixed RNN with Interpretable Optimization`
- `RNN architecture design`
- `Sequence Model Literature Review`
- `Stagewise Sequence Modeling`

### Feature Transforms And BST

Purpose: capture the feature-discovery and tabular nonlinear modeling layer used
inside the applied p12n workflow.

Likely child page:

- `wiki/projects/p12n/feature-transforms-and-bst.md`

Expected content:

- bin smoother tree
- out-of-fold derived predictions
- feature transform grammar
- product bins and derived features
- residualization and leakage control
- binned nonlinearities, interaction search, and function-tree-like ideas

Primary feeds:

- [raw/obsidian/p12n/ml.md](../../raw/obsidian/p12n/ml.md)
- `Boosting components loop`
- product-bin and binned-regression conversations
- unassigned quant material on histograms, nonlinearities, and feature hashing

### Execution And Policy

Purpose: keep trading policy, thresholds, fills, and utility separate from pure
forecast modeling.

Likely child page:

- `wiki/projects/p12n/execution-and-policy.md`

Expected content:

- BPTE experiments
- edge vectors, thresholding, and fill-rate targets
- forecast as input to execution
- target position and CPA formulations
- disaggregated PnL, risk, and liquidation losses
- validation stopping and post-hoc threshold refits

Primary feeds:

- [raw/obsidian/p12n/overview.md](../../raw/obsidian/p12n/overview.md)
- [raw/obsidian/p12n/signals.md](../../raw/obsidian/p12n/signals.md)
- Obelisk child pages on edge, exits, and forecast realization as historical
  context

### Experiment Infrastructure

Purpose: capture the machinery that lets p12n iterate safely.

Likely child page:

- `wiki/projects/p12n/experiment-infrastructure.md`

Expected content:

- `duct` pipeline framework
- dependency resolution and in-memory caching
- config and parameter management
- lazy recomputation and model/statistics comparison
- Rust and reporting notes

Primary feeds:

- [raw/obsidian/p12n/duct.md](../../raw/obsidian/p12n/duct.md)
- [raw/obsidian/p12n/rust.md](../../raw/obsidian/p12n/rust.md)
- [raw/obsidian/p12n/overview.md](../../raw/obsidian/p12n/overview.md)

## Quant Method Categories

These should not become `p12n` pages by default. Pull them into p12n only when
they directly support an active p12n thread.

### Regression Stability And Validation

Likely method page:

- `wiki/topics/quant/regression-stability-and-validation.md`

Expected content:

- cross-validation as self-influence deletion
- LOOCV and hat-matrix identities
- temporal/block CV
- validation loss, shrinkage, and generalization diagnostics
- leakage and out-of-fold transformations

Source feeds:

- `unassigned/quant`
- `p12n/math`
- `p12n/machine learning`
- `genesis/quant` only when the material is more general than p12n

### Temporal Evidence And Window Risk

Likely method page:

- `wiki/topics/quant/temporal-evidence.md`

Expected content:

- whitened regression evidence
- congruency matrices and ACF-like summaries
- trailing-window original-risk scores
- `p^2` FFT method for small feature dimension and large windows
- p=1 special case

Source feeds:

- `Temporal Cross-Validation Unification`
- conversations on trailing-window risk and temporal evidence
- unassigned quant computation notes

### Adaptive Filters, EMA, And Kalman Views

Likely method page:

- `wiki/topics/quant/adaptive-filters-and-ema.md`

Expected content:

- EMA decay, dynamic forgetting, and input-dependent timescales
- LMS/NLMS/RLS and adaptive filtering
- Kalman filtering and covariance matching
- fast weights and online regression interpretations
- relation to Obelisk dynamic EMA decay and p12n sequence-model analogies

Source feeds:

- `Adaptive Filtering in Sequence Models`
- Obelisk `Dynamic EMA Decay`
- unassigned `quant/ema`
- p12n dynamic EMA and forget-gate conversations

### Structured Return Models

Likely method page:

- `wiki/topics/quant/structured-return-models.md`

Expected content:

- diagonal, low-rank, and diagonal-plus-low-rank return maps
- reduced-rank regression and PLS-like discovery
- temporal filters over lagged returns
- cross-sectional residual/reversion operators
- additive components and residual fitting

This page should cross-link heavily with the p12n n-linear page. The p12n page
should stay project-shaped; this method page can hold the general formulation.

### Tabular Nonlinearities And Feature Search

Likely method page:

- `wiki/topics/quant/tabular-nonlinearities.md`

Expected content:

- binned means, product bins, and hierarchical bins
- feature hashing and collision handling
- MARS, splines, function trees, KAN-like ideas
- ReLU/gating as regression features
- greedy feature search and residual fitting

Source feeds:

- unassigned `quant/histogram`
- p12n BST and feature transform notes
- unassigned machine-learning/tabular material

### Optimization And Computation

Likely method page:

- `wiki/topics/quant/optimization-and-computation.md`

Expected content:

- Gauss-Newton, ADMM, LSTQ gradients, LSQR/LSMR
- efficient MSE and LOOCV computations
- block coordinate descent
- alternating least-squares for structured models
- computational tradeoffs for rolling and streaming fits

Source feeds:

- unassigned `quant/computation`
- unassigned `quant/optimization`
- unassigned `math/optimization`
- p12n implementation handoff conversations

### Generalization And Regularization

Likely method page:

- `wiki/topics/quant/generalization-and-regularization.md`

Expected content:

- ridge, sparse features, OOF scaling
- gradient similarity measures
- forecast horizon generalization
- data-driven shrinkage/generalizer ideas
- validation-aware regularization

Source feeds:

- `p12n/machine learning`
- `p12n/math`
- `genesis/quant`
- unassigned `quant/generalization`
- unassigned `quant/ridge`

## Bridge Pages

Some pages should explicitly sit between project and method layers:

- `dynamic-ema-decay`: already exists under Obelisk, but should be cross-linked
  from p12n and later generalized into the adaptive-filter method page.
- `n-linear-returns-models`: p12n child page for the active model family, with a
  later quant method counterpart for the general formulation.
- `temporal-evidence`: quant method page, but many examples are p12n-motivated.
- `regression-stability-and-validation`: method page that should be linked from
  p12n BST, p12n n-linear, and future quant pages.
- `sequence-model-analogies`: p12n page now, possibly later cross-linked to
  Genesis if the focus broadens into general AI research.

## Source Assignment Rules

Use these defaults during synthesis:

| Source Bundle | Default Destination | Notes |
| --- | --- | --- |
| `p12n/quant` | p12n child pages | Move reusable parts into quant method pages later. |
| `p12n/ai` | p12n sequence-model page | Cross-link to quant methods when about fast weights, adaptive filters, or regression. |
| `p12n/math` | quant methods plus p12n links | Usually validation/generalization or model-fitting math. |
| `p12n/machine learning` | quant methods plus p12n links | Usually generalization and regularization. |
| `p12n/current priorities` | p12n hub | Current context, not durable method content. |
| `unassigned/quant` | quant methods | Pull into p12n only if clearly part of current p12n work. |
| `unassigned/math` | quant or revelation methods | Use p12n only for direct model-fitting support. |
| `unassigned/ai` | genesis by default | Pull into p12n for sequence-model or fast-weight material. |
| `obelisk/quant` | Obelisk archive | Cross-link only durable lessons into p12n or quant. |
| `genesis/quant` | Genesis or quant methods | Use p12n only when directly applicable to the trading model. |

## Immediate Next Step

Before writing final prose, make a p12n source map that assigns the 80 p12n
artifacts and the most relevant `unassigned/quant` artifacts to the categories
above.

Then draft:

1. `wiki/projects/p12n.md`
2. `wiki/projects/p12n/temporal-returns-experiments.md`
3. `wiki/projects/p12n/n-linear-returns-models.md`

Those three pages should be enough to test whether the taxonomy works before
expanding into the rest of the p12n and quant method pages.
