# xz5g — arena-pivot-rotate

## Summary

The player solves three rotation puzzles by clicking a free
pivot cell on a 64×64 grid and pressing ACTION5 to rotate every
"rotatable" sprite 90° clockwise around the pivot. A tiny
pink "+" marks the exact pivot cell so the player can read off
the rotation centre at a glance. There is no direct movement
verb — pawns reach their targets only via the world-rotation
transform. Level 1 delivers a single blue avatar onto a
colour-matched target ring with one rotation. Level 2 adds an
orange companion pawn — both pawns co-rotate, so the player
must find a single pivot whose two rotations deliver each pawn
to its own target. Level 3 retains the same two-pawn cast
(blue avatar, orange companion) but reconfigures the layout
diagonally so that no single rotation can win the level —
exactly two rotations around the centre are required to cycle
each pawn through to its diagonally-opposite target. The win
predicate is single-clause: every target must hold a
colour-matched pawn.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Commit-rotate. If `_pivot is None`, no-op (still consumes 1 step). Otherwise transforms every `rotatable` sprite by 90° clockwise around `_pivot` using `(x, y) → (px+py−y, py+x−px)`; rejects entire rotation if any rotatable sprite would land out of bounds or two rotatables would collide on the same destination cell (clean simultaneous swap excluded). | always; consumes 1 step |
| ACTION6 | Click at display pixel (x, y); via `camera.display_to_grid` to grid (gx, gy). Two rules in order: (1) hits any `rotatable` / `target` sprite → no-op; (2) else set `_pivot = (gx, gy)` and reposition the 3×3 "+" `pivot_marker` so its centre pixel coincides with `(gx, gy)` (INTANGIBLE). | always |

(`available_actions=[5, 6]`. ACTION1-4 omitted — no cardinal motion
verb. ACTION7 omitted — no undo. Rotation direction is fixed CW
throughout the game; the source retains the CCW formula and
visit-checkpoint scaffolding for future extension but they are
unreachable in any of the 3 shipped levels.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base dynamic system: M1 pivot-set + M2 commit-rotate. | avatar at (12, 32); avatar_target at (32, 12); single CW rotation around pivot (32, 32) lands avatar on target. **Witness `[ACTION6@(32, 32), ACTION5]`** (2 actions). Step budget 25. |
| 2 | + M3 companion-pawn-deliver — second rotatable pawn (orange companion) co-rotates with the avatar; both must land on colour-matched targets. The two pawns are placed on orthogonal axes (avatar on the horizontal axis, companion on the vertical axis), each across the centre from its target. | avatar at (8, 32) → (56, 32); companion at (32, 8) → (32, 56). Two CWs around (32, 32) deliver both. **Witness `[ACTION6@(32, 32), ACTION5, ACTION5]`** (3 actions). Step budget 30. |
| 3 | Same mechanic family as L2 (M1 + M2 + M3); the new contribution is a **diagonal corner layout** that proves no single rotation can win — exactly two are required. The pawns sit on the NW and NE corners; each target sits diagonally across, on SE and SW. Brute-force verified: zero (pivot, direction) pairs admit a 1-rotation win. | avatar at (12, 12) → (52, 52); companion at (52, 12) → (12, 52). 1 CW around (32, 32) cycles avatar (12, 12) → (52, 12) [companion's start] and companion (52, 12) → (52, 52) [avatar's target] — pawns on each other's start/target, not their own. 2nd CW completes the cycle: avatar → (52, 52) ✓, companion → (12, 52) ✓. **Witness `[ACTION6@(32, 32), ACTION5, ACTION5]`** (3 actions). Step budget 40. |

## Win condition

Single clause: every sprite tagged `target` is coincident
(top-left equality) with at least one `rotatable` sprite of
matching tag (`avatar_target` ↔ `avatar`; `companion_target`
↔ `companion`). When true, `self.next_level()` fires; after
L3's `next_level()` the engine fires WIN automatically
(3-level cap). The visit-checkpoint clause in the source is
retained but vacuously true on every level (no `anchor_pin`
sprites are placed in any of the 3 shipped levels).

## Lose condition

`self._steps_left` is initialised in `on_set_level` from
`level.get_data("step_budget")` and decrements 1 per handled
action (both ACTION5 and ACTION6 cost 1 regardless of outcome).
When `_steps_left ≤ 0` after the action handlers,
`self.lose()` fires. No instant-fail hazard.

## Internal state

- `self._pivot: tuple[int, int] | None` — currently-marked
  pivot cell, persistent across rotations.
- `self._direction: str` — `"CW"` or `"CCW"`, default `"CW"`,
  toggled by clicking the `direction_indicator` widget.
- `self._steps_left: int` — per-level remaining-action counter,
  decremented per handled action.
- `self._visited_pins: set[tuple[int, int]]` — cells of
  `anchor_pin` sprites that have been coincident with a
  rotatable sprite at some prior end-state during the current
  level. Re-initialised to empty in `on_set_level`.
- `self._step_hud: StepCounterHud` — the bottom-row depleting
  bar.

## Notable code patterns

- **Free-pivot whole-arena rotation.** `_handle_rotate`
  computes per-sprite destinations via the closed-form
  rotation formula (CW or CCW around `_pivot`); validates all
  destinations against bounds + rotatable-rotatable collision
  (clean swap excepted); then commits via `set_position` plus
  `sprite.rotate(90)` or `rotate(270)`. The pivot is held
  across rotations until the next ACTION6 click on an empty
  cell.
- **Tiny "+" marker on the pivot cell.** A 3×3 sprite with a
  pink-and-magenta "+" pattern (transparent corners) — the
  centre pixel coincides exactly with `_pivot`. REMOVED until
  the first click; INTANGIBLE after. The minimal footprint
  lets the player read off the precise rotation centre even
  when the pivot lies adjacent to a pawn or target.
- **Visit-checkpoint scaffold (unused at ship).** The source
  retains `_visited_pins` tracking and the
  `ANCHOR_PIN_UNVISITED → ANCHOR_PIN_VISITED` palette flip
  for an `anchor_pin` tag, plus the 4×4 `anchor_pin` sprite
  in the bank. No level places one in the 3 shipped levels,
  so the visit-clause is vacuously true throughout.
- **Direction-toggle scaffold (unused at ship).** The source
  carries the CCW formula and a two-variant `direction_indicator`
  sprite (CW / CCW corner-pip variants) plus a `_toggle_direction`
  helper. No level places either variant in the 3 shipped
  levels, so the rotation direction is fixed CW throughout.
- **Symmetric pawn-target visual pairing.** Same 6×6 frame
  with palette accent (blue 9 / orange 12) for both
  pawn-and-its-target — checklist 21 *identical-visuals →
  correlated-roles*. Filled-vs-hollow centre is the
  role-distinction (pawn = filled body; target = transparent
  centre).
- **Init-order awareness.** Field defaults (`_pivot`,
  `_direction`, `_steps_left`, `_visited_pins`) are set
  *before* `super().__init__()`, because the parent constructor
  calls `set_level(0) → on_set_level`, and on_set_level reads
  these defaults; setting them after super.__init__ would
  clobber the per-level setup the parent already ran.
