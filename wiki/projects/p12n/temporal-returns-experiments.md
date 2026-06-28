---
title: Temporal Returns Experiments
status: draft
page_type: research-thread
projects:
  - p12n
categories:
  - quant
  - trading
  - time-series
  - machine-learning
source_bundles:
  - p12n/quant
  - p12n/current priorities
  - p12n/project context
  - unassigned/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/p12n
related:
  - projects/p12n
  - projects/p12n/n-linear-returns-models
  - topics/quant/temporal-evidence
  - topics/quant/structured-return-models
  - topics/quant/regression-stability-and-validation
created: 2026-06-27
updated: 2026-06-28
---

# Temporal Returns Experiments

The temporal returns thread is the empirical side of p12n's forecasting work.
It asks which lagged return structures appear to carry stable predictive
content before deciding how much model complexity to spend on them.

This should stay closer to signal study than architecture design. The companion
[N-Linear Returns Models](n-linear-returns-models.md) page covers the structured
model family; this page covers what those models are trying to measure.

## Current Empirical Hints

The current weekly note records three main effects to investigate:

- strong short-lag predictiveness around lags `2-5`;
- demeaned longer-lag predictiveness around lags `5-10`;
- round-minute lag predictiveness.

Treat these as live hypotheses, not settled facts. In a low-SNR crypto returns
setting, the main failure mode is mistaking a correlated in-sample feature
family for a stable out-of-sample effect. The useful question is therefore not
whether a lag bucket can fit, but whether it adds durable prediction-space value
across folds, assets, and time windows.

## Research Questions

The first pass should separate several effects that can otherwise collapse into
one another:

- self-lag continuation or reversal;
- cross-sectional return structure;
- market or sector residual structure;
- round-minute and time-of-day periodicity;
- volatility- or liquidity-conditioned decay;
- forecast-horizon dependence.

The important distinction is between a temporal profile and the asset operator
attached to it. A short-lag impulse, an EMA-difference filter, and a
round-minute filter should each be evaluated with a simple self component first,
then with cross-sectional and low-rank components only if the simple version
survives validation.

## Experiment Axes

Temporal filters:

- raw lag impulses;
- fixed lag buckets;
- EMA and fast-minus-slow EMA profiles;
- smooth basis functions over lag;
- periodic or round-minute filters;
- time-of-day-specific lag profiles;
- learned decay schedules initialized from fixed bases.

Asset structure:

- diagonal self effects;
- market or cross-sectional residual effects;
- low-rank cross-asset factors;
- diagonal plus low-rank operators;
- sparse residual edges after structured residualization.

Targets:

- one-step or short-horizon returns;
- multi-horizon dense returns;
- horizon sums or utility-aligned return mixtures;
- market-residualized or cross-sectionally demeaned returns;
- order returns and fill-aware execution targets.

Validation:

- foldwise `X^T y` stability by lag family;
- walk-forward loss, IC, or utility-aligned metrics;
- prediction-space correlation between candidate filters;
- residualized incremental value over already selected filters;
- out-of-fold derived predictions before dependent fitting;
- robustness selection across time windows and symbols.

## Proposed Workflow

1. Build causal normalized returns, including volatility and time-of-day
   normalization where appropriate.
2. Compute foldwise temporal evidence objects: lagged cross moments,
   autocovariances, and target cross moments.
3. Score candidate temporal filters before fitting high-capacity asset maps.
4. Fit simple self effects, then diagonal-plus-low-rank asset structure.
5. Judge each candidate by validation lift and residualized incremental value.
6. Add sparse residual edges, nonlinear gates, or dynamic decay only after the
   broad temporal and asset structures are stable.

This workflow keeps the exploratory step cheap and explicit. It also prevents
the n-linear architecture from becoming a dumping ground for every weakly
positive lagged feature.

## Target Setup

The first experiment fork is target definition, not model architecture.

Candidate targets:

- raw forward returns, if directional exposure is allowed and common movement is
  part of the desired signal;
- cross-sectionally demeaned returns, if the target book is relative value or
  market-neutral within the traded universe;
- market or sector residualized returns, if common factors are nuisance
  variation;
- dense horizon returns, if the goal is to learn where predictability lives
  across the future path;
- summed or utility-weighted horizons, if the deployment rule only consumes a
  scalar forecast;
- fill-aware passive-order returns, if the trading action is an order tuple
  rather than a symbol-level directional position.

These should be compared as different supervised problems. A raw-return model
can look useful because it predicts a common move that the final portfolio will
hedge away. A residualized model can look weaker by ordinary `R^2` while being
better aligned with the trade.

## Temporal Evidence

The recurring implementation idea is to reduce lag exploration to reusable
statistics before fitting full models. For stationary ungated cases, lagged
return regression can be studied through Gram and cross-moment objects:

```text
S[l, j, m, k] = sum_t X[t, l, j] X[t, m, k]
R[l, j, i]    = sum_t X[t, l, j] Y[t, i]
```

These statistics make it possible to inspect lag profiles, project into temporal
bases, and solve many structured regressions without repeatedly scanning the
full time axis. They also give a common language for Toeplitz approximations,
autocorrelation diagnostics, and sparse-lag AR fits.

The caveat is that crypto returns are unlikely to be globally stationary. The
statistics should therefore be computed by fold, by window, and sometimes by
conditioning regime. The question is not whether the aggregate moment is large;
it is whether the evidence appears in enough independent blocks to trade.

The reusable method view lives in
[Temporal Evidence](../../topics/quant/temporal-evidence.md). That page covers
sample-level congruency, ACF-like evidence summaries, and the connection between
temporal evidence filters and hat-matrix smoothers.

Once a temporal basis appears stable, the reusable modeling layer is
[Structured Return Models](../../topics/quant/structured-return-models.md).
Validation protocol choices live in [Regression Stability And
Validation](../../topics/quant/regression-stability-and-validation.md).

## Forecast Realization

Lagged-return experiments should distinguish a rolling horizon from a fixed
endpoint. At time `t`, the dense targets might be:

```text
[r_{t+1}, r_{t+2}, ..., r_{t+H}]
```

After one bar realizes, the remaining forecast to the original endpoint is not
the same object as a new `H`-step rolling forecast. This matters when inspecting
multi-horizon coefficients or deciding whether the model should behave like a
convolutional lag filter or a recurrent state update.

A useful experiment is to track innovation updates:

```text
surprise_{t+1} = r_{t+1} - r_hat_{t+1|t}
r_hat_{t+2|t+1} = r_hat_{t+2|t} + gain * surprise_{t+1}
```

If a forecasted first step occurs as expected, the remaining cumulative forecast
to the same endpoint shrinks because one term is now realized, while the fixed
endpoint forecast should change only through surprise. This is a practical way
to separate "prediction was realized" from "the state has new information."

## Basis And Horizon Tests

For the current lag study, the high-value tests are:

- direct summed-horizon regression versus dense multi-horizon regression summed
  after prediction;
- horizon-head recombination selected only on validation data;
- projection of multi-horizon predictions onto the horizon-sum direction;
- separate short-lag, medium-lag, and round-minute basis families, then
  residualized incremental tests;
- Toeplitz-projected or tapered covariance estimates as a low-variance
  stationary baseline;
- frequency or DCT views of lag filters to detect high-frequency mean reversion
  versus slower persistence.

The goal is not to prove that the world is stationary. It is to get a cheap
baseline for what stationary second-order structure would imply, then inspect
where live crypto data departs from it.

## Round-Minute Effects

Round-minute lag predictiveness is interesting because it is structured rather
than merely "recent." At a five-second sampling rate, one minute corresponds to
twelve bars, so a round-minute effect should appear as a periodic lag family
rather than as a generic short-memory decay.

That suggests testing round-minute filters as their own temporal basis family:

```text
psi_round(l) = basis functions concentrated near l = 12, 24, 36, ...
```

This should be compared against smooth decay filters and short-lag impulses in
prediction space. If a round-minute basis only recreates a short-lag or EMA
prediction, it is not a separate source of signal.

## Dynamic Decay

Dynamic decay ideas belong here as hypotheses about signal persistence. The
weekly note points at decay schedules that change with current features or recent
state. A pragmatic first version is not a fully learned recurrence; it is a
fixed bank of decay profiles with a small gated mixer.

The stronger versions can come later:

- learn decay weights with Gauss-Newton-like updates;
- condition decay on cumulative time or volatility features;
- visualize empirical decay schedules by sign and magnitude;
- treat an n-linear atom as a reusable cell inside a hierarchical fit.

The design rule is the same as for other temporal features: first show that a
fixed decay family has stable incremental value, then spend complexity on making
the decay adaptive.

## Execution-Aware Targets

P12n ultimately trades actions, not abstract return labels. For passive
execution, the prediction tuple can expand from:

```text
(time, symbol)
```

to:

```text
(time, symbol, side, edge)
```

The useful decomposition is:

- probability of fill within the decision interval;
- conditional return given fill;
- expected action value after fees, spread, and adverse selection;
- liquidity or edge normalization that makes symbols comparable.

This should not replace the return signal study, but it should constrain which
return targets survive. A forecast that predicts mid returns but has no edge
after passive fill probability and conditional fill return is not an execution
signal.

One reasonable first pass is to treat normalized edge, side, symbol, volatility,
spread, and liquidity as features in a shared model, then compare it with
edge-bucketed models only if the shared model misses obvious monotone or
threshold structure.

## Relationship To N-Linear Models

The temporal returns page answers:

```text
Which lag, basis, and horizon structures seem to contain signal?
```

The n-linear page answers:

```text
How should those structures be parameterized and fit once selected?
```

In practice the loop is iterative. Temporal evidence proposes basis families;
n-linear models test whether those basis families still matter once asset
structure, residualization, and validation are handled correctly.

## Open Questions

- Which of the short-lag, longer-lag, and round-minute effects survive
  walk-forward validation?
- Is longer-lag predictiveness mainly self effect, cross-sectional effect, or
  market-residual effect?
- Do time-of-day and round-minute features explain the same variation?
- How should horizon weights be selected without leaking validation information?
- Can Toeplitz or autocorrelation approximations make the exploratory stage cheap
  enough to run routinely?
- When is adaptive decay worth the extra estimation risk?

## Source Map

- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
- [p12n overview](../../../ops/artifacts/obsidian/p12n-overview.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
- [Returns Model Design](../../../ops/artifacts/chatgpt/69eaa7ea-ca34-839c-a770-0c47bb62edba.md)
- [Sparse-lag AR Models](../../../ops/artifacts/chatgpt/6a0950af-853c-83ec-9b55-472bb305fd38.md)
- [Temporal Model Design](../../../ops/artifacts/chatgpt/6a08121e-703c-83ec-b7e5-3eac501ba732.md)
- [Branch - Lagged Returns Prediction](../../../ops/artifacts/chatgpt/69e73c9f-6c8c-839e-bcc2-5e6695180ba8.md)
- [Lagged Returns Prediction](../../../ops/artifacts/chatgpt/69e23cd4-d9bc-839c-b2e9-63e62b275d18.md)
- [Impulse Forecasting Explanation](../../../ops/artifacts/chatgpt/69cccd65-5520-839f-aecd-e5420a505bc7.md)
- [Pooling Branch - Impulse Forecasting Explanation](../../../ops/artifacts/chatgpt/69cfd775-8a8c-839d-8746-8e40e2b149a3.md)
- [Market Making PnL Estimate](../../../ops/artifacts/chatgpt/686d210c-45d8-8009-b076-ed3216006e96.md)
- [Predicting Asset Returns](../../../ops/artifacts/chatgpt/69983c39-aac0-839a-a0a9-c23e8d7d6aab.md)
- [Predicting Returns and Fills](../../../ops/artifacts/chatgpt/6710eaf9-ec70-8009-b573-28274dc3d163.md)
- [Returns Forecasting with Regression](../../../ops/artifacts/chatgpt/69983e0f-e664-839b-88fb-408fd5249246.md)
