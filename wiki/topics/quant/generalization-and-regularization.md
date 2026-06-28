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
  - unassigned/quant
  - unassigned/ai
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - topics/quant/regression-stability-and-validation
  - topics/quant/temporal-evidence
  - topics/quant/tabular-nonlinearities
  - projects/p12n/execution-and-policy
created: 2026-06-27
updated: 2026-06-28
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

## Proxy-Target Curriculum

A proxy target is useful when it extracts a stable latent direction that the
true deployment target estimates too noisily. In linear regression, the object
being estimated is the target-feature cross moment:

```text
g_h = X^T y_h
```

Changing from a long horizon to a short horizon changes `g_h`. Ridge on the
long target cannot generally reproduce that change because it is still driven
by the noisy long-horizon cross moment.

A structured curriculum should therefore smooth or combine horizon cross
moments rather than rely on initialization alone. For fully solved convex
linear problems, initialization has no effect unless the objective changes. Two
useful objective changes are:

```text
sum_h ||y_h - X beta_h||^2
  + lambda sum_h ||beta_h||^2
  + gamma sum_h ||beta_h - beta_{h-1}||^2
```

and a proximal continuation:

```text
beta_h = argmin_beta ||y_h - X beta||^2
       + lambda ||beta||^2
       + rho ||beta - beta_{h-1}||^2
```

The first shares strength across horizons globally. The second treats shorter
horizons as a prior mean for longer horizons. Both make the "curriculum" real in
the estimator, instead of relying on an optimization path that disappears after
full convergence.

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

## Ridge Penalty Geometry

In one-dimensional ridge without an intercept, the validation-optimal penalty
has a simple closed form if the labeled validation moments are known. With
training moments:

```text
a = x_train^T y_train
b = x_train^T x_train
```

and validation moments:

```text
c = x_val^T y_val
d = x_val^T x_val
```

the ridge coefficient is:

```text
beta(lambda) = a / (b + lambda)
```

and the validation-optimal candidate is:

```text
lambda* = a d / c - b
```

with boundary handling when the expression is negative, undefined, or the
training and validation slopes disagree in sign. The point is not that this
formula should be used operationally. It depends on validation labels and is
unstable when `c` is small. The useful lesson is geometric: ridge is choosing a
shrink factor that reconciles the train slope with the validation slope.

In multiple dimensions, a single `lambda` moves along a restricted shrinkage
path. If validation failure is caused by the wrong coefficient direction, not
only too much amplitude, scalar ridge may not be expressive enough. That is
where feature-group penalties, spectral shrinkage, proxy targets, or learned
post-training transforms become relevant.

## Quadratic Level Sets

In linear regression, "flat" and "sharp" are not properties of different local
minima. The squared-loss Hessian is fixed:

```text
H = X^T X
```

Near an optimum `w*`, the epsilon-level set is:

```text
(w - w*)^T H (w - w*) <= epsilon
```

Small eigenvalues of `H` give wide directions; large eigenvalues give narrow
directions. This is useful for thinking about near-optimal alternatives,
robustness, and implicit bias, but it is not the deep-learning notion of
choosing among distinct basins. In linear models, generalization usually comes
from how the solution is selected within this geometry: minimum norm, ridge,
sparse path, grouped shrinkage, or validation-calibrated transform.

## Kernel And Tangent-Feature View

The NTK view is useful here as a bridge between neural networks and ordinary
regularized regression. Near initialization, a network can be linearized as:

```text
f_theta(x) ~= f_theta0(x) + J_x (theta - theta0)
```

The tangent feature is `J_x`, and the kernel is the inner product
`K(x, x') = J_x J_x'^T`. Gradient descent writes residuals into the parameter
displacement as a combination of training-example tangent features. Prediction
then reads that displacement back through kernel similarities.

For p12n, the actionable lesson is not to rely on the NTK regime. It is to
recognize when a model is effectively fixed-feature regression. Random features,
reservoir states, fixed RBF centers, frozen neural features, and linearized
blocks all need the same generalization controls:

- ridge or spectral shrinkage on the readout;
- validation-aware early stopping when iterative fitting is used;
- leverage and self-influence checks;
- inspection of which kernel or feature modes are being fit;
- caution around low-eigenvalue modes that look like high-frequency noise.

Early stopping and ridge are both spectral filters in this view. They learn
large-eigenvalue, smoother modes first and suppress harder, lower-eigenvalue
target components.

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

## Alternative Smoothers And Metrics

Not every regression-like smoother is ordinary linear regression. A learned
Mahalanobis metric with a kernel smoother is still linear in the observed
responses for fixed metric:

```text
y_hat = S(M) y
```

but it is generally nonlinear as a function of the query features and has a
different hypothesis class from OLS. With an identity distance kernel, the
training-point smoother can even have zero self-influence because each point's
distance to itself is zero.

The regularization lesson is that raw parameter count can mislead. A full metric
has quadratic algebraic parameters, but diagonal, low-rank, trace-normalized, or
nearest-neighbor-constrained versions can have much lower effective complexity.
For p12n this is mostly a cautionary analogy: if a learned smoother appears to
generalize, inspect its self-influence, locality, and validation protocol rather
than comparing parameter counts directly with OLS.

## Interpretable ReLU And Additive Structure

Shallow ReLU networks are piecewise-linear models. That gives several
regularization and interpretation handles before reaching for a generic deep
network:

- decompose predictions into main effects and low-order interactions through
  functional ANOVA or additive-surrogate fits;
- constrain the architecture to GAM or GA2M-style components when
  interpretability is required by design;
- grow hinge or ReLU units stagewise against residuals so each added basis
  function has a visible role;
- inspect local linear regions or activation patterns as regime-specific linear
  models;
- distill a trained component into splines, trees, or additive basis functions
  when the exact network is too hard to read.

The p12n rule should be conservative: if a shallow ReLU block is valuable, first
ask whether its effect can be expressed as hinge bases, product bins, local
linear regimes, or additive components with comparable validation performance.
Only the residual value beyond those interpretable forms should justify the
opaque block.

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
- [Branch - Proxy-target training in regression](../../../ops/artifacts/chatgpt/69d5ed83-dbb4-83a1-b4fd-1f878f014cf9.md)
- [Flat vs Sharp Minima in Linear Regression](../../../ops/artifacts/chatgpt/67b3134f-cf50-8009-9265-a47222f57525.md)
- [Interpretable Deep Learning Models](../../../ops/artifacts/chatgpt/672ba721-c398-8009-9c8c-75e489f722b8.md)
- [Mahalanobis vs Linear Regression](../../../ops/artifacts/chatgpt/68480c76-7cbc-8009-aca1-4934960c1980.md)
- [NTK Kernel Representation Explanation](../../../ops/artifacts/chatgpt/69ed7a30-5620-83a1-bbdf-aee44f9ad3fb.md)
- [Optimal Ridge Penalty Computation](../../../ops/artifacts/chatgpt/6876f4ab-b368-8009-9320-b72c69c8ce00.md)
- [ReLU Network Interpretability Research](../../../ops/artifacts/chatgpt/67d19849-1f64-8009-9f88-7980df924237.md)
- [Ridge Penalty Optimization](../../../ops/artifacts/chatgpt/6876f4ac-77cc-8009-8b48-a1327e12c379.md)
- [Robust Regression Research Directions](../../../ops/artifacts/chatgpt/67191c44-b954-8009-8e92-c5799747b9bb.md)
- [temporal relationship of response](../../../ops/artifacts/obsidian/generalization.md)
- [ideas](../../../ops/artifacts/obsidian/regression.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
