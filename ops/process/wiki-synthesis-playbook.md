# Wiki Synthesis Playbook

This playbook defines the repeatable process for turning triaged source
artifacts into curated wiki pages.

The current goal is to produce useful draft wiki pages with clear provenance.
Do not optimize for final polish too early. A page can become more concise after
its child pages and related project pages exist.

## Inputs

Start from these inputs:

- `ops/clusters/<date>/source-inventory.qmd`: human-readable synthesis queue.
- `ops/clusters/<date>/manifest.csv`: machine-readable bundle inventory.
- `ops/artifacts/<source>/`: applied per-source artifacts with YAML
  frontmatter.
- `raw/<source>/`: copied raw source material, used only when the artifact points
  to a transcript or copied note that must be read directly.
- `ops/context/project-glossary.yaml`: project names and descriptions.
- `ops/context/chatgpt-project-glossary.yaml`: inferred ChatGPT project ID
  mappings.

## Page Types

Use the smallest page type that fits the material.

- `project-hub`: overview page for a named project, with links to child concept
  and method pages.
- `concept`: durable idea that can apply across projects.
- `method`: reusable procedure, model, workflow, or implementation pattern.
- `research-thread`: investigation with open questions and partial results.
- `source-index`: intentionally source-facing map for a bundle or import batch.

Project hubs should be short. They should not carry every detail from a bundle
once child pages exist.

## Frontmatter

Every wiki page should have YAML frontmatter.

Required fields:

```yaml
---
title: Forecast Realization
status: draft
page_type: concept
projects:
  - obelisk
categories:
  - quant
source_bundles:
  - obelisk/quant
created: 2026-06-27
updated: 2026-06-27
---
```

Optional fields:

```yaml
parent: projects/obelisk
aliases:
  - realization schedule
related:
  - projects/obelisk/edge-and-utility
  - projects/p12n/temporal-modeling
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
confidence: medium
```

Status values:

- `draft`: synthesized but not yet reviewed.
- `reviewed`: checked for structure, source support, and obvious omissions.
- `stable`: useful enough to treat as ordinary wiki context.
- `archive`: retained mainly for historical context.

Page type values:

- `project-hub`
- `concept`
- `method`
- `research-thread`
- `source-index`

## Synthesis Process

1. Choose one bundle from the QMD inventory.
2. Read the bundle row, artifact links, and relevant raw notes/transcripts.
3. Decide whether the bundle should become one page or a hub plus child pages.
4. Draft the hub first if the bundle has more than one durable concept.
5. Move detailed material into child pages rather than making the hub long.
6. Put source links in compact `Sources` or `Source Map` sections.
7. Keep the body readable as distilled knowledge, not as a commentary on the
   source files.
8. Add open questions when the source material points to unresolved work.
9. Link related pages even if they do not exist yet, when the relationship is
   structurally important.
10. Leave the page as `status: draft` until a review pass checks scope and
    traceability.

## Decomposition Rules

Split a page when:

- a section could be useful outside the current project;
- a section has its own source cluster;
- a section contains methods, equations, or workflow details;
- the hub starts reading like a report rather than a map;
- multiple future pages would want to link to the same idea.

Keep material on the hub when:

- it defines the project;
- it summarizes durable lessons;
- it explains how child pages fit together;
- it warns how to interpret archive-mode or obsolete material.

## Source Use

Prefer this citation shape:

```markdown
Sources:
[trade-vs-forecast](../../ops/artifacts/obsidian/obelisk-trades-vs-forecast-and-optimization.md),
[summary](../../ops/artifacts/obsidian/obelisk-summary.md)
```

The prose should not cite every sentence. Instead, source sections should make
the support for each section auditable.

Use raw files only through artifact links where possible. If a claim depends on
raw transcript details, link the artifact that points to the transcript.

## Semantic Tags

Use YAML frontmatter now. Do not add XML-style semantic tags by default.

Inline semantic tags are allowed only when page-level metadata and source
sections are not enough. Prefer invisible comments over visible custom XML:

```markdown
<!-- weaver:claim id="forecast-realization-state" confidence="medium" -->
Forecast realization needs a low-dimensional state, otherwise the policy state
is effectively a vector of future returns.
<!-- /weaver:claim -->
```

Do not use inline semantic comments for ordinary prose. They add friction and
should be reserved for claims that need later machine extraction, review, or
cross-page reconciliation.

## Subagent Delegation Contract

A delegated synthesis task should include:

- bundle key, such as `obelisk/quant`;
- target page path;
- page type;
- required source artifacts;
- expected child pages or explicit instruction not to split;
- metadata values to use;
- constraints on scope;
- requested output shape.

Suggested task shape:

```text
Synthesize bundle: obelisk/quant
Target: wiki/projects/obelisk/forecast-realization.md
Page type: concept
Use sources:
- ops/artifacts/obsidian/obelisk-conditional-forecast-realization.md
- ops/artifacts/obsidian/obelisk-summary.md
- ops/artifacts/obsidian/obelisk-signal-research-and-feature-engineering.md
Constraints:
- Write distilled wiki prose, not a source summary.
- Include YAML frontmatter.
- Put source links at the bottom.
- Preserve open questions separately.
```

Subagents should not update project hubs independently unless the task asks for
hub integration. Hub updates are coordination points.

## Review Checklist

Before considering a page reviewed:

- frontmatter exists and uses known values;
- page title and path match the concept;
- body reads like wiki knowledge, not a triage report;
- source support is present but not noisy;
- obvious child pages are either created or listed as planned;
- open questions are separated from conclusions;
- archive-mode material is clearly marked when relevant;
- links are relative and point to existing files where possible.

## Current Convention

The first synthesized project page is `wiki/projects/obelisk.md`. It is a draft
project hub created from `obelisk/quant`. The next expected step is to split it
into child pages and shrink the hub into a map.
