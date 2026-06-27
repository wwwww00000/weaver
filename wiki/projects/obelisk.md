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
now in archive mode.

Its durable value is not the strategy implementation itself. The useful residue
is a set of modeling lessons about edge, exits, realization schedules, regime
selection, and adaptive temporal estimators that can inform newer trading work.

## Map

- [Edge and Utility](obelisk/edge-and-utility.md): how forecasts, fills,
  adversity, variance, covariance, and inventory entered the decision objective.
- [Entries and Exits](obelisk/entries-and-exits.md): why entries could contain
  signal while the full strategy still failed through exits, horizon mismatch,
  and risk-limit behavior.
- [Forecast Realization](obelisk/forecast-realization.md): why long-horizon
  expectations were not enough, and how realization schedules could bridge
  forecasts to policy.
- [Regime and Instrument Selection](obelisk/regime-and-instrument-selection.md):
  why performance concentrated in specific instruments, time periods, sampling
  choices, and market-structure regimes.
- [Dynamic EMA Decay](obelisk/dynamic-ema-decay.md): reusable adaptive EMA and
  temporal-modeling ideas that probably belong in p12n as well.

## Summary

Obelisk repeatedly ran into the same central problem: a signal can improve entry
quality without producing a robust strategy. The missing pieces were often exit
policy, horizon consistency, adverse-selection treatment, and the state needed
to understand how a forecast realizes through fills and future decisions.

The project also suggested a useful research pattern: start with empirical trade
or forecast behavior, infer the objective or state model it implies, and then
test whether the implied objective survives under realized utility, capacity,
and market-structure constraints.

## Status

Treat this as archive-mode research context. Reusable modeling ideas should be
pulled forward into active project pages, especially p12n. Historical
implementation details should stay subordinate to the concepts above.

## Source Bundle

This hub and its child pages were synthesized from the `obelisk/quant` bundle in
[the source inventory](../../ops/clusters/2026-06-24/source-inventory.qmd).
