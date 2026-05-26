# kf42 — tether-pawn-cycle

## Summary
Two single-cell coloured pawns sit on a walled grid joined by an
invisible maximum-distance tether (Chebyshev). The player clicks a
pawn to designate it active, then arrow keys move only the active
pawn one cell at a time. The inactive pawn is dragged exactly one
cell toward the active pawn whenever an active-pawn step would
otherwise stretch the tether past its level-specific length. From
level 2 onward, walking the active pawn onto a coloured "set-pad"
assigns the pawn that pad's colour outright (no cycle alphabet —
direct write, idempotent on a second visit). The level wins when
each pawn simultaneously occupies a distinct target pad whose
colour equals the pawn's current body colour; the only way to
lose is to exhaust the per-level step counter without satisfying
the win predicate.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | move active pawn UP one cell | only after first ACTION6 selection |
| ACTION2 | move active pawn DOWN one cell | only after first ACTION6 selection |
| ACTION3 | move active pawn LEFT one cell | only after first ACTION6 selection |
| ACTION4 | move active pawn RIGHT one cell | only after first ACTION6 selection |
| ACTION6 | click `(data["x"], data["y"])`; if it lands on a pawn, that pawn becomes active | always valid |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | tether-drag alone (open 12×12 arena, no cyclers) | tether L = 4; player learns that one pawn can be steered by clicks + arrows and that walking far enough drags the second pawn |
| 2 | colour-set pad (one blue pad on 14×14 with a short interior wall) | tether L = 5; both pawns start red; one must be routed onto the blue pad before reaching its target without dragging the other onto the same pad |
| 3 | composition of tether + colour-set + maze topology (two corridors, two cyclers, 16×16) | tether L = 6; pawns start red and blue but the layout forces each through the opposite-colour cycler first, then a click-switch reassigns colours via a second pass |

## Win condition

There exists a bijection f from the two pawns to the two target
pads such that each pawn's grid position equals the centre cell of
f(pawn) AND the pawn's body colour equals the pad's solid colour.

## Lose condition

`step_counter == 0` AND the win predicate is false. No hazards, no
chasing agents — the step counter is the only failure mode.

## Internal state

- `self.pawns: list[Sprite]` — exactly two single-cell pawn
  sprites, sorted by `(y, x)` at level start.
- `self.active_pawn: Sprite | None` — the pawn currently under
  arrow control. `None` before the first ACTION6 click. Reset on
  level entry.
- `self.tether_length: int` — read from `level.get_data("Tether")`
  in `on_set_level`.
- `self.target_pads: list[Sprite]` — the two diamond-cross
  target-pad sprites in the current level.
- `self.cycler_pads: list[Sprite]` — the colour-set pads in the
  current level (empty for level 1).
- `self.max_steps: int` — per-level action budget from
  `level.get_data("StepCounter")`.
- `self.step_bar: StepBarHud` — single-row depleting bar at row
  63 showing remaining steps as a fraction of `max_steps`.
- Hidden state `(2, 2) np.int16`:
  `[[active_pawn_index, remaining_steps], [pawn[0].colour, pawn[1].colour]]`.

## Notable code patterns

- Step counter HUD: a `RenderableUserDisplay` subclass holding
  `(max_steps, current_steps)`; `set_current(remaining)` is called
  at the top of every `step()` from the formula
  `max_steps - self._action_count`. The HUD is registered via
  `Camera(interfaces=[step_bar, active_marker])`.
- Active-pawn outline HUD: a second `RenderableUserDisplay` that
  reads `self.game.active_pawn`, scales grid → display via
  `64 // grid_dim`, and paints four corner pixels around the
  active pawn's display block.
- `_get_valid_actions`-based gating: before any ACTION6 selection,
  only ACTION6 entries (one per pawn, with display-coord centres)
  are returned. After selection, ACTION1..4 are also offered.
- Tether-drag invariant: in `_try_move_active`, the sequence is
  (1) bounds + wall check on the proposed active-pawn cell,
  (2) Chebyshev-distance check after the proposed move, (3) if
  the post-move distance exceeds the tether length, propose a
  `sign`-based one-cell drag of the inactive pawn and bounds +
  wall check the drag too — if the drag is invalid, the active-
  pawn step is reverted (the constraint binds against the wall).
- Cycler trigger: on each successful active-pawn move,
  `level.get_sprite_at(pawn.x, pawn.y, tag="cycler")` runs once;
  if a cycler is found, `pawn.color_remap(None, cycler.pixels[0,0])`
  applies in place. Idempotent on repeat visits because the
  remap to the same colour is a no-op.
