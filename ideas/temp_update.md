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
