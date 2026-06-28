# Weaver Agent Notes

This repository contains deterministic tooling for triaging personal knowledge
sources before they are imported into a curated wiki.

Keep v0 focused on explicit files for human review. Do not add LLM calls,
databases, vector indexes, or automatic synthesis until the triage workflow is
working end to end.

Generated triage documents should remain editable Markdown, with stable
`source_id` markers and matching machine-readable manifests.

For wiki synthesis, review, or source-mining tasks, read
`ops/process/wiki-synthesis-playbook.md` and
`ops/process/wiki-synthesis-task-template.md` before writing or delegating wiki
pages. Treat those files as the workflow source of truth.
