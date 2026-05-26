# bw7k — actor-replay-shade

## Summary

A small avatar walks the grid one cell per arrow press, leaving a
faint off-white trail of dots behind it that records the cells
it has visited. Scattered on the board are coloured rune-pads
paired with same-coloured hollow rings. The first time the
avatar steps onto a rune-pad, a ghostly companion of the matching
colour appears at that pad and animates over the next several
turns, walking the same shape the avatar just walked but starting
from the pad's cell; the companion drops its own same-coloured
trail of dots as it goes, so the player can see both paths side
by side. A companion step blocked by a wall or grid-edge is
skipped (it stays in place that tick and the iteration moves on).
The level resolves when the avatar stands on its goal-frame and
every spawned companion stands on its same-coloured ring; a step
counter ends the level on a `lose()` if it empties first.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move actor up 4 pixels (one logical cell). Records the attempted vector `(0, -4)` to the move-tape regardless of whether the actor was blocked. | always |
| ACTION2 | Move actor down 4 pixels; records `(0, +4)`. | always |
| ACTION3 | Move actor left 4 pixels; records `(-4, 0)`. | always |
| ACTION4 | Move actor right 4 pixels; records `(+4, 0)`. | always |

(`available_actions=[1, 2, 3, 4]` — ACTION5/6/7 not used.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Walking + Anchor-spawn-shade + Shade-replays-tape (the base dynamic system, 3 mechanics). | Open arena along column x=12; actor walks straight up through anchor_red to actor_goal; the shade naturally lands at target_red two-anchor-distances above the spawn. Witness `[ACTION1] × 13`. |
| 2 | + Replay-walls (walls that cause the shade's replay to skip blocked moves). | The actor must walk a non-trivial path-shape (RIGHT×6 + UP×6 + LEFT×6 → anchor) so that, replayed from the anchor, the shade reaches `target_red` and the trailing LEFTs are skipped by the wall east of target. Witness `[ACTION4]×6 + [ACTION1]×6 + [ACTION3]×6 + [ACTION1]×7` (25 actions). |
| 3 | + Multi-shade simultaneity (two anchor-target colour pairs whose replay-tapes share a strict-prefix relationship from the same actor history). | Detour wall between anchors forces a DOWN-RIGHT-UP between-anchors path; the inserted moves appear in `shade_yellow`'s tape and a second replay-wall north-east of the second target skips a tail of RIGHTs so the trailing UP correctly seats the shade on `target_yellow`. Witness `[ACTION1]×6 + [ACTION2]×1 + [ACTION4]×8 + [ACTION1]×1 + [ACTION1]×8 + [ACTION3]×4` (28 actions). |

## Win condition

Plain English: the actor's grid cell equals the `actor_goal` cell, AND every spawned shade's grid cell equals its same-coloured target cell. Predicate evaluated at the end of each `step()` after the actor moves and any anchor-spawn-shade firing.

## Lose condition

Plain English: the per-level step counter `steps_remaining` reaches 0 without the win predicate being satisfied.

## Internal state

- `step_budget` / `steps_remaining`: per-level budget, initialised in `on_set_level` from `level.get_data("step_budget")`.
- `move_history: list[tuple[int, int]]`: the actor's per-level move-tape `T`. Each tick appends the attempted `(dx, dy)` (regardless of whether the actor was blocked).
- `spawned_anchor_names: set[str]`: names of anchors that have already been triggered and consumed (set to `InteractionMode.REMOVED`); prevents double-spawn on revisit.
- (No additional flags or counters — shade replay is resolved instantly on spawn via a single helper `_compute_replay_endpoint` that walks the entire current tape from the anchor's cell, applying skip-on-block per entry.)

## Notable code patterns

- **Tag-based sprite querying**: every per-frame lookup uses `level.get_sprites_by_tag(...)` (`actor`, `actor_goal`, `target`, `target_red`, `target_yellow`, `anchor`, `shade`, `shade_red`, `shade_yellow`, `wall`, `trail_actor`, `trail_shade`). No name-based lookups in the step path.
- **sp80-style animation via game-mode flag**: `self.mode` is `"actor"` (process input normally) or `"shade_replay"` (advance each active shade by one tape entry per `step()` call, do NOT call `complete_action()` so the engine re-renders and re-enters `step()` for the next animation tick; when every shade is exhausted, flip mode back to `"actor"` and `complete_action()`). Lets the player watch the shade walk the same shape they walked, rather than seeing it teleport to a final cell.
- **Trail-dot visualisation**: every actor move (and every successful shade-replay move) drops a small `trail_*` sprite at the cell entered, on layer -1 so the dots render behind interactive sprites. The actor's trail is off-white (palette 1); the red-shade trail is maroon (palette 13); the yellow-shade trail is orange (palette 12). This makes the recording-and-replay rule directly observable: the player sees their own dots being laid down as they walk, and the same-shape coloured dots being laid down by the shade.
- **Anchor consumption via `set_interaction(InteractionMode.REMOVED)`**: per the universal-scaffold "two-sprite swap" idiom, an anchor that has spawned its shade is set to `REMOVED` so it is hidden from rendering AND excluded from collision; visiting it again is a no-op.
- **Step-counter HUD as a row-63 depleting bar**: `StepCounterHud(RenderableUserDisplay)` draws palette-2 leading cells and palette-3 trailing cells along the bottom row, proportional to `steps_remaining / step_budget`. The HUD only decrements when the player has agency (in `"actor"` mode); shade-replay animation ticks are free.
- **Move-tape recorded on attempted-vector**: `move_history.append((dx, dy))` happens whether or not the actor's destination cell was free. Ensures the shade replay is deterministic given the player's input sequence — a blocked actor still emits a tape entry that the shade will encounter and itself skip.
