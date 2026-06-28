# Weaver

Deterministic triage tooling for building a personal knowledge wiki from
existing sources.

The first workflow scans an Obsidian vault and writes:

- an editable Markdown triage document for human decisions
- a CSV manifest with the same source metadata for later processing

Each note gets an editable `Category labels` field. Use it for comma-separated
labels you want to assign during triage, distinct from source tags already found
in Obsidian notes.

```bash
weaver triage obsidian /path/to/vault --out ops/triage/obsidian.md
```

If no vault path is provided, the command scans
`/mnt/c/Users/limwe/Documents/obsidian`. By default, it ignores common Obsidian
metadata and low-signal bulk directories: `.obsidian/`, `.trash/`, `.git/`,
`node_modules/`, `assets/`, `attachments/`, `daily/`, and `weekly/`.

By default, the command writes `ops/triage/obsidian.md` and
`ops/manifests/obsidian.csv`.

After marking decisions in the triage document, apply selected notes with:

```bash
weaver triage apply ops/triage/obsidian.md
```

By default, `apply` copies notes marked `include` or `extract-insights` into
`raw/obsidian/` and writes per-note intermediate artifacts plus an index under
`ops/artifacts/obsidian/`.

ChatGPT exports can be triaged from an extracted export directory, a direct
conversation JSON file, or a ZIP archive:

```bash
weaver triage chatgpt raw/exports/chatgpt/2026-06-23 --out ops/triage/chatgpt.md
```

For large exports, split the triage into smaller part files:

```bash
weaver triage chatgpt raw/exports/chatgpt/2026-06-23 --split-size 100
```

After marking decisions, apply selected ChatGPT conversations with:

```bash
weaver triage apply-chatgpt ops/triage/chatgpt.md
```

By default, `apply-chatgpt` copies conversations marked `include` or
`extract-insights` into `raw/chatgpt/` as JSON plus Markdown transcripts, and
writes per-conversation intermediate artifacts under `ops/artifacts/chatgpt/`.

After applying source triage, generate a deterministic QMD inventory workbench:

```bash
weaver cluster qmd
```

By default, this reads `ops/artifacts/obsidian/` and
`ops/artifacts/chatgpt/`, infers project labels from source metadata and
glossary files, normalizes obvious category typos, and writes
`ops/clusters/<date>/source-inventory.qmd` plus `manifest.csv`. The QMD also
includes candidate synthesis bundles keyed by `project/category` and simple
lexical topic hints for unassigned artifacts.

## Project Status

Current project state lives in [ops/status/dashboard.md](ops/status/dashboard.md)
with one editable status card per project under `ops/status/projects/`. The
schema is documented in
[ops/status/project-card-schema.md](ops/status/project-card-schema.md).

## Development

```bash
uv run pytest
uv run weaver --help
```
