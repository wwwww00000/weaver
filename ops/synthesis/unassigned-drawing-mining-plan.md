# Unassigned Drawing Mining Plan

Date: 2026-06-28

This is the routing layer for `unassigned/drawing` source artifacts. It is not
final wiki prose. Use it to decide which existing page, new page, or defer
bucket should consume each source.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Method

Treat `unassigned/drawing` as Conjuration practice material, not as a generic
art-history or tool-collection dump. The durable axis is: how does the source
help turn imagination, observation, perspective, and hand practice into visible
marks with feedback?

Destinations:

- `conjuration`: drawing as imagination-building, visual practice, and creative
  output.
- `constructive drawing`: line quality, form construction, perspective,
  reference study, subject tracks, session design, and feedback loops.
- `visualization`: mental imagery, first-person visual field practice,
  perspective intuition, and image-to-page translation.
- `studio stack`: materials, software, courses, reference sources, painting
  experiments, and tool ideas that support practice without becoming the main
  practice.

Actions:

- `merge`: read during the next pass for the destination page.
- `dual-link`: split between visualization and constructive drawing.
- `new-page`: create a candidate page before synthesis.
- `defer`: leave out of the next pass unless a later page needs it.
- `skip`: low-signal, duplicate, empty, or already mined into an existing page.

Priority means:

- `P1`: useful for the next page-deepening pass.
- `P2`: potentially useful, but not worth blocking the next pass.
- `P3`: likely skip or archive-only.

## Queue Order

| Queue | Count | First pass |
| --- | ---: | --- |
| Practice Architecture And Tracking | 8 | Deepen Constructive Drawing Practice with session design, error isolation, line quality, subject tracks, and feedback. |
| Perspective And Visualization Bridge | 7 | Deepen Visualization and Constructive Drawing around first-person perspective, image translation, and 3D feedback. |
| Studio Stack, Resources, And Projects | 7 | Create a small Conjuration child page for tools, courses, references, supplies, painting, and software ideas. |
| Already Mined Or Reference Tail | 1 | Keep museum notes as source-map/reference material unless later art queue needs it. |

## Status

- 2026-06-28: Created initial routing plan for `unassigned/drawing`.
- 2026-06-28: Completed the practice architecture and tracking pass by
  deepening
  [Constructive Drawing Practice](../../wiki/projects/conjuration/constructive-drawing-practice.md).
- 2026-06-28: Completed the perspective and visualization bridge pass by
  deepening
  [Visualization And Imagination Training](../../wiki/projects/conjuration/visualization-and-imagination-training.md).

## Practice Architecture And Tracking

Primary destination:
[Constructive Drawing Practice](../../wiki/projects/conjuration/constructive-drawing-practice.md).

Secondary destination:
[Conjuration](../../wiki/projects/conjuration.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Structured Perspective Drawing Practice](../artifacts/chatgpt/f69edf75-69a6-411a-860f-c1b113c91f57.md) | merge | P1 | Session shape, planning, review, tracking. |
| [Ideas for Inktober construction prompts](../artifacts/chatgpt/85260439-d95d-4667-968f-8e270a1939b9.md) | merge | P1 | Prompt-to-subject conversion with construction focus. |
| [drawabox](../artifacts/obsidian/drawing-drawabox.md) | merge | P1 | Construction, ghosting, animal simplification. |
| [line quality](../artifacts/obsidian/drawing-line-quality.md) | merge | P1 | Previsualize, ghost, elbow motion. |
| [figure and gesture drawing](../artifacts/obsidian/drawing-figure-and-gesture-drawing.md) | merge | P1 | Gesture as information compression. |
| [portrait](../artifacts/obsidian/drawing-portrait.md) | merge | P1 | Block-in order, measuring, cranium/cheek structure. |
| [reference study](../artifacts/obsidian/drawing-reference-study.md) | merge | P1 | Understand form instead of copying; checkpoint overlays. |
| [sketchbook](../artifacts/obsidian/drawing-sketchbook.md) | merge | P2 | Casual volume, subjects, medium choice. |

Status: complete. The pass added practice tracking, checkpointed error
isolation, line-quality rules, prompt translation, and sharper subject-track
guidance for portraits, animals, gesture, and Inktober-style prompts.

## Perspective And Visualization Bridge

Primary destination:
[Visualization And Imagination Training](../../wiki/projects/conjuration/visualization-and-imagination-training.md).

Secondary destination:
[Constructive Drawing Practice](../../wiki/projects/conjuration/constructive-drawing-practice.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [observation and visualization](../artifacts/obsidian/drawing-observation-and-visualization.md) | dual-link | P1 | First-person perspective, visual field mapping, feedback. |
| [intuitive perspective](../artifacts/obsidian/drawing-perspective.md) | dual-link | P1 | Existing scene/grid as perspective scaffold. |
| [Find Perspective Drawing References](../artifacts/chatgpt/2567beed-ea30-4773-b569-c522a7106c4c.md) | merge | P2 | Reference source strategy; mostly support material. |
| [Visualization and Perspective Exercises](../artifacts/chatgpt/67a0f79f-4ec8-8009-9b6d-e71fcf77298a.md) | merge | P1 | Embodied perspective, memory-to-sketch, scene construction. |
| [Visualization Skill Development](../artifacts/chatgpt/b069844b-4fb6-406c-86a3-b551c247e776.md) | merge | P2 | Visualization exercise menu; partly already mined. |
| [Modes of Mental Visualization](../artifacts/chatgpt/a00ee50c-d8cd-426c-b746-0d71f2a840e1.md) | merge | P2 | Visualization mode taxonomy; already source-mapped. |
| [3d sketching](../artifacts/obsidian/drawing-3d-sketching.md) | dual-link | P2 | 3D sketching tools as feedback and spatial practice. |

Status: complete. The pass added embodied first-person perspective drills,
reference and 3D feedback loops, and a clearer predict-first/reveal-second
protocol for image-to-page translation.

## Studio Stack, Resources, And Projects

Primary destination:
new Conjuration child page candidate
`wiki/projects/conjuration/drawing-studio-stack-and-projects.md`.

Secondary destination:
[Conjuration](../../wiki/projects/conjuration.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [courses](../artifacts/obsidian/drawing-courses.md) | merge | P2 | Course/resource backlog. |
| [resources](../artifacts/obsidian/drawing-resources.md) | merge | P2 | External art references. |
| [software](../artifacts/obsidian/drawing-software.md) | merge | P1 | Tool ideas including ellipse trainer and canvas rotation. |
| [supplies](../artifacts/obsidian/drawing-supplies.md) | merge | P2 | Materials list; keep lightweight. |
| [design](../artifacts/obsidian/drawing-design.md) | merge | P2 | Shape carving, settei, mechtober, fantasy design references. |
| [projects](../artifacts/obsidian/drawing-painting.md) | merge | P2 | Painting, color, medium experiments, customization projects. |
| [inspiration prompt](../artifacts/obsidian/drawing-inktober.md) | merge | P2 | Inktober/trip/plane-window prompt; construction challenge source. |

## Already Mined Or Reference Tail

Primary destination:
source-map/reference only unless the later `unassigned/art` pass needs exact
details.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [museum notes](../artifacts/obsidian/drawing-ideas.md) | skip | P3 | Already mined into Constructive Drawing Practice; may reappear in art queue. |

## Next Pass

The practice architecture/tracking and perspective/visualization bridge passes
are complete. Next, move to the drawing studio stack, resources, and projects.
