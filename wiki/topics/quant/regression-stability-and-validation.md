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
  - unassigned/math
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
updated: 2026-06-28
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

## Exact Versus Summary Risk

Exact LOOCV needs row-level residuals and row-level leverages:

```text
e_i = y_i - x_i^T beta
h_i = x_i^T (X^T X)^-1 x_i
```

The diagonal of the hat matrix cannot be recovered from `X^T X`, `X^T y`, and
`beta` alone. Those summaries forget which row had which leverage. An exact
memory-light implementation can stream rows to accumulate `h_i` and `e_i`, but
it still needs access to each row.

When only aggregate summaries are available, use a proxy such as GCV:

```text
GCV = (RSS / n) / (1 - trace(H) / n)^2
```

This is useful for fast screening, but it hides leverage concentration. If rare
features, clustered regimes, or sparse rows create uneven leverage, exact OOF or
blocked validation is safer than a trace-only proxy.

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

## Foldwise Shrinkage Ratios

One way to inspect unstable coefficient geometry is to compare the slope learned
on training folds with the slope implied by held-out folds. In a principal or
otherwise orthogonalized basis:

```text
r_i,k = alpha_val_i,k / alpha_train_i,k
```

where `i` indexes the direction and `k` indexes the fold. If `r_i,k` is
consistently below one, the direction is too large in training relative to
validation. If it changes sign or varies wildly, the direction is probably not a
stable signal.

This is a diagnostic first. Turning ratios into penalties requires pooling and
nested discipline:

- aggregate ratios by median, trimmed mean, Huber estimate, or
  inverse-variance weighting;
- smooth ordered principal components when signal should decay by spectrum;
- use groups or bands when the basis directions correspond to feature families;
- choose the pooling rule inside training folds, then emit held-out predictions;
- reserve a later period for final testing.

The danger is subtle leakage. A ratio computed on the same held-out rows later
used to score the model has already consumed those labels. Treat per-direction
shrinkage exactly like feature selection or stacking: it must be cross-fitted
before downstream validation.

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

[Linear Regression Identities And Solvers](linear-regression-identities-and-solvers.md)
owns the underlying OLS algebra: sufficient statistics, leverage computation,
GCV approximations, level-set geometry, sketching, and solver choice. This page
uses those identities to choose validation protocols.

The two pages should stay linked:

- use temporal evidence to discover where effects appear stable;
- use validation protocols to decide whether a model using those effects should
  be trusted.

## Proxy Targets

Changing the target can be a stronger inductive bias than changing the
regularization value. A shorter-horizon or easier proxy target can produce a
prediction that beats every point on the direct long-horizon ridge path when the
long target has lower SNR or unstable cross moments.

Validation should treat this as a different estimator, not as "just more
regularization." For train and validation matrices:

```text
beta_direct(lambda) = (G_train + lambda I)^-1 X_train^T y_long
beta_proxy(mu)      = (G_train + mu I)^-1 X_train^T y_short
```

The proxy can win because it changes the direction of `X^T y`, while ridge only
shrinks or rotates within the geometry induced by the same target. In an
orthogonalized design this is especially clear: each target defines a different
ray, and regularization mostly chooses position along the ray.

Practical validation pattern:

- choose source horizons on a small ordered grid;
- generate OOF proxy predictions for each source horizon;
- evaluate them on the true deployment target with purged or rolling folds;
- fit any calibration or horizon recombination using only training-fold data;
- keep a final later period untouched, because source-horizon search is feature
  selection over targets.

If a proxy target repeatedly wins, the next step is usually a structured
horizon model or proximal continuation across horizons, not a one-off
hard-coded source horizon.

## Selection Paths

Feature selection procedures create their own validation risk. Least Angle
Regression, lasso paths, forward stagewise regression, and greedy feature search
all expose a path of candidate models rather than a single model.

The path is useful because it shows when predictors enter, whether correlated
features share credit, and how sparse explanations evolve. It is also a leakage
risk when the path is chosen on all rows before validation. The validation rule
is:

```text
for each fold:
  fit the entire selection path on training rows
  choose path position using training-internal risk or nested validation
  emit held-out predictions
```

For p12n, sparse selection should be judged by blocked OOF performance and
temporal evidence stability, not only by entry order or in-sample residual
correlation.

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
- [Branch - Proxy-target training in regression](../../../ops/artifacts/chatgpt/69d5ed83-dbb4-83a1-b4fd-1f878f014cf9.md)
- [Least Angle Regression Explained](../../../ops/artifacts/chatgpt/674c0a48-e938-8009-94fa-c205a686cd89.md)
- [Optimal Ridge Penalty Computation](../../../ops/artifacts/chatgpt/6876f4ab-b368-8009-9320-b72c69c8ce00.md)
- [Ridge Penalty Optimization](../../../ops/artifacts/chatgpt/6876f4ac-77cc-8009-8b48-a1327e12c379.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
