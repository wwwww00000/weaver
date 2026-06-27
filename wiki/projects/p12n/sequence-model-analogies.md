---
title: Sequence-Model Analogies
status: draft
page_type: research-thread
projects:
  - p12n
categories:
  - quant
  - trading
  - machine-learning
  - sequence-modeling
  - time-series
source_bundles:
  - p12n/ai
  - p12n/quant
  - p12n/current priorities
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/p12n
related:
  - projects/p12n
  - projects/p12n/temporal-returns-experiments
  - projects/p12n/n-linear-returns-models
  - topics/quant/temporal-evidence
created: 2026-06-27
updated: 2026-06-27
---

# Sequence-Model Analogies

This thread translates modern sequence-model ideas into p12n primitives that can
be fitted, inspected, and controlled in a low-SNR trading setting.

The goal is not to turn p12n into a generic RNN or transformer research project.
The goal is to borrow the useful structure: fast weights, temporal bases,
adaptive memory, linear attention, gating, and stagewise recurrence, then express
them in a form compatible with regression diagnostics and conservative
validation.

## Design Pressure

P12n wants the expressiveness of sequence models without giving up the practical
advantages of the current quant workflow:

- explicit temporal and asset structure;
- closed-form or least-squares subproblems when possible;
- stable baselines that can be recovered by turning off extra components;
- interpretable per-sample or per-window diagnostics;
- strong controls against long-horizon and low-SNR overfitting.

The current default should be conservative: start with fixed temporal bases and
adaptive mixing before introducing learned recurrence.

## Fast Weights And Online Regression

One useful analogy is to treat recurrent state as fast parameters of a local
predictor.

In this view, a state update is not just "memory." It is an online estimation
step:

```text
fast_state_{t+1} = update(fast_state_t, features_t, error_or_surprise_t)
prediction_t     = readout(fast_state_t, features_t)
```

Adaptive filtering gives concrete versions of this pattern:

- LMS as streaming gradient descent on a linear head;
- normalized LMS as scale-corrected fast updating;
- RLS as recursive least squares with a forgetting factor;
- affine projection methods as small-window least-squares updates;
- set-membership filtering as update-only-when-surprised logic.

For p12n, the most plausible first use is not a giant test-time-trained model.
It is a small fast module: a local linear head, a decay mixer, a low-rank adapter,
or a bank of expert coefficients that can be updated with explicit forgetting
and inspected like a regression.

The reusable method background is split out in
[Adaptive Filters And EMA](../../topics/quant/adaptive-filters-and-ema.md).

## Benchmarking Recurrent Updates

Even when a recurrent state was not designed as an optimizer, it can be diagnosed
against optimizer-like targets.

For a state `h_t` and loss at time `t`, compute an offline diagnostic gradient:

```text
g_t = grad_h loss(g_theta(h, x_t), y_t) at h = h_{t-1}
delta_h_t = h_t - h_{t-1}
```

Then inspect:

- cosine alignment between `delta_h_t` and `-g_t`;
- the best-fit scalar step size;
- residual update energy not explained by a gradient step;
- whether a linear preconditioner explains updates;
- whether the update field has large antisymmetric or rotational components.

This is mostly a diagnostic, not necessarily a runtime prescription. In an
ordinary forecasting setup, the transition does not have access to future
targets. The gradient-like comparison is still useful for deciding whether a
candidate recurrence behaves like adaptation, smoothing, rotation, gating, or
something harder to interpret.

## Timescale-Separated State

The simplest sequence-model import is a fixed bank of state channels with known
decays:

```text
s_{t+1,j} = alpha_j s_{t,j} + (1 - alpha_j) g_j(x_t)
```

This gives p12n an interpretable basis of memory half-lives. Horizon-specific
readouts can then decide which timescales matter, with explicit regularization
by horizon. This is close to a diagonal SSM, minGRU-like recurrence, or EMA
feature bank, but it remains easy to reason about.

Useful controls:

- log-spaced fixed half-lives;
- horizon-wise ridge or degrees-of-freedom targets;
- smoothness penalties across forecast horizon;
- residualized fitting from short horizons to longer horizons;
- pruning or grouping entire timescale channels.

This should be the first stop before dynamic gates. If fixed decays plus
adaptive linear mixing do not validate, a more flexible recurrence is unlikely
to be trustworthy.

## Linear Attention

Linear attention is useful in p12n less as a transformer imitation and more as a
structured regression view.

A simple scalar-value linear attention model can be written:

```text
q_t = W_Q x_t
k_t = W_K x_t
v_t = w_V^T x_t
s_t = s_{t-1} + k_t v_t
y_hat_t = q_t^T s_t
```

This has three useful interpretations:

- a recurrent sufficient-statistics accumulator;
- a low-rank tensor regression over current and past features;
- a fast-weight memory with keys, queries, and scalar values.

The optimization is structured. With some blocks frozen, the other blocks can
often be updated by ridge-like subproblems, alternating least squares, or
Gauss-Newton/Levenberg-Marquardt. That makes it closer to p12n's preferred
numerical style than an opaque end-to-end transformer block.

The link to [N-Linear Returns Models](n-linear-returns-models.md) is direct:
source asset and lag structure act like keys, target-asset exposure acts like
queries, raw returns act like values, and diagonal self effects should remain
explicit rather than hidden in the value map.

## Gates From Filtering

Kalman filtering gives a clean theoretical motivation for gates.

In a scalar linear Gaussian model, the posterior mean update can be written:

```text
x_hat_t = (1 - K_t) a x_hat_{t-1} + K_t y_t
```

Here `K_t` behaves like an update gate. It opens when observations are reliable
or prior uncertainty is high, and closes when observations are noisy or the
state estimate is already confident.

The useful mapping is:

- `R_t` measurement noise controls the input/update gate;
- `Q_t` process noise controls forgetting or state drift;
- posterior covariance `P_t` is a hidden confidence state;
- innovation quality can drive adaptive noise or regime updates.

For p12n this suggests a small, tractable design pattern: track innovation or
prediction-error summaries, then let those summaries modulate decay, update
strength, or model weights. That is more interpretable than making every
recurrent parameter fully dynamic.

## Temporal Regime Descriptors

The cleanest motivation for regime descriptors is predictive compression.

A useful regime state should encode the part of history that changes the future
law, not merely a cluster label. In p12n terms, a regime descriptor should earn
its keep by improving future return, fill, volatility, or execution behavior,
while remaining low-capacity and slow enough not to chase noise.

Practical versions:

- low-dimensional sticky regime variables;
- slow gates over timescale banks;
- mixture weights over a small set of filters;
- predictive bottleneck or contrastive future summaries as auxiliary training
  signals;
- innovation-driven mode probabilities as a filtering-inspired alternative.

This is a later-stage idea. The first p12n pass should prefer explicit temporal
bases and evidence diagnostics before adding learned latent regimes.

## Stagewise Fitting

The preferred p12n synthesis of these ideas is stagewise sequence modeling.

Start with a baseline, inspect residuals or gradient-like diagnostics, add one
small recurrent primitive, validate it, then refit only controlled pieces. A
stage should define:

- the residual or evidence object it tries to explain;
- the module family being added;
- the fitting objective;
- the stability and regularization constraints;
- the contribution trace used for interpretation;
- the validation rule for keeping or rejecting it.

Candidate primitive library:

- fixed EMA or temporal basis bank;
- dynamic decay EMA with heavy regularization;
- shock or impulse channel;
- low-rank linear attention channel;
- mixture-of-timescales gate;
- local regression or RLS-style fast head;
- Kalman-inspired innovation gate.

This is the bridge between modern sequence-model expressiveness and p12n's need
for auditability. Each primitive should be removable, residualized, and tested
for incremental validation value.

## Open Questions

- Which recurrence primitives actually add validation lift beyond fixed temporal
  bases?
- Which diagnostics should trigger a dynamic decay module versus a nonlinear
  feature transform?
- Can fast-weight ideas be implemented as small structured adapters rather than
  whole-model test-time training?
- How much of linear attention's value is captured by n-linear diagonal plus
  low-rank return operators?
- What innovation summaries are stable enough to drive gates in crypto data?
- Can stagewise recurrence remain identifiable after several modules are added?

## Source Map

- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
- [p12n overview](../../../ops/artifacts/obsidian/p12n-overview.md)
- [Adaptive Filtering in Sequence Models](../../../ops/artifacts/chatgpt/69992303-31c0-839c-8f32-640d3fbc88a1.md)
- [Benchmarking Recurrent State Updates](../../../ops/artifacts/chatgpt/694bb258-cdb0-8322-bc06-8e605305a9f5.md)
- [Fixed RNN with Interpretable Optimization](../../../ops/artifacts/chatgpt/698c58da-57a4-83a1-9602-bead070b12bf.md)
- [Optimization of linear attention](../../../ops/artifacts/chatgpt/693be35d-abc0-8324-94c3-829b017f3382.md)
- [RNN architecture design](../../../ops/artifacts/chatgpt/690030a3-f2d8-8323-8d98-505aaad9c238.md)
- [Sequence Model Literature Review](../../../ops/artifacts/chatgpt/69698dfb-0798-8322-a395-371306852c5d.md)
- [Stagewise Sequence Modeling](../../../ops/artifacts/chatgpt/6951463c-52b0-8321-b465-d273b01f9ee9.md)
- [Kalman Filter and Gating](../../../ops/artifacts/chatgpt/69b0226e-f6f4-839c-a508-b8e93f3d06d6.md)
- [Temporal Regime Descriptors](../../../ops/artifacts/chatgpt/69bf98fa-60ac-839b-8800-2816de8748c8.md)
