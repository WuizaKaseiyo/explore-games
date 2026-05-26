# dj5h — pulley-pair-platform

## Summary

The player controls a small humanoid avatar walking left-right across a chain of floor islands separated by pits. Suspended overhead from a horizontal beam hang one or more pulley wheels, each with a pair of coloured rectangular platforms attached to ropes on its two sides — the platforms are coupled by rope-length conservation, so toggling a wheel inverts both at once (one rises HIGH while the other falls LOW). The primary actions are walking with the arrows, clicking a wheel to make it the active pulley, and pressing the freedom action to toggle the active pulley's binary state. The win condition is to reach a goal cell on the level's far side, sometimes by walking on a LOW bridge platform, sometimes by riding a platform from LOW to HIGH while standing on it. The key constraint is the step counter at row 63, which decreases per action and triggers a lose if it reaches zero.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Walk avatar 4 px in -y | always; rejected if destination cell isn't walkable |
| ACTION2 | Walk avatar 4 px in +y | always; rejected if destination cell isn't walkable |
| ACTION3 | Walk avatar 4 px in -x | always; rejected if destination cell isn't walkable |
| ACTION4 | Walk avatar 4 px in +x | always; rejected if destination cell isn't walkable |
| ACTION5 | Toggle the active pulley (and cable-coupled partner if any); both platforms swap HIGH↔LOW; if avatar's foot was on a moved platform, avatar rides with it | excluded from `_get_valid_actions()` when no pulley is active |
| ACTION6 | Click at (x, y); if cell hits any wheel's 5×5 footprint, that wheel becomes the active pulley | always; click outside any wheel is a no-op |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 walk + M2 click-pulley + M3 toggle (base dynamic system) | One pulley with a red platform and a blue platform. Avatar must click PA, ACTION5 to drop red to LOW, walk onto red, then ACTION5 again to ride red up to the goal at HIGH. Witness: `[ACTION6@(30,7), ACTION5, ACTION4, ACTION4, ACTION4, ACTION4, ACTION5]` (6 actions; step budget 30). |
| 2 | + M4 peg-pickup-and-socket-drop | One pulley starts at LEFT_LOW (no bridge). Avatar must click PA + ACTION5 to bring blue platform to LOW for the A→B bridge, walk onto B, pick up the red peg at col 19, walk further along B to drop it on the red socket at col 27 (wall on cols 32-35 removes), then walk past the removed wall to D's goal. Witness: `[ACTION6@(10,7), ACTION5, ACTION4 ×14]` (16 actions; step budget 80). |
| 3 | + M5 opposite-phase cable coupling | Three pulleys; PA and PC are cable-coupled in opposite phase. Avatar walks A → PA-blue (initial bridge) → B (picks up blue peg at col 19) → walks LEFT back across PA-blue → drops peg on PA-blue socket at col 11 (wall removes). Walks forward across B → PB-blue-clone → C → past the removed wall → onto PC-red at LOW. Click PC + ACTION5 fires the cable-toggle: PC-red rises HIGH carrying the avatar to the goal at (57, 13); PA flips simultaneously. Witness: `[ACTION4 ×4, ACTION3 ×2, ACTION4 ×13, ACTION6@(58,7), ACTION5]` (20 actions; step budget 150). |

## Win condition

`next_level()` fires at the end of any `step()` when the avatar's foot pixel cell `(avatar.x + 1, avatar.y + 2)` falls inside the goal_marker's 3×3 footprint. After L3, the engine resolves to `WIN`.

## Lose condition

`lose()` fires at the start of `step()` if `_action_count > step_budget`. Pit cells are unwalkable rather than fatal — moves into pit are rejected without the avatar falling in.

## Internal state

- `self.active_pulley` — name (e.g. `"PA"`) of the currently-selected pulley, or `None`. Surfaced via `pulley_halo` set to TANGIBLE on the active wheel.
- `self.pulley_state` — per-pulley dict mapping pulley name → `"LEFT_HIGH"` or `"LEFT_LOW"`. Surfaced via the platforms' rendered y-positions.
- `self.pulley_cfg` — per-level configuration of pulleys (wheel position, platform x-positions).
- `self.cable_pairs` — list of `(pulleyA, pulleyB, phase)` tuples set per-level. Surfaced via `cable_segment` polylines along the beam.
- `self.carrying` — colour of the peg currently carried by the avatar, or `None`. Surfaced via the `avatar` ↔ `avatar_carry_<colour>` interaction-mode swap.
- `self.seated_pegs` — set of socket names whose pegs have been seated. Surfaced via the socket's recolour and the bound wall's REMOVED interaction.

## Notable code patterns

- **Step counter HUD widget.** `StepCounterHud(RenderableUserDisplay)` overrides `render_interface(frame)` to paint row 63 with palette-12 / palette-4 cells proportional to remaining budget; it reads `level.get_data("step_budget")` against `self._game._action_count`.
- **Pulley toggling drives both platforms + ridable avatar.** `_toggle_active_pulley` flips the active pulley's state, propagates through any cable-pair, then `_ride_platforms` checks whether the avatar's foot was on a pre-toggle LOW/HIGH platform and updates `avatar.y` to the new platform's row. Avatar variants (`avatar_carry_*`) are kept in sync by `_sync_avatar_variant`.
- **Two-sprite swap idiom for avatar carrying.** Four avatar sprite variants (`avatar`, `avatar_carry_red/blue/green`) live in the level; toggling between TANGIBLE and REMOVED produces the visible head-tint cue without moving sprites around.
- **Hidden floor under a wall.** Floor blocks at the wall's columns are placed normally; the wall renders on top (higher layer). When the wall's `interaction` is set to REMOVED on peg-drop, the floor underneath becomes visible AND walkable (the wall-collision check skips REMOVED walls).
- **Cable-pair coupling.** `cable_pairs` is a list of `(A, B, phase)`; a single ACTION5 propagates across linked pulleys preserving their phase relation. Opposite phase is encoded by initial-state choice (PA = LEFT_HIGH, PC = LEFT_LOW); a simultaneous flip preserves the inverted relation.
