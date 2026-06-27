---
title: Entries and Exits
status: draft
page_type: concept
projects:
  - obelisk
categories:
  - quant
  - trading
  - market-making
parent: projects/obelisk
source_bundles:
  - obelisk/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
created: 2026-06-27
updated: 2026-06-27
---

# Entries and Exits

One of Obelisk's clearest lessons is that entry quality and strategy quality are
not the same thing. A signal can select good entries while the full policy loses
value through exits, horizon mismatch, risk limits, or inventory handling.

## Entry Signal Was Not The Whole Bottleneck

Several experiments suggested that entries were not the main weakness. Order
returns could improve under some variants, and changing the forecast to a moving
average version could fix performance despite similar order returns. The bigger
gaps appeared after the fill: how inventory was exited, how horizons were
applied, and how the policy handled position limits.

This matters because optimizing entry statistics alone can hide downstream
policy errors. A better entry model may increase exposure to cases where the
exit model is weakest.

## Horizon Consistency

Obelisk repeatedly hit horizon mismatch problems. Single-period horizons did not
work cleanly, and using horizon-1 exits could cut off performance from forecast
entries. Fine-grid and resampled-grid experiments showed that trade interval,
exit interval, and exit price handling could change results substantially.

The practical lesson is to evaluate an entry forecast together with the horizon
over which its edge is realized. If the forecast has a multi-period realization
profile but the policy exits as if all alpha is single-period, the strategy can
prematurely discard profitable trajectories.

## Exits Need Their Own Model

Exits are not merely the negation of entries. In adverse regimes, a model may
want to trade less, but using the same penalty on both sides can also penalize
necessary exits. Obelisk notes this directly in the residuals work: adverse
regime logic must separate entry suppression from exit permission.

That separation suggests at least three policy components:

- entry selection: when opening or adding exposure is worth it;
- exit selection: when reducing exposure is worth it;
- risk-limit handling: what to do when max position or capacity constraints are
  already binding.

## Position Limits And Capacity

Some performance changes were tied to time spent at position limits. Reducing
time at limits could reduce profitability if it prevented the strategy from
realizing alpha that only appears while inventory is held. Capacity and risk
limits therefore need to be evaluated as part of the policy, not merely as
external constraints.

## Design Implications

- Report entry and exit performance separately.
- Test whether exit logic preserves the forecast horizon.
- Evaluate policies under realistic position limits and capacity constraints.
- Avoid using one adverse-regime rule for both entries and exits unless the
  interaction has been tested.
- Treat fine-grid simulation and resampling choices as model assumptions.

## Open Questions

- What diagnostics best separate entry alpha from exit alpha?
- How should exit permission differ from entry suppression in adverse regimes?
- Can a policy learn a realization-aware exit rule without a large state space?

## Sources

- [fine grid](../../../ops/artifacts/obsidian/obelisk-fine-grid.md)
- [residuals](../../../ops/artifacts/obsidian/obelisk-residuals.md)
- [trades study](../../../ops/artifacts/obsidian/obelisk-trades-study.md)
- [trades vs forecast and optimization](../../../ops/artifacts/obsidian/obelisk-trades-vs-forecast-and-optimization.md)
- [conditional forecast realization](../../../ops/artifacts/obsidian/obelisk-conditional-forecast-realization.md)
