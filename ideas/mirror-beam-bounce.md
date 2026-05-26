# Mirror-Beam-Bounce

## Summary

A fixed **emitter sprite** at one edge of the grid sends a single
straight **beam** of one fixed colour into the grid in a fixed
direction (one of 4 cardinals). The beam travels cell-by-cell;
any cell it enters that is empty floor (or has a non-mirror
target sprite) is *transit*. When the beam enters a **diagonal
mirror cell**, the beam reflects 90° (the mirror's orientation
chooses left- or right-90°). When the beam enters a wall or the
grid edge, it stops. The beam recomputes from scratch after
every action — so the live geometry is always reflected.

The player verb: ACTION6 click on a mirror to **rotate it** 90°
(the mirror has 2 orientations, NW-SE and NE-SW). Rotating
re-routes the beam.

Each level has one or more **target sprites** (1×1 hollow rings
of a specific colour). A target is satisfied when the beam
passes through the target's cell. The level wins when every
target is satisfied AT THE END of the most recent action. The
only failure mode is exhausting the per-level step counter.

## Visual elements

- 12×12 grid; pale-grey floor.
- The **emitter** is a 2-cell rectangular sprite at one edge,
  orienting toward the grid; its inner pixel is bright (beam
  colour).
- The **beam** is a 1-pixel-wide line drawn in the emitter's
  colour, traced through every transit cell.
- **Diagonal mirror** cells are 1×1 with a 1-pixel light-grey
  diagonal stripe — `/` for NE-SW, `\` for NW-SE. The stripe
  rotation visualises the mirror's current orientation.
- **Walls** are solid black 1×1.
- **Target rings** are hollow 1-pixel rings of the colour the
  target requires. (Some levels have multi-colour targets; see
  M5.)

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click on a mirror cell to rotate it 90° (toggle between `/` and `\`). Clicks on non-mirror cells are no-ops. | always |

`available_actions = [6]`.

## Mechanics enumeration

- **M1 — beam-trace:** after every action, re-trace the beam:
  start at emitter cell with the emitter's direction; step
  cell-by-cell. On each cell, check: if wall/edge, stop; if
  mirror, reflect direction (the mirror's orientation deflects
  the beam — `/` reflects E→N or N→E or W→S or S→W; `\` reflects
  E→S or S→E or W→N or N→W); else continue. Record every cell
  the beam visits.
- **M2 — mirror-rotate:** ACTION6 click toggles a mirror
  between its two orientations.
- **M3 — target-hit:** a target is satisfied iff the beam
  enters the target's cell at some point during the current
  trace.
- **M4 — colour-filter cell (level 2+):** specific cells (1-cell
  filter sprites) tint the beam's colour as it passes through:
  e.g. the beam's colour becomes `mix(beam.colour,
  filter.colour)` for the rest of the trace until the beam
  hits another filter or stops. Filter cells are non-rotatable
  and act as transit (beam continues straight through).
- **M5 — colour-target match:** the target is satisfied iff the
  beam passes through with a colour matching the target's
  required colour. (Without filters, the beam stays at
  emitter's colour, so this matches only same-colour targets;
  filters allow changing the colour mid-path.)
- **M6 — beam-splitter cell (level 3+):** specific clickable
  diagonal-cross cells SPLIT the beam — when the beam enters,
  it both *transmits* straight through AND *reflects* 90° (one
  direction per orientation). The beam now has two
  simultaneous arms. Each arm continues until it hits walls or
  splitters. Click on a splitter to rotate it (4 orientations:
  which side reflects).

## Per-level progression

### Level 1 — base system (M1 + M2 + M3)
- 8×8 region; emitter emits orange beam. 4 mirrors. Target.
- **Witness:** 15 actions. The player must rotate the mirrors to bounce the beam around walls to reach the target.
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (filter) + M5 (colour-match)
- 10×10 region; multiple mirrors and filters. Multiple targets of different colours.
- **Witness:** 35 actions. The player must sequence the beam through specific filters before hitting specific targets. Rotating one mirror affects the entire downstream path, so the player must work backwards from the targets to determine the correct mirror orientations.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (beam-splitter) + composition
- 12×12 region; multiple filters, splitters, mirrors, and targets.
- **Witness:** 60+ actions. The splitters divide the beam into multiple arms, each of which must be routed through different filters to hit different targets simultaneously. The player must solve a complex optical circuit where changing one mirror might fix one arm but break another. 
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition
After every ACTION6 that resolves to a rotation, recompute the beam (and all its splits) and walk every target sprite. For each, check that the beam passes through its cell with the right colour. If every target is satisfied, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`. Misclicks consume no step.

## Internal state
- `self.emitters: list[(int, int, int, int)]` — pos, direction, colour.
- `self.mirrors: dict[(int, int), str]` — pos → orientation (`'/'` or `'\\'`).
- `self.filters: dict[(int, int), int]` — pos → filter colour.
- `self.splitters: dict[(int, int), int]` — pos → splitter orientation (level 3+).
- `self.walls: set[(int, int)]`.
- `self.targets: list[(Sprite, int, int, int)]` — sprite, pos, required colour.
- `self.beam_cells: set[(int, int, int)]` — cells visited by beam, with colour at visit (recomputed each step).
- `self.mix_table: dict[(int, int), int]`.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `lq5x — lantern-cone-illuminate`**: mirror-beam is a 1-pixel-wide BEAM from a fixed emitter that bounces off rotatable mirrors and is filtered/split by static cells.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random mirror rotations produce random beam paths; for L3 with multiple targets requiring exact colour matching via filters and splitters, the chance of random rotations satisfying all targets simultaneously is extremely small.

## Planning depth
- **L1:** moderate — trace the beam mentally to find the right angles.
- **L2:** deep — colour changes at filters dictate the order of target-hits.
- **L3:** very deep — splitter cells create multiple interdependent arms. Commuting two adjacent rotations changes which arm reaches which filter, and thus which colour reaches which target. The player must solve the entire circuit globally.
