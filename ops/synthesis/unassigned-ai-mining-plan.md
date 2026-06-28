# Unassigned AI Mining Plan

Date: 2026-06-28

This is the routing layer for `unassigned/ai` source artifacts. It is not final
wiki prose. Use it to decide which existing page, new page, or defer bucket
should consume each source.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Method

Treat `unassigned/ai` as a mining queue, not as one giant AI page.

For each artifact, assign:

- `merge`: read during the next pass for the destination page.
- `dual-link`: split between a project-facing page and a reusable concept or
  method page.
- `new-page`: create a candidate page before synthesis.
- `defer`: leave out of the next pass unless a later page needs it.
- `skip`: low-signal or not worth importing into the wiki.

Priority means:

- `P1`: useful for the next page-deepening pass.
- `P2`: potentially useful, but not worth blocking the next pass.
- `P3`: likely skip or archive-only.

## Queue Order

| Queue | Count | First pass |
| --- | ---: | --- |
| Reasoning Models And Tool Use | 4 | Create a Genesis child page and cross-link to agentic tooling. |
| Agentic Tooling And Weaver Interfaces | 5 | Deepen existing Genesis agentic tooling and Weaver pages. |
| Credit Assignment And Training Signals | 7 | Create a Genesis AI research child page for credit assignment, dense supervision, and toy RL loops. |
| Sequence, State-Space, And Gated Architectures | 4 | Deepen P12n sequence-model analogies and Genesis AI research where non-trading lessons remain. |
| Nonlinear Function Classes And Interpretability | 12 | Route mostly into Quant method pages, with Genesis links for AI-research framing. |
| AI Research Backlog And Resources | 2 | Fold into the Genesis AI research map only if the raw note has concrete follow-up value. |

## Status

- 2026-06-28: Created initial routing plan for `unassigned/ai`.

## Reasoning Models And Tool Use

Primary destination:
[Reasoning Models And Tool Use](../../wiki/projects/genesis/reasoning-models-and-tool-use.md).

Secondary destinations:
[AI Research Map](../../wiki/projects/genesis/ai-research-map.md) and
[Agentic Tooling](../../wiki/projects/genesis/agentic-tooling.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [LLM Token Generation Insight](../artifacts/chatgpt/69c55877-4974-839c-9c83-428afc7312a3.md) | merge | P1 | Decoder mechanics and next-token limits. |
| [Reasoning LLM Components Overview](../artifacts/chatgpt/6829fc1b-bd8c-8009-96d7-e19bdccbfe0d.md) | merge | P1 | Component map for reasoning-model systems. |
| [Tool calling in LLMs](../artifacts/chatgpt/689b43ca-b158-8328-8f70-890af13a106f.md) | dual-link | P1 | Model/tool interface; also useful for agentic tooling. |
| [World Models vs LLMs](../artifacts/chatgpt/69c2c3f3-e24c-8399-aecc-4c2c9fd54dd5.md) | merge | P1 | Distinguishes sequence prediction from environment modeling. |

## Agentic Tooling And Weaver Interfaces

Primary destinations:
[Agentic Tooling](../../wiki/projects/genesis/agentic-tooling.md) and
[Weaver As A Knowledge System](../../wiki/projects/genesis/weaver-as-knowledge-system.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Agentic Workflows in ML](../artifacts/chatgpt/69b6e7ae-cac0-8398-b6bf-506df883700b.md) | merge | P1 | Already source-mapped to agentic tooling; mine for ML workflow detail. |
| [Context Management in LLMs](../artifacts/chatgpt/69acf566-8c94-839f-9dc5-9e4931ab63ba.md) | dual-link | P1 | Context compiler and memory model source. |
| [LLM Coding Workflows](../artifacts/chatgpt/6a31f45a-f0e0-83ec-8a47-08c0e09e206c.md) | merge | P1 | Already source-mapped to agentic tooling; mine for workflow mechanics. |
| [LLM Note-taking Tools](../artifacts/chatgpt/67e29c1d-88f4-8009-b717-e92513a6543e.md) | dual-link | P1 | Weaver and later writing queue bridge. |
| [next](../artifacts/obsidian/weaver.md) | dual-link | P1 | Already used by Weaver; mine only if new interface details remain. |

## Credit Assignment And Training Signals

Primary destination:
[Credit Assignment And Training Signals](../../wiki/projects/genesis/credit-assignment-and-training-signals.md).

Secondary destination:
[AI Research Map](../../wiki/projects/genesis/ai-research-map.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Branch - Credit Assignment Scaling](../artifacts/chatgpt/69f83ba8-0674-83a1-9961-b38d0460b344.md) | merge | P1 | Branch source for credit-assignment scaling thread. |
| [Credit Assignment Scaling](../artifacts/chatgpt/69f36da9-8d1c-83a0-8d24-8180ac364ad8.md) | merge | P1 | Main credit-assignment scaling source. |
| [Experiment Branch - Credit Assignment Scaling](../artifacts/chatgpt/69f99528-1ae8-839f-9308-30cbba5a2b53.md) | merge | P1 | Experimental follow-up source. |
| [Dense Supervision in RL](../artifacts/chatgpt/69c562d7-dfd0-839d-9aed-3c7baa9adad0.md) | merge | P1 | Dense reward or auxiliary target framing. |
| [Cotangents and Backpropagation](../artifacts/chatgpt/69f22f99-32a4-839c-a2b7-1b072ee23783.md) | merge | P1 | Backprop/cotangent concept bridge. |
| [RNNs and RL Similarities](../artifacts/chatgpt/18bc73af-ff96-4d61-ae44-6be82b89d3d7.md) | dual-link | P2 | Training-signal analogy plus sequence-model overlap. |
| [Time Travel Deep Learning](../artifacts/chatgpt/69f1f23c-ca74-8398-bd3e-c9ebb282e9a7.md) | merge | P2 | Speculative credit-assignment idea; keep separated from conclusions. |

## Sequence, State-Space, And Gated Architectures

Primary destination:
[P12n Sequence-Model Analogies](../../wiki/projects/p12n/sequence-model-analogies.md).

Secondary destinations:
[AI Research Map](../../wiki/projects/genesis/ai-research-map.md) and
[Quant adaptive filters](../../wiki/topics/quant/adaptive-filters-and-ema.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Gated Layers and Approximations](../artifacts/chatgpt/6728c741-b2f8-8009-b3e5-c1fabd74ad94.md) | merge | P1 | Already merged at high level; revisit only if new gated-layer details are needed. |
| [RNNs as Transformers](../artifacts/chatgpt/68355831-4d24-8009-854b-57da7ec562f8.md) | merge | P1 | Sequence architecture analogy. |
| [Simplified Gated RNN](../artifacts/chatgpt/6752ad04-8df8-8009-bcf0-6001804e4628.md) | merge | P1 | Minimal gated recurrence source. |
| [State-Space Duality Explanation](../artifacts/chatgpt/6a0a66e5-699c-83ec-a8f5-d3af30104eb1.md) | dual-link | P1 | SSM/attention/recurrent duality. |

## Nonlinear Function Classes And Interpretability

Primary destinations:
[Tabular Nonlinearities And Feature Search](../../wiki/topics/quant/tabular-nonlinearities.md),
[Optimization And Computation](../../wiki/topics/quant/optimization-and-computation.md), and
[Generalization And Regularization](../../wiki/topics/quant/generalization-and-regularization.md).

Secondary destination:
[AI Research Map](../../wiki/projects/genesis/ai-research-map.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Alternative Models for Non-linearities](../artifacts/chatgpt/672e2c3c-fdb8-8009-bc12-e39f9281128b.md) | merge | P1 | Nonlinear basis and model-family menu. |
| [Analytical Neural Network Training](../artifacts/chatgpt/672ba4a5-0098-8009-bf41-8abd9ed48760.md) | dual-link | P2 | Quant optimization plus AI-research method framing. |
| [Base Learner Options TS](../artifacts/chatgpt/6830a950-368c-8009-ab4b-c7baf293dd2e.md) | merge | P1 | Time-series learner menu; already relevant to tabular nonlinearities. |
| [Discretization in Deep Learning](../artifacts/chatgpt/67b71b0c-5d0c-8009-8093-27d79fdb7289.md) | dual-link | P1 | Bucketization and neural numeric features. |
| [Gauss-Newton for Nonlinear Layers](../artifacts/chatgpt/69e63991-5ef4-83a1-a9bb-cd1a23247290.md) | merge | P1 | Nonlinear block optimization. |
| [Interpretable Deep Learning Models](../artifacts/chatgpt/672ba721-c398-8009-9c8c-75e489f722b8.md) | dual-link | P1 | Interpretability and model constraints. |
| [Leaky ReLU regression fit](../artifacts/chatgpt/68c04aa7-bc9c-8328-a7ab-ce4f8b854cc9.md) | merge | P2 | Specific activation-fitting example. |
| [Modern RBF Network Developments](../artifacts/chatgpt/672c1906-c84c-8009-9acf-bad5dee5522e.md) | merge | P1 | RBF and local basis background. |
| [Non-linear Feature Transformations](../artifacts/chatgpt/674b3994-918c-8009-9724-e8dd5d984766.md) | merge | P1 | General transform menu. |
| [Nonlinear Regression with RBFs](../artifacts/chatgpt/14a7c2eb-c92f-4a9a-b85a-5d9bcfbbfe20.md) | merge | P1 | RBF regression detail. |
| [NTK Kernel Representation Explanation](../artifacts/chatgpt/69ed7a30-5620-83a1-bbdf-aee44f9ad3fb.md) | dual-link | P2 | Kernel interpretation; may belong in Genesis AI research if not useful for quant. |
| [ReLU Network Interpretability Research](../artifacts/chatgpt/67d19849-1f64-8009-9f88-7980df924237.md) | dual-link | P1 | Interpretable ReLU networks and linear-region view. |

## AI Research Backlog And Resources

These sources may contain useful research-list material, but should not drive a
page unless the raw note has concrete project direction.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [iclr2025](../artifacts/obsidian/iclr2025.md) | defer | P2 | Conference/resource note; route only selected threads into AI research map. |
| [generative ai](../artifacts/obsidian/generative-ai.md) | defer | P2 | Resource note; read before deciding whether it adds concrete project direction. |

## Next Pass

Start with Reasoning Models And Tool Use because it adds a missing Genesis child
page and gives the agentic tooling/context-management sources a clearer AI
systems frame. Then deepen agentic tooling and Weaver interfaces before moving
to credit assignment, sequence architectures, and nonlinear method spillovers.
