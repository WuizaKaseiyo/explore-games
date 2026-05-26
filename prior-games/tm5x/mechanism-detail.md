# tm5x — thermal-aura-imprint

## Summary

A single pawn walks a 16×16 thermal grid, carrying a polarity (hot
or cold) it can toggle with ACTION5. After every step, the pawn's
own thermal cell is imprinted at ±2 (sign of polarity) and the
four cardinal-neighbour cells at ±1; all other cells reset to 0.
Goal markers latch permanently the moment their underlying cell
shows the marker's required temperature value, surfacing the latch
visually as a gold-frame variant. The level wins when every marker
is latched, and loses when the step counter exhausts. Walls (L3)
block both pawn movement and aura-imprint propagation, partitioning
the field's reachability.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move pawn one thermal cell up (display y -= 4) | destination in-bounds AND not a wall cell |
| ACTION2 | Move pawn one thermal cell down (display y += 4) | as above |
| ACTION3 | Move pawn one thermal cell left (display x -= 4) | as above |
| ACTION4 | Move pawn one thermal cell right (display x += 4) | as above |
| ACTION5 | Toggle polarity hot ↔ cold (swaps pawn variant) | always valid |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | walk + aura-imprint | Pawn at thermal (8, 8) hot; one hot target at (8, 13) requiring +2. Witness `[ACTION2, ACTION2, ACTION2, ACTION2, ACTION2]` (5 actions) — walk DOWN onto target. Step budget 30. |
| 2 | + ACTION5 polarity toggle | Pawn at (8, 8) hot; hot target at (3, 8) and cold target at (13, 8) requiring +2 and -2 respectively. Witness `[ACTION3 ×5, ACTION5, ACTION4 ×10]` (16 actions) — walk LEFT onto hot target (latches), toggle to cold, walk RIGHT to cold target. Step budget 60. |
| 3 | + insulator walls | Pawn at (3, 1) hot; hot target at (3, 13), cold target at (13, 13); 12-cell vertical wall at col 8 rows 4..15 with gap rows 0..3. Witness `[ACTION2 ×12, ACTION5, ACTION1 ×10, ACTION4 ×10, ACTION2 ×10]` (43 actions) — walk DOWN to hot target, toggle to cold, route UP through gap, RIGHT, DOWN to cold target. Removing the wall would shorten the witness from 43 to 23, confirming the wall is non-decorative. Step budget 100. |

## Win condition

After every action, the per-level integer temperature grid is
recomputed from the pawn's position + polarity. Each unsatisfied
target sprite (tag `"target"`) checks its underlying thermal
cell's value; if it matches the target's required value
(`target_hot` requires +2, `target_cold` requires -2), the target
is added to `_satisfied`, the original sprite is set to
`InteractionMode.REMOVED`, and a gold-framed `target_<X>_satisfied`
variant is added at the same position. When every target placed in
the level is in `_satisfied`, `self.next_level()` fires.

## Lose condition

If `self._action_count >= step_budget` (per-level data; 30/60/100
for L1/L2/L3), `self.lose()` fires. There is no other lose state —
no hazards, no enemies, no irreversible soft-lock.

## Internal state

- `self._polarity: int` — `+1` (hot) or `-1` (cold). Toggled by ACTION5. Surfaced visually by which pawn variant (pawn_hot vs pawn_cold) is `InteractionMode.TANGIBLE`.
- `self._satisfied: set[str]` — names of latched targets. Surfaced visually by gold-frame target_<X>_satisfied sprites.
- `self._initial_target_names: set[str]` — captured at level start, used as the "all targets latched" target for the win-check.
- `self._temperature: np.ndarray (16, 16)` — recomputed every step from pawn position + polarity (positional, not accumulating).
- `self._step_counter_hud: StepCounterHud` — RenderableUserDisplay with current/max for the depleting bar.

## Notable code patterns

- **Pawn-variant two-sprite swap.** Both pawn_hot and pawn_cold are
  pre-placed at the level's start cell; one is TANGIBLE (active)
  and the other REMOVED. ACTION5 swaps them: the variant matching
  the new polarity becomes TANGIBLE at the active pawn's position;
  the previously-active variant moves to the same position and
  becomes REMOVED. This is the
  `code/universal-scaffold.md` "Two-sprite swap" idiom — cleaner
  than `set_visible(False)` because collision is also gated.
- **Positional thermal field.** `_recompute_temperature` is a pure
  function of pawn position + polarity + walls; the field has no
  history. This makes the game trivially deterministic and easy to
  reason about (no cellular-automaton state to debug).
- **Big sprite as the rendered field.** `temperature_field` is a
  64×64 sprite at position (0, 0). Every step, its `pixels` array
  is rebuilt from the 16×16 temperature grid by stamping a 4×4
  chamfered-tile pattern per thermal cell. One sprite, one
  numpy-update — much cheaper than 256 individual sprite swaps.
- **Cumulative-latch win.** Targets latch on first match-with-
  required and stay latched even when pawn moves away (unlike
  pf3w wavefront-converge-timing's single-tick-coincidence model).
  Implemented as a `set[str]` on the Game instance plus a sprite
  swap to a gold-frame variant.
- **Chamfered-tile thermal patterns.** Each of 5 temperature
  values renders as a 4×4 block with a solid centre + corner
  accents (no diagonals). This satisfies checklist item 20's
  "no chunky uniform-colour blocks" rule while avoiding any
  pattern that resembles a letter (X-shapes were rejected at
  critique-spec).
