---
title: Agentic Tooling
status: draft
page_type: concept
projects:
  - genesis
categories:
  - ai
  - tools
  - software
  - agentic-workflows
source_bundles:
  - genesis/tech
  - genesis/ai
  - genesis/uncategorized
  - unassigned/ai
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/genesis
related:
  - projects/genesis
  - projects/genesis/weaver-as-knowledge-system
  - projects/genesis/reasoning-models-and-tool-use
  - projects/p12n/experiment-infrastructure
created: 2026-06-28
updated: 2026-06-28
---

# Agentic Tooling

Agentic tooling is the Genesis thread about building environments where humans
and models can work over visible state, executable actions, and durable
artifacts.

The recurring taste is Emacs-like: small primitives, command-driven control,
inspectable state, live feedback, and the ability to promote repeated workflows
into reusable commands. The new ingredient is an LLM that can author, select,
and execute those commands while leaving a reviewable trace.

## Shared Shape

Several tools rhyme:

- an agent harness is a REPL whose expressions are plans and tool calls;
- a notebook is a REPL plus a document model and rich outputs;
- an editor is a live workspace over buffers, selections, processes, and
  commands;
- a knowledge base is a graph of modules that can be searched, linked, and
  rewritten.

The unifying loop is:

```text
state -> action -> observable effect -> feedback -> updated state
```

The state may be code, notes, a notebook kernel, an experiment graph, a plan, or
the current wiki synthesis task. The effect may be a diff, plot, shell output,
new note, query result, or test failure. The tooling problem is to make these
objects addressable and composable instead of hiding them behind a chat stream.

## Core Primitives

A small reusable ontology is more valuable than a large menu of features:

- `resource`: file, note, notebook, dataset, task, URL, or artifact;
- `buffer`: view or materialization of a resource;
- `selection`: a range, node, cell, object, row set, or focused context;
- `command`: typed transformation over resources and selections;
- `effect`: patch, tool call, process output, generated artifact, or state
  update;
- `registry`: discoverable commands, tools, schemas, and help;
- `replay`: enough provenance to rerun or audit a workflow.

AI should enter as a command author, command router, and buffer transformer. It
should not be the only place where state lives.

## Notebook And Kernel Workflows

For data science and ML work, the useful substrate is often not a notebook file
as an artifact. It is a persistent computational state with rich output
semantics.

A good agentic notebook controller should expose high-level operations:

- read and write cells or code blocks;
- execute code against a persistent kernel;
- return typed outputs: text, errors, tables, images, and plots;
- inspect variables and dataframe previews;
- checkpoint, branch, restore, and export findings.

Jupyter MCP or a Jupyter-backed execution tool is a good fit when plots,
dataframes, and human takeover in the same kernel matter. A thinner persistent
REPL tool can be enough when the notebook UI itself is incidental. For P12n-like
research, durable code should still move back into modules, tests, and CLI smoke
commands after the exploratory loop stabilizes.

## Data Science Workbenches

The practical workflow should keep modules, CLIs, and tests as the durable
spine while adding a thin interactive workbench for exploration.

The useful pattern:

- permanent code lives in modules;
- Typer or similar CLIs expose repeatable operations;
- tests and tiny smoke commands make agent verification cheap;
- scratch analysis happens in text-first notebooks, scripts, marimo, or a
  persistent kernel;
- successful scratch work is promoted back into modules and tests.

This preserves the agent's strengths: editing files, running commands, reading
diffs, and iterating from failures. A persistent kernel is still valuable when
data loading is expensive or plots matter, but it should be treated as scratch
state rather than as the source of truth.

For plot-heavy exploratory analysis, the key requirement is not a notebook
file. It is a tool surface that can execute against live state, return rich
outputs, and let the model inspect plots or tables before deciding the next
analysis step. A Jupyter-backed MCP server is one way to expose that. A smaller
stateful Python execution tool may be enough when notebook editing is
incidental.

Useful command surfaces for agentic ML work:

```text
myproj dev load-sample --limit 1000
myproj dev fit-one-batch --config configs/tiny.yaml
myproj dev inspect-feature returns_ema --sample tiny
myproj kernel exec --name dev "df.head()"
```

The point is to give the agent fast, bounded feedback loops. Full data rebuilds,
production backtests, and credentialed actions should stay outside the default
tool surface unless explicitly approved.

## Editor Substrates

VS Code is a practical substrate because it already provides commands,
extension APIs, webviews, language services, and the ecosystem behind many AI
IDEs. Its limitation is also central: extensions are intentionally boxed behind
public APIs and cannot freely mutate the whole workbench like Emacs Lisp can
mutate Emacs.

That suggests a ladder:

- prototype inside VS Code, Joyride, Jupyter, marimo, or terminal tools;
- isolate the object model and command system from the host UI;
- fork or build a custom shell only after the extension surface becomes the
  bottleneck.

The first Genesis bet should probably be a terminal-first or notebook-controller
experiment, not a full IDE.

## Agent Harness Design

The durable harness properties are:

- typed tool calls with short, discriminative schemas;
- explicit permissions and reviewable patches;
- event logs for tool calls, results, and artifacts;
- visible compaction and memory objects;
- task frames that can be delegated to subagents;
- repeatable verification commands.

The harness should distinguish a custom tool from an MCP server. A tool is the
operation the agent invokes. MCP is a packaging and connection protocol that can
make those operations discoverable across clients. For a private Genesis
prototype, a direct tool can be simpler; MCP becomes valuable when the same
kernel, vault, or command surface should be reused by multiple agent clients.

The agent should be able to modify tools and workflows, but through ordinary
repo changes and tests. Recursive improvement is useful only when it remains
auditable.

## Open Questions

- Should the first build be a Jupyter-backed execution tool, a command palette,
  or a Weaver context compiler?
- What is the smallest command registry that would feel compounding rather than
  like a pile of scripts?
- How much should be hosted inside an existing editor versus a terminal-first
  substrate?
- What provenance format is rich enough for replay without making every session
  feel like a notebook?

## Source Map

- [Interactive Frameworks Exploration](../../../ops/artifacts/chatgpt/6995d77b-eae4-839a-8a44-b116ec7cba39.md)
- [Agentic Jupyter Framework Design](../../../ops/artifacts/chatgpt/69c55397-2afc-839a-85b1-a008c69855d9.md)
- [Tool Archetypes Exploration](../../../ops/artifacts/chatgpt/69514d7f-1ee0-8324-821b-e7b5e1f8c513.md)
- [VS Code for AI IDEs](../../../ops/artifacts/chatgpt/69515053-9434-8320-80d4-f013e4076f69.md)
- [Emacs of Agentic Harnesses](../../../ops/artifacts/chatgpt/69b809c3-7408-839c-a568-49bbf0275cea.md)
- [Agentic Workflows in ML](../../../ops/artifacts/chatgpt/69b6e7ae-cac0-8398-b6bf-506df883700b.md)
- [LLM Coding Workflows](../../../ops/artifacts/chatgpt/6a31f45a-f0e0-83ec-8a47-08c0e09e206c.md)
- [Context Management in LLMs](../../../ops/artifacts/chatgpt/69acf566-8c94-839f-9dc5-9e4931ab63ba.md)
- [All-In-One Text Editor](../../../ops/artifacts/chatgpt/39df03c2-2958-44ff-bac3-e23440a5ae5e.md)
