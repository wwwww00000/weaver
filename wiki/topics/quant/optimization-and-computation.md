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
updated: 2026-06-28
---

# Optimization And Computation

Many p12n and quant ideas are attractive only if they can be evaluated across
many assets, lags, folds, windows, or candidate transforms. The reusable
question is not "what optimizer is best?" but "what algebraic shape does this
problem expose?"

This page collects computational patterns for regression-heavy experiments:
row-wise exact formulas, large linear solves, autocorrelation scans,
sufficient statistics, block-coordinate fitting, Gauss-Newton, bilevel
objectives, and variable splitting.

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

## Large Linear Solves And Sketches

When exact normal equations are too large, choose the solve from the kind of
access the feature matrix supports.

- dense moderate-width data: QR, Cholesky, or eigendecomposition for ridge
  paths;
- tall out-of-core data: TSQR or communication-avoiding QR;
- generated features: LSQR or LSMR with only `X v` and `X^T u` products;
- sparse high-dimensional features: coordinate descent or block coordinate
  descent;
- `n << p`: dual solves or Woodbury identities;
- approximate screening: sketch-and-solve, then validate against exact held-out
  loss.

For ridge, iterative solvers can use the augmented operator:

```text
[ X              ] beta ~= [ y ]
[ sqrt(lambda) I]         [ 0 ]
```

Sketching is safest when the same sketch is applied to both the design and the
target:

```text
min_beta ||S X beta - S y||^2
```

Sketching only `X^T X` is a surrogate quadratic or preconditioner, not the
original least-squares problem. The quality criterion is usually spectral
approximation or leverage preservation, not simply matching total variance.

This also prevents a common Hessian mistake. For ordinary least squares, the
Hessian is exactly proportional to `X^T X`; the empirical gradient covariance is
`X^T D X`, with `D` determined by residuals. They coincide only under special
homoskedastic residual assumptions.

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

## Multi-Target Autoregressive Statistics

For a multivariate autoregressive fit, the reusable summaries are:

```text
G = X^T X
C = X^T Y
T = Y^T Y
```

Once those are accumulated, many outputs, horizons, and regularization settings
can be evaluated without another time scan. For a coefficient matrix `B`:

```text
RSS(B) = tr(T) - 2 tr(B^T C) + tr(B^T G B)
```

If `G = L L^T`, whitening once gives:

```text
Z = X L^-T
A = Z^T Y = L^-1 C
```

Reduced-rank variants then become SVD problems on the whitened cross-statistic
`A`. Ridge paths can reuse an eigendecomposition of `G`, and horizon-smoothing
penalties often produce Sylvester equations:

```text
G B + lambda B Omega = C
```

The penalty basis matters. Ridge in the whitened coordinate is a penalty on
`beta^T G beta`, not ordinary Euclidean ridge on the original coefficients.
This is acceptable when the model is explicitly prediction-space regularized,
but it should not be silently substituted for coefficient shrinkage.

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

## Block-Orthogonal And Partially Decoupled Designs

Some feature generators naturally produce blocks whose within-block Gram matrix
is diagonal, identity-like, or cheap to invert. In that case, the full solve
should expose the block structure instead of immediately densifying everything.

Useful backends include:

- block Cholesky when cross-block coupling is dense but stable;
- block QR or TSQR when rows are large and features are grouped;
- Woodbury updates when a small coupling block modifies an easy base solve;
- LSQR or conjugate gradients with a block-Jacobi preconditioner;
- block coordinate descent when only a few blocks matter for a candidate pass.

This is especially relevant for binned bases, orthogonal temporal bases,
per-asset blocks, and low-rank residual corrections. If validation gains are
small, the blockwise diagnostic is often more useful than the fitted parameter
matrix: it shows which feature families actually survive shrinkage.

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

The approximation drops the residual-weighted curvature term:

```text
H = J^T J + sum_i r_i Hessian(r_i)
```

So it is strongest when the residual is already small, the downstream map is
locally affine, or the model can be written as a convex loss composed with a
network output. In the latter case, generalized Gauss-Newton keeps a positive
semidefinite output-loss curvature:

```text
G = J_f^T H_loss J_f
```

Variable projection is the clean separable case: solve the linear block exactly
at each outer iterate, then optimize only the nonlinear block. This is the
right default when a large readout, basis coefficient, or asset map is linear
conditional on a smaller nonlinear parameter set.

## Layer-Wise Least Squares And IRLS

For a frozen linear layer followed by downstream map `g`, the layer update is:

```text
min_DeltaW sum_i ||r_i + J_i DeltaW x_i||^2
```

If `g` is affine, one Gauss-Newton step is the exact least-squares solution. If
`g` is ReLU-like and the update stays inside one activation region, the same is
true locally. The number of useful relinearizations is then tied to how many
activation boundaries the update crosses.

Smooth saturating nonlinearities need more care. A tiny Jacobian can make the
local regression say that the layer has no leverage even when a finite move in
latent space would help. For sigmoid-like heads, a better regression target is
often the inverse-link or clipped latent target:

```text
Delta a_i ~= logit(clip(y_i)) - a_i
```

Then solve a damped ridge regression in latent space and relinearize. This is
close in spirit to IRLS: choose a working response and weight from the current
nonlinear state, solve a weighted least-squares problem, and keep the step
inside a trust region.

Sequence gates add one more requirement: per-sample gradients still need the
backward recurrence. For a gated state

```text
h_t = (1 - alpha_t) h_{t-1} + alpha_t x_t
```

the state adjoint accumulates future influence through `(1 - alpha_{t+1})`.
The local gradients are then:

```text
dL / dx_t     = alpha_t * delta_h_t
dL / dalpha_t = (x_t - h_{t-1}) * delta_h_t
```

That recurrence is the line between a true row-local least-squares update and a
sequence update that only looks row-local after the adjoints have been scanned.

## Bilevel Data Weighting

Data weighting, per-feature ridge, and window-shape tuning are nested
objectives. A typical inner problem is weighted ridge:

```text
A(theta) beta = b(theta)
A = X^T W(theta) X + lambda I
b = X^T W(theta) y
```

The validation objective should be differentiated through the solve rather than
through repeated refits. With an adjoint solve:

```text
A q = X_val^T r_val
```

the hypergradient for a training weight has the form:

```text
dF / dw_i ~= -(x_i^T q) (y_i - x_i^T beta)
```

The sign is informative: a training row gains weight when its residual aligns
with validation leverage. This suggests a practical p12n recipe: parameterize
weights with a small number of smooth window or regime parameters, normalize
within each training window, keep a ridge floor, and validate the outer
objective on genuinely future data. Otherwise the outer loop becomes a powerful
way to overfit the validation split.

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
5. Block-orthogonal, dual, Woodbury, or iterative linear solvers.
6. Sketching or approximate solves for screening, followed by exact validation.
7. Gauss-Newton or Levenberg-Marquardt for nonlinear residual blocks.
8. Bilevel hypergradients when the thing being tuned changes the fit.
9. ADMM or lifting when splitting creates materially simpler subproblems.
10. Autodiff and generic first-order optimization when no structure remains.

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
- Which outer-loop tuning problems are worth treating as bilevel optimization
  rather than ordinary grid search?

## Source Map

- [LOOCV Error Efficient Computation](../../../ops/artifacts/chatgpt/6811ed55-0e14-8009-9c2a-f4b586b27278.md)
- [MSE Computation for Trailing Window](../../../ops/artifacts/chatgpt/69de5663-b9e0-83a1-aa8a-b0463403013b.md)
- [Branch - MSE Computation for Trailing Window](../../../ops/artifacts/chatgpt/69e1d90a-cb1c-839d-8acb-dbf91b58ee07.md)
- [Gradient computation for LSTQ](../../../ops/artifacts/chatgpt/694233c9-c518-8322-98cc-9a709eabb499.md)
- [Gauss-Newton Optimization Insights](../../../ops/artifacts/chatgpt/69ce12d1-750c-839e-9dbc-b85b63d0aa5b.md)
- [RNN Gauss-Newton Optimization](../../../ops/artifacts/chatgpt/69e75b42-c304-839b-809e-dcca2b2b4394.md)
- [ADMM Variable Splitting Tutorial](../../../ops/artifacts/chatgpt/69a1cc34-679c-8398-a265-a5cb0821fb1e.md)
- [Analytical Neural Network Training](../../../ops/artifacts/chatgpt/672ba4a5-0098-8009-bf41-8abd9ed48760.md)
- [Autoregressive Model Optimization](../../../ops/artifacts/chatgpt/69ef1db7-01f8-839e-a148-7f69cd23ab49.md)
- [Bi-level Linear Regression](../../../ops/artifacts/chatgpt/69cfcf41-b4b0-839d-bd3b-1a3c20a6e4d5.md)
- [Block Orthogonal LS Solvers](../../../ops/artifacts/chatgpt/68366f18-3ba4-8009-b87c-de2db683bc74.md)
- [Branch - Meta-Optimization for Data Weighting](../../../ops/artifacts/chatgpt/69cab2fa-d744-839a-877e-4de1169a753a.md)
- [Efficient Linear Regression Methods](../../../ops/artifacts/chatgpt/68462ac7-0d9c-8009-82de-bd0feb0b02a5.md)
- [Exploring Parameter Space Solutions](../../../ops/artifacts/chatgpt/672c38c2-8398-8009-8978-599861ac0f0c.md)
- [Gauss-Newton for Nonlinear Layers](../../../ops/artifacts/chatgpt/69e63991-5ef4-83a1-a9bb-cd1a23247290.md)
- [IRLS Initialization Tricks](../../../ops/artifacts/chatgpt/6a09778e-befc-83ec-9902-b880f91fea81.md)
- [Least Squares for NN](../../../ops/artifacts/chatgpt/68108d59-4888-8009-ba88-e1e9820a5728.md)
- [Least Squares Regression Estimation](../../../ops/artifacts/chatgpt/6810edb2-1740-8009-a05e-5137df01c05e.md)
- [Linear Regression Hessian Approximation](../../../ops/artifacts/chatgpt/69d09be4-a6e8-83a0-8ea9-6ef0cbf1c7f1.md)
- [Meta-Optimization for Data Weighting](../../../ops/artifacts/chatgpt/69ca7f5e-4848-839a-8937-dedf9e79b363.md)
- [Speeding Up Linear Regression](../../../ops/artifacts/chatgpt/674f4736-7960-8009-a075-e546853a02f9.md)
