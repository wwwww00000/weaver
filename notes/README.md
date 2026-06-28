# Notes Inbox

Use `notes/inbox/` for new Markdown notes that should enter Weaver directly
without an Obsidian vault import step.

Typical flow:

```bash
uv run weaver triage notes
uv run weaver triage apply-notes ops/triage/notes.md
uv run weaver cluster qmd
```

For notes outside the repo, point `--source-root` at the directory that owns the
files and pass file or directory paths relative to that root:

```bash
uv run weaver triage notes idea.md --source-root /path/to/source
uv run weaver triage apply-notes ops/triage/notes.md --source-root /path/to/source
```
