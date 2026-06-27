---
title: Temporal Evidence
status: draft
page_type: method-note
projects:
  - p12n
categories:
  - quant
  - regression
  - validation
  - time-series
  - machine-learning
source_bundles:
  - unassigned/quant
  - p12n/quant
  - quant/regression
  - quant/computation
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - projects/p12n
  - projects/p12n/temporal-returns-experiments
  - projects/p12n/n-linear-returns-models
  - topics/quant/regression-stability-and-validation
created: 2026-06-27
updated: 2026-06-27
---

# Temporal Evidence

Temporal evidence is a way to inspect whether a regression effect is stable over
time before committing to a particular cross-validation split, rolling window,
EMA treatment, or high-capacity model.

The companion validation page is
[Regression Stability And Validation](regression-stability-and-validation.md),
which covers deletion protocols, OOF features, and shrinkage choices.

The core idea is to treat regression evidence as a time series of sufficient
statistics. Instead of asking only whether `X` predicts `y` in aggregate, ask
whether the per-sample and per-block evidence points in compatible directions
over time.

## Whitened Evidence

Start with a linear or ridge regression geometry:

```text
C = X^T X + lambda I
```

Define whitened features and per-sample evidence:

```text
z_t = C^{-1/2} x_t
u_t = y_t z_t
```

Here `u_t` is the target-weighted, covariance-normalized evidence contributed by
sample `t`. Two samples support the same coefficient direction when their
evidence vectors have a positive inner product.

The sample-pair congruency matrix is:

```text
G_ij = u_i^T u_j
     = y_i y_j x_i^T C^{-1} x_j
```

In unregularized OLS, with hat matrix `H = X (X^T X)^{-1} X^T`, this is:

```text
G = diag(y) H diag(y)
G_ij = y_i H_ij y_j
```

That makes in-sample explained variation decomposable into sample-pair terms:

```text
y^T H y = sum_i sum_j G_ij
```

The diagonal captures self-leverage. The off-diagonal terms show which samples
support, oppose, or fail to interact with each other under the regression
geometry.

## Block Consistency

For a time block `A`, define:

```text
q_A = X_A^T y_A
```

The congruence between two blocks is:

```text
q_A^T C^{-1} q_B
```

This equals the sum of sample-pair congruencies between the two blocks:

```text
q_A^T C^{-1} q_B = sum_{i in A} sum_{j in B} G_ij
```

That gives a common language for:

- k-fold cross-validation;
- block deletion;
- rolling-window coefficient stability;
- temporal smoothing of `X^T y`;
- train-past-test-future validation;
- cross-fitted feature scoring.

The reusable diagnostic is cross-block alignment. A feature group with high
within-block evidence but weak or negative cross-block alignment is probably
fitting local noise. A feature group with repeated positive alignment across
blocks is more likely to contain a stable effect.

## ACF-Like Summaries

The full `n x n` congruency matrix is usually too large to inspect directly.
The compact time-series summary is a regression-evidence autocovariance:

```text
gamma(h) = mean_t G_{t,t+h}
         = mean_t y_t y_{t+h} x_t^T C^{-1} x_{t+h}
```

Equivalently:

```text
gamma(h) = mean_t u_t^T u_{t+h}
```

This is richer than the target ACF because target agreement only counts when
the predictor rows are aligned in the regression metric. It is richer than a
feature ACF because the feature alignment is target-weighted.

Useful plots:

- raw `gamma(h)` for evidence magnitude by lag;
- normalized evidence correlation for directional persistence;
- block-summed congruence heatmaps;
- cumulative positive-lag scores;
- within-block versus cross-block congruence ratios.

## Temporal Hat Smoothers

Temporal filtering of evidence induces a modified hat smoother.

Let a temporal kernel `K` build a coefficient/evidence state:

```text
m_t = sum_s K_ts u_s
```

The prediction at time `t` is:

```text
y_hat_t = z_t^T m_t
        = sum_s K_ts H_ts y_s
```

So the whole prediction vector is:

```text
y_hat = (K o H) y
```

where `o` is elementwise multiplication. This is not generally `H W y` for one
global sample-weight matrix `W`; each prediction row can have its own temporal
weights.

The original-risk improvement for a temporal smoother is:

```text
J(K) = 2 y^T (K o H) y - y^T (K o H)^T (K o H) y
```

For ordinary OLS, `K` is all ones, `K o H = H`, and the expression reduces to
`y^T H y` because `H` is symmetric and idempotent.

## Local Weighted OLS Boundary

For a single time `t`, the row `K_t:` can be viewed as the diagonal of a sample
weight matrix:

```text
W_t = diag(K_t:)
```

Then:

```text
y_hat_t = x_t^T (X^T X)^{-1} X^T W_t y
```

This is a globally normalized evidence filter. It is not full locally weighted
OLS unless the covariance normalization is also local:

```text
y_hat_t = x_t^T (X^T W_t X)^{-1} X^T W_t y
```

The cheaper temporal-evidence view assumes the predictor covariance is stable
enough that the drift worth studying is mostly in `X^T y`. That is often the
right first approximation in low-SNR financial settings, but it should be
checked by blockwise covariance diagnostics.

## Learnable Lag And EMA Kernels

For free lag weights, use:

```text
m_t = sum_l a_l u_{t-l}
```

Then:

```text
y_hat_t = sum_l a_l phi_{t,l}
phi_{t,l} = z_t^T u_{t-l}
```

Learning lag weights under the original prediction objective becomes an
ordinary ridge regression of `y_t` on the lag features `phi_{t,l}`.

For EMA evidence states:

```text
e_{m,t} = rho_m e_{m,t-1} + (1 - rho_m) u_{t-1}
psi_{t,m} = z_t^T e_{m,t}
y_hat_t = sum_m theta_m psi_{t,m}
```

This turns "which evidence timescale matters?" into a small regression problem
over a bank of causal temporal-evidence predictions.

## Efficient Computation

The full congruency matrix does not need to be materialized.

If feature dimension `p` is modest, compute `U = y * X C^{-1/2}` and use FFT
autocorrelations on the columns of `U`:

```text
gamma(h) = sum_k ACF(U[:, k])(h)
```

If `p` is large, sketch the evidence with random projections or aggregate by
feature group before computing lag summaries.

For trailing-window original-risk scores with large maximum lag and small `p`,
the useful trick is a prefix-sum plus FFT method. With:

```text
P_t = sum_{s < t} u_s
s_t(L) = z_t^T (P_t - P_{t-L})
```

the objective for all window lengths can be computed by expanding:

```text
B_L = sum_{t >= L} [z_t^T (P_t - P_{t-L})]^2
```

The expansion reduces to suffix sums and cross-correlations over `p` and `p^2`
derived sequences. This is attractive when `L_max` is large and `p` is small.
The special `p = 1` case reduces to a few scalar FFT correlations.

## Relationship To P12n

In p12n, temporal evidence is a diagnostic layer before n-linear or
sequence-model-like complexity.

Use it to ask:

- which lag families have stable evidence;
- whether short-lag, longer-lag, and round-minute effects are distinct;
- which effects survive block and walk-forward alignment checks;
- whether a temporal basis adds prediction-space value after residualization;
- whether local covariance drift is small enough for global whitening to be a
  useful approximation.

The temporal-evidence page is therefore a method companion to
[P12n Temporal Returns Experiments](../../projects/p12n/temporal-returns-experiments.md),
not a replacement for the project-specific experiment log.

## Open Questions

- Which normalization should be the default: global covariance, blockwise
  covariance, diagonal local covariance, or full local weighted OLS?
- How should block consistency be normalized to avoid selecting tiny but stable
  effects or large but unstable effects?
- Which evidence summaries are most useful as visual EDA artifacts?
- When should the method prefer explicit CV risk over ACF-like congruence
  summaries?
- How should multi-output returns be handled: per-target evidence, shared
  target geometry, or low-rank output factors?

## Source Map

- [Temporal Cross-Validation Unification](../../../ops/artifacts/chatgpt/69ec7a41-1fb0-839b-ad3c-7c0a3c6800c0.md)
- [p^2 Branch - Temporal Cross-Validation Unification](../../../ops/artifacts/chatgpt/69ef5eea-aed0-839c-88cb-b70b24e63a44.md)
- [Autocorrelation Based Regression](../../../ops/artifacts/chatgpt/69dc435b-3bd8-839b-9ae5-06021df8d193.md)
- [Sparse-lag AR Models](../../../ops/artifacts/chatgpt/6a0950af-853c-83ec-9b55-472bb305fd38.md)
- [Returns Model Design](../../../ops/artifacts/chatgpt/69eaa7ea-ca34-839c-a770-0c47bb62edba.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
