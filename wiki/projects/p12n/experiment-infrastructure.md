---
title: Experiment Infrastructure
status: draft
page_type: project-system
projects:
  - p12n
categories:
  - quant
  - trading
  - infrastructure
  - experimentation
  - software
source_bundles:
  - p12n/project context
  - p12n/current priorities
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: projects/p12n
related:
  - projects/p12n
  - projects/p12n/feature-transforms-and-bst
  - projects/p12n/execution-and-policy
created: 2026-06-27
updated: 2026-06-27
---

# Experiment Infrastructure

P12n needs experiment infrastructure that makes modeling iterations cheap,
auditable, and separable by responsibility.

The core infrastructure idea is `duct`: a lightweight computational graph and
job registry for dependency resolution, in-memory caching, config management,
and lazy recomputation.

## Why It Exists

The p12n workflow has many derived artifacts:

- market data slices;
- feature transforms;
- binned feature indices;
- fold definitions;
- model predictions;
- out-of-fold derived predictions;
- execution simulations;
- reports and comparison metrics;
- threshold and policy refits.

Without an explicit pipeline layer, experiments become hard to compare because a
small parameter change can silently reuse the wrong intermediate product or
force too much recomputation.

`duct` is meant to solve:

- dependency resolution;
- intermediate product caching;
- parameter and config management;
- output directory management;
- isolating effects of parameter changes;
- lazy recomputation after argument replacement.

## Job Model

The desired abstraction is:

```text
job_name + output_name + branch_args -> output
```

Jobs are computational graph nodes. Functions are implementation details. The
decorator API is convenience, not the entire model.

Important design points:

- functions do not need to return dictionaries;
- output names can be declared in the job definition;
- auxiliary outputs can pipe inputs forward;
- input argument names can be inferred with `inspect`;
- global config overrides can be represented as inserted shims;
- jobs may be defined manually when decorator coupling is too restrictive.

The pipeline should make it easy to ask for a named output without manually
remembering every upstream call.

## Branches And Parameters

P12n experiments frequently vary:

- end month or date range;
- universe;
- fold definition;
- feature transform parameters;
- model hyperparameters;
- execution thresholds;
- BPTE step counts;
- symbol subsets.

The `duct` note frames a branch as the set of non-default arguments. That branch
should participate in cache keys so the system can tell when an upstream product
is still valid.

Open issue: mapped products over parameter sets need first-class support. A
single experiment often wants to run the same job over many universes, folds,
symbols, or thresholds and then compare outputs.

## Caching

The first implementation target is in-memory caching.

That is deliberately simpler than file caching:

- no global file layout decision;
- no serialization contract for every output;
- no stale artifact cleanup;
- easier reasoning while the graph design is still evolving.

The key requirement is that cached intermediate inputs are identified by all
relevant upstream arguments. A compound key based on job, output, and branch
arguments is the right mental model.

File-system caching is a later extension. It needs:

- persistent result paths;
- hash keys or parameterized filenames;
- parent output directories;
- read-from-file hooks;
- job-specific serialization logic.

This should probably be a `duct.Job` subclass or companion layer rather than the
first version of every job.

## Config Management

The infrastructure should prevent configuration from leaking into model code.

The p12n notes call out Rust specifically: shared config should not be embedded
in Rust code. The same applies to Python experiments. Config should be a graph
input or job output so experiments can be reproduced by branch arguments rather
than hidden globals.

Good config objects should make these effects explicit:

- date range;
- data source;
- universe;
- fold scheme;
- feature set;
- target definition;
- execution assumptions;
- report output path.

## Workflow Separation

The p12n overview notes a desired separation between:

- forecast training;
- execution simulation;
- threshold training;
- policy or BPTE training;
- reports and comparisons.

This separation is central. A forecast experiment should not implicitly refit a
threshold unless that is the experiment. A threshold refit should not be
mistaken for forecast improvement. A report should make clear which upstream
artifacts changed.

`duct` should make these boundaries visible by making each stage a named job
with typed outputs and explicit dependencies.

## Reports And Comparisons

Reports are part of the experiment graph, not an afterthought.

The current p12n notes mention:

- baseline EMA policy simulations in reports;
- incremental `R^2`;
- accuracy metrics;
- symbol and time labels;
- PnL per volume;
- disaggregated BPTE loss terms;
- model and statistic comparison files.

The infrastructure should prefer stable report artifacts that can be regenerated
from a branch. Reports should include enough metadata to answer:

```text
What data, features, targets, model params, execution assumptions, and threshold
params produced this result?
```

## Engineering Backlog

Near-term infrastructure backlog:

- logging in `Job` when jobs run;
- realistic example jobs;
- unit tests for caching behavior;
- pytest migration;
- product/mapped job support;
- job-output upstream argument syntax;
- file-system result cache design;
- mmap storage for binned feature indices;
- support one-off data fetching from REST or `data.binance.vision`;
- shared config loading for Rust and Python tools.

## Relationship To Other P12n Pages

[Feature Transforms And BST](feature-transforms-and-bst.md) needs the strongest
pipeline support because out-of-fold derived features, product bins, binned
indices, and residualized components create many intermediate artifacts.

[Execution And Policy](execution-and-policy.md) needs the clearest workflow
separation because forecast changes, threshold refits, execution assumptions,
and policy optimization can otherwise be conflated.

The modeling pages need the infrastructure to make comparisons cheap enough that
validation, not anecdote, decides which ideas survive.

## Open Questions

- What is the minimal stable `duct` API before file caching is added?
- Should output names be declared in job definitions, function annotations, or
  a separate registry file?
- How should branch arguments be normalized for hash keys?
- What artifact metadata belongs in every report?
- When should file-system caching become part of the framework rather than
  job-specific behavior?
- How should Rust jobs consume shared config without duplicating Python config
  logic?

## Source Map

- [p12n duct](../../../ops/artifacts/obsidian/p12n-duct.md)
- [p12n overview](../../../ops/artifacts/obsidian/p12n-overview.md)
- [p12n rust](../../../ops/artifacts/obsidian/p12n-rust.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
