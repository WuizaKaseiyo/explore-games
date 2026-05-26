# kj82 — plank-pivot-walk

## Summary

Plank-Pivot Crossing is a path-walking puzzle on a plane of long
rigid planks pinned at one end by fixed anchors. The player walks
a small pawn one cell per arrow-press across plank cells, clicks a
plank to select it as active, and presses ACTION5 to pivot the
active plank 90° clockwise around its anchor — the plank's free
tip sweeps through a quarter-arc and the pawn rides with the plank
if it was on a non-anchor cell. Posts toggle between solid (blocks
plank rotations whose arc would pass through them) and hollow
(passable for both plank and pawn). Springs anchored to a plank
launch the pawn 5 cells in the direction the plank extends from
its anchor when the pawn ends a turn on the spring's centre. Win
when the pawn stands on the goal tile before the step counter
drains; lose only if the budget exhausts.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Walk pawn 1 cell up | destination must be a plank cell and not a blocking-post cell |
| ACTION2 | Walk pawn 1 cell down | same |
| ACTION3 | Walk pawn 1 cell left | same |
| ACTION4 | Walk pawn 1 cell right | same |
| ACTION5 | Pivot active plank 90° CW around its anchor; pawn rides if off-anchor | requires `_active_plank` set; rejected if any new plank cell is on a blocking post or off-grid |
| ACTION6 | Click; on post: toggle blocking↔permeable; on plank: select/deselect that plank | always available |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | walk-on-plank + select-and-pivot-with-carry | One length-8 plank east at (10, 5)..(17, 11), pawn at (13, 10), goal at (10, 17). Pivot south once, then walk south on the rotated plank to the goal. Witness `[ACTION6@(13,10), ACTION5, ACTION2, ACTION2, ACTION2, ACTION2]` (6 actions). |
| 2 | + post-toggle-controls-rotation | Two length-13 planks, a blocking post at (4, 12) sits in the south-arc of plank_alpha. Player must toggle the post first, then pivot, then walk south to the bridge cell, then east to goal. Witness `[ACTION6@(4,12), ACTION6@(8,6), ACTION5, ACTION2×8, ACTION4×12]` (23 actions). |
| 3 | + spring-launch-along-plank-axis | Plank_gamma length 13 east at (4, 8); plank_delta length 8 east at (4, 20); blocking post at (4, 14); spring on plank_delta's east tip at (11, 20); goal at (16, 20) off any plank. Toggle post, pivot plank_gamma south, walk to plank_delta, walk east onto spring; spring fires east 5 cells onto goal. Witness `[ACTION6@(4,14), ACTION6@(8,8), ACTION5, ACTION2×8, ACTION4×7]` (18 actions). |

## Win condition

After every action's `complete_action()`: if the pawn's grid cell
exactly equals the level's `goal_tile` cell, fire `next_level()`.

## Lose condition

At the top of `step()`, if `_action_count >= _max_steps` (per-level
budget read from `level.get_data("step_budget")`), fire `lose()`.
No collision-based or hazard-based loss path. Step budgets:
30 / 50 / 60 (L1 / L2 / L3, non-shrinking).

## Internal state

- `_active_plank: _PlankState | None` — currently selected plank
  instance, or None.
- `_planks: list[_PlankState]` — every plank instance in this
  level, with its anchor cell, length, current orientation
  (0=east, 1=south, 2=west, 3=north), and references to its
  fixture and optional spring child.
- `_post_pairs: list[dict]` — pairs of (blocking, permeable)
  twin sprites at the same cell. Toggle swaps which is TANGIBLE.
- `_springs: list[_PlankState]` — planks that own a spring child
  sprite, used to iterate over springs at end-of-step.
- `_pawn`, `_goal`, `_halo: Sprite` — singleton sprite references
  for the pawn avatar, goal tile, and the active-plank halo
  overlay.
- `_max_steps: int` — per-level step budget.
- `_step_counter_ui: StepCounterHud` — depleting bar widget.

## Notable code patterns

- **Plank rotation by pixel-array swap.** The plank sprite's
  `pixels` attribute is reassigned to a `np.rot90(base, k=...)` of
  the east-frame stripe pattern; `set_position` is recomputed so
  the anchor cell stays at the same grid coordinate. Cell-set per
  orientation derived directly from a (i, j) east-frame indexer
  with explicit transformations per orientation. Reusable as
  "rotate a multi-cell sprite around an off-centre pivot".
- **Pivot-carry via offset transform.** Pawn at offset (dx, dy)
  from anchor → after CW pivot, new offset (-dy, dx). Same
  transform used to move the spring child sprite along with its
  plank. Reusable as "rigid-group rotation around a fixed point".
- **Two-sprite swap for posts.** Co-positioned `post_blocking` and
  `post_permeable` sprites; toggle swaps `InteractionMode.TANGIBLE
  ↔ REMOVED` between them. Pixel-perfect visible cue without
  pixel-mutation.
- **Active-plank visual via overlay halo.** Separate `anchor_halo`
  sprite gets repositioned and toggled INTANGIBLE/REMOVED when the
  active plank changes. Avoids the tu93 anti-pattern of
  pixel-mutating the plank itself to show selection state.
- **Spring-launch with destination-validity check.** Spring fires
  in the direction the underlying plank extends; intermediate cells
  blocked only by `post_blocking`; destination must be a plank
  cell or the goal cell or the launch is rejected silently.
  Reusable as "ranged jump with mid-flight obstacle veto".
