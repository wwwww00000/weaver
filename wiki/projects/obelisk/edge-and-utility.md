---
title: Edge and Utility
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

# Edge and Utility

Obelisk framed a market-making decision as more than expected return. A quote or
order needed enough edge after accounting for fill probability, adverse
selection, inventory, variance, covariance with existing exposure, and eventual
exit behavior.

## Edge Has Probability And Adversity

The edge-function notes separate two objectives for a candidate horizon:

- probability: how likely the order or opportunity is to pay;
- adversity: how bad the fill or realized path is conditional on getting filled.

Using volatility as a proxy for adversity was attractive but incomplete. In
negative-autocorrelation or mean-reverting regimes, edge can be lower than a
plain volatility estimate. During certain opportunities, scaling edge by
volatility can also hide trades where absolute distance from price matters more
than normalized distance.

This means edge should not be treated as a single universal threshold. The right
threshold depends on the interaction between fill probability, markout,
reversion, and realized path.

## Utility Made Failure Modes Visible

A useful Obelisk abstraction was to express total return as inventory exposure
plus order return. In simplified form:

```text
total_return = inventory * forecast + quantity * order_return
```

The strategy objective then becomes expected return minus a risk penalty. This
brings variance and covariance terms into the decision, including the covariance
between inventory forecast and the new order return.

That formulation exposed a practical failure mode: adding more quadratic terms
can make expected utility look better while realized utility gets worse. If the
variance, covariance, or conditional-return estimates are inaccurate, the
optimizer can overweight the wrong trades even when raw order returns look
promising.

## Optimization Versus Trades

The project also raised an inverse question: given a working set of trade
parameters, what utility constants would reproduce the same behavior? This is a
useful diagnostic move. A heuristic strategy implicitly encodes a risk appetite,
adverse-selection model, and exit preference. Making those constants explicit
lets you compare the implied objective against realized utility.

The reverse direction is equally important. A clean utility objective may fail
to reproduce a robust trade policy if its covariance assumptions, horizon
assumptions, or exit assumptions are wrong.

## Design Implications

- Treat edge as a modeled object, not only a volatility multiple.
- Separate fill probability from adverse-selection severity.
- Validate utility terms against realized trades, not just simulated expected
  utility.
- Compare heuristic trade parameters with their implied objective constants.
- Treat covariance and cross terms as high-risk estimates that need shrinkage or
  empirical validation.

## Open Questions

- When should edge be scaled by volatility, and when should absolute distance
  from price dominate?
- What is the right low-dimensional adversity model for market-making fills?
- Can implied utility constants be used as a diagnostic for strategy drift?

## Sources

- [edge function](../../../ops/artifacts/obsidian/obelisk-edge-function.md)
- [trades vs forecast and optimization](../../../ops/artifacts/obsidian/obelisk-trades-vs-forecast-and-optimization.md)
- [summary](../../../ops/artifacts/obsidian/obelisk-summary.md)
- [opportunity set](../../../ops/artifacts/obsidian/obelisk-opportunity-set.md)
