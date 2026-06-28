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
updated: 2026-06-28
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

The deep-learning analogue is a numerical-feature embedding: bucketize the
scalar, then look up a learned vector or a piecewise-linear encoding. The useful
lesson is not that the embedding must be trained by a neural net. It is that a
scalar can be turned into a local basis with ordered support, and a regularized
linear readout can learn the nonlinear shape.

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

## Hashing And Target-Aware Buckets

Feature hashing is attractive when product bins are too numerous to enumerate.
For a tuple of bin indices, useful deterministic or randomized encodings include:

- mixed-radix keys when the product of cardinalities is small enough;
- Zobrist or tabulation hashing for fast variable-cardinality tuples;
- signed hashing to reduce collision bias;
- separate hash spaces for main effects, pair effects, and higher-order
  residuals.

A single hashed row bucket keeps the fitted design diagonal: each bucket gets a
count and a target sum. The ridge-like update is:

```text
beta_b = sum_y_b / (n_b + lambda)
```

This is fast, but collisions are not free. Frequent or high-signal keys should
either get collision-free treatment or be protected by a hot-key dictionary,
minimal-perfect hash, or explicit feature table. Rare buckets should usually be
shrunk toward a prior rather than deleted.

Target-aware hashing is a supervised grouping problem. Safer versions include:

- out-of-fold target encoding with m-estimate or empirical-Bayes shrinkage;
- leaf IDs from a shallow regression tree as supervised buckets;
- sorting row keys by out-of-fold target mean, then quantizing those means;
- learned binary or semantic hashes only after a held-out leakage check.

The rule is the same as for target encoding: a row's target must not participate
in the bucket statistic later used to predict that row.

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

A practical hybrid is a low-rank backbone plus a sparse residual cache. The
backbone captures broad interaction structure:

```text
y_hat = sum_r product_j A_j[r, bin_j(x)]
```

The residual cache stores only product-bin exceptions that survive validation.
This keeps the "borrow strength from parents" spirit without needing to choose a
single parent in a product-bin DAG.

## Functional ANOVA And Varying Coefficients

A second-order functional ANOVA with histogram main effects and product-bin
interactions is still a linear model, but it may be too large to materialize.
Useful fitting strategies are:

- backfitting: alternate main-effect and interaction fits against partial
  residuals;
- block or coordinate descent over bin groups;
- aggregated sufficient statistics by bin or bin pair;
- iterative solvers with sparse matrix-vector products;
- low-rank tensor or spline approximations for interaction surfaces.

Backfitting is a block Gauss-Seidel method on the normal equations. It is
well-behaved when the penalized solution is unique, but can be slow when
components overlap heavily. Damping, ridge penalties, and better initialization
are therefore part of the model, not just implementation details.

The same algebra covers fixed soft mixtures of linear regressions. If
`s_ij = w(z_i, c_j)` is a fixed soft assignment, stack the weighted blocks:

```text
X_tilde = [D_1 X | D_2 X | ... | D_k X]
```

Then solve one ridge regression over the block coefficients. Learning the
centers or bandwidths turns it into a nonlinear outer-loop problem.

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

## Greedy Module Discovery

Feature search does not have to imitate ordinary forward selection. For
exploratory p12n-style work, a candidate group can be scored as a small module:

```text
score(j | S) =
  validation_gain(j | S)
  + gamma * synergy(j, S)
  + lambda * coherence(j, S)
  - rho * reuse_penalty(j)
```

Where possible, compute `V(S)` out of fold, then define a conservative synergy
term:

```text
synergy(j, S) = V(S union {j}) - max(V(S), V({j}))
```

This favors groups that are jointly useful, not just individually strong. The
coherence term can use feature-family metadata, lag-profile similarity,
coefficient-profile similarity, or semantic tags. Early stopping and restarts
then produce several small feature groups instead of one large opaque selected
set.

The main failure mode is fake suppression: features that look valuable only
because they cancel fold noise. Use time-aware cross-fitting, ridge inside the
group score, and stability penalties across folds.

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
- benchmark `searchsorted` against sorted-block lookup, small-edge linear scans,
  and compare-sum tricks when the number of edges is tiny;
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
- When should p12n use target-aware buckets rather than ordinary feature
  hashing?
- Is a greedy module-discovery pass useful enough to promote into tooling, or
  should it stay an analysis procedure?

## Source Map

- [Boosting components loop](../../../ops/artifacts/chatgpt/6957de3f-9af0-8322-9487-410fe60d459d.md)
- [Base Learner Options TS](../../../ops/artifacts/chatgpt/6830a950-368c-8009-ab4b-c7baf293dd2e.md)
- [ML Regression with Product Bins](../../../ops/artifacts/chatgpt/6871e0bb-14a8-8009-a8c9-fbf8690c0430.md)
- [Non-linear Feature Transformations](../../../ops/artifacts/chatgpt/674b3994-918c-8009-9724-e8dd5d984766.md)
- [Continuous Histogram Smoothing](../../../ops/artifacts/chatgpt/6a2221ce-33d8-83ec-978d-7626e8ff3c3f.md)
- [Discretization in Deep Learning](../../../ops/artifacts/chatgpt/67b71b0c-5d0c-8009-8093-27d79fdb7289.md)
- [Histogram smoother to B-spline](../../../ops/artifacts/chatgpt/697db20f-cd94-839d-a687-af61e186b9c9.md)
- [Faster histogram alternatives](../../../ops/artifacts/chatgpt/68501c0c-6f4c-8009-b40a-1f39f1799091.md)
- [Feature Hashing Alternatives](../../../ops/artifacts/chatgpt/68382bfb-6f44-8009-a58e-7a6a8bf15ad8.md)
- [Fitting Functional ANOVA Models](../../../ops/artifacts/chatgpt/678f78e8-7f04-8009-8be1-1e12a5dee954.md)
- [Iterative Greedy Feature Selection](../../../ops/artifacts/chatgpt/69eb6c3d-c5d8-839e-97e0-8caedc8c6584.md)
- [Linear Model with Nonlinearity](../../../ops/artifacts/chatgpt/d55275c4-b7fe-4cd7-bcce-d66d0c3f1c68.md)
- [Linear Regression with Modulation](../../../ops/artifacts/chatgpt/6834364d-3f9c-8009-b633-c4fc44a8399d.md)
- [Streaming k-means extension](../../../ops/artifacts/chatgpt/69b65ceb-6620-8398-8796-e663ba3066cf.md)
- [Tabular ML for Time Series](../../../ops/artifacts/chatgpt/67dc2d07-fa44-8009-b9fa-0ac6fc749115.md)
- [Ridge CV vs OOF Scaling](../../../ops/artifacts/chatgpt/6763f3ae-17ec-8009-8723-49f1fcb2e6c1.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
