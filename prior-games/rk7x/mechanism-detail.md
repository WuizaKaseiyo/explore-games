# rk7x — live-switch-routing

## Summary
A small coloured courier walks the corridor network autonomously, one
cell per player action, with no direct input that steers it. Every
junction in the network has a clickable blade that selects which
outgoing corridor the courier takes on arrival. The player's only verb
is ACTION6: clicks on a junction toggle its blade between two states;
clicks on empty cells just tick the courier one cell (the implicit
"wait"). The courier must visit every coloured stop and reach a
matching coloured terminal before the per-level step budget runs out;
walking into a wall ends the level. Level 3 adds a second courier on a
disjoint corridor; both walk in lockstep on every click.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click at (x, y). On a junction sprite: swap its H/V twin pair. Then advance every courier one cell. | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Live switch routing — clicking a junction toggles its blade; the courier reads the blade as it enters and turns accordingly. | Default blade routes the courier into a stub wall; the player must toggle the single junction once before the courier arrives. **Witness:** click on the junction sprite once at any tick from 1-6, then 13 wait-clicks anywhere. |
| 2 | Adds coloured stops gating the win — the terminal is only "active" once every stop has been passed over. | Two south-detour loops, each with a single stop. Default blades route the courier straight along the artery, missing both stops; the player must toggle each detour's two junctions (entry + rejoin) to make the courier traverse both detours. **Witness:** four junction toggles (J1_in, J1_out, J2_in, J2_out) followed by the courier's natural walk through both detours and back to the terminal — about 32 actions total. |
| 3 | Adds a second courier of a different colour walking its own disjoint corridor in lockstep with the first. The conflict-cell rule (two couriers may not co-occupy) is enforced by the engine but is dormant on the witness path. | Both couriers' default routes walk into their respective row's terminating wall. Four junction toggles required: J_R_top to V to send red south, J_R_bot to H to deflect red east at the bottom, J_B_top to V to send blue north, J_B_bot to H to deflect blue east at the top. Coloured stops are placed on each courier's main path (no detour required at L3). **Witness:** four toggles (in any order before the relevant courier reaches its junction) plus ~17 ticks of walking — about 21 actions total. |

## Win condition

After every player action, every courier in the level must be on its
matching `terminal_<color>` cell AND every required `stop_<color>`
sprite must have been visited (its `stop_<color>_visited` twin must be
the currently TANGIBLE one of the stop pair).

## Lose condition

Three predicates, checked in order each tick:
1. **Wall hit** — any courier's new cell is a `wall_tile` cell.
2. **Conflict cell** (L3) — two couriers occupy the same cell after
   stepping. Implemented but the L3 layout uses disjoint corridors so
   this rule is not exercised by the witness path.
3. **Step budget exhausted** — `_action_count >= step_budget` without
   a win.

## Internal state

- `couriers`: list of TANGIBLE courier sprites in the current level
  (1 in L1/L2, 2 in L3).
- `directions`: dict mapping each courier sprite to its current
  walking vector `(dx, dy)`. Updated when a courier enters a junction
  or bend cell.
- `colors`: dict mapping each courier sprite to its colour name
  ("red"/"blue"); used to choose which stop tag and terminal tag to
  match against.
- `junction_tables`: dict keyed by `(grid_x, grid_y)` cell, mapping
  to `{"H": <pass_h dict>, "V": <pass_v dict>, "id": <int>}`. The
  `pass_h` and `pass_v` dicts map `came_from` direction (one of N, S,
  E, W) to `exit` direction.
- `bend_tables`: dict keyed by `(grid_x, grid_y)` cell mapping to a
  single `pass` dict (no toggle).
- `step_budget`: copied from level data on `on_set_level`.
- StepBarHud: a `RenderableUserDisplay` subclass painting a 32-pixel
  yellow-on-black bar at row 63 reflecting `actions_remaining /
  step_budget`.

## Notable code patterns

- **Two-sprite-swap idiom for state toggles.** Each junction is two
  twin sprites (`junction_h` + `junction_v`) at the same grid cell;
  one is TANGIBLE and the other REMOVED at any time. Clicking the
  switch swaps interaction modes via `set_interaction(...)`. Same
  idiom is used for stops (`stop_<color>` ↔ `stop_<color>_visited`).
- **Per-cell routing tables.** Junction and bend behaviour is encoded
  as a `dict[came_from, exit_dir]` looked up in `step()` whenever a
  courier's new cell is a junction/bend. Came_from is inferred from
  the courier's pre-move direction; if the lookup fails (no entry
  for that came_from in the current state), the engine treats it as
  a wall hit.
- **Scaled-grid trick.** `grid_size` is `(64, 64)` and sprites are
  4×4 pixel arrays placed at multiples of 4. This gives a 16×16
  *logical* cell grid where each cell renders as a 4×4 display
  block, while still allowing primary sprites (couriers, junctions,
  stops, terminals) to carry internal pixel patterns rather than
  uniform 1-cell solid blocks.
- **Bend sprite as terrain feature.** A third sprite type (`bend`)
  with a fixed routing table provides passive direction-changes at
  corridor corners. Bends are not toggleable and are not counted
  among the per-level mechanics — they're terrain, not a player
  verb.
