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
  - unassigned/ai
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/p12n
related:
  - projects/p12n
  - projects/p12n/temporal-returns-experiments
  - projects/p12n/n-linear-returns-models
  - topics/quant/temporal-evidence
  - topics/quant/adaptive-filters-and-ema
created: 2026-06-27
updated: 2026-06-28
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

A diagonal state-space model is the next boundary to understand. A scalar
state-space duality uses one decay structure across the hidden state; a diagonal
version lets each state channel have its own time-varying decay. Conceptually,
this is still a bank of fading memories before it is a general recurrent
network. That makes it a useful midpoint for p12n:

- fixed diagonal decays become an interpretable memory basis;
- learned diagonal decays become gated timescale channels;
- readout weights can still reveal which half-lives and state channels matter;
- full hidden-state mixing should remain a later step, because it is much
  harder to inspect.

The practical read is that many "SSM versus attention" distinctions collapse
into how a model stores and reads from structured temporal state. P12n should
exploit the structured-state side first.

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

The same mechanism can be written as a recurrent prefix update: accumulate
`phi(k_t) v_t^T` and a normalizer, then read the current output with `phi(q_t)`.
That makes linear attention trainable with parallel prefix-scan machinery while
still running as a streaming recurrent state at inference time. For p12n, this
is a useful constraint: the memory is not arbitrary context. It is a low-rank
bank of sufficient statistics whose saturation, forgetting, and normalization
can be inspected.

The optimization is structured. With some blocks frozen, the other blocks can
often be updated by ridge-like subproblems, alternating least squares, or
Gauss-Newton/Levenberg-Marquardt. That makes it closer to p12n's preferred
numerical style than an opaque end-to-end transformer block.

The link to [N-Linear Returns Models](n-linear-returns-models.md) is direct:
source asset and lag structure act like keys, target-asset exposure acts like
queries, raw returns act like values, and diagonal self effects should remain
explicit rather than hidden in the value map.

## Gated Layers As Product Features

Many neural gated layers have the rough form:

```text
output = value(x) * gate(x)
```

If the gate is locally affine, or if it is replaced by bins, splines, or other
explicit basis functions, the layer begins to look like a bilinear model or a
linear model over product features. For p12n this is useful because product
features can be fitted with ridge, inspected as regression terms, and validated
with the same machinery used for tabular nonlinearities.

Useful translations:

- feature value times current feature bin;
- timescale state times regime descriptor;
- EMA state times volatility or liquidity bucket;
- source-asset return times target-asset exposure;
- forecast output times execution-context bucket.

The caveat is composition. A single product-feature layer is still linear in its
expanded basis, but stacking multiple product-feature layers makes downstream
predictions nonlinear in hidden outputs. That loses the clean closed-form solve
unless the workflow changes.

Practical workarounds are:

- flatten the desired products into one explicit feature map and solve once;
- freeze upstream transforms, then solve only the readout;
- add product-feature components stagewise with out-of-fold residual targets;
- use Gauss-Newton or alternating least squares only for small controlled
  nonlinear blocks;
- promote a gated module only after the explicit product-feature version has
  validation lift.

This makes gated-layer research useful as a feature-design lens, not as an
argument for building a deep stack before the shallow regression analogue has
failed.

The same caution applies to gated recurrence. A minimal gated cell can be
written as:

```text
h_t = f_t h_{t-1} + (1 - f_t) W x_t
```

If the gates are fixed, the hidden states form a temporal basis and the readout
can be treated like an ordinary regression problem. If the gates are learned
from current inputs, the recurrence becomes nonlinear through products over
time. That suggests an incremental fitting route: fit fixed or externally
defined gates first, solve the linear pieces, then consider alternating updates
or local linearizations for the gate parameters only if the fixed-gate version
has validation lift.

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

The candidate ordering should be:

1. fixed half-life banks and explicit product features;
2. diagonal state channels with regularized horizon-specific readouts;
3. low-rank linear-attention accumulators with explicit forgetting;
4. input-driven gates over a small state bank;
5. deeper learned recurrence only if the earlier stages fail cleanly.

This keeps the modern sequence-model import concrete. The first four stages can
all be expressed as inspectable state updates plus regression-like readouts.

## Open Questions

- Which recurrence primitives actually add validation lift beyond fixed temporal
  bases?
- Which diagnostics should trigger a dynamic decay module versus a nonlinear
  feature transform?
- Can fast-weight ideas be implemented as small structured adapters rather than
  whole-model test-time training?
- How much of linear attention's value is captured by n-linear diagonal plus
  low-rank return operators?
- Which gated-layer ideas are already captured by explicit product features and
  which require true learned composition?
- What innovation summaries are stable enough to drive gates in crypto data?
- Can stagewise recurrence remain identifiable after several modules are added?

## Source Map

- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
- [p12n overview](../../../ops/artifacts/obsidian/p12n-overview.md)
- [Adaptive Filtering in Sequence Models](../../../ops/artifacts/chatgpt/69992303-31c0-839c-8f32-640d3fbc88a1.md)
- [Benchmarking Recurrent State Updates](../../../ops/artifacts/chatgpt/694bb258-cdb0-8322-bc06-8e605305a9f5.md)
- [Gated Layers and Approximations](../../../ops/artifacts/chatgpt/6728c741-b2f8-8009-b3e5-c1fabd74ad94.md)
- [Fixed RNN with Interpretable Optimization](../../../ops/artifacts/chatgpt/698c58da-57a4-83a1-9602-bead070b12bf.md)
- [Optimization of linear attention](../../../ops/artifacts/chatgpt/693be35d-abc0-8324-94c3-829b017f3382.md)
- [RNNs as Transformers](../../../ops/artifacts/chatgpt/68355831-4d24-8009-854b-57da7ec562f8.md)
- [Simplified Gated RNN](../../../ops/artifacts/chatgpt/6752ad04-8df8-8009-bcf0-6001804e4628.md)
- [State-Space Duality Explanation](../../../ops/artifacts/chatgpt/6a0a66e5-699c-83ec-a8f5-d3af30104eb1.md)
- [RNN architecture design](../../../ops/artifacts/chatgpt/690030a3-f2d8-8323-8d98-505aaad9c238.md)
- [Sequence Model Literature Review](../../../ops/artifacts/chatgpt/69698dfb-0798-8322-a395-371306852c5d.md)
- [Stagewise Sequence Modeling](../../../ops/artifacts/chatgpt/6951463c-52b0-8321-b465-d273b01f9ee9.md)
- [Kalman Filter and Gating](../../../ops/artifacts/chatgpt/69b0226e-f6f4-839c-a508-b8e93f3d06d6.md)
- [Temporal Regime Descriptors](../../../ops/artifacts/chatgpt/69bf98fa-60ac-839b-8800-2816de8748c8.md)
