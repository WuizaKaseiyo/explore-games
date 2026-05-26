# qj4r — fold-mirror-pair

## Summary
Cardinal arrows fold the active rectangular playfield across its central horizontal or vertical axis: pieces on the pressed-direction half reflect across the central axis to the opposite half over a 4-frame animation (3 in-flight interpolated frames + 1 snap), and the folded-out half is permanently retired into the dim padding region (the active region halves on every fold). **Targets are anchored**: they don't reflect — they stay at their absolute logical cells. If a fold retires a target's cell into padding, the target is destroyed and the level is unwinnable (`self.lose()` fires immediately). Two same-colour pieces that meet at one cell after a fold *merge* into a single piece (count goes 2→1, marked with a maroon rim + double inner dot). The win is to land each coloured piece on its same-coloured target ring with per-colour piece-count exactly equal to per-colour target-count.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Fold top onto bottom; kept = bottom y-range; pieces in top y reflect across central horizontal axis | always (no-op if active y-range is 1 cell) |
| ACTION2 | Fold bottom onto top; kept = top y-range | always (no-op if active y-range is 1 cell) |
| ACTION3 | Fold left onto right; kept = right x-range; pieces in left x reflect across central vertical axis | always (no-op if active x-range is 1 cell) |
| ACTION4 | Fold right onto left; kept = left x-range | always (no-op if active x-range is 1 cell) |

(`available_actions=[1, 2, 3, 4]`. No click, no ACTION5, no undo.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 fold-mirror-translate (with anchored-target destruction) | 1 orange piece at logical (1,1); 1 orange anchored target at (6,6). Piece+target differ on both axes so the witness must perform one x-fold AND one y-fold, ensuring the player observes the mechanic. **2 of 4 first folds (ACTION2, ACTION4) instantly lose** — they retire the target's row or column into padding, destroying the target and triggering `lose()`. Witness `[ACTION3, ACTION1]` (or symmetric `[ACTION1, ACTION3]`). |
| 2 | M2 same-colour-piece-merge (composed with M1 + anchored target) | 2 orange pieces at (1,4) and (6,4); 1 anchored target at (5,4). Witness must use M2 to reduce orange count from 2 to 1 (count==1 per colour predicate) AND avoid retiring the target's row (ACTION2) or its kept x-column (ACTION4). Witness `[ACTION3, ACTION4]`. |
| 3 | M1 + M2 (no new mechanic vs L2; second colour group added) | 2 orange pieces (1,4) and (6,4); orange anchored target at (5,4); 1 purple piece at (2,1); purple anchored target at (5,1). Witness `[ACTION3, ACTION4]` is unique among 2-step paths: every other 2-step sequence retires at least one of the two anchored targets and loses. Step 1 merges oranges and lands purple on target_P; step 2 lands the merged orange on target_O. |

## Win condition

For each colour C ∈ {orange, purple} present in the level: `count(active C-pieces) == count(C-targets)` AND each C-piece's logical cell coincides one-to-one with a C-target's cell. Additionally, `count(active grey decoys) == 0`. When all conditions hold, `self.next_level()`.

## Lose condition

`self.lose()` fires when EITHER:
- A finalised fold leaves any colour with `count(pieces) > count(targets)` — i.e. an anchored target was destroyed by being retired into padding (computed in `_is_unwinnable()`).
- `self._action_count >= self._step_budget`.

## Internal state

- `active_x_min`, `active_x_max`, `active_y_min`, `active_y_max` — current logical bounds of the playable region (initially 0..7 × 0..7; halves per fold).
- `_cell_size = 4` — display-pixel cell granularity (constant).
- `_grid_offset = 16` — frame-pixel offset for the active region's top-left.
- `_step_budget` — per-level step cap; read from `level.get_data("step_budget")` at level-start.
- `_step_bar` — `StepBarHud` widget on the camera's interfaces list.
- `_anim_phase` (sentinel `-1` = idle), `_anim_total` (= 3), `_anim_action_id`, `_anim_paths` (list of `(sprite, px0, py0, px1, py1, new_cx, new_cy)`), `_anim_axis`, `_anim_kept_lo`, `_anim_kept_hi` — fold animation state machine.
- `active_floor` sprite — 64×64 sprite (cloned per level) whose pixels are mutated in-place per fold to render the checkered active region (palettes 1/2 in idle; maroon overlay in folded-half during in-flight frames).

## Notable code patterns

- **Multi-phase animation via `_anim_phase` sentinel.** `step()` checks `_anim_phase >= 0` first; if so, it advances the phase, renders an in-flight frame (interpolating piece positions and recolouring the folded half), and *omits* `complete_action()` so the engine re-renders and re-calls `step()`. On the final phase, `_finalize_fold()` snaps to destinations and `complete_action()` fires. Reusable for any single-action multi-frame transformation (lifts, sweeps, falls).
- **Fold reflection as a closure factory.** `_compute_fold(action_id)` returns a `(axis, reflect_fn, kept_lo, kept_hi)` tuple where `reflect_fn(cx, cy) -> (cx, cy)` applies the mirror formula `x_new = (lo + hi) - x_old` (or y) for cells in the folded half and identity for kept-half cells. Reusable for any "central-axis reflection on a contractable rectangle" mechanic.
- **Anchored sprites via tag-skipping in the reflection pass.** `_start_fold_animation` builds `_anim_paths` only for sprites NOT tagged `target` (or `active`); targets stay at their absolute cells. `_finalize_fold` then iterates `get_sprites_by_tag("target")` and removes any whose cell is now outside the contracted active region. Reusable for any "some entities anchor while others drift" rule.
- **In-place pixel mutation for variable-shape sprite (`active_floor`).** Instead of rebuilding the Sprite per fold, the same Sprite's `pixels` ndarray is overwritten via `pixels[:] = -1` then per-cell `pixels[py:py+cs, px:px+cs] = color`. Cheaper than reconstructing the sprite.
- **Two-pass transformation pipeline after a fold.** After the reflection snap, `_finalize_fold` sequentially applies (1) anchored-target survival check, (2) same-colour merge by grouping pieces by destination cell.
- **Sprite.set_interaction(InteractionMode.REMOVED) for transient removal.** M2 (other-piece collapse) and target-destruction-on-retire both use this to retire sprites without removing them from the level structure.
