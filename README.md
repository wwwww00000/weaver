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

## Development

```bash
uv run pytest
uv run weaver --help
```
