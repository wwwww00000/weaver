---
title: Execution And Policy
status: draft
page_type: research-thread
projects:
  - p12n
categories:
  - quant
  - trading
  - execution
  - policy
  - crypto
source_bundles:
  - p12n/project context
  - p12n/current priorities
  - quant/returns
  - obelisk/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/p12n
related:
  - projects/p12n
  - projects/p12n/temporal-returns-experiments
  - projects/p12n/feature-transforms-and-bst
  - topics/quant/generalization-and-regularization
  - projects/obelisk/edge-and-utility
  - projects/obelisk/entries-and-exits
  - projects/obelisk/forecast-realization
created: 2026-06-27
updated: 2026-06-27
---

# Execution And Policy

Execution and policy is the part of p12n that turns forecasts into realized
trading behavior.

Forecasting is necessary but not sufficient. A return model can improve
prediction metrics and still fail after thresholds, fills, inventory, position
limits, exits, and risk penalties are applied. This page keeps those concerns
separate from pure return forecasting.

## Current Scope

The current p12n execution thread includes:

- baseline EMA policy simulations;
- unnormalized order-return prediction;
- alternative edge-vector definitions;
- fixed-edge versus variable-target distributions at equal fill rate;
- long EMA of past order returns as an intercept or feature;
- threshold and multiplier estimation;
- entries conditioned on forecasts and volatility;
- BPTE experiments with inventory and position constraints.

The practical question is:

```text
Given forecasts and market state, what order should be placed, at what edge,
with what size, threshold, and exit behavior?
```

## Prediction Objects

Execution modeling has several related targets:

- future asset returns;
- passive fill probability;
- conditional order return given fill;
- expected order value across edge, side, symbol, and time;
- realized PnL under a policy;
- risk, liquidation, and inventory penalties.

The order-return target is especially important because it is the payoff of the
action actually being taken. It is not identical to a mid-price return forecast.
Fill selection and adverse selection can make conditional order returns negative
even when a raw forecast looks useful.

The older `Predicting Returns and Fills` source suggests a useful decomposition:
model fill probability and conditional return separately when diagnosis matters,
but also evaluate direct expected-return or utility targets because the policy
ultimately acts on their product.

## Forecast-To-Policy Boundary

Keep three layers distinct:

1. forecast model: predicts returns or order returns;
2. execution model: predicts fills, conditional markouts, and edge behavior;
3. policy model: chooses thresholds, sizes, exits, and inventory actions.

Mixing these too early creates confusing metrics. A forecast may be good, but
the policy can lose value by exiting on the wrong horizon or applying a threshold
that destroys fill quality. Conversely, a weaker forecast may become tradable if
the policy only uses it in regimes where execution is favorable.

This is the main lesson inherited from Obelisk:

- [Entries and Exits](../obelisk/entries-and-exits.md) are separate objects.
- [Forecast Realization](../obelisk/forecast-realization.md) determines how
  alpha arrives through fills and exits.
- [Edge and Utility](../obelisk/edge-and-utility.md) must include fill,
  adversity, inventory, variance, and realized path.

## BPTE Thread

BPTE is the current p12n route for learning policy behavior through a differentiable
or semi-differentiable simulation-like objective.

Current notes:

- loose inventory constraints caused convergence issues;
- l1/l2 penalties on timestep positions were tested;
- removing liquidation penalty modestly improved USDC PnL per volume;
- adding a position or forecast term before the sigmoid had small effect;
- sided parameters had small effect;
- validation stopping or post-hoc stopping is still open;
- thresholds may need to be frozen during BPTE and refit afterward;
- disaggregated loss logging is needed for PnL, risk, and liquidation.

The important design rule is to keep BPTE diagnostics decomposed. A single final
Pnl number is not enough to understand whether a change improved forecast use,
inventory behavior, liquidation avoidance, or threshold calibration.

## Thresholds And Multipliers

Threshold and multiplier estimation is data-limited because relevant samples are
conditioned on fills and selected actions.

The p12n notes suggest enumeration as a practical first pass:

- slice to the relevant filled or thresholded samples;
- test candidate multipliers directly;
- compare mean/variance or utility metrics;
- keep volatility conditioning explicit;
- refit thresholds after BPTE if joint fitting is unstable.

This favors small, auditable searches over highly parameterized threshold
models. Volatility-conditioned thresholds are still useful, but they should be
expressed as a low-dimensional family.

## Target Position And CPA

The target-position or CPA formulation is a possible alternative to directly
choosing orders or thresholds. In that view, the policy learns the desired
inventory trajectory or target exposure, and execution becomes a control problem
around that target.

This may make risk constraints easier to express, but it also changes the
diagnostic surface. A target-position model must still answer:

- how forecasts translate into position;
- how fills move actual position relative to target;
- how exits are triggered;
- how liquidation and variance penalties enter;
- whether forecast realization horizon is preserved.

## Realization And Horizon

Obelisk's forecast-realization lesson is directly relevant. Long-horizon
forecasts should not be evaluated only by terminal markout. The policy needs to
know how the forecast is realized over time:

- does edge arrive immediately or slowly?
- does fill status change the future return profile?
- should exits preserve a multi-period forecast?
- are large forecasts stickier than small forecasts?
- do thresholds change the realized horizon?

For p12n, multi-horizon return targets and order-return targets should be
treated as a basis for policy design, not only as forecast metrics. The policy
may want to weight early horizons more heavily if later horizons do not
generalize.

The reusable horizon-decomposition and recombination discussion lives in
[Generalization And
Regularization](../../topics/quant/generalization-and-regularization.md).

## Validation

Execution validation should report at least:

- forecast metric by fold;
- fill probability and conditional return diagnostics;
- policy PnL and PnL per volume;
- realized utility after risk penalties;
- inventory and position-limit occupancy;
- disaggregated loss terms;
- threshold and multiplier stability;
- performance by symbol, side, volatility regime, and edge.

Validation should also distinguish forecast improvement from policy
improvement. A model change should not be credited to forecasting if the gain
comes from threshold refit, fill selection, or reduced inventory risk.

## Open Questions

- Should p12n model fill probability and conditional order return separately, or
  primarily model direct expected order value?
- What is the right edge normalization across symbols: volatility multiple,
  equal fill probability, or raw price distance?
- How should thresholds be refit after BPTE without causing secondary
  divergence?
- Can forecast realization schedules reduce the policy state enough for stable
  learning?
- Which BPTE loss terms should be logged and validated independently?
- When should execution conditioning use BST-style bins versus a learned policy
  component?

## Source Map

- [p12n overview](../../../ops/artifacts/obsidian/p12n-overview.md)
- [p12n signals](../../../ops/artifacts/obsidian/p12n-signals.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
- [Predicting Returns and Fills](../../../ops/artifacts/chatgpt/6710eaf9-ec70-8009-b573-28274dc3d163.md)
- [Predicting Asset Returns](../../../ops/artifacts/chatgpt/69983c39-aac0-839a-a0a9-c23e8d7d6aab.md)
- [Forecast Horizon Generalization](../../../ops/artifacts/chatgpt/69dce9bb-bd10-8399-987b-c262e6f85e63.md)
- [Obelisk Edge and Utility](../obelisk/edge-and-utility.md)
- [Obelisk Entries and Exits](../obelisk/entries-and-exits.md)
- [Obelisk Forecast Realization](../obelisk/forecast-realization.md)
