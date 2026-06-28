---
title: N-Linear Returns Models
status: draft
page_type: research-thread
projects:
  - p12n
categories:
  - quant
  - trading
  - machine-learning
  - time-series
source_bundles:
  - p12n/quant
  - p12n/math
  - p12n/uncategorized
  - unassigned/math
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/p12n
related:
  - projects/p12n
  - projects/obelisk/dynamic-ema-decay
  - topics/quant/structured-return-models
created: 2026-06-27
updated: 2026-06-27
---

# N-Linear Returns Models

The n-linear returns thread is about building an expressive but controlled model
class for predicting multi-asset crypto returns from lagged multi-asset returns.
The reusable method counterpart is
[Structured Return Models](../../topics/quant/structured-return-models.md).

The motivating failure mode is straightforward: a naive regression over all
assets, all lags, and all target assets is too large and too correlated. It can
absorb nuisance features, improve in-sample fit, and still fail to generalize.
The p12n direction is therefore to impose structure before estimation.

## Core Model

Let `x[t, l, j]` be predictor asset `j` at lag `l`, and let `y[t, i]` be the
target return for asset `i`. The unrestricted linear model uses a coefficient
tensor:

```text
y[t, i] ~= sum_l sum_j W[i, j, l] x[t, l, j]
```

The first useful restriction is separability:

```text
W[i, j, l] = a[l] B[i, j]
```

Here `a` is a shared lag profile and `B` is an asset mixer. The preferred asset
mixer is not fully dense by default:

```text
B = diagonal self effect + low-rank cross-asset effect
```

In matrix terms:

```text
B = D + U V^T
```

This says: first form a lag-filtered return vector, then let each asset receive
a self effect plus a small number of shared cross-sectional factors. That
captures useful phenomena like own-lag continuation, broad cross-asset effects,
and medium-term reversion without giving every asset-lag-target triple a free
coefficient.

## Why N-Linear

The basic bilinear model has two coefficient factors: lag and asset mixing. The
n-linear version adds more axes while keeping each axis structured:

- lag or temporal basis
- predictor asset
- target asset
- time-of-day or round-minute phase
- volatility or liquidity regime
- horizon, feature family, or component index

A practical formulation is:

```text
y_hat[t, i] =
  sum_r O_r[t, i]
    sum_j B_r[i, j]
      sum_l A_r[t, l, j] x[t, l, j]
```

The implementation-friendly mental model is staged:

```text
lag/input stage -> asset bridge -> output modulation
```

This is not ordinary matrix multiplication with a fragile ordering constraint.
It is a tensor contraction. When the factors separate cleanly, lag and asset
summations can be evaluated in different orders. Order becomes semantically
important only when a nonlinearity, normalization, state-dependent gate, or
softmax-like operation is inserted between stages.

## Temporal Bases

The strongest current design idea is to stop asking ALS to discover all temporal
diversity from scratch. Instead, give the model an interpretable lag-basis bank
and fit the asset structure conditional on each temporal view.

Useful basis families include:

- raw short lag impulses
- fixed lag buckets
- EMA profiles
- fast-minus-slow EMA differences
- smooth spline or bump functions over lag
- periodic or round-minute modes
- time-of-day-specific lag profiles

This changes the model from a free lag vector per atom into:

```text
z_b[t, j] = sum_l psi_b[l] x[t, l, j]
y_hat[t] = sum_b B_b z_b[t]
```

Each temporal basis gets its own asset map, such as:

```text
B_b = D_b + U_b V_b^T
```

This creates a cleaner diagnostic question: which temporal profiles have stable
incremental value, and what asset structure do they support?

## Fitting

There is no single global least-squares solution once the lag profile and asset
factors multiply each other. The useful property is conditional linearity. With
all other blocks frozen, each block has a closed-form or least-squares-like
update.

For a single atom:

```text
Y_hat = Z(a) [diag(d) + p q^T]
Z(a) = sum_l a[l] X_l
```

Given the lag filter `a`, the diagonal self coefficients and rank-one
cross-asset factors can be fit by target-wise ridge regressions and rank-one
reduced-rank updates. Given the asset operator, the lag coefficients can be fit
by ridge regression over effective lag features. A lag basis `a = H alpha`
simply projects the lag normal equations into basis coordinates.

The recurring update pattern is:

```text
fit lag block -> fit asset block -> normalize scales -> repeat
```

Scale normalization matters because the model is invariant under transformations
like:

```text
a -> c a
B -> B / c
```

and, in low-rank factors:

```text
p -> c p
q -> q / c
```

Without a convention, parameters can drift even when predictions are stable.

## Sufficient Statistics

For ungated, time-stationary pieces, many ALS updates can be computed from
precomputed sufficient statistics:

```text
S[l, j, m, k] = sum_t X[t, l, j] X[t, m, k]
R[l, j, i]    = sum_t X[t, l, j] Y[t, i]
```

These are the lag-asset Gram matrix and lag-asset-to-target cross moment. They
let the lag update and dense asset update avoid rescanning time.

This trick has limits. Time-varying output gates, input gates, regime weights,
or sample-specific modulation turn the required statistics into weighted
versions. If the weights change during fitting, the implementation needs either
chunked recomputation, a basis-weighted statistics bank, or an approximation.

The likely practical split is:

- use sufficient-statistics backends for static lag and asset ALS;
- use chunked normal-equation accumulation for gated or time-varying pieces.

## Linear Attention View

Many of these models can be written in a linear-attention form:

```text
z[t] = sum_j sum_l k[j, l] x[t, l, j]
y_hat[t, i] = q[i]^T z[t]
```

The useful question is not whether this representation exists. Many
representations are nearly tautological if arbitrary value maps are allowed. The
useful question is which representation gives good learning dynamics.

The preferred gauge is:

- keys encode source asset and lag structure;
- queries encode target-asset exposure;
- values stay close to raw scalar returns;
- diagonal self effects are handled explicitly;
- low-rank cross effects pass through a shared latent factor bottleneck;
- optional state or time variation gates latent factor strengths rather than
  making every query and key fully dynamic.

This keeps pressure on the model to learn reusable predictor-lag factors instead
of hiding the whole target-space map in a value projection.

## Amortized Local Regression Prototype

A useful p12n prototype fuses query and key maps into one matrix:

```text
M = W_q W_k^T
y_hat = (L .* X M X^T) y
```

where `L` is a fixed causal mask and `.*` denotes elementwise multiplication.
For scalar targets this becomes:

```text
c_t = sum_s L[t, s] y_s x_s
y_hat_t = x_t^T M c_t
```

The mask controls the memory:

- full causal prefix: `c_t = sum_{s < t} y_s x_s`;
- sliding window: `c_t = sum_{l=1}^w y_{t-l} x_{t-l}`;
- exponential decay: `c_{t+1} = rho c_t + y_t x_t`;
- general lag kernel: filter each coordinate of `y_t x_t` by the kernel.

Once `c_t` is built, the fused problem is ordinary least squares on the lifted
feature `c_t kron x_t`. The original query/key factorization is a low-rank
constraint on `M`.

This resembles sliding-window regression but is not the same estimator. A local
windowed ridge fit would compute:

```text
G_t = X_w^T X_w
c_t = X_w^T y_w
beta_t = (G_t + lambda I)^-1 c_t
y_hat_t = x_t^T beta_t
```

The fused attention-like prototype instead learns one global operator:

```text
beta_t = M c_t
```

So `M` is an amortized inverse-covariance or preconditioner. This is attractive
when local Gram structure is stable enough to share. If local covariance changes
materially, the model needs either access to `G_t`, regime-specific operators,
or a more explicit streaming-regression backend.

The learned `M` should not be expected to be symmetric. Current features
`x_t` and historical memory `c_t` play different roles. Symmetry only becomes
natural in same-vector quadratic forms such as `x_t^T W x_t`, where the
skew-symmetric part is unidentifiable.

## Diagnostics

The first atom or first temporal profile may dominate. In low-SNR returns, that
is not surprising and should be treated as information rather than failure.

Useful diagnostics:

- evaluate validation lift, not just training loss;
- refit scalar weights over frozen atoms;
- residualize a later atom's prediction against earlier atom predictions before
  judging incremental value;
- compare prediction-space correlation between temporal bases;
- test stability of lag profiles, self effects, and low-rank factors across
  windows;
- prefer broad, stable structure before sparse pairwise residual effects.

The core question for any additional atom or basis is:

```text
Does this add stable validation signal not already spanned by the existing
predictions?
```

## Open Questions

- Should p12n start with fixed temporal bases, sparse mixtures of bases, or fully
  learned lag vectors?
- How much of the signal is captured by the first structured atom?
- Which temporal bases are genuinely distinct in prediction space after
  accounting for autocorrelation?
- Should time-of-day enter first as basis-specific lag profiles, scalar atom
  gates, or latent factor gates?
- Which backend should be primary for implementation: precomputed static
  sufficient statistics, chunked normal equations, or autodiff-backed
  Gauss-Newton fallbacks?

## Source Map

- [Returns Model Design](../../../ops/artifacts/chatgpt/69eaa7ea-ca34-839c-a770-0c47bb62edba.md)
- [Bilinear Model Generalization](../../../ops/artifacts/chatgpt/69fb6b98-5d84-839f-a5f8-fef0e1b96345.md)
- [Basis Function Branch - Bilinear Model Generalization](../../../ops/artifacts/chatgpt/6a081747-34fc-83ec-9431-0075044dd952.md)
- [Bilinear Autoregressive LSQ](../../../ops/artifacts/chatgpt/6a200ef7-f71c-83ec-8c98-cceb472c5baa.md)
- [Framework Branch - Bilinear Model Generalization](../../../ops/artifacts/chatgpt/6a14f60f-5eb4-83ec-b398-eaf71c6e4763.md)
- [Linear Attention Branch - Bilinear Model Generalization](../../../ops/artifacts/chatgpt/69fb6ffd-cdc0-83a0-b8eb-d4d5437aad8a.md)
- [Low-Rank Tensor Regression](../../../ops/artifacts/chatgpt/68639f33-2858-8009-8a85-351d48135a5a.md)
- [N-linear model fitting](../../../ops/artifacts/chatgpt/6a1bd091-cafc-83ec-9c0d-5bfdf73d5c93.md)
- [Solving for Beta](../../../ops/artifacts/chatgpt/6a1718c0-976c-83ec-83df-0e71575a25a0.md)
- [Sparse-lag AR Models](../../../ops/artifacts/chatgpt/6a0950af-853c-83ec-9b55-472bb305fd38.md)
- [Temporal Model Design](../../../ops/artifacts/chatgpt/6a08121e-703c-83ec-b7e5-3eac501ba732.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
