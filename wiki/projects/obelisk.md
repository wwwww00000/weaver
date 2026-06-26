---
title: Obelisk
status: draft
page_type: project-hub
projects:
  - obelisk
categories:
  - quant
  - trading
  - market-making
source_bundles:
  - obelisk/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
created: 2026-06-27
updated: 2026-06-27
---

# Obelisk

Obelisk was an older crypto market-making and trading research project. It is
now in archive mode, but it contains durable ideas about edge estimation,
forecast realization, exit policy design, adaptive temporal models, and
diagnosing where trading simulations diverge from realized utility.

The most useful way to preserve Obelisk is not as a live strategy specification.
It should be treated as a research case study: a record of what mattered, what
failed, and which modeling ideas can be reused in newer trading work.

## Core Model

The project revolved around turning forecasts, fill probabilities, adverse
selection, inventory, and exit behavior into a trading decision. Several notes
frame the decision in utility terms rather than pure expected return:

- order or position return comes from inventory exposure plus filled quantity
- edge must account for both probability and adversity
- variance and covariance terms matter because fills interact with inventory
- exits can dominate whether a good entry signal is actually monetized

The clearest formulation appears in the trade-vs-forecast work: total return is
modeled as inventory forecast plus order return, and utility is expected return
minus a variance penalty. That makes the key failure mode visible: inaccurate
quadratic and covariance terms can overweight uncertain estimates even when
order returns look good.

Sources:
[trade-vs-forecast](../../ops/artifacts/obsidian/obelisk-trades-vs-forecast-and-optimization.md),
[edge function](../../ops/artifacts/obsidian/obelisk-edge-function.md),
[summary](../../ops/artifacts/obsidian/obelisk-summary.md)

## Main Lessons

### Entries Were Easier Than Exits

Several notes converge on the same diagnosis: entry logic had useful signal, but
exit behavior and horizon consistency were the fragile parts. In the fine-grid
experiments, changing exit handling and trade intervals had large effects, and
single-period horizons did not work cleanly. The residual note is even more
direct: entries were acceptable, but exits and risk-limit behavior were the
problem.

This suggests that future trading systems should evaluate entries and exits as
separate model components. A signal can be real and still fail as a strategy if
the exit policy prematurely cuts trajectories, penalizes exits during adverse
regimes, or spends too much time at position limits.

Sources:
[fine grid](../../ops/artifacts/obsidian/obelisk-fine-grid.md),
[residuals](../../ops/artifacts/obsidian/obelisk-residuals.md),
[trade study](../../ops/artifacts/obsidian/obelisk-trades-study.md),
[trade-vs-forecast](../../ops/artifacts/obsidian/obelisk-trades-vs-forecast-and-optimization.md)

### Forecast Realization Is a Separate Problem

Long-horizon conditional expectation was not enough. The notes repeatedly point
to a realization schedule: how a forecast, edge, or conditional return actually
materializes over future fills and exits. Without a low-dimensional realization
model, the state is effectively a vector of future returns and value-function
learning becomes impractical.

The reusable idea is to estimate forecast realization curves, then use them to
adjust expected order returns under existing fills, non-fills, and future exit
opportunities. This becomes a bridge between forecast research and policy
optimization.

Sources:
[conditional forecast realization](../../ops/artifacts/obsidian/obelisk-conditional-forecast-realization.md),
[summary](../../ops/artifacts/obsidian/obelisk-summary.md),
[signal research](../../ops/artifacts/obsidian/obelisk-signal-research-and-feature-engineering.md)

### Regime And Instrument Effects Were Central

Performance was concentrated in specific instruments and regimes. Rolling
regression and profitability-regime notes treat this as a universe-selection or
state-conditioning problem: identify when and where a basic trade is profitable,
then condition edge selection, feature use, or participation on that state.

The project also surfaced practical market-structure hazards:

- time-varying tick-size artifacts
- differences between instruments such as BUSD and USDT markets
- trade interval and sampling frequency effects
- capacity changes from sparsity, trade interval, and position limits

Sources:
[profitability regimes](../../ops/artifacts/obsidian/obelisk-profitability-regimes.md),
[rolling regression](../../ops/artifacts/obsidian/obelisk-rolling-regression.md),
[trade study](../../ops/artifacts/obsidian/obelisk-trades-study.md),
[opportunity set](../../ops/artifacts/obsidian/obelisk-opportunity-set.md)

## Reusable Research Threads

### Dynamic Edge And Volatility Estimation

The ChatGPT conversations attached to this bundle develop a family of dynamic
EMA and adaptive volatility ideas. The durable insight is that an EMA decay is a
learning rate, so adapting the decay turns a fixed estimator into a small online
learning system.

Promising variants:

- gated EMA updates, where large standardized surprises temporarily increase the
  variance update rate
- two-sided or smoothed gain rules, so volatility can rise quickly but release
  excess surprise mass after quiet periods
- online-gradient updates of the EMA decay, using future or outer loss rather
  than same-step loss
- multi-timescale ensembles or Kalman-style adaptive gains as more stable
  alternatives to fragile single-decay meta-gradients

This thread should probably migrate into p12n as a general temporal-modeling
primitive, while remaining linked to Obelisk as the historical motivation.

Sources:
[gated EMA families](../../ops/artifacts/chatgpt/6936a790-5b38-8321-8b75-eb1b44aa8da1.md),
[dynamic EMA decay](../../ops/artifacts/chatgpt/694277f3-e9f0-8324-a701-f326a5fb6f1c.md),
[EMA decay derivation](../../ops/artifacts/chatgpt/69442455-8f98-8321-9ba3-e9d4383c0e09.md),
[learning dynamic temporal models](../../ops/artifacts/chatgpt/69451015-6760-8323-b46f-b4acf7358496.md)

### Rolling And Conditional Feature Research

The signal research notes are less about a single winning feature and more about
a workflow:

- generate candidate features from feature importance, binned plots, time-series
  diagnostics, covariance heatmaps, and outlier or misclassification analysis
- test rolling regression, pooled and non-pooled variants, and rolling decision
  trees
- split market and residual components
- condition return effects on time of day, large moves, cross-sectional
  explainability, volume, and market-neutral variants

One repeated result is that rolling multivariate regression could outperform
full-sample regression for lagged-return features, but improvements in forecast
performance did not always translate into tradeable performance.

Sources:
[signal research](../../ops/artifacts/obsidian/obelisk-signal-research-and-feature-engineering.md),
[rolling regression](../../ops/artifacts/obsidian/obelisk-rolling-regression.md),
[covariance](../../ops/artifacts/obsidian/obelisk-covariance.md)

### Optimization Versus Trades

One unresolved axis is how to reconcile a trade-parameter view with an
optimization-constant view. Given a set of trade parameters, the project asked
what implied utility constants would reproduce the same solution. Conversely,
given a utility formulation, it asked why realized trades diverged from expected
utility.

This is a useful diagnostic pattern for future strategies: derive the implied
objective from the behavior of a working heuristic, then compare that objective
against realized utility and policy exits.

Sources:
[trade-vs-forecast](../../ops/artifacts/obsidian/obelisk-trades-vs-forecast-and-optimization.md),
[summary](../../ops/artifacts/obsidian/obelisk-summary.md)

## Open Questions To Preserve

- How should a strategy separate entry quality from exit quality?
- What is the minimal state needed for a useful forecast realization schedule?
- When should edge be scaled by volatility, and when does absolute distance from
  price matter more?
- Can rolling or dynamic models identify profitability regimes without simply
  overfitting recent PnL?
- Which adaptive temporal primitives from the dynamic EMA work are stable enough
  to become p12n building blocks?

## Source Map

Primary Obsidian sources:

- [conditional forecast realization](../../ops/artifacts/obsidian/obelisk-conditional-forecast-realization.md)
- [edge function](../../ops/artifacts/obsidian/obelisk-edge-function.md)
- [fine grid](../../ops/artifacts/obsidian/obelisk-fine-grid.md)
- [ideas](../../ops/artifacts/obsidian/obelisk-ideas.md)
- [market making](../../ops/artifacts/obsidian/obelisk-market-making.md)
- [opportunity set](../../ops/artifacts/obsidian/obelisk-opportunity-set.md)
- [profitability regimes](../../ops/artifacts/obsidian/obelisk-profitability-regimes.md)
- [residuals](../../ops/artifacts/obsidian/obelisk-residuals.md)
- [rolling regression](../../ops/artifacts/obsidian/obelisk-rolling-regression.md)
- [signal research and feature engineering](../../ops/artifacts/obsidian/obelisk-signal-research-and-feature-engineering.md)
- [summary](../../ops/artifacts/obsidian/obelisk-summary.md)
- [trades study](../../ops/artifacts/obsidian/obelisk-trades-study.md)
- [trades vs forecast and optimization](../../ops/artifacts/obsidian/obelisk-trades-vs-forecast-and-optimization.md)

ChatGPT sources:

- [gated EMA families](../../ops/artifacts/chatgpt/6936a790-5b38-8321-8b75-eb1b44aa8da1.md)
- [dynamic EMA decay insights](../../ops/artifacts/chatgpt/694277f3-e9f0-8324-a701-f326a5fb6f1c.md)
- [branch dynamic EMA decay insights](../../ops/artifacts/chatgpt/6942ca88-6cd8-8324-92fb-f22be8e6b689.md)
- [EMA decay update derivation](../../ops/artifacts/chatgpt/69442455-8f98-8321-9ba3-e9d4383c0e09.md)
- [learning dynamic temporal models](../../ops/artifacts/chatgpt/69451015-6760-8323-b46f-b4acf7358496.md)
