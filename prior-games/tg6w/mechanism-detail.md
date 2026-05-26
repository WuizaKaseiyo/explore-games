# tg6w — settle-pile-tilt

## Summary

Each arrow press sets the playfield's "down" direction; every loose **block** sprite slides simultaneously and multi-cell in that direction, animated one cell per engine tick, until obstructed by a wall, another block, or the playfield border. Coloured-rim walls (yellow-rim, orange-rim) are passable to blocks of the matching colour and full-blocking to all others. Red **hazard walls** kill any block whose slide enters their cell — the engine plays the entry frame, then fires `lose()`. The level wins when every block sits on a same-coloured target; loses when the step counter exhausts OR a hazard wall is touched.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | UP — set gravity vector to (0, -1); every loose block slides upward until obstructed | always |
| ACTION2 | DOWN — gravity (0, +1); every loose block slides downward until obstructed | always |
| ACTION3 | LEFT — gravity (-1, 0); every loose block slides leftward until obstructed | always |
| ACTION4 | RIGHT — gravity (+1, 0); every loose block slides rightward until obstructed | always |

`available_actions = [1, 2, 3, 4]` (pure cardinal motion; no click, no ACTION5 freedom slot, no undo). The directional input IS the distinctive verb (m0r0 / tr87 pattern).

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1: arrow-press = simultaneous slide-to-end of every loose block. | 7×7 lattice, 2 yellow blocks at lattice (1, 1) and (5, 1); 2 yellow targets at (1, 5) and (5, 5). No interior walls. Witness `[ACTION2]` — single DOWN press settles both blocks on their targets. Step budget 12. |
| 2 | + M2: coloured-rim walls passable to matching-colour blocks only. | Row-3 divider with `wall_rim_yellow` at (3, 3), `wall_rim_orange` at (5, 3), `wall_solid` elsewhere. Stop-wall at (4, 5). Yellow at (3, 1), orange at (5, 1); yellow target at (1, 5), orange target at (5, 5). Witness `[ACTION2, ACTION3]` — DOWN ferries each block through its own rim; LEFT nudges yellow alone (the (4, 5) stop-wall holds orange in place). Step budget 25. |
| 3 | + M3: red hazard walls — any block whose slide destination is a `wall_hazard` cell enters the cell visually then fires `lose()`. | Row-3 divider with `wall_rim_yellow` at (1, 3) and `wall_rim_orange` at (5, 3); other row-3 cells full-blocking. In the bottom row, between yellow target at lattice (3, 5) and orange target at lattice (5, 5), a 2-base-col `wall_grey_thin` at base (12, 15) and a 1-base-col `wall_hazard` at base (14, 15) — the grey wall blocks yellow's RIGHT slide so it settles at the (9, 15) target; the red wall sits one cell right of the grey wall as a deadly secondary hazard for any path that breaches the grey or arrives at base col 14. Yellow at (3, 1), orange at (5, 1). Witness `[ACTION3, ACTION2, ACTION4, ACTION2]` — LEFT positions yellow at column 1 (its rim column); DOWN sends yellow through (1, 3) rim to (1, 5); RIGHT slides yellow rightward — yellow stops at the yellow target (9, 15) because the grey wall at (12, 15) blocks further travel; final DOWN sends orange through (5, 3) orange-rim to (5, 5). Step budget 30. |

## Win condition

After every slide animation drains, evaluate `_check_win()`:

> Every block sprite occupies a cell at which a same-coloured target sprite is also positioned (sharing the colour-tag pair `block_yellow ↔ target_yellow`, `block_orange ↔ target_orange`).

If true, fire `self.next_level()`.

## Lose condition

After every slide animation drains:

- **Hazard contact (immediate)**: if any block's destination cell during the slide was a `wall_hazard` (red wall) sprite, the block enters that cell visually and `self.lose()` fires the same turn. This is the L3 distinguishing behaviour for M3.
- **Step exhaustion**: `self._steps_used >= self._step_budget` → `self.lose()`.

No irreversible soft-locks (the L1/L2 layouts have no irreversible state, and L3's only kill condition is hazard contact, which fires `lose()` immediately rather than leaving the player in a no-win waiting room).

## Internal state

- `self._step_budget: int` — current level's step budget (read from `level.get_data("step_budget")` in `on_set_level`).
- `self._steps_used: int` — actions consumed this level (private counter, NOT the engine's `self._action_count`, to avoid the RESET-counts-as-step bug).
- `self._step_counter_ui: StepCounterHud` — `RenderableUserDisplay` that draws the depleting yellow bar across frame row 0.
- `self._anim_queue: list[list[(Sprite, int, int)]]` — slide-animation frames waiting to play. Each frame is a list of per-block move tuples; `step()` pops one frame per engine tick.
- `self._hazard_pending: bool` — set during slide simulation when any block's destination cell is a `wall_hazard`. After the animation drains, `step()` fires `lose()` instead of the standard finalisation.

## Notable code patterns

- **State init before super().__init__()**: `NovaBaseGame.__init__` calls `set_level(0)` which calls `on_set_level`. Per-level state attributes (`_step_budget`, `_steps_used`, `_anim_queue`, `_hazard_pending`) are initialised on `self` BEFORE `super().__init__()` so the parent constructor's `set_level(0)` finds them already defined. Otherwise post-super initialisation overwrites the on_set_level-populated values, causing an immediate `lose()` on the first action with `_steps_used = 0 - 1 < 0`. (Same lesson recorded in lv4k and xn5p mechanism-details.)
- **Multi-block lockstep slide animation**: the slide simulator (`_compute_slide_animation`) runs against a snapshot of block positions, ticking one cell per frame; on each tick it orders blocks by slide direction (rightmost-first for RIGHT, etc.) so the block furthest in the direction commits first and trailing blocks see the new positions when checking collisions. Each block's per-tick move is recorded as a `(block, new_x, new_y)` tuple; the resulting frame list is consumed by `step()` one frame per engine tick, with `complete_action()` deferred until the queue is empty (the wt39 single-pawn pattern, generalised to multi-block lockstep).
- **Colour-permeable wall as a passable-tag check**: `_block_can_pass(block, wall)` reads tags on both sides — `wall_rim_yellow` is passable iff the block has tag `block_yellow`. The slide simulator never "stops at a permeable rim cell"; it treats the rim as empty for the matching colour and a full block for any other.
- **Hazard wall as an "enter then die" cell**: in `_compute_slide_animation`, a destination cell whose wall has tag `wall_hazard` is treated specially — the block is moved INTO the cell (so the player sees the entry frame as the last animation tick) and `hazard_triggered` flips True. `_resolve_after_animation` reads the flag once the queue drains and fires `self.lose()` in lieu of the normal win/budget check. This pattern lets the visual cue ("block touched the red bar") play on screen before the engine reports the loss.
- **Non-lattice-aligned thin wall placement** via the `_place_at(name, x, y)` helper: the L3 grey wall (2 base cols wide, base TL (12, 15)) and red hazard wall (1 base col wide, base TL (14, 15)) are positioned at exact base coords because they are narrower than the 3-cell lattice stride. This gives them the visual "thin bar between standard 3×3 sprites" reading from the user-supplied design sketch.
- **Layered rendering**: targets at layer 0, walls (incl. hazards) at layer 1, blocks at layer 3. The yellow target (donut outline at lattice (3, 5)) renders correctly even with the grey/red walls placed in adjacent base cells — neither wall overlaps the target sprite, and the block, when settled at the target, layers above it.
