# nz3v — rotor-pivot-walk

## Summary

A central 2×2 rotor pillar at the centre of a 12×12 playfield projects a 90° "lit" angular sector that the player rotates manually via ACTION5. The player controls a 2×2 avatar with cardinal arrows; the avatar is **safe as long as at least one of its 4 footprint cells lies in the currently-lit sector** ("half on the dotted area"). The puzzle dynamic: walk the avatar to a sector boundary so its footprint straddles two quadrants, press ACTION5 to rotate the wedge, and continue walking — half of the avatar is always in the lit sector, allowing incremental traversal around the rotor to the target. **3 lives per level**: stepping/rotating into a position where all 4 footprint cells are dark respawns the avatar at the level start with one less life; running out of lives ends the run. L2 adds wall obstacles forcing a south-detour around the wedge boundary; L3 adds a counter-rotation switch that reverses ACTION5's direction, allowing one-quadrant travel toward an SW target instead of three.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move avatar one cell up; blocked by wall/rotor/out-of-bounds (action ticks, no move). | always |
| ACTION2 | Move avatar one cell down. | always |
| ACTION3 | Move avatar one cell left. | always |
| ACTION4 | Move avatar one cell right. | always |
| ACTION5 | Rotate the lit wedge one quadrant in the current direction (+1 clockwise default; -1 counter-clockwise after counter_switch). | always |

After every move or rotation, if every cell of the avatar's footprint is outside the lit sector, the avatar dies, the level state (rotor angle, direction) resets, and the avatar respawns at the per-level start. Lives decrement; reach 0 → `self.lose()`.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 = walk + ACTION5-rotate, 2×2 avatar straddles sector boundaries (single mechanic). | 12×12 grid, rotor at (5,5)–(6,6), avatar at (1,1), target at (10,10). 3 lives, step budget 32. Witness `[4,4,4,4,5,4,4,4,2,2,2,2,5,2,2,2,4,2]` (18 actions) walks east into NW/NE straddle at (5,1), rotates to NE, walks east+south to NE/SE straddle at (8,5), rotates to SE, walks south+east to (9,9) whose footprint includes the target (10,10). |
| 2 | + M2 = wall obstacles within sectors force south-detour through the NE quadrant. | Same start/target as L1; walls at (7,0), (7,1), (7,2) block direct east traversal at the top of the NE quadrant — the avatar must descend to gy=3 to pass at (6,3)→(7,3)→(8,3). 3 lives, step budget 36. Witness `[4,4,4,4,5,2,2,4,4,4,2,2,5,2,2,2,4,2]` (18 actions) routes through the gap. |
| 3 | + M3 = counter-rotation switch reverses ACTION5's direction. | Avatar (1,1), target (1,10) in SW. Walls at (2,7), (2,8), (2,9) block direct south at gx=2 in SW; counter-switch at (3,1) in NW reverses rotation so a single ACTION5 sends the wedge NW → SW instead of NW → NE. 3 lives, step budget 36. Witness `[4,4,2,2,2,2,5,2,2,2,2,2,3,3]` (14 actions) triggers the switch at action 1 (footprint covers (3,1)), descends to NW/SW straddle at (3,5), rotates (direction reversed: NW → SW), walks south past the walls, then west to the target. |

## Win condition

After every action (move or rotate), if any cell of the avatar's 2×2 footprint coincides with the target's cell, fire `self.next_level()`. The engine fires `self.win()` after L3's `next_level()`. Identical predicate at all 3 levels.

## Lose condition

`self.lose()` fires when the lives counter hits 0 (after a fatal step or fatal rotation that the respawn cannot recover) OR when the step counter exhausts (`_actions_taken >= _step_budget`).

A single "dark step" (where the avatar's full footprint sits outside the lit sector after a move or after a rotation) costs one life and respawns the avatar at the per-level start position with the rotor angle and direction also reset to defaults — but does not end the run while lives remain.

## Internal state

- `_rotor_angle ∈ {0, 1, 2, 3}` — current sector (NW/NE/SE/SW). Reset to 0 each level and on each respawn.
- `_direction ∈ {+1, -1}` — rotation direction applied by ACTION5; +1 default; toggled by counter_switch. Reset to +1 each level and on each respawn.
- `_lives` — starts at 3 per level; decremented on each dark-footprint death.
- `_step_budget`, `_actions_taken` — per-level countdown.
- `_avatar_start` — cached level-start position for respawn.
- `_spent_switches` — set of (gx, gy) for consumed switch tiles (visual remap + retrigger prevention).

## Notable code patterns

- **Avatar footprint as set membership**: every walkability / safety / win / switch check iterates over `_avatar_footprint(gx, gy)` which yields the 4 cells `(gx+dx, gy+dy)` for `dx, dy ∈ {0, 1}`. The same footprint primitive answers four questions (any-cell-blocked-by-wall, any-cell-in-lit-sector, any-cell-equals-target, any-cell-on-switch), keeping the per-action dispatch clean.
- **Player-driven rotation via ACTION5**: there is no auto-advancing rotation counter; pressing ACTION5 advances `_rotor_angle` by `_direction` (mod 4) immediately. The mechanic's tempo is entirely under the player's control, which removes the "wait for the right beat" gate of timing-based variants and replaces it with a "where do I rotate while standing on a straddle" puzzle.
- **Wedge-as-textured-overlay**: `WedgeOverlay(RenderableUserDisplay)` paints a 4-corner-dot + centre pattern at the cell-rendered position of every cell in the current lit sector, tinting only `BACKGROUND_COLOR` pixels so sprites placed in the sector retain their pixel detail.
- **Rotor direction-marker pixel**: `RotorDirectionMarker(RenderableUserDisplay)` paints one palette 6 (magenta) pixel at the rotor's clockwise-next-corner (or counter-clockwise-next-corner if direction reversed) — surfaces the otherwise-hidden direction state at every frame.
- **Three-pip lives HUD**: `LivesHud(RenderableUserDisplay)` paints 3 small palette 8 (red) pips at the top-left of the frame; pips dim to palette 4 as lives are spent. Visible across all levels.
- **Respawn-on-death with state reset**: when a death is detected, `_start_death_animation` sets `_death_anim_phase = 0` and the step handler RETURNS WITHOUT calling `complete_action`. The novaengine's `perform_action` loop drives `step()` repeatedly (rendering one frame per loop iteration) until `complete_action` fires, so the multi-tick death animation runs entirely inside the player's fatal action — telling the player what happened before the level resets. Once the animation completes, `_respawn_avatar` returns the avatar to `_avatar_start`, resets `_rotor_angle = 0`, resets `_direction = 1`, restores any consumed counter_switch sprites, and re-shows the avatar.
- **Multi-phase death animation (15 frames per death)**: phases 0–5 flicker the avatar (`set_visible(phase % 2 == 0)`) so the player sees their controlled sprite blink in place before disappearing; phase 6 holds the avatar invisible for one tick to mark the "gone" moment; phases 7–11 flicker the dying life-pip in `LivesHud` (alternating palette 8 → palette 4 — the pip-flicker rendering reads `game._death_anim_phase` directly to draw the dying pip's alternate state); the final flicker tick (phase 11) decrements `_lives` so the pip stays visibly empty from phase 12 onward; phase 12 holds the empty state one more tick; phase 13 calls `_respawn_avatar` and `complete_action`. If `_lives` drops to 0 at the decrement, `self.lose()` is called instead of respawning, ending the run.
