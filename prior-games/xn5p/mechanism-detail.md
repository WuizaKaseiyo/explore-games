# xn5p — chamber-stamp-partition

## Summary

A yellow pawn walks an open chamber filled with discrete coloured "molecule" sprites (red rings, blue plus-shapes, green X-shapes). Cardinal arrow keys move the avatar one 3-cell stride per press; ACTION5 stamps a permanent wall block at the avatar's current cell (or, at level 3, toggles an existing stamp off). The level wins as soon as every connected component of the chamber's open cells (excluding both static walls and stamped walls) contains molecules of exactly one colour, with every colour represented in some component. The single per-step constraint is the step-counter HUD bar — running out of steps fires `lose()`.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move avatar 3 cells north. If destination cell holds a molecule sprite, push the molecule one stride north; if push destination is a wall, an out-of-bounds cell, or another molecule, the push fails and the avatar's move is rejected. | always |
| ACTION2 | Move avatar 3 cells south. Push semantics identical. | always |
| ACTION3 | Move avatar 3 cells west. Push semantics identical. | always |
| ACTION4 | Move avatar 3 cells east. Push semantics identical. | always |
| ACTION5 | At avatar's current cell: if no `wall_stamp` is present, place one. If a `wall_stamp` is present AND the level's `stamp_toggle` data flag is set (L3 only), remove it. Otherwise the action is consumed with no effect. | always |

`available_actions = [1, 2, 3, 4, 5]`. No click, no undo.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | base dynamic: walk + stamp + partition-win | 20×20 grid, 18×18 inner chamber, 6×6 lattice on 3-cell stride. Static walls in lattice column i=2 except at j=2 form the only channel between left half (red) and right half (blue). Avatar starts at lattice (5, 0) — top-right corner, away from the bridge so a single ACTION5 at level start does not trivially win. Witness `[ACTION2, ACTION2, ACTION3, ACTION3, ACTION3, ACTION5]` (6 actions): south twice, west three times to lattice (2, 2), stamp the channel. Any cell in the row-2 bridge (lattice i ∈ {1, 2, 3}, j = 2) wins when stamped. Step budget 30. |
| 2 | + push-molecule (sokoban-style on walk-into) | Same chamber, with static walls at lattice cols 2 and 3 j ∈ {0, 1, 3, 4, 5} leaving two row-2 channels; an obstacle red molecule at lattice (3, 2) blocks the right channel. Avatar starts at (5, 0). Witness `[ACTION2, ACTION2, ACTION3, ACTION3, ACTION5]` (5 actions): walk south twice, west twice (the second west pushes the obstacle into the empty col-2 channel), then stamp. The remaining right-channel cell (3, 2) becomes a wall by stamping; the implementation's layout closes col 3 entirely, leaving col 2's (2, 2) as the only open cell which connects red on both sides. Step budget 60. |
| 3 | + stamp-toggle (re-press ACTION5 to remove a stamp) AND a third colour (green) | Same chamber + a vertical alcove at lattice column 3 rows 3-5 (closed off by static walls on col 4 j ∈ {3, 4, 5}). Green molecule lives in the alcove at (3, 4); blue main at (5, 5); red main at (0, 0); obstacle red at (3, 2); avatar at (5, 0). Witness `[ACTION2, ACTION2, ACTION3, ACTION3, ACTION5]` (5 actions) — same shape as L2; the alcove's bounding walls plus the pushed-out obstacle red collapse the layout into three monochrome components after one stamp at (3, 2). The stamp-toggle mechanic is exposed (`stamp_toggle: True` in level data) and verified by independent custom check, but is not counterfactually required by the optimal witness. Step budget 100. |

## Win condition

After every step, build the set of "open cells" (every grid cell not covered by a sprite tagged `wall` — both `wall_static` and `wall_stamp` block; molecules and the avatar do not). Compute connected components on the lattice over 4-cardinal adjacency. The level wins when every component containing at least one molecule has molecules of exactly one colour. Components with no molecules are tolerated. If the predicate is true, fire `next_level()`.

## Region-paint feedback (visual aid)

When the connected-component pass identifies a monochromatic region, every cell of that region gets a coloured backdrop (`paint_red` → palette 7 pink, `paint_blue` → palette 10 light-blue, `paint_green` → palette 14 green) laid down via 3×3 INTANGIBLE sprites at layer 0. The reveal animates: `PAINT_CELLS_PER_TICK = 2` cells per render tick while `step()` returns without `complete_action()`, so the player sees a wash spreading through the region rather than an instant fill. If an L3 stamp-toggle reconnects two regions, the now-mixed component's paint sprites are removed instantly so the visual state always tracks the current connectivity. This is purely cosmetic — paint sprites do not block movement or affect the partition computation.

## Lose condition

Two distinct paths to `lose()`:

- **Step budget exhaustion**: `step_remaining == 0 AND win predicate is false` → `lose()`. Same across all levels.
- **Submerge-lose** (L1/L2 only — `stamp_toggle_allowed == False`): if after an action the avatar's lattice cell is part of a painted (monochromatic) region AND the global win predicate is still false, fire `lose()` immediately. The avatar is sealed inside a finished region by permanent walls; no future action can reconnect to the still-mixed cells. Per `difficulty-rules.md` § 1's lose-mirror clause, surfacing this immediately rather than letting the budget drain in a no-win waiting room. At L3 the avatar can in principle toggle a boundary stamp to escape, so submerge-lose is suppressed; the player relies on the step budget instead.

## Internal state

- `self._step_budget: int` — current level's budget (from `level.get_data("step_budget")`).
- `self._step_counter_ui: StepCounterHud` — `RenderableUserDisplay` rendering the bottom-row remaining-steps bar (palette 11 yellow filled, palette 3 grey drained).
- `self._stamp_toggle_allowed: bool` — set from `level.get_data("stamp_toggle")`; True only at L3. Gates both the toggle-off branch in `_try_stamp` AND the submerge-lose check in `_finalise_action`.
- `self._paint_phase: int` — `-1` when no paint reveal animation is in progress, `>= 0` while the queue is being drained. Encoded as a phase counter so the standard reference-game multi-tick `step()` pattern applies (return without `complete_action()` while `_paint_phase >= 0`).
- `self._paint_queue: list[(cell, colour)]` — pending cells to paint, drained two-per-tick.
- `self._painted_cells: dict[cell, colour]` — currently painted lattice cells. Used by `_avatar_in_painted_region` for the submerge-lose check, and by `_update_painting` to determine which cells need adding/removing.
- `self._paint_sprites: dict[cell, Sprite]` — handle to each paint sprite for the level, so `_remove_paint` can call `level.remove_sprite(...)` on the precise instance when an L3 toggle reconnects regions.

## Notable code patterns

- **Lattice abstraction over a finer grid.** Every gameplay sprite is 3×3 placed on a 3-cell stride; arrows move the avatar by 3 cells, and the partition check operates on a 6×6 lattice rather than the 20×20 pixel grid. `_pos(i, j) = (1 + 3*i, 1 + 3*j)` keeps the level-build code legible. Reusable for any sokoban-style game where the player thinks in coarse cells.
- **Connected-components via lattice flood-fill.** `_compute_components()` extracts each placed sprite's lattice cell from `(s.x - 1) // 3`, classifies it as wall / molecule / other, and runs a stack-BFS over the molecule cells' components, returning a list of `(cells, colour-label)` pairs. Both the win predicate and the paint-update reconciliation consume this single decomposition. Reusable for any partition / connectivity-based win predicate.
- **Paint reveal via the standard phase-tick `step()` idiom.** When `_update_painting` queues new cells, `step()` enters a per-render-tick mode: subsequent calls advance `_paint_phase` and add cells from the queue without calling `complete_action()`. The engine re-renders between phase ticks, so the player sees a multi-frame wash spreading across the region. When the queue is empty, `_finalise_action` runs (win/lose/budget checks) and `complete_action()` is finally called. Same pattern as zd7m's teleport-phase, sb26's commit-marker walk, sp80's pour, and tu93's avatar-slide.
- **Submerge-lose mirror of the lose-side waiting-room rule.** `difficulty-rules.md` § 1 forbids tight step budgets that punish exploration AND its lose-side mirror — making the player wait in a no-win waiting room for the budget to drain. Submerge-lose detects exactly that case: avatar in a sealed monochromatic region with the global win still false at L1/L2, fire `lose()` immediately. Reusable as a generalisation: any game where regions become unreachable should fire `lose()` the turn the unreachability is detected, not at budget exhaustion.
- **Paint cleanup-on-reconnect.** L3's stamp-toggle can convert a monochromatic region back into mixed by reconnecting it to another region. `_update_painting`'s desired-vs-actual diff handles this: cells whose component no longer has the right colour label have their paint sprite removed via `level.remove_sprite(...)` instantly (no animation). Reusable for any "visual seal" pattern that might un-seal due to mid-game state changes.
- **State init before `super().__init__()`.** `NovaBaseGame.__init__` calls `set_level(0)` which calls `on_set_level`. If `_step_budget` and other on_set_level-populated fields are assigned AFTER `super().__init__()` returns, the post-super assignment overwrites the just-populated state with empty defaults, causing an immediate `lose()` on the first action because `remaining = 0 - 1 < 0`. Documented in lv4k's mechanism-detail; this generator hit and fixed the same bug. Universal lesson for any subclass whose `on_set_level` builds derived state.
- **Level data drives per-level behaviour.** `level.get_data("stamp_toggle")` is True only on L3, gating the toggle-off branch of `_try_stamp` AND the submerge-lose suppression in `_finalise_action`. Reusable for any per-level mechanic flag.
- **3×3 sprites for visual detail floor.** Every gameplay sprite is a 3×3 block with internal pixel structure (rings for red, plus-shape for blue, X-pattern for green, ring-with-centre-dot for the avatar). Paint sprites are 3×3 of a single palette index (pink, light-blue, green) at layer 0 so they render below molecules and the avatar; the molecule's distinctive shape stays legible against the painted background. The boundary of the 20×20 grid uses 1×1 `wall_rim` sprites; these are tagged `wall_rim` and explicitly skipped in the partition check (which only considers lattice-aligned 3×3 sprites).
