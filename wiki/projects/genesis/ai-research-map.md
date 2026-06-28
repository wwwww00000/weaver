---
title: AI Research Map
status: draft
page_type: research-thread
projects:
  - genesis
categories:
  - ai
  - research
  - machine-learning
  - neuro-symbolic
source_bundles:
  - genesis/ai
  - genesis/math
  - genesis/quant
  - genesis/machine learning
  - unassigned/ai
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/genesis
related:
  - projects/genesis
  - projects/genesis/agentic-tooling
  - projects/genesis/reasoning-models-and-tool-use
  - projects/genesis/credit-assignment-and-training-signals
  - topics/quant/generalization-and-regularization
  - topics/quant/optimization-and-computation
created: 2026-06-28
updated: 2026-06-28
---

# AI Research Map

Genesis AI research should focus on small, testable systems where a single
researcher can learn something real without frontier-scale training.

The highest-value theme is not generic model scaling. It is the boundary between
neural policies, symbolic tools, explicit search, verifiers, and test-time
adaptation. Those are the places where a hobbyist can build concrete systems,
run ablations, and understand contemporary reasoning models without needing a
large pretraining run.

## ARC-AGI And Neuro-Symbolic Systems

ARC-AGI is the cleanest research testbed in the current notes because it rewards
generalization, typed abstractions, and efficient test-time reasoning.

The useful conceptual split:

- transduction: predict the test output grid directly from examples;
- induction: infer a program or rule that maps inputs to outputs;
- latent programs: search or optimize over a continuous program-like
  representation before producing an executable result.

The Genesis direction is a hybrid. Symbolic primitives should handle crisp
operations: selections, connected components, color transforms, translations,
rotations, masks, object attributes, and relation queries. Small learned modules
can appear as typed "neural slots" when a hand-written primitive is too brittle,
but the overall trace should remain executable and verifiable.

Important guardrails:

- keep the DSL typed and small enough that search is not hopeless;
- prefer verifiable programs over unconstrained pixel prediction;
- score candidate traces with train-pair exactness plus augmentation stability;
- use per-puzzle test-time training carefully, because it can both help and
  overfit;
- log programs, intermediate selections, and verifier failures for inspection.

## Tool-Use Training And Reasoning Loops

Modern reasoning systems can be read as neural controllers over symbolic or
semi-symbolic environments. Tool calls, constrained decoding, code execution,
verifiers, notebook kernels, and typed workspaces push systems toward the
neuro-symbolic end because model outputs are interpreted, checked, and acted on
by external machinery.

The model-behavior view is split out in
[Reasoning Models And Tool Use](reasoning-models-and-tool-use.md). This page
keeps the research-program map; the child page keeps the action-space,
tool-calling, RL, distillation, and world-model notes.

The training-side map includes:

- imitation and supervised traces for bootstrapping tool use;
- preference optimization such as DPO or RLHF for broad behavior;
- GRPO-like group-relative updates when rewards are automatic;
- verifier-guided search over candidate traces;
- self-training loops that turn successful search trajectories into new data;
- AlphaZero-like loops when the task environment has closed rules and exact
  rewards.

For Genesis, the practical way to study this is not to train a large assistant.
It is to build toy environments with automatic checkers: ARC subsets, code
tasks, math tasks, string puzzles, small tool-use sandboxes, or synthetic DSL
tasks. The point is to understand the loop: sample, execute, verify, compare,
distill.

## Small Optimization Experiments

Several Genesis sources explore optimization alternatives that fit a hobbyist
or research-playground setting:

- target propagation and OLS-style block updates for shallow networks;
- gated linear experts trained by alternating least squares, hard assignments,
  EM-style responsibilities, or tree-like routing;
- gradient generalization, validation-aware updates, and regularization ideas.
- cotangent shaping and branch/path credit routing, split into
  [Credit Assignment And Training Signals](credit-assignment-and-training-signals.md).

These should mostly become reusable methods under [Quant](../../topics/quant.md)
or broader ML method pages when they are about regression, validation, and
modeling rather than Genesis itself. Genesis should keep the research-program
view: which experiments are worth running, what they might teach, and how they
connect to AI reasoning, tool use, or small-model learning.

## Paper Backlog

The ICLR 2025 note is a paper-watch list rather than a synthesized direction,
but three threads are worth keeping visible:

- parameter-efficient tabular deep learning ensembles, especially when they can
  be compared against ridge, tree, and feature-map baselines;
- one-run Data Shapley or sample-value approximations using sample-gradient
  inner products;
- fast additive explanations for Shapley-style attributions.

These belong downstream in the Quant method pages if they become implementation
work. For Genesis, they are reminders of small experiments that connect neural
modeling, interpretability, and efficient validation.

## First Research Loop

A reasonable first Genesis AI research loop:

1. Build or reproduce a tiny ARC harness with deterministic evaluation.
2. Implement a small typed DSL for selections and grid transforms.
3. Add a policy-guided or heuristic search loop over short programs.
4. Add one or two neural slots only after the symbolic baseline is inspectable.
5. Track exact match, augmentation stability, program length, search budget, and
   failure categories.
6. Only then consider toy RL or GRPO-style updates on synthetic tasks.

This sequence keeps the work grounded. It also produces reusable tooling for
later experiments in verifiers, test-time compute, tool calling, and search.

## Open Questions

- Is ARC-AGI the best first experiment, or should tool-use training be tested on
  a smaller synthetic environment first?
- Which DSL primitives are expressive enough without making search explode?
- Where should neural slots be allowed, and how should their use be penalized?
- What evaluation artifacts should every run preserve so failures become
  inspectable?
- Which optimization ideas belong in Genesis as AI-research threads versus in
  Quant as reusable statistical methods?

## Source Map

- [Project Genesis Roadmap](../../../ops/artifacts/chatgpt/67eeb281-c574-8009-8563-e8286c940bb0.md)
- [Hobbyist AI research avenues](../../../ops/artifacts/chatgpt/68a41e4c-787c-8324-b4de-5cfa89a0643d.md)
- [ARC-AGI hobbyist guide](../../../ops/artifacts/chatgpt/68a524d0-a2d8-832b-9b31-d693aa5b5aa3.md)
- [Neuro-symbolic reasoning in LLMs](../../../ops/artifacts/chatgpt/68cb9ede-b3cc-8328-bfad-f1a6e38b4baf.md)
- [RL techniques overview](../../../ops/artifacts/chatgpt/68d944f9-4a38-8322-a529-a719912bc84f.md)
- [Deep Learning Optimization Alternatives](../../../ops/artifacts/chatgpt/69a06096-458c-839c-a1d6-a94cf2917aa6.md)
- [Gated Linear Experts Training](../../../ops/artifacts/chatgpt/699e4ba2-0544-83a1-ac7b-8df05bfee5d9.md)
- [LLM Token Generation Insight](../../../ops/artifacts/chatgpt/69c55877-4974-839c-9c83-428afc7312a3.md)
- [Reasoning LLM Components Overview](../../../ops/artifacts/chatgpt/6829fc1b-bd8c-8009-96d7-e19bdccbfe0d.md)
- [Tool calling in LLMs](../../../ops/artifacts/chatgpt/689b43ca-b158-8328-8f70-890af13a106f.md)
- [World Models vs LLMs](../../../ops/artifacts/chatgpt/69c2c3f3-e24c-8399-aecc-4c2c9fd54dd5.md)
- [Credit Assignment Scaling](../../../ops/artifacts/chatgpt/69f36da9-8d1c-83a0-8d24-8180ac364ad8.md)
- [Dense Supervision in RL](../../../ops/artifacts/chatgpt/69c562d7-dfd0-839d-9aed-3c7baa9adad0.md)
- [Cotangents and Backpropagation](../../../ops/artifacts/chatgpt/69f22f99-32a4-839c-a2b7-1b072ee23783.md)
- [iclr2025](../../../ops/artifacts/obsidian/iclr2025.md)
- [source inventory](../../../ops/clusters/2026-06-24/source-inventory.qmd)
