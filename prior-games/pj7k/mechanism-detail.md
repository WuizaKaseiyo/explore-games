# pj7k — rolling-cube-face-paint

## Summary
The player controls a single 3×3 cube sprite whose six faces each
carry a distinct palette colour. Arrow keys (and only arrow keys —
no twist, no click) roll the cube one logical cell in that direction;
the roll permutes the face colours deterministically (the side facing
the move direction rotates to the new top, the trailing side becomes
the new bottom). The colour that ends up on the bottom after a roll
is deposited as paint on the landed cell. The level wins when every
target cell has been satisfied. Step counter HUD bar at the top
depletes 1 per attempted action; on zero, the level is lost. The
three levels share the same rolling-paint verb but place the player
under progressively stronger constraints: visit-anywhere → reach a
distant single target → match required colours at multiple targets.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Roll cube one cell north; permute faces (`T'=F, Bo'=Ba, F'=Bo, Ba'=T`); deposit `bottom` on landed cell. | always; out-of-bounds rejection still consumes 1 step. |
| ACTION2 | Roll south (`T'=Ba, Bo'=F, F'=T, Ba'=Bo`); deposit. | as ACTION1 |
| ACTION3 | Roll west (`T'=R, Bo'=L, R'=Bo, L'=T`); deposit. | as ACTION1 |
| ACTION4 | Roll east (`T'=L, Bo'=R, L'=Bo, R'=T`); deposit. | as ACTION1 |

(No ACTION5; no ACTION6; no ACTION7. Pure cardinal rolling.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Rolling-paint inside an unfolded-cube net (constrained corridor) | 6×6 logical board with black walls everywhere except the 7-cell unfolded-cube net `{(0,2)} ∪ cross{(1,2),(2,1),(2,2),(2,3),(3,2),(4,2)}`. Cube starts at (0, 2) and once it leaves the start cell it cannot return. The 6 net cells carry colour-specific target rings (orange, red, yellow, green, purple, blue) chosen from the witness's face-permutation so the level is solvable in one canonical sequence. Witness `[E, E, S, N, N, S, E, E]` (8 actions); win = every target has its required paint colour. |
| 2 | + Diagonal traversal with first-arrival match | 4×4 logical board; cube at (0, 0), single red target at (3, 3) (diagonal opposite corner). Natural axis-by-axis path `[E, E, E, S, S, S]` (6 actions) deposits red at (3, 3) on the first arrival. Witnesses the rolling rule across BOTH axes (east and south) before the player commits. |
| 3 | + Multi-target colour matching with backtrack | 4×4 logical board; cube at (0, 0); three targets requiring specific colours: (1, 0)=green, (3, 0)=red, (3, 1)=yellow. Win = each target has the matching paint. Witness `[E, S, E, N, W, E, E, S]` (8 actions). The player must plan a non-trivial path that paints (1, 0) on a return pass with the correct face on bottom. |

## Win condition

Per level, every sprite tagged `target` must satisfy:

- if `level.data["win_mode"] == "any"`: a `paint` sprite exists at
  the target's cell (any colour).
- else (`exact`): a `paint` sprite exists at the target's cell AND
  its colour equals the target's required colour (encoded by
  sub-tag `target_<colour>`).

When all targets satisfy, fire `next_level()`. After L3, the engine
fires `win()`.

## Lose condition

Step counter reaches zero — `lose()` fires. There is no instant-fail
collision; out-of-bounds rejections only consume a step without
ending the run.

## Internal state

- `self.faces: dict[str, int]` keyed
  `top`/`bottom`/`front`/`back`/`left`/`right`. Reset in
  `on_set_level` to `{T:11, Bo:9, F:14, Ba:8, L:15, R:12}`.
- `self.cube_x, self.cube_y: int` — current grid position.
- `self.step_counter: StepBarHud` — HUD widget.
- `self._paint_seq: int` — monotonic naming for paint sprites.
- `self._win_mode: str` — `"any"` (L1) or `"exact"` (L2/L3), read
  from `level.data["win_mode"]`.
- `self._logical_size: int` — derived from `level.grid_size[0] //
  STRIDE` (4 for L2/L3, 6 for L1) so that `_try_roll` can bounds-
  check against the per-level board.

## Notable code patterns

- **Cube pixels rebuilt per step from a face dict.** `Sprite.rotate`
  is a 2D in-plane rotation; this game needs a 3D-rotation effect
  on the cube's visible faces. The cube's `pixels` array is
  re-synthesised every step from `self.faces`
  (`back/back/back // left/top/right // front/front/front`),
  giving the player a top-down view that shows top + the four side
  strips.
- **Roll-permutation tables as pure dict→dict functions.** Four
  helpers (`_roll_north/south/west/east`) each take a face dict
  and return the permuted face dict; deterministic, side-effect
  free.
- **Per-level grid size + camera resize.** L1 uses
  `grid_size=(24, 24)` to fit the 6×6 cube-unfold net; L2/L3 use
  `(16, 16)` for the 4×4 board. `on_set_level` mutates
  `camera.width / camera.height` to match (and recomputes
  `_logical_size` from the new grid_size).
- **Win-mode level-data flag.** A single `data["win_mode"]` field
  on each Level distinguishes "step on every target" (L1's
  pedagogical first-encounter goal) from "match each target's
  required colour" (L2/L3's planning constraint). The same
  `_check_win` helper handles both.
- **Tag-encoded colour sub-tags.** Every colour-bearing sprite
  carries a sub-tag `target_<colour>` / `paint_<colour>` matching
  one of `{yellow, blue, green, red, purple, orange}`; a single
  `_colour_from_subtag` helper decodes the colour value via a
  pre-built `NAME_TO_COLOUR` lookup.
