# wt39 — glide-deflect-thaw

## Summary

A red pawn glides cell-by-cell across a tiled ice arena in the
direction of the most recent arrow press, stopping only when the
slide meets a wall, an angled-bumper deflector (which turns the
glide ninety degrees in flight), or a thaw-tile that has already
cracked. Player input is pure cardinal motion (ACTION1-4); there is
no click and no modal verb. The level wins when, after a slide
settles, the pawn sits on the goal cell; it loses when the per-level
step budget reaches zero. The game uses physics (momentum,
frictionless glide, ninety-degree elastic deflection) and topology
(reachability through cracked-thaw walls) as its core priors.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Slide pawn north until blocked | always valid |
| ACTION2 | Slide pawn south until blocked | always valid |
| ACTION3 | Slide pawn west until blocked | always valid |
| ACTION4 | Slide pawn east until blocked | always valid |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 = slide-until-wall (base dynamic system) | A 5-slide zig-zag through the open arena. Pawn at (2, 2) must reach goal (10, 10); five interior wall blocks at (11, 2), (10, 6), (2, 5), (3, 11), (11, 10) carve out the staircase route. Witness: `[ACTION4, ACTION2, ACTION3, ACTION2, ACTION4]` (RIGHT, DOWN, LEFT, DOWN, RIGHT). Step budget 50. |
| 2 | M2 = bumper-deflect (90° in-flight deflection) | A 5-slide route requiring TWO angled bumpers — one at (10, 2) (col 10 rows 1-4 are sealed except via this deflection) and one at (9, 7) (col 9 has no slide-stops at any row, so without the press-4 E→S deflection the pawn cannot reach (9, 10) and therefore cannot reach the goal). Walls (10, 5), (3, 4), (4, 8), (9, 11), (11, 10) provide the slide-stops in between. Witness: `[ACTION4 (bumper deflect), ACTION3, ACTION2, ACTION4 (bumper deflect), ACTION4]` (RIGHT, LEFT, DOWN, RIGHT, RIGHT). Step budget 100. |
| 3 | M3 = thaw-cracking (one-pass-then-becomes-wall) | A 6-slide route on a layout DISTINCT from L2: bumper2 sits at (8, 7) instead of (9, 7); wall (9, 11) is dropped; two frozen thaws are introduced — a decorative one at (4, 5) (consumed by press-3 DOWN col 4) and a load-bearing one at (8, 9). The press-4 RIGHT slide deflects E→S off bumper(8, 7), drives the pawn down col 8 cracking thaw(8, 9), and overshoots to (8, 12); press-5 UP col 8 is then stopped by the new cracked-thaw wall at (8, 9) and settles the pawn on (8, 10); press-6 RIGHT row 10 reaches the goal at (10, 10) via wall (11, 10). Thaw(8, 9) is counterfactually necessary: with it frozen, no slide-stop terminates anywhere in col 8 because col 8 has no other walls between rows 1 and 12. Witness: `[ACTION4, ACTION3, ACTION2, ACTION4 (bumper deflect, cracks thaw), ACTION1 (stops on cracked thaw), ACTION4]` (RIGHT, LEFT, DOWN, RIGHT, UP, RIGHT). Step budget 140. |

## Win condition

The pawn's stable position after a slide settles equals the goal
sprite's grid position. A slide that *passes through* the goal cell
mid-flight (because the cell after is not a wall and the pawn has
remaining momentum) does NOT trigger win — only stopping ON the
goal does. Same predicate for L1, L2, L3.

## Lose condition

The per-level step budget (30 / 60 / 80 for L1 / L2 / L3) reaches
zero before the win predicate fires. There is no other lose path —
no hazards, no respawn cost, and cracked thaws never harm the pawn
(they only block future slides).

## Internal state

- `_step_budget`, `_steps_remaining` — per-level integer counters.
  Budget is read from `level.get_data("step_budget")` in
  `on_set_level`; `_steps_remaining` decrements one per action.
- `_step_hud` — `StepCounterHud` instance, registered as the
  Camera's only interface; renders a depleting top-row bar.
- The pawn's grid position lives on the pawn `Sprite` itself
  (queried via `level.get_sprites_by_tag("pawn")`); the game class
  does not cache it separately.
- Thaw cracking is implemented by remove-and-replace: when a slide
  passes through a `thaw_frozen` sprite at (x, y), that sprite is
  removed from the level and a freshly-cloned `thaw_cracked` sprite
  is added at the same position. The cracked sprite has tag
  `cracked` and is collidable; the slide loop treats `cracked`
  the same as `wall`.

## Notable code patterns

- **Pure-iteration slide simulator** (`Wt39._slide`): a single
  while-loop that advances the pawn one cell at a time, classifies
  the next cell via tag membership (`wall`, `bumper`, `frozen`,
  `cracked`), and either continues, deflects, or breaks. No
  recursion, no animation phase counters, no engine-level event
  hooks.
- **Tag-based blocker classification** (`_blocker_at`): one
  iteration over `current_level.get_sprites()` per cell-check, with
  early-exit on `wall` / `cracked` / `bumper` tag membership. Sprites
  marked `InteractionMode.REMOVED` are skipped, so the same level
  data could be repurposed with toggle-able obstacles by flipping
  interaction modes (not used in this game but the pattern is
  there).
- **Add-then-remove for transient state** (`_crack`): rather than
  swapping `interaction` modes between two co-located sprites, the
  cracking handler simply removes the frozen sprite and adds a fresh
  cracked clone. Cleaner for a one-shot transition; the alternative
  (the InteractionMode.REMOVED swap) would require placing both
  sprites at level-build time and tracking which is currently
  TANGIBLE.
- **Bumper deflection table** (`_DEFLECT_BACK`): a 4-entry dict
  keyed by incoming `(dx, dy)` returning the outgoing direction.
  Trivially extensible: a `_DEFLECT_FWD` for "/" bumpers would be
  the same shape with opposite mappings, registered by tag membership
  inside `_slide`.
- **Camera viewport set in `on_set_level`** even though all three
  levels share `grid_size = (14, 14)`: defensive boilerplate that
  makes adding a fourth level with different dimensions safe in the
  future.
