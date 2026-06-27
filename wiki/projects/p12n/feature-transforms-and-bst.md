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
updated: 2026-06-27
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

## Source Map

- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
- [p12n overview](../../../ops/artifacts/obsidian/p12n-overview.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
- [Boosting components loop](../../../ops/artifacts/chatgpt/6957de3f-9af0-8322-9487-410fe60d459d.md)
- [ML Regression with Product Bins](../../../ops/artifacts/chatgpt/6871e0bb-14a8-8009-a8c9-fbf8690c0430.md)
- [Ridge CV vs OOF Scaling](../../../ops/artifacts/chatgpt/6763f3ae-17ec-8009-8723-49f1fcb2e6c1.md)
- [Non-linear Feature Transformations](../../../ops/artifacts/chatgpt/674b3994-918c-8009-9724-e8dd5d984766.md)
