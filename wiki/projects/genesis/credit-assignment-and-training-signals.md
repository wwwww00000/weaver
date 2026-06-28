---
title: Credit Assignment And Training Signals
status: draft
page_type: research-thread
projects:
  - genesis
categories:
  - ai
  - credit-assignment
  - deep-learning
  - training-signals
source_bundles:
  - unassigned/ai
  - genesis/ai
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/genesis
related:
  - projects/genesis/ai-research-map
  - projects/genesis/reasoning-models-and-tool-use
  - projects/p12n/sequence-model-analogies
created: 2026-06-28
updated: 2026-06-28
---

# Credit Assignment And Training Signals

This thread is about treating the backward signal as an object worth shaping,
not merely accepting exact backpropagation and then relying on a fancy optimizer
to clean up the resulting parameter gradients.

The working hypothesis:

> Modern training is sophisticated about parameter-space updates, but still
> primitive about the cotangent, target, reward, and path-credit signals that
> generate those updates.

This remains speculative. The useful part is that it suggests small, testable
experiments instead of vague "better optimizer" work.

## Cotangent View

Backpropagation propagates cotangents: covectors that map a perturbation in an
activation to a scalar change in loss.

For a layer:

```text
y = f(x, theta)
```

the backward pass receives a downstream cotangent and computes:

```text
credit to earlier activations = J_x^T cotangent
parameter gradient            = J_theta^T cotangent
```

For a linear layer:

```text
y = W x
grad_W = delta_y x^T
delta_x = W^T delta_y
```

So the parameter gradient is already a pairing of two factors:

- the forward local cause: activation or feature;
- the backward local price: cotangent or credit signal.

An ordinary optimizer sees the collapsed product. A credit-assignment method can
instead inspect or modify the cotangent before the gradient is formed.

## Dense Supervision

In reasoning-model RL, dense supervision is the same high-level problem in a
different setting. Outcome-only rewards provide one scalar after a long
trajectory. The research direction is to manufacture denser token-, step-, or
turn-level credit from richer signals:

- process reward models or verifiers;
- step-value estimates from future success likelihood;
- self-distillation from rich textual feedback;
- likelihood of a known answer under partial reasoning prefixes;
- tool or environment feedback such as compiler errors and judge messages;
- hybrid dense rewards anchored by verifiable pass/fail signals.

This connects to [Reasoning Models And Tool Use](reasoning-models-and-tool-use.md):
the model emits context-transforming actions, and training has to decide which
actions deserve credit. Dense supervision is not necessarily gold process
labels. It can be dense credit assignment derived from a sparse terminal
objective.

## Validation-Implied Cotangents

One concrete idea is to ask whether a training cotangent would push upstream
parameters in a direction aligned with a validation gradient.

For an upstream linear layer:

```text
h = W x
```

the per-example training gradient has the form:

```text
grad_W_train = delta_h x^T
```

If `G_val` is a validation gradient for `W`, then:

```text
<delta_h x^T, G_val> = delta_h^T (G_val x)
```

The vector:

```text
v_h = G_val x
```

is the validation-implied cotangent at the upstream activation. It says: for
this input, what activation-space credit signal would align the training update
with validation?

For a downstream scaler at site `z = F(h)`, a diagonal backward gate changes the
upstream cotangent. The alignment coefficient for a channel can be estimated as:

```text
training cotangent at z * J_{h -> z}(v_h)
```

That can be computed several ways:

- JVP through the forward segment;
- finite-difference JVP if forward-mode AD is unavailable;
- VJP per group or mask;
- random VJP probing for large diagonal gates.

The adjacent two-linear-layer case is the cleanest toy experiment because the
score has a simple analytic form and can be checked against actual gradient
alignment.

## Activation Displacement Diagnostics

A second family of diagnostics compares a representation's movement against
the current cotangent.

Let:

```text
a_minus = activation before an update
a_plus  = activation after an update
delta_plus = current cotangent
Delta a = a_plus - a_minus
```

Then:

```text
- delta_plus * Delta a
```

asks whether the previous update moved this representation coordinate in a
direction the current loss likes. Aggregated over a tensor, it approximates a
local directional derivative of the current loss along the previous update.

This is related to gradient similarity, but it decomposes the signal by
representation channel rather than by parameter block.

- Gradient similarity asks: did this parameter block want the same update across
  batches?
- Activation displacement asks: did this internal representation channel move
  in a direction endorsed by the current credit field?
- Cotangent-only similarity is weaker because it ignores the activation or
  feature factor that turns a cotangent into a parameter gradient.

The activation method is a JVP-side computation. Its scalar version is adjoint
to a backward computation that dots the current gradient with the previous
parameter update. The value of the activation view is the local channel
decomposition, especially when the intended intervention is a backward gate at
an activation site.

## Branch And Mixing Sites

The most important refinement is where to intervene.

In a pure sequential chain, a scalar backward gate mostly behaves like a prefix
learning-rate multiplier. It changes scale, but it does not make a real choice
between sources of credit.

At a branch or recombination, ordinary backprop adds contributions:

```text
delta_h = delta_h_path_1 + delta_h_path_2 + ...
```

That implicitly gives equal additive authority to every downstream path. A
credit-routing intervention can replace this with a conservative weighted
mixture:

```text
delta_h_tilde = sum_m q_m delta_h_path_m
```

The path score can compare each path contribution against the same reference:

```text
score_m = - <delta_h_path_m, Delta h>
```

or against a validation-implied cotangent. The key is to compare paths within a
shared branch family, where scale and semantics are more comparable than across
unrelated layers.

Channelwise gates are most meaningful around non-diagonal mixing:

- dense linear layers;
- convolutions that mix channels;
- attention projections;
- recurrent transitions;
- residual or auxiliary-loss recombinations;
- mixture or expert aggregation;
- cross-sectional or temporal mixing in sequence models.

If an operation is diagonal or elementwise and there is only one path, a
channelwise gate often commutes through the chain and is mostly redundant.

## Differentiable Unroll

The expensive "nuclear" version trains gates by differentiating through a
virtual optimizer step.

The computation is:

```text
gate -> modified train gradient -> virtual parameters -> next-batch loss
```

Implementation shape:

1. Insert backward gate modules into the model.
2. Compute train gradients with `create_graph=True`.
3. Build virtual parameters using differentiable tensor operations, not
   `no_grad`.
4. Evaluate next-batch or validation loss with a functional model call.
5. Differentiate that loss with respect to the gate parameters.
6. Update the real model normally afterward.

This is the most faithful test of the causal question:

> If this gate were more open, would the optimizer step induced by the train
> batch improve the next batch?

It is also costly and fragile. It should come after cheaper diagnostics suggest
that a particular gate site matters.

## Experimental Path

Start with observe-only diagnostics, not online control.

1. Adjacent linear toy:
   verify the validation-implied cotangent formula against exact upstream
   gradient alignment.
2. Branch toy:
   insert identity branch gates before recombination and compare path cotangent
   contributions.
3. Activation-displacement diagnostic:
   log `-delta * Delta a` by layer/channel across batches.
4. Gradient-similarity baseline:
   compare against parameter-block update agreement.
5. Fixed dampers:
   choose persistently bad branch or channel sites and apply small conservative
   dampers.
6. Online gates:
   only after fixed dampers help, try EMA-based dampers or differentiable
   unroll.

Useful initial constraints:

- avoid dropout and stateful normalization in the toy tests;
- use deterministic paired batches;
- keep gates near one;
- prefer damping over amplification;
- compare unnormalized dots and cosine-like normalized scores;
- track whether gains come from better generalization or merely slower
  learning.

## Open Questions

- Are branch/path gates actually useful beyond acting like local learning-rate
  multipliers?
- Which reference signal is best: validation gradient, next-batch update,
  activation displacement, auxiliary loss, or likelihood-based process value?
- Can cotangent shaping improve low-SNR sequence models without suppressing the
  useful exploration from stochastic gradients?
- Are channelwise gates around mixing operations worth the extra complexity?
- Does differentiable unroll give different decisions from cheap diagnostics,
  or does it mostly confirm them?
- Should this live under Genesis as AI research, or become a P12n experiment if
  the first tests use trading sequence models?

## Source Map

- [Branch - Credit Assignment Scaling](../../../ops/artifacts/chatgpt/69f83ba8-0674-83a1-9961-b38d0460b344.md)
- [Credit Assignment Scaling](../../../ops/artifacts/chatgpt/69f36da9-8d1c-83a0-8d24-8180ac364ad8.md)
- [Experiment Branch - Credit Assignment Scaling](../../../ops/artifacts/chatgpt/69f99528-1ae8-839f-9308-30cbba5a2b53.md)
- [Dense Supervision in RL](../../../ops/artifacts/chatgpt/69c562d7-dfd0-839d-9aed-3c7baa9adad0.md)
- [Cotangents and Backpropagation](../../../ops/artifacts/chatgpt/69f22f99-32a4-839c-a2b7-1b072ee23783.md)
- [RNNs and RL Similarities](../../../ops/artifacts/chatgpt/18bc73af-ff96-4d61-ae44-6be82b89d3d7.md)
- [Time Travel Deep Learning](../../../ops/artifacts/chatgpt/69f1f23c-ca74-8398-bd3e-c9ebb282e9a7.md)
- [source inventory](../../../ops/clusters/2026-06-24/source-inventory.qmd)
