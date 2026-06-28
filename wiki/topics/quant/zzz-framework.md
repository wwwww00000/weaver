---
title: Zzz's Framework
status: draft
page_type: reference-note
categories:
  - quant
  - trading
  - forecasting
  - machine-learning
source_bundles:
  - unassigned/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - projects/p12n
  - topics/quant/temporal-evidence
  - topics/quant/regression-stability-and-validation
  - topics/quant/structured-return-models
  - topics/quant/tabular-nonlinearities
created: 2026-06-28
updated: 2026-06-28
---

# Zzz's Framework

This page captures a terse note about zzz's, also known as sheriffpony's,
approach to quant trading. The source is too compact to treat as a complete
system description, but it is useful as a reference architecture: many calibrated
signals, organized into thematic forecasts, combined on a short realization
grid.

## Source-Grounded Summary

The raw note gives six concrete points:

- the system has tens of thousands of signals;
- there are about 11 forecasts or thematic models;
- each thematic model has thousands of signals;
- some forecasts combine signals nonlinearly, including interaction terms in
  regressions;
- rolling ridge and lasso regressions expect signals to be fairly stable in
  time;
- component signals have their own shorter-period internal calibrations;
- forecasts are frozen, with hyperparameters that do not change much;
- signals are combined on a 5-second realization grid.

The important shape is a two-timescale architecture. Component signals can have
shorter calibration loops, but the forecast objects are comparatively stable and
frozen. The fast-moving layer is not the whole forecast specification; it is the
calibration of inputs feeding a stable forecast bank.

## Interpreted Architecture

A plausible system decomposition is:

1. Signal factory: produce many simple, typed component signals from market,
   order-book, cross-asset, time, and execution context.
2. Component calibration: normalize, winsorize, decay, and recalibrate each
   signal over shorter windows so that the forecast layer receives stable units.
3. Thematic forecast models: group signals into about a dozen forecast families,
   each representing a theme such as short-horizon flow, cross-sectional move,
   volatility/liquidity state, microstructure pressure, or event behavior.
4. Nonlinear theme construction: allow interactions inside a theme when there is
   a strong reason to believe the joint state matters more than additive
   evidence.
5. Frozen forecast registry: keep forecast definitions and hyperparameters
   stable enough that evaluation is about signal quality, not continual
   hyperparameter churn.
6. Realization-grid combination: align forecast outputs on a 5-second grid, then
   combine them into a final prediction or policy input.

This is not a single-model worldview. It is closer to a forecast-bank worldview:
many weak and partially redundant signals are organized into stable modules, and
the outer combination layer decides how much to trust each module now.

## Design Principles

The framework suggests several durable principles.

First, separate signal calibration from forecast identity. A signal can need
short-horizon recalibration because its raw scale, volatility, or reliability
drifts. That does not mean the thematic forecast that consumes it should be
retuned constantly.

Second, make themes the unit of stability. A forecast family is easier to audit
than tens of thousands of raw features. It can have a definition, a validation
history, a failure profile, and a known interaction with other forecasts.

Third, use rolling ridge or lasso as combination machinery, not as an excuse to
re-mine the entire signal universe. The regularized rolling model should reward
signals and forecasts that remain stable through time while shrinking noisy
ones.

Fourth, keep the realization grid explicit. A 5-second grid forces all forecast
outputs into a shared time contract. That makes it easier to reason about
latency, target alignment, execution handoff, and realized utility.

## Relation To P12n

This framework is a useful reference for [P12n](../../projects/p12n.md)
because p12n currently has a tension between model-family exploration and
forecast-system construction.

The main lesson is to avoid treating "the model" as a monolith. P12n could
separate:

- raw feature streams;
- calibrated component signals;
- stable forecast modules;
- a forecast combination layer;
- execution and threshold policy.

That would let p12n experiment with nonlinear features, temporal bases, and
sequence-model analogies inside bounded modules while still evaluating stable
forecast objects over time.

The framework also supports p12n's preference for regression-heavy tooling.
Ridge and lasso are natural outer combiners when the inputs are already
calibrated forecasts or typed signal components. The difficult part is not the
outer regression; it is building stable, nonleaky, well-calibrated forecast
inputs.

## Speculative Extensions

The following are extrapolations from the source note, not claims about zzz's
actual implementation.

A p12n version could make forecast modules first-class artifacts. Each forecast
would record its input feature families, target horizon, realization grid,
calibration method, frozen hyperparameters, training window, and validation
history. This would make a forecast more like a versioned asset than an
ephemeral experiment.

The "11 forecasts" shape suggests a useful cap. The goal is not to create one
forecast per signal family forever. It is to compress a large signal universe
into a small number of durable themes whose outputs can be monitored and
combined.

Internal calibration can be handled by small models: rolling z-scores, robust
volatility normalization, isotonic or spline calibration, decay adjustment, and
target-scale correction. Those calibrators should be replayable and
out-of-fold-safe, because they sit upstream of the final forecast evidence.

Interaction terms should probably be local to themes. Cross-theme interactions
are tempting, but they can quickly turn the outer layer into another opaque
feature search process. A safer rule is: put interactions inside the forecast
that owns the causal or market-structure interpretation; keep the outer layer
mostly shrinkage and weighting.

## Open Questions

- What were the 11 thematic forecasts, and how were their boundaries chosen?
- What does "frozen forecast" mean operationally: frozen features, frozen
  hyperparameters, frozen coefficients, or only frozen model class?
- How are shorter-period signal calibrations prevented from leaking future
  information into forecast evaluation?
- Does the 5-second realization grid represent target measurement, forecast
  publication, execution decision cadence, or all three?
- How are forecast outputs translated into execution policy and realized
  utility?

## Source Map

- [zzz's framework](../../../ops/artifacts/obsidian/zzz-s-framework.md)
