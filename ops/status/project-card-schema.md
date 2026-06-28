# Project Status Card Schema

Project status cards are the live-state layer for Weaver projects. They are
shorter and more current than wiki project pages. The wiki page owns durable
knowledge; the status card owns current focus, decisions, next actions, and
promotion candidates.

Cards live under:

```text
ops/status/projects/
```

## Frontmatter

Required fields:

```yaml
---
project: p12n
status: active
updated: 2026-06-29
wiki: ../../../wiki/projects/p12n.md
review_cadence: weekly
tags:
  - project-status
---
```

Field meanings:

- `project`: canonical project code name.
- `status`: `active`, `archive-mode`, `paused`, or `incubating`.
- `updated`: last human or agent update date.
- `wiki`: relative link to the durable project hub.
- `review_cadence`: expected review interval, usually `weekly`, `monthly`, or
  `as-needed`.
- `tags`: machine-friendly labels.

## Body

Each card should keep these headings in this order:

```md
<!-- weaver:project-status-card v1 -->

# Project Status

## Current Focus

## Recent Changes

## Decisions

## Next Actions

## Open Questions

## Blocked Or Waiting

## Promote To Wiki

## Links
```

Parsers should prefer frontmatter and heading names. The HTML comment is only a
lightweight marker so tools can distinguish status cards from ordinary notes.

## Dashboard Use

[dashboard.md](dashboard.md) should summarize the cards, not replace them. If a
dashboard statement and card statement conflict, the card is the source of
truth.

Older weekly context should be captured through git history or a future rolling
weekly note. Do not let project cards become long journals.
