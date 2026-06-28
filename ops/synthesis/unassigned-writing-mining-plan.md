# Unassigned Writing Mining Plan

Date: 2026-06-28

This is the routing layer for `unassigned/writing` source artifacts. It is not
final wiki prose. Use it to decide which existing page, new page, or defer
bucket should consume each source.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Method

Treat `unassigned/writing` as three overlapping queues:

- `chronicle`: writing practice, journaling, voice, style, metaphor, poetry,
  eloquence, reflection, and everyday literary attention.
- `conjuration`: fiction premises, worldbuilding, speculative concepts,
  characters, plot devices, and imagination-to-story practice.
- `genesis`: writing or note-taking tools, AI-assisted writing systems, and
  Weaver-facing knowledge interfaces.

Actions:

- `merge`: read during the next pass for the destination page.
- `dual-link`: split between a project-facing page and a reusable concept or
  method page.
- `new-page`: create a candidate page before synthesis.
- `defer`: leave out of the next pass unless a later page needs it.
- `skip`: low-signal, duplicate, empty, or better handled by another queue.

Priority means:

- `P1`: useful for the next page-deepening pass.
- `P2`: potentially useful, but not worth blocking the next pass.
- `P3`: likely skip or archive-only.

## Queue Order

| Queue | Count | First pass |
| --- | ---: | --- |
| Chronicle Writing Practice And Voice | 13 | Create or deepen a Chronicle child page for writing practice, voice, and poetic attention. |
| Conjuration Fiction Premises And Worldwork | 11 | Deepen Sourcebook Worldwork or create a fiction-premise page if the concepts are large enough. |
| Weaver And AI Writing Tools | 2 | Route to Genesis Weaver/agentic tooling only if new tool interface insights remain. |
| Defer Or High-Level Only | 2 | Keep sensitive premise notes out of detailed synthesis unless reframed safely. |

## Status

- 2026-06-28: Created initial routing plan for `unassigned/writing`.
- 2026-06-28: Completed the Chronicle writing practice and voice pass:
  [Writing Practice And Voice](../../wiki/projects/chronicle/writing-practice-and-voice.md).
- 2026-06-28: Completed the Conjuration fiction premises and worldwork pass:
  [Fiction Premises And Motif Catalog](../../wiki/projects/conjuration/fiction-premises-and-motif-catalog.md),
  with a boundary link from
  [Sourcebook Worldwork](../../wiki/projects/conjuration/sourcebook-worldwork.md).
- 2026-06-28: Completed the Weaver/AI writing tools cleanup:
  `LLM Note-taking Tools` was already mined into
  [Weaver As A Knowledge System](../../wiki/projects/genesis/weaver-as-knowledge-system.md),
  and `Switching Cognitive Modes` was merged into
  [Writing Practice And Voice](../../wiki/projects/chronicle/writing-practice-and-voice.md).

## Chronicle Writing Practice And Voice

Primary destination:
new Chronicle child page candidate `wiki/projects/chronicle/writing-practice-and-voice.md`.

Secondary destinations:
[Morning Pages And Life OS](../../wiki/projects/chronicle/morning-pages-and-life-os.md),
[Travel And Environment Design](../../wiki/projects/chronicle/travel-and-environment-design.md),
and [Conjuration Visualization And Imagination Training](../../wiki/projects/conjuration/visualization-and-imagination-training.md)
when the material becomes imagination practice.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Creative Journaling Ideas](../artifacts/chatgpt/67f79e50-67fc-8009-b997-323354966349.md) | merge | P1 | Journaling prompts and creative reflection. |
| [Daily Writing Exercises](../artifacts/chatgpt/67e297fe-698c-8009-a997-46ffa17c2ff6.md) | merge | P1 | Habit and exercise loop. |
| [Developing Eloquence and Metaphors](../artifacts/chatgpt/f3874be3-2942-45be-8808-da0b3bcfc8aa.md) | merge | P1 | Style, metaphor, and speech/writing precision. |
| [Exercise-Centric Writing Books](../artifacts/chatgpt/1f7f7ae1-a193-4ffc-8950-2ae7db80efc1.md) | merge | P1 | Book/source recommendations as practice design. |
| [Exploring Writing Styles](../artifacts/chatgpt/afb27847-8584-4eba-b585-6c8fa474c147.md) | merge | P1 | Style sampling and deliberate imitation. |
| [Lyrical Quality of Lyrics](../artifacts/chatgpt/683ec446-d7f8-8009-b68e-162b5fbad2fa.md) | merge | P2 | Lyricism, compression, musical language. |
| [Poetry in Everyday Things](../artifacts/chatgpt/e2a1f094-8642-4820-95c7-e5effe66dc07.md) | merge | P1 | Poetic attention and ordinary detail. |
| [Portable Reflection Practices](../artifacts/chatgpt/67e9464a-bfd0-8009-993f-980a427bb245.md) | skip | P3 | Already mined into Chronicle meditation and portable reflection. |
| [Writers Travel for Inspiration](../artifacts/chatgpt/d71d0d40-779c-49cb-9cbc-a953632c61ea.md) | dual-link | P2 | Chronicle travel/environment bridge. |
| [ideas](../artifacts/obsidian/writing-exercises-the-reluctant-i.md) | merge | P1 | Specific writing exercise source. |
| [morning pages](../artifacts/obsidian/books-the-artist-s-way.md) | merge | P2 | Artist's Way and morning-pages practice. |
| [the poetic state](../artifacts/obsidian/the-poetic-state.md) | merge | P1 | Poetic state and literary attention. |
| [writing exercise list](../artifacts/obsidian/writing-exercise-list.md) | merge | P1 | Exercise list; likely compact into practice page. |

## Conjuration Fiction Premises And Worldwork

Primary destination:
[Sourcebook Worldwork](../../wiki/projects/conjuration/sourcebook-worldwork.md)
unless the fiction-premise cluster becomes large enough to deserve its own
Conjuration child page.

Secondary destination:
[Visualization And Imagination Training](../../wiki/projects/conjuration/visualization-and-imagination-training.md)
when a source is mainly imagery or persona practice.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [anonymous office employees](../artifacts/obsidian/anonymous-office-employees.md) | merge | P2 | Character/social premise. |
| [approach](../artifacts/obsidian/proof-by-contradiction.md) | merge | P2 | Abstract approach or argumentative premise. |
| [dictionary of obscure singaporean sorrows](../artifacts/obsidian/dictionary-of-obscure-singaporean-sorrows.md) | dual-link | P1 | Chronicle voice plus Conjuration concept catalog. |
| [magician fantasy](../artifacts/obsidian/magician-fantasy.md) | merge | P1 | Fantasy premise and world rules. |
| [perception is reality](../artifacts/obsidian/perception-is-reality.md) | merge | P1 | Speculative metaphysics premise. |
| [prometheus](../artifacts/obsidian/prometheus.md) | merge | P2 | Mythic/speculative premise. |
| [reconnaissance high school](../artifacts/obsidian/reconnaissance-high-school.md) | merge | P1 | Story premise. |
| [revolution](../artifacts/obsidian/revolution.md) | merge | P2 | Political/story premise. |
| [story ideas](../artifacts/obsidian/story-ideas.md) | merge | P1 | Existing worldwork source already referenced; inspect for remaining details. |
| [worldbuilding](../artifacts/obsidian/writing-books.md) | merge | P1 | Worldbuilding book/source note already referenced by Sourcebook Worldwork. |
| [unique skill](../artifacts/obsidian/unique-skill.md) | merge | P2 | RPG-like self/persona skill frame; useful for motif catalog. |

## Weaver And AI Writing Tools

Primary destinations:
[Weaver As A Knowledge System](../../wiki/projects/genesis/weaver-as-knowledge-system.md)
and [Agentic Tooling](../../wiki/projects/genesis/agentic-tooling.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [LLM Note-taking Tools](../artifacts/chatgpt/67e29c1d-88f4-8009-b717-e92513a6543e.md) | skip | P3 | Already mined during `unassigned/ai` into Weaver/agentic tooling. |
| [Switching Cognitive Modes](../artifacts/chatgpt/69872a09-944c-83a0-b662-670e2c57db24.md) | merge | P2 | Writing-mode transition ritual merged into Chronicle writing practice. |

## Defer Or High-Level Only

Primary destination:
defer unless a future fiction-premise page needs a high-level motif.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [infohazard terrorism](../artifacts/obsidian/infohazard-terrorism.md) | defer | P3 | Sensitive premise; do not expand operational detail. |
| [lethal injection](../artifacts/obsidian/lethal-injection.md) | defer | P3 | Dark/sensitive premise; high-level fiction motif only if needed. |

## Next Pass

The Chronicle writing practice/voice, Conjuration fiction-premise, and
Weaver/AI cleanup passes are complete. The two deferred sensitive premise
notes remain archive-only unless a future fiction page needs a high-level
motif. The `unassigned/writing` queue has now been mined at first-pass depth.
