# bz3k — drift-impulse-cardinal

## Summary

bz3k ("Drift-Impulse Cardinal") puts a single avatar on a 64×64
playfield where its cardinal velocity `(vx, vy)` is persistent across
turns. Each arrow press is an *impulse* — a ±1 change to one velocity
component — followed by a per-axis slide (horizontal then vertical)
that moves the avatar by `vx` cells horizontally, then `vy` cells
vertically, one cell at a time with collision and trigger checks at
each step. The destination latches only when the avatar enters the
target cell with both velocity components exactly zero, so the
player must plan deceleration. One special tile refines the mechanic
later: a **cap-band** clamps speed to magnitude 1 on traversal. L2
places that cap inside a wall-column passage and starts the avatar
off-axis so the player must turn vertically before going through; L3
keeps the same toolset and sets it inside an open arena with sparse
scattered obstacle blocks plus one central blocker that splits the
direct east path — the player must shift the avatar's vy to detour
around the blocker before re-aligning onto the target row.
Velocity is surfaced visually by a trailing wake of pixels behind the
avatar plus a velocity-dot HUD widget in the top-right corner; walls
zero the matching velocity component on collision.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 (UP) | `vy -= 1`, then per-axis slide | always |
| ACTION2 (DOWN) | `vy += 1`, then per-axis slide | always |
| ACTION3 (LEFT) | `vx -= 1`, then per-axis slide | always |
| ACTION4 (RIGHT) | `vx += 1`, then per-axis slide | always |

ACTION5, ACTION6, ACTION7 are not used. ACTION7 is omitted because no
undo verb exists (per checklist 22 — slot 7 is strict-undo or absent).

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | drift-impulse + speed-zero target | Open arena. Avatar at center (8, 32); target at center (33, 32). Discover that arrows are impulses (not direct moves), and that targets latch only at vx=vy=0. **Witness** (10 actions): `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION3, ACTION3, ACTION3, ACTION3, ACTION3]` — symmetric east-ramp then west-decel. Step budget 30. |
| 2 | + velocity cap-band; off-axis start forces a turn | Internal wall column at x=32 with single passage; cap-band fills the passage (center (32, 32)). Avatar starts **south of the passage** at center (8, 44) so the player must build vy first to line up with the gap before drifting east through the cap. Target at (55, 32). **Witness** (21 actions): 8-impulse vy ramp `[↑, ↑, ↑, ↓, ↓, ↑, ↓, ↓]` lifts the avatar to y=32 with vy=0, then `[→×7]` rams to the cap-clamp at x=32, then `[→×6]` rams east into the boundary wall at the target row. Step budget 60. |
| 3 | + open-arena obstacle course (no new tile mechanic) | Open 64×64 chamber with the cap-band on the direct east path (center (28, 32)) and a central 8×8 wall blocker (top-left (38, 28)) on the avatar's direct line to the target — the player must shift the avatar's vy north or south to detour around the blocker before re-aligning onto the target row. Eight additional 5×5 wall blocks are scattered around the arena (off the natural path) to give an open-but-populated feel. The cap clamps speed at the chokepoint, then the player must thread the gap above (or below) the central blocker without the surrounding decorative obstacles, and finally return to y=30 with vx=vy=0 on the target cell. **Witness** (33 actions): `[→×9]` (drift through cap, ram the central blocker, settle at the west face) + `[↑↑↓↑↓↓]` (vy ramp north to detour above blocker) + `[→→→←←→→←←→←←]` (12 x-impulses past the blocker eastward, decelerating onto target column) + `[↓↓↑↓↑↑]` (vy ramp south back to target row, vy=0). Step budget 60. |

## Win condition

`(player.x, player.y) == (target.x, target.y)` AND `vx == 0` AND
`vy == 0`, evaluated at end-of-turn after the per-axis slide. Triggers
`self.next_level()`. The final level's `next_level()` call promotes
the engine to `GameState.WIN` automatically.

## Lose condition

Two predicates trigger `self.lose()`:
1. **Hazard contact** during a slide step.
2. **Step budget exhausted** (`_action_count >= step_budget`) without
   target latch.

## Internal state

- `self.vx: int`, `self.vy: int` — current velocity components.
- `self.player_sprite: Sprite` — handle to the active level's avatar
  (rebound each `on_set_level`).
- `self.wake_sprites: list[Sprite]` — INTANGIBLE wake-pixel sprites
  placed each turn behind the avatar; cleared at top of next `step()`.
- `self.hazard_pending: bool` — set during slide if avatar enters a
  hazard cell; consumed at end of `step()` to fire `self.lose()`.
- `self.step_hud: StepCounterHud` — bottom-row depleting bar.
- `self.velocity_hud: VelocityDotHud` — top-right 4×4 dot-cross widget
  that reads `(vx, vy)` magnitude per axis (capped at 2 dots per axis).

## Notable code patterns

- **Per-axis slide loop.** `_slide_axis(axis)` slides one cell at a
  time on the named axis (`x` or `y`), checking wall collision, cap-
  band, flipper, hazard, and (deferred) target at each step. Cap
  clamps the matching axis to ±1 and stops the slide; flipper negates
  both axes and stops the slide; wall zeroes the matching axis and
  stops; hazard sets `hazard_pending` and stops.
- **Center-cell trigger query.** `_check_trigger_at_center(gx, gy)`
  resolves cap/flipper/target via center-position alignment (sprite
  top-left + (2, 2) == query position), and hazard via bounding-box
  + non-transparent-pixel check. Avoids ambiguity from multi-cell
  visual sprites.
- **Wake-pixel lifecycle.** Cleared at the top of each `step()` (so
  every render reflects current-turn velocity only), rebuilt after
  the slide using INTANGIBLE clones placed on the level via
  `level.add_sprite`. Wake fans behind the avatar opposite the
  velocity direction; magnitude `|vx| + |vy|`.
- **Wall pixel-perfect collision.** Walls are TANGIBLE+collidable and
  use the engine's `Sprite.collides_with(...)` for pixel-perfect
  blocking, while cap/flipper/target/hazard sprites are INTANGIBLE
  (visual-only) so the avatar passes through them — game logic alone
  decides their effects via the center-cell query.
- **HUD widgets registered on the Camera.** `Camera(interfaces=[step_hud,
  velocity_hud])` — both widgets persist for the whole game; their
  state is reset in `on_set_level`.
