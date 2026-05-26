# zd7m — cohort-step-route

## Summary

Each press of a cardinal arrow attempts to step every movable
pawn on the board one cell in that direction simultaneously.
Pawns that would collide with a wall, an immovable anchor, or
another pawn whose own destination is blocked stay put for the
turn while the rest of the cohort moves; resolution is
deterministic in (y, x) row-then-column order. The win
predicate iterates the pawn list and requires every pawn to be
standing on a target tile of its own colour. Anchored sprites
(grey/off-black checker blocks) are immovable obstacles that
selectively block individual pawns, letting the player change
the cohort's relative offsets. Portal pairs (purple double
rings) teleport a pawn from `portal_a` to `portal_b` on
landing, providing access to chamber positions otherwise
walled off.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Cohort step UP — every movable pawn attempts (x, y - 1) | always |
| ACTION2 | Cohort step DOWN — every movable pawn attempts (x, y + 1) | always |
| ACTION3 | Cohort step LEFT — every movable pawn attempts (x - 1, y) | always |
| ACTION4 | Cohort step RIGHT — every movable pawn attempts (x + 1, y) | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Cohort-step + colour-matching | Three free pawns + three same-colour targets in two rows; a single direction lands each pawn on its colour-matched target. Witness: `[ACTION2] × 10`. |
| 2 | Adds anchor blocks | Two pawns with different start positions and target positions; two anchor blocks selectively block one pawn at a time so the cohort's relative offset can change. Witness: `[ACTION4] × 10 + [ACTION2] × 4`. |
| 3 | Adds portal pair | Two pawns + carrying-forward anchor mechanic + chamber walls + portal pair; one pawn's target sits inside an anchor-sealed chamber accessible only via portal teleport. Witness: `[ACTION4] × 10 + [ACTION2] × 4`. |

## Win condition

For each pawn, the engine looks up the target sprite at the
pawn's top-left grid cell; if no target is there, or the
target's first pixel does not equal the pawn's first pixel
(the colour comparison), the level is not won. Win fires
`self.next_level()` (or `self.win()` on the last level).

## Lose condition

When the per-level step counter reaches zero
(`_action_count >= step_budget`), `self.lose()` fires and the
run ends. There is no other lose path: pawns cannot be
destroyed, collisions are non-lethal, and the game is fully
deterministic.

## Internal state

- `self._step_budget: int` — per-level step cap loaded from
  `level.get_data("step_budget")`.
- `self._step_counter_ui: StepCounterHud` — `RenderableUserDisplay`
  drawing a horizontal green/off-black bar at frame row 0
  reflecting steps remaining.
- `self._teleport_phase: int` — `-1` when idle; `0..5` while a
  teleport animation is mid-flight (advanced by one tick per
  `step()` call until phase reaches 6, at which point the
  pending teleport is committed).
- `self._pending_teleport: list[(Sprite, Sprite)]` — pawns that
  just landed on a `portal_a` sprite this press, paired with the
  portal they hit; flushed when the animation completes.

## Notable code patterns

- **Cohort-step resolution.** Sort pawns by `(y, x)` to give a
  deterministic single-pass order, then for each pawn check
  anchor + pawn collisions at the proposed cell. The order
  prevents two pawns from racing for the same destination cell;
  pawn-pawn collisions are rare in this corpus because the
  placed pawns are spaced ≥4 cells apart.
- **TANGIBLE / INTANGIBLE for blocking vs decoration.** Targets
  and portals are `InteractionMode.INTANGIBLE` so pawns walk
  through them; anchors and pawns are TANGIBLE; teleporting
  pawns are temporarily set REMOVED during the animation's
  fade-out half.
- **Multi-frame teleport animation in `step()`.** `step()`
  short-circuits through `TELEPORT_FRAMES = 6` ticks after a
  pawn lands on a portal — pulsing both portal sprites'
  pixels and toggling the pawn's interaction mode — then
  commits the position swap and finally calls
  `complete_action()`. This is the same multi-frame phase-cursor
  pattern used in `cn04`, `sp80`, and `tu93`.
- **Layer order matters when sprites overlap.** Targets render
  at layer 1 and portals at layer 0 so target colour shows
  through when the two co-locate (as they do at the L3
  chamber's lone valid pawn cell). Pawns sit at layer 2 above
  both.
- **Per-level camera resize as a no-op safety net.** All three
  levels use `grid_size=(20, 20)`, so the camera resize in
  `on_set_level` is technically idempotent — but the pattern
  is kept so future spec edits that vary grid_size do not
  silently mis-render.
