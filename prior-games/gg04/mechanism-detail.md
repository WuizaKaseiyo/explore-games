# gg04 — mirror-beam-bounce (multi-beam, single-sided mirrors)

## Summary
A pure-click optics puzzle. Each level has **multiple emitters**
seated at the rim of the 12×12 grid, each emitting a 1-pixel
**beam** in one fixed cardinal direction with one fixed colour.
The player's only verb is ACTION6: clicking on a **mirror cell**
rotates that mirror 90° (toggling between the two diagonal
orientations `/` and `\`).

**Single-sided mirrors**: every mirror has a reflective *front*
face (the SW half-cell) and a transparent *back* face (the NE
half-cell). A beam approaching from W or S (i.e. moving E or N
into the cell) hits the front and reflects; a beam approaching
from N or E (moving S or W into the cell) hits the back and
**transmits straight through** unchanged. This means **two beams
can share a single mirror cell without merging** — one reflecting
off the front, the other transmitting through the back. The
single-sided rule applies to **prisms** as well; only the
filter-cell is direction-agnostic.

**Multi-beam tracing**: the beams are traced independently from
each emitter. Cells visited by different beams accumulate a
**set** of colours; the win predicate checks each target cell's
colour set for the required colour. Beams never merge — each
keeps its own colour all the way to its eventual exit.

**Fake beams (L2, L3)**: at least one emitter per advanced level
emits a colour (`CYAN`) that matches no target. The fake's beam
paints cells but cannot satisfy any target check; it is pure
visual noise. S-bound fake beams (used at L2, L3) transmit
through every mirror they cross, dramatically demonstrating the
back-side share.

The level wins when every target ring has its required colour in
the cell's colour set; the only failure mode is exhausting the
per-level step counter.

**Decoy-mirror twist**: every level still seeds at least one
mirror that is already in its winning-state orientation. Clicking
it flips it OFF-true; a "click every mirror" strategy that
flips the decoy *before* the witness state is reached leaves the
level NOT_FINISHED. (Empirically: 4 of 6 click orders for L3
deflect the level into a non-winning state; only orders that
finish the witness *before* clicking the decoy succeed.)

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click pixel `(x, y)`. The engine resolves it to a logical cell `(cx, cy) = (gx // 5, gy // 5)`. If the cell hosts a rotatable mirror, toggle its orientation (`/` ↔ `\`) and consume 1 step. Clicks that miss any mirror — including clicks on floor, walls, filters, prisms, emitter rim, target rings, or the HUD strip — are no-ops with no step consumed. | always offered. |

`available_actions = [6]`. No avatar, no arrow keys, no commit
phase.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Configuration & witness |
|---|---|---|
| 1 | M1 (mirror-rotate) + M2 (single-sided beam reflect) + M3 (target colour-match) + M4 (multi-beam: two real beams sharing one mirror) + M5 (decoy mirror) | **Three mirrors. Two emitters: ORANGE west-rim row 3, BLUE south-rim col 5. M_shared at (5, 3) reflects both real beams. Decoy M_o at (5, 1). Required-flip M_b at (8, 3).** Witness state: M_shared=`/`, M_o=`/`, M_b=`\`. Witness clicks: 2 (M_shared, M_b). Targets: ORANGE at (8, 1), BLUE at (8, 5). |
| 2 | + M6 (filter-cell tints beam) + M7 (fake beam) | Three mirrors as in L1 (relocated to rows 1, 2). Filter BLUE at (7, 1) tints orange→PURPLE. Three emitters: ORANGE west-rim row 2, BLUE south-rim col 5, **fake CYAN north-rim col 9** (S-bound — transmits through every mirror it crosses; never a target colour). Witness: 2 clicks (M_shared, M_b). Targets: PURPLE at (10, 1), BLUE at (8, 5). |
| 3 | + M8 (prism: combined tint + 90° reflect) | Three mirrors (M_shared at (4, 6), M_o1 at (4, 3), decoy M_b at (8, 6)). Prism BLUE-`\` at (7, 3) (orange→purple, deflect E→S). Filter YELLOW at (7, 6) (purple→red). Three emitters: ORANGE west-rim row 6, BLUE south-rim col 4, fake CYAN north-rim col 8. Witness: 2 clicks (M_shared, M_o1). Targets: RED at (7, 8), BLUE at (8, 8). The fake CYAN beam passes through M_b's back-face on its column-8 descent — visible proof of single-sided sharing. |

## Win condition
After every action, every emitter's beam is re-traced from
scratch. For each cell visited, the cell's *colour set* is
populated with that beam's current colour at that visit. A
**target** at `(tx, ty)` with required colour `tc` is satisfied
iff `tc ∈ cell_colors[(tx, ty)]`. The level wins when every
target is satisfied; `self.next_level()` fires.

## Lose condition
`self.steps_used >= self.max_steps` triggers `self.lose()`. The
per-level budget is L1=14, L2=24, L3=36 — generous over the
witness lengths (2, 2, 2) and over recovery from a wrong-decoy
click (4, 5, 6).

## Internal state
- `self.emitters: list[(int, int, int, int)]` — list of `(cx, cy,
  direction, beam_color)`. Coordinates are virtual rim positions:
  `cx = -1` west rim, `cx = GRID_W` east rim, `cy = -1` north
  rim, `cy = GRID_H` south rim. The first iteration of
  `_trace_beam` steps the beam to its first in-grid cell.
- `self.mirrors: dict[(int, int), str]` — rotatable mirrors;
  values are `'/'` or `'\\'`.
- `self.filters: dict[(int, int), int]` — fixed filter cells with
  filter colour as the value (direction-agnostic tinting).
- `self.prisms: dict[(int, int), tuple[int, str]]` — fixed prism
  cells; value is `(filter_color, orientation)`. Single-sided
  like mirrors: only E/N approach reflects + tints; S/W approach
  transmits.
- `self.targets: list[(int, int, int)]` — `(cx, cy,
  required_color)`.
- `self.steps_used: int` / `self.max_steps: int`.

## Notable code patterns
- **Single-sided REFLECT table.** `REFLECT['/'] = {E: N, N: E}`
  and `REFLECT['\\'] = {E: S, N: W}` only. A direction missing
  from the table for a given orientation means the beam
  transmits unchanged. This rule is shared by mirrors and prisms;
  filters tint regardless of direction.
- **Per-emitter trace.** `_trace_beam(emitter)` walks one beam.
  `_trace_all_beams()` calls `_trace_beam` per emitter and
  aggregates the results into a `dict[(int, int), set[int]]`
  for the win predicate, plus a per-emitter path list for the
  beam-overlay sprites. The two return values share one full
  trace pass per call.
- **Beams don't merge** — they're separate entities through the
  whole pipeline. Visually overlapping cells display the LAST
  beam's overlay (later emitters draw on top). The win predicate
  uses the cell's colour SET, never a single colour, so visual
  collapse never affects correctness.
- **Mix table as sorted-tuple keys.** `MIX[tuple(sorted([c1,
  c2]))]` makes the colour-mix lookup symmetric in the two input
  colours. `mix(c1, c2)` returns `c1` (no-op) for pairs not in
  the table.
- **Multi-rim emitter rendering.** `_sync_sprites` resolves each
  emitter's rim position from `(cx, cy, direction)` and places
  the emitter sprite at the corresponding edge of the playfield.
  Currently supports west/east/north/south rims.
- **Decoy-mirror twist preserved.** A mirror is a decoy if its
  initial orientation matches the winning-state orientation. The
  click-everything strategy maps initial → its complement. With
  ≥1 decoy that complement is at Hamming-distance ≥1 from the
  winning state — i.e. on a wrong configuration — *unless* the
  player happens to click in an order that hits the witness
  state before reaching the decoy.

## Witness traces (validated programmatically)

| Level | Witness clicks (cells) | Beam endpoints |
|---|---|---|
| L1 | M_shared (5, 3), M_b (8, 3) | Orange: (0..5, 3) → reflect E→N → (5, 1..2) → reflect N→E (decoy) → (6..11, 1); ORANGE target at (8, 1) ✓. Blue: (5, 4..11) → reflect N→E at M_shared → (6..8, 3) → reflect E→S at M_b → (8, 4..5..0); BLUE target at (8, 5) ✓. |
| L2 | M_shared (5, 2), M_b (8, 2) | Orange: (0..5, 2) → reflect E→N → (5, 1) decoy N→E → (6..7, 1) filter BLUE → PURPLE → (8..11, 1); PURPLE target at (10, 1) ✓. Blue: (5, 11..3) → reflect N→E at M_shared → (6..8, 2) → reflect E→S at M_b → (8, 3..5..); BLUE target at (8, 5) ✓. Fake CYAN: (9, 0..11) — transmits straight through every cell. |
| L3 | M_shared (4, 6), M_o1 (4, 3) | Orange: (0..4, 6) → reflect E→N at M_shared → (4, 5..3) → reflect N→E at M_o1 → (5..7, 3) → prism `\` E→S, ORANGE→PURPLE → (7, 4..6) → filter YELLOW PURPLE→RED → (7, 7..11); RED target at (7, 8) ✓. Blue: (4, 11..7) → reflect N→E at M_shared → (5..8, 6) → reflect E→S at decoy M_b → (8, 7..11); BLUE target at (8, 8) ✓. Fake CYAN: (8, 0..11) — transmits through M_b at (8, 6) on its way south, demonstrating back-side sharing with the blue beam that ALSO passes through (8, 6) at a different turn. |

## Validation summary

- **Discovery**: `Arcade(...).make("gg04")` resolves and loads
  `Gg04` from this directory.
- **Initial-state**: every level's `_check_win()` is False at
  level start (verified all three levels).
- **L1 + L2 + L3 witnesses solve cleanly**: 6 total clicks across
  the run produce `WIN`, score=3.
- **Misclick semantics**: clicks on non-mirror cells (floor,
  walls, filters, prisms, target rings, HUD strip rows 60..63)
  are no-ops with `steps_used` unchanged and no level advance.
- **Decoy twist verified per level**: clicking the decoy
  *before* reaching the witness state leaves the level
  NOT_FINISHED. Specifically tested 6 click orders for L3; only
  the 2 that complete the witness before reaching the decoy
  result in WIN.
- **Fake beam properties** (verified):
  - Fake colour (CYAN = 10) is not in any target's required-colour
    set.
  - Fake beam transmits through every mirror on its path
    (`(8, 6)` for L3 is one such mirror cell).
  - Fake beam appears in 12 cells per level but contributes
    nothing to the win predicate.
- **Multi-beam coexistence**: 8 cells host ≥2 distinct beam
  colours simultaneously without merging — including (4, 6)
  where ORANGE (E-bound front face) and BLUE (N-bound front face)
  reflect off the same mirror in different directions, and (7, 6)
  where ORANGE (post-prism PURPLE, S-bound back face) and BLUE
  (E-bound through filter) cross.
- **Step-budget exhaust**: long enough to allow click-everything
  + recovery (4, 5, 6 actions respectively).
- **Frame rendering**: `camera.render(...)` returns a 64×64 int8
  array; the beams, mirrors, target rings, prism, filter,
  emitters at all 4 rim positions, and HUD step bar are all
  visible at the expected pixel rows.
