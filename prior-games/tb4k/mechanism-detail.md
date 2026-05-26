# tb4k — tumble-block-stand-fall

## Summary

The player controls a 1×1×2 brick on a tiled floor. Cardinal arrow
presses tumble the brick end-over-end one move at a time; the brick
has three footprint states — **standing** (1-cell), **lying
horizontal** (1×2 east-west), and **lying vertical** (2×1
north-south) — that alternate deterministically with each tumble.
The win condition is to bring the brick to rest in the **standing**
state exactly on the level's goal cell. Hole tiles destroy the
brick if any part of its footprint coincides with them (3 lives per
level, with respawn at start); narrow 1-cell-wide bridges flanked by
holes force the player to keep the brick standing or lying *along*
the bridge axis when crossing.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Tumble UP (north). Standing→lying-v; lying-v→standing 2 cells north; lying-h→lying-h one row north. | always; off-grid destination silently no-ops (step still counts). |
| ACTION2 | Tumble DOWN (south). Mirror of ACTION1. | as above |
| ACTION3 | Tumble LEFT (west). Mirror of ACTION4. | as above |
| ACTION4 | Tumble RIGHT (east). Standing→lying-h; lying-h→standing 2 cells east; lying-v→lying-v one column east. | as above |

`available_actions = [1, 2, 3, 4]`. No ACTION5/6/7.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 (tumble) — base dynamic system | Tutorial: brick starts standing at Bloxorz cell (3, 3), goal at (11, 11). Solid floor; no hazards. Witness `[ACTION4]×8 + [ACTION2]×8` (K=16, D=2 — alternating standing↔lying parity reaches the goal in exactly 16 tumbles). Step budget 40. |
| 2 | + M2 (hole hazard + lives, +1) | Holes at cells (7,3), (8,3), (9,3), (8,4), (7,5)-(11,5) block the direct east route and the south mid-detour. Brick starts standing (2, 4), goal at (14, 4). 3 lives per level; HUD shows 3 life pips top-right; on hole-fall the brick respawns at start and a pip vanishes. Witness `[ACTION4]×4 + [ACTION1]×2 + [ACTION4]×4 + [ACTION2]×2 + [ACTION4]×4` — north mid-detour, K=16, D=3. Step budget 60. |
| 3 | + M3 (narrow bridge, +1) | Middle column-band cx ∈ [6..9] is entirely holes except a 1-cell-wide bridge at y=3. Brick starts standing (2, 5), goal at (12, 1). Crossing the bridge requires east-only tumbles on cx ∈ [6..9]; lying N-S overhangs into flanking holes and dies. Composes M1 + M2 + M3. Witness `[ACTION1]×2 + [ACTION4]×4 + [ACTION4]×4 + [ACTION1]×2 + [ACTION4]×2` (K=14, D=2). Step budget 70. Trivial greedy heuristic (climb to y=1 first) dies on (6, 1) hole. |

## Win condition

After every action: `brick_state == "standing" AND brick_cell ==
goal_cell`. If true, fire `self.next_level()`. The check fires after
the tumble has been applied and after the hole/lives logic has been
evaluated.

## Lose condition

Two paths to `self.lose()`:
1. **Lives exhausted**: a hole-fall decrements lives_remaining; if
   the counter hits 0, `self.lose()` fires.
2. **Step budget exhausted**: at the top of every `step()`, if
   `_action_count >= step_budget`, `self.lose()` fires.

L1 has no hard-death path (no holes; off-grid tumbles silently
no-op); only the step-budget path is reachable on L1. L2 and L3
have both paths.

## Internal state

- `brick_state: str` — one of `"standing"`, `"lying_h"`, `"lying_v"`.
- `brick_cell: tuple[int, int]` — anchor cell (standing: the single
  cell; lying_h: west cell; lying_v: north cell).
- `start_cell: tuple[int, int]` — per-level respawn position.
- `goal_cell: tuple[int, int]` — win predicate target.
- `hole_cells: set[tuple[int, int]]` — pre-cached hole positions
  loaded in `on_set_level`.
- `lives_remaining: int` — per-level life count (3 for L2/L3, 0 for
  L1).
- `step_budget: int` — per-level step budget (40/60/70).
- `_brick_standing`, `_brick_lying_h`, `_brick_lying_v: Sprite` —
  references to the three brick variants for `set_interaction`
  swapping.
- `_life_pips: list[Sprite]` — references to the 3 HUD pip sprites,
  removed one-by-one on death.

## Notable code patterns

- **Three-sprite state machine for the brick.** All three variants
  (standing/lying_h/lying_v) are placed in the Level constructor
  at the start cell; at any moment exactly one has
  `InteractionMode.TANGIBLE` while the other two are `REMOVED`.
  Tumbling means computing the new state + anchor, swapping
  interactions, and `set_position` on the now-tangible variant.
- **State-alternating tumble rule.** Per-direction lookup tables map
  each `(state, direction)` pair to the new `(state, anchor)`:
  - Standing + E → lying_h at (cx, cy).
  - lying_h + E → standing at (cx+2, cy).
  - lying_v + E → lying_v at (cx+1, cy).
  Bloxorz's "tumble parity" — standing positions reachable by N or E
  tumbles share the start cell's parity — falls out naturally.
- **Per-level data dict drives parameters.** Each Level declares
  `data={"start": (cx, cy), "goal": (cx, cy), "step_budget": N,
  "lives": 3}`; `on_set_level` reads with `level.get_data(...)`.
- **HUD via two channels.** Step counter is a single
  `RenderableUserDisplay` subclass painting row 0 of the frame
  (depleting bar); life count is three `life_pip` sprites placed at
  Bloxorz row y=0 (top edge) and selectively `REMOVED` on death.
- **Bounds reservation of HUD row.** Tumble bounds check enforces
  `1 ≤ cy ≤ 15` so the brick can never enter the HUD row at y=0,
  avoiding visual collision between the brick and the life pips.
- **Hard-death + respawn loop.** A single `_hard_death` helper
  decrements lives, removes the rightmost pip via `set_interaction
  (REMOVED)`, then either calls `self.lose()` (if 0 lives left) or
  `_respawn_brick()` (restores standing state at start_cell).
