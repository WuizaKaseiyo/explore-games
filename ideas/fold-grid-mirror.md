# Fold-Grid-Mirror

## Summary

The playfield is treated as a sheet of paper. Four **fold buttons**
sit at the centre of each rim (top, bottom, left, right). Clicking
a fold button **commits a fold** of the corresponding half onto the
opposite half across the central axis perpendicular to that rim:

- **Top button** — fold the TOP half DOWN across a horizontal axis
  at row `floor(active_height / 2)`. The top half is then empty.
- **Bottom button** — fold the BOTTOM half UP across the same
  horizontal axis.
- **Left button** — fold the LEFT half RIGHT across a vertical
  axis at column `floor(active_width / 2)`.
- **Right button** — fold the RIGHT half LEFT across the same
  vertical axis.

Every non-anchored sprite on the active half is reflected across
the axis and overlaid onto the corresponding cell on the opposite
half. Sprites that land on the same cell **merge** by a
level-defined mix table (e.g. `red + blue = purple`); same-colour
sprites stack into one cell of that colour; pairs not in the mix
table **cancel** (both disappear). After commit, the active half
is empty AND the active region for subsequent folds shrinks to
the still-populated half (so the next fold halves whatever is
left).

Some sprites are **anchored** — they refuse to fold and stay in
place. Anchored cells also block any folded sprite from landing
on them: a sprite that would land on an anchored cell is cancelled.

The level wins when every **target cell** holds a sprite of the
target's colour after folds settle; the only failure mode is
exhausting the per-level step counter.

## Visual elements (distinct from prior corpus)

- Inner grid: 11×11 paper.
- Four **fold buttons**, one centred on each rim: a 2×2 grey
  square with a 1-pixel coloured arrow-stub indicating the fold
  direction. A button is **disabled** (rendered dimmed) if the
  current active region's fold along its axis would be a no-op
  (e.g. the active region is already only one half on that axis).
- The **active region** is highlighted by a 1-pixel border drawn
  on the four sides of the currently-live half. The border
  shrinks visibly after each fold.
- Pieces are flat coloured 2×2 blocks; targets are hollow rings
  of the required colour.
- Anchored sprites carry a 1-pixel **dark-grey pin** in their
  corner to mark immobility under folds.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click on a fold button. The fold of the corresponding half is committed across the central axis perpendicular to that rim within the current active region. Clicks on disabled buttons or off-button cells are no-ops (no step consumed). | always |

`available_actions = [6]`. No avatar, no arrow keys.

## Mechanics enumeration

- **M1 — pick-fold-direction:** the four fold buttons each
  commit a fold of one half (top / bottom / left / right) of
  the current active region across the perpendicular central
  axis.
- **M2 — commit-fold:** ACTION6 click on a fold button reflects
  every non-anchored sprite on the active half across the axis
  onto the opposite half, cell-by-cell. Reflected sprites land
  at `axis - (source - axis)` (for the perpendicular direction
  of the fold). After the fold, the active region shrinks to
  exclude the half that was folded; subsequent folds operate on
  the smaller region.
- **M3 — colour-mix-on-overlay:** when two sprites land on the same
  cell, their colours blend via the level's mix table (e.g.
  `red + blue → purple`); two same-colour sprites stack into one of
  that colour; an unlisted pair *cancels* (both sprites disappear).
- **M4 — anchored-sprite:** sprites tagged `anchor` are immune to the
  fold — they stay where they are. They still BLOCK overlay (a folded
  sprite cannot land on an anchored cell; if it would, it cancels).
- **M5 — multi-fold-composition:** after a fold, the active region
  is HALF of the original; subsequent folds can fold this half again.
  At least two folds are required when the goal cell is not directly
  reachable in one fold.

## Per-level progression

### Level 1 — base system (M1 + M2)
- Active region: full 11×11. Single colour (orange). Multiple orange blocks. Multiple targets.
- **Witness:** 15 actions. The player must fold the grid sequentially to overlap all the orange blocks onto the target cells. 
- **Mechanics required:** M1, M2.

### Level 2 — + M3 (colour mix)
- Active region: full 11×11. Mix table shown as a 3-cell strip near the bottom rim: `red + blue = purple`. Red block, blue block, purple ring targets.
- **Witness:** 35 actions. The player must align the specific coloured blocks to merge them before delivering them to the targets. Since folding shrinks the grid, the player must sequence folds so that blocks combine correctly without accidentally cancelling out un-mixed blocks.
- **Mechanics required:** M1, M2, M3.

### Level 3 — + M4 (anchor) + M5 (multi-fold composition)
- Active region: 15×15. Multiple anchors, complex mix table.
- **Witness:** 60+ actions. Anchors are immune to folds and act as blockers. The player must navigate around the anchors by folding other sections of the grid first. Since each fold commits and shrinks the active region, a single wrong fold will strand blocks on the wrong side of an anchor or cancel them out. The sequence of 10+ folds must be perfectly calculated.
- **Mechanics required:** M1, M2, M3, M4, M5.

## Win condition
After every commit, walk every target sprite. If every target's cell contains a sprite whose pixel colour equals the target's ring colour, fire `self.next_level()`. After level 3, the engine auto-fires `self.win()`.

## Lose condition
`steps_used >= max_steps` triggers `self.lose()`. Misclicks consume no step.

## Internal state
- `self.fold_buttons: dict[str, Sprite]` — keys `"top"|"bottom"|"left"|"right"`; each sprite carries `pos` and `enabled: bool`.
- `self.active_region: (x0, y0, x1, y1)` — bounding box of the currently-live half.
- `self.mix_table: dict[frozenset[int], int]` — colour pair → output colour. Pairs not in the table cancel.
- `self.targets: list[Sprite]` — target rings (static across the level).
- `self.anchors: set[(int, int)]` — cells whose sprites resist folds.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `ar25 — shape-mirror-cover`**: Here the fold is a one-shot transform of the entire grid half — sprites do not move 1-cell-at-a-time, the playfield itself folds.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random folds will rapidly shrink the grid to 1x1, likely cancelling most blocks. The chance of randomly sequencing the folds to produce the exact target arrangement is infinitesimally small.

## Planning depth
- **L1:** moderate — visualise the reflection of multiple blocks simultaneously.
- **L2:** deep — plan the sequence of merges while avoiding accidental cancellations.
- **L3:** very deep — anchors severely restrict the folding order. The player must solve the grid's topology by determining which regions must be folded first to bypass the anchors.
