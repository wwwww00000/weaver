---
title: Structured Return Models
status: draft
page_type: method-note
projects:
  - p12n
categories:
  - quant
  - trading
  - machine-learning
  - time-series
  - regression
source_bundles:
  - p12n/quant
  - p12n/uncategorized
  - unassigned/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - projects/p12n/n-linear-returns-models
  - projects/p12n/temporal-returns-experiments
  - topics/quant/temporal-evidence
  - topics/quant/optimization-and-computation
created: 2026-06-27
updated: 2026-06-28
---

# Structured Return Models

Structured return models are a family of linear or conditionally linear models
for predicting target returns from lagged multi-asset returns without fitting a
fully free asset-by-lag-by-target coefficient tensor.

The motivating problem is dimensionality and correlation. A naive model gives
each target asset a free coefficient for every predictor asset and every lag:

```text
y_hat[t, i] = sum_j sum_l W[i, j, l] x[t - l, j]
```

That formulation is too flexible for low-SNR return data. It can fit local
noise, absorb redundant predictors, and make validation behavior hard to
interpret. The useful pattern is to constrain `W` before estimation.

## Stationary Baseline

For a single stationary return series, the population linear regression from a
past lag window to future returns is already structured. With:

```text
x_t = [r_t, r_{t-1}, ..., r_{t-p+1}]
y_t = [r_{t+1}, ..., r_{t+H}]
```

the predictor covariance is Toeplitz and the predictor-target covariance is a
shifted autocovariance surface:

```text
Sigma_xx[i, j] = gamma(|i - j|)
Sigma_xy[i, h] = gamma(h + i)
B = Sigma_xx^{-1} Sigma_xy
```

This is the Wiener-Hopf or Yule-Walker view of the return model. It says that
some banded or diagonal-looking structure in multi-horizon coefficient matrices
is not accidental. It is the regression form of shift-invariant autocovariance.

The caveat is that the clean Toeplitz object is the covariance surface, not
necessarily the fitted coefficient matrix. The inverse covariance partials out
competing lags, so a shared lag relation can appear in different coefficients
after being screened by a different information basis.

## Base Atom

The first useful atom separates temporal structure from asset structure:

```text
W[i, j, l] = B[i, j] a[l]
y_hat[t] = B z[t]
z[t, j] = sum_l a[l] x[t - l, j]
```

Here `a` is a lag filter and `B` is an asset map. The preferred asset map is
usually not fully dense:

```text
B = D + U V^T
```

`D` captures diagonal self effects. `U V^T` captures a small number of
cross-asset factors. This diagonal-plus-low-rank form is often the right first
default because own-lag behavior and broad market structure should not compete
inside one dense matrix.

## Additive Atoms

One separable atom is rarely enough. The general pattern is an additive
dictionary:

```text
y_hat[t] = sum_r g_r[t] B_r z_r[t]
z_r[t] = sum_l a_r[l] x[t - l]
B_r = D_r + U_r V_r^T
```

The scalar or vector gate `g_r[t]` can encode time of day, volatility regime,
liquidity regime, or a slowly varying factor strength. The core restriction is
still that each component has a legible temporal filter and a legible
cross-sectional map.

This formulation turns model growth into a residual-fitting question:

```text
Does the next atom explain validation-stable residual signal not already
spanned by the existing atom predictions?
```

## Temporal Basis Bank

A practical route is to avoid learning every lag profile from scratch. Define a
bank of fixed or lightly parameterized temporal basis filters:

```text
z_b[t] = sum_l psi_b[l] x[t - l]
y_hat[t] = sum_b B_b z_b[t]
B_b = D_b + U_b V_b^T
```

Useful basis families include:

- raw short-lag impulses
- lag buckets
- EMA traces
- fast-minus-slow EMA differences
- smooth bumps or splines over lag
- periodic or round-minute lag modes
- time-of-day-specific lag profiles

Fixed bases make the diagnostic clearer. Each temporal view can be evaluated
alone, jointly, and after residualization against the other basis predictions.
This matters because different lag filters may be distinct in parameter space
but highly correlated in prediction space.

## Realization And State

There are two different temporal objects that should not be conflated:

- the target kernel, which defines what future returns are being aggregated;
- the predictor realization, which defines how past signal remains available to
  future predictions.

For example, a forward discounted target can satisfy:

```text
z_t = y_t + lambda z_{t+1}
```

but that identity does not make a model remember a past input impulse. Memory
comes from the predictor state:

```text
s_t = rho s_{t-1} + x_t
y_hat_t = c s_t
```

If a recent signal should keep affecting forecasts after the original event, the
model needs lagged inputs, EMA states, or another recurrent realization. The
target smoothing alone does not provide that state.

This matters for multi-horizon returns. The forecast for a fixed endpoint and
the forecast for a rolling horizon are different objects. When a one-step return
realizes as expected, the remaining cumulative forecast to the same endpoint
shrinks because one future term is now known. The endpoint forecast itself is
updated only by the innovation in the new observation.

## Amortized Local Regression

A useful bridge between structured return models and sequence-model analogies is
to treat a fixed temporal mask as a memory operator. Let:

```text
c_t = sum_s L[t, s] y_s x_s
y_hat_t = x_t^T M c_t
```

With a causal all-ones mask, `c_t` is a prefix target-feature memory. With a
sliding window, it is a trailing `X^T y` state. With exponential weights, it is
an EMA memory. Once `c_t` is built, fitting the fused query-key matrix `M` is
ordinary least squares on lifted features:

```text
phi_t = c_t kron x_t
```

This is an amortized version of sliding-window regression. Local OLS would use:

```text
beta_t = G_t^{-1} c_t
```

where `G_t` is the local feature Gram. The amortized model learns one global
operator:

```text
beta_t = M c_t
```

It is attractive when local covariance geometry is stable enough that a shared
preconditioner works, while the local target-feature cross moment carries the
interesting drift.

## Additional Axes

The same structure can extend beyond target asset, predictor asset, and lag.
Common additional axes are:

- feature type
- horizon
- time of day
- volatility or liquidity regime
- market direction
- sector, cluster, or asset embedding

A compact tensor factorization is:

```text
W[i, j, l, m] = sum_r u_r[i] v_r[j] a_r[l] c_r[m]
```

where `m` indexes an extra mode such as regime, horizon, or feature family. In
practice, diagonal self effects should usually stay outside the low-rank tensor
so they do not need to be rediscovered through shared factors.

This page uses "low rank" in the practical tensor-regression sense. Candidate
coefficient structures include:

- CP factors, where each atom is a product of one vector per mode;
- Tucker factors, where each mode has its own rank and a small interaction core;
- tensor-train factors when there are many small modes;
- sparse plus low-rank decompositions when a few edges coexist with broad
  shared factors.

For return models, the natural modes are target asset, predictor asset, lag,
horizon, feature family, and regime. The reason to use these structures is not
only computational. They make it possible to ask whether a pattern is a
diagonal self effect, a cross-asset factor, a horizon profile, or a regime gate
instead of treating all coefficients as unrelated.

An asset-embedding variant is:

```text
W[i, j, l] = e_i^T C_l e_j + 1[i = j] d[i, l]
```

This is useful when asset identity should be compressed into a learned or
hand-built embedding rather than represented as a fully free matrix.

## Linear Attention View

The model can also be read as a constrained linear-attention layer. Predictor
tokens are lagged source-asset observations. Target assets provide queries:

```text
W[i, j, l, t] = q_i[t]^T k_j[l, t]
y_hat[t, i] = q_i[t]^T sum_j sum_l k_j[l, t] x[t - l, j]
```

The attention view is useful when thinking about dynamic keys, queries, gates,
and recurrent summaries. It is not automatically a better estimator. A robust
compromise is:

- keep values close to raw scalar returns;
- keep an explicit diagonal self path;
- use static or slowly varying query/key features first;
- gate latent factor strengths before making every coefficient dynamic.

This gives some of the expressive shape of sequence models while preserving a
regression-like fitting problem.

## Fitting

These models are usually conditionally linear rather than globally linear. With
one block frozen, another block often has a ridge, reduced-rank, or
least-squares-like update.

A practical fitting loop:

1. Choose or fit a temporal basis view `z_b`.
2. Fit diagonal self effects for that view.
3. Fit low-rank cross-asset residual structure by reduced-rank regression or
   SVD-like updates.
4. Refit scalar weights over frozen atom predictions.
5. Residualize and test whether another atom or basis has incremental
   validation value.

For learned lag filters, alternate between asset and lag blocks:

```text
fit asset map B given lag filter a
fit lag filter a given asset map B
normalize scales
repeat
```

Scale normalization is required because products like `B a` are invariant under
opposite rescalings of the two factors.

The computational counterpart is
[Optimization And Computation](optimization-and-computation.md), especially the
sections on sufficient statistics and block-coordinate fitting.

## Diagnostics

Good diagnostics are prediction-space diagnostics.

Useful checks:

- validation lift for each atom or basis;
- prediction correlation between atoms;
- incremental lift after residualizing against existing predictions;
- stability of lag profiles across windows;
- stability of diagonal and low-rank asset effects across windows;
- separate evaluation of diagonal-only, low-rank-only, and
  diagonal-plus-low-rank components;
- horizon and time-of-day robustness.

The first atom may dominate in low-SNR data. That is not a failure by itself.
Later atoms should be kept only when they add stable validation signal.

## Target Alignment

If the scored objective is the sum of future returns, the direct population
linear target is:

```text
s_t = 1^T y_t
b_sum = Sigma_xx^{-1} Sigma_xy 1
```

The full multi-target coefficient matrix is still useful for diagnostics,
regularization, and horizon-shape discovery, but modes orthogonal to the horizon
sum direction do not directly help the summed-return score. A practical
compromise is to fit multi-target or low-rank horizon structure, then always
evaluate the projection that will actually be traded.

For multi-asset settings, target alignment also includes common-factor handling.
Raw returns, cross-sectionally demeaned returns, market-residualized returns,
and fill-aware execution returns are different supervised problems. The model
structure should follow the target that matches the intended book: directional,
relative value, hedged alpha, or passive-execution payoff.

## Relationship To P12n

[N-Linear Returns Models](../../projects/p12n/n-linear-returns-models.md) is
the project-facing page for the active p12n model family. This page is the
method-facing version: coefficient tensor structure, basis design, fitting
patterns, and diagnostics that can outlive the current implementation.

[Temporal Evidence](temporal-evidence.md) supplies a complementary diagnostic
view. It asks where lagged samples agree or conflict in a whitened regression
geometry before committing to a particular structured return model.

## Open Questions

- Which temporal basis bank should be the default first pass?
- How much of the signal is diagonal self effect versus cross-asset low rank?
- Should time of day enter through lag filters, scalar gates, or factor-strength
  gates?
- When does a dynamic query/key formulation beat fixed basis plus structured
  regression?
- Which atom-selection rule best predicts future validation stability?

## Source Map

- [Returns Model Design](../../../ops/artifacts/chatgpt/69eaa7ea-ca34-839c-a770-0c47bb62edba.md)
- [Bilinear Model Generalization](../../../ops/artifacts/chatgpt/69fb6b98-5d84-839f-a5f8-fef0e1b96345.md)
- [Basis Function Branch - Bilinear Model Generalization](../../../ops/artifacts/chatgpt/6a081747-34fc-83ec-9431-0075044dd952.md)
- [Framework Branch - Bilinear Model Generalization](../../../ops/artifacts/chatgpt/6a14f60f-5eb4-83ec-b398-eaf71c6e4763.md)
- [Linear Attention Branch - Bilinear Model Generalization](../../../ops/artifacts/chatgpt/69fb6ffd-cdc0-83a0-b8eb-d4d5437aad8a.md)
- [N-linear model fitting](../../../ops/artifacts/chatgpt/6a1bd091-cafc-83ec-9c0d-5bfdf73d5c93.md)
- [Solving for Beta](../../../ops/artifacts/chatgpt/6a1718c0-976c-83ec-83df-0e71575a25a0.md)
- [Sparse-lag AR Models](../../../ops/artifacts/chatgpt/6a0950af-853c-83ec-9b55-472bb305fd38.md)
- [Temporal Model Design](../../../ops/artifacts/chatgpt/6a08121e-703c-83ec-b7e5-3eac501ba732.md)
- [Autocorrelation Based Regression](../../../ops/artifacts/chatgpt/69dc435b-3bd8-839b-9ae5-06021df8d193.md)
- [Bilinear Autoregressive LSQ](../../../ops/artifacts/chatgpt/6a200ef7-f71c-83ec-8c98-cceb472c5baa.md)
- [Comparing Financial Return Models](../../../ops/artifacts/chatgpt/67d307e8-d668-8009-8008-4a8eb7d5ba55.md)
- [Hierarchical AR Models](../../../ops/artifacts/chatgpt/69dc4552-db34-839e-8d02-50ff207486f8.md)
- [Impulse Forecasting Explanation](../../../ops/artifacts/chatgpt/69cccd65-5520-839f-aecd-e5420a505bc7.md)
- [Low-Rank Tensor Regression](../../../ops/artifacts/chatgpt/68639f33-2858-8009-8a85-351d48135a5a.md)
- [Returns Forecasting with Regression](../../../ops/artifacts/chatgpt/69983e0f-e664-839b-88fb-408fd5249246.md)
