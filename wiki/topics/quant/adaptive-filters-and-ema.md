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
updated: 2026-06-28
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

## Working Stance

The conservative design rule is:

```text
fixed filters before learned filters;
filter mixtures before dynamic decay;
small adaptive readouts before learned latent recurrence.
```

Most of the useful ideas in this area can be arranged as a ladder:

1. fixed lag, EMA, pole, or dyadic-bin feature banks;
2. orthogonalized or residualized versions of those banks;
3. linear mixtures of fixed filters, fitted by OLS, ridge, or validation;
4. one or a few shared dynamic decay channels;
5. RLS, Kalman, or local online-regression modules on small state blocks;
6. learned recurrent gates only after the earlier levels validate.

This ordering matters because low-SNR time series make dynamic freedom look
better in-sample than it is. A dynamic decay or fast-weight module should have
to beat a fixed bank plus regularized mixing before it earns complexity.

## EMA As The Base Case

An EMA is the simplest adaptive filter:

```text
m_t = rho m_{t-1} + alpha x_t
alpha = 1 - rho
```

The update weight `alpha` is a learning rate. Small `alpha` gives long memory
and low variance. Large `alpha` reacts quickly but chases noise.

Use half-life notation when possible:

```text
rho = exp(-log(2) / H)
alpha = 1 - rho
```

where `H` is the number of samples needed for an old observation to lose half
its weight.

An EMA is useful for:

- volatility estimates;
- edge or return baselines;
- stateful feature transforms;
- fixed temporal basis banks;
- simple dynamic-memory channels.

The first robust design pattern is not to learn one flexible decay immediately.
Maintain a bank of fixed decays, fit their mixture weights, and only then ask
whether the decay itself needs to become dynamic.

## Startup Bias And Normalization

Zero-initialized EMAs have startup bias. The Adam-style correction is:

```text
corrected_m_t = m_t / (1 - rho^t)
```

The more general implementation is to track accumulated exponential weight:

```text
s_t = rho s_{t-1} + alpha w_t x_t
c_t = rho c_{t-1} + alpha w_t
m_t = s_t / c_t
```

With `w_t = 1`, this is algebraically the same correction. The denominator view
is more useful in production because it extends to missing data, sparse events,
irregular clocks, and reliability-weighted observations.

## Fixed Banks And Filter Mixtures

A fixed bank converts decay selection into linear modeling:

```text
s_{k,t} = alpha_k x_t + rho_k s_{k,t-1}
z_t = sum_k theta_k s_{k,t}
```

Once the `rho_k` values are fixed, `theta` can be fitted by OLS, ridge, lasso,
or a convex constrained solve. This is usually a better first move than
backpropagating through a free half-life.

The same trick supports simple dynamic mixtures without a recurrent optimizer.
Let side information `u_t` choose mixture weights linearly:

```text
z_t = sum_k sum_c gamma_{k,c} u_{t,c} s_{k,t}
```

The unknowns `gamma_{k,c}` still enter linearly, so the batch solve stays
ordinary regression. If the weights must be nonnegative or sum to one, use
nonnegative least squares or a small quadratic program.

Use a log-spaced half-life grid first. Numerical half-life optimization is
possible, but recursive gradients can be ill-conditioned for long memory. A
grid plus regularized mixing is easier to validate, easier to inspect, and
often close enough.

## EMA Geometry In Regression

Let `S` be the linear EMA operator. If predictions are smoothed before scoring,
the exact objective is:

```text
min_beta ||S X beta - y||^2
```

The gradient is:

```text
2 X^T S^T (S X beta - y)
```

Several useful consequences follow.

First, smoothing the predictions is equivalent to smoothing each feature column
before ordinary regression:

```text
S X beta = (S X) beta
```

This is exact but can make an originally orthogonal design non-orthogonal.

Second, inverting the EMA on the target is not, by itself, the same Euclidean
least-squares problem. If `y_star = S^-1 y`, then:

```text
||S X beta - y||^2 = (X beta - y_star)^T S^T S (X beta - y_star)
```

So target inversion changes the problem into weighted least squares under the
`S^T S` metric. It may be a useful re-expression or approximation, but the
original loss still requires the EMA-induced geometry.

Third, some cross-terms can be amortized. For scalar screening with one
predictor `x_j` and one half-life:

```text
beta_hat = (x_j^T S^T y) / (x_j^T S^T S x_j)
```

The numerator can be pushed to the target side by computing a backward EMA
`S^T y` once per half-life. The denominator still depends on the predictor's
autocorrelation under the EMA kernel, so it cannot be removed in general.

This is the right mental model: EMAs are cheap linear filters, but they change
the inner product. Shortcuts that ignore the changed inner product are
approximations unless the design has a special structure.

## Orthogonal And Multiscale Bases

Raw EMA banks are heavily collinear. Several replacements keep the same
fading-memory spirit while reducing redundancy.

Difference-of-EMA features create approximate bands:

```text
d_1 = EMA_{H_1}(x)
d_k = EMA_{H_k}(x) - EMA_{H_{k-1}}(x)
```

These are not exactly orthogonal, but they often capture the incremental
information at each timescale better than the raw levels.

Disjoint moving averages give a causal multiresolution summary:

```text
last 1 sample,
previous 2 samples,
previous 4 samples,
previous 8 samples,
...
```

The bins have disjoint support, so they avoid double-counting history. Adding
Haar-like detail features, such as newer-half minus older-half inside each bin,
recovers trend information that plain bin averages lose.

For a more formal filter basis, use:

- empirical whitening of an EMA bank;
- Gram-Schmidt on the EMA kernels;
- Laguerre or Kautz orthonormal basis functions;
- PCA or PLS on the realized EMA design if interpretability is less important.

The practical choice is usually between difference-of-EMAs for interpretability
and whitening for numerical conditioning.

## Pole Grids And Differencing

EMA filters are real one-pole filters. A complex pole pair:

```text
lambda = r exp(i theta)
```

has a damped sinusoidal impulse response. Even when the data are not truly
periodic, the angle can act like a differencing or band-pass primitive.

The angle implies a pseudo-period:

```text
T = 2 pi / theta
```

A useful bound is to choose `r` so that the response is mostly gone after a few
pseudo-periods:

```text
r^(k T) ~= eps
r = exp(-log(1 / eps) / (k T))
```

This avoids high-angle filters with unrealistically long memory. If the input is
already differenced at lag `ell`, then the matching angle is roughly:

```text
theta ~= pi / ell
```

In that case the differencing has already supplied the zero in the spectrum, and
the corresponding complex pole may be redundant.

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

## EKF And Nonlinear Online Regression

The extended Kalman filter keeps the same online-regression interpretation after
local linearization.

For drifting nonlinear regression:

```text
beta_t = beta_{t-1} + w_t
y_t = g(beta_t; x_t) + v_t
```

the EKF linearizes `g` around the current estimate and applies a Kalman update
using the Jacobian:

```text
J_t = d g(beta; x_t) / d beta
```

This is an online Gauss-Newton or local MAP update, not an exact nonlinear
Bayesian update. It is useful when the nonlinearity is mild and the state has a
clear meaning, such as drifting coefficients.

The warning is that state-space features and time-varying coefficients multiply
into a bilinear observation if both are latent:

```text
y_t = beta_t^T z_t + noise
```

That is no longer an ordinary Kalman filter. The cleaner design is usually:

```text
state-space feature extractor -> filtered feature estimate -> adaptive linear readout
```

Use the Kalman/RLS machinery for the adaptive readout, and learn or specify the
feature dynamics separately.

## RTRL-Style Fast Adapters

A small fast adapter can be trained online while the larger recurrent model is
treated as fixed. For a gated state:

```text
h_t = g_t * (x_t theta(i_t)) + (1 - g_t) * h_{t-1}
```

where `theta(i_t)` is a scalar category adapter, maintain the RTRL trace:

```text
e_t^(k) = (1 - g_t) * e_{t-1}^(k)
          + 1[i_t = k] * g_t * x_t
```

Then:

```text
d y_hat_t / d theta_k = grad_h y_hat_t dot e_t^(k)
```

This keeps the online update local and inspectable. It also separates two
different traces:

- the RTRL trace through the recurrent state;
- the target or credit-assignment trace used for delayed returns.

For discounted-return targets, exact supervised learning requires either
waiting for the full target or buffering enough past prediction gradients. TD
and TD(lambda) introduce bootstrapping to collapse that temporal credit into a
single exponentially decayed trace. That is useful, but it is a modeling choice,
not merely an algebraic reordering of the supervised loss.

There is also a useful two-pole intuition. The recurrent state has a memory pole
such as `1 - g`, while the target trace has a credit pole such as
`gamma * lambda`. If both are close to one, or close to each other, the effective
learning kernel can become very long-tailed and noisy. This is a reason to tune
feature memory and target-credit memory separately.

## Shared Decay And Sparse Updates

When many channels share the same dynamic decay:

```text
h_{t,k} = g_t h_{t-1,k} + u_{t,k}
```

factor out the cumulative decay:

```text
C_t = product_{s <= t} g_s
q_{t,k} = h_{t,k} / C_t
q_{t,k} = q_{t-1,k} + u_{t,k} / C_t
```

Now inactive channels need no update. This is the main efficiency trick for
sparse event features: the global decay is paid once, and each feature stores an
undecayed offset. Materialize `h_k = C_t q_k` only when needed.

If every channel is dense and the full vector is needed every step, this
factorization is mostly a reparameterization. Its value comes from sparsity,
lazy materialization, and shared dynamic decay.

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

## Long-Memory Failure Modes

Very long EMAs can fail abruptly in low-SNR interaction models.

The main failure is effective-sample-size collapse. A long EMA is highly
autocorrelated, so adjacent rows stop providing independent evidence. When that
state is then crossed with bins, products, or nonlinear interactions, the model
can create many apparent degrees of freedom over only a small number of
effective samples.

Common symptoms:

- interaction bins with tiny occupancy;
- large condition-number or variance-inflation jumps;
- validation lift that disappears under gap or block splits;
- long-lag features that behave like slow levels rather than new information;
- ridge penalties that shrink coefficients but do not fix the lack of data.

Useful controls:

- cap half-lives relative to forecast horizon unless there is strong evidence;
- use difference-of-EMAs or residualized long-memory channels;
- penalize terms involving long-memory features more heavily;
- validate with gaps at least as long as the longest relevant memory;
- avoid high-order products involving near-constant slow state;
- use low-rank or hierarchical interaction surfaces instead of full bin grids.

For sparse event streams, a plain EMA can also saturate during bursts. Prefer a
linear hidden state with a concave readout first:

```text
u_t = rho u_{t-1} + x_t
z_t = log(1 + u_t)
```

Other useful variants are count/mass normalization, crowding-corrected updates,
bounded-capacity updates, decayed max, and refractory-state downweighting. Keep
the state update linear unless the nonlinear update itself is needed.

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
2. orthogonalized or residualized fixed bank;
3. fitted mixture of fixed decays;
4. scalar dynamic decay from innovation statistics;
5. diagonal or grouped forgetting;
6. small RLS/Kalman readout;
7. RTRL-style adapter on a small state block;
8. learned nonlinear gates.

Keep each adaptive state small enough to inspect. Log the effective decay,
innovation, update size, and contribution trace. Validate adaptive components by
incremental out-of-sample value, not by prettier state plots.

## Open Questions

- Which fixed filter bank should become the default p12n temporal basis:
  log-spaced EMAs, difference-of-EMAs, dyadic bins, or a mixed basis?
- Which innovation summaries are stable enough to drive dynamic decay in crypto
  returns?
- How long can a memory channel be before it stops adding effective samples and
  starts acting as a leakage-like slow level?
- Should fast adapters use TD-style traces, delayed supervised targets, or a
  reward-regrouped Monte Carlo gradient for long-horizon returns?
- Which pieces belong in project code first: fixed banks, whitening,
  target-side backward EMA screening, or sparse shared-decay state?

## Source Map

- [Adaptive Filtering in Sequence Models](../../../ops/artifacts/chatgpt/69992303-31c0-839c-8f32-640d3fbc88a1.md)
- [Adaptive Regression Models Research](../../../ops/artifacts/chatgpt/67bf16db-de44-8009-a053-1fb7756e3302.md)
- [Bias correction techniques EMA](../../../ops/artifacts/chatgpt/69381b2a-a4d4-832b-94f5-7cc7c01d20e3.md)
- [Branch - RTRL-driven Regressor Design](../../../ops/artifacts/chatgpt/69ae20aa-8790-839f-9ad3-bb05bc4c5ccb.md)
- [Decay bounds for poles](../../../ops/artifacts/chatgpt/68341b7f-25b4-8009-8b87-cf7e7adee187.md)
- [Disjoint Moving Averages](../../../ops/artifacts/chatgpt/6994248e-1824-83a1-b6c7-76a8ecf35b09.md)
- [EKF Online Regression Analogy](../../../ops/artifacts/chatgpt/69b7c1ef-0bc8-839d-8d99-a5ecace216c0.md)
- [EMA Computation Efficiency](../../../ops/artifacts/chatgpt/69cfd35f-b000-839d-83da-034106b7584c.md)
- [EMA Smoothing in Regression](../../../ops/artifacts/chatgpt/68075640-8f14-8009-893a-cb2a34f24c1a.md)
- [EMA State Saturation](../../../ops/artifacts/chatgpt/6a22202a-b30c-83ec-9c6d-ade434282e17.md)
- [EMA Transformation for Regression](../../../ops/artifacts/chatgpt/6752bf06-1800-8009-be1a-4dd1718c840b.md)
- [Fast and Slow Weights](../../../ops/artifacts/chatgpt/69a5b11a-3d38-839d-a554-ad4bb56bba78.md)
- [Fitting EMA Half-Lives](../../../ops/artifacts/chatgpt/67b178be-a9a8-8009-bb82-826da560e0c8.md)
- [Global decay offset trick](../../../ops/artifacts/chatgpt/69ccc4ca-aa38-839a-86d4-68ea6a0550e1.md)
- [Inverse EMA in Regression](../../../ops/artifacts/chatgpt/67cf90b3-984c-8009-9b64-df5238549eb5.md)
- [Kalman Filter State-Space Integration](../../../ops/artifacts/chatgpt/69abc878-f2a0-83a0-b672-01b48fb393d9.md)
- [Kalman filter update intuition](../../../ops/artifacts/chatgpt/69b21439-56cc-8399-9022-6f58147ac799.md)
- [Long EMA Overfitting Analysis](../../../ops/artifacts/chatgpt/6842af6f-3198-8009-ae3c-1d48793e028e.md)
- [Non-TD Branch - RTRL-driven Regressor Design](../../../ops/artifacts/chatgpt/69ad830b-2734-83a0-ace6-1cf85c61fead.md)
- [Orthogonal Matrix EMA Simplification](../../../ops/artifacts/chatgpt/6878a1fb-a638-8009-8535-4c1a8c1e2bc5.md)
- [Orthogonalizing EMA Features](../../../ops/artifacts/chatgpt/6810fc5e-f9e8-8009-a69f-a57b3d8d56a1.md)
- [RTRL-driven Regressor Design](../../../ops/artifacts/chatgpt/69a93d32-da28-839c-85b2-b1d0e285ad05.md)
- [Dynamic EMA Decay](../../projects/obelisk/dynamic-ema-decay.md)
- [p12n ml](../../../ops/artifacts/obsidian/p12n-ml.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
