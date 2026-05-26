# mechanic-spec.md — dh4j (tile-coded-stride) — v3

**Revision log**: v3 addresses both v2 issues from `critique-revisions.md` v2:
- v2 Issue 1 → §3 (pivot sprite): replaced upward-arrow interior with a "+" cross (allowed topological symbol). `avatar_pivot_pending` corner accent simplified to a 2×2 white block.
- v2 Issue 2 → §3, §4 L3, §6: **pivot is now one-shot** — consumed on the next press after landing (regardless of success). Pivot cell sprite swaps to `floor_pip_2_*` after consumption. The greedy "spam UP" heuristic now irrecoverably fails (vs ties at v2).

v2 in turn addressed all 8 issues from v1 critique:
- Consolidated to leap-over interpretation (intermediate fly-over, destination must be open & in-grid).
- Filter swap changed to 2↔3 (1-pip stays stride-1).
- L1 redesigned with 1-row wall barrier at y=3.
- L2 redesigned with 2-row wall barrier (y=2..3).
- L3 with 3-row wall barrier (y=2..4) and stride-bonus pivot.
- Avatar simplified to single 2×2 white center (no "face dots").
- HUD legend chip pixel layout specified.
- Negative-similarity 8-dimension re-check.

## 1. Title
*Stride Pips* — a tile-coded-stride leap-over puzzle. Working title (NOT visible in-game).

## 2. Mechanic family
**tile-coded-stride** (objectness + basic physics + basic geometry/topology).

Each walkable cell visibly displays a *stride pip count* (1, 2, or 3 small pips painted on its tile face). When the player presses a cardinal-arrow action, the avatar **leaps** by N cells in the pressed direction (where N is the origin cell's pip count under the currently-active legend). The leap is a destination-only translation: the avatar's destination is the cell N units in the pressed direction; if the destination is a wall or outside the grid, the press is a no-op (avatar stays). **Intermediate cells along the leap are fly-over** — they have no interaction effect (the avatar does not collide with intermediate walls; it visually flies over them in an animated cell-by-cell rendering for legibility). This is the central novelty: leaps cross walls, making variable stride a *path-enabler*, not just a step-budget optimization.

Levels compose by adding:
- a **filter cell** (L2) which globally toggles the active legend between Yellow (identity: 1→1, 2→2, 3→3) and Blue (2↔3 swap: 1→1, 2→3, 3→2), visualised by recoloring every floor cell's pip accent;
- a **facing-pivot cell** (L3) which, when landed on, sets a one-shot **stride-bonus +1** for the next press. The pending bonus is visualised as a small "+1" arc decoration around the avatar until the next press resolves.

Prior categories used: **objectness** (avatar, walls, goal, filter, pivot are persistent sprites), **basic physics** (discrete N-cell translation per press; walls are destination obstacles), **basic geometry & topology** (the leap is a 2D cardinal translation; bonus addition is arithmetic).

## 3. Sprite roster

Display: each game cell is **8×8 pixels**. Level `grid_size = (64, 64)` (full canvas, 1:1 — no engine scaling). The playfield occupies 8 columns × 7 rows of cells (cell positions: x ∈ {0, 8, 16, 24, 32, 40, 48, 56}; y ∈ {0, 8, 16, 24, 32, 40, 48}). Pixel rows 56..63 are the HUD area (8 pixel rows): rows 56..62 for the legend display, row 63 for the step counter bar.

Palette (deliberate subset):
- 0 (white) — accent white, inner pip color in pivot, target inner.
- 1 (off-white) — floor interior.
- 2 (light-grey) — dim accents on inactive legend chip.
- 3 (grey) — letter-box / HUD background.
- 4 (off-black) — wall fill.
- 5 (black) — cell outlines, step-counter empty.
- 6 (magenta) — avatar.
- 10 (light-blue) — blue-legend pip accent.
- 11 (yellow) — yellow-legend pip accent / step-counter fill.
- 12 (orange) — filter-cell accent.
- 13 (maroon) — pivot-cell accent.
- 14 (green) — goal-cell accent.

Sprites (all 8×8 unless noted):

- `floor_pip_1_yellow` — 8×8 cell, 1-pixel black (5) outer border, off-white (1) interior, single 2×2 yellow (11) pip centered at pixel (3, 3)..(4, 4). Tags `["floor"]`. Layer 0.
- `floor_pip_2_yellow` — 8×8 cell, same border + interior, two 2×2 yellow pips at pixel (2, 3)..(3, 4) and (5, 3)..(6, 4). Tags `["floor"]`. Layer 0.
- `floor_pip_3_yellow` — 8×8 cell, same border + interior, three 1×2 yellow pips at columns 2, 4, and 6 (each 1 wide × 2 tall) on row 3..4. Tags `["floor"]`. Layer 0.
- `floor_pip_1_blue`, `floor_pip_2_blue`, `floor_pip_3_blue` — same shapes but pips in light-blue (10). Used when the active legend is Blue.
- `wall_block` — 8×8 solid off-black (4) interior with 1-pixel black (5) border. Tags `["wall"]`. Layer 0.
- `goal_cell` — 8×8 frame: pixels 0 (top row + bottom row + left col + right col) green (14), inner 6×6 with a 4×4 white core, and inside that a central 2×2 green inner mark. Tags `["goal"]`. Layer 1 (drawn above floor).
- `filter_cell` — 8×8 frame: 1-pixel black (5) outer border, interior 6×6 orange (12); inside the interior a horizontal stripe of yellow (11) at pixel row 3 and a horizontal stripe of light-blue (10) at pixel row 4 — the two-color stripe visually suggests "swap of yellow ↔ blue". Tags `["filter"]`. Layer 1.
- `pivot_cell` — 8×8 frame: 1-pixel black (5) outer border, interior 6×6 maroon (13); inside the interior, a centered **"+" cross** in white (0) — horizontal 3-pixel stripe at row 4, columns 2..6 (cols 2, 3, 4, 5, 6 — 5 pixels), and vertical 3-pixel column at column 4, rows 2..6 (rows 2, 3, 4, 5, 6 — 5 pixels). The crossing pixel (4, 4) is shared. This produces a clean "+" topological symbol abstractly suggesting "bonus / addition" without directional or symbolic content. Tags `["pivot"]`. Layer 1.
- `pivot_floor_pip_2_yellow` — 8×8 composite: combines `floor_pip_2_yellow`'s pip layout with the pivot's maroon ring + "+" cross overlay. The two-pip yellow accents are at (2, 3)..(3, 4) and (5, 3)..(6, 4); the cell border is maroon (13) (instead of black 5); a centered white (0) "+" cross sits at column 4, rows 1..2 and row 1..2 columns 3..5 (small, fitting between the pip rows). Tags `["floor", "pivot"]`. Layer 1.
- `pivot_floor_pip_2_blue` — same composite but with blue (10) pips.
- `avatar_normal` — 8×8 magenta (6) rounded sprite: outer perimeter has -1 (transparent) at the four corners (pixels (0, 0), (0, 7), (7, 0), (7, 7)), filling the rest with magenta; a central **2×2 white (0) block at pixels (3, 3)..(4, 4)** (abstract focal accent — NOT a pair of "face" dots, just a single small square in the center). Tags `["avatar"]`. Layer 2.
- `avatar_pivot_pending` — same magenta blob as `avatar_normal` plus an abstract 2×2 white (0) corner accent at top-right pixels (5, 1)..(6, 2) — a small square decoration indicating "bonus pending" without arrow or symbol content. Tags `["avatar"]`. Layer 2. Used as a swap replacement (via `InteractionMode`) when `_pending_bonus == 1`.

HUD widgets (rendered via `RenderableUserDisplay` subclasses, atop the playfield frame):

- `StepCounterHud` — renders pixel row y=63 across all 64 columns. Left portion (steps_remaining / max_steps) is yellow (11); right portion is off-black (4). Updated each `step()` call.
- `LegendChipHud` — renders pixel rows y=56..62 (7 rows) across all 64 columns:
  - **Yellow chip** at pixels (x=0..31, y=56..62). 32 columns × 7 rows.
    - Three vertically-stacked rows, each 2 px tall + 1 px gap:
      - Row 1 (y=56..57): "1-pip → stride-1" mapping. Left half (x=0..15): a single 2×2 yellow pip at (8, 56)..(9, 57). Right half (x=16..31): a single 2×2 yellow pip at (23, 56)..(24, 57) — representing "stride 1 cell" visually.
      - Row 2 (y=58..59): "2-pip → stride-2". Left: two 2×2 yellow pips. Right: two 2×2 yellow pips (representing stride 2).
      - Row 3 (y=60..61): "3-pip → stride-3". Left: three 1×2 yellow pips. Right: three 1×2 yellow pips.
      - Row 4 (y=62): spacing.
    - Background: when yellow legend is active, off-white (1); when inactive, dim grey (3).
    - Active legend has a 1-pixel black (5) outline around the entire 32×7 strip.
  - **Blue chip** at pixels (x=32..63, y=56..62). 32 columns × 7 rows. Same layout but with the swap:
    - Row 1: "1-pip → stride-1". Same layout — 1↔1.
    - Row 2: "2-pip → stride-3". Left: two blue pips. Right: three blue pips.
    - Row 3: "3-pip → stride-2". Left: three blue pips. Right: two blue pips.
    - Background: active → off-white (1); inactive → grey (3).
    - Active outline as above.

Role summary:
- **Avatar** (movable, tangible): the player's piece.
- **Wall** (immovable): blocks leap *destinations* (and grid edges block destinations too).
- **Floor (with pip pattern)** (walkable): pip count + active legend → next-press stride.
- **Goal** (walkable): when avatar overlaps goal at end of a slide animation OR at the slide's destination, the level advances. Goal stays in place.
- **Filter** (L2+, walkable): on overlap, toggles legend (Yellow ↔ Blue); recolors all `floor_pip_*` sprites to the matching color variant. Re-usable.
- **Pivot** (L3+, walkable, **one-shot**): on overlap, if the cell still carries the `pivot` tag, sets `_pending_bonus = 1` AND the avatar swaps to `avatar_pivot_pending` rendering. On the next press (success or no-op), the effective stride is `(origin_cell_stride + _pending_bonus)`, then `_pending_bonus = 0`, the avatar reverts to `avatar_normal`, AND the pivot cell is **consumed**: the `pivot_floor_pip_2_yellow`/`pivot_floor_pip_2_blue` sprite at that cell is replaced with a regular `floor_pip_2_yellow`/`floor_pip_2_blue` matching the current legend (the maroon ring and "+" cross are removed; the underlying pip pattern is preserved). Once consumed, the pivot cell is just a normal 2-pip floor cell. A pivot can be triggered at most once per level.

## 4. Level progression, mechanic enumeration, and witness solutions

Three levels. All use `grid_size = (64, 64)` and `available_actions = [1, 2, 3, 4]`. Coordinates are cell-coordinates (cx, cy), placed at pixel (cx*8, cy*8). Playfield is 8 cols × 7 rows of cells (cy ∈ {0..6}).

### Level 1 — base dynamic system

**Mechanics required by the witness** (N = 2):
- **M1 (cell-pip-stride-leap)**: pressing an arrow translates the avatar by N cells in the pressed direction (N = origin cell's pip count). The destination must be open (not a wall, not off-grid); intermediate cells are fly-over. If the destination is illegal, the press is a no-op.
- **M2 (goal-overlap-wins)**: when the avatar overlaps the `goal_cell` (after a leap's destination resolves), the level ends and `next_level()` fires.

**Necessity per mechanic** (per checklist item 12, strict counterfactual):
- **L1 cannot be solved without triggering M1** because the wall row at y=3 (cells `(0,3), (1,3), ..., (7,3)` — 8 wall cells forming a complete horizontal barrier) blocks every stride-1 destination from `y ∈ {2, 4}` to `y ∈ {3}`. The avatar starts at `(3, 5)`. Stride-1 UP from any `(x, 4)` has destination `(x, 3)` = wall → no-op. The wall row cannot be crossed by stride-1 walking from the south side. The only floor cell on the south side that has a leap-capable stride is `(3, 4)`, a stride-3 cell; UP from `(3, 4)` has destination `(3, 1)` — open, above the wall row. *Witness fires M1 at step 2.*
- **L1 cannot be solved without triggering M2** because reaching the cell `(3, 1)` is the only event that ends the level; M2 is the win predicate.

**Initial layout** (8×7 grid):
- `wall_block` placed at `(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3)` — 8 wall cells covering all of row y=3.
- `floor_pip_1_yellow` placed at every other empty cell (cx ∈ 0..7, cy ∈ 0..6, cy ≠ 3) EXCEPT for the cell `(3, 4)`.
- `floor_pip_3_yellow` placed at `(3, 4)` — the leap cell.
- `goal_cell` placed at `(3, 1)`.
- `avatar_normal` placed at `(3, 5)`.
- Step budget: 30.

**Witness solution** (length **2**):
`[ACTION1, ACTION1]`
1. **UP** from `(3, 5)` (stride-1 yellow) → destination `(3, 4)`. Legal (open floor). Avatar moves to `(3, 4)`.
2. **UP** from `(3, 4)` (stride-3 yellow) → destination `(3, 1)`. Legal (`(3, 1)` is the goal cell). Avatar leaps `(3,4)→(3,3)→(3,2)→(3,1)` with fly-over animation across the wall row at y=3. Lands at `(3, 1)`; M2 fires; `next_level()`.

**Per-mechanic counterfactual table** (per checklist item 12):

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 | no | Without variable stride (all cells stride-1), UP from `(3, 4)` has destination `(3, 3)` = wall → no-op. Stride-1 cannot leap the y=3 wall row; the wall row spans all 8 columns, so neither side-step nor down-then-up paths exist. Stuck. |
| L1 | M2 | no | M2 is the win predicate; without it the goal cell does nothing. |

Alternative strategies a fully-informed player might try and why they fail:
- *"Walk around the wall row"*: walls cover all 8 columns of y=3 → no walk-around.
- *"DOWN and approach from the bottom"*: from `(3, 5)` DOWN to `(3, 6)`. Stride-1 from `(3, 6)` UP → `(3, 5)`. No new ground gained. Avatar can't get above the wall row via stride-1.
- *"Spam directions from `(3, 5)`"*: only UP-stride-1 to `(3, 4)` (then stride-3 leap) lands legally toward the goal.

**Difficulty justification** (per `difficulty-rules.md` § 2):
- **(a) Random-resistance**: 4² = 16 random pairs of presses. Of these, only `[UP, UP]` succeeds. Hit probability 1/16. A random agent with 30 actions can take up to 28 random sequences of length 2, hitting probability ≈ 1 − (15/16)^28 ≈ 84% over 28 tries. *Tutorial L1 may be solvable by random play* — and `composition-and-tutorial.md` explicitly says: *"Random agents can occasionally stumble into success at this stage, which is acceptable by design."* The tutorial's purpose is mechanic-teaching, not random-resistance.
- **(b) Human-tractable**: A human reads the screen: avatar, goal, wall barrier, pip patterns. Press UP and see stride-1 motion to `(3, 4)`. Press UP from `(3, 4)` and observe the 3-cell leap over the wall. Land at goal. **Expected human time: 20–45 seconds.**
- **(c) Planning depth**: **No strict planning requirement at L1** (per `difficulty-rules.md` § 2c L1). Once the player understands that the cell pip count = stride distance and leaps cross walls, the witness is the only meaningful path. No multi-step reasoning needed.
- **(d) Step budget**: **30**. Witness = 2. Generous buffer (28 actions of slack) for exploration of all 4 directions from start, plus mis-pressing (which is mostly no-ops since walls cap most directions).

### Level 2 — base system + 1 new mechanic

**Mechanics required by the witness** (M = N + 1 = 3):
- M1 (carried forward).
- M2 (carried forward).
- **M3 (filter swap)**: when avatar overlaps a `filter_cell`, the active legend toggles between Yellow (1→1, 2→2, 3→3) and Blue (1→1, 2→3, 3→2). All `floor_pip_2_yellow` sprites swap to `floor_pip_2_blue` (and similarly for 3-pip — both visual variants flipped). The HUD legend chips' active outline shifts. The filter cell stays.

**Necessity per mechanic** (counterfactual, per item 12):
- **L2 cannot be solved without triggering M1** because the same 2-row barrier blocks stride-1 walking through y=2..3 (every UP press's destination in y=4 is y=3 = wall; every DOWN press's destination in y=1 is y=2 = wall). Stride-1 alone is insufficient.
- **L2 cannot be solved without triggering M2** because M2 is the win predicate.
- **L2 cannot be solved without triggering M3** because the leap-cell at `(3, 4)` is a 2-pip cell (`floor_pip_2_yellow`). In Yellow legend, 2-pip = stride-2. UP from `(3, 4)` stride-2 → destination `(3, 2)` = wall (the lower row of the 2-row barrier) → no-op. Stride-2 alone is insufficient. Stride-3 is required. There are NO 3-pip cells in the L2 layout (only 1-pip and 2-pip), so stride-3 is reachable only via filter-swap (turning 2-pip into stride-3 via Blue legend). Without filter, no stride-3 is available anywhere → no leap → no win.

**Initial layout** (8×7 grid):
- `wall_block` placed at `(0, 2), (1, 2), ..., (7, 2)` AND `(0, 3), (1, 3), ..., (7, 3)` — 16 wall cells covering rows y=2 and y=3 (2-row horizontal barrier).
- `floor_pip_1_yellow` placed at every empty cell EXCEPT `(3, 4)`.
- `floor_pip_2_yellow` placed at `(3, 4)` — the leap candidate.
- `filter_cell` placed at `(5, 5)`.
- `goal_cell` placed at `(3, 0)`.
- `avatar_normal` placed at `(3, 5)`.
- No 3-pip cells anywhere (enforces stride-3 only reachable via filter).
- Step budget: 50.

**Witness solution** (length **7**):
`[ACTION4, ACTION4, ACTION3, ACTION3, ACTION1, ACTION1, ACTION1]`
1. **RIGHT** from `(3, 5)` (stride-1 yellow) → destination `(4, 5)`. Legal.
2. **RIGHT** from `(4, 5)` (stride-1 yellow) → destination `(5, 5)` = filter. Legal. *M3 fires*; legend toggles → Blue; all floor pip sprites' accents change yellow→blue; HUD legend chip active-outline swaps from yellow to blue.
3. **LEFT** from `(5, 5)` (stride-1 blue, but 1-pip = 1 under blue too) → destination `(4, 5)`. Legal.
4. **LEFT** from `(4, 5)` (stride-1 blue) → destination `(3, 5)`. Legal.
5. **UP** from `(3, 5)` (stride-1 blue) → destination `(3, 4)`. Legal.
6. **UP** from `(3, 4)` (2-pip blue = **stride-3**) → destination `(3, 1)`. Avatar leaps `(3,4)→(3,3)→(3,2)→(3,1)` over walls at y=3, y=2. Destination `(3, 1)` is open. Lands at `(3, 1)`. *M1 fires with Blue stride*.
7. **UP** from `(3, 1)` (stride-1 blue) → destination `(3, 0)` = goal. *M2 fires*; `next_level()`.

**Per-mechanic counterfactual table**:

| Level | Mechanic | Solvable without triggering M? | Why not |
|---|---|---|---|
| L2 | M1 | no | All cells stride-1 means UP from `(3, 4)` → `(3, 3)` = wall → no-op. Wall barrier cannot be crossed. |
| L2 | M2 | no | M2 is the win predicate. |
| L2 | M3 | no | Without filter, legend stays Yellow. 2-pip yellow = stride-2; UP from `(3, 4)` → `(3, 2)` = wall → no-op. No 3-pip cells exist in L2 layout; max yellow-legend stride = 2 < 3 needed to clear the 2-row wall barrier. No alternate path circumvents this (walls span full width). |

Alternative strategies a fully-informed player would try and why they fail:
- *"Go directly UP without using filter"*: from `(3, 5)` UP → `(3, 4)`. UP stride-2 yellow → `(3, 2)` = wall → no-op. Stuck.
- *"Find a 3-pip cell elsewhere"*: there are no 3-pip cells in the layout. (The mechanic-spec verifies this in the cell list.)
- *"Walk RIGHT along bottom row to find a side passage"*: walls span full width of y=2..3; no side passage exists. RIGHT from `(3, 5)` → `(4, 5)` → `(5, 5)` = filter, which is the witness step 2 (filter swap is unavoidable).
- *"Use filter then walk back DOWN then approach from a different angle"*: equivalent to the witness; no shortcut.

**Difficulty justification**:
- **(a) Random-resistance**: 4⁷ = 16384 random sequences of length 7. Of these, very few hit the witness exactly. Even with 50 actions, random play has ≈ 50/16384 ≈ 0.3% per-sequence-length hit rate. Walls clamp most directions to no-ops, but the filter is reachable by a simple RIGHT-RIGHT walk, and then the leap requires UP from `(3, 4)`. Random path with appropriate steps: ≈ 1/2000 chance per ~10-step sequence. With a 50-step budget, random play has < 5% chance of solving.
- **(b) Human-tractable**: human observes the new filter cell (orange ring at `(5, 5)`), steps on it, sees all floor pips change color (yellow → blue), notes the legend chip outline change. Reasons that the legend has swapped 2↔3. Retraces to `(3, 5)` and leaps. **Expected human time: 90 seconds – 2 minutes.**
- **(c) Planning depth (post-discovery, L2)**: with all mechanics known, the post-discovery player faces decisions:
  - Decision space at start: 4 first moves from `(3, 5)`. Of these, 2 lead to legal floor cells (UP, RIGHT); 2 hit walls / boundary (DOWN, LEFT lead to legal cells but away from filter). So 4 first-moves with 2 productive (RIGHT toward filter, UP toward leap-cell).
  - Plausible wrong alternative: UP from start, leap attempt fails (2-pip yellow = stride-2, hits wall). The player must reject this and go RIGHT to filter first.
  - Reasoning chain: "the wall is 2 rows thick; my only 2-pip cell gives stride-2 in yellow; I need stride-3; filter swaps 2-pip to stride-3 in blue; route to filter first, then return to leap."
- **(d) Step budget**: **50**. Witness = 7. Generous: 43 actions of slack for exploration of the filter mechanic and any backtracking. Per `difficulty-rules.md` § d, "budget must NOT shrink relative to the witness as level number rises" — 50 > 30, satisfies.

### Level 3 — system + 1 new mechanic

**Mechanics required by the witness** (M' = M + 1 = 4):
- M1, M2, M3 (carried forward).
- **M4 (facing-pivot stride-bonus +1, one-shot)**: when the avatar overlaps a `pivot_floor_pip_*` composite cell, `_pending_bonus` is set to 1 and the avatar's sprite swaps to `avatar_pivot_pending` rendering. On the *next* press, the effective stride is `(legend-transformed cell stride) + 1`. After that press resolves (success or no-op), `_pending_bonus` resets to 0, the avatar reverts to `avatar_normal`, AND the pivot cell itself is consumed: its `pivot_floor_pip_2_yellow`/`pivot_floor_pip_2_blue` sprite is replaced with the matching `floor_pip_2_yellow`/`floor_pip_2_blue` (maroon ring + "+" cross removed; pip count preserved). The pivot tag is removed from that cell. **A pivot can be triggered at most once per level**; once consumed, it is just a regular 2-pip floor cell.

**Necessity per mechanic** (counterfactual, per item 12):
- **L3 cannot be solved without M1** because all cells default to stride-1 only would leave the avatar unable to cross the 3-row wall barrier at y=2..4 (every direct UP press has wall destination).
- **L3 cannot be solved without M2** because M2 is the win predicate.
- **L3 cannot be solved without M3** because the only 2-pip cell available is the pivot-overlay at `(3, 5)`. In Yellow legend, 2-pip + pivot-bonus = stride-3. UP from `(3, 5)` stride-3 → destination `(3, 2)` = wall (top row of 3-row barrier) → no-op. Stride-3 insufficient. Stride-4 is needed (to clear 3 wall rows and land at y=1). Stride-4 = 2-pip + pivot-bonus = (2 + 1) = 3 in yellow, OR (3 + 1) = 4 in blue. So Blue legend is required.
- **L3 cannot be solved without M4** because the maximum achievable stride without pivot bonus is 3 (2-pip in Blue legend), insufficient for a 3-row wall barrier (need stride-4 to leap from y=5 to y=1). Pivot's +1 bonus is the only way to reach stride-4. No 3-pip cells exist in L3 layout.

**Initial layout** (8×7 grid):
- `wall_block` placed at `(0, 2), (1, 2), ..., (7, 2)` AND `(0, 3), ..., (7, 3)` AND `(0, 4), ..., (7, 4)` — 24 wall cells covering rows y=2, 3, 4 (3-row barrier).
- `floor_pip_1_yellow` placed at every empty cell EXCEPT `(3, 5)` and `(5, 5)`.
- `pivot_floor_pip_2_yellow` placed at `(3, 5)` — composite pivot + 2-pip cell.
- `filter_cell` placed at `(5, 5)`.
- `goal_cell` placed at `(3, 0)`.
- `avatar_normal` placed at `(3, 6)`.
- No 3-pip cells, no other 2-pip cells anywhere.
- Step budget: 80.

**Witness solution** (length **7**):
`[ACTION1, ACTION4, ACTION4, ACTION3, ACTION3, ACTION1, ACTION1]`
1. **UP** from `(3, 6)` (stride-1 yellow) → destination `(3, 5)` = pivot+2-pip composite. Legal. *M4 fires*; `_pending_bonus = 1`; avatar swaps to `avatar_pivot_pending`.
   - **WAIT**: this step lands the avatar on the pivot. The pivot's bonus is pending. The next press should leap. But the avatar needs to be in Blue legend for the 2-pip to become stride-3, then +1 bonus = stride-4. So the player needs to visit the filter FIRST, then come back to the pivot. Let me re-trace:

Actually let me re-trace step 1. The PIVOT must be visited AFTER the filter, because the pivot bonus is one-shot and must apply to the leap press. If the player steps on the pivot, then walks to filter, then walks back, the pivot bonus is consumed when leaving the pivot.

So the witness order is: filter first, then pivot, then leap.

Re-trace:
1. **RIGHT** from `(3, 6)` (stride-1 yellow) → destination `(4, 6)`. Legal.
2. **UP** from `(4, 6)` (stride-1 yellow) → destination `(4, 5)`. Legal.
3. **RIGHT** from `(4, 5)` (stride-1 yellow) → destination `(5, 5)` = filter. Legal. *M3 fires*; legend → Blue.
4. **LEFT** from `(5, 5)` (stride-1 blue) → destination `(4, 5)`. Legal.
5. **LEFT** from `(4, 5)` (stride-1 blue) → destination `(3, 5)` = pivot+2-pip composite. Legal. *M4 fires*; `_pending_bonus = 1`.
6. **UP** from `(3, 5)` (2-pip blue = stride-3, +1 bonus = **stride-4**) → destination `(3, 1)` (y=5 - 4 = 1). Wall barrier at y=2,3,4 fly-over (intermediate); destination `(3, 1)` is open. Avatar leaps `(3,5)→(3,4)→(3,3)→(3,2)→(3,1)`. M1 fires with bonus; `_pending_bonus` clears; avatar reverts to `avatar_normal`.
7. **UP** from `(3, 1)` (stride-1 blue) → destination `(3, 0)` = goal. *M2 fires*; `next_level()`.

Witness length: **7 actions**.

**Per-mechanic counterfactual table**:

| Level | Mechanic | Solvable without triggering M? | Why not |
|---|---|---|---|
| L3 | M1 | no | Stride-1-only cannot clear the 3-row wall barrier (every direct UP destination in y=2..4 is wall). |
| L3 | M2 | no | M2 is the win predicate. |
| L3 | M3 | no | Without filter, max stride is 2 (2-pip yellow). With pivot bonus +1, max stride is 3 (2-pip yellow + 1). UP from `(3, 5)` stride-3 → destination `(3, 2)` = wall → no-op. Cannot leap 3-row barrier with stride-3. |
| L3 | M4 | no | Without pivot bonus, max stride is 3 (2-pip blue, after filter). UP from `(3, 5)` stride-3 → `(3, 2)` = wall → no-op. Stride-4 unreachable. And because the pivot is **one-shot**, the player must visit it AFTER the filter (so legend is Blue and the +1 bonus combines with stride-3 to make stride-4); visiting the pivot before the filter consumes the pivot on a stride-3-yellow-attempt that hits a wall, leaving no way to recover stride-4. |

Alternative strategies a fully-informed player would try and why they fail:
- *"Use pivot first, then filter, then leap"*: from `(3, 6)` UP → `(3, 5)` = pivot; bonus pending. Then walk to filter requires LEFT/RIGHT/UP/DOWN — any press consumes the bonus on the first non-pivot press. E.g., RIGHT from `(3, 5)` 2-pip yellow + bonus = stride-3 → destination `(6, 5)`. Wait `(3+3, 5) = (6, 5)`. Open. Lands at `(6, 5)`. Bonus consumed. Then can the player still reach filter? RIGHT × ... `(6, 5)` is between filter at `(5, 5)` and edge. LEFT from `(6, 5)` → `(5, 5)` = filter. M3 fires. Legend → Blue. Then need to return to `(3, 5)` and trigger pivot again. Walk back. But now pivot at `(3, 5)` was already used — does stepping on it re-trigger the bonus? Per spec: "Stepping onto a pivot while `_pending_bonus` is already 1 does NOT re-set it; idempotent". But what about after pending was cleared (= 0)? The spec should say: stepping on a pivot ALWAYS sets `_pending_bonus = 1` (unless already 1). After bonus is consumed (= 0), stepping on pivot re-sets it. So the pivot is RE-USABLE. Then the alternative path could work: use pivot, consume bonus (non-leap), reach filter, come back to pivot, re-trigger bonus, leap. Witness length is longer but solvable. Let me verify this alternative more carefully:
  1. UP → `(3, 5)` = pivot, bonus pending. (1 action)
  2. RIGHT from `(3, 5)` 2-pip yellow + 1 = stride-3 → `(6, 5)`. Bonus consumed. (1 action; cumulative 2)
  3. LEFT from `(6, 5)` stride-1 → `(5, 5)` = filter; legend → Blue. (1 action; cumulative 3)
  4. LEFT from `(5, 5)` stride-1 → `(4, 5)`. (cumulative 4)
  5. LEFT from `(4, 5)` stride-1 → `(3, 5)` = pivot; bonus re-set to 1. (cumulative 5)
  6. UP from `(3, 5)` 2-pip blue + 1 = stride-4 → destination `(3, 1)`. (cumulative 6)
  7. UP from `(3, 1)` stride-1 → `(3, 0)` = goal. (cumulative 7)

  Same number of actions (7) as the witness order. So the witness order ("filter first, pivot second") is one of two optimal solutions; both use M3 and M4.

- *"Spam UP from start"*: UP from `(3, 6)` → `(3, 5)`. UP from `(3, 5)` 2-pip yellow + 0 (no bonus pending since this is the FIRST press at pivot, but pivot sets bonus AFTER landing; the bonus applies to the NEXT press). So the press from `(3, 5)` doesn't yet have the bonus. Actually — clarification needed: when does the bonus apply? Per spec: "On the *next* press, the effective stride is `(legend-transformed cell stride) + 1`." So landing on pivot sets bonus; the press DEPARTING from pivot uses the bonus.

  So step 2 ("UP from `(3, 5)` 2-pip yellow + 0") is WRONG — the press departing from pivot has bonus. Re-trace step 2: UP from `(3, 5)` 2-pip yellow + 1 = stride-3 → destination `(3, 2)` = wall → no-op. Bonus consumed without effect. Now at `(3, 5)` with bonus = 0 and yellow legend. Player must navigate to filter. RIGHT from `(3, 5)` 2-pip yellow = stride-2 → `(5, 5)` = filter. Legend → Blue. Then navigate back to pivot, re-trigger, leap. Witness:
  1. UP → `(3, 5)` = pivot, bonus set. (1 action)
  2. UP → `(3, 2)` wall NO-OP, bonus consumed wastefully. (2 actions; bonus = 0)
  3. RIGHT from `(3, 5)` stride-2 → `(5, 5)` = filter; legend → Blue. (3 actions)
  4. LEFT from `(5, 5)` stride-1 blue → `(4, 5)`. (4)
  5. LEFT from `(4, 5)` stride-1 blue → `(3, 5)` = pivot; bonus re-set. (5)
  6. UP from `(3, 5)` 2-pip blue + 1 = stride-4 → `(3, 1)`. (6)
  7. UP → goal. (7)

  Same length. The trivial "spam UP" heuristic ends up consuming the bonus wastefully on a wall hit (step 2), so it CAN still finish in 7 actions because the pivot re-triggers. But the WITNESS path (filter first, then pivot) takes 7 actions too. So both paths are 7-action solutions and they both exercise all 4 mechanics.

  Actually — let me verify the witness's filter-first path doesn't have a shorter alternative:

  The witness:
  1. RIGHT → `(4, 6)`. (cumul 1)
  2. UP → `(4, 5)`. (cumul 2)
  3. RIGHT → `(5, 5)` filter, legend Blue. (cumul 3)
  4. LEFT → `(4, 5)`. (cumul 4)
  5. LEFT → `(3, 5)` pivot. (cumul 5)
  6. UP stride-4 → `(3, 1)`. (cumul 6)
  7. UP → `(3, 0)` goal. (cumul 7)

  Length 7. Both paths same length. Multiple optimal witnesses is fine.

  The "spam UP first" alternative wastes the bonus once, but recovers. So the trivial-greedy heuristic ALSO solves in 7 actions. Hmm — this is a concerning sign for L3 planning depth.

  Let me re-examine. The trivial heuristic ("go toward goal greedily") would do UP-first. UP → pivot. UP → wall. Then needs filter. Total 7 actions. So the "trivial" heuristic finishes in 7 actions.

  This means **L3's planning challenge is weak**: a greedy player still finishes in the optimal action count. Per `difficulty-rules.md` § L3 (planning depth: challenging even for attentive human; named trivial heuristic must fail), this is a problem.

  **Mitigation**: design L3 such that the trivial heuristic ACTUALLY fails (loses more steps). One way: increase the wall thickness OR add more 1-pip cells between pivot and filter so the "RIGHT" recovery from `(3, 5)` doesn't reach the filter directly.

  Actually, looking at step 3 of the trivial path (RIGHT from `(3, 5)` stride-2 → `(5, 5)` filter): the trivial player's RIGHT stride-2 from `(3, 5)` lands exactly on the filter. That's lucky. To make it not-lucky, make the filter at `(6, 5)` instead of `(5, 5)`. Then RIGHT from `(3, 5)` stride-2 → `(5, 5)` (a 1-pip cell), not filter. Player must press RIGHT again to reach filter at `(6, 5)`. Extra action.

  Re-design with filter at `(6, 5)`:

  Witness order ("filter first"):
  1. RIGHT → `(4, 6)`. (1)
  2. UP → `(4, 5)`. (2)
  3. RIGHT → `(5, 5)`. (3)
  4. RIGHT → `(6, 5)` filter, legend Blue. (4)
  5. LEFT → `(5, 5)`. (5)
  6. LEFT → `(4, 5)`. (6)
  7. LEFT → `(3, 5)` pivot. (7)
  8. UP stride-4 → `(3, 1)`. (8)
  9. UP → goal. (9)

  Length 9.

  Trivial heuristic ("spam UP"):
  1. UP → `(3, 5)` pivot. (1)
  2. UP → wall NO-OP, bonus consumed. (2)
  3. RIGHT stride-2 yellow → `(5, 5)`. (3)
  4. RIGHT stride-1 → `(6, 5)` filter, legend Blue. (4)
  5. LEFT stride-1 blue → `(5, 5)`. (5)
  6. LEFT stride-1 blue → `(4, 5)`. (6)
  7. LEFT stride-1 blue → `(3, 5)` pivot. (7)
  8. UP 2-pip blue + 1 = stride-4 → `(3, 1)`. (8)
  9. UP → goal. (9)

  Both 9 actions. Still tied. The trivial heuristic doesn't lose actions because the WASTED bonus at step 2 is "free" (no-op doesn't consume a turn beyond the press itself).

  Hmm. The pivot bonus being "consumed on attempted press regardless of success" is what makes the trivial heuristic recoverable. If I change the rule so that **the bonus is consumed only on SUCCESSFUL presses**, then the wasted press at step 2 wouldn't consume the bonus, and the player could continue using it. Reverting to current rule: bonus consumed on attempt.

  Alternative rule: bonus persists across no-ops (only consumed on successful move). Then the trivial heuristic:
  1. UP → pivot, bonus set. (1)
  2. UP → wall NO-OP, bonus NOT consumed. (2)
  3. RIGHT stride-2 yellow + 1 = stride-3 → destination `(6, 5)` = filter. Bonus consumed on this successful press. Legend → Blue.
  4. LEFT stride-1 → `(5, 5)`. (4)
  5. LEFT → `(4, 5)`. (5)
  6. LEFT → `(3, 5)` pivot, bonus set again. (6)
  7. UP 2-pip blue + 1 = stride-4 → `(3, 1)`. (7)
  8. UP → goal. (8)

  8 actions. SHORTER than the filter-first path (9). So the trivial heuristic WINS with this rule.

  Hmm this is bad. Let me revert: bonus consumed on attempt (any press). Then both paths are 9. Tied.

  Even tied is okay-ish. The "trivial heuristic" doesn't fail outright; it just doesn't beat the witness. Per `difficulty-rules.md` § 2c L3: "Greedy / monotone-progress / follow-the-obvious-gradient strategies should not reliably win." A tie isn't quite "fail" but it's not a clear win for the greedy heuristic either.

  Let me redesign to truly make the greedy heuristic fail (run out of budget OR get stuck). One way: make the layout require a specific filter-pivot ORDER, where the greedy path leads to a state where neither pivot nor filter can be re-applied to finish.

  Simpler: add a SECOND filter cell that's only useful when visited AFTER the pivot. Or make the filter cells one-shot (consumed when used).

  Actually for simplicity, let me just declare that the greedy "UP-first" path ALSO works (in the same 7-9 actions), AND the planning challenge is the REASONING ("why does the witness work"). The player doesn't need to find an asymmetric path; they need to understand the mechanics.

  Update L3 planning-depth justification:
  - Plausible wrong heuristic: "Spam UP toward goal" (greedy). UP → `(3, 5)` (pivot). UP → wall (no-op, bonus wasted in yellow legend). Player is now stuck on pivot with bonus = 0 and Yellow legend. They cannot leap from here. They must walk to filter (RIGHT × 2 → filter at `(6, 5)`), come back to pivot, leap. **Total 9 actions for the recovery path** vs **9 actions for the optimal witness path**. The heuristic "spam UP" produces no advantage over the witness; both require visiting filter AND pivot.

  OK 9 vs 9 is a "tie" — neither faster. The planning depth here is moderate: the player must understand that filter and pivot are BOTH needed in any order, and the order doesn't matter for action count. But the player must execute correctly OR run out of budget.

  Let me also check: can the player avoid one of the mechanics entirely? No (per the counterfactual table). So all 4 mechanics are exercised by any winning path.

  Accept the design: L3 has 9-action witness, generous budget (80), and the planning depth comes from understanding the M3+M4 combination rather than from finding a non-greedy path.

  Note: I'll update the L3 budget to 80 to be safe.

OK let me finalize L3 layout with filter at `(6, 5)`:

**Initial layout (L3 final)**:
- `wall_block` at `(0..7, 2)`, `(0..7, 3)`, `(0..7, 4)` — 24 wall cells (3-row barrier).
- `floor_pip_1_yellow` at every empty cell EXCEPT `(3, 5)` and `(6, 5)`.
- `pivot_floor_pip_2_yellow` at `(3, 5)`.
- `filter_cell` at `(6, 5)`.
- `goal_cell` at `(3, 0)`.
- `avatar_normal` at `(3, 6)`.
- Step budget: **80**.

**Witness solution (L3 final, length 9)**:
`[ACTION4, ACTION1, ACTION4, ACTION4, ACTION3, ACTION3, ACTION3, ACTION1, ACTION1]`

1. **RIGHT** from `(3, 6)` stride-1 → `(4, 6)`. (cumul 1)
2. **UP** from `(4, 6)` stride-1 → `(4, 5)`. (2)
3. **RIGHT** from `(4, 5)` stride-1 → `(5, 5)`. (3)
4. **RIGHT** from `(5, 5)` stride-1 → `(6, 5)` = filter; legend → Blue. (4)
5. **LEFT** from `(6, 5)` stride-1 blue → `(5, 5)`. (5)
6. **LEFT** from `(5, 5)` stride-1 blue → `(4, 5)`. (6)
7. **LEFT** from `(4, 5)` stride-1 blue → `(3, 5)` = pivot; `_pending_bonus = 1`. (7)
8. **UP** from `(3, 5)` 2-pip blue (=stride-3) + bonus (+1) = **stride-4** → destination `(3, 1)`. Bonus consumed; legend stays Blue. (8)
9. **UP** from `(3, 1)` stride-1 blue → `(3, 0)` = goal. *M2 fires*. (9)

**Difficulty justification (L3)**:
- **(a) Random-resistance**: 4⁹ = 262144 random sequences of length 9. Hit probability ≈ 1/100K. Step budget 80 allows several attempts; probability of random success in 80 actions ≈ 80 × 4⁻⁹ ≈ 0.03%. Very low.
- **(b) Human-tractable**: human needs to discover the pivot ("+1 bonus") mechanic by trial: step on pivot, observe avatar's "+1" arc decoration, press direction, observe distance +1 from normal. Then combine with filter knowledge. **Expected human time: 2.5–4 minutes.**
- **(c) Planning depth (post-discovery, L3)**: with all 4 mechanics known:
  - Decision space at start: 4 first moves from `(3, 6)`. Of these, RIGHT (toward filter route) and UP (toward pivot) are the two productive directions; LEFT and DOWN are time-wasters. The witness path uses RIGHT first (filter-first); the greedy heuristic uses UP first (pivot-first, monotonic toward goal).
  - **Trivial heuristic that IRRECOVERABLY FAILS**: "greedy: spam UP toward goal". UP from `(3, 6)` → `(3, 5)` pivot (`_pending_bonus = 1`). UP from `(3, 5)` 2-pip yellow (stride-2) + 1 bonus = stride-3 → destination `(3, 2)` = wall → no-op. Bonus consumed; **pivot consumed**: the cell becomes a regular `floor_pip_2_yellow`. Now the greedy player faces a different game: pivot is gone, legend still Yellow, max stride achievable = 2 (since 2-pip yellow = stride-2; no bonus available). Subsequent presses can navigate to filter (`(6, 5)`) but cannot regain the bonus. Even after reaching filter and swapping to Blue, the 2-pip cell at `(3, 5)` gives stride-3 (max), insufficient for stride-4 needed to clear the 3-row wall. **The greedy player is irrecoverably stuck.** They will exhaust the step budget (80 actions) and lose.

  The reasoning chain for the witness: (i) the 3-row wall barrier (y=2..4) requires stride-4 to clear (leap from y=5 to y=1); (ii) max base stride from any cell type in this layout is 3 (2-pip blue, after filter); (iii) +1 pivot bonus brings stride to 4, but pivot is ONE-SHOT — it can only be used once; (iv) therefore, the player must arrange to be at the leap-cell (`(3, 5)`) WITH pivot-bonus pending AND legend = Blue at the moment of the leap press. (v) This forces a specific ordering: visit filter FIRST (to swap to Blue), THEN visit pivot LAST (to gain bonus immediately before the leap). The pivot-first ordering wastes the one-shot bonus on a yellow-legend stride-3 attempt that hits the wall.

- **(d) Step budget**: **80**. Witness = 9. Generous: 71 actions of slack. Per `difficulty-rules.md` § d, "budget must NOT shrink relative to the witness as level number rises" — 80 > 50 > 30, satisfies.

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`. No ACTION5, no ACTION6, no ACTION7.

| Action | Effect |
|---|---|
| ACTION1 | UP leap: avatar attempts to translate (0, -N) cells, where N = legend-transformed pip count of avatar's current cell, plus `_pending_bonus`. Destination cell must be open (not wall, not off-grid); else no-op. Animation: avatar visually moves cell-by-cell through intermediate cells (which are fly-over, no interaction). On landing: filter / pivot / goal effects fire based on destination. `_pending_bonus` is consumed (set to 0). |
| ACTION2 | DOWN leap: same but (0, +N). |
| ACTION3 | LEFT leap: same but (-N, 0). |
| ACTION4 | RIGHT leap: same but (+N, 0). |

The press's stride is computed as: `N = legend_transform(origin_cell_pip_count) + _pending_bonus`. Legend transform: Yellow legend = identity; Blue legend = 2↔3 swap (1-pip → 1, 2-pip → 3, 3-pip → 2). `_pending_bonus` is 0 normally, 1 when avatar just stepped on a pivot.

## 6. HUD and per-game state

**Visible HUD widgets** (rendered via `RenderableUserDisplay`):
- `StepCounterHud`: pixel row y=63 across all 64 columns. Left portion (`steps_remaining / max_steps`) yellow (11); right portion off-black (4).
- `LegendChipHud`: pixel rows y=56..62 across 64 columns. Two chips side-by-side (yellow chip x=0..31, blue chip x=32..63). Each chip displays 3 pip→stride rows; the active chip's background is off-white (1) with 1-pixel black (5) outline, the inactive chip's background is grey (3) with no outline. The HUD's role is to communicate the active legend's pip→stride mapping so the player can read it off the screen.

**Internal state** (on the `Dh4j(NovaBaseGame)` instance):
- `self._legend` — `"yellow"` or `"blue"` (active legend identifier).
- `self._pending_bonus` — `int` (0 or 1).
- `self._slide_phase` — `int` sentinel; -1 = idle, ≥ 0 = animating a multi-cell slide; advances one cell per `step()` until full slide is resolved.
- `self._slide_remaining` — cells left to slide.
- `self._slide_dir` — `(dx, dy)` of active slide.
- `self._slide_origin` — `(ox, oy)` of slide origin (for goal-mid-slide detection).
- `self._steps_taken`, `self._max_steps` — step counter / lose trigger.

**State-to-visual-cue mapping (per checklist item 19)**:
- `_legend` is visualised by: floor cells' pip color (yellow vs blue) AND the HUD legend chip's active outline.
- `_pending_bonus = 1` is visualised by: avatar sprite swaps from `avatar_normal` to `avatar_pivot_pending` (which has a 2×2 white corner accent). The cue persists from landing on pivot through to the next press.
- Pivot consumption is visualised by: the pivot cell's sprite swaps from `pivot_floor_pip_2_*` to `floor_pip_2_*` (matching the current legend's variant) — maroon ring and "+" cross are removed. The persistent visual cue tells the player "the pivot is used up".
- `_slide_phase` ≥ 0 is transient (during a slide animation only) — no persistent cue needed because it resolves in a single press's effects.
- Step counter HUD is always visible.

No hidden state.

## 7. Win condition

When the avatar's grid-cell position overlaps the `goal_cell`'s position (cell-aligned), call `self.next_level()`. Check is done after every animation frame of a slide AND at the final destination, so reaching the goal mid-slide ends the slide early. After L3 wins, the engine auto-fires `self.win()`.

## 8. Lose condition

When `self._steps_taken >= self._max_steps` (level's `step_budget`), call `self.lose()`. No instant-fail. No hazards. Walls clamp via destination-block but never lose.

## 9. Novelty note

The mechanic-pick.md document's full novelty walkthrough applies (cited for completeness): NOVEL on both positive-similarity (taxonomy + prior-games index) and negative-similarity (8-dimension test) against all near-misses.

### Closest taxonomy entries (distinguishing rules)

- **bp35 (gravity-fall-navigation)** — implicit gravity + side-step. *Distinguishing rule*: dh4j has no auto-motion; every press is explicit with cell-encoded variable stride.
- **lt7m (ell-jump-tour-block)** — click an L-shape-reachable cell to jump. *Distinguishing rule*: lt7m's verb is *click + L-shape*; dh4j's is *arrow + cardinal-stride-N*. Different jump shape (L vs cardinal) and different input.
- **ls20 (cycler-attribute-match)** — avatar hops 5-pixel cells; pellets with shape/color/rot indices. *Distinguishing rule*: ls20 has constant hop distance + avatar-carried attributes; dh4j has variable per-cell stride + no carried state.
- **tu93 (lockstep-multi-maze)** — fixed 1-cell-per-press, multi-agent. *Distinguishing rule*: dh4j is variable-N-per-press, single agent.
- **m0r0 (mirror-orb-merge)** — multi-avatar mirrored controls. *Distinguishing rule*: dh4j is single-avatar; no mirroring.

### Closest prior-games entries (distinguishing rules)

- **bz3k (drift-impulse-cardinal)** — pawn carries persistent integer velocity; arrows ±1 impulse. *Distinguishing rule*: bz3k's velocity is *avatar-internal*, persists across turns; dh4j reads stride from origin cell each press, *no carried velocity*. Visual signature: bz3k features velocity-arrow accent on avatar; dh4j features per-cell pip-pattern floor + leap animations.
- **fz5j (phase-step-tile)** — cells open/close periodically by time. *Distinguishing rule*: fz5j cells change with time; dh4j cells don't.
- **kn58 (anchor-pull-magnet)** — clicks drop anchor; pawns slide one cell toward it. *Distinguishing rule*: kn58's direction is magnetic-radial; dh4j's is player-chosen-cardinal.
- **vt6q (grapple-anchor-yank)** — fire grapple to first anchor. *Distinguishing rule*: vt6q's distance depends on first encountered anchor; dh4j's depends on origin cell pip-count.
- **wt39 (glide-deflect-thaw)** — pawn glides until wall; bumpers deflect. *Distinguishing rule*: wt39 has indefinite slide + reflection; dh4j has bounded variable stride and walls block destinations (no reflection).
- **ek73 (wake-trail-evade)** — 1-cell-per-press with hazard wake. *Distinguishing rule*: dh4j has no wake or hazard; variable per-cell stride.
- **pk4m (duotone-flip-walk)** — binary avatar color gates per-cell. *Distinguishing rule*: pk4m's binary is pawn-state; dh4j's three-state is per-cell-encoding-of-stride-distance.
- **lz7q (dual-plane-walk)** — two superimposed planes; ACTION5 toggle. *Distinguishing rule*: lz7q has plane-switch; dh4j has filter-legend-swap on a single playfield, no ACTION5 at all.
- **fw8c (pigment-mix-walk)** — carrier accumulates 3-bit pigment subset. *Distinguishing rule*: fw8c has carried subset state; dh4j has no carried state (except the one-shot pivot bonus, which is single-press scope).
- **vk6m (altitude-grip-climb)** — discrete altitude + grip state for climbs. *Distinguishing rule*: vk6m's cells encode altitude with grip-gated transitions; dh4j's cells encode stride-distance.
- **xz5g (arena-pivot-rotate)**, **nz3v (rotor-pivot-walk)** — rotate sprites or playfield around pivot. *Distinguishing rule*: dh4j's pivot adds a stride bonus to the next press, neither rotates sprites nor playfield.

### Negative-similarity 8-dimension re-check (post-revision)

vs **bz3k** (strongest near-miss):
1. Board: pawn + grid + walls. SHARED.
2. Player: arrow presses (no ACTION5 in either). SHARED.
3. Win: reach goal. SHARED.
4. Killer: step counter. SHARED.
5. Elements: bz3k cap-bands + flippers; dh4j filter + pivot. DIFFERENT.
6. Visual: bz3k velocity-arrow accent on avatar; dh4j per-cell pip-pattern floor + 3-row wall barriers at L3. DIFFERENT.
7. Pixel grain: bz3k linear motion + velocity-arrows; dh4j pip-pattern floor + leap animations. DIFFERENT.
8. Dynamic: bz3k impulse-into-velocity; dh4j cell-coded stride-leap with destination-only-block, fly-over intermediates. DIFFERENT.

Shared: 1, 2, 3, 4. Named principles (6, 7, 8) all differ. **PASSES**.

vs **lz7q** (unindexed near-miss, same prior set):
1. Board: pawn + grid. SHARED.
2. Player: arrows + ACTION5 (lz7q); arrows only (dh4j). DIFFERENT.
3. Win: reach goal. SHARED.
4. Killer: step counter. SHARED.
5. Elements: lz7q dual-plane + plane-tagged sprites; dh4j filter + pivot. DIFFERENT.
6. Visual: lz7q dim-ghost-outline on inactive plane; dh4j pip-pattern floor + filter+pivot decorated cells. DIFFERENT.
7. Pixel: DIFFERENT.
8. Dynamic: lz7q plane-switch globally; dh4j cell-coded stride-leap. DIFFERENT.

Shared: 1, 3, 4. **PASSES**.

vs **vk6m**:
1. Board: SHARED.
2. Player: vk6m ACTION5 grip toggle; dh4j arrows only. DIFFERENT.
3. Win: vk6m visit targets, dh4j reach goal. DIFFERENT.
4. Killer: SHARED.
5. Elements: vk6m altitude tiles + grip + sticky/spring; dh4j pip floor + filter + pivot. DIFFERENT.
6. Visual: vk6m altitude-tier shading; dh4j pip-pattern floor. DIFFERENT.
7. Pixel: DIFFERENT.
8. Dynamic: vk6m carried-grip-state + altitude-gated climbs; dh4j cell-coded-stride-leap. DIFFERENT.

Shared: 1, 4. **PASSES**.

vs **wt39 (glide-deflect-thaw)**:
1. Board: SHARED.
2. Player: arrows. SHARED.
3. Win: reach goal. SHARED.
4. Killer: SHARED.
5. Elements: wt39 bumpers + brittle tiles; dh4j filter + pivot. DIFFERENT.
6. Visual: wt39 glide-trajectory lines through bumpers; dh4j pip-pattern floor + leap animations. DIFFERENT.
7. Pixel: DIFFERENT.
8. Dynamic: wt39 glides indefinitely + reflects; dh4j cell-coded bounded stride + destination-only-block. DIFFERENT.

Shared: 1, 2, 3, 4. Named differ. **PASSES**.

Overall verdict: NOVEL on all axes.

---

This is spec v2 addressing all 8 critique-revisions issues. Ready for re-critique.
