---
title: Generalization And Regularization
status: draft
page_type: method-note
projects:
  - p12n
categories:
  - quant
  - generalization
  - regularization
  - validation
  - machine-learning
source_bundles:
  - p12n/machine learning
  - p12n/math
  - quant/generalization
  - quant/ridge
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - topics/quant/regression-stability-and-validation
  - topics/quant/temporal-evidence
  - topics/quant/tabular-nonlinearities
  - projects/p12n/execution-and-policy
created: 2026-06-27
updated: 2026-06-27
---

# Generalization And Regularization

Generalization is the gap between fitting an observed relationship and building
a predictor that survives new rows, new time periods, and downstream policy
use. In p12n-like return modeling, the problem is sharpened by low signal,
serial dependence, sparse features, and forecast horizons whose later pieces may
be mostly noise.

This page collects reusable regularization ideas that sit above ordinary model
fitting: horizon decomposition, ridge and sparse-feature shrinkage,
validation-calibrated parameter transforms, and gradient-similarity diagnostics.

## Horizon Decomposition

If a full-horizon target is a sum of disjoint future slices:

```text
Y = sum_k Y_k
```

then fitting each slice separately and summing the predictions does not
automatically improve generalization. In linear regression with the same
features and same ridge penalty:

```text
beta_full = (X^T X)^-1 X^T sum_k Y_k
          = sum_k (X^T X)^-1 X^T Y_k
          = sum_k beta_k
```

The equivalence also holds for plain linear SGD under matching initialization,
loss scaling, sample order, and learning rate.

Horizon decomposition helps only when it changes the effective learning
procedure:

- shared nonlinear representation;
- different regularization by horizon;
- validation-learned recombination weights;
- horizon-specific diagnostics;
- auxiliary supervision for easier near horizons;
- prevention of residual cancellation across slices.

The useful deployment view is to treat horizon heads as a basis:

```text
y_hat = sum_k w_k y_hat_k
```

with `w_k` chosen by validation or constrained by policy needs. If the first
few horizons generalize and the full long horizon has negative test `R^2`, the
likely outcome is not that equal-weight multi-target training fixes everything.
It is that the decomposition reveals which parts of the future should be
trusted.

## Ridge And Prediction Scaling

Ridge changes coefficient geometry during fitting:

```text
beta_ridge = (X^T X + lambda I)^-1 X^T y
```

Out-of-fold prediction scaling changes only the final amplitude:

```text
y ~= c y_hat_oof
0 <= c <= 1
```

These coincide only in special cases such as orthonormal designs, where ridge
is uniform shrinkage. In correlated designs, ridge changes coefficient shape;
one scalar prediction shrinker cannot reproduce that.

The practical split is:

- use OOF scaling for calibration;
- use ridge or structured shrinkage when coefficient geometry is unstable;
- inspect the gap between unscaled and scaled validation performance to
  distinguish miscalibration from overfit feature shape.

## Sparse Feature Regularization

Unit-variance scaling can under-regularize sparse features when zeros mean
missing or unavailable rather than real zeros.

If feature `j` is active on fraction `p_j` of rows, full-column variance can be:

```text
s_j^2 ~= p_j Var(x_j | active)
```

Ridge on standardized features is equivalent in original units to:

```text
lambda sum_j s_j^2 beta_j^2
```

so sparse columns can receive weaker original-coordinate penalties even though
they have fewer effective observations.

Useful fixes:

- distinguish real zero from missing zero;
- include missingness or activation indicators;
- standardize on active observations when that matches semantics;
- add penalty weights based on active count;
- require stronger validation evidence for rare features;
- group sparse features before estimating individual effects.

Sparse features should be judged by effective support, leverage, and
out-of-fold stability, not only by standardized column norm.

## Learned Generalizers

A recurring idea is to learn a post-training parameter transform:

```text
w_plus = G_theta(w_train)
```

The base model is trained normally on each fold. The transform `G_theta` is
then optimized on validation loss across folds:

```text
min_theta mean_k L_val(k)(f(X_val(k); G_theta(w_k)), y_val(k))
```

No gradients through training are required. This makes the idea simpler than
full bilevel regularizer learning.

Conservative `G_theta` families:

- uniform calibration shrinkage;
- diagonal gates by feature group;
- spectral shrinkage in a principal-component basis;
- low-rank harmful-direction suppression;
- monotone shrinkage curves over eigenvalue, t-statistic, or effective support;
- post-hoc prox maps such as soft thresholding or group shrinkage.

This includes ridge-like and lasso-like behavior as special cases, but the
learned object is the transform from trained parameters to more generalizable
parameters, not a penalty inserted into the original training objective.

Guardrails:

- low capacity;
- identity bias;
- monotonicity or smoothness constraints;
- many folds or rolling windows;
- final untouched test period;
- reporting the transformed parameter difference in prediction space.

## Gradient Similarity

Gradient similarity measures whether different samples, folds, horizons, or
tasks push parameters in compatible directions.

For a linear model with per-sample loss:

```text
g_i(w) = (w^T x_i - y_i) x_i
```

One can measure:

- pairwise gradient dot products;
- cosine similarities;
- gradient variance inside a batch;
- gradient alignment between train and validation blocks;
- task or horizon gradient interference.

For two task or horizon losses `L_A` and `L_B`, a gradient-difference penalty is:

```text
R(w) = ||grad L_A(w) - grad L_B(w)||^2
```

The cross term:

```text
grad L_A(w)^T grad L_B(w)
```

is the alignment measure. Positive alignment means both blocks want similar
updates. Negative alignment means one block's improvement tends to undo the
other's.

This is a diagnostic before it is a regularizer. In p12n, likely uses are:

- horizon-slice interference analysis;
- train versus validation gradient alignment;
- detecting noisy feature groups;
- testing whether sequence-model heads share useful representation;
- comparing raw gradients to optimizer-scaled update vectors.

## Validation-Aware Regularization Loop

A pragmatic regularization loop for quant experiments:

1. Fit a base model and generate out-of-fold predictions.
2. Evaluate blocked or rolling validation, not only random folds.
3. Separate amplitude calibration from coefficient-shape regularization.
4. Inspect temporal evidence and gradient alignment for stability.
5. Apply the simplest shrinker that explains the failure mode.
6. Refit or transform on full training data.
7. Hold out a later test period for final honesty.

The goal is not maximal regularization sophistication. The goal is to identify
which failure mode is present: noisy horizon, sparse feature leverage,
miscalibration, unstable coefficient direction, or feature group conflict.

## Open Questions

- Should p12n learn validation-calibrated horizon recombination weights?
- Can sparse-feature penalty weights be learned from active support and foldwise
  stability?
- Is a low-capacity post-training generalizer useful beyond ordinary ridge?
- Which gradient-alignment diagnostics predict blocked validation survival?
- Should optimizer-scaled updates be the default for gradient-similarity plots?

## Source Map

- [Forecast Horizon Generalization](../../../ops/artifacts/chatgpt/69dce9bb-bd10-8399-987b-c262e6f85e63.md)
- [Gradient Similarity and Generalization](../../../ops/artifacts/chatgpt/67691f82-f864-8009-b4b0-7991c0068fa1.md)
- [Gradient similarity measures](../../../ops/artifacts/chatgpt/68f1ff98-c128-8322-9b6c-a2f8296d7f5d.md)
- [Regularization concept exploration](../../../ops/artifacts/chatgpt/689a25e1-4428-8329-b331-49afd82fb261.md)
- [Ridge CV vs OOF Scaling](../../../ops/artifacts/chatgpt/6763f3ae-17ec-8009-8723-49f1fcb2e6c1.md)
- [Sparse Features in Ridge](../../../ops/artifacts/chatgpt/69cff0f3-96b8-839e-8380-caf5d0b911b6.md)
- [temporal relationship of response](../../../ops/artifacts/obsidian/generalization.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
