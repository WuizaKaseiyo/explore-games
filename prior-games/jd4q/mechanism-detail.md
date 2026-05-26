# jd4q — echo-trail-teleport

## Summary
The player walks an avatar through a stride-4 maze on a 64×64 grid.
Every cell the avatar leaves becomes a fading **echo-stone** (yellow
plus-pattern) that lasts 12 subsequent steps. Clicking any visible
echo teleports the avatar back to that cell and consumes that echo
plus every echo deposited after it. **Closing-doors** are one-way
passages that seal into walls the moment the avatar leaves them —
introduced from L1, they trap the avatar after a pickup and force
the player to discover the click-on-echo mechanic. **Eraser** cells
wipe the entire trail when entered (introduced at L2). **Anchor
cells** deposit a permanent (non-fading) echo when walked over,
providing a teleport target that survives long detours (introduced
at L3). Win condition is per-level: collect required pickups then
stand on the goal cell; running out of step budget loses.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Walk avatar one cell up | not blocked by wall / sealed door |
| ACTION2 | Walk avatar one cell down | not blocked by wall / sealed door |
| ACTION3 | Walk avatar one cell left | not blocked by wall / sealed door |
| ACTION4 | Walk avatar one cell right | not blocked by wall / sealed door |
| ACTION6 | Click — if click cell holds an echo, teleport avatar there and consume that echo + all later echoes | echoes_active per-level data |

`available_actions=[1, 2, 3, 4, 6]`. ECHO_LIFESPAN = 12 steps.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Walk + echo-teleport + closing-doors (base system) | Tiny layout: avatar east through 3 closing-door cells to pickup_a; doors seal; the only way back is to click the visible yellow echo at S; then walk south to goal. Witness ~13 actions. step_budget=30. |
| 2 | + eraser | Two pickups in two closing-door dead-end branches at junction J; the path from J to goal passes through an eraser cell that wipes the trail. The witness teleports back to J via S→J echoes after collecting each pickup, then walks J → eraser → goal. Witness ~28 actions. step_budget=80. required_pickups=["pickup_a","pickup_b"]. |
| 3 | + anchor cell (deposits a permanent echo) | Three pickups in two branches: branch B (east) is a 6-door corridor to pickup_b; branch A (south, gated by an eraser at its entrance) is a 5-door corridor to pickup_a, then a tail floor that passes pickup_c on the way to the goal. With `echo_lifespan=6`, regular echoes from S→J fade by the time the avatar reaches K_B — the only surviving teleport target is the permanent echo deposited when walking over the anchor cell on the S→J path. After clicking the anchor and walking back to J, committing to branch A walks the avatar through the eraser, which wipes the anchor too — so the avatar is forced forward through the sealing doors to K_A, then K_C, then the goal. Going branch A first traps the player: the eraser destroys the anchor, branch A's doors seal behind, and K_B becomes unreachable (no echoes for teleport, branch B's path is past J which is now beyond a sealed corridor). Witness ~28 actions. step_budget=100. echo_lifespan=6. required_pickups=["pickup_a","pickup_b","pickup_c"]. |

## Win condition

After every action: if the avatar's current cell holds a `goal`-tagged
sprite AND every name in the level's `required_pickups` list is in
`self.collected_pickups`, fire `self.next_level()`. Engine
auto-calls `self.win()` after the final level.

## Lose condition

If `self._action_count >= step_budget` (per-level data), fire
`self.lose()`. No instant-fail collision.

## Internal state

- `self.avatar`: the player sprite.
- `self.echoes`: ordered list of `(sprite, age, cell_xy, permanent)`
  quadruples in deposit-order. Permanent echoes (deposited via
  walking off an anchor cell) skip aging.
- `self.collected_pickups`: `set[str]` of pickup-sprite names visited.
- `self.step_counter_ui`: `StepCounterHud` `RenderableUserDisplay`
  drawing a depleting bar at `frame[0, :]`.

## Notable code patterns

- **Two-sprite-swap for closing-doors**: `door_open` (light-blue
  interior, `closing_door` tag, collidable=False) is replaced by
  `door_sealed` (black interior, `wall` tag, collidable=True) when
  the avatar exits its cell. Sealed doors share the `wall` tag so
  `_cell_blocked` queries them via the same loop as static walls.
- **Permanent-vs-fading echoes via per-echo flag**: each entry in
  `self.echoes` carries a `permanent` boolean. `_age_and_prune`
  skips permanent entries; `_deposit_echo(... permanent=True)`
  uses the `echo_anchor` sprite (red-corners-on-yellow) to render
  visually distinct from regular yellow `echo` sprites.
- **Anchor cells delegate to the egress code**: a normal-floor
  cell tagged `anchor_floor` causes `_handle_egress` to flag the
  deposited echo as permanent. No new ACTION needed; the mechanic
  composes with the existing walking system.
- **Eraser fires on ingress** (`_handle_ingress`): walking ONTO an
  eraser-tagged cell wipes the entire trail (regular AND permanent
  echoes). This composes with the closing-doors mechanic to force
  visit-ordering at L3 — the eraser-branch must be last.
- **Click-teleport consumes-and-truncates**: `_handle_click` finds
  the index of the clicked echo in `self.echoes` and slices
  `[:i]` to keep the prefix; every echo deposited after the
  clicked one is removed. Models the "rewind to this point"
  semantic cleanly.
