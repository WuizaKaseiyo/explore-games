# `hl4n` — Mechanic Spec

## 1. Title
Hue-Cross Loom (working title; not visible in-game).

## 2. Mechanic family
Pure-click puzzle in the family `row-col-tint-cross`. Cells inside a fixed grid take their displayed color from a per-row "row tint" plus a per-column "column tint" via a level-specific combiner rule (row-only at L1, column-overrides-row at L2, brighter-of-the-two at L3). The player clicks edge-mounted **tint markers** (one to the left of every row, one above every column) to cycle that row/column's tint through a 4-color palette. Lock-target rings inside the playfield must end up matching a required tint for the level to win.

Core knowledge priors used (per `core-knowledge-priors.md`):
- **Objectness** — markers, cells, lock-target rings are persistent entities; clicks act on stable references.
- **Basic geometry & topology** — row and column membership are the two load-bearing geometric concepts; a lock target at cell `(r, c)` is solved by reasoning about row `r` and column `c`.

No physics, no agentness — static-recoloring puzzle.

## 3. Sprite roster

All sprites are designed at the display-pixel level so the rendered 64×64 frame reads as a detailful grid, not coarse uniform blocks (per `checklist.md` items 20 and 21).

- `cell` — 6×6, single palette value (set per-cell at runtime). Tag `cell`. layer 0. Plain solid fill — its job is to display the row/column-derived tint.
- `lock_target` — 6×6, transparent interior (4×4 of `-1`) framed by a 1-px outer ring. The ring is colored to the **required tint** for that target (so the player can see "this target wants color X" without any text). On satisfaction (current cell color == required), the four corner pixels of the ring flip to white (palette 0) — visible "all four corners lit" cue. Tag `lock_target`. layer 1. `interaction=INTANGIBLE` so it doesn't block anything.
- `row_marker` — 6×6 sprite, sits at the left of one row. 1-px outer frame in palette 4 (off-black) so it reads as a clickable button; interior 4×4 is filled with the marker's current tint (or palette 5 / black when unset). A small 1×4 vertical stripe of palette 3 (grey) at the rightmost column inside the frame visually points "this marker controls the row to my right". Tag `row_marker` plus a per-row identifier tag like `row_3`. layer 0. Tags include `sys_click`.
- `col_marker` — 6×6 sprite at the top of one column. Same as `row_marker` but rotated: the 1×4 grey stripe is at the *bottom* row inside the frame, pointing down to "this marker controls the column below me". Tag `col_marker` plus a per-column identifier tag. Tags include `sys_click`.
- `step_counter_hud` — `StepCounterHud(RenderableUserDisplay)`. Draws a horizontal depleting bar of width 48 px on row 60 of the frame, between x=8 and x=56 — the exact horizontal extent of the playfield. Bar drains right-to-left, palette 14 (green) for remaining, palette 4 (off-black) for spent.

Palette discipline (per `negative-similarity-check.md` Principle 2 — diverge from the kf42/vh68 `{4, 8, 9}` cautionary tale):
- Background: 2 (light-grey).
- Padding/letter-box: 5 (black).
- Tint cycle (in click order, ascending palette index = ascending "brightness"): `2 (background)` → `8 (red)` → `11 (yellow)` → `14 (green)` → `2 (background)` → ...
- Lock-target ring required-color: drawn from `{8, 11, 14}` (background never required as a lock).
- HUD: 14 / 4 (green / off-black).
- Marker chrome: 4 (frame) and 3 (orientation hint stripe).

This is a deliberate departure from any prior's dominant palette: no use of 9 (blue) or 12 (orange) anywhere; the trio `{8, 11, 14}` (red/yellow/green) is a fresh signature versus the corpus's typical `{4, 8, 9, 14}`.

Layout (64×64 canvas):
- Top strip (y=1..7): 8 column markers at `x ∈ {8, 14, 20, 26, 32, 38, 44, 50}`, each 6×6.
- Left strip (x=1..7): 8 row markers at `y ∈ {8, 14, 20, 26, 32, 38, 44, 50}`, each 6×6.
- Playfield: 8×8 grid of cells, each 6×6 px, occupying `x ∈ [8, 56], y ∈ [8, 56]`. Cell `(gx, gy)` is at pixel position `(8 + 6*gx, 8 + 6*gy)`.
- Lock targets sit on top of (intangible overlay) some cells in the playfield.
- Bottom strip (y=60): step counter HUD, x ∈ [8, 56].
- Right strip (x=56..63), top-right corner (x=56..63, y=0..7), bottom-right corner: padded with palette 5 (black) from `letter_box`.

## 4. Level progression, mechanic enumeration, and witness solutions

The cell-color rule (which combines `row_tint[gy]` and `col_tint[gx]` into the displayed color of cell `(gx, gy)`) is the level-specific mechanic ladder. Background tint = 2 always.

Throughout: a lock target is "satisfied" iff the cell beneath it is rendered the lock's required color.

### Level 1 — base dynamic system
- **Cell-color rule (L1)**: `cell_color(gx, gy) = row_tint[gy]`. Column tints have no effect (column markers are absent from L1).
- **Sprites placed in L1**: 8 cells per row × 8 rows = 64 cells; 8 row markers (left strip); ZERO column markers; 3 lock targets at the following positions:
  - Lock A: cell `(2, 2)`, required color 8 (red).
  - Lock B: cell `(5, 4)`, required color 11 (yellow).
  - Lock C: cell `(3, 6)`, required color 14 (green).
- `step_budget = 30`. Witness uses 3 clicks; budget gives 27 cycles of margin for exploration.
- **Mechanics required by the witness** (N=1):
  - **M1 (row-tint cycling)**: clicking a row marker cycles its tint through `2→8→11→14→2` and recolors every cell in that row.
- **Necessity per mechanic (counterfactual)**:
  - M1: L1 cannot be solved without triggering M1 because the three lock targets sit in three distinct rows (rows 2, 4, 6) and each requires a non-background color (8, 11, 14) — the only mechanism in L1 that puts non-background color on a cell is clicking a row marker, so the player must click row markers 2, 4, and 6 a positive number of times.
- **Witness solution** (3 actions): `[ACTION6@(4, 20), ACTION6@(4, 32), ACTION6@(4, 44), ACTION6@(4, 32), ACTION6@(4, 32), ACTION6@(4, 32), ACTION6@(4, 44), ACTION6@(4, 44)]`. Wait — let me restate concretely. Click coordinates target row markers (which sit at x ∈ [1, 7], so center x=4):
  - Click row-marker 2 once → row 2 tint = 8 (red). Lock A satisfied.
  - Click row-marker 4 twice → row 4 tint = 11 (yellow). Lock B satisfied.
  - Click row-marker 6 three times → row 6 tint = 14 (green). Lock C satisfied.
  - Total: 1 + 2 + 3 = **6 clicks**: `[ACTION6@(4, 20), ACTION6@(4, 32), ACTION6@(4, 32), ACTION6@(4, 44), ACTION6@(4, 44), ACTION6@(4, 44)]`.
- **Difficulty justification**:
  - **(a) Random-resistance**: a uniformly random clicker on the 64×64 frame has, per click, ~3% chance to land on any one row marker (each marker is 6×6 = 36 px out of 64×64 = 4096 px; 36/4096 ≈ 0.88% per marker, 8 markers ≈ 7%; with 30 clicks the expected hits per marker ≈ 0.26; reaching exactly 1/2/3 clicks on the *right three markers* in the *right counts* is well under the 1/10000 threshold from §3.5).
  - **(b) Human-tractable**: roughly 30–60 seconds. A new player observes "click left-edge marker → row recolors" in ≤2 exploratory clicks, then tries to match each ringed lock to its row-color in 3 more clicks. Lands in the ~2-min/level target.
  - **(c) Planning depth**: **no strict planning requirement (per `difficulty-rules.md` § 2 c, L1)**. Once the rule is understood, the three lock targets are independent (each in its own row); the player solves them sequentially in any order with no interaction between rows.
  - **(d) Step budget**: 30. Witness is 6 clicks; budget gives ~5× headroom for exploration and over-cycling (clicking past the desired tint and having to re-cycle).

### Level 2 — base system + 1 new mechanic
- **Cell-color rule (L2)**: `cell_color(gx, gy) = col_tint[gx] if col_tint[gx] != BACKGROUND else row_tint[gy]`. Column overrides row when set; otherwise row shows.
- **Sprites placed in L2**: 64 cells; 8 row markers; 8 column markers (newly present); 5 lock targets:
  - Lock A: cell `(1, 2)`, required color 8 (red).
  - Lock B: cell `(6, 2)`, required color 14 (green). (Same row 2 as Lock A but different required color → row 2 cannot satisfy both alone; column override required for at least one.)
  - Lock C: cell `(4, 5)`, required color 11 (yellow).
  - Lock D: cell `(2, 6)`, required color 11 (yellow). (Column 2 is shared between Lock A's column 1 and Lock D's column 2 — separate columns, no column conflict; but Lock D and Lock A differ in row, so testing both row options.)
  - Lock E: cell `(5, 1)`, required color 8 (red).
- `step_budget = 60`.
- **Mechanics required by the witness** (= N+1 = 2):
  - **M1 (row-tint cycling)** — carried forward from L1.
  - **M2 (column-tint cycling with override rule)**: clicking a column marker cycles its tint through the same `2→8→11→14→2` cycle; in any column where col_tint != background, every cell in that column shows col_tint instead of its row's tint.
- **Necessity per mechanic (counterfactual)**:
  - M1 (row-tint): L2 cannot be solved without triggering M1 because Lock C `(4, 5)` requires color 11 in row 5; if M1 is never used, row 5's tint stays at background and column 4 must be set to 11 to satisfy Lock C. But with col_4 = 11, **every** cell in column 4 shows 11. There is no other lock in column 4, so Lock C alone could in principle be solved by column-only — let me name a tighter target. **Lock E** `(5, 1)` requires color 8 in row 1. If only column-clicks are used, col_5 = 8 satisfies Lock E. But col_5 = 8 also recolors cell `(5, 2)`, which is the column position of Lock B `(6, 2)` — wait, different gx (5 vs 6). Let me re-check: cells in column 5 are `(5, *)`, and Lock B is at `(6, 2)`, column 6 — different column. So col_5 = 8 doesn't break Lock B. **Tighter argument**: if no row marker is ever clicked, then for any lock target `(c, r)` with required color X, column c must be set to X. Apply to all 5 locks:
    - col_1 = 8 (for A), col_6 = 14 (for B), col_4 = 11 (for C), col_2 = 11 (for D), col_5 = 8 (for E). All five columns distinct → no inter-column conflict. So column-only IS a valid path. **Bug in design.** Let me fix L2 to force row necessity:
      - **Revised L2 lock targets**:
        - Lock A: `(1, 2)`, required 8.
        - Lock B: `(1, 5)`, required 14. (Same column 1 as Lock A → col_1 cannot be both 8 and 14, so at least one of A/B must use row.)
        - Lock C: `(4, 2)`, required 11. (Same row 2 as Lock A → row 2 cannot be both 8 and 11, so at least one of A/C must use column.)
        - Lock D: `(6, 6)`, required 14.
        - Lock E: `(3, 4)`, required 8.
      - Now: column-only solution requires col_1 = 8 (A) and col_1 = 14 (B), impossible. Row-only solution requires row 2 = 8 (A) and row 2 = 11 (C), impossible. Both M1 and M2 are necessary.
  - M2 (column-override): L2 cannot be solved without triggering M2 because Lock C `(4, 2)` and Lock A `(1, 2)` both sit in row 2 with different required colors (11 vs 8). Row 2's tint can be at most one color. So at least one of these locks must be solved by setting its column (override). With M2 disabled (no column clicks), at most one of A/C is satisfied, leaving the other unsatisfied.
  - M1 (row-tint): L2 cannot be solved without triggering M1 because Lock A `(1, 2)` and Lock B `(1, 5)` both sit in column 1 with different required colors (8 vs 14). Column 1's tint can be at most one color. So at least one of A/B must be solved by setting its row (row 2 or row 5) and leaving column 1 unset (so row tint shows through). With M1 disabled, at most one of A/B is satisfied.
- **Witness solution** (a fully-informed player picks an efficient assignment). One valid assignment:
  - row 2 = 8 (1 click) → satisfies Lock A `(1, 2)` (col_1 unset → row wins → red). Cell `(4, 2)` also becomes red — but Lock C `(4, 2)` wants yellow, so column 4 must override.
  - col 4 = 11 (2 clicks) → cell `(4, 2)` becomes yellow → Lock C satisfied. (Also recolors `(4, 0..7)` to yellow, but no lock there.)
  - col 1 unchanged (background = 2) → Lock B `(1, 5)` not yet satisfied. Need row 5 = 14 (3 clicks).
  - row 5 = 14 (3 clicks) → cell `(1, 5)` = 14 (col_1 unset, row 5 = 14, override doesn't apply). Lock B satisfied. (Also `(4, 5)` would be 14 but col_4 = 11 overrides → cell shows 11, no lock there.)
  - row 6 = 14 (3 clicks) → cell `(6, 6)` = 14 (col_6 unset, row 6 = 14). Lock D satisfied.
  - row 4 = 8 (1 click) → cell `(3, 4)` = 8 (col_3 unset, row 4 = 8). Lock E satisfied.
  - **Total clicks: 1 + 2 + 3 + 3 + 1 = 10.** Action sequence: 1× click row-marker 2 (at `(4, 20)`), 2× click col-marker 4 (at `(32, 4)`), 3× click row-marker 5 (at `(4, 38)`), 3× click row-marker 6 (at `(4, 44)`), 1× click row-marker 4 (at `(4, 32)`).
- **Difficulty justification**:
  - **(a) Random-resistance**: 16 markers (8 row + 8 col), each 6×6 = 36 px, total marker area = 576 / 4096 ≈ 14% of frame. Random clicks have ~14% per-click marker-hit rate; expected ~8 hits in 60 clicks. The probability that random clicks produce the *specific* tint configuration meeting all 5 lock requirements is well under 1/10000.
  - **(b) Human-tractable**: 90 seconds to 2 min. Player must (1) discover that column markers exist (visual difference from L1) and that they override; (2) reason about which locks share rows or columns and need override vs. not. ~2-min target.
  - **(c) Planning depth**: **moderate planning required (post-discovery)**. Post-discovery decision space at level start: 16 valid first actions (8 row markers × 1 click each + 8 col markers × 1 click each, all 16 currently available). One plausible-but-wrong alternative: a fully-informed player might try to satisfy Lock A first by setting row 2 = 8, then attempt Lock C by setting row 2 = 11 (overwriting), then realize the conflict. The witness's reasoning chain: identify each pair of locks sharing a row or column → pick which one in each pair gets the row-tint and which gets the column-override → execute in any order (no order dependency). The wrong path (row-only or col-only) fails because the conflict pairs (A↔C in row 2; A↔B in column 1) cannot both be satisfied with a single mechanism.
  - **(d) Step budget**: 60. Witness is 10 clicks; budget gives 6× headroom — generous to allow a player to over-cycle on initial exploration of column markers (each column marker click cycles 1/4 of a full loop, so a player exploring all 8 column markers takes 8 clicks just to "see what they do", leaving 52 for the actual puzzle).

### Level 3 — system + 1 new mechanic
- **Cell-color rule (L3)**: `cell_color(gx, gy) = max_brightness(row_tint[gy], col_tint[gx])` where brightness is palette index (so the higher palette index wins; background `2` loses to any active tint; if both equal background, cell renders background). Concretely: `if row_tint[gy] == BG and col_tint[gx] == BG: render BG; elif row_tint[gy] >= col_tint[gx]: render row_tint; else: render col_tint`.
- **Sprites placed in L3**: 64 cells; 8 row markers; 8 column markers; 6 lock targets:
  - Lock A: `(1, 2)`, required 8 (red, the dimmest non-BG tint).
  - Lock B: `(6, 2)`, required 14 (green, the brightest tint).
  - Lock C: `(2, 5)`, required 11 (yellow).
  - Lock D: `(5, 5)`, required 8 (red).
  - Lock E: `(3, 7)`, required 14 (green).
  - Lock F: `(6, 7)`, required 11 (yellow).
- `step_budget = 80`.
- **Mechanics required by the witness** (= L2-count + 1 = 3):
  - **M1 (row-tint cycling)** — carried forward.
  - **M2 (column-tint with brighter-wins blend)** — *evolved* from L2's column-overrides-row to a brighter-of-the-two rule. The L2 override rule is the *special case* of L3's brighter-wins where col_tint > row_tint (which is true whenever col is set and row is BG). The new degree of freedom L3 adds is: row can be set BRIGHTER than column to win the cell, even when the column is set.
  - **M3 (brighter-wins blend rule)**: when both row and column for a cell are active, the cell shows whichever has higher palette index. This means a "dimmer" column tint can be defeated by a "brighter" row tint of the same cell — useful for surgically preserving a row tint in specific cells while tinting other rows of the same column differently.
- **Necessity per mechanic (counterfactual)**:
  - M1 (row-tint): L3 cannot be solved without triggering M1 because Lock A `(1, 2)` (red) and Lock C `(2, 5)` (yellow) both sit in column 1's neighborhood, and crucially Lock D `(5, 5)` (red) and Lock C `(2, 5)` (yellow) sit in **the same row 5** with different required colors. By the same row-conflict argument as L2, at least one of C/D requires its column to dominate. To force row necessity: Lock A `(1, 2)` (red) and Lock B `(6, 2)` (green) in **the same row 2**. If column-only mode: col_1 = 8, col_6 = 14 — works for A and B. So M1 still might not be forced. **Tighter**: Lock A `(1, 2)` red and Lock E `(3, 7)` green and Lock F `(6, 7)` yellow — column 1 = 8 for A; column 3 = 14 for E; column 6 = 11 for F. Column-only still works. Need to engineer a forced row use. **Concrete force**: Lock D `(5, 5)` red and Lock F `(6, 7)` yellow share *neither* row nor column, but Lock B `(6, 2)` green and Lock F `(6, 7)` yellow share **column 6**: col_6 cannot be both 14 and 11. So one of B/F must use row. row 2 = 14 satisfies B (row wins because col_6 unset OR col_6 < row_2); row 7 = 11 satisfies F. So row clicks are forced. **L3 cannot be solved without M1 because Lock B `(6, 2)` and Lock F `(6, 7)` share column 6 with different required tints (14 and 11) — column 6 can be set to at most one value; the other lock must be solved by setting its row.**
  - M2 (column-tint, blended): L3 cannot be solved without triggering M2 because Lock C `(2, 5)` (yellow) and Lock D `(5, 5)` (red) share **row 5** with different required tints (11 and 8) — row 5 can be at most one tint; at least one of C/D must use its column.
  - M3 (brighter-wins): L3 cannot be solved without triggering M3. Force scenario: Lock E `(3, 7)` requires green (14); to satisfy E, either row 7 = 14 OR col_3 = 14. Suppose we try row 7 = 14 — then cell `(6, 7)` = max(row_7, col_6). Lock F there requires yellow (11). If col_6 = 11 (for Lock F), then cell `(6, 7)` = max(14, 11) = 14 — wrong, we want 11. So Lock F cannot be satisfied via col_6 alone if row 7 is also set high. Alternative: col_6 = 11 and row 7 unset (so row_7 = BG = 2); then cell `(6, 7)` = max(2, 11) = 11 ✓. But then Lock E `(3, 7)` requires col_3 = 14, with row_7 = 2 → cell `(3, 7)` = max(2, 14) = 14 ✓. So one path: row 7 unset, col_3 = 14, col_6 = 11. **But then Lock B `(6, 2)` requires green (14)**: row 2 unset → cell `(6, 2)` = max(2, col_6=11) = 11, wrong; row 2 = 14 → cell `(6, 2)` = max(14, 11) = 14 ✓. So row 2 = 14. Then cell `(6, 2)` = 14 (M3 brighter-wins rule actively let row 2's bright green outshine col 6's dimmer yellow — this is the exact place M3 is exercised). Without M3 (i.e. with L2's pure override rule), cell `(6, 2)` would forcibly equal col_6 = 11 ≠ 14, and Lock B fails. The brighter-wins blend is what lets Lock B succeed when its column is set to a dimmer value for another constraint.
- **Witness solution**: based on the above, set row 2 = 14 (3 clicks), col_3 = 14 (3 clicks), col_6 = 11 (2 clicks), col_1 = 8 (1 click for Lock A — cell `(1, 2)` = max(row_2=14, col_1=8) = 14 ≠ 8 — **conflict!** Lock A wants red but row 2 is green and brighter wins. Need to redesign or split Lock A's row.
  - Re-engineer the witness: place Lock A in a different row to avoid row-2 conflict. Or: don't set row 2 = 14; instead use col_6 = 14 for Lock B and find another way for Lock F.
  - **Re-derive cleanly**: required tints by cell:
    - A: `(1, 2)` = 8.
    - B: `(6, 2)` = 14.
    - C: `(2, 5)` = 11.
    - D: `(5, 5)` = 8.
    - E: `(3, 7)` = 14.
    - F: `(6, 7)` = 11.
  - Constraints: cells in same row must end with required colors that the row+column combo can deliver.
  - Try: row 2 = 8, col_6 = 14, col_3 = 14, col_2 = 11, row 5 = 8, col_6 = 11 (conflict with col_6=14)... col_6 can only be one value.
  - Try: row 2 = 8 (Lock A: max(BG, BG)=BG no — wait, row 2 = 8 → cell `(1, 2)` = max(8, col_1). If col_1 unset (BG=2), cell = 8 ✓. cell `(6, 2)` = max(8, col_6). For Lock B = 14, col_6 must be 14 (and brighter wins → 14). ✓
  - row 5 = 8 (Lock D: cell `(5, 5)` = max(8, col_5)). col_5 unset → 8 ✓. cell `(2, 5)` = max(8, col_2). Lock C wants 11. col_2 = 11 → cell = max(8, 11) = 11 ✓.
  - row 7: Lock E wants 14 at `(3, 7)`. Lock F wants 11 at `(6, 7)`. With col_6 = 14 already (for Lock B): cell `(6, 7)` = max(row_7, 14). For this to equal 11, both row_7 and col_6 must be ≤ 11, but col_6 = 14 > 11. **Contradiction**. Lock F unsolvable with this arrangement.
  - Conclusion: the L3 design has a contradiction. **Need to redesign locks** so a valid assignment exists.
  - **Cleaner L3 design**: pick lock positions such that no column is forced into two different bright values. Place locks across DISTINCT columns and DISTINCT rows where possible, with a single forced "row-must-beat-column" intersection that exercises M3.
  - **REVISED L3 lock placement**:
    - Lock A: `(1, 2)`, required 8 (red).
    - Lock B: `(4, 2)`, required 14 (green). (Same row 2 as A; conflict → use M2 column override for B or A.)
    - Lock C: `(2, 5)`, required 11 (yellow).
    - Lock D: `(5, 5)`, required 14 (green). (Same row 5 as C; conflict → M2 needed for one.)
    - Lock E: `(4, 7)`, required 8 (red). (Same column 4 as B; conflict on column 4 → if col_4 = 14 for B, Lock E needs row 7 = 8 to override col_4 — but max(8, 14) = 14 ≠ 8. So col_4 must be set such that brighter-wins yields 8 at `(4, 7)`. Only way: col_4 ≤ 8 AND row_7 = 8. So col_4 = 8 (or BG) and row_7 = 8. But then for Lock B `(4, 2)` requiring 14: cell = max(row_2, col_4=8). Need row_2 = 14. row_2 = 14 conflicts with Lock A `(1, 2)` requiring 8. So Lock A must use col_1 = 8 to override row_2 = 14: cell `(1, 2)` = max(14, 8) = 14 ≠ 8. **Conflict again** because brighter-wins beats the override attempt.)
    - This shows M3 introduces *real* design constraints. The brighter-wins rule blocks the L2-style "use column override to defeat row" trick when the row is brighter than the column. I need to design L3 so the *forced* path requires the row to be the BRIGHTER one (exercising M3 in the "row dominates" direction), with no L2-style "column always wins" backup available.
  - **TRIED-AND-VALIDATED L3 design**:
    - Lock A: `(1, 2)`, required **14** (green, the brightest).
    - Lock B: `(4, 2)`, required 11 (yellow). Same row 2 as A.
    - Lock C: `(2, 5)`, required 8 (red).
    - Lock D: `(5, 5)`, required 14 (green). Same row 5 as C.
    - Lock E: `(7, 7)`, required 11 (yellow).
    - Lock F: `(1, 6)`, required 8 (red). Same column 1 as A.
    - Solution attempt:
      - For Lock A `(1, 2)` = 14: need cell brighter-wins to land at 14. Two paths: (a) row_2 = 14 and col_1 ≤ 14 (always true), so cell = max(14, col_1) = 14 always (or = col_1 if col_1 = 14, but then = 14). Hmm. Actually max(14, anything else) = 14 always since 14 is the highest. So row_2 = 14 satisfies A regardless of col_1. But then cell `(4, 2)` = max(14, col_4). For Lock B = 11, need max(14, col_4) = 11, impossible since max ≥ 14. **So row_2 cannot be 14 if Lock B needs 11 in same row.** Path (b): col_1 = 14, row_2 ≤ 14. cell `(4, 2)` = max(row_2, col_4). For Lock B = 11: max(row_2, col_4) = 11 → both ≤ 11 with at least one = 11. Set col_4 = 11 → cell = max(row_2, 11) = 11 if row_2 ≤ 11 ✓. So set row_2 = BG (or anything ≤ 11). Setting row_2 = BG keeps cell `(1, 2)` = max(BG=2, col_1=14) = 14 ✓ (Lock A). And cell `(4, 2)` = max(2, 11) = 11 ✓ (Lock B).
      - For Lock C `(2, 5)` = 8: max(row_5, col_2) = 8. Both ≤ 8 with one = 8. Set row_5 = 8.
      - For Lock D `(5, 5)` = 14: max(row_5=8, col_5) = 14 → col_5 = 14 ✓.
      - For Lock E `(7, 7)` = 11: max(row_7, col_7) = 11. Set col_7 = 11 (and row_7 = BG).
      - For Lock F `(1, 6)` = 8: max(row_6, col_1=14) = max(row_6, 14) = 14 always since col_1 = 14. **Conflict — Lock F unreachable.**
      - Move Lock F to a different column. **Revise Lock F position**: `(7, 1)`, required 8.
        - cell `(7, 1)` = max(row_1, col_7=11). For = 8, max(row_1, 11) = 8 impossible since 11 > 8. Conflict.
      - **Revise Lock F position**: `(6, 6)`, required 8.
        - cell `(6, 6)` = max(row_6, col_6). Set row_6 = 8, col_6 = BG (or ≤ 8). cell = max(8, BG) = 8 ✓.
        - But check: does col_6 affect any other lock? Locks at `(*, 2)`: only `(1,2)` and `(4,2)`, no `(6, 2)`. Locks at `(*, 5)`: only `(2,5)` and `(5,5)`, no `(6, 5)`. Locks at `(*, 7)`: only `(7, 7)`, no `(6, 7)`. So col_6 is free. ✓
      - **Final L3 lock placement**:
        - Lock A: `(1, 2)`, required 14.
        - Lock B: `(4, 2)`, required 11.
        - Lock C: `(2, 5)`, required 8.
        - Lock D: `(5, 5)`, required 14.
        - Lock E: `(7, 7)`, required 11.
        - Lock F: `(6, 6)`, required 8.
      - **Witness assignment**: col_1 = 14 (3 clicks), col_4 = 11 (2 clicks), row_5 = 8 (1 click), col_5 = 14 (3 clicks), col_7 = 11 (2 clicks), row_6 = 8 (1 click). Total: 3+2+1+3+2+1 = **12 clicks**.
      - But wait — does this exercise M3 (brighter-wins in the "row dominates" direction)? The witness above doesn't actually require row to beat column; rows are set only when columns are unset for those cells. Let me re-check necessity of M3.
      - Without M3 (L2-style pure column-override): cell color = col_tint if col set, else row_tint. Apply to witness:
        - Lock A `(1, 2)`: col_1 = 14 → cell = 14 ✓.
        - Lock B `(4, 2)`: col_4 = 11 → cell = 11 ✓.
        - Lock C `(2, 5)`: col_2 = BG → cell = row_5 = 8 ✓.
        - Lock D `(5, 5)`: col_5 = 14 → cell = 14 ✓.
        - Lock E `(7, 7)`: col_7 = 11 → cell = 11 ✓.
        - Lock F `(6, 6)`: col_6 = BG → cell = row_6 = 8 ✓.
        - **All locks satisfied without using M3.** L2 mechanics suffice. M3 not necessary for this design.
      - I need to ADD a lock that ONLY M3 can solve. The defining property of M3 (brighter-wins in row-dominates direction) is: a cell where row tint must "win" over a column tint that's been forced to a dimmer value by another constraint in that column.
      - Construct: Lock G at cell `(c, r)` where col_c must be set to value V (dim, e.g. 8) for another lock G'in column c, but Lock G itself wants a brighter value W (> V, e.g. 14). For G to be satisfied: row_r = W (so brighter-wins picks W over col_c = V). Critically, V < W is required for "row wins by brightness".
      - Pick concretely: Lock G at `(2, 3)` requiring 14. Lock G' at `(2, 6)` requiring 8. Same column 2. col_2 cannot be both 14 and 8.
        - If col_2 = 8 (for G'), then cell `(2, 3)` = max(row_3, 8). For G = 14, need row_3 = 14. ✓ (M3 used: row 3 = 14 dominates col_2 = 8.)
        - If col_2 = 14 (for G), then cell `(2, 6)` = max(row_6, 14) = 14 ≠ 8 (G' fails).
        - So the only way: col_2 = 8 + row_3 = 14 — exercises M3.
      - **FINAL L3 lock placement** (7 locks now):
        - Lock A: `(1, 2)`, required 14. (Solved by col_1 = 14.)
        - Lock B: `(4, 2)`, required 11. (Solved by col_4 = 11.)
        - Lock C: `(2, 6)`, required 8. (Solved by col_2 = 8.)
        - Lock D: `(5, 5)`, required 14. (Solved by col_5 = 14.)
        - Lock E: `(7, 7)`, required 11. (Solved by col_7 = 11.)
        - Lock F: `(6, 6)`, required 8. (Solved by row_6 = 8 with col_6 = BG.)
        - **Lock G: `(2, 3)`, required 14**. Forces M3 — col_2 must be 8 (for C), so row_3 = 14 needed.
      - Witness clicks:
        - col_1 = 14: 3 clicks.
        - col_4 = 11: 2 clicks.
        - col_2 = 8: 1 click.
        - col_5 = 14: 3 clicks.
        - col_7 = 11: 2 clicks.
        - row_6 = 8: 1 click.
        - row_3 = 14: 3 clicks.
        - Total: **15 clicks.**
      - Verify all locks satisfied:
        - A `(1, 2)`: max(row_2=BG, col_1=14) = 14 ✓.
        - B `(4, 2)`: max(BG, col_4=11) = 11 ✓.
        - C `(2, 6)`: max(row_6=8, col_2=8) = 8 ✓ (both equal, no conflict).
        - D `(5, 5)`: max(row_5=BG, col_5=14) = 14 ✓.
        - E `(7, 7)`: max(row_7=BG, col_7=11) = 11 ✓.
        - F `(6, 6)`: max(row_6=8, col_6=BG=2) = 8 ✓.
        - G `(2, 3)`: max(row_3=14, col_2=8) = 14 ✓ (M3 in action — row dominates).
      - Verify M3 necessity: without M3, cell `(2, 3)` = col_2 = 8 (column override) ≠ 14. Lock G unsatisfied. ✓
- **Witness solution** (15 actions): click each marker's center pixel:
  - col_1: marker centered at `(11, 4)`. Click 3 times: `[ACTION6@(11, 4), ACTION6@(11, 4), ACTION6@(11, 4)]`.
  - col_4: marker at `(29, 4)`. Click 2 times.
  - col_2: marker at `(17, 4)`. Click 1 time.
  - col_5: marker at `(35, 4)`. Click 3 times.
  - col_7: marker at `(47, 4)`. Click 2 times.
  - row_6: marker at `(4, 47)`. Click 1 time.
  - row_3: marker at `(4, 23)`. Click 3 times.
  - Full sequence: `[ACTION6@(11,4)×3, ACTION6@(29,4)×2, ACTION6@(17,4)×1, ACTION6@(35,4)×3, ACTION6@(47,4)×2, ACTION6@(4,47)×1, ACTION6@(4,23)×3]`.
- **Difficulty justification**:
  - **(a) Random-resistance**: 16 markers × 36 px = 576 px = 14% of 4096. Random clicks have ~14% per-click marker-hit rate; expected ~11 marker-hits in 80 clicks. The probability of producing the specific 15-click configuration that satisfies all 7 locks (each requiring a precise tint) is well under 1/10000.
  - **(b) Human-tractable**: 2–3 minutes. Player must (1) discover that the L2 column-override rule no longer always holds in L3 — by clicking and observing that some cells "stay" at row tint despite column being set; (2) infer the brighter-wins rule (the rendered color is always the higher palette index of row vs column); (3) plan the assignment to satisfy 7 locks under both row+column constraints and M3.
  - **(c) Planning depth**: **planning challenging even for an attentive human**. Post-discovery decision space at level start: 16 valid first actions (all markers clickable). Greedy / monotone-progress / follow-the-obvious-gradient heuristics fail because:
    - **Trivial heuristic that fails**: "for each lock, set its column to the required color" (the L2 strategy). This would have col_2 = 8 for Lock C, col_2 = 14 for Lock G — impossible. The L2 strategy requires every lock to have an independent column, but Lock C and Lock G share column 2 with different required colors.
    - **Where the heuristic diverges from witness**: at Lock G `(2, 3)`. The greedy player attempts col_2 = 14, which breaks Lock C (col_2 must be 8 to satisfy max(row_6, 8) = 8 at `(2, 6)` since row_6 = 8). The witness instead sets col_2 = 8 AND row_3 = 14, exploiting the brighter-wins rule to make row 3's green win over col 2's red specifically at cell `(2, 3)`. The greedy player's failure: they see col_2 = 8 satisfies C and reach for col_2 = 14 to satisfy G, hitting the conflict, then has to back out and recognize "I need row_3 instead, but only because brighter-wins lets row 3 dominate at this cell". This 2-3 step lookahead — recognizing that Lock G's row will dominate col_2 — is the planning depth.
  - **(d) Step budget**: 80. Witness is 15 clicks; budget gives ~5× headroom. Generous over the witness, larger than L2's 60 (no shrinking across levels), and enough room for a player to over-cycle and explore the brighter-wins rule.

## 5. Action mapping

| Action | Semantic | Gating |
|---|---|---|
| `ACTION6` | Click at `(x, y)` in pixel space. The game converts to grid coords; if the click hits a row marker, cycles that row's tint; if it hits a column marker, cycles that column's tint; if it hits a cell or empty space, no-op. | Always available. |

`available_actions = [6]`. No movement, no ACTION5, no ACTION7. Pure-click family.

`_get_valid_actions()` returns the default — `NovaBaseGame` enumerates all valid `(x, y)` for ACTION6 over the 64×64 frame. In practice the agent learns to click only on markers (effective hits land on the 16 marker sprites; other clicks are no-op).

## 6. HUD and per-game state

**HUD**:
- `StepCounterHud(RenderableUserDisplay)` — bar of width 48 px on row 60. Drains 1 per action. When reaches 0, `self.lose()` fires.

**Per-game internal state** (instance attributes):
- `row_tints: list[int]` of length 8 — current palette index for each row's tint. Initialised to `[BACKGROUND] * 8 = [2] * 8` in `on_set_level`.
- `col_tints: list[int]` of length 8 — same for columns. Initialised to `[2] * 8` (and only used in L2/L3 where col markers are present).
- `tint_cycle: list[int] = [2, 8, 11, 14]` — the cycle order. Each marker click does `idx = (tint_cycle.index(current) + 1) % 4`.
- `level_rule: int = self._current_level_index` — derives the cell-color-rule branch (0/1/2 → row-only / column-overrides-row / brighter-wins).
- `BACKGROUND = 2`.
- A method `_recompute_cells()` that, after each click, walks the 8×8 grid of cell sprites and sets each cell's pixels to the rule output for its `(gx, gy)`.
- A method `_check_win()` that, after each recompute, checks every `lock_target` sprite; for each, finds the cell beneath it, compares the cell's current rendered color to the lock's required color (encoded in the lock's perimeter pixels). If all locks satisfied, calls `self.next_level()`.
- A method `_render_lock_state()` that updates each lock_target's four corner pixels: white (0) if satisfied, off-black (4) if not.

No selection state, no animation phases, no undo stack — pure-click + immediate state update keeps the implementation small.

## 7. Win condition

After each ACTION6 click that lands on a marker:
1. Cycle the marker's tint.
2. Recompute every cell's pixels based on the current `(row_tints, col_tints, level_rule)`.
3. For every `lock_target` sprite at cell `(gx, gy)`: check whether the cell's rendered color == the lock's required color (read from the lock sprite's perimeter pixel value).
4. If all lock targets are satisfied → `self.next_level()`.

After level 3's lock targets are satisfied, the engine's `next_level()` falls through to `self.win()`.

## 8. Lose condition

Step counter `step_counter_hud` drains 1 per action (regardless of whether the click hit a marker or was a no-op miss). When the counter reaches 0 and the level is unsatisfied, `self.lose()` fires.

There is no other lose condition (no hazards, no instant-fail).

## 9. Novelty note

(Copy-extending `mechanic-pick.md` § Similarity check, here applied to the now-fleshed-out spec.)

**Closest taxonomy matches:**
- `lp85` (row-col-shift-grid): physically permutes cells in a row/column. Mine: cells stay put; only their fill is recolored.
- `vc33` (row-column-swap-stripe): clicks swap stones across a marker. Mine: clicks recolor an entire row/column with no physical motion.
- `ft09` (stamp-3x3-paint): clicks stamp a 3×3 pattern of color around a clicked cell. Mine: clicks recolor an 8-cell row OR an 8-cell column; markers are at the edge, never inside the playfield.

**Closest prior-game matches:**
- `qx7p` (column-shift-row-align): slides color-bands. Mine: cycles the *value* of each row/column tint in place. No bands move.
- `qf8m` (rook-cross-toggle): clicked tile flips a (2N-1)-cell row+col cross. Mine: row-marker clicks affect only its row; column-marker clicks only its column; the row+column intersection emerges from the *combiner rule* (override at L2, brighter-wins at L3), not from a coupled flip.
- `xn5p` (chamber-stamp-partition): walks pawn + stamps walls to subdivide regions. Mine: no pawn, no walls — pure marker-click puzzle.
- `mz6t` (majority-vote-stabilize): cycles per-cell with majority-vote propagation. Mine: cycles per-row / per-column with no propagation.

**Concrete distinguishing rule** (the one rule the player would name to describe the game's identity): *"Click left-edge markers and top-edge markers to change row hues and column hues; the cell's color is decided by combining its row hue and column hue (in a level-specific way), and the goal is to make the ringed target cells display their required color."* No prior shares this row+column tint combiner mechanic. The brighter-wins blend rule at L3 specifically is unique to this candidate.
