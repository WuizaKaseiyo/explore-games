# kx14 — tide-tilt-buoyant

## Summary
The playfield is a vertical cross-section of a fluid tank: light-blue
water fills cells from a movable surface line down to the bottom row,
and off-white air fills cells above. The player has three categories of
verb: ACTION1/2 raise / lower the water surface by 1 row each press,
ACTION3/4 tilt every un-anchored floating ball one cell left / right,
and ACTION6 click on a ball to toggle its anchor (which pins it
against both surface changes and tilts). Each level resolves when
every coloured ball sits inside its same-coloured target ring. The
single failure mode is exhausting the per-level step counter; missing
clicks (no ball under the cursor) do not consume a step.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Raise water surface by 1 row (toward grid top); re-project un-anchored balls upward unless blocked by a same-column platform in their rise path. | Always valid; clamped at row 0. Always consumes 1 step. |
| ACTION2 | Lower water surface by 1 row (toward grid bottom); re-project un-anchored balls downward unless blocked. | Always valid; clamped at row N_CELLS. Always consumes 1 step. |
| ACTION3 | Tilt left: iterate balls column-ascending; each un-anchored ball moves one cell left if `(c-1, r)` is in-bounds, not a platform-cell, and not occupied by another ball. Re-projection runs after the tilt. | Always valid. Always consumes 1 step. |
| ACTION4 | Tilt right: iterate balls column-descending; each un-anchored ball moves one cell right under the same conditions. Re-projection runs after. | Always valid. Always consumes 1 step. |
| ACTION6 | Click `(x, y)` (display pixels). Convert via `camera.display_to_grid` then floor-divide by `CELL_PIXELS=5` to find the clicked cell. If a ball occupies that cell AND `level.get_data("AnchorEnabled")` is true, swap that ball's `dmzpvavhuh` (float) and `vqfwzbpxir` (anchored) sprite pair via `set_interaction(InteractionMode.{TANGIBLE,REMOVED})`. | Always offered. Consumes a step only if the click resolved to an anchorable ball. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Tide control + tilt (base system, N=2) | Open tank, no platforms, no anchor. One orange ball at (3, 8); one orange target ring at (8, 4); water level starts at row 8, step budget 25. Both verbs must fire at least once in the witness. |
| 2 | + platform-block (N+1=3) | One orange ball at (1, 9); one orange target ring at (10, 3); one 3-cell-wide platform at row 6 cols 0–2 blocks the direct rise from column 1; step budget 30. Witness must tilt right past the platform's right edge before continuing the rise. |
| 3 | + anchor toggle (N+2=4) | Two balls (orange at (3, 9), green at (8, 9)) that must SWAP horizontal sides — orange lands at orange-target (8, 5), green at green-target (3, 5). One platform at row 6 cols 4–6 blocks the upper tilt corridor for the second ball. Step budget 45. Witness anchors orange, lifts green to its target, anchors green, unanchors orange, lowers water below the platform, tilts orange right, then raises water — uses both directions of every prior mechanic plus the anchor toggle. |

## Witness solution — Level 3

A 21-action sequence that wins L3 (verified end-to-end against the
implementation; ends with `state=GameState.WIN`):

```
 1. ACTION6 click cell (3, 9)   # anchor the orange ball at its start
 2. ACTION1                     # water 9→8; green (8, 9)→(8, 8); orange pinned
 3. ACTION1                     # water 8→7; green (8, 8)→(8, 7)
 4. ACTION1                     # water 7→6; green (8, 7)→(8, 6) (col 8 clear of platform)
 5. ACTION1                     # water 6→5; green (8, 6)→(8, 5)
 6. ACTION3                     # tilt left; green (8, 5)→(7, 5) (row 5 clear, platform at row 6)
 7. ACTION3                     # tilt left; green (7, 5)→(6, 5)
 8. ACTION3                     # tilt left; green (6, 5)→(5, 5)
 9. ACTION3                     # tilt left; green (5, 5)→(4, 5)
10. ACTION3                     # tilt left; green (4, 5)→(3, 5) — green at green target
11. ACTION6 click cell (3, 5)   # anchor green at its target
12. ACTION6 click cell (3, 9)   # unanchor orange; orange rises in col 3, blocked by anchored green;
                                # lands at (3, 6)
13. ACTION2                     # water 5→6; orange at (3, 6) is now at the surface (no row change)
14. ACTION2                     # water 6→7; orange falls with the surface to (3, 7)
15. ACTION4                     # tilt right; orange (3, 7)→(4, 7) (row 7 below platform — clear)
16. ACTION4                     # tilt right; orange (4, 7)→(5, 7)
17. ACTION4                     # tilt right; orange (5, 7)→(6, 7)
18. ACTION4                     # tilt right; orange (6, 7)→(7, 7)
19. ACTION4                     # tilt right; orange (7, 7)→(8, 7)
20. ACTION1                     # water 7→6; orange re-projects up to (8, 6) (col 8 clear)
21. ACTION1                     # water 6→5; orange re-projects up to (8, 5) — orange at orange target
```

ACTION6 click coordinates in display pixels: `(col*5 + 2, row*5 + 2)`
maps the cell centre into the camera viewport with the 2-pixel
letter-box offset accounted for.

Mechanic exercise: M1 (water-control, both raise and lower), M2 (tilt,
both left and right), M3 (platform-block — forces the orange ball's
descend-tilt-rise detour at row 7 because tilt-right at row 6 is
blocked by the middle platform), and M4 (anchor toggle — three uses:
anchor orange at start, anchor green at target, unanchor orange to
reroute).

## Win condition

After every committed action, walk the list of target rings. For each
target at `(col, row, target_color)`, check whether some ball has
`b["col"] == col`, `b["row"] == row`, and `b["color"] == target_color`.
Target colour comes from the ring sprite's dominant non-{4,5} palette;
ball colour from the float sprite's dominant non-{4,5} palette. If
every target is colour-matched by at least one ball,
`self.next_level()` fires; the engine handles the L3-completes →
`self.win()` transition automatically.

## Lose condition

Single fail mode: `self._steps_used >= self._max_steps` while the win
predicate is False. The lose check fires AFTER the win check on each
action so a final-action-completes-the-puzzle case wins instead of
loses. No hazards, no chasers, no instant-fail collision.

## Internal state

- `self._water_level: int` — current water surface row (0 = top, N_CELLS = below grid).
- `self._water_sprite: Sprite | None` — the `wkkqxbjzye` instance for the active level; pixels are mutated each tide change.
- `self._balls: list[dict]` — one entry per placed ball with keys `float_s`, `anchor_s`, `col`, `row`, `color`, `anchored`. Float and anchor sprite variants share the cell; only one is `TANGIBLE` at any time.
- `self._platforms: list[tuple[int, int, int]]` — `(col_start, col_end_inclusive, row)` per platform sprite, derived from sprite position and width in `on_set_level`.
- `self._targets: list[tuple[int, int, int]]` — `(col, row, color)` per target ring.
- `self._anchor_enabled: bool` — set from `level.get_data("AnchorEnabled")`. False in L1 + L2; True in L3.
- `self._max_steps: int`, `self._steps_used: int` — per-level budget and tally; the HUD bar reads `max_steps - steps_used`.
- `self._step_bar: bekzbtmcoz` — the `RenderableUserDisplay` widget (registered with the camera in `__init__`).

## Notable code patterns

- **Pixel-mutated water sprite as a 60×60 background.** A single
  60×60 sprite with `pixels` rebuilt from a numpy slice
  (`new_pixels[wp:, :] = WATER_COLOR` then `self._water_sprite.pixels =
  new_pixels`) lets the water surface be expressed as one sprite with
  layer=0 instead of N row-strip sprites. Cheap O(60²) on each tide
  change; visually crisp.
- **Float/anchor sprite-pair swap.** Each ball has two sprite
  instances (`dmzpvavhuh` float + `vqfwzbpxir` anchored variant) at
  the same cell, with one set to `InteractionMode.TANGIBLE` and the
  other to `REMOVED`. Toggling anchor swaps which is `TANGIBLE`. This
  is the universal-scaffold's "Two-sprite swap" idiom — cleaner than
  mutating pixels in place because the alternative state is fully
  inspectable in the level (and renders as a different sprite shape
  for visual feedback).
- **Re-projection after every effective action.** A single
  `_reproject_balls()` helper, called after every state-changing
  action, computes each un-anchored ball's natural row given current
  water level + platforms. The helper uses two coord-aware platform
  queries: `_max_platform_row_in_col_in_range` for the "rising ball
  blocked from below" case (largest-row platform blocks first) and
  `_min_platform_row_in_col_in_range` for the "falling ball blocked
  from above" case (smallest-row platform blocks first). Inter-ball
  collisions are resolved by backing the moving ball off one cell at
  a time in its motion direction.
- **Private `_steps_used` counter** following qz73's pattern. The
  engine's `_action_count` advances on every action; `_steps_used`
  advances only when the action did something effective, letting
  misclicks be no-cost. The HUD bar and the lose check both read
  `_steps_used`.
- **Tag-based level introspection in `on_set_level`.** Platform /
  target / ball / water sprites are all queried by tag
  (`level.get_sprites_by_tag("platform")` etc.) and projected into
  the per-game state lists. Dominant-colour extraction handles
  per-instance recolour by looking at the most-frequent
  non-{4,5}-and-non-transparent palette value of the sprite.
