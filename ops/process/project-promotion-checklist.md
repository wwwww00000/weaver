# Project Promotion Checklist

Use this checklist when a child page, topic page, source stream, or informal
work label should become a top-level project.

Promotion is a classification change, not a source rewrite. Keep historical
triage files, generated manifests, and copied source artifacts as records of
what the system believed at the time. Update current context, wiki, status, and
process files so future work routes correctly.

## Promotion Criteria

Promote a label when most of these are true:

- it has an ongoing workstream, not just a reusable idea;
- it needs its own current-state card, next actions, and open questions;
- future notes should route to it before broader parent projects or categories;
- it has enough durable material for a project hub;
- its boundary can be stated without making an existing project incoherent.

Do not promote a label just because a source bundle is large. Large reusable
idea clusters should usually become topic pages.

## Required Updates

1. Choose the canonical slug, title, status, and one-sentence description.
2. Update project context:
   - [ops/context/projects.md](../context/projects.md)
   - [ops/context/project-glossary.yaml](../context/project-glossary.yaml)
   - [ops/context/chatgpt-project-glossary.yaml](../context/chatgpt-project-glossary.yaml),
     if exported ChatGPT project IDs should now map to the promoted project.
3. Create or move the wiki hub to `wiki/projects/<slug>.md`.
4. Set wiki frontmatter:
   - `page_type: project-hub`
   - `projects: [<slug>]`
   - relevant `categories`
   - `source_bundles`
   - `source_inventory`
   - `related`
   - `updated`
5. Update the old parent or sibling page to explain the new boundary.
6. Update [wiki/index.md](../../wiki/index.md).
7. Add `ops/status/projects/<slug>.md` using
   [project-card-schema.md](../status/project-card-schema.md).
8. Update [ops/status/dashboard.md](../status/dashboard.md).
9. Update related status cards so they link to the new project where useful.
10. Update process or planning docs that link to the old page path.

## Path And Link Rules

- Prefer moving the existing synthesized page when it already represents the
  promoted project.
- If the old page path has many current links, update those links instead of
  leaving a duplicate page.
- Do not rewrite old generated artifacts solely for link freshness.
- Keep source-map links relative to the new page path.
- If keeping a bridge page at the old path, make it short and clearly point to
  the new canonical project hub.

## Boundary Notes

Every promotion should leave behind a boundary statement in the old parent or a
nearby sibling page. The statement should answer:

- what the promoted project now owns;
- what the old project still owns;
- when future artifacts should be dual-labeled;
- which project status card owns live decisions.

For example, Weaver now owns source triage, wiki synthesis, provenance, status
surfaces, semantic note mechanics, and context compilation. Genesis still owns
broader building practice, AI research, agentic tooling, and software projects
that are not primarily about the knowledge system.

## Checks

Before finishing:

- run `git diff --check`;
- run the local Markdown link checker over touched Markdown files;
- check that every status card still has the project-card marker and expected
  heading order;
- run project inventory tests when glossary changes could affect tooling;
- report whether historical generated files were intentionally left unchanged.
