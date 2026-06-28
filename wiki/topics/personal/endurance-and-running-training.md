---
title: Endurance And Running Training
status: draft
page_type: method
projects: []
categories:
  - personal
  - endurance
  - running
  - training
  - fitness
source_bundles:
  - unassigned/personal
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
parent: topics/personal
related:
  - projects/whetstone/problem-solving-and-skill-acquisition
  - projects/chronicle/morning-pages-and-life-os
created: 2026-06-28
updated: 2026-06-28
---

# Endurance And Running Training

The running notes point toward a simple goal: build aerobic capacity without a
race-specific plan. The useful frame is not to maximize pace on every run. It
is to accumulate recoverable aerobic work, learn personal intensity signals, and
track whether the same effort gradually produces better movement.

This page is a personal-practice note, not a medical or coaching plan. It should
be revised against actual training data and recovery.

## Training Stance

For a non-race aerobic base block, two runs per week can still be useful if the
sessions are consistent and recoverable:

- one weekday steady easy run around 45 to 60 minutes;
- one longer weekend easy run around 75 to 120 minutes, built gradually;
- optional relaxed strides after an easy run when the body feels fresh.

The main variable is time at a genuinely easy aerobic effort. Pace is allowed to
be slower than a watch prescription if the prescription produces a
non-conversational effort.

## Zone 2 As A Target

Z2 is best understood as a proxy for work near or below the first aerobic
threshold, not as a universal watch label. The practical target is:

- conversational breathing;
- RPE around 2 to 4 out of 10;
- relaxed enough that the run does not compromise the next day;
- mostly below the point where breathing noticeably changes.

Different systems label zones differently. A watch's "base" pace or Z3 label
may not match the endurance-community use of easy Z2. When the watch and the
body disagree, use talk test and RPE to sanity-check the watch.

## Heart Rate, RPE, And Pace

Heart rate is useful, but it is a lagging and drift-prone signal.

Use it differently by workout:

- easy and long runs: HR can be a cap, with RPE as a sanity check;
- tempo blocks: use RPE plus a sustainable pace range, then use HR as a ceiling
  after the first few minutes;
- short intervals: use pace, time, or RPE, because HR does not respond fast
  enough to control the rep.

Large disconnects between pace/RPE and HR can be normal during intervals:
heart rate rises slowly during fast segments and decays slowly during recovery.
They can also come from wrist optical sensor error, smoothing, or cadence lock.
For HR-guided workouts, a chest strap and longer steady blocks produce cleaner
data.

## Drift And Z3 Creep

Late-run HR drift is not automatically a failed Z2 run. Heat, hydration,
glycogen use, and accumulating fatigue can raise HR at the same pace and same
felt effort.

Use a gradient rule:

- if breathing is easy and drift is modest, keep the natural easy jog;
- if HR creeps slightly into low Z3 near the end but RPE stays easy, treat it as
  a normal aerobic-durability signal;
- if breathing becomes labored, drift is large, or recovery suffers, slow down,
  walk briefly, or shorten the run.

The point is not militant zone purity. The point is to keep most easy volume
below the point where it becomes a hidden tempo workout.

## Long Run Adaptation And Recovery

Long Z2 runs matter because duration changes the metabolic stress. Early in the
run, aerobic metabolism is warming up and glycogen use is still comfortable.
Later, lower glycogen and accumulated fatigue push the body toward more fat
oxidation and mitochondrial signaling.

Useful signs near the end of a long run:

- pace becomes slightly harder to hold at the same HR;
- legs feel heavy without major breathlessness;
- RPE rises mildly while the effort remains aerobic;
- HR drifts upward at steady pace.

Recovery should be treated as part of the workout:

- eat carbohydrates plus protein after longer runs;
- rehydrate with attention to sodium in hot or humid conditions;
- sleep enough to absorb the session;
- use walking or very easy movement the next day if it improves recovery;
- avoid stacking glycogen-depletion tricks on top of high work or life stress.

## Cadence And Running Economy

Speed is cadence times stride length. Most runners naturally choose a cadence
near their economy optimum for a given pace, so cadence should not become a
number chase.

Use cadence as a form cue when needed:

- a small increase can reduce overstriding and braking;
- "quick feet" late in a run can prevent fatigue from turning into long,
  reaching strides;
- higher cadence at the same pace usually means less push per step but more
  steps;
- the goal is compact landing and smooth rearward push, not spinning tensely.

Strides are short relaxed accelerations, not all-out sprints. They can preserve
coordination and leg speed during mostly easy aerobic training.

## Efficiency Metrics

Efficiency metrics are diagnostics, not goals by themselves.

Useful signals:

- efficiency index: speed divided by HR;
- pace-per-HR: pace seconds per kilometer divided by HR;
- Pa:HR decoupling: compare pace/HR relation between the first and second half
  of a steady run;
- grade, heat, wind, surface, and sensor quality annotations.

Runalyze can expose aerobic decoupling and efficiency-style views. Garmin and
Strava may not show the exact metric natively without extra fields or exports.

When analyzing a run, smooth pace and HR over 60 to 120 seconds, ignore the
first warmup segment, and treat sudden "free speed" spikes with suspicion until
terrain, wind, GPS smoothing, and HR sensor behavior are ruled out.

## Two-Run Weekly Template

A conservative two-run pattern:

```text
Weekday: 45-60 min easy, conversational
Weekend: 75-120 min easy, gradually extended
Optional: 4-6 relaxed 20-30 s strides after one easy run
```

Progress the weekend run slowly. The success condition is not that every run is
faster. It is that the same easy effort becomes more stable, drifts less, and
recovers more cleanly.

## Open Questions

- What HR source is trustworthy enough for analysis: wrist sensor or chest
  strap?
- What personal HR/RPE/talk-test boundary best approximates aerobic threshold?
- How much low-Z3 drift is acceptable before recovery starts to degrade?
- Which metric should be tracked weekly: easy pace at fixed RPE, decoupling, or
  long-run duration?
- Does two-run consistency outperform a more ambitious plan that is less
  recoverable?

## Source Map

- [Aerobic training overview](../../../ops/artifacts/chatgpt/68f07744-7f68-8320-befb-2d8b1b5e3956.md)
- [Base pace clarification](../../../ops/artifacts/chatgpt/69330884-93e8-832f-adb3-05e3c541beda.md)
- [Cadence vs Muscular Exertion](../../../ops/artifacts/chatgpt/695a31c9-b4ac-8322-bb8a-b649179a1e65.md)
- [HR vs RPE in Running](../../../ops/artifacts/chatgpt/69514080-0344-8320-a2ad-dcc120cef015.md)
- [Running efficiency metrics](../../../ops/artifacts/chatgpt/68d9275f-42f4-8332-b355-72f08e6e51ac.md)
- [Z2 vs Z3 endurance impact](../../../ops/artifacts/chatgpt/690aa334-3f30-8322-93a8-08c9d9c9cefe.md)
- [Zone 2 run recovery](../../../ops/artifacts/chatgpt/68f11dd4-8768-8323-a59c-2678209f7197.md)
