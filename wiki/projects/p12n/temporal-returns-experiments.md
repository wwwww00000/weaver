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
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/p12n
related:
  - projects/p12n
  - projects/p12n/n-linear-returns-models
  - topics/quant/temporal-evidence
  - topics/quant/structured-return-models
  - topics/quant/regression-stability-and-validation
created: 2026-06-27
updated: 2026-06-27
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
