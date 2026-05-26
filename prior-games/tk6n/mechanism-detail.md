# tk6n — boomerang-arc-catch

## Summary

The player controls a single avatar that walks one cell per arrow
press and carries a thrown projectile (the "boomerang"). ACTION5
launches the boomerang in the avatar's current facing direction; it
travels outbound a fixed number of cells, then enters a HOMING
RETURN phase where each tick it advances one cell in the cardinal
direction whose Manhattan-component to the avatar's CURRENT cell is
larger (ties broken x-first). The boomerang lights coloured target
sprites it overlaps on either leg, and is caught when its cell
coincides with the avatar's. Win = every target lit AND boomerang
held; lose = step budget exhausted, or (L3 only) avatar collides
with the patrolling guard.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Walk UP one cell; set facing=UP. | always |
| ACTION2 | Walk DOWN one cell; set facing=DOWN. | always |
| ACTION3 | Walk LEFT one cell; set facing=LEFT. | always |
| ACTION4 | Walk RIGHT one cell; set facing=RIGHT. | always |
| ACTION5 | If boomerang held: launch in current facing. If dropped and avatar overlaps it: pick up. | gated invalid while in flight |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base system: throw + outbound + homing-return + catch + target-light-on-overlap. | Open arena. Avatar at `(20, 36)`; target at `(32, 22)` — offset on BOTH axes so the player must first walk to align with the target's row (or column) before throwing. Witness `[ACTION1×14, ACTION4, ACTION5, (ACTION1/ACTION2 oscillation)×24]` (40 actions in smoke test; step_budget=50). |
| 2 | + wall-height gating (wall_tall blocks both, wall_short blocks avatar walking only). | Sealed corridor west-wall_tall, ceiling+floor wall_tall, east-wall_tall, with a wall_short barrier mid-corridor at col 22; target at col 28 east of barrier. Avatar bounded west of barrier; only path to target is for boomerang to fly OVER the wall_short. Witness `[ACTION5] + [ACTION1, ACTION2] × 16` (33 actions in smoke test; budget 60). |
| 3 | + deterministic patrolling guard with boomerang-freeze rule. | Same corridor as L2, wall_short at col 28; target at col 40; guard sprite patrolling cols 12..24 row 32 east-then-west. Avatar must throw east; boomerang's outbound east-of-row-32-area path overlaps guard mid-flight, freezing it. Avatar oscillates rows above/below guard while waiting for catch. Witness `[ACTION5] + [ACTION1, ACTION2] × 35+` (70 actions in smoke test; budget 100). |

## Win condition

All sprites with tag `target` carry the `lit` tag (i.e. every
`target_dim` has been swapped to `target_lit` by the boomerang's
overlap rule), AND the boomerang is in `held` phase (caught by
the avatar).

## Lose condition

Either the step counter has decremented to zero, OR (L3 only) the
avatar's cell coincides with the active (non-frozen) guard's cell
after either avatar move or guard tick.

## Internal state

- `avatar` — Sprite reference, 5×5 player.
- `boomerang` — Sprite reference, 3×3 projectile; hidden via
  InteractionMode.REMOVED when held, INTANGIBLE when in flight or
  dropped.
- `boomerang_phase` — `held` / `outbound` / `returning` / `dropped`.
- `boomerang_throw_dir` — (dx, dy) cardinal; None when held.
- `boomerang_outbound_remaining` — outbound advances left.
- `boomerang_pos` — current (x, y) when in flight or dropped.
- `facing` — (dx, dy) cardinal; surfaced via avatar sprite rotation.
- `lit_targets` — set of lit target sprites.
- `steps_remaining` — per-level step counter.
- `guard` / `guard_patrol_dir` / `guard_min_x` / `guard_max_x` /
  `guard_freeze_remaining` / `freeze_duration` — guard patrol state
  (L3 only).
- `throw_range` — per-level outbound length.

## Notable code patterns

- **Phase-state machine in `step()`.** Avatar action and boomerang
  advance happen on the SAME tick; while in flight, ACTION5 is gated
  invalid via `_get_valid_actions`. Captures the multi-tick
  projectile lifecycle without spawning a separate animation
  scheduler.
- **Sprite-swap for state visualisation.** Lit targets and frozen
  guards are rendered by REPLACING the sprite (`add_sprite` +
  `remove_sprite`) with a recoloured variant rather than mutating
  pixels; clean, idiomatic, survives the engine's render pipeline
  without surprises.
- **Bounce-on-wall during outbound, drop-on-wall during return.**
  When the boomerang's per-tick advance hits a wall_tall or grid
  boundary, outbound switches to returning at the cell BEFORE the
  wall; returning DROPS at its current cell. Player must walk to
  the dropped boomerang and ACTION5 to pick up.
- **Greedy-Manhattan homing return.** Boomerang's return path
  picks the cardinal step with the larger absolute Manhattan
  component to avatar (ties x-first). Simple, deterministic, and
  visibly chases the avatar across the playfield.
- **Two-mode wall sprites by tag.** `wall_tall` and `wall_short`
  share the `wall` tag for grouping, but the boomerang advance
  loop only checks `wall_tall` cells via `get_sprites_by_tag(
  "wall_tall")` — `wall_short` cells are silently passable to the
  projectile, idiomatically "fly over".
