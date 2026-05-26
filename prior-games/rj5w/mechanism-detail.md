# rj5w — axis-fold-mirror

## Summary
The playfield is a sheet of "paper" with one or two thin fold-line
cursors that the player can slide across the sheet using arrow
keys. Pressing ACTION5 commits a fold along the **active**
fold-line; every (unlocked) pawn's position is reflected across
that line. ACTION6 clicks toggle which axis is active by hitting
the corresponding fold-line cursor cell. The level is won when
every coloured nub-pawn coincides with its same-colour target ring.
Pawns that move onto their target via a fold become **locked** —
visibly dimmed — and are no longer affected by subsequent folds.
The mechanic draws on geometry/topology (axis reflection) and
objectness (persistent pawns and targets). The lose condition is
exhausting the per-level step counter.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move active fold-line UP one row | active axis is H (L2/L3 only) |
| ACTION2 | Move active fold-line DOWN one row | active axis is H (L2/L3 only) |
| ACTION3 | Move active fold-line LEFT one column | active axis is V (all levels) |
| ACTION4 | Move active fold-line RIGHT one column | active axis is V (all levels) |
| ACTION5 | Commit a fold along the active axis | always |
| ACTION6 | Click `(gx, gy)`: gx == F_v → V active, else gy == F_h → H active, else no-op | L2/L3 only |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | V-fold (slide V-line + ACTION5 commit box-reflects pawns through column F_v: anchor `x → 2·F_v − x − (s−1)` for an `s×s` sprite) | Single green pawn must reach a single green target on the opposite half of the sheet. Witness `[ACTION4, ACTION4, ACTION5]` (3 actions, F_v: 30→32, then commit). |
| 2 | + H-fold (perpendicular axis with ACTION1/2 + ACTION5) and + active-axis toggle (ACTION6 click on a fold-line cursor) | Three pawns / three targets in a diagonally-symmetric layout; the same F_v=32 and F_h=32 satisfy all three pairs. Witness `[ACTION4, ACTION4, ACTION5, ACTION6@(20, 30), ACTION2, ACTION2, ACTION5]` (7 actions). |
| 3 | + Lock-on-target (a pawn that moves onto its colour-matched target locks and is not affected by subsequent folds; visible cue via dim color-remap) | Three pawns/targets arranged so a single fold-each-axis greedy heuristic fails. Witness exploits the double-V-fold-cancels-itself property: after the first V-fold locks green and yellow, a second V-fold undoes purple's V-displacement while green and yellow stay put; then a single H-fold (at F_h=34) delivers purple. Witness `[ACTION4×4, ACTION5, ACTION5, ACTION6@(20, 30), ACTION2×4, ACTION5]` (12 actions). |

## Win condition
Every pawn (one of each colour present in the level) sits at the
same `(x, y)` as its colour-matched target sprite. Concretely,
for each `(pawn_<col>, target_<col>)` pair the pawn's anchor x and
y both equal the target's anchor x and y. When the predicate holds,
`self.next_level()` fires.

## Lose condition
Step-counter exhaustion. Each action (other than the engine's
internal `RESET`) decrements the per-level `step_budget` by 1; if
the budget reaches zero before a win triggers on the same turn,
`self.lose()` fires.

## Internal state
- `self.active_axis` — `"V"` or `"H"`, the axis ACTION5 acts on.
- `self.fv` / `self.fh` — current column of the V-line cursor and
  current row of the H-line cursor (`-1` if absent in the current
  level).
- `self.locked_pawns` — set of pawn sprites that have landed on
  their colour-matched target via a fold.
- `self.step_budget` — remaining actions before `lose()`. Per-level
  starts: L1 = 25, L2 = 100, L3 = 160.
- `self.pawn_to_target` — `id(pawn) → target` map computed in
  `on_set_level`.
- `self.pawn_to_color` — `id(pawn) → "green"/"purple"/"yellow"`
  map for cue management.

## Notable code patterns
- **Step-counter HUD as a single-row depleting bar** — universal
  pattern from the 25 reference games; `StepCounterHud` paints
  row 63 with palette 6 (filled) and palette 4 (empty) proportional
  to budget remaining.
- **Axis activation via runtime `color_remap`** — the V- and H-line
  cursors are placed once per level with palette 12 pixels; toggle
  swaps via `color_remap(12, 3)` and `color_remap(3, 12)` rather
  than swapping sprite instances.
- **Lock-on-target via dim color-remap** — when a pawn locks, its
  base colour (14/15/11) is remapped to palette 3, dimming the pawn
  as the persistent visual cue per checklist item 19.
- **Fold-line cursors declared `InteractionMode.INTANGIBLE`** —
  they render but do not block pawn collisions; pawns can occupy
  the same column/row as the fold-line without being deflected.
- **Box reflection** — the whole sprite footprint mirrors through
  the fold-line as a unit. `_commit_fold` computes
  `new_x = 2·F_v − old_x − (PAWN_SIZE − 1)` (and the analogous
  H-fold form) so the sprite's centre lands on the geometrically-
  correct mirror cell. The reflected anchor is bounds-checked
  against `[GRID_MIN, GRID_MAX] = [0, 64 − PAWN_SIZE]` before
  committing the move; out-of-bounds reflections leave the pawn
  in place. Pawns whose reflected anchor equals their current
  anchor (the fold-line passing through the sprite's centre, i.e.
  `F = anchor + (PAWN_SIZE − 1)/2`) also stay put without
  triggering the lock-on-target check.
