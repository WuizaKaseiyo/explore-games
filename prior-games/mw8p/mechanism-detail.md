# mw8p — predator-prey-triangle

## Summary

The player controls a single light-blue A-creature with cardinal
arrow keys on an 8-cell × 8-cell logical playfield (rendered on
the native 64×64 canvas). Two species of autonomous NPC share the
playfield: B (orange, spiky) pursues A one cell per turn under a
Manhattan-dominant policy (tie → x) and removes A on same-cell
coincidence; C (green, leafy) pursues the nearest live B under
the same policy and removes that B on coincidence. The triangle
closes via the A-eats-C rule: when A walks onto a C, A enters the
cell and the C is consumed. Walls block all three species, and
the level wins when A enters the exit cell.

Each ACTION1..4 produces FIVE rendered frames in sequence (A's
move, B's half-step, B's full-step, C's half-step, C's full-step)
so the chase and the eats are visually legible to the player.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | MOVE UP — translate A by one logical cell (8 px) in −y. | always; no-op on wall / OOB / B-cell (lose) / consume C on enter |
| ACTION2 | MOVE DOWN — +y. | same rules |
| ACTION3 | MOVE LEFT — −x. | same rules |
| ACTION4 | MOVE RIGHT — +x. | same rules |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1: B-chases-A and kills on same-cell. | A at (0, 0), B at (2, 1), exit at (7, 7), open arena. Naïve RIGHT-first loses at turn 8 because B's column-mirroring pursuit positions B at (7, 1) just as A reaches (7, 0). The player must reason that DOWN-first escapes B's projected interception. Witness `[2,2,2,2,2,2,2,4,4,4,4,4,4,4]` (DOWN ×7 then RIGHT ×7) — 14 actions. |
| 2 | M2: C-chases-B and kills on coincidence. | A at (0, 0), C at (4, 3), B at (4, 5), exit at (7, 7), open arena. The player must reason that B's Manhattan-dominant pursuit policy means the FIRST action determines whether B steps vertical (toward C's reach, triggering M2 at turn 1) or horizontal (away from C, leading to A being caught). Only RIGHT-first preserves the vertical-pull condition. Witness `[4,4,4,4,4,4,4,2,2,2,2,2,2,2]` — 14 actions. |
| 3 | M3: A-eats-C on entry. | A at (0, 0), C₁ at (1, 0), C₂ at (1, 7), B at (4, 4), wall at (0, 1), exit at (7, 7). A's only legal first move is onto C₁ (forces M3 turn 1). Naïve continued RIGHTs catch A at (4, 0) by turn 4. The player must RETREAT 3 steps west after advancing to (3, 0) to draw B's pursuit into C₂'s vertical pursuit range — defeats the greedy-toward-exit heuristic. M2 fires at turn 6 when C₂ lands on B at (1, 1). Witness `[4,4,4,3,3,3,4,4,4,4,4,4,4,2,2,2,2,2,2,2]` — 20 actions. |

## Win condition

When A's logical cell after a successful phase-0 move equals the
level's exit-cell coordinates (read from
`level.get_data("exit_cell")`), the game calls `self.next_level()`
(or transitions to `WIN` after L3). The win-check fires BEFORE
the B and C pursuit phases of the same turn, so A "snapping the
win" by stepping onto the exit cell takes precedence over any B
about to step onto A on the same turn.

## Lose condition

`self.lose()` fires in any of:

1. A walks onto a B-cell in phase 0 (A's destination is a B; A enters and is removed).
2. After phase 2 (all B's complete their full step), a B's new cell coincides with A's cell.
3. `self._steps_used >= self._max_steps` at the end of phase 4 (or on a phase-0 fast lose path).

## Internal state

- `self._steps_used: int` — private per-level action counter (NOT the engine's `_action_count`; private to avoid the implicit-RESET drain bug per `fix_implementation.md`'s canonical pattern).
- `self._max_steps: int` — read from `level.get_data("max_steps")` in `on_set_level`.
- `self._exit_cell: tuple[int, int]` — read from `level.get_data("exit_cell")`.
- `self._phase: int` — animation phase cursor 0..4. Reset to 0 on level start and at the end of each completed action.
- `self._b_pending: list[(Sprite, dx, dy)]` — planned B steps for the current action, computed at phase 0 and executed during phases 1, 2.
- `self._c_pending: list[(Sprite, dx, dy)]` — planned C steps, computed at phase 2 and executed during phases 3, 4.
- `self._step_bar: StepCounterHud` — bottom-row HUD widget.

## Notable code patterns

- **Five-phase per-action animation via a `self._phase` counter that short-circuits `complete_action()`.** Each ACTION1..4 enters phase 0, mutates A's position immediately, then schedules B's movements (phase 1, 2) and C's movements (phase 3, 4). The engine's `perform_action` loop calls `step()` repeatedly until `complete_action()` is invoked at phase 4, producing 5 distinct rendered frames per logical turn. Half-steps move sprites 4 px (`HALF_STRIDE`); full-steps complete the remaining 4 px to land on the next logical cell.
- **One shared pursuit policy parameterised by who-chases-whom.** Both B's (chasing A) and C's (chasing nearest B) use the same `_plan_step(mover_cell, target_cell, reserved, kill_target_tag)` helper, which computes the Manhattan-dominant cardinal step (tie → x) considering walls, grid bounds, and reserved destination cells (so multiple movers don't pile into the same target). The `kill_target_tag` parameter (only passed for C's call) lets C pass through B's cell, removing B; B's never use a kill tag and are simply blocked by C's.
- **Plan-then-animate separation.** Phase 0 computes A's move and plans B's intended steps without yet animating; phases 1, 2 then animate those planned steps. This separates intent-resolution (which respects mutual blocking and the kill rules) from frame-rendering (which only mutates pixel positions). The same pattern repeats at phases 2 (plan C) and 3, 4 (animate C).
- **`InteractionMode.REMOVED` for consumed/killed sprites.** A-eats-C (M3) and C-kills-B (M2) both set the consumed sprite's interaction to `REMOVED` rather than re-positioning off-grid or filtering by visibility, so the sprite stays in the level's sprite list for inspection but is hidden from rendering and collision.
- **Private `_steps_used` counter** (per `fix_implementation.md`'s canonical CHECK_LOSE_PATH_EXISTS pattern). Avoids the implicit-RESET "first-frame energy already lost" bug that arises when reading `self._action_count`.
- **Step-counter HUD as a horizontal drain bar.** `StepCounterHud(RenderableUserDisplay)` paints `frame[63, :]` left-to-right with palette-14 (green) for the filled portion and palette-4 (off-black) for the drained portion; updated in `_consume_step()` at the end of phase 4 of every action.
