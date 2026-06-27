---
title: Dynamic EMA Decay
status: draft
page_type: method
projects:
  - obelisk
  - p12n
categories:
  - quant
  - temporal-modeling
  - online-learning
parent: projects/obelisk
related:
  - projects/obelisk/regime-and-instrument-selection
  - topics/quant/adaptive-filters-and-ema
source_bundles:
  - obelisk/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
created: 2026-06-27
updated: 2026-06-27
---

# Dynamic EMA Decay

Dynamic EMA decay is the idea that an EMA's decay parameter should itself adapt
to the recent behavior of the series. In Obelisk, this emerged from volatility
and edge estimation, but the idea generalizes to temporal modeling in p12n.

## EMA As Online Learning

An EMA can be read as online gradient descent on a mean-estimation problem:

```text
estimate_t = estimate_{t-1} + alpha * (observation_t - estimate_{t-1})
```

The decay `alpha` is the learning rate. A small `alpha` is stable but slow; a
large `alpha` is responsive but noisy. Making `alpha` dynamic turns the EMA into
a small learning-to-learn system.

## Gated EMA

A simple family uses standardized surprise to choose the update rate. When a
return is ordinary, the EMA uses a slow baseline decay. When the return is a
large surprise, the update rate ramps upward so the volatility estimate catches
up quickly.

The most practical version is a piecewise linear gate:

- below a lower surprise threshold, use the baseline decay;
- between two thresholds, ramp the decay upward;
- above the upper threshold, use the fast decay.

This is easy to inspect, tune, and test against application-specific strategy
metrics.

## Releasing Excess Surprise Mass

A one-sided gate can leave volatility elevated for too long. After a large
surprise, standardized residuals become small because the denominator is now
large, so the model may revert only at the slow baseline rate.

Several fixes stay in the same spirit:

- use a two-sided gate, where very small standardized residuals accelerate
  downward adjustment;
- smooth the dynamic `alpha` so it decays toward baseline after shocks;
- use asymmetric smoothing, with fast upward moves and slower controlled
  downward release;
- add a weak baseline pull while keeping the EMA update as the main mechanism.

The goal is to react quickly to new volatility without staying overestimated
after the shock has passed.

## Learning The Decay

The decay can also be updated by online gradient descent. This requires care
because same-step loss is degenerate: if the goal is only to fit the current
observation, the optimal decay chases the latest tick. A useful decay update
needs an outer objective, such as future predictive loss or calibration.

Two loss families have different meanings:

- least squares optimizes point prediction and moves according to raw error;
- Gaussian negative log-likelihood optimizes predictive distribution quality and
  makes updates scale-aware through variance.

For volatility or uncertainty modeling, NLL-style objectives are attractive
because they reward calibrated uncertainty, not only point accuracy.

## More Stable Alternatives

The dynamic-decay idea points to several more stable temporal-modeling
directions:

- maintain a bank of EMAs at fixed timescales and combine them online;
- use a Kalman-filter view, where adaptive gain is the principled version of a
  dynamic EMA decay;
- learn only a small number of decay or process-noise scalars;
- use gradient or residual persistence as a signal that a parameter block should
  move faster.

These are good candidates for p12n because they add adaptive temporal structure
without immediately jumping to a large deep learning model.

The broader method layer is
[Adaptive Filters And EMA](../../topics/quant/adaptive-filters-and-ema.md).
This Obelisk note keeps the project-specific dynamic EMA thread; the quant note
keeps the reusable adaptive-filter framework.

## Design Implications

- Treat decay as a timescale parameter, not just a smoothing constant.
- Do not optimize decay against same-step fit.
- Prefer future loss, calibration loss, or ensemble weighting for decay
  adaptation.
- Keep dynamic freedom small and interpretable before making many parameters
  time-varying.
- Test dynamic estimators inside the trading objective, not only on residual
  plots.

## Open Questions

- Which loss best matches the downstream trading use of volatility?
- When is a dynamic single decay better than an ensemble of fixed decays?
- Should p12n use dynamic EMA decay as a preprocessing primitive, a model
  component, or a diagnostic for when richer temporal models are needed?

## Sources

- [gated EMA families](../../../ops/artifacts/chatgpt/6936a790-5b38-8321-8b75-eb1b44aa8da1.md)
- [dynamic EMA decay insights](../../../ops/artifacts/chatgpt/694277f3-e9f0-8324-a701-f326a5fb6f1c.md)
- [branch dynamic EMA decay insights](../../../ops/artifacts/chatgpt/6942ca88-6cd8-8324-92fb-f22be8e6b689.md)
- [EMA decay update derivation](../../../ops/artifacts/chatgpt/69442455-8f98-8321-9ba3-e9d4383c0e09.md)
- [learning dynamic temporal models](../../../ops/artifacts/chatgpt/69451015-6760-8323-b46f-b4acf7358496.md)
