---
title: Optimization And Computation
status: draft
page_type: method-note
projects:
  - p12n
categories:
  - quant
  - optimization
  - computation
  - regression
  - machine-learning
source_bundles:
  - quant/computation
  - quant/optimization
  - unassigned/quant
  - p12n/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - topics/quant/regression-stability-and-validation
  - topics/quant/temporal-evidence
  - topics/quant/structured-return-models
  - projects/p12n/experiment-infrastructure
created: 2026-06-27
updated: 2026-06-27
---

# Optimization And Computation

Many p12n and quant ideas are attractive only if they can be evaluated across
many assets, lags, folds, windows, or candidate transforms. The reusable
question is not "what optimizer is best?" but "what algebraic shape does this
problem expose?"

This page collects computational patterns for regression-heavy experiments:
row-wise exact formulas, autocorrelation scans, sufficient statistics,
block-coordinate fitting, Gauss-Newton, and variable splitting.

## Row-Level Versus Summary-Level Computation

Some quantities are determined by aggregate sufficient statistics:

```text
X^T X
X^T y
y^T y
```

Training SSE for a fitted linear model can be computed from summaries:

```text
RSS = y^T y - beta^T X^T y
```

Other quantities require row-level access. Exact LOOCV needs:

```text
e_i = y_i - x_i^T beta
h_i = x_i^T (X^T X)^-1 x_i
```

The diagonal of the hat matrix is not determined by `X^T X` alone. Exact
LOOCV can avoid storing `n x n` matrices, but it still must stream through rows
to compute each residual and leverage.

This distinction should be explicit in implementation notes:

- summary-only: cheap, cacheable, fold-composable;
- row-streaming: memory-light but still data-pass dependent;
- row-pair or window-pair: likely needs FFT, blocking, sketching, or an
  approximation.

## Exact Linear-Smoother Shortcuts

For OLS, the LOOCV formula is:

```text
LOOCV = mean_i (e_i / (1 - h_i))^2
```

The leverages can be computed without materializing the hat matrix. With a thin
QR factorization:

```text
X = Q R
h_i = row_norm(Q_i)^2
```

With a Cholesky factorization of `X^T X`, stream rows and compute:

```text
h_i = x_i^T (X^T X)^-1 x_i
```

For block deletion, use block hat corrections instead of full refits when the
held-out block is small enough:

```text
e_S^(-S) = (I - H_SS)^-1 e_S
```

The main engineering point is to expose fit backends that can return the small
objects needed for diagnostics: residuals, leverages, trace, diagonal, and
block submatrices when feasible.

## Autocorrelation And Toeplitz Scans

When a transform is linear, shift-invariant, and evaluated with a quadratic
criterion, autocorrelation structure often makes large scans cheap.

For a scalar trailing-window coefficient:

```text
z_t = x_t y_t
beta_t,w = (1 / w) sum_{j=1}^w z_{t-j}
y_hat_t = x_t beta_t,w
```

The cross term is controlled by lag products of `z`:

```text
r_k = sum_t z_t z_{t-k}
C(w) ~= (2 / w) sum_{k=1}^w r_k
```

The fixed-scale objective also needs the squared prediction term:

```text
SSE(w) = sum y_t^2 - 2 C(w) + V(w)
```

If `x_t^2 ~= 1` and the process is treated as stationary, `V(w)` has a
Bartlett-weighted approximation:

```text
V(w) per time ~= (1 / w^2) [
  w gamma_0 + 2 sum_{k=1}^{w-1} (w - k) gamma_k
]
```

This can be scanned over all windows using prefix sums of `gamma_k` and
`k gamma_k` after an FFT autocorrelation pass.

The caveat is important: keeping the exact `x_t^2` factor turns the squared
term into a two-lag object:

```text
sum_t x_t^2 z_{t-i} z_{t-j}
```

That no longer collapses to a one-dimensional autocovariance unless extra
stationarity or independence assumptions are made.

## Sufficient Statistics For Structured Models

Structured return models often contain static ungated blocks. Those should use
precomputed normal-equation statistics when possible:

```text
S[l, j, m, k] = sum_t X[t, l, j] X[t, m, k]
R[l, j, i]    = sum_t X[t, l, j] Y[t, i]
```

These statistics support dense, diagonal, and low-rank updates without scanning
time for every candidate. They are especially useful for:

- fixed temporal bases;
- diagonal self effects;
- low-rank asset maps;
- static lag filters;
- foldwise recomputation by additive train/test statistics.

Time-varying gates, sample weights, and regime-conditioned models break the
static-statistics shortcut. Then the backend should either accumulate weighted
statistics by chunk, use a basis of precomputed weight profiles, or fall back to
row streaming.

## Block Coordinate And ALS

Many model families here are conditionally linear. Use that structure before
defaulting to generic nonlinear optimization.

Examples:

- fit asset map given lag filters;
- fit lag filters given asset map;
- fit diagonal effects before low-rank residual effects;
- fit scalar weights over frozen atom predictions;
- fit output readout given recurrent state;
- fit transform component to current residual.

The normal loop is:

```text
choose block
solve the block by ridge or constrained least squares
normalize scales
measure validation/residual improvement
repeat
```

Block coordinate methods need identifiability conventions. Products such as
`B a` or `U V^T` have scale symmetries, so the implementation should normalize
after updates and report prediction-space changes, not just parameter changes.

## Gauss-Newton

For nonlinear least squares:

```text
min_theta 0.5 ||r(theta)||^2
```

Gauss-Newton fits the local linearized residual:

```text
p = argmin_p 0.5 ||r + J p||^2
(J^T J) p = -J^T r
```

The useful interpretation is "linear regression on the Jacobian." At a current
iterate, `J` is a local design matrix:

- singular values diagnose identifiable parameter directions;
- row leverage identifies samples dominating the step;
- damping is local ridge regression;
- the projected residual shows how much the local model can fix.

Gauss-Newton is attractive when the model has efficient `Jv` and `J^T u`
products, separable linear blocks, or recurrent structure with cheap scans. It
is an escalation path after exact block solves, not a replacement for them.

## ADMM And Lifting

Variable splitting is useful when one formulation contains a difficult
coupling but the lifted subproblems are easy:

```text
min_x f(x) + g(x)
equiv
min_x,z f(x) + g(z) subject to x = z
```

ADMM alternates primal subproblem solves and dual updates. The pattern is
relevant when:

- a smooth loss and nonsmooth penalty should be separated;
- a dynamic constraint should be softened into a residual;
- hidden state trajectories should be fitted separately from gates;
- consensus or distributed fits need local variables;
- constraints are easier to project onto than optimize through directly.

The cost is extra state and penalty tuning. Use ADMM when the split creates
simple, inspectable subproblems; do not use it just to rename a hard problem.

## Practical Escalation Order

Prefer the cheapest faithful computation first:

1. Closed-form sufficient statistics.
2. Streaming row pass with `O(p^2)` state.
3. FFT or Toeplitz scan for shift-invariant quadratic transforms.
4. Block coordinate or ALS with exact block solves.
5. Iterative linear solvers for large normal equations.
6. Gauss-Newton or Levenberg-Marquardt for nonlinear residual blocks.
7. ADMM or lifting when splitting creates materially simpler subproblems.
8. Autodiff and generic first-order optimization when no structure remains.

This order is not ideological. It is a way to keep p12n experiments fast enough
that validation and ablation are affordable.

## Open Questions

- Which fit backends should become first-class in p12n: QR, Cholesky, LSQR, or
  chunked normal-equation accumulation?
- Which diagnostics should every backend expose by default?
- How often do Bartlett or stationarity approximations agree with exact
  finite-sample checks on p12n data?
- Can structured return ALS share one statistics cache across many model
  variants?
- Where does Gauss-Newton add value beyond block coordinate solves?

## Source Map

- [LOOCV Error Efficient Computation](../../../ops/artifacts/chatgpt/6811ed55-0e14-8009-9c2a-f4b586b27278.md)
- [MSE Computation for Trailing Window](../../../ops/artifacts/chatgpt/69de5663-b9e0-83a1-aa8a-b0463403013b.md)
- [Branch - MSE Computation for Trailing Window](../../../ops/artifacts/chatgpt/69e1d90a-cb1c-839d-8acb-dbf91b58ee07.md)
- [Gradient computation for LSTQ](../../../ops/artifacts/chatgpt/694233c9-c518-8322-98cc-9a709eabb499.md)
- [Gauss-Newton Optimization Insights](../../../ops/artifacts/chatgpt/69ce12d1-750c-839e-9dbc-b85b63d0aa5b.md)
- [RNN Gauss-Newton Optimization](../../../ops/artifacts/chatgpt/69e75b42-c304-839b-809e-dcca2b2b4394.md)
- [ADMM Variable Splitting Tutorial](../../../ops/artifacts/chatgpt/69a1cc34-679c-8398-a265-a5cb0821fb1e.md)
- [Autoregressive Model Optimization](../../../ops/artifacts/chatgpt/69ef1db7-01f8-839e-a148-7f69cd23ab49.md)
