# kg7p — beam-tether-haul

## Summary
A single avatar walks a 64×64 arena via arrow keys. The avatar always
faces its last walked direction and projects a one-cell tether beam
from its front edge. Pressing ACTION5 toggles the beam: turning the
beam on attempts an immediate couple to whatever haulable block sits
in the beam cell, turning it off detaches any coupled block in place.
While a block is coupled, it walks in lockstep with the avatar
preserving a fixed grid-aligned offset; walks rejected if either
destination collides with a wall or an uncoupled block. Direction-
locked blocks carry a magenta edge-stripe along one cardinal edge
and can only be coupled and hauled in the direction that matches the
stripe.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Walk avatar one cell north; rotate avatar to face north. If a block is coupled, haul it in lockstep. Walks rejected if avatar's or coupled block's destination is invalid, or if a coupled directional block's allowed haul direction is not north. | Always selectable. |
| ACTION2 | Walk south. Same rules; direction-lock check is "stripe south". | Always. |
| ACTION3 | Walk west. Direction-lock check is "stripe west". | Always. |
| ACTION4 | Walk east. Direction-lock check is "stripe east". | Always. |
| ACTION5 | Toggle beam. ON ⇒ attempt to couple any block in the cell in front of the avatar (subject to direction-lock match). OFF ⇒ detach the currently coupled block in place. | Always. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | walk-avatar + beam-couple-haul | Single block + single target on a row. Witness `[ACTION5, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]` (9 actions). |
| 2 | + beam-release (toggle off mid-game) | Two blocks (orange, yellow) with two colour-paired targets. Yellow's straight south path passes through orange's start cell; the order matters. Witness 29 actions (orange-first then yellow): `[ACTION5, ACTION4×4, ACTION3×5, ACTION5, ACTION1, ACTION4×6, ACTION1×2, ACTION5, ACTION2×8]`. |
| 3 | + direction-locked blocks | Two directional blocks: block_C with north-stripe (haul north), block_D with east-stripe (haul east). block_D's east path passes through block_C's start cell, forcing the player to deliver block_C first. Witness 25 actions: `[ACTION4×3, ACTION2×3, ACTION3, ACTION5, ACTION1×4, ACTION5, ACTION3×3, ACTION2×3, ACTION5, ACTION4×5]`. |

## Win condition
After every action, the game checks whether every `block` sprite
sits at the same (x, y) as a target whose sub-tag matches the
block's sub-tag (`block_basic` ↔ `target_basic`; `block_dir` ↔
`target_dir`). If yes, `self.next_level()` fires. After the third
level's win, the engine's default behaviour fires `self.win()`.

## Lose condition
`self._action_count >= self.level_budget` at the start of `step()`
triggers `self.lose()`. Budgets per level: L1=40, L2=60, L3=80
(generous over the witness lengths).

## Internal state
- `self.avatar` — the single avatar sprite for this level.
- `self.facing_dir` — `(dx, dy)` cell-stride vector of the avatar's
  current facing; matches the rotation set on the avatar sprite.
- `self.beam_on` — boolean; whether the tether beam is currently
  emitting.
- `self.coupled_block` — the currently coupled haulable block, or
  `None`.
- `self.coupled_offset` — pixel offset between coupled block and
  avatar at the moment of coupling; preserved across walks.
- `self.beam_indicator_sprite` — the spawned green-ring sprite that
  visually marks the beam cell while the beam is on.
- `self.level_budget` — the step budget loaded from
  `level.get_data("step_budget")` in `on_set_level`.
- `self._step_counter_ui` — the HUD widget rendering the depleting
  step-counter bar on row 63.

## Notable code patterns
- **Coupling-on-rotation** — when the player presses a direction
  button, the avatar's rotation and facing_dir update first; THEN
  the beam indicator is re-anchored to the new front cell; THEN
  `_try_couple()` runs against the front cell before the avatar's
  collision check. This is necessary because the front cell often
  contains an uncoupled block; without this ordering the avatar
  would be rejected as "destination occupied" before it could
  couple.
- **Two-sprite simultaneous-move with offset preservation** — when
  hauling, the avatar's `move(dx, dy)` is called first and then
  the coupled block's `move(dx, dy)` is called with the same
  vector. The collision checks run BEFORE the moves; both
  destinations are validated together so a single failure rolls
  back the whole walk.
- **Direction-lock via rotation-encoded edge marker** — the
  `block_dir` sprite carries a magenta stripe on its east edge in
  rotation 0; rotations 90/180/270 carry the stripe to
  north/west/south edges (np.rot90 is CCW in novaengine). The
  `_block_dir_allowed_haul()` helper maps rotation → allowed haul
  direction without inspecting pixels.
- **Beam-indicator as a separate INTANGIBLE sprite** — kept on
  layer 5 (above the block), spawned when the beam toggles on,
  removed when the beam toggles off. The indicator's position
  updates after every walk and every rotation so it always points
  at the cell the beam currently covers.
- **Per-block layer bump on couple** — coupling raises the block's
  render layer from 3 to 4 so it renders above the target it might
  cross; releasing the block restores layer 3.
