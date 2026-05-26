# fz5j — phase-step-tile

## Summary
The player nudges a small green avatar through a corridor of cells, some of which are *phase tiles* that pulse open and closed on a fixed period (light-blue every 2 steps, magenta every 3, orange every 4). The avatar can only enter a tile during a step when the global step counter `t` satisfies `t % period == offset`. **Stepping into a closed tile costs a life and respawns the avatar at the level's start cell with the step counter reset to 0.** Walking into a wall is a free implicit-wait (no movement, no life lost, counter still ticks). Each level grants 3 lives; the level is lost when lives reach 0 OR the per-level step budget is exhausted. Win condition: reach the goal cell.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move avatar one cell up; rejected by walls (counter still ticks); rejected by closed phase tile (death + respawn). | always |
| ACTION2 | Move avatar one cell down; same rejection rules. | always |
| ACTION3 | Move avatar one cell left; same rejection rules. | always |
| ACTION4 | Move avatar one cell right; same rejection rules. | always |

(`available_actions=[1, 2, 3, 4]`. No click, no ACTION5/6/7. Wall-bumping is the implicit "wait" verb.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Avatar walk + period-2 phase-tile gate. | 1-cell corridor on row 5 (walls fill rows 1-4 and 6-14). Two period-2-offset-0 chokepoints at cols 5 and 10; the inter-tile walking distance is odd (5 cells) so direct walking arrives at the second tile on the wrong residue. **Witness `[4, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 4, 4]` (14 actions; ACTION1 at step 9 wall-bumps the row-4 wall to insert one wait so col 10 is entered at step 10).** |
| 2 | Adds period-3 phase-tile gate; corridor rotates from horizontal (L1) to vertical for diversity. | Vertical corridor in col 5 (walls fill all interior columns except col 5). Chokepoints at rows 5 (period-2-offset-0), 9 (period-3-offset-1), 12 (period-2-offset-1). Witness `[2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2]` (15 actions; two consecutive ACTION3 wall-bumps at row 8 to align row 9 with `t%3==1`; row 12 self-aligns at the resulting step parity). |
| 3 | Adds period-4 phase-tile gate AND a period-3 pair on adjacent cells. | L-shaped corridor: row 1 east to col 10, then south down col 10 to the goal. Five chokepoints — period-2 at (4,1), period-3 at (8,1), period-4 at (10,5), and a period-3 pair at (10,12) and (10,13) immediately adjacent. The adjacent pair locks both residues to a single arrival step at (10,12) — there's no room to insert a wait between them, so the entire upstream wait count must produce exactly the right arrival residue. Witness `[4, 4, 1, 4, 4, 4, 4, 1, 1, 4, 4, 4, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2]` (29 actions; 7 waits placed against perimeter / row-2 / bracket walls). |

## Win condition

After every successful move, if the avatar's new cell equals the goal cell, fire `self.next_level()`. The engine auto-fires `self.win()` after the last level's `next_level()`.

## Lose condition

Two predicates:
1. The step counter reaches the per-level `step_budget` at the end of any action.
2. After a death (closed-tile entry), the lives counter has dropped to zero.

There is no other lose state — every move into a closed tile spends one of the three lives but otherwise lets the player retry the level from the start cell.

## Internal state

- `_step_counter` (int): ticks per action attempt regardless of outcome; resets to 0 on respawn after death; phase-rule input.
- `_max_steps` (int): per-level budget loaded from `level.get_data("step_budget")`.
- `_lives` (int): starts at 3 each level, decremented on each closed-tile entry.
- `_level_start_cell` (tuple): respawn cell, loaded from `level.get_data("level_start_cell")`.
- `_phase_state` (dict): per-cell `(period, offset, open_sprite, closed_sprite)` resolved in `on_set_level`.
- `_step_counter_hud` (`StepCounterHud`): bottom-row depleting bar.
- `_lives_hud` (`LivesHud`): three pips along the top row that dim from red to off-black as lives are lost.

## Notable code patterns

- **Two-sprite-swap for periodic state**: each phase-tile cell pre-places both `*_open` and `*_closed` sprite variants at the same position; `_refresh_phase_tiles()` flips `InteractionMode.TANGIBLE`/`InteractionMode.REMOVED` per step based on `(step_counter % period) == offset`. Reusable for any "two-state cell that flips on a counter."
- **Open / closed pixel design**: open tiles are a period-coloured 4×4 frame with a transparent (palette -1) centre — the background shows through the hole, signalling "you may pass." Closed tiles paint a black palette-5 cross over both diagonals of the 4×4 cell while keeping the period colour on the off-diagonal cells; the diagonals are an unambiguous "do not enter" mark. Walls (solid palette-4) remain visually distinct from both states.
- **Respawn-on-death with counter reset**: `_respawn_avatar()` returns the avatar to `_level_start_cell`, sets `_step_counter` to 0, refreshes phase-tile rendering, and updates the step-counter HUD. Each life is a clean attempt at the temporal puzzle, not a partial-progress retry.
- **Wall-bump as implicit wait**: a move attempt against a wall (perimeter, interior wall_block, or `wall_frame` edges) is rejected without advancing the avatar, but the step counter still ticks. This gives the player a deliberate one-step wait verb without consuming an action slot. Crucially, walls and closed phase tiles are visually distinct, so the player can choose between safe-wait (wall-bump) and committed-walk (any open direction) every turn.
- **LivesHud**: three pips in the top pixel row, drawn directly into the frame by a `RenderableUserDisplay`, dimming from palette-8 (red) to palette-4 (off-black) as lives are lost. Sits visually on top of the perimeter wall — no playfield real-estate consumed.
- **Single big perimeter sprite (`wall_frame`)**: rather than placing 60 individual perimeter walls, a single 64×64 sprite with palette-4 perimeter and palette-(-1) interior covers all four edges. Interior walls are placed as small 4×4 `wall_block` sprites only where needed. Reduces per-level sprite-list verbosity.
