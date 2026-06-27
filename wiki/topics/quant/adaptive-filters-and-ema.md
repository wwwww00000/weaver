---
title: Adaptive Filters And EMA
status: draft
page_type: method-note
projects:
  - p12n
  - obelisk
categories:
  - quant
  - online-learning
  - temporal-modeling
  - filtering
  - time-series
source_bundles:
  - p12n/quant
  - p12n/ai
  - obelisk/quant
  - unassigned/quant
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/quant
related:
  - projects/p12n/sequence-model-analogies
  - projects/obelisk/dynamic-ema-decay
  - topics/quant/temporal-evidence
created: 2026-06-27
updated: 2026-06-27
---

# Adaptive Filters And EMA

Adaptive filters are the reusable method layer behind dynamic EMA decay,
test-time regression, fast weights, Kalman-style gates, and local online
regression.

The common question is:

```text
How should a model update a small state or parameter block as new observations
arrive?
```

For p12n and Obelisk, this matters because the market is nonstationary but
low-SNR. A model needs to adapt, but most adaptive freedom should be small,
regularized, and inspectable.

## EMA As The Base Case

An EMA is the simplest adaptive filter:

```text
m_t = m_{t-1} + alpha (x_t - m_{t-1})
```

The decay `alpha` is a learning rate. Small `alpha` gives long memory and low
variance. Large `alpha` reacts quickly but chases noise.

This makes an EMA a useful primitive for:

- volatility estimates;
- edge or return baselines;
- stateful feature transforms;
- fixed temporal basis banks;
- simple dynamic-memory channels.

The first robust design pattern is not to learn one flexible decay immediately.
Maintain a bank of fixed decays, fit their mixture weights, and only then ask
whether the decay itself needs to become dynamic.

## LMS And NLMS

Least-mean-squares filtering is online gradient descent on a linear predictor:

```text
w_{t+1} = w_t + mu x_t (y_t - w_t^T x_t)
```

Normalized LMS rescales the update:

```text
w_{t+1} = w_t + mu x_t e_t / (epsilon + ||x_t||^2)
```

The normalized version is often the better analogy for sequence models because
feature magnitudes drift. It is the adaptive-filter version of "do not let a
large feature vector create a huge fast-weight update."

For p12n, LMS-like rules are plausible for small local heads or adapters, but
they should be benchmarked against batch or rolling least-squares baselines
before being used as live modeling primitives.

## RLS And Recursive Least Squares

Recursive least squares tracks the exponentially weighted least-squares
solution online:

```text
min_w sum_i lambda^{t-i} (y_i - w^T x_i)^2 + ridge
```

The state includes both coefficients and an inverse covariance or preconditioner
`P_t`. The update is therefore much more curvature-aware than LMS.

RLS is the cleanest bridge between:

- online regression;
- in-context least-squares;
- covariance-normalized linear attention;
- Kalman filtering for drifting regression coefficients;
- recursive prediction-error methods.

The cost is state size. Full `P_t` is a `p x p` object, so exact RLS belongs on
small or structured parameter blocks: low-rank adapters, per-feature groups,
small expert heads, or diagonal/block approximations.

## Kalman View

A drifting linear regression can be written as:

```text
beta_t = beta_{t-1} + w_t
y_t = x_t^T beta_t + v_t
```

with:

```text
w_t ~ N(0, Q)
v_t ~ N(0, R)
```

The Kalman filter keeps a mean coefficient estimate and a covariance:

```text
m_{t|t-1} = m_{t-1|t-1}
P_{t|t-1} = P_{t-1|t-1} + Q
nu_t      = y_t - x_t^T m_{t|t-1}
S_t       = x_t^T P_{t|t-1} x_t + R
K_t       = P_{t|t-1} x_t S_t^{-1}
m_{t|t}   = m_{t|t-1} + K_t nu_t
```

This is recursive least squares with explicit uncertainty semantics:

- `Q` is coefficient drift or forgetting;
- `R` is observation noise or caution;
- `P_t` is confidence in the coefficients;
- `K_t` is an adaptive learning-rate vector;
- `nu_t` is the innovation or surprise signal.

This framing is useful because it turns update strength into a statistical
quantity rather than an arbitrary gate.

## Gates From Uncertainty

Kalman filtering also gives a clean story for recurrent gates.

In a scalar model:

```text
x_hat_t = (1 - K_t) a x_hat_{t-1} + K_t y_t
```

The gain `K_t` behaves like an update gate. It opens when the observation is
reliable or the prior is uncertain. It closes when the observation is noisy or
the prior is already confident.

The useful mapping is:

- measurement noise `R_t` controls input trust;
- process noise `Q_t` controls memory drift;
- covariance `P_t` is the hidden confidence state;
- innovation statistics can drive dynamic gates.

This is the principled version of a gated EMA. A learned gate can be interpreted
as a neural approximation to an uncertainty-controlled Kalman gain.

## Choosing How Much To Forget

There are several ways to make forgetting dynamic.

Scalar forgetting:

- use innovation magnitude or error statistics;
- reduce the forgetting factor when residuals remain large;
- use change detection to open adaptation only after a regime break;
- use set-membership rules to update only enough to satisfy an error bound;
- run a mixture of filters with different forgetting factors and weight them by
  likelihood.

Directional forgetting:

- forget only along currently excited feature directions;
- preserve directions that current data cannot relearn;
- use low-rank or diagonal approximations for practical implementations;
- apply different forgetting rates per feature group or state slot.

The scalar question is "how quickly should the memory decay?" The directional
question is "which parts of memory are safe to decay?" They solve different
problems and should not be collapsed into a single gate.

## Innovation-Driven Adaptation

The innovation:

```text
nu_t = y_t - y_hat_{t|t-1}
```

is the canonical adaptive signal in filtering. In a well-specified model,
innovations should be approximately zero-mean, correctly scaled, and weakly
autocorrelated.

Useful diagnostics:

- innovation magnitude;
- normalized innovation squared;
- rolling innovation variance;
- short-lag innovation autocorrelation;
- residual whiteness;
- calibration of predicted versus realized error variance.

Possible adaptations:

- increase `R_t` when observations look unreliable;
- increase `Q_t` or inflate `P_t` when the model is overconfident or stale;
- switch probability mass across a bank of filters;
- increase a local learning rate only when persistent mismatch appears.

This is the filtering counterpart to p12n's desire to use prediction accuracy as
a meta-signal for memory and recurrence.

## Dynamic EMA

The Obelisk dynamic EMA thread is the project-specific version of this method.
The simplest gated EMA uses standardized surprise:

- ordinary residuals use a slow baseline decay;
- large surprises use a faster decay;
- post-shock release prevents the estimate from staying elevated too long.

The important caution is that same-step fitting of a decay is usually
degenerate: the fastest decay wins if the objective only rewards matching the
current observation. Decay adaptation needs a future loss, calibration loss, or
outer validation objective.

For low-SNR trading, fixed EMA banks plus learned or validated mixtures are often
a better first move than fully dynamic decay.

## Relationship To Temporal Evidence

[Temporal Evidence](temporal-evidence.md) studies whether regression evidence is
stable over time. Adaptive filters decide how to update an online state after
that evidence has been observed.

A sensible workflow is:

1. use temporal evidence to identify stable lag, window, or basis structures;
2. fit fixed EMA or lag-basis models;
3. validate adaptive mixtures or scalar forgetting;
4. only then try directional forgetting, local RLS, or Kalman-inspired gates.

This keeps the adaptive machinery from becoming a noise amplifier.

## Implementation Guidance

Prefer this escalation order:

1. fixed decay bank;
2. fitted mixture of fixed decays;
3. scalar dynamic decay from innovation statistics;
4. diagonal or grouped forgetting;
5. small RLS/Kalman readout;
6. directional forgetting or low-rank covariance updates;
7. learned nonlinear gates.

Keep each adaptive state small enough to inspect. Log the effective decay,
innovation, update size, and contribution trace. Validate adaptive components by
incremental out-of-sample value, not by prettier state plots.

## Open Questions

- Which p12n states are worth adapting: return filters, execution thresholds,
  local heads, or decay mixers?
- Should innovation statistics drive `Q`, `R`, direct gates, or filter mixture
  weights?
- When is full covariance tracking worth the cost compared with diagonal or
  grouped approximations?
- Which dynamic decay objectives avoid same-step degeneracy while remaining
  cheap enough for experimentation?
- How should adaptive filters be cross-validated under temporal dependence?

## Source Map

- [Adaptive Filtering in Sequence Models](../../../ops/artifacts/chatgpt/69992303-31c0-839c-8f32-640d3fbc88a1.md)
- [Kalman Filter and Gating](../../../ops/artifacts/chatgpt/69b0226e-f6f4-839c-a508-b8e93f3d06d6.md)
- [Kalman filter update intuition](../../../ops/artifacts/chatgpt/69b21439-56cc-8399-9022-6f58147ac799.md)
- [Kalman Filter State-Space Integration](../../../ops/artifacts/chatgpt/69abc878-f2a0-83a0-b672-01b48fb393d9.md)
- [Dynamic EMA Decay](../../projects/obelisk/dynamic-ema-decay.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
