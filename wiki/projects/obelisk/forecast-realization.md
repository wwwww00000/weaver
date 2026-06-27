---
title: Forecast Realization
status: draft
page_type: concept
projects:
  - obelisk
categories:
  - quant
  - trading
  - temporal-modeling
parent: projects/obelisk
aliases:
  - realization schedule
source_bundles:
  - obelisk/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
created: 2026-06-27
updated: 2026-06-27
---

# Forecast Realization

Forecast realization is the problem of turning a forecast into a model of how
returns actually arrive through fills, non-fills, inventory, and future exits.

In Obelisk, long-horizon conditional expectation was not enough. A forecast may
be directionally useful while still being hard to monetize if its return is
realized on the wrong horizon or through the wrong path.

## Why A Realization Schedule Is Needed

Without a simplifying model, the policy state is effectively a vector of future
returns. That state is too large for practical value-function learning. A
realization schedule compresses that vector into a smaller description of how
edge decays or arrives over time.

A schedule could be constant, linear, exponential, leaf-specific, edge-specific,
or conditioned on forecast magnitude. The important point is not the first
parametric choice. The important point is to make the realization assumption
explicit and testable.

## Empirical Realization

The Obelisk notes point toward estimating empirical realization curves by leaf,
edge, fill state, or forecast magnitude. This makes it possible to ask:

- after a strong forecast, when do returns actually arrive?
- are large predictions stickier than small predictions?
- do different leaves have different decay schedules?
- how do existing fills change the expected return of new orders?
- how should non-fills be represented so missing covariates do not bias the
  estimates?

This shifts forecast research from "is the forecast good?" to "how does the
forecast become tradable return under the policy?"

## Link To Value Functions

Forecast realization is the bridge between forecasting and policy optimization.
A value function needs a compact state. If the state includes every future
return, it is infeasible. If the state includes a scalar edge plus a tested
realization schedule, it becomes possible to reason about exits, inventory, and
future fills.

That makes realization schedules a candidate state-reduction device. They are
not only diagnostics; they define what information the strategy carries forward
after a forecast or fill.

## Design Implications

- Do not evaluate long-horizon forecasts only by terminal markout.
- Estimate realization curves under the actual fill and exit process.
- Keep realization assumptions low-dimensional enough to use inside a policy.
- Test whether realization schedules differ by leaf, forecast magnitude, and
  edge.
- Treat non-fills as informative when estimating conditional returns.

## Open Questions

- What is the minimal realization state that preserves enough policy value?
- Should realization schedules be forecast-specific, leaf-specific, or shared?
- How should existing inventory and prior fills modify a new order's expected
  return?

## Sources

- [conditional forecast realization](../../../ops/artifacts/obsidian/obelisk-conditional-forecast-realization.md)
- [summary](../../../ops/artifacts/obsidian/obelisk-summary.md)
- [signal research and feature engineering](../../../ops/artifacts/obsidian/obelisk-signal-research-and-feature-engineering.md)
- [trades vs forecast and optimization](../../../ops/artifacts/obsidian/obelisk-trades-vs-forecast-and-optimization.md)
