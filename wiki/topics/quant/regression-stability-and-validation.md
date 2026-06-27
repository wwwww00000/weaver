---
title: Regression Stability And Validation
status: draft
page_type: method-note
projects:
  - p12n
categories:
  - quant
  - regression
  - validation
  - machine-learning
  - time-series
source_bundles:
  - p12n/math
  - p12n/machine learning
  - unassigned/quant
  - quant/ridge
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - topics/quant/temporal-evidence
  - topics/quant/tabular-nonlinearities
  - topics/quant/generalization-and-regularization
  - projects/p12n/temporal-returns-experiments
  - projects/p12n/feature-transforms-and-bst
created: 2026-06-27
updated: 2026-06-27
---

# Regression Stability And Validation

Regression validation is not just a final score. For low-SNR time-series
models, validation is a way to ask whether an effect survives deletion,
resampling, temporal separation, and shrinkage.

The central distinction is:

- training fit asks whether a coefficient can explain the rows it was fit on;
- stability asks whether the same coefficient direction transfers to rows that
  were not allowed to influence it.

This page collects the reusable validation primitives behind p12n-style return
experiments and tabular feature discovery.

## LOOCV And Leverage

For ordinary least squares, leave-one-out predictions can be computed from one
full fit:

```text
e_i^(-i) = e_i / (1 - h_ii)
LOOCV = mean_i (e_i / (1 - h_ii))^2
```

where `H = X (X^T X)^-1 X^T` and `h_ii` is the leverage of sample `i`.

This says that LOOCV is training residual error reweighted by self-influence.
A point matters more when it is both badly fit and high leverage.

In the intercept-only model, leverage is constant:

```text
h_ii = 1 / n
```

so LOOCV reduces to a uniform inflation of training error. In simple regression
with intercept:

```text
h_ii = 1 / n + (x_i - mean(x))^2 / sum_j (x_j - mean(x))^2
```

so edge points or covariate outliers receive stronger correction. The
nontrivial content of LOOCV is leverage variation.

## Block Deletion

For a held-out block `S`, the scalar LOOCV correction becomes a block
correction:

```text
e_S^(-S) = (I - H_SS)^-1 e_S
```

This is the right mental model for k-fold CV in linear smoothers: remove the
held-out block's self-influence, then renormalize the residual through the
block hat submatrix.

The block view matters for time series. If neighboring samples are serially
correlated, ordinary LOOCV can be optimistic because the left-out sample is
still partly represented by adjacent training rows. Blocking makes the deletion
large enough to remove local dependence.

## Time-Series Splits

The validation split should match the deployment question.

Useful split families:

- block CV: hold out contiguous chunks;
- h-block CV: hold out a block and purge a gap around it;
- rolling-origin CV: train on the past and test the next period;
- expanding-window CV: grow the training set through time;
- sliding-window CV: hold training history length fixed;
- grouped CV: keep asset, session, or regime groups from leaking across folds.

For forecasting and trading, random folds are usually a diagnostic only. They
answer a weaker question than future-facing validation because they allow
future rows and adjacent rows to influence training.

## Analytical Risk Proxies

For a linear smoother:

```text
y_hat = S_lambda y
```

the same leverage identity gives analytic LOO:

```text
LOO(lambda) = mean_i ((y_i - y_hat_i) / (1 - S_ii(lambda)))^2
```

Generalized cross-validation replaces individual diagonal terms with the
average degrees of freedom:

```text
1 - S_ii ~= 1 - trace(S) / n
```

These are useful for ridge, kernel ridge, smoothing splines, and iterative
regularization. They are fast because a single fit or path can evaluate many
regularization settings.

With serial dependence, IID LOO/GCV needs adjustment. Options include:

- block or h-block CV;
- pre-whitening and applying ordinary formulas to the transformed problem;
- correlated-GCV or HAC-adjusted risk estimates;
- moving-block or stationary bootstrap for final uncertainty;
- effective-sample-size scaling as a rough sanity check.

The practical rule is simple: use analytic IID formulas for speed only after
checking that dependence does not dominate the target validation question.

## OOF Scaling Versus Ridge

Out-of-fold prediction scaling is a useful calibration tool:

```text
y ~= c y_hat_oof
0 <= c <= 1
```

It can shrink an overconfident model cheaply, especially when OOF predictions
are already available. It is not the same as choosing a ridge penalty in
general.

Ridge changes the coefficient vector during fitting:

```text
beta_ridge = (X^T X + lambda I)^-1 X^T y
```

Post-hoc OOF scaling changes only the final prediction amplitude. In an
orthonormal design, ridge reduces to uniform coefficient shrinkage and can be
matched by a scalar prediction shrinkage. In correlated designs, ridge changes
coefficient shape and cannot be replaced by one scalar.

Use OOF scaling for calibration and stacking. Use ridge or another in-model
regularizer when the feature geometry itself is unstable.

## Out-Of-Fold Derived Features

Any derived feature that was fit using the target should be cross-fitted before
it is consumed downstream.

This applies to:

- target encodings;
- prediction-derived features;
- residual-derived features;
- stacked model predictions;
- bin means;
- product bins involving fitted predictions;
- feature transforms selected on target evidence.

The pattern is:

```text
for each fold:
  fit transform on training folds
  emit transform value on held-out fold
concatenate held-out emissions
fit downstream model using the OOF feature
```

For time series, the fold structure should be causal or blocked. A random OOF
feature can still leak future regime information.

## Internal Validation Objectives

Some models bring validation-like objectives inside the fit:

- empirical Bayes or marginal likelihood for prior and kernel parameters;
- analytic LOO or GCV for linear smoothers;
- SURE for denoising and thresholding under Gaussian noise assumptions;
- information criteria along regularization paths;
- early stopping interpreted as an implicit smoother.

These methods are useful when their assumptions match the data. They should not
be confused with an external test set. They are efficient internal risk proxies,
not proof that the deployment setting has been simulated.

## Relationship To Temporal Evidence

[Temporal Evidence](temporal-evidence.md) is the EDA and geometry layer. It
studies whether per-sample or per-block regression evidence points in compatible
directions.

This page is the validation decision layer. It asks how to turn that evidence
into deletion protocols, OOF features, shrinkage choices, and final model
selection rules.

The two pages should stay linked:

- use temporal evidence to discover where effects appear stable;
- use validation protocols to decide whether a model using those effects should
  be trusted.

## Open Questions

- What default block length should p12n use for highly oversampled crypto
  returns?
- Should OOF feature generation use pure past-only folds, blocked folds, or both?
- Which analytic risk proxy is reliable enough for fast screening?
- How should repeated feature selection be accounted for in validation reports?
- Can temporal evidence scores predict which candidate features survive blocked
  validation?

## Source Map

- [LOOCV in Linear Regression](../../../ops/artifacts/chatgpt/697029f8-1a68-8327-b141-4702e8e890bd.md)
- [Optimizing Validation Loss Internally](../../../ops/artifacts/chatgpt/68610ec1-9fdc-8009-9d90-04b57d2d2089.md)
- [Temporal Cross-Validation Unification](../../../ops/artifacts/chatgpt/69ec7a41-1fb0-839b-ad3c-7c0a3c6800c0.md)
- [p^2 Branch - Temporal Cross-Validation Unification](../../../ops/artifacts/chatgpt/69ef5eea-aed0-839c-88cb-b70b24e63a44.md)
- [LOOCV Error Efficient Computation](../../../ops/artifacts/chatgpt/6811ed55-0e14-8009-9c2a-f4b586b27278.md)
- [Ridge CV vs OOF Scaling](../../../ops/artifacts/chatgpt/6763f3ae-17ec-8009-8723-49f1fcb2e6c1.md)
- [Sparse Features in Ridge](../../../ops/artifacts/chatgpt/69cff0f3-96b8-839e-8380-caf5d0b911b6.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
