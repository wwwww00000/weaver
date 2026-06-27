---
title: Tabular Nonlinearities And Feature Search
status: draft
page_type: method-note
projects:
  - p12n
categories:
  - quant
  - machine-learning
  - tabular-modeling
  - feature-engineering
  - regression
source_bundles:
  - p12n/quant
  - unassigned/quant
  - quant/histogram
  - quant/ridge
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - projects/p12n/feature-transforms-and-bst
  - topics/quant/temporal-evidence
created: 2026-06-27
updated: 2026-06-27
---

# Tabular Nonlinearities And Feature Search

This page collects reusable methods for adding nonlinear structure to regression
models while keeping the result inspectable and regularized.

The p12n version lives in
[Feature Transforms And BST](../../projects/p12n/feature-transforms-and-bst.md).
This page keeps the general toolbox: binned smoothers, splines, product bins,
feature hashing, additive components, and leakage-safe derived features.

## Scalar Nonlinearities

The simplest robust nonlinear primitive is a histogram smoother:

```text
f(x) = mean(y | x in bin_b)
```

It is cheap, local, and easy to inspect. It is also a degree-zero spline: a
piecewise constant function with knots at bin edges.

Continuous upgrades:

- piecewise-linear hat basis as a differentiable soft histogram;
- quadratic or cubic B-splines for smoother derivatives;
- P-splines with second-difference penalties for controlled smoothness;
- RBF features when smoothness matters more than sparsity;
- threshold or indicator features when interpretability matters most.

For scalar features, splines and histogram smoothers are often better first
choices than small MLPs: they have local support, simple regularization, and
clear plots.

## Product Bins

Product bins model interactions by combining discretized feature categories:

```text
prediction = mean(y | bin_a(x1), bin_b(x2), ...)
```

The immediate problem is sparsity. High-order product bins have low counts and
will overfit unless they borrow strength from simpler effects.

Regularization options:

- shrink a product-bin mean toward lower-order parent bins;
- require minimum counts before using a deeper bin;
- learn a smoothing weight such as `N / (N + gamma)`;
- use out-of-fold target encoding for bin means;
- prune product candidates by validation gain;
- hash rare product bins into a bounded residual cache.

The main structural issue is that product-bin hierarchies are usually DAGs, not
trees. A tuple like `(x_bin, y_bin, z_bin)` has multiple valid parents. A method
must choose one of:

- fixed parent order;
- best-evidence backoff;
- DAG smoothing across all parents;
- low-rank tensor factorization instead of explicit parents.

## Low-Rank Interaction Backbones

One alternative to explicit product-bin hierarchies is a low-rank categorical
interaction model:

```text
y_hat = sum_k product_j A_j[k, bin_j(x)]
```

This is a CP-style tensor factorization over binned features. It borrows
strength continuously because every bin participates through shared latent
components. A residual cache can then store only the high-value product-bin
exceptions.

This is less directly interpretable than a single binned mean, but it avoids
exponential storage and the ambiguous-parent problem.

## Additive Component Loops

Many nonlinear transforms fit naturally into a stagewise additive loop:

```text
prediction = sum_m component_m(features)
```

Each family proposes candidate components. The engine fits candidates to the
current residual, chooses the best one, adds it, and optionally emits derived
features for later stages.

Useful component families:

- histogram or spline smoothers;
- pairwise products;
- product bins;
- small tree stumps or shallow trees;
- feature crosses;
- RBF or kernel centers;
- temporal transforms such as EMAs;
- prediction-derived features;
- low-rank interaction features.

Backfitting can reoptimize components by coordinate descent on partial
residuals, but it needs damping and identifiability constraints.

## Leakage Control

Derived features are the main risk.

If a fitted component's prediction becomes an input to a later component, then
the derived feature should be cross-fitted:

```text
fit component on training folds
emit prediction for held-out fold
use the concatenated held-out predictions as the derived feature
```

This matters for:

- target encoding;
- prediction-derived features;
- residual-derived features;
- stacked components;
- products involving fitted predictions;
- downstream models that consume forecast outputs.

Post-hoc OOF scaling can calibrate a prediction, but it is not a substitute for
regularization inside a correlated feature model. In orthonormal cases, global
prediction scaling can resemble uniform ridge shrinkage. In typical correlated
features, ridge changes the coefficient shape in ways a single scalar cannot.

## Computation

Binning can become a bottleneck if it is repeated often. Useful implementation
patterns:

- reuse base feature bin indices across transforms;
- prefer arithmetic indexing for equal-width bins;
- use vectorized or JIT bin-index kernels for irregular bins;
- use compact integer encodings for product bins;
- compute mixed-radix product-bin IDs incrementally;
- use hashing for high-order sparse products;
- cache fitted component predictions by feature version.

For spline smoothers, exploit local support. A degree `p` B-spline touches only
`p + 1` basis functions per row, so normal-equation accumulation is effectively
linear in samples for small knot counts.

## Validation And Regularization

Tabular nonlinearities are useful because they are easy to overfit. The controls
should be first-class:

- minimum bin counts;
- shrinkage toward parents or global mean;
- ridge or smoothness penalties;
- foldwise target encoding;
- out-of-fold derived predictions;
- blocked validation for time series;
- residualized incremental value;
- validation gain thresholds;
- pruning unused feature crosses;
- contribution plots by feature and fold.

The most useful primitive is not "add nonlinear features." It is "add a
nonlinear feature only when its incremental value survives a validation protocol
that matches the data dependence."

## Relationship To P12n

P12n uses these methods for feature transform discovery, forecast features, and
eventually execution conditioning. The project-specific concerns are stronger
than the general method page:

- causal feature construction;
- time-series folds;
- serial dependence;
- forecast-to-execution leakage;
- symbol and market feature metadata;
- products of fitted predictions;
- downstream BPTE and threshold training.

This page should remain the reusable toolbox. P12n pages should decide which
parts of the toolbox are currently active.

## Open Questions

- Is a product-bin DAG smoother worth implementing, or should p12n prefer
  low-rank interaction backbones plus sparse residual caches?
- Which scalar smoother should be the default: histogram, hat basis, or
  P-spline?
- How should feature metadata restrict product generation?
- Can a meta-model learn which transform candidates are worth evaluating?
- What is the right validation statistic for tiny but stable nonlinear effects?

## Source Map

- [Boosting components loop](../../../ops/artifacts/chatgpt/6957de3f-9af0-8322-9487-410fe60d459d.md)
- [ML Regression with Product Bins](../../../ops/artifacts/chatgpt/6871e0bb-14a8-8009-a8c9-fbf8690c0430.md)
- [Non-linear Feature Transformations](../../../ops/artifacts/chatgpt/674b3994-918c-8009-9724-e8dd5d984766.md)
- [Continuous Histogram Smoothing](../../../ops/artifacts/chatgpt/6a2221ce-33d8-83ec-978d-7626e8ff3c3f.md)
- [Histogram smoother to B-spline](../../../ops/artifacts/chatgpt/697db20f-cd94-839d-a687-af61e186b9c9.md)
- [Faster histogram alternatives](../../../ops/artifacts/chatgpt/68501c0c-6f4c-8009-b40a-1f39f1799091.md)
- [Ridge CV vs OOF Scaling](../../../ops/artifacts/chatgpt/6763f3ae-17ec-8009-8723-49f1fcb2e6c1.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
