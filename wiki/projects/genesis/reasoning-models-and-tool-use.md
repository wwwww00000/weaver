---
title: Reasoning Models And Tool Use
status: draft
page_type: research-thread
projects:
  - genesis
categories:
  - ai
  - reasoning-models
  - tool-use
  - agentic-workflows
source_bundles:
  - unassigned/ai
  - genesis/ai
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/genesis
related:
  - projects/genesis/ai-research-map
  - projects/genesis/agentic-tooling
  - projects/genesis/weaver-as-knowledge-system
created: 2026-06-28
updated: 2026-06-28
---

# Reasoning Models And Tool Use

The useful Genesis frame is that a reasoning model is not just an answer
generator. It is a policy over context-transforming actions.

Plain token emission is the degenerate action: append one token to the stream.
Tool calling makes the broader structure visible. A model can emit a tool call,
the harness executes it, and an observation is appended to the working context.
Reasoning traces, scratch buffers, summaries, retrievals, subagent reports, and
final answers can all be treated as different action types with different
effects on future computation.

## Context-Transforming Actions

The core action algebra can stay small:

- `think`: spend local inference budget or write a scratch note;
- `tool_call`: request an external observation;
- `observe`: incorporate a tool result;
- `summarize`: compress a working buffer;
- `commit`: promote a summary or decision into durable context;
- `answer`: produce the user-facing artifact.

This separates three roles that ordinary chat transcripts blur together:

- working memory used to solve the task;
- environment interaction used to fetch or verify facts;
- final communication meant for the user or evaluator.

The design rule is model-native control, harness-native storage. Let the model
choose among stable control actions. Keep persistence, permissions, retention,
redaction, replay, and compaction policy in the harness where they can be
audited and changed.

This is also the bridge to [Agentic Tooling](agentic-tooling.md). The tooling
work is the runtime substrate; this page is the learning and model-behavior
view of the same loop.

## Token Choices, Observations, And Gradients

The training picture becomes clearer if token choices and tool observations are
kept distinct.

In ordinary teacher-forced language-model training, the model is trained on the
known next token from the dataset. Its own sampled token is not fed back during
training, so the non-differentiable decoding choice is sidestepped.

At inference time and in RL-style post-training, sampled tokens are actions.
They are discrete, but that is normal for policy-gradient methods: the update
uses log probabilities of sampled actions and rewards or advantages, not
gradients through an argmax.

Tool outputs are different. A compiler error, search result, API response, or
database row is an environment observation. Gradients can train the model to use
that observation once it is in context, but they do not ordinarily backpropagate
through the external tool into the earlier call that produced it.

The practical training options are therefore:

- supervised traces for interface competence;
- DPO or preference optimization for better trajectories;
- RL or GRPO-style updates for delayed success signals;
- hindsight or privileged-context distillation, where a teacher sees tool
  feedback and distills better token targets back into the deployable policy.

That last pattern is the useful reading of SDPO-like ideas here. Rich feedback
text can become dense supervision without treating the external environment as
a differentiable graph.

## Tool Calling As A Runtime Loop

The contemporary tool loop has a stable shape:

1. The harness exposes a registry of tool names, descriptions, and argument
   schemas.
2. The model chooses to answer directly or emit a tool call.
3. The harness validates the arguments, possibly with constrained decoding or
   schema repair.
4. The harness executes the tool outside the model.
5. The result returns as an observation in the next model step.
6. The loop repeats until the model emits a final answer.

The important engineering choices are not exotic:

- keep tool schemas short and discriminative;
- validate arguments before execution;
- treat tool outputs as untrusted data;
- log tool calls, outputs, errors, and latency for replay;
- separate the tool-call phase from the final-answer phase when reliability
  matters;
- use explicit state objects when argument values must persist across turns.

For Genesis, this means a first experiment does not need a full AI IDE. It
needs a small harness where actions and observations are visible, replayable,
and scorable.

## Reasoning Training Stack

The sources converge on a layered post-training map:

- instruction tuning teaches the base model task and conversation format;
- reasoning or tool-use traces teach it the shape of useful intermediate work;
- preference optimization and RL shape the policy toward successful
  trajectories;
- verifier, compiler, unit-test, or answer-checker feedback supplies cheap
  rewards when the task is closed enough;
- search and self-refinement generate better trajectories that can be distilled.

For small experiments, the right question is not "can we reproduce a frontier
reasoning model?" It is whether a narrow model can learn when to call, when to
summarize, when to continue thinking, and when to stop under a simple reward
scheme.

Binary rewards are enough if the environment produces some successes within a
sample group. Group-relative methods such as GRPO turn a set of completions into
relative advantages, while auxiliary format or process rewards can keep early
training from degenerating when every answer is wrong.

## World Models And LLMs

The world-model discussion is useful because it prevents over-identifying all
reasoning with next-token prediction.

A text model can contain an implicit world model. If the world is a text game,
then predicting future text and predicting future state can blur together. But
the stronger world-model claim is state-based and action-conditional: encode the
current situation into a latent state, imagine how that state changes under
candidate actions, then evaluate the imagined future.

That is closer to planning:

```text
state -> candidate action -> predicted next state -> cost/value -> revise
```

JEPA-style objectives emphasize predicting latent representations instead of
raw next observations. The intended benefit is to model task-relevant structure
without wasting capacity on unpredictable surface detail. The central failure
mode is representation collapse: if every target embedding becomes trivial or
indistinguishable, the predictor can minimize loss without learning useful
state.

For Genesis, the takeaway is modest. LLM tool use, verifier-guided search, and
latent world models are not the same thing, but they share a planning-shaped
loop: maintain state, choose an action, observe or imagine consequences, score
them, and update the next action.

## Hobby-Scale Research Program

A reasonable first experiment is harness-first and model-small:

1. Pick one verifiable environment: arithmetic, string puzzles, code with unit
   tests, toy tool lookup, or a small ARC-like DSL task.
2. Expose only four actions: `think`, `tool_call`, `summarize`, and `answer`.
3. Generate trajectories with an open-weight model small enough to iterate on
   locally.
4. Score final success with an automatic checker.
5. Score process constraints separately: valid action syntax, no unnecessary
   tool calls, correct summary format, and bounded token cost.
6. Compare supervised traces, DPO-style pair training, and a small
   GRPO/RL-style run.
7. Distill successful or feedback-informed trajectories into the base policy.

The exact open-weight model choice should be refreshed before implementation.
The durable part is the experiment shape, not a specific model family name.

The goal is intuition, not scale: learn what changes when context management is
an explicit action space rather than an implicit side effect of emitting more
tokens.

## Open Questions

- What is the smallest action algebra that gives real benefit over plain
  tool-calling?
- Should summaries and commits be model actions, harness policies, or both?
- Which environments produce rich enough feedback for SDPO-like distillation?
- How should a harness score the cost of context actions, not only final
  correctness?
- When is a subagent better than a scratch buffer or separate working context?
- Can a toy world-model or JEPA experiment clarify anything useful for
  tool-using LLMs, or is it a separate research branch?

## Source Map

- [LLM Token Generation Insight](../../../ops/artifacts/chatgpt/69c55877-4974-839c-9c83-428afc7312a3.md)
- [Reasoning LLM Components Overview](../../../ops/artifacts/chatgpt/6829fc1b-bd8c-8009-96d7-e19bdccbfe0d.md)
- [Tool calling in LLMs](../../../ops/artifacts/chatgpt/689b43ca-b158-8328-8f70-890af13a106f.md)
- [World Models vs LLMs](../../../ops/artifacts/chatgpt/69c2c3f3-e24c-8399-aecc-4c2c9fd54dd5.md)
- [source inventory](../../../ops/clusters/2026-06-24/source-inventory.qmd)
