---
title: Linear Regression Identities And Solvers
status: draft
page_type: method-note
projects:
  - p12n
categories:
  - quant
  - regression
  - linear-algebra
  - computation
  - validation
source_bundles:
  - unassigned/math
  - p12n/math
  - unassigned/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - topics/quant/regression-stability-and-validation
  - topics/quant/optimization-and-computation
  - topics/quant/generalization-and-regularization
  - topics/quant/structured-return-models
  - projects/p12n/experiment-infrastructure
created: 2026-06-28
updated: 2026-06-28
---

# Linear Regression Identities And Solvers

Linear regression is useful in p12n because it exposes the algebra. The same
few objects explain fit, validation, risk approximation, solver choice, and
near-solution geometry:

```text
G = X^T X
c = X^T y
s = y^T y
```

For a coefficient vector `beta`, the training loss can be evaluated from
summaries:

```text
RSS(beta) = s - 2 beta^T c + beta^T G beta
```

That is the clean part. The important boundary is that many useful diagnostics
are not summary-only. Exact leverage, LOOCV, row influence, sparse rare-event
protection, and sketch quality all need row-level structure.

## Summary-Only Versus Row-Level

Summary statistics are enough for:

- training loss at a fitted `beta`;
- normal-equation solves when `G` is available;
- ridge paths if eigendecomposition or Cholesky of `G` is available;
- some GCV-style risk proxies based on degrees of freedom;
- fold-composable training statistics when folds can be added and subtracted.

They are not enough for exact LOOCV:

```text
e_i = y_i - x_i^T beta
h_i = x_i^T (X^T X)^-1 x_i
LOO_i = e_i / (1 - h_i)
```

The diagonal of the hat matrix is not determined by `X^T X` alone. Exact
LOOCV can be memory-light, but it still needs a row stream to compute each
residual and leverage.

Use this distinction in implementation notes:

- summary-only means cacheable and composable;
- row-streaming means no `n x n` object, but at least one data pass remains;
- row-sketching means the fitted problem itself has changed.

## Leverage And GCV

With a thin QR factorization:

```text
X = Q R
h_i = ||Q_i||^2
```

With a Cholesky factorization of `G`, leverages can be streamed as:

```text
h_i = x_i^T G^-1 x_i
```

Generalized cross-validation replaces individual leverages with an average
degree-of-freedom correction:

```text
GCV = (RSS / n) / (1 - trace(H) / n)^2
```

For OLS, `trace(H) = p`. For ridge and other linear smoothers, `trace(S_lambda)`
depends on the penalty. GCV is cheap because it is a scalar approximation. It
is not the same as LOOCV when leverage is concentrated.

For time-series and spatial data, ordinary GCV can be optimistic because rows
are not independent. Correlated-GCV style corrections try to inflate the risk
estimate using sample-correlation structure. The important practical rule is:
if correlation mismatch or noise-correlation assumptions are unclear, use
blocked or purged validation as the external check.

## Level-Set Geometry

Around the OLS optimum, the loss is a quadratic:

```text
L(beta) = L(beta_hat) + (beta - beta_hat)^T G (beta - beta_hat)
```

The near-optimal set

```text
L(beta) <= L(beta_hat) + epsilon
```

is an ellipsoid in identifiable directions and a cylinder along null-space
directions. Eigenvalues of `G` define flat and sharp directions:

- large eigenvalues: small coefficient changes raise loss quickly;
- small eigenvalues: large coefficient changes can preserve training loss;
- zero eigenvalues: predictions are unchanged along the null space.

This is a useful geometry, but it is not the deep-learning "flat minima" story.
In linear regression the curvature is fixed by the data; different minima do
not have different local Hessians. Generalization depends on how a point is
chosen inside the near-solution set: minimum norm, ridge, constraints,
validation selection, interpretability, or robustness.

To sample a fixed loss contour, diagonalize:

```text
G = V diag(lambda) V^T
u = sqrt(epsilon) * w / ||w||
delta = V (u / sqrt(lambda))
beta = beta_hat + delta
```

Small or zero eigenvalues need explicit handling. Null-space moves preserve
training predictions exactly, so they should be governed by an additional
criterion rather than sampled blindly.

## Sketching And Approximate Hessians

For least squares, the Hessian is exactly:

```text
H = X^T X / n
```

The empirical gradient covariance is not the same object:

```text
sum_i g_i g_i^T = X^T diag(r_i^2) X
```

That is residual-weighted curvature. It can be useful as a heteroskedastic or
Gauss-Newton-like object, but it is not a faithful OLS Hessian unless residual
weights are effectively constant.

The default one-shot approximation should be sketch-and-solve:

```text
beta_tilde = argmin_beta ||S X beta - S y||^2
```

Applying the same sketch to `X` and `y` changes both `X^T X` and `X^T y`
consistently. Sketching only `X^T X` while keeping exact `X^T y` is a surrogate
quadratic or approximate Newton solve. That can be useful, but the desired
property is spectral approximation, not merely matching total energy, trace, or
diagonal scale.

Leverage-score sampling is a principled row sketch:

```text
l_i = x_i^T (X^T X)^-1 x_i
```

Rows with rare feature combinations often matter because they preserve
directions that uniform sampling may drop. Exact leverage scores are circular,
but approximate or ridge leverage scores are usually enough. A practical
pipeline is a cheap oblivious sketch, approximate whitening, then leverage-like
row sampling.

## Solver Choice

Choose the solver from the access pattern.

| Setting | Preferred Tool | Reason |
| --- | --- | --- |
| moderate dense `p`, stable `G` | Cholesky or QR | exact, simple diagnostics |
| tall out-of-core data | LSQR, LSMR, or CG on normal equations | uses `X v` and `X^T u` products |
| streaming exact gradient feasible | batch gradient with exact line search or CG | avoids forming full `G` |
| very wide generated features | `LinearOperator` plus iterative solve | no feature materialization |
| block-orthogonal columns | block Cholesky, block QR, or block-Jacobi preconditioning | diagonal block solves are cheap |
| sparse high-dimensional data | coordinate or block-coordinate descent | exploits sparsity and separability |
| approximate enough | row sketch and solve | reduces `n` before forming pairwise products |

For a least-squares gradient:

```text
g(beta) = -X^T (y - X beta) / n
```

With ridge:

```text
g(beta) = -X^T (y - X beta) / n + lambda beta
```

For exact line search along descent direction `d`:

```text
alpha = (X d)^T r / (X d)^T (X d)
```

This uses the quadratic structure directly. In practice, conjugate gradient is
often a better use of the same matrix-vector products because it builds
conjugate directions instead of repeatedly descending along the current
gradient.

## Pathwise Feature Entry

Least Angle Regression is useful as a geometric reference point for sparse
linear modeling. It starts with the predictor most correlated with the residual,
then moves in a direction that keeps all active predictors equally correlated
with the residual until another predictor catches up.

The reusable ideas are:

- active-set paths can be piecewise linear;
- feature entry is governed by residual correlations;
- the equiangular direction accounts for covariance among active predictors;
- lasso-like paths need removal events when a coefficient crosses zero.

For p12n, LARS is more likely to be a diagnostic or analogy than a default
solver. It is useful when feature entry order is informative, but low-SNR
time-series work still needs blocked validation before treating path order as
signal.

## Structured Feature Expansions

Some linear regressions are only large because the features are products of two
feature sets:

```text
y_i ~= x_i^T B z_i
```

The naive design has `p q` columns, but the coefficient vector can be treated
as a matrix `B`.

Useful strategies:

- exact or regularized Sylvester/Kronecker solves when the algebra applies;
- low-rank `B = U V^T` when a factor model is acceptable;
- TensorSketch or feature hashing for approximate cross features;
- generated-on-the-fly `X v` and `X^T u` products for iterative solvers;
- kernel ridge when `n` is much smaller than `p q`.

This is the same family of ideas used by [Structured Return Models](structured-return-models.md):
exploit the coefficient tensor before expanding the design.

## Relationship To Other Pages

[Regression Stability And Validation](regression-stability-and-validation.md)
owns validation protocols: LOOCV, block deletion, OOF features, time splits,
proxy targets, and leakage control.

[Optimization And Computation](optimization-and-computation.md) owns broader
computational patterns: sufficient statistics, ALS, variable splitting,
autocorrelation scans, and large-model engineering.

[Generalization And Regularization](generalization-and-regularization.md) owns
regularization, shrinkage, and validation-aware model selection.

This page owns the algebraic identities and solver map for linear regression
itself.

## Open Questions

- Which linear-regression backend should p12n standardize first: QR/Cholesky,
  LSQR/LSMR, CG, or sketch-and-solve?
- Which diagnostics need row streams versus only cached sufficient statistics?
- Should exact leverage/LOOCV be supported for generated feature pools?
- Which sketching strategy is safest for sparse rare-event features?
- When should near-solution geometry be used for exploration rather than
  treated as a distraction from validation?

## Source Map

- [Block Orthogonal LS Solvers](../../../ops/artifacts/chatgpt/68366f18-3ba4-8009-b87c-de2db683bc74.md)
- [CorrGCV Formulation Summary](../../../ops/artifacts/chatgpt/6867e44f-d85c-8009-95f8-42ee9d7effda.md)
- [Exploring Parameter Space Solutions](../../../ops/artifacts/chatgpt/672c38c2-8398-8009-8978-599861ac0f0c.md)
- [Flat vs Sharp Minima in Linear Regression](../../../ops/artifacts/chatgpt/67b3134f-cf50-8009-9265-a47222f57525.md)
- [Least Angle Regression Explained](../../../ops/artifacts/chatgpt/674c0a48-e938-8009-94fa-c205a686cd89.md)
- [Linear Regression Hessian Approximation](../../../ops/artifacts/chatgpt/69d09be4-a6e8-83a0-8ea9-6ef0cbf1c7f1.md)
- [Linear Regression Tricks](../../../ops/artifacts/chatgpt/685d3eb8-5fec-8009-a4e3-e5b91d369995.md)
- [LOOCV Error Efficient Computation](../../../ops/artifacts/chatgpt/6811ed55-0e14-8009-9c2a-f4b586b27278.md)
- [Speeding Up Linear Regression](../../../ops/artifacts/chatgpt/674f4736-7960-8009-a075-e546853a02f9.md)
- [linear regression](../../../ops/artifacts/obsidian/linear-regression.md)
