# nh4w — arc-loft-shot

## Summary
The player walks a small launcher pawn left and right along the floor of a 64×64 playfield with arrow keys (only ACTION3/ACTION4 are bound — there is no vertical movement). Clicking any cell with ACTION6 fires a yellow projectile that travels in a discrete parabolic arc from the launcher's muzzle to the clicked cell; the arc's peak height equals one third of the horizontal click-distance, so short shots fly low and long shots fly high. Brick walls standing on the floor block any arc whose peak altitude at the wall's x-band is too low; hanging grey stalactites with maroon dripping tips block any arc whose peak altitude is too high to fit under them. Each level wins when every coloured target square on the floor has been hit by a landed projectile.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION3 | Walk launcher 4 px LEFT (`launcher.x -= 4`); blocked if new position would overlap a wall sprite or fall off the playfield. | always callable; effect may be no-op if blocked |
| ACTION4 | Walk launcher 4 px RIGHT (`launcher.x += 4`); blocked symmetrically. | always callable; effect may be no-op if blocked |
| ACTION6 | Click cell `(cx, cy)` → spawn projectile at the launcher's muzzle origin `(launcher.x + 2, 50)` and animate it along a parabolic arc to landing-x = `clip(cx, origin_x ± 48)` (max range 48 px). Per-frame collision check against walls and ceilings; if any non-transparent projectile pixel coincides with a non-transparent wall/ceiling pixel, the projectile fizzles at that frame. If the arc reaches the landing cell unobstructed and the projectile sprite overlaps a target sprite's footprint, that target is consumed. | always callable; the multi-frame animation does not consume additional agent actions (engine ticks `step()` repeatedly until `complete_action()` resolves on the final flight frame) |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Walk + click-fire (M1, M2). Single yellow target out of 48-px arc range from the start; player walks one step right then clicks the target. | Witness `[ACTION4, ACTION6@(56, 51)]` (2 actions). Step budget 15. |
| 2 | + Wall-clearance rule (M3). 8-px-tall brick wall stands between the launcher's reachable positions and the target; only the launcher x where the arc's peak is high enough at the wall's x-band AND the click-distance is within range gives a winning shot. | Witness `[ACTION4, ACTION4, ACTION6@(62, 51)]` (3 actions). Step budget 25. |
| 3 | + Ceiling-block rule (M4). Two stalactites + two targets; yellow target reachable only from x=8 (where the shorter-distance arc just clears the wall and stays under ceiling1); blue target reachable only from x=12 (where the longer-distance arc clears the wall and tucks under ceiling2). The trivial heuristic "fire both shots from the same launcher position" fails — no shared x works for both targets. | Witness `[ACTION4, ACTION6@(40, 51), ACTION4, ACTION6@(52, 51)]` (4 actions). Step budget 35. |

## Win condition
After every projectile flight resolves, if the projectile landed (no mid-flight collision) on a target sprite's footprint, that target is removed from the level. When `len(self.targets) == 0`, fire `self.next_level()`. The engine auto-fires `self.win()` after L3's `next_level()` since L3 is the last entry in `levels`.

## Lose condition
`self._step_remaining` decrements by exactly 1 on every walk action and on the LAST frame of every fire-arc flight. If `self._step_remaining <= 0` and at least one target is still on the level, fire `self.lose()`. There is no soft-lock state — the player can always continue submitting actions until the budget runs out.

## Internal state
- `self.launcher` — the launcher sprite for the current level (captured in `on_set_level` via `level.get_sprites_by_tag("launcher")[0]`).
- `self.walls`, `self.ceilings`, `self.targets` — captured per-level via tag-based queries.
- `self.projectile` — the in-flight projectile sprite (None when idle).
- `self.flight_phase` — `-1` when idle; `>= 0` indexes the next path-frame to render during animation.
- `self.flight_path` — pre-computed sequence of `(x, y)` pixel positions the projectile will visit, built at `_begin_flight` time.
- `self.flight_target_sprite` — the target the projectile will consume if it lands successfully.
- `self.flight_collision_index` — frame index of the first collision, or None if the arc reaches the landing cell.
- `self._step_max` / `self._step_remaining` — per-level step budget tracking.
- `self._step_counter_ui` — `StepBarHud` widget rendering the green→red bar in row 0.

## Notable code patterns
- **Per-pixel collision against tapered sprites.** Bbox collision is too pessimistic against the tapered stalactite shape (the wide-trunk-narrow-tip silhouette has a large bbox but most of its bottom rows are transparent). Per-pixel collision iterates each non-transparent projectile pixel and each blocker pixel at the same world coordinate, returning True only on actual pixel overlap. Reusable for any game with non-rectangular obstacle sprites.
- **Pre-computed flight path with deferred animation.** `_begin_flight()` walks the entire arc trajectory once, computing per-frame `(x, y)` pixel positions and detecting collisions/landings up front. Then `step()` simply advances `flight_phase` one frame per engine tick, moving the projectile sprite along the precomputed path. `complete_action()` is called only on the final frame (collision OR end-of-arc), matching the sk48/sp80 multi-frame-animation pattern.
- **Sprite-construction helpers for parameterised obstacles.** `_make_brick_wall(height)`, `_make_stalactite(clearance)`, `_make_target(palette, kind)` construct sprite variants from a single function rather than inlining big pixel arrays. Lets the spec scale wall heights and ceiling clearances per-level by editing one integer.
- **Discrete parabolic-arc altitude formula.** `alt(x) = floor(peak * 4 * t * (1 - t))` where `t = (x - origin_x) / horizontal_distance` and `peak = floor(horizontal_distance / 3)`. Symmetric around the arc midpoint; `floor()` keeps the formula deterministic and replayable. Reusable for any "throw an object in an arc" mechanic.
- **Tag-based per-level resource collection.** `on_set_level` uses `level.get_sprites_by_tag("wall")`, `("ceiling")`, `("target")`, `("launcher")` to build per-level lists once instead of re-querying each frame. Standard NovaPlay idiom (~25/25 reference games).
