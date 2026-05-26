# Droplet-Trace-Blend

## Summary

The player walks a single 1-cell **droplet sprite** around the
grid with arrow keys. Behind the droplet, every cell it leaves
is **painted** with the droplet's current colour — a persistent
trail. The droplet starts each level with a level-specific
**source colour**. When the droplet enters a **mixer cell**
(fixed at level start, carrying its own colour), the droplet's
colour is **replaced** by the level's `mix(droplet.colour,
mixer.colour)` table lookup (e.g. `red + blue = purple`). The
mixer cell is consumed (becomes a blank floor cell) after one
use.

Each level shows **target cells** with required colours. The
level wins when every target cell's current paint colour matches
its required colour AT THE END of the most recent action. The
only failure mode is exhausting the per-level step counter.

## Visual elements

- 14×14 grid; pale-grey unpainted floor.
- The **droplet** is a 1×1 cell in its current colour with a
  1-pixel white outline (visual highlight).
- A **painted cell** is the trail colour at the time the
  droplet left it; trails stay painted until a future re-paint
  by the droplet on a return visit.
- A **mixer cell** is a 1×1 cell with a 1-pixel dark-grey
  diagonal slash; the cell's body is filled with the mixer's
  colour. After consumption, it becomes pale-grey floor.
- A **target cell** is a 1×1 hollow ring in the required colour.
- A **wall** is a solid black 1×1 cell.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION1 | Move droplet 1 cell up. The cell the droplet leaves is painted the droplet's pre-move colour. If the destination cell has a mixer, the droplet's colour updates to `mix(droplet, mixer)` AFTER the destination paints (so the destination is painted with the new mixed colour). | always; out-of-bounds is no-op (consumes 1 step). |
| ACTION2 | Down. | always |
| ACTION3 | Left. | always |
| ACTION4 | Right. | always |

`available_actions = [1, 2, 3, 4]`. No clicks; no special verbs.

## Mechanics enumeration

- **M1 — droplet-walk-paint:** ACTION1-4 moves droplet 1 cell;
  the cell the droplet OCCUPIED before the move is painted
  with the droplet's pre-move colour. The cell the droplet
  enters (after the move) is painted with the droplet's
  post-move colour (which may differ if a mixer was hit).
- **M2 — mixer-blend:** stepping onto a mixer cell replaces
  the droplet's colour via the level's `mix_table`
  `dict[(int, int), int]`. The mixer cell is consumed (removed
  from the grid).
- **M3 — wall-block:** the droplet cannot enter a wall; if the
  move would, it's cancelled (no step consumed; no paint
  applied).
- **M4 — match-target-paints:** the win predicate compares
  every target cell's current paint colour to its required
  colour.
- **M5 — re-paint-overwrite (level 2+):** if the droplet
  walks back over a previously-painted cell, the cell's paint
  is OVERWRITTEN with the droplet's current colour. This means
  re-visits can correct earlier mistakes, but the mixer is
  already consumed, so the droplet may not have the original
  colour available.
- **M6 — locked-paint cell (level 3+):** specific cells, once
  painted, are tagged `locked` and refuse subsequent
  re-painting. Visualised by a 1-pixel dark-grey corner notch
  on the cell. The first paint colour applied is final.

## Per-level progression

### Level 1 — base system (M1 + M3 + M4)
- 10×10 region. Droplet starts orange. Target consists of 8 target rings (4 orange, 4 blue). One blue mixer.
- **Witness:** ~18 moves. The droplet must walk to the 4 orange targets first, then navigate into the blue mixer (consuming it and turning blue), then walk to the 4 blue targets. If the player hits the mixer too early, they lose the orange color permanently.
- **Mechanics required:** M1, M2, M3, M4.

### Level 2 — + M2 (mixer) + M5 (overwrite)
- 12×12 region. Maze of walls. Droplet starts orange. Two mixers (blue, yellow). Target requires purple (orange+blue) and green (blue+yellow). 
- **Witness:** ~35 moves. The corridor to the blue targets is blocked by the yellow mixer. The player must paint the purple targets, walk OVER their own painted trail to reach the yellow mixer (overwriting the trail temporarily), then navigate back to fix the trail before hitting the green targets. 
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (locked paint) + complex routing
- 14×14 region. Four mixers. Multiple targets including *locked* cells (which can only be painted once). 
- **Witness:** ~60 moves. The locked cells are positioned in narrow bottlenecks. The player must secure the correct droplet colour *before* passing through the bottleneck, because walking through it with the wrong colour will permanently lock it to the incorrect colour. This requires a highly non-trivial traversal order of the mixers.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition
After every move, walk every target cell. For each, check `paint[target.pos] == target.required_colour`. If all match, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`.

## Internal state
- `self.droplet_pos: (int, int)`.
- `self.droplet_colour: int`.
- `self.paint: dict[(int, int), int]` — current paint colour per cell.
- `self.mixers: dict[(int, int), int]` — cell → mixer colour (consumed entries are removed).
- `self.mix_table: dict[(int, int), int]` — pair → mixed colour.
- `self.walls: set[(int, int)]`.
- `self.locked_cells: set[(int, int)]` — cells whose first paint is final (level 3+).
- `self.targets: list[(Sprite, int, int, int)]` — sprite, pos, required colour.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `pj7k — rolling-cube-face-paint`**: Droplet-trace's colour changes are *triggered by mixer cells* embedded in the environment, not by intrinsic geometric permutation.
- **vs `gv47 — seed-grow-surround-dissolve`**: Droplet-trace paints linearly along the droplet's path, rather than area-filling.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random walking will quickly exhaust the mixers in the wrong order or permanently corrupt locked cells.

## Planning depth
- **L1:** moderate — player must separate targets into "before mixer" and "after mixer" phases.
- **L2:** deep — player must intentionally overwrite their own trails to navigate the maze, requiring backtracking and re-painting.
- **L3:** very deep — locked bottlenecks force a strict global ordering on mixer visits. The player must plan the entire colour-sequence from start to finish.
