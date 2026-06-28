# Unassigned Cognitive Mining Plan

Date: 2026-06-28

This is the routing layer for `unassigned/cognitive` source artifacts. It is not
final wiki prose. Use it to decide which existing page, new page, or defer bucket
should consume each source.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Method

Treat `unassigned/cognitive` as a mining queue, not as one giant cognition page.

For each artifact, assign:

- `merge`: read during the next pass for the destination page.
- `dual-link`: split between a project-facing page and a durable topic or
  adjacent project page.
- `new-page`: create a candidate page before synthesis.
- `defer`: leave out of the next pass unless a later page needs it.
- `skip`: low-signal or not worth importing into the wiki.

Priority means:

- `P1`: useful for the next page-deepening pass.
- `P2`: potentially useful, but not worth blocking the next pass.
- `P3`: likely skip or archive-only.

## Queue Order

| Queue | Count | First pass |
| --- | ---: | --- |
| Problem Solving And Skill Acquisition | 19 | Create a Whetstone child page and link to Revelation where math learning is specific. |
| Attention And Mental-State Regulation | 14 | Deepen Whetstone felt-sense/modes and possibly Chronicle attention hygiene. |
| Contemplative Practice And Liminal Cognition | 11 | Split Chronicle meditation/nonduality from Whetstone state-control mechanics. |
| Visualization And Imagination Practice | 4 | Dual-link Whetstone cognitive technique and Conjuration imagination practice. |
| Knowledge Systems And Agency Spillovers | 3 | Route to Genesis/Weaver and Whetstone only where cognitive tooling is explicit. |
| Personal Life Operations Spillovers | 5 | Save for `unassigned/personal` unless needed by Chronicle/Whetstone pages. |

## Status

- 2026-06-28: Created initial routing plan for `unassigned/cognitive`.
- 2026-06-28: Completed the problem-solving and skill-acquisition pass:
  [Whetstone problem solving and skill acquisition](../../wiki/projects/whetstone/problem-solving-and-skill-acquisition.md).
- 2026-06-28: Completed the attention and state-regulation pass:
  [Attention And State Regulation](../../wiki/projects/whetstone/attention-and-state-regulation.md),
  with supporting updates to Whetstone, Chronicle, Felt Sense, and Morning
  Pages.
- 2026-06-28: Completed the contemplative practice and liminal cognition pass:
  [Meditation And Nonduality](../../wiki/projects/chronicle/meditation-and-nonduality.md),
  with a bounded Conjuration cross-link for liminal imagery.
- 2026-06-28: Completed the visualization and imagination practice pass:
  [Conjuration visualization and imagination training](../../wiki/projects/conjuration/visualization-and-imagination-training.md)
  and [Whetstone problem solving and skill acquisition](../../wiki/projects/whetstone/problem-solving-and-skill-acquisition.md).
- 2026-06-28: Completed the knowledge systems and agency spillover pass:
  [Genesis Weaver as knowledge system](../../wiki/projects/genesis/weaver-as-knowledge-system.md)
  and [Whetstone think tags and metacognition](../../wiki/projects/whetstone/think-tags-and-metacognition.md).

## Problem Solving And Skill Acquisition

Primary destination:
[Whetstone problem solving and skill acquisition](../../wiki/projects/whetstone/problem-solving-and-skill-acquisition.md).

Secondary destinations when useful:
[Think Tags And Metacognition](../../wiki/projects/whetstone/think-tags-and-metacognition.md)
and [Revelation active learning](../../wiki/projects/revelation/active-learning-for-math-and-physics.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Brain Networks in Problem-Solving.](../artifacts/chatgpt/b1dc3a90-0f45-427d-a986-dff17d101f39.md) | merge | P1 | Cognitive network framing for problem solving. |
| [Metacognition in problem solving.](../artifacts/chatgpt/a84f0334-18ef-420b-997c-45dbaf6ba2e4.md) | merge | P1 | Monitoring and control during hard tasks. |
| [Problem-solving Competencies](../artifacts/chatgpt/565db9f3-9674-4601-89b3-31f2b55abec1.md) | merge | P1 | Competency taxonomy. |
| [Problem Solving Competencies](../artifacts/chatgpt/029dbdb1-6e82-409d-a8bd-8bc0408cabbe.md) | merge | P1 | Related competency taxonomy; reconcile with duplicate title. |
| [problem solving](../artifacts/obsidian/problem-solving.md) | merge | P1 | Obsidian note for personal problem-solving framing. |
| [Decision Loop Models](../artifacts/chatgpt/b9793ea5-5532-4ee3-a262-284ca09fe287.md) | merge | P1 | Loop model for cognitive control. |
| [Diverse Internal Mental Models](../artifacts/chatgpt/6894a6ab-551b-474d-a4e9-7eb5719792bb.md) | merge | P1 | Mental-model diversity as problem-solving resource. |
| [Cognitive Skills Enhancement Exercises](../artifacts/chatgpt/43e3c0b2-3688-469a-9337-573d3d04afe6.md) | merge | P1 | Drill menu for Whetstone. |
| [Mind Gym Workout Plan](../artifacts/chatgpt/68122dfb-d4dc-8009-a6a0-ddcff4693eca.md) | merge | P1 | Practice structure for cognitive exercises. |
| [Cognitive training analogy](../artifacts/chatgpt/68f1e100-d078-8324-8bb1-232d951a71fa.md) | merge | P1 | Training analogy and transfer caveats. |
| [Efficient Skill Acquisition Strategies](../artifacts/chatgpt/5563ad7d-f855-4ee5-8e6e-20e97d04bbab.md) | merge | P1 | Skill acquisition loop. |
| [Metacognition Enhances Skill Acquisition](../artifacts/chatgpt/1b354d00-21dd-4348-9de0-f51d78260a2c.md) | merge | P1 | Metacognitive monitoring in practice. |
| [Previsualization for Skill Acquisition](../artifacts/chatgpt/bbdfbb2e-feb6-4d99-8785-1c76619161f4.md) | dual-link | P1 | Skill acquisition plus visualization bridge. |
| [Self-Improvement through Skill Analysis](../artifacts/chatgpt/d0dc26f6-cd63-4b4e-aa45-457c8f12185f.md) | merge | P1 | Decompose self-improvement into trainable subskills. |
| [Effective Learning: Project vs. Drilling](../artifacts/chatgpt/31f75215-9321-4cb7-9786-704625233ac9.md) | dual-link | P1 | Learning strategy; also useful for Revelation. |
| [Linear vs Depth-First Learning](../artifacts/chatgpt/10e5bea0-e687-4057-ada7-a6f637ff4b7c.md) | dual-link | P1 | Learning route strategy; also useful for Revelation. |
| [learning matrix style](../artifacts/obsidian/learning-matrix-style.md) | dual-link | P1 | Obsidian learning strategy note. |
| [Commonalities in Technical Fields](../artifacts/chatgpt/7ead5315-8e81-4b69-bed6-aa1a933b2b73.md) | merge | P2 | Transfer across technical domains. |
| [Mental Fatigue: Reading Mathematics](../artifacts/chatgpt/f4d0ea68-cbba-4e8f-a5b8-8031e03a037d.md) | dual-link | P2 | Cognitive-load note; Revelation-specific detail. |

## Attention And Mental-State Regulation

Primary destinations:
[Felt Sense And Modes](../../wiki/projects/whetstone/felt-sense-and-modes.md)
and [Chronicle morning pages and life OS](../../wiki/projects/chronicle/morning-pages-and-life-os.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Balancing DMN and Exec Functions](../artifacts/chatgpt/e83a5506-3dfc-4e31-a84a-009109d64433.md) | merge | P1 | Default-mode/executive balance and state switching. |
| [Cognitive Tricks for Focus](../artifacts/chatgpt/67e94beb-ef98-8009-8545-9d88804e077d.md) | merge | P1 | Focus tactics. |
| [Cognitive Behavioral Therapy for Performance Enhancement](../artifacts/chatgpt/d7d53c0d-ce50-4ae6-871c-8f8047fe1c4b.md) | merge | P1 | Performance and reframing techniques. |
| [Productivity Improvement Techniques](../artifacts/chatgpt/d9a6f79a-85ca-4600-bbf5-6911ecf1f3ff.md) | dual-link | P2 | Productivity tactics; likely overlaps personal operations. |
| [Book summary stress management](../artifacts/chatgpt/68bc4c3e-a4cc-8323-aeb7-e0951b601ed6.md) | merge | P2 | Stress management summary. |
| [Two Mental Modes Explained](../artifacts/chatgpt/9d7b6484-cfcc-40e0-b9f4-1f2a7a0a689b.md) | merge | P1 | Mode vocabulary. |
| [Modes of Thought Insights](../artifacts/chatgpt/3c31f6d3-5117-4fda-8eaf-e0bd24946d86.md) | merge | P1 | Thought-mode taxonomy. |
| [Understanding Qualia](../artifacts/chatgpt/0a267517-4534-442d-b70e-fcb24591491b.md) | merge | P2 | Qualia and introspective vocabulary. |
| [resources](../artifacts/obsidian/low-level-consciousness.md) | merge | P2 | Low-level consciousness resource note. |
| [practices](../artifacts/obsidian/qualia-neural-circuits-mental-modes.md) | merge | P1 | Obsidian note for mode and qualia practices. |
| [Autism Stimming Behaviors Explanation](../artifacts/chatgpt/b133f591-b3fd-43e4-a448-368534785e2d.md) | merge | P2 | Use carefully as regulation/stimming context, not diagnosis. |
| [Regaining Rich Thought Patterns](../artifacts/chatgpt/67d45443-b6c4-8009-b03a-8dd16b8a8c62.md) | merge | P1 | Recovering rich internal cognition. |
| [Vivid Eclectic Thought Experience](../artifacts/chatgpt/8ee2dbd5-5b98-45fb-89fa-f1aa52b3ba5d.md) | merge | P1 | First-person state vocabulary. |
| [Disconnected self: Unease and erosion.](../artifacts/chatgpt/8dba6d1d-fd8e-4178-91ce-55de91d68f5a.md) | dual-link | P2 | Chronicle-facing self/state note. |

## Contemplative Practice And Liminal Cognition

Primary destination:
[Chronicle morning pages and life OS](../../wiki/projects/chronicle/morning-pages-and-life-os.md).

Secondary destination:
[Felt Sense And Modes](../../wiki/projects/whetstone/felt-sense-and-modes.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Build Meditation Habit.](../artifacts/chatgpt/8253f6fe-81ac-40a3-8cbf-542816adc4c5.md) | merge | P1 | Meditation habit formation. |
| [Jhanas and Meditation Practice](../artifacts/chatgpt/67d1aca5-c834-8009-9fc6-6a54992b671d.md) | merge | P1 | Concentration practice. |
| [meditation](../artifacts/obsidian/meditation.md) | merge | P1 | Obsidian meditation note. |
| [Nondual Awareness Instructions](../artifacts/chatgpt/1ef216c2-b5ff-4a86-8096-9073f16a7a85.md) | merge | P1 | Nondual instruction source. |
| [nonduality](../artifacts/obsidian/books-waking-up.md) | merge | P1 | Waking Up / nonduality note. |
| [Rituals for altered consciousness](../artifacts/chatgpt/06e7e981-6a83-404a-bffe-8a5b11cc8857.md) | merge | P2 | Altered-state ritual source. |
| [Lucid Dreaming Techniques](../artifacts/chatgpt/673caaf4-09dc-8009-9aef-07872776aa5f.md) | dual-link | P2 | Liminal practice plus Conjuration. |
| [lucid dreaming](../artifacts/obsidian/lucid-dreaming.md) | dual-link | P2 | Obsidian lucid-dreaming note. |
| [Edison's Pen Inspiration](../artifacts/chatgpt/37e6cc50-f4d0-48c3-851c-1151ef27c0c2.md) | dual-link | P2 | Hypnagogic capture; Chronicle/Conjuration bridge. |
| [ideas before bed](../artifacts/obsidian/ideas-before-bed.md) | dual-link | P2 | Bedtime ideation and capture. |
| [Portable Reflection Practices](../artifacts/chatgpt/67e9464a-bfd0-8009-993f-980a427bb245.md) | dual-link | P1 | Reflection practice; also writing queue. |

## Visualization And Imagination Practice

Primary destinations:
[Conjuration visualization and imagination training](../../wiki/projects/conjuration/visualization-and-imagination-training.md)
and [Whetstone problem solving and skill acquisition](../../wiki/projects/whetstone/problem-solving-and-skill-acquisition.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Tesla's Visualization Technique](../artifacts/chatgpt/554d6d50-4e57-44dd-9495-a9038c61feb5.md) | dual-link | P1 | Visualization as cognitive technique and imagination practice. |
| [Visualization Techniques for Cognitive Tasks](../artifacts/chatgpt/4254a9f4-dc4b-4c3e-90c0-c9cf4885af68.md) | dual-link | P1 | Cognitive visualization toolkit. |
| [Creative Commute Exercises](../artifacts/chatgpt/4f97f718-3907-48ae-898a-1b01f112e69c.md) | dual-link | P2 | Commute exercises; Conjuration and Chronicle. |
| [chuu2](../artifacts/obsidian/imagination.md) | dual-link | P1 | Obsidian imagination note. |

## Knowledge Systems And Agency Spillovers

Primary destinations:
[Genesis Weaver as knowledge system](../../wiki/projects/genesis/weaver-as-knowledge-system.md)
and [Whetstone think tags and metacognition](../../wiki/projects/whetstone/think-tags-and-metacognition.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Semantic Notetaking Systems](../artifacts/chatgpt/6985b8d3-8a14-839c-aa84-7f617c78ad3e.md) | dual-link | P1 | Knowledge system and semantic memory workflow. |
| [next](../artifacts/obsidian/weaver.md) | dual-link | P1 | Weaver note; route mainly to Genesis. |
| [Taste and agency in AI](../artifacts/chatgpt/689b6e60-1688-8322-95a3-6848c2ab85c5.md) | dual-link | P2 | Genesis agency/taste with Whetstone cognition angle. |

## Personal Life Operations Spillovers

These sources have cognitive labels but are better saved for the
`unassigned/personal` queue unless a later Chronicle/Whetstone pass needs them.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [prodsys](../artifacts/obsidian/prodsys.md) | defer | P2 | Personal productivity system; likely `unassigned/personal`. |
| [reminders](../artifacts/obsidian/reminders.md) | defer | P2 | Reminder/life operation note. |
| [walks](../artifacts/obsidian/walks.md) | defer | P2 | Walk practice; Chronicle/personal queue. |
| [ideas before bed](../artifacts/obsidian/ideas-before-bed.md) | dual-link | P2 | Also in contemplative queue; handle with Chronicle if needed. |
| [Disconnected self: Unease and erosion.](../artifacts/chatgpt/8dba6d1d-fd8e-4178-91ce-55de91d68f5a.md) | dual-link | P2 | Also in state-regulation queue; may fit personal narrative pass. |

## Next Pass

No further `unassigned/cognitive` synthesis pass is queued. The personal life
operations spillovers are deferred to `unassigned/personal`, where they can be
handled with the rest of the personal operations material.
