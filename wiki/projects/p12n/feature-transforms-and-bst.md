---
title: Feature Transforms And BST
status: draft
page_type: research-thread
projects:
  - p12n
categories:
  - quant
  - trading
  - machine-learning
  - feature-engineering
  - tabular-modeling
source_bundles:
  - p12n/quant
  - p12n/project context
  - p12n/current priorities
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/p12n
related:
  - projects/p12n
  - projects/p12n/temporal-returns-experiments
  - projects/p12n/sequence-model-analogies
  - topics/quant/tabular-nonlinearities
  - topics/quant/regression-stability-and-validation
  - topics/quant/generalization-and-regularization
created: 2026-06-27
updated: 2026-06-28
---

# Feature Transforms And BST

The feature-transform and bin smoother tree thread is p12n's applied nonlinear
feature-discovery layer.

It sits between raw market features and the forecasting or execution models. Its
job is to create useful nonlinear, temporal, and interaction features without
letting the workflow become an opaque high-capacity learner.

## Current Role

BST currently serves three purposes:

- discover feature transforms with incremental predictive value;
- produce out-of-fold derived predictions for downstream modeling;
- provide interpretable nonlinear components such as binned smoothers, product
  bins, and residualized feature additions.

The p12n notes emphasize this as part of the streaming feature and transforms
framework. It is not just a model family; it is also the machinery for studying
which feature transforms are worth reifying into the broader system.

## Stagewise Loop

The intended loop is stagewise:

1. Start with base features and feature metadata.
2. Propose transform candidates.
3. Fit candidates against the current target or residual.
4. Score candidates with time-aware validation metrics.
5. Add the best component if it clears a threshold.
6. Generate out-of-fold derived predictions when later stages depend on it.
7. Optionally refit or backfit controlled pieces.
8. Log contribution traces, fold metrics, and feature metadata.

This is similar to boosting or a generalized additive model, but the base
families are p12n-specific: binned smoothers, EMAs, products, symbol and market
return features, execution-derived features, and temporal transforms.

## Out-Of-Fold Derived Features

Prediction-derived features are dangerous because they can leak validation
influence into later stages. The p12n notes explicitly call out this failure
mode and the implementation of out-of-fold derived predictions.

The rule should be:

```text
Any fitted prediction that becomes an input to another fitted model must be
cross-fitted or otherwise generated without same-row validation leakage.
```

This applies to:

- predictions from a selected feature component;
- residualized features;
- in-context-learning-like derived features;
- products involving fitted predictions;
- downstream BPTE or execution inputs that consume forecast outputs.

Open design issue: p12n may need fold-specific residual sets rather than one
global residual, especially when later stages are strongly fold-dependent.

## Transform Grammar

The feature-transform system needs an explicit grammar rather than ad hoc
feature explosion.

Current transform families include:

- raw feature bins;
- quantile and approximate bins;
- EMAs and fixed temporal bases;
- time-of-day and round-minute transforms;
- symbol, market, and cross-sectional return features;
- products and multiplicative derived features;
- prediction-derived features;
- binned EMAs and hashed binned EMAs;
- returns-like normalization by volatility or units metadata.

Feature metadata matters because not every feature should be allowed in every
product. The p12n notes point at moving product permissions into feature meta,
pruning unused product permissions, and computing reusable base bins once.

## Selective Temporal Feature Maps

One promising BST direction is to emulate sequence-model selectivity while
staying inside the "feature map plus ridge" workflow.

The conservative base learner menu is:

- distributed-lag linear models with ridge or elastic-net readouts;
- fixed filter banks, EMAs, or diagonal SSM poles crossed with current bins;
- reservoir or ESN states with analytic ridge readouts;
- sparse hashed lag kernels that act like a cheap attention-style convolution;
- tree or spline components only after the linear feature-map baselines are
  exhausted.

The strongest p12n-shaped idea from the unassigned queue is the selective hashed
temporal kernel. For a scalar or feature channel, emit sparse features such as:

```text
hash(current_bin, past_bin, lag_bucket) * past_value
```

This is a convolutional analogue of attention: current content gates which past
content and lag region matter, but the fit is still one regularized linear
solve. Useful variations include:

- signed or magnitude-difference bins;
- log-dilated lag buckets;
- wave or Fourier lag probes;
- fixed pole/filter states crossed with current bins;
- residual hashed buckets for rare high-value interactions.

This belongs in BST when the transform is explicitly generated, scored, and
logged. It should not become a recurrent module until the explicit version has
survived blocked validation and ablation.

## Binning And Product Bins

Binning is attractive because it gives robust nonlinear scalar effects with
simple diagnostics. Product bins add interactions, but they overfit quickly.

Useful product-bin controls:

- require minimum counts;
- shrink product-bin means toward lower-order effects;
- compare full product bins against parent/main-effect backoffs;
- hash only selected product combinations;
- add product permissions by metadata rather than by default;
- prune product candidates that do not clear incremental improvement thresholds.

The most important modeling distinction is whether a product bin is a final
prediction component or merely a derived feature offered to later stages. The
second is more flexible but raises leakage risk.

For p12n, target-aware buckets should be treated as fitted features. If bucket
means, tree leaves, or semantic hashes use target information, they must be
computed out of fold before becoming inputs to later components.

## Validation And Selection

Feature selection needs time-aware diagnostics, not only aggregate train fit.

Current or planned signals:

- out-of-fold valid `R^2`;
- cumulative out-of-fold validation curves;
- time-series gain plots per feature;
- per-fold contribution traces;
- HAC-style t-statistics of gain;
- residualization effects;
- base predictor benchmark suites;
- minimum incremental improvement thresholds;
- pruning rules based on iteration and unused metadata.

Greedy feature discovery should prefer small, interpretable modules over a long
forward-selection path. A candidate group is useful when it has:

- incremental validation gain;
- stable contribution across time folds;
- semantic or metadata coherence;
- synergy with the existing group, not just standalone strength;
- low reuse of already-explained feature families.

This suggests a workflow of seeded restarts: choose a plausible seed feature,
grow a small group with a validation/coherence score, stop early, log the group,
then restart with reuse penalties. The output is a collection of feature modules
that can be promoted, pruned, or handed to the sequence-model analogy pages.

The reusable method layer is split across
[Regression Stability And Validation](../../topics/quant/regression-stability-and-validation.md)
for leakage and out-of-fold feature handling, [Temporal
Evidence](../../topics/quant/temporal-evidence.md) for foldwise signal
diagnostics, and [Generalization And
Regularization](../../topics/quant/generalization-and-regularization.md) for
shrinkage and sparse-feature concerns.

## Relationship To Sequence Models

BST is not separate from the sequence-model thread. Several p12n ideas express
sequence-model behavior as feature transforms:

- filter-bank features conditioned on bins;
- EMA products and binned EMA states;
- diagonal SSM pole states crossed with current feature bins;
- hashed triplets of current bin, past bin, and lag bucket;
- attention-like feature hash triplets;
- in-context-learning-like transforms from causal target products;
- rolling regression states exposed as features;
- dynamic decay gates driven by current feature bins.

The conservative workflow is to implement these as explicit transforms first,
then promote only the stable ones into recurrent or adaptive modules.

## Open Questions

- What is the minimal feature metadata schema needed for safe transform
  generation?
- Should products be selected greedily, by parent permissions, or by a learned
  meta-scoring model?
- How should fold-specific residuals and out-of-fold derived predictions be
  represented in the pipeline?
- Which feature gain metrics are robust enough under serial dependence?
- When should a transform become a permanent p12n primitive rather than remain a
  study artifact?
- How much of BST should remain forecast-only versus feed execution and
  threshold training?
- Which selective feature-map baseline should be implemented first: binned EMA
  states, fixed pole states, or hashed tri-bin lag kernels?
- What audit artifact should record a discovered feature module before it is
  promoted into the production feature registry?

## Source Map

- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
- [p12n overview](../../../ops/artifacts/obsidian/p12n-overview.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
- [Boosting components loop](../../../ops/artifacts/chatgpt/6957de3f-9af0-8322-9487-410fe60d459d.md)
- [Base Learner Options TS](../../../ops/artifacts/chatgpt/6830a950-368c-8009-ab4b-c7baf293dd2e.md)
- [ML Regression with Product Bins](../../../ops/artifacts/chatgpt/6871e0bb-14a8-8009-a8c9-fbf8690c0430.md)
- [Ridge CV vs OOF Scaling](../../../ops/artifacts/chatgpt/6763f3ae-17ec-8009-8723-49f1fcb2e6c1.md)
- [Non-linear Feature Transformations](../../../ops/artifacts/chatgpt/674b3994-918c-8009-9724-e8dd5d984766.md)
- [Feature Hashing Alternatives](../../../ops/artifacts/chatgpt/68382bfb-6f44-8009-a58e-7a6a8bf15ad8.md)
- [Iterative Greedy Feature Selection](../../../ops/artifacts/chatgpt/69eb6c3d-c5d8-839e-97e0-8caedc8c6584.md)
- [Linear Regression with Modulation](../../../ops/artifacts/chatgpt/6834364d-3f9c-8009-b633-c4fc44a8399d.md)
- [Streaming k-means extension](../../../ops/artifacts/chatgpt/69b65ceb-6620-8398-8796-e663ba3066cf.md)
- [Tabular ML for Time Series](../../../ops/artifacts/chatgpt/67dc2d07-fa44-8009-b9fa-0ac6fc749115.md)
