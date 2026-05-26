# pz4t — anchor-pivot-place

## Summary

Anchor-Pivot Jigsaw (拼图) is a turn-based polyomino tiling puzzle.
Each level shows ONE single connected dark-grey **target region**
on the board and a small palette of distinct coloured **component
pieces** below it. The player picks up a component by clicking a
non-transparent pixel of it — that pixel becomes the **anchor
offset** (its (col, row) within the component's rendered bounding
box). A subsequent click on any cell places the held component
such that the anchor cell lands on the clicked cell (i.e.
`sprite.position = click − anchor`). The player can transform the
held component before placing: ACTION5 rotates 90° clockwise; the
4 cardinal arrows reflect — ACTION1 / ACTION2 toggle the up-down
mirror (reflect across the horizontal axis), ACTION3 / ACTION4
toggle the left-right mirror (reflect across the vertical axis).
The level wins when the union of every component's filled cells
exactly equals the target region (no overlap between pieces, no
cell outside the target). The only failure mode is exhausting the
per-level step counter.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Toggle the held component's *vertical mirror* (`set_mirror_ud(not _mirror_ud)`); the anchor mirrors with the pixels (`new_row = height − 1 − old_row`). | Always offered. No-op if no component held. Always consumes 1 step. |
| ACTION2 | Same as ACTION1 (the up-down mirror is involutive, so UP and DOWN both toggle the same axis). | Same. |
| ACTION3 | Toggle the held component's *horizontal mirror* (`set_mirror_lr(not _mirror_lr)`); the anchor mirrors with the pixels (`new_col = width − 1 − old_col`). | Always offered. No-op if no component held. |
| ACTION4 | Same as ACTION3. | Same. |
| ACTION5 | Rotate the held component 90° clockwise; the anchor follows the rotation (`new_col = old_height − 1 − old_row`, `new_row = old_col`). | Always offered. No-op if no component held. |
| ACTION6 | Click at `(data["x"], data["y"])`. Convert via `camera.display_to_grid`. If nothing is held, look up a sprite tagged `component` at the clicked cell (PIXEL_PERFECT mode skips transparent pixels): pick it up, set `self.held_component`, record `self.anchor_offset = (gx − sprite.x, gy − sprite.y)`. If a component is held, set `held.position = (click − anchor)` and drop. | Always offered. Always consumes 1 step. |

`available_actions = [1, 2, 3, 4, 5, 6]`. The distinctive verb is
on **ACTION6** (the click pick-up-and-place pair); ACTION5 and
ACTION1-4 are component-transformation extensions introduced at
L2 and L3.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | anchor-pivot place (base, N=1) | 10×10 grid; single connected target region (5-cell L-pentomino at (3,2),(4,2),(5,2),(3,3),(3,4)); 2 components (red 3-bar at (1,8); yellow 1×2 vertical bar at (6,7)) totalling 5 cells. Step budget 16. Witness `[click(1,8), click(3,2), click(6,7), click(3,3)]` (4 actions). |
| 2 | + rotation (N+1=2) | 12×12 grid; single connected U-shape target (7 cells: (3,3),(5,3),(3,4),(5,4),(3,5),(4,5),(5,5)); 3 components (red 3-bar, yellow 1×2 vertical, green 2-bar horizontal) totalling 7 cells. Green is initially horizontal but the only remaining slot for it is a vertical pair — ACTION5 rotation strictly required. Step budget 28. Witness `[click(1,9), click(3,5), click(5,9), click(3,3), click(8,10), ACTION5, click(5,3)]` (7 actions). |
| 3 | + reflection (N+2=3) | 14×14 grid; single connected target region of 12 cells covering an S-tetromino sub-region plus a magenta-bar row + green vertical-bar column + yellow L. 4 components (red Z-tetromino, yellow L, green 2-bar, magenta 3-bar). Z must be flipped (ACTION3 or ACTION4 toggling mirror_lr) to become S-shape — strictly required because Z has 180° rotation symmetry, so all 4 rotations of Z give only Z-shape (never S). Green still requires rotation. Step budget 40. Witness 10 actions: `[click(1,11), ACTION3, click(5,3), click(5,11), click(5,4), click(9,11), ACTION5, click(3,5), click(1,13), click(4,2)]`. Adjacent-action commute test: swapping ACTION3 (flip) with the place-click after picking Z breaks the solution because flipping has no effect with nothing held. |

## Win condition

After every commit-place (ACTION6 in held phase): collect the union
of all component sprites' currently-occupied cells (their
post-rotation, post-mirror filled pixels at their current
positions). If two components' cells overlap → not won (overlap
rejection). Otherwise compare the union to the set of cells
holding `target` shadow sprites; equality ⇒ `self.next_level()`.
The engine fires `self.win()` after L3 advances.

## Lose condition

`self.steps_left <= 0` ⇒ `self.lose()`. The step counter
decrements once per `step()` call regardless of action result;
mis-placements are recoverable (a placed component can be picked
back up by clicking it again).

## Internal state

- `self.held_component: Optional[Sprite]` — currently picked-up
  component (None when nothing held).
- `self.anchor_offset: tuple[int, int]` — (col, row) of the
  anchor relative to the held component's rendered bounding-box
  top-left.
- `self.steps_left: int` — remaining step budget; mirrored to
  the `StepCounterHud`.
- `self.step_budget: int` — pulled from `level.get_data("StepBudget")`.

The held component's `rotation`, `_mirror_lr`, and `_mirror_ud`
flags also encode state, mutated by ACTION5 / ACTION1-4.

## Notable code patterns

- **Two-phase click via single ACTION6.** The branch on
  `self.held_component is None` distinguishes pick-up phase from
  place phase; no separate held-phase / unheld-phase action slots
  needed.
- **Anchor offset transform on every transformation.** Each
  transformation handler pre-reads the current rendered W or H,
  applies the engine call (`rotate`, `set_mirror_ud`,
  `set_mirror_lr`), then computes the new anchor offset so the
  click-pixel-on-component invariant holds across the transform.
- **Single shared anchor-marker sprite per level.** A single
  `anchor_marker` (palette-1, 1×1, layer 4) is placed in every
  level at REMOVED interaction. Pick-up repositions it to the
  anchor cell and switches to INTANGIBLE; place reverts it to
  REMOVED.
- **Single connected target as a multi-cell shadow group.** Each
  target cell is realised as a 1×1 `target_shadow` sprite (palette
  3 mid-grey, layer 0). The level constructor uses a small
  `_shadows(cells)` helper to clone+position one shadow per cell.
- **Win check as set equality plus overlap rejection.** Each
  component's rendered (post-rotation, post-mirror) non-transparent
  cells are accumulated into a union; if a component's cells
  overlap any cell already in the union, the predicate is False.
  Final test: union equals the set of `target` sprite cells.
- **Pixel-perfect click filtering.** Sprites default to
  `BlockingMode.PIXEL_PERFECT`, so `level.get_sprite_at(gx, gy,
  tag="component")` skips clicks on transparent pixels of the
  component's bounding box — picking up requires hitting a
  filled pixel of the component.
