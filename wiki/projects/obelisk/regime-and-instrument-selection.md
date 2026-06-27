---
title: Regime and Instrument Selection
status: draft
page_type: research-thread
projects:
  - obelisk
categories:
  - quant
  - trading
  - market-structure
parent: projects/obelisk
source_bundles:
  - obelisk/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
created: 2026-06-27
updated: 2026-06-27
---

# Regime and Instrument Selection

Obelisk found that profitability was concentrated in specific instruments and
specific regimes. This made instrument selection, temporal filtering, and
market-structure diagnostics central to the research process.

## Profitability Was Regime-Dependent

Some instruments worked only during brief volatility windows, while others were
not well served by simple rolling-performance filters. The project explored
rolling regression, volatility scaling, clipping, edge combinations, and
sliding-window performance simulations as ways to decide when to trade.

The durable idea is to treat participation as a modeled decision. If most PnL
comes from a few instruments or regimes, the strategy needs a participation
model, not only a better forecast.

## Rolling Regression As A Regime Lens

Rolling regression was useful less as a final model and more as a way to expose
temporal structure. With lagged-return features, rolling multivariate regression
could outperform full-sample regression. Rolling decision trees also performed,
but less strongly.

The results suggest that time-varying feature sensitivities were real, but not
all forecast gains were tradeable. That distinction matters: a feature can
improve predictive loss while failing to improve fills, exits, or realized
utility.

## Instrument And Market-Structure Hazards

The notes preserve several practical hazards:

- time-varying tick-size artifacts, especially on large-tick instruments;
- differences between BUSD and USDT instruments;
- sampling frequency and trade interval effects;
- edge-selection behavior that changes between coarse and fine grids;
- volume and capacity changes caused by trade sparsity;
- missing or incomplete aggregate-trade data.

These are not just data-cleaning details. They can change which horizon appears
profitable, which edge threshold is selected, and how much capacity the strategy
seems to have.

## Participation Model

A participation model could combine:

- recent instrument-level profitability;
- rolling edge-selection performance;
- volatility and tick-size state;
- trade interval and sampling diagnostics;
- cross-sectional market-factor behavior;
- volume, aggressor volume, and price-impact features.

This would turn "which instruments should we trade right now?" into a first
class modeling problem.

## Open Questions

- Which regime filters generalize rather than chase recent PnL?
- How should a strategy distinguish temporary opportunity from overfit
  instrument selection?
- Which market-structure artifacts should be excluded from modeling versus
  modeled explicitly?

## Sources

- [profitability regimes](../../../ops/artifacts/obsidian/obelisk-profitability-regimes.md)
- [rolling regression](../../../ops/artifacts/obsidian/obelisk-rolling-regression.md)
- [trades study](../../../ops/artifacts/obsidian/obelisk-trades-study.md)
- [opportunity set](../../../ops/artifacts/obsidian/obelisk-opportunity-set.md)
- [signal research and feature engineering](../../../ops/artifacts/obsidian/obelisk-signal-research-and-feature-engineering.md)
- [covariance](../../../ops/artifacts/obsidian/obelisk-covariance.md)
