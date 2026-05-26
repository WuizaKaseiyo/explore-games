# SUPERSEDED — see `marble-drop-switchyard.md`

> This file is retained for traceability but the mechanic is being
> dropped from the unimplemented pool. See `REVISIONS.md` for rationale
> (Conway's Life on a 7×7 grid is visually a blocky binary CA — same
> register as heat/fuse/sandpile/sandbar — and "match a target pattern
> after N ticks" has poor solvability).

---

# (former) Life-Tick-Evolve

## Summary

The grid is a small **2-state cellular automaton** under Conway's
Life rule. Every cell is either *alive* (filled) or *dead* (empty).
The player clicks cells to toggle them, then presses ACTION5 to
advance the simulation by **one tick**. After a tick, every cell's
new state is determined by the standard rule: a dead cell with
exactly 3 live neighbours becomes alive; a live cell with 2 or 3
live neighbours stays alive; otherwise the cell dies. Neighbours
are the 8 cells in the king-move (Chebyshev-distance-1) ring.

Each level shows a fixed **target pattern** of live cells in a
small region of the grid. The level wins when the live cells in
that region exactly equal the target pattern at the END of any
tick (after ACTION5 fires). The only failure mode is exhausting
the per-level step counter.

## Visual elements

- 7×7 active region (smaller than most other generated games to
  keep the search space tractable).
- A live cell renders as a solid 1×1 dark-blue cell; a dead cell
  renders as the pale-grey background.
- The target pattern hovers in a 1-pixel-thick **target frame** at
  the right side of the grid: a 3×3 or 4×4 sub-region rendered
  in dark-purple solid cells (live) and grey (dead).
- A small **tick counter** sits along the bottom rim — small dark
  notches accumulate one per ACTION5 press, capped by the level
  budget.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Advance the simulation by one Conway-Life tick. The active region recomputes. | always |
| ACTION6 | Click cell `(x, y)` to toggle its alive/dead state. Clicks outside the active region are no-ops (no step consumed). | always |

`available_actions = [5, 6]`. No avatar.

## Mechanics enumeration

- **M1 — toggle-cell:** ACTION6 click toggles a cell's state inside
  the active region.
- **M2 — life-tick:** ACTION5 applies Conway's Life rule once to
  every cell in the active region simultaneously. Cells outside
  the active region are treated as permanently dead (the boundary
  is a hard "dead" border).
- **M3 — match-target-region:** the win predicate compares the
  live/dead state of every cell in a fixed *target sub-region*
  (e.g. cells in the 3×3 box at the centre) against the target
  pattern.
- **M4 — frozen-cell (level 2+):** specific cells are tagged
  `frozen` and IGNORE the Life rule — their state is fixed for
  the whole level. The player cannot toggle them; they are dead
  or alive permanently. Visualised with a small 1-pixel border.
- **M5 — multi-tick window (level 3+):** the win check runs at
  every tick, not only the most recent — but the target may
  require an OSCILLATING pattern (different at tick T and T+1)
  to be hit at the **right tick parity**. The level data
  declares which tick parity is the winning one.

## Per-level progression

### Level 1 — base system (M1 + M2 + M3)
- 7×7 active region. Target is a specific 5-cell still life (e.g., a boat or a tub) located at a specific coordinate. 
- **Witness:** 15 actions. The player must place a multi-cell seed pattern (at least 6 cells) that reliably evolves into the target still life after exactly 3 ticks.
- **Mechanics required:** M1 (toggle), M2 (tick), M3 (match).

### Level 2 — + M4 (frozen cell)
- 10×10 active region. 3 frozen-live cells scattered in the region. Target is a glider or complex oscillator.
- **Witness:** 35 actions. The player must design a seed pattern that interacts with the frozen cells. The frozen cells act as permanent catalysts, altering the standard Game of Life evolution. The player must bounce their pattern off the frozen cells to reach the target configuration.
- **Mechanics required:** M1, M2, M3, M4.

### Level 3 — + M5 (tick-parity)
- 12×12 active region with multiple frozen cells creating a complex boundary. Target is a large 2-period oscillator that must be in phase-A on EVEN ticks.
- **Witness:** 60+ actions. The player must build a multi-stage reaction (e.g., a glider that hits a block to form a blinker) that perfectly phases with the required tick-parity. Placing the initial seed 1 cell over or advancing 1 extra tick breaks the parity alignment.
- **Mechanics required:** M1, M2, M3, M4, M5.

## Win condition
After every ACTION5, compare the live/dead state of every cell in the level's *target region* against the level's target pattern. For L3, also check that the current tick parity matches the level's required parity. If equal, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` triggers `self.lose()`. There is no per-cell death penalty; players may toggle and tick freely until the budget runs out.

## Internal state
- `self.alive: np.ndarray[bool]` — boolean grid of the active region.
- `self.frozen_alive: set[(int, int)]` — cells whose alive=True is immutable (level 2+).
- `self.frozen_dead: set[(int, int)]` — cells whose alive=False is immutable.
- `self.tick: int` — number of ACTION5 ticks since level start.
- `self.target_region: tuple[int, int, int, int]` — bounding box inside which the comparison runs.
- `self.target_pattern: np.ndarray[bool]` — required state, one per phase for L3.
- `self.target_parity: int | None` — required tick parity (L3).
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `dc22 — colour-cycle-walk`**: Life evolves the WHOLE grid by a global rule each tick.
- **vs `gv47 — seed-grow-surround-dissolve`**: Life applies a deterministic local rule; the player only seeds the initial state and chooses when to advance.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
A random clicker toggles random cells; the chance of any random configuration evolving into the exact target pattern is vanishingly small. Solving requires deliberate, highly structured seeding.

## Planning depth
- **L1:** moderate — player must know or discover how simple seeds evolve over multiple ticks.
- **L2:** deep — player must reason about how the frozen-live cell shifts the Life rule's neighbour count for adjacent cells, effectively creating a new CA rule locally.
- **L3:** very deep — precise phase alignment required. The player must orchestrate a complex reaction chain where the timing of the intermediate structures matches the global tick parity.
