# Weaver Agent Notes

This repository contains deterministic tooling for triaging personal knowledge
sources before they are imported into a curated wiki.

Keep v0 focused on explicit files for human review. Do not add LLM calls,
databases, vector indexes, or automatic synthesis until the triage workflow is
working end to end.

Generated triage documents should remain editable Markdown, with stable
`source_id` markers and matching machine-readable manifests.
