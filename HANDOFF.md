# Codex Handoff: Initial Triage Tooling for Personal LLM Wiki

## Context

We are starting a new git-backed personal knowledge repo inspired by Karpathy’s LLM wiki idea, but with a stronger focus on personal note ingestion, Obsidian vault cleanup, ChatGPT conversation extraction, and later agent-assisted synthesis.

The immediate priority is **not** to build the full LLM wiki or cognitive IDE. The first implementation target is deterministic tooling for creating **human triage documents** from existing knowledge sources.

The user has two main existing sources:

1. An Obsidian vault with many Markdown notes.
2. OpenAI ChatGPT conversation exports.

The goal is to scan these sources and produce triage documents where the user can quickly decide what to include in the new wiki project.

A later design issue — how exactly to call LLMs from this system, whether interactively through Codex, via generated task envelopes, via `codex exec`, or through API calls — has been noted but should be deferred. For now, prefer deterministic Python tooling that produces explicit files for human review.

---

## Immediate Goal

Implement code that can:

1. Walk through one or more Obsidian vault directories.
2. Produce a triage document listing note files for human inclusion decisions.
3. Parse OpenAI ChatGPT export files.
4. Produce a similar triage document for ChatGPT conversations.
5. Use a common triage schema across both sources.
6. Support an `include later` category in addition to include/exclude decisions.

The intended workflow is:

```bash
weaver-notes triage obsidian /path/to/vault --out ops/triage/obsidian.md

weaver-notes triage chatgpt /path/to/chatgpt-export --out ops/triage/chatgpt.md
```

The generated Markdown files should be manually editable by the user.

---

## Suggested Project Layout

Assume this is a new repo, perhaps called `weaver-wiki` or `weaver-notes`.

```text
weaver-wiki/
  pyproject.toml
  README.md
  AGENTS.md

  ops/
    triage/
      obsidian.md
      chatgpt.md
    manifests/
      obsidian.csv
      chatgpt.csv

  raw/
    obsidian/
    chatgpt/

  wiki/
    index.md

  src/
    weaver_notes/
      __init__.py
      cli.py
      triage/
        __init__.py
        schema.py
        obsidian.py
        chatgpt.py
        render.py
```

Use Python. Typer is a good CLI choice, but argparse is acceptable if keeping dependencies minimal.

---

## Common Triage Model

Both Obsidian notes and ChatGPT conversations should be normalized into a common `TriageItem`.

Suggested fields:

```python
@dataclass
class TriageItem:
    source_id: str
    source_kind: Literal["obsidian", "chatgpt"]
    title: str
    path: str | None
    created_at: str | None
    updated_at: str | None
    size_bytes: int | None
    word_count: int | None
    summary_hint: str | None
    tags: list[str]
    suggested_decision: str | None
```

Do not overcomplicate v0. The main job is to produce a useful human checklist.

---

## Triage Decisions

The generated triage doc should allow these categories:

```text
[ ] include
[ ] extract-insights
[ ] include-later
[ ] skip
[ ] sensitive / exclude
```

Meanings:

* `include`: likely safe/useful to import as a source.
* `extract-insights`: do not import the full raw material, but later extract durable ideas.
* `include-later`: potentially useful, but not part of initial batch.
* `skip`: low value, obsolete, duplicate, or not worth migrating.
* `sensitive / exclude`: personal/private material that should not enter the new repo.

The `include-later` category matters. It lets the user avoid all-or-nothing decisions during the first pass.

---

## Obsidian Triage

Implement a scanner that recursively walks one or more vault directories and finds Markdown files.

Ignore common directories by default:

```text
.obsidian/
.trash/
.git/
node_modules/
```

Potentially also ignore attachments unless explicitly requested:

```text
assets/
attachments/
```

For each Markdown file, capture:

* relative path
* file stem as title
* size
* modified time
* approximate word count
* first heading if available
* YAML frontmatter tags if available
* Obsidian-style `#tags` if easy to extract
* whether file appears empty or very short

The generated Obsidian triage document could look like:

```markdown
# Obsidian Vault Triage

Generated: 2026-06-21

Instructions:
Mark one decision for each note. Add brief comments where useful.

Decision options:
- include
- extract-insights
- include-later
- skip
- sensitive / exclude

## Summary

- Total markdown files: 1234
- Empty or tiny files: 42
- Large files: 17

## Notes

### 001. Project Ideas
- source_id: obsidian:project-ideas
- path: Projects/Project Ideas.md
- words: 842
- modified: 2025-11-03
- tags: project, ideas

Decision:
- [ ] include
- [ ] extract-insights
- [ ] include-later
- [ ] skip
- [ ] sensitive / exclude

Comments:
>
```

Also emit a machine-readable manifest CSV or JSONL containing the same item metadata. This will make later processing easier.

---

## ChatGPT Export Triage

OpenAI ChatGPT exports usually contain a `conversations.json` file. Implement a parser that can handle a directory path or direct JSON file path.

For each conversation, extract:

* conversation id
* title
* create time
* update time
* number of messages
* approximate total words / chars
* first user message excerpt
* maybe last user message excerpt
* maybe keyword hints from title or first messages

Do not try to perfectly reconstruct every conversation in v0. The immediate goal is triage.

Generated ChatGPT triage document could look like:

```markdown
# ChatGPT Conversation Triage

Generated: 2026-06-21

Instructions:
Mark one decision for each conversation. Prefer `extract-insights` for conversations that contain useful ideas but should not be imported verbatim.

Decision options:
- include
- extract-insights
- include-later
- skip
- sensitive / exclude

## Summary

- Total conversations: 430
- Long conversations: 31
- Untitled conversations: 12

## Conversations

### 001. Training Data Attribution
- source_id: chatgpt:abc123
- created: 2026-06-19
- updated: 2026-06-19
- messages: 8
- approx_words: 2450

First user message:
> is there a way to get an interpretable decomposition of a neural networks predictions...

Decision:
- [ ] include
- [ ] extract-insights
- [ ] include-later
- [ ] skip
- [ ] sensitive / exclude

Comments:
>
```

Also emit a manifest CSV or JSONL.

---

## CLI Design

Suggested commands:

```bash
weaver-notes triage obsidian VAULT_PATH --out ops/triage/obsidian.md
weaver-notes triage chatgpt EXPORT_PATH --out ops/triage/chatgpt.md
```

Nice-to-have options:

```bash
--manifest ops/manifests/obsidian.csv
--include-glob "**/*.md"
--exclude-glob ".obsidian/**"
--max-excerpt-chars 500
--sort modified-desc
--sort title
--sort path
--limit 100
```

Do not build LLM calls yet. These commands should be deterministic.

---

## Rendering Requirements

The Markdown triage docs should be optimized for manual scanning and editing.

Prefer:

* clear section headings
* stable numbering
* checkboxes for decisions
* compact metadata
* short excerpts
* comments block
* summary counts at top

Avoid producing giant walls of text. For Obsidian, filenames and paths are usually enough. For ChatGPT, title plus first user excerpt is useful.

---

## Later Compatibility

Design with later stages in mind:

1. The user manually edits triage docs.
2. A later command parses completed triage docs.
3. The system copies/imports selected raw sources.
4. Another agent/Codex task extracts durable insights into the compiled wiki.

So the generated triage docs should be parseable enough. Consider using a stable marker per item:

```markdown
<!-- triage-item: obsidian:abc123 -->
```

or:

```markdown
source_id: obsidian:abc123
```

Later we can implement:

```bash
weaver-notes triage apply ops/triage/obsidian.md
```

But that is not required for the first pass.

---

## Implementation Priorities

1. Set up Python package and CLI.
2. Implement common `TriageItem`.
3. Implement Obsidian scanner.
4. Implement ChatGPT export parser.
5. Implement Markdown renderer.
6. Emit manifest CSV/JSONL.
7. Add minimal tests with fixture files.
8. Add README examples.

Keep the implementation simple and inspectable. Do not introduce a database, vector index, or LLM API calls.

---

## Testing Ideas

Create small fixtures:

```text
tests/fixtures/obsidian/
  Projects/Foo.md
  Journal/2024-01-01.md
  .obsidian/app.json

tests/fixtures/chatgpt/
  conversations.json
```

Test that:

* ignored directories are ignored
* Markdown files are found
* word counts are roughly correct
* frontmatter tags are detected
* ChatGPT conversations are parsed
* Markdown triage docs contain stable source ids
* manifest rows match generated triage items

---

## Design Principle

The first version should help the user answer:

> “Which parts of my existing knowledge mess are worth bringing into the new LLM wiki?”

It should not yet answer:

> “How do we automatically synthesize all of this into a finished wiki?”

That comes later.

