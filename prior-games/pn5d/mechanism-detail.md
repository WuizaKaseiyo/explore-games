# pn5d — vessel-equalize-flow

## Summary
A horizontal row of open-top vessels stands on the playfield, joined at their bases by toggleable valves. The player slides a yellow ring-cursor between vessels (ACTION3/4), presses the pour key (ACTION5) to add one liquid unit to every vessel in the cursor's currently-connected group, and clicks valves (ACTION6) to flip their open/closed state and re-partition the connectivity. Each vessel has a red inward target pip on its right wall; a vessel may also have an outward orange overflow lip on its left wall, capping its surface regardless of how high the rest of the connected group rises. Win when every vessel's surface matches its target; lose when the bottom step bar runs out.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION3 | Move pour-cursor LEFT one vessel (decrement `_cursor_index`, clamped at 0). | Always valid; consumes 1 step. |
| ACTION4 | Move pour-cursor RIGHT one vessel (increment `_cursor_index`, clamped at `len(_vessels)-1`). | Always valid; consumes 1 step. |
| ACTION5 | Pour 1 height-unit into every vessel of the cursor's currently-connected group. After the rise, every vessel with an `overflow_cap` clips its surface to the cap row. | Always valid; consumes 1 step. |
| ACTION6 | Click `(x, y)` (display pixels). Convert via `camera.display_to_grid(int(x), int(y))`. If the resolved cell is a valve sprite (and not fixed), swap its `valve_open`/`valve_closed` siblings via `set_interaction(InteractionMode.{TANGIBLE, REMOVED})`. Otherwise no-op. | Always offered; consumes 1 step. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 pour-and-equalize (base mechanic) | 2 vessels A, B with one fixed-open valve. Targets A=B=4. Step budget 12. Witness `[ACTION5, ACTION5, ACTION5, ACTION5]` — 4 pours raise both vessels through the fixed-open connection. |
| 2 | + M2 valve-toggle (one-or-more new) | 3 vessels A, B, C with 2 toggleable valves both initially open. Targets A=3, B=2, C=5 (distinct heights). Step budget 18. Witness `[ACTION5, ACTION5, ACTION6@(24,19), ACTION6@(34,19), ACTION5, ACTION4, ACTION4, ACTION5, ACTION5, ACTION5]` — 2 merged pours up to B's target, then 2 toggles to isolate, then per-vessel pours via cursor moves. |
| 3 | + M3 overflow-cap | 4 vessels A, B, C, D with 3 toggleable valves all initially closed. C carries an overflow cap at row 2. Targets A=B=D=9, C=2. Step budget 20. Witness `[ACTION6@(20,19), ACTION6@(31,19), ACTION6@(42,19), ACTION5×9]` — 3 toggles merge all 4 vessels, then 9 pours raise A, B, D to 9; C's cap clips its surface to 2 from the third pour onward. The closed-valve fallback costs 32 actions (over budget); only the merge-then-cap-absorbs strategy fits. |

## Win condition

After every committed action, check `all(v["level"] == v["target"] for v in self._vessels)`. If every vessel's current surface equals its target, fire `self.next_level()`. L3's terminal `next_level()` triggers the engine's automatic `self.win()`.

## Lose condition

Single fail mode: if `self._action_count >= self._max_steps` and the win predicate is False, fire `self.lose()`. Checked AFTER the win check on each action so that the final-action-completes-the-puzzle case wins instead of losing. No hazards, no soft-lock states.

## Internal state

- `_cursor_index: int` — index 0..N-1 of the vessel under the pour-cursor.
- `_max_steps: int` — per-level step budget read from `level.get_data("max_steps")`.
- `_vessels: list[dict]` — one entry per vessel with the live `outline_sprite`, `fill_sprite`, current `level`, `target`, `cap`, `x`, `y`, and `cursor_x`.
- `_valves: list[dict]` — one entry per valve with the live `open_sprite`, `closed_sprite` (or None for fixed valves), `is_open`, `left_index`, `right_index`, and `fixed` flag.
- `_step_bar: StepCounterHud` — the registered `RenderableUserDisplay` widget rendering the bottom-row energy bar.

## Notable code patterns

- **Two-sprite swap for valve state.** Each toggleable valve holds both a `valve_open` and `valve_closed` sprite at the same grid position, with one `TANGIBLE` and the other `REMOVED`. Toggling flips the pair's interaction modes — the same idiom used by kx14 for ball-anchor swapping. Cleaner than `set_visible(False)` because collision is also gated.
- **Connected-group BFS via valve adjacency.** A small `_connected_group(start_index)` helper walks the valves list, following only those with `is_open == True`, to compute which vessels rise on a pour. O(V + E) per call where V = vessel count and E = valve count — both ≤ 4 in this game.
- **Pixel-mutated fill sprite as the liquid surface.** Each vessel's `liquid_fill` sprite is 6×12. After every pour, `_update_fill` rebuilds the pixel array via `np.full((12, 6), -1)` and sets the bottom `level` rows to palette 10 (light-blue). Cheaper than maintaining N row-strip sprites; matches kx14's pixel-mutated water-sprite idiom.
- **Per-level data dict for parameterisation.** Each `Level(...)` declares `data={"max_steps": N, "vessels": [...], "valves": [...]}`; `on_set_level` reads them via `level.get_data(...)` and reconstructs `_vessels` / `_valves` by tag-querying the cloned level's sprites. Adding a new level needs only one new dict entry.
- **Camera viewport defaults to grid_size.** All three levels use `grid_size=(64, 64)` so no per-level camera resize is required; the default 64×64 viewport matches the playable area.
