---

title: Structured Context as a Portable LLM Substrate
project: Genesis
status: parked
type: seed-note
tags:

* llms
* context-management
* agent-harnesses
* structured-memory
* graphify
* qmd
* recursive-language-models
* weaver-adjacent
  created: 2026-06-29

---

# Structured Context as a Portable LLM Substrate

## One-line summary

Explore whether LLM workflows can be improved by treating chat transcripts as event logs and maintaining a portable, inspectable layer of structured artifacts: claims, decisions, todos, affordance cards, code notes, experiment summaries, and retrieval-ready context packs.

## Why this belongs under Genesis

This is primarily an AI/LLM engineering idea rather than a pure personal-wiki idea. It overlaps with Weaver and the LLM wiki project, but the broader question is about how to build better LLM-driven workflows using today’s models.

The practical motivation is simple: current LLM sessions have too much cold-start friction. Useful state is often trapped in long chats, manually pasted summaries, or vague memory. We want sessions to become more cumulative, reusable, and portable across ChatGPT, Codex, Claude Code, local models, and future agent harnesses.

The deeper theoretical motivation is that current LLM usage is biased toward linear, append-only context. This may be partly coupled to the autoregressive next-token prediction paradigm, but the transcript does not have to be the durable state. A better framing might be:

```text
linear context : next-token continuation
structured context : state transition / artifact rewrite / recursive context access
```

## Recent conversation background

This note follows from several recent threads:

* The Graphify / QMD discussion, where we considered whether raw notes should first be transformed into a more structured intermediate representation before LLM synthesis.
* The `tobi/qmd` discussion, where we clarified that QMD is a specific project and not just generic markdown syntax. This made the idea of a markdown-first, search-first intermediate layer more concrete.
* The “context management” thread, where we discussed chain-of-thought, tool calls, compaction, retrieval, and harness interventions as different strategies for managing limited context.
* The auxiliary-controller idea, where a small controller or harness policy could decide what to retrieve, mount, summarize, compact, or externalize.
* The Recursive Language Models / coding-agent analogy, where modern agent systems already act somewhat like recursive context systems over external artifacts: codebases, files, notes, test outputs, and tool results.
* The idea that current coding agents with tool calls are a “high-level textual ancestor” of something more native: models with structured context operations, addressable external memory, and perhaps activation-level retrieval.

## Core thesis

Text should remain the universal interface and serialization layer, but not necessarily the conceptual layer.

We can build a portable high-level system where:

```text
chat transcript = event log
markdown/code/artifacts = durable state
semantic tags = portable structure
QMD-like search = retrieval substrate
Graphify-like overlay = relationship substrate
affordance cards = usage-attraction layer
controller = context routing and memory hygiene
LLM = reasoning/generation engine
```

This avoids overcommitting to one model provider or architecture. The artifacts remain inspectable and git-backed. The system can be used by ChatGPT, Claude Code, Codex, local models, or future harnesses by rendering the relevant state as text.

## Key design idea: context packs

Instead of starting every LLM session from a blank prompt or long pasted history, generate a task-specific context pack.

Example command shape:

```bash
ctx open --project genesis --task "think about structured context and affordance fields"
```

Possible output:

```xml
<context_pack project="genesis">
  <current_focus>
    Parked idea: structured context as a portable LLM substrate.
  </current_focus>

  <relevant_decisions>
    <decision id="decision.text_as_serialization_layer">
      Use text/markdown/XML as the portable interface, but do not confuse it with the conceptual substrate.
    </decision>
  </relevant_decisions>

  <relevant_claims>
    <claim id="claim.transcript_as_event_log">
      The transcript should be treated as an event log, not as the durable project state.
    </claim>
  </relevant_claims>

  <relevant_affordances>
    <artifact id="affordance.qmd_layer">
      Useful when we need portable local retrieval over markdown notes, docs, and project artifacts.
    </artifact>
  </relevant_affordances>

  <open_questions>
    <question>
      What is the minimal useful semantic tag vocabulary?
    </question>
  </open_questions>
</context_pack>
```

The goal is not to hide everything behind a magical agent. The goal is to give each session the right state, at the right level of abstraction, in a portable textual format.

## Key design idea: session close

At the end of a meaningful session, run a close operation:

```bash
ctx close --project genesis transcript.md
```

This proposes durable updates:

```xml
<proposed_updates>
  <add type="claim" id="claim.structured_context_as_state_transition">
    Structured context can be understood as a state-transition problem rather than pure transcript continuation.
  </add>

  <add type="decision" id="decision.start_sidecar_not_harness">
    Start with a sidecar context system before modifying a deeper agent harness.
  </add>

  <add type="todo" id="todo.prototype_ctx_open_close">
    Build a minimal ctx open/close prototype over markdown artifacts.
  </add>
</proposed_updates>
```

This should be human-reviewed before being applied. Memory hygiene matters. Not every thought deserves to become durable project state.

## Semantic tags

Semantic tags may be a good fit because they are portable across model providers and easy to inspect.

Possible minimal vocabulary:

```xml
<claim>...</claim>
<decision>...</decision>
<todo>...</todo>
<question>...</question>
<handoff>...</handoff>
<artifact>...</artifact>
<affordance>...</affordance>
<when_to_use>...</when_to_use>
<when_not_to_use>...</when_not_to_use>
<invariant>...</invariant>
<failure_mode>...</failure_mode>
<context_pack>...</context_pack>
<state_delta>...</state_delta>
```

The goal is not to make XML sacred. The goal is to create stable, parseable, model-readable boundaries between different kinds of project state.

## Affordance fields

The most interesting practical primitive may be the “affordance field.”

A normal note or code module says what something is. An affordance card says when it wants to be used.

Example:

```markdown
---
id: affordance.vault_triage_builder
type: affordance
target: src/vault_triage.py
status: active
tags: [obsidian, ingestion, triage, deterministic]
---

# Vault triage builder

<summary>
Scans an Obsidian vault and produces a human-reviewable triage document.
</summary>

<when_to_use>
- The task involves deciding which notes should enter the LLM wiki.
- The input is a local markdown vault.
- The desired output is deterministic and reviewable.
</when_to_use>

<when_not_to_use>
- The input is a ChatGPT export.
- The task requires semantic summarization of note contents.
- The task should mutate source notes.
</when_not_to_use>

<invariants>
- Never mutate source notes.
- Preserve relative paths.
- Emit deterministic output.
</invariants>

<failure_modes>
- Accidentally treating generated index files as user notes.
- Over-including archived or template notes.
</failure_modes>
```

The hope is that these affordance cards create a kind of semantic attraction field during retrieval. The system should retrieve not only textually similar artifacts, but artifacts whose usage conditions match the current task.

This is especially relevant for code. A function or module should be coupled to usage notes, invariants, failure modes, examples, and design rationale.

## Possible architecture

A portable high-level version might look like:

```text
human artifacts
  markdown, code, docs, experiment logs, todos
      ↓
QMD-like retrieval
  keyword search + semantic search + reranking
      ↓
Graphify-like overlay
  links, entities, relationships, provenance
      ↓
affordance layer
  when-to-use / when-not-to-use / invariants / failure modes
      ↓
controller
  selects, mounts, prunes, and formats context
      ↓
portable context pack
  markdown/XML/YAML
      ↓
any LLM or coding agent
      ↓
proposed state delta
  human-reviewed durable update
```

## Relationship to model architecture ideas

The practical version is high-level and textual, but it points at lower-level primitives.

The purist objection is valid: asking a model to emit structured summaries through raw text is awkward. It feels like a userland emulation of something that should eventually exist as lower-level model/runtime operations.

Possible lower-level descendants:

* special memory/action tokens
* a restricted context-operation vocabulary
* controller heads for retrieval/update decisions
* object references or pointer tokens into external artifacts
* activation-level retrieval over latent object stores
* memory tokens or recurrent external state
* recursive latent access to structured context
* models trained on response plus state-delta targets

The practical sidecar system can be viewed as a prototype for discovering which primitives are actually useful before pushing anything down into architecture or post-training.

## Relationship to Recursive Language Models

Recursive Language Models suggest that the active context does not need to contain the whole problem. Instead, the model can recursively inspect and operate over an external environment.

Coding agents already resemble this:

```text
repo lives outside context
agent searches files
agent opens relevant snippets
agent calls tools
agent patches code
agent runs tests
agent observes results
```

The version explored here generalizes that idea:

```text
project state lives outside context
agent retrieves relevant artifacts
agent mounts a structured context pack
agent reasons/writes/edits
agent proposes durable state updates
```

A lower-level future version might replace textual tool calls with latent retrieval and object-level memory access. But for now, text remains the most portable interface.

## Testing strategy

Avoid starting with an overly academic benchmark. Start with personal usefulness, then add small evaluations.

Recommended substrates:

### 1. Dogfood on Weaver / Genesis conversations

Use the system to reduce cold starts in ongoing LLM design conversations.

Test question:

```text
Does ctx open produce a better session preamble than manual memory or pasted summaries?
```

### 2. Use the LLM wiki ingestion tooling as a concrete software project

This is less meta than building the memory system to remember itself.

Possible target:

```text
Obsidian vault triage generator
ChatGPT export triage generator
```

These naturally require:

* design decisions
* code affordance cards
* todos
* invariants
* handoffs
* tests
* usage documentation

Test question:

```text
Does the agent reuse the right abstractions and preserve known invariants when given affordance cards?
```

### 3. Create tiny fixture tasks

Example fixture:

```yaml
task: "Implement ChatGPT export triage."
expected_retrieval:
  - decision.ingestion_before_agent_layer
  - affordance.chatgpt_export_triage
  - todo.chatgpt_export_triage
unexpected_retrieval:
  - affordance.vault_triage_builder_as_primary
```

Metrics can be simple:

* retrieval precision
* retrieval restraint
* affordance activation
* invariant preservation
* handoff usefulness
* memory hygiene
* duplication avoidance

## Deferred implementation plan

This is parked for later. A possible first version:

```text
weaver-context/
  projects/
    genesis/
      state.md
      decisions.md
      claims.md
      questions.md
      todos.md
      handoffs.md
      affordances/
        qmd_layer.md
        graph_overlay.md
        context_pack.md
        session_close.md
      fixtures/
        retrieval_tasks.yaml
```

Initial commands:

```bash
ctx open --project genesis "task description"
ctx close --project genesis transcript.md
ctx inspect --project genesis --artifact affordance.qmd_layer
ctx eval --project genesis
```

Do not start with a database, graph visualization, or custom model architecture. Start with markdown artifacts, semantic tags, simple retrieval, and human-reviewed state deltas.

## Current stance

This seems worth parking as a future Genesis/Weaver-adjacent project.

The practical value is improving continuity across LLM sessions.

The research value is exploring whether transcript-based context should be replaced by structured, inspectable, portable project state.

The theoretical north star:

```text
The transcript is an event log, not the state.
Text is the serialization layer, not the conceptual layer.
The LLM should operate over mounted structured context, not merely continue a linear chat.
```

## Open questions

* What is the smallest useful semantic tag vocabulary?
* Should XML tags, markdown sections, or YAML frontmatter be the primary structure?
* How much should the system write automatically versus propose for review?
* How do we prevent memory pollution?
* How do we represent uncertainty, provenance, and superseded claims?
* How do affordance fields differ from ordinary documentation?
* Can a small local model handle routing, duplicate detection, and memory hygiene?
* Should QMD-like retrieval be the first layer before any graph extraction?
* When does a graph overlay provide real value over typed markdown search?
* What would make this useful enough to integrate into the actual Weaver harness?
* Which primitives, if any, seem worth pushing down into post-training or architecture later?
