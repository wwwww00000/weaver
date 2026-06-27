---
title: Quant
status: draft
page_type: topic-hub
categories:
  - quant
  - trading
  - machine-learning
  - time-series
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
created: 2026-06-27
updated: 2026-06-27
---

# Quant

Quant is the reusable methods layer for trading-related modeling ideas that
should outlive any one project implementation.

Use this hub for regression stability, temporal validation, adaptive filters,
time-series diagnostics, tabular nonlinearities, optimization tricks, and
structured return models. Project pages such as [P12n](../projects/p12n.md)
should stay anchored to active work; quant pages should hold the durable
technique or mathematical pattern.

## Map

- [Temporal Evidence](quant/temporal-evidence.md): regression-evidence
  congruency, ACF-like summaries, temporal hat smoothers, and window-risk
  diagnostics.
- [Regression Stability And Validation](quant/regression-stability-and-validation.md):
  cross-validation as self-influence deletion, LOOCV identities, leakage
  control, and out-of-fold transforms.
- [Adaptive Filters And EMA](quant/adaptive-filters-and-ema.md): dynamic
  forgetting, RLS/LMS/Kalman views, fast weights, and decay diagnostics.
- [Structured Return Models](quant/structured-return-models.md): diagonal,
  low-rank, and diagonal-plus-low-rank return operators with temporal filters.
- [Tabular Nonlinearities And Feature Search](quant/tabular-nonlinearities.md):
  bins, product features, feature hashing, splines, MARS-like functions, and
  greedy residual fitting.
- [Optimization And Computation](quant/optimization-and-computation.md):
  Gauss-Newton, ADMM, LSQR/LSMR, block coordinate descent, and efficient risk
  computations.
- [Generalization And Regularization](quant/generalization-and-regularization.md):
  ridge, shrinkage, horizon generalization, validation-aware regularization,
  and gradient similarity.

## Boundary With P12n

P12n is the active applied crypto trading project. Quant is the archival method
layer.

When a p12n conversation produces a reusable method, keep the project-facing
summary under p12n and move the general formulation here. The two layers should
cross-link rather than duplicate each other.

## Source Map

- [P12n and Quant Categorization](../../ops/synthesis/p12n-quant-categorization.md)
- [source inventory](../../ops/clusters/2026-06-24/source-inventory.qmd)
