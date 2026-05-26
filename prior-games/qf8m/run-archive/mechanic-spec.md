# mechanic-spec — qf8m

## 1. Title

Rook-Cross Toggle Pattern Match

## 2. Mechanic family

Each level renders a 5×5 grid of square *state-tiles* on a 64×64
frame; clicking a tile (ACTION6) toggles the discrete state of
every tile sharing that tile's row OR column ("rook-cross
flip"), and the player must drive the grid into a target pattern
shown beside the playfield. Two priors are exercised:
**objectness** (each tile is a persistent entity at a fixed cell
with a discrete state) and **basic geometry/topology**
(row/column connectivity is the load-bearing reach relation —
two tiles are "co-rook" iff they share a row or column).

## 3. Sprite roster

All tile sprites are 8×8 px. The 5×5 grid is rendered as
40×40 px placed at frame offset (2, 2). The target-pattern
display is a 20×20 px mirror-grid (4×4 mini-tiles) placed at
(44, 22). Step-counter HUD bar runs across row 63.

### Tile sprites (state-bearing)

- **`rook_tile_dark`** — 8×8, palette `{4 background, 3
  light-grey internal +-cross}`. Tag `tile`, sub-tag `rook`,
  state-tag `state_0`. Role: a rook-typed cell in state 0
  (dark / inactive).
- **`rook_tile_lit`** — 8×8, palette `{6 magenta background,
  4 off-black +-cross}`. Tag `tile`, sub-tag `rook`,
  state-tag `state_1`. Role: a rook-typed cell in state 1
  (lit / active).
- **`bishop_tile_dark`** — 8×8, palette `{4 background, 3
  light-grey internal X-cross}`. Tag `tile`, sub-tag `bishop`,
  state-tag `state_0`. Role: a bishop-typed cell in state 0.
- **`bishop_tile_lit`** — 8×8, palette `{10 light-blue
  background, 4 off-black X-cross}`. Tag `tile`, sub-tag
  `bishop`, state-tag `state_1`. Role: a bishop-typed cell
  in state 1.
- **`tristate_tile_s0`** — 8×8, palette `{4 background, 7 pink
  ring, 2 light-grey centre}`. Tag `tile`, sub-tag `tristate`,
  state-tag `state_0`. Role: a tri-state cell in state 0.
- **`tristate_tile_s1`** — 8×8, palette `{4 background, 7 pink
  ring, 6 magenta centre}`. Tag `tile`, sub-tag `tristate`,
  state-tag `state_1`.
- **`tristate_tile_s2`** — 8×8, palette `{4 background, 7 pink
  ring, 10 light-blue centre}`. Tag `tile`, sub-tag `tristate`,
  state-tag `state_2`.

The internal motif (+-cross for rook, X-cross for bishop, ring
for tri-state) is the **player's only cue** to which click-rule
governs that cell. The motif is preserved across the dark/lit
sprites of the same kind; only the palette accents change with
state. This satisfies checklist item 21 — *sprite UI ≈ sprite
role* — because the visual identity of each cell (its motif) is
load-bearing for predicting the click semantics.

### Target-display sprites (read-only mirror)

- **`target_cell_dark`** — 4×4, all palette `4`. Tag
  `target_cell`. Role: a target mini-tile showing "should be
  state 0".
- **`target_cell_lit_rook`** — 4×4, palette `{6 magenta core,
  4 frame}`. Tag `target_cell`. Role: target mini-tile for a
  rook cell in state 1.
- **`target_cell_lit_bishop`** — 4×4, palette `{10 light-blue
  core, 4 frame}`. Tag `target_cell`. Role: target mini-tile for
  a bishop cell in state 1.
- **`target_cell_tri_s0/s1/s2`** — 4×4, palette `{2/6/10
  centre, 7 pink frame}`. Tag `target_cell`. Role: target
  mini-tile for tri-state cell in each of its 3 states.

The target display is **frozen at level start** and never
changes during play; the player matches the live playfield to
this static reference.

### Frame sprites (purely cosmetic)

- **`playfield_frame`** — 44×44 with a 2-px palette-3 border,
  placed at (0, 0) to enclose the playfield. Tag `frame`.
- **`target_frame`** — 24×24 with a 2-px palette-3 border,
  placed at (43, 21) to enclose the target display. Tag `frame`.
- **`hud_back`** — 64×1 row at row 63, palette 3. Tag `hud`.

## 4. Level progression, mechanic enumeration, and witness solutions

The grid is 5×5 across all 3 levels; same `grid_size=(64, 64)`.
Initial state is *all dark (state 0)* in every level. The
target display per level is pre-rendered as a sprite group
showing the desired final pattern.

For each click action `ACTION6@(px, py)`, the click resolves to
grid-cell coordinates `(col, row) ∈ {0..4}×{0..4}` via:
`col = (px - 2) // 8`, `row = (py - 2) // 8`. Out-of-grid
clicks are no-ops.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 1):
  1. **`rook-flip`** — clicking a rook-typed tile at cell (a, b)
     toggles state mod 2 of every tile in row a OR col b. A
     5×5 grid of all-rook tiles. Each click flips 9 tiles.
- **Necessity per mechanic**:
  - L1 cannot be solved without triggering `rook-flip` because
    every tile in L1 is a rook tile, ACTION6 is the only
    action available, and the only way ACTION6 changes any
    state is by firing the rook-flip rule on the clicked
    tile's row+col — there is no other state-change path.
- **Witness solution** (2 actions, target reached):
  ```
  [ACTION6 @ click on tile (1, 1)  =>  pixel (10, 10)]
  [ACTION6 @ click on tile (3, 3)  =>  pixel (26, 26)]
  ```
  Concretely the action data is `(x=10, y=10)` then
  `(x=26, y=26)`.
- **Target pattern** (shown in the target display):
  ```
  0 1 0 1 0
  1 1 1 0 1
  0 1 0 1 0
  1 0 1 1 1
  0 1 0 1 0
  ```
  (= XOR of two rook-cross flips, one centred at (1,1), one
  centred at (3,3); see derivation in Notes below.)
- **Difficulty justification**:
  - **(a) Random-resistance**: a uniform-random ACTION6 over
    the 25 tiles for k clicks visits a small fraction of the
    Z₂⁵ click-vector space; the target lives in a coset of
    the column space and ≤2-click solutions are rare relative
    to the 25-click budget — random click sequences have <0.5%
    chance of producing this exact 25-bit pattern.
  - **(b) Human-tractable**: an attentive human observes
    "click flips a row+col" within 1-2 exploratory clicks,
    then deduces from the target's 4-fold symmetric look
    that two clicks at the inner-corner-of-pattern positions
    will produce it. ~1 minute of play including discovery.
  - **(c) Planning depth**: *no strict planning requirement
    at L1.* The discovery gate (learning the rook-flip rule)
    is the entire difficulty; once the rule is understood,
    matching this 2-click target is near-immediate by visual
    inspection.
  - **(d) Step budget**: 25. The witness is 2 actions; budget
    leaves ample room to misclick 23 times and still recover
    (each click is self-inverse under Z₂, so re-clicking the
    same cell undoes it).

### Level 2 — base system + 1 new mechanic (M = N + 1 = 2)

- **Mechanics required by the witness**:
  1. **`rook-flip`** — carried forward from L1.
  2. **`bishop-flip`** *(NEW)* — clicking a bishop-typed tile
     at cell (a, b) toggles state mod 2 of every tile lying
     on either diagonal through (a, b): main diagonal cells
     `(i, j) | i − j = a − b` and anti-diagonal cells
     `(i, j) | i + j = a + b`. A bishop click flips up to 9
     tiles (5 main + 5 anti − 1 centre, fewer near edges).
  Layout: 23 rook tiles + 2 bishop tiles at fixed cells
  `(1, 1)` and `(3, 3)`. Bishop tiles are visually distinct
  by their internal X-cross motif (vs the +-cross of rook).
- **Necessity per mechanic**:
  - L2 cannot be solved without triggering `rook-flip` because
    the L2 target row 2 is `0 1 1 1 0` — three lit tiles in
    row 2 — and the only sequence of bishop clicks reaching
    three same-row tiles in 50 clicks is excluded by the
    diagonal-only reach: a single bishop hits at most 2 cells
    of row 2 (one per diagonal), so producing three lit cells
    in row 2 with parity-tight cancellation on the rest of
    the grid would require a many-bishop construction that
    overflows the step budget. The clean solution clicks the
    rook tile at (2, 2), which alone produces the row-2
    skeleton.
  - L2 cannot be solved without triggering `bishop-flip`
    because the L2 target's row-parity vector is
    `(0, 1, 3, 1, 0)` — mixed. Linear-algebra over Z₂ on
    rook-flip-only proves: a rook-only sequence reaches only
    patterns whose row parities are all equal AND whose
    column parities are all equal. The target violates this,
    so at least one bishop click is forced.
- **Witness solution** (3 actions):
  ```
  [ACTION6 @ rook tile (2, 2)    =>  pixel (18, 18)]
  [ACTION6 @ bishop tile (1, 1)  =>  pixel (10, 10)]
  [ACTION6 @ bishop tile (3, 3)  =>  pixel (26, 26)]
  ```
- **Target pattern**:
  ```
  0 0 0 0 0
  0 0 1 0 0
  0 1 1 1 0
  0 0 1 0 0
  0 0 0 0 0
  ```
  (A 5-cell plus centred at (2, 2); produced by rook(2,2)
  XOR bishop(1,1) XOR bishop(3,3) — see derivation in Notes.)
- **Difficulty justification**:
  - **(a) Random-resistance**: a uniform-random click sequence
    has near-zero chance of producing this specific
    5-cell-lit pattern: the target is one of `2²⁵` possible
    binary patterns (~33M), and the reachable cosets in 50
    clicks remain combinatorial in 4 free parameters
    (rook-row-parities, rook-col-parities, two bishop
    indicators), so random play hits the target ~1 in 10⁵.
  - **(b) Human-tractable**: ~2 minutes. Discovery (learning
    that bishop tiles X-flip diagonally vs rook tiles +-flip
    rook-cross) takes 2-3 exploratory clicks watching what
    flips. Planning then identifies that the centred plus
    needs the centre rook click + the two off-centre bishops
    to cancel the rook click's "arms" (top/bottom/left/right
    extending past the plus) into the small plus.
  - **(c) Planning depth (post-discovery)**: **moderate** —
    after discovery, the player has ≥ 25 valid first
    actions (any of 25 cells). Plausible-but-wrong
    alternative the post-discovery player would consider:
    *"I'll click two bishop tiles, then a rook tile to mop
    up"* — but firing both bishops first lights the main
    diagonal twice (cancels) plus two anti-diagonal sets,
    leaving (0,2),(2,0),(2,4),(4,2) lit; then a single rook
    click cannot turn that into the centred plus without
    over-flipping row 2's edges. The post-discovery
    reasoning chain: (i) plus-shape requires rook(2,2) for
    the row-2 + col-2 skeleton; (ii) row 0 and row 4 are
    fully dark so the rook(2,2)'s column-2 over-flips at
    rows 0 and 4 must be cancelled, which is what each
    bishop click's main-diagonal pass through (0,0),(4,4)
    achieves while their anti-diagonals lit-then-unlit
    (0,2),(4,2),(2,0),(2,4) cancel rook(2,2)'s arms.
  - **(d) Step budget**: 50.

### Level 3 — system + 1 new mechanic (M = (N+1) + 1 = 3)

- **Mechanics required by the witness**:
  1. **`rook-flip`** — carried forward.
  2. **`bishop-flip`** — carried forward.
  3. **`tri-state-cell`** *(NEW)* — a designated cell at
     `(2, 2)` whose state cycles **mod 3** instead of mod 2
     when its row/col/diagonal is touched by a click. The
     cell is rendered with a pink ring framing a centre that
     palettes light-grey → magenta → light-blue → light-grey
     across states 0, 1, 2. Other cells continue to flip mod 2
     under rook/bishop rules.
  Layout: 22 rook tiles + 2 bishop tiles at `(1, 1)` and
  `(3, 3)` (carried from L2) + 1 tri-state tile at `(2, 2)`.
- **Necessity per mechanic**:
  - L3 cannot be solved without triggering `rook-flip` because
    the L3 target has a non-zero row-0 binary pattern
    (`0 1 0 1 1`) which a bishop-only construction cannot
    span without flipping cells outside row 0 in
    counterproductive places — specifically, row 0's lit
    cells are at (0,1), (0,3), (0,4); bishop reach into row 0
    flips at most one cell per click (the anti-diagonal
    through that bishop), so producing 3 lit cells in row 0
    in a 60-click budget would require 3 bishops each
    cancelling each other's main-diagonal effects — the
    witness solves it cleaner with the single rook click at
    (0, 4).
  - L3 cannot be solved without triggering `bishop-flip`
    because the L3 target's binary-restricted row-parity
    vector (rows: `(3, 2, 0, 2, 3)` excluding the tri-state
    cell) is mixed-parity → unreachable by rook-only.
  - L3 cannot be solved without triggering the
    `tri-state-cell` because the target cell at (2, 2) must
    be in state **2** (light-blue centre); state 2 is
    reachable only by EXACTLY two flips landing on (2, 2).
    Any sequence that produces fewer or more flips at (2, 2)
    leaves it in state 0 (no flips or 3) or state 1 (1 or 4
    flips). The witness fires bishop(1,1) and bishop(3,3),
    each of which lies on the main diagonal through (2, 2),
    delivering exactly 2 flips. A solution that doesn't
    touch (2, 2) twice — i.e., doesn't exercise the
    tri-state cycling — leaves (2, 2) in the wrong state.
- **Witness solution** (4 actions):
  ```
  [ACTION6 @ rook tile (0, 4)    =>  pixel (34, 2)]
  [ACTION6 @ rook tile (4, 0)    =>  pixel (2, 34)]
  [ACTION6 @ bishop tile (1, 1)  =>  pixel (10, 10)]
  [ACTION6 @ bishop tile (3, 3)  =>  pixel (26, 26)]
  ```
  (Click order is irrelevant for the binary cells — every
  flip is mod 2 commutative — but presented in this order
  for cleaner reading.)
- **Target pattern** (binary cells written 0/1, tri-state
  at (2,2) written `[2]` for state 2):
  ```
  0 1 0 1 1
  1 0 0 0 1
  0 0 [2] 0 0
  1 0 0 0 1
  1 1 0 1 0
  ```
- **Difficulty justification**:
  - **(a) Random-resistance**: 25-cell target with one
    tri-state cell and 24 binary cells gives `3 · 2²⁴ ≈
    50M` possible patterns; reachable cosets under 60
    clicks span a small fraction. Random play hits this
    specific target with vanishing probability (~10⁻⁵).
  - **(b) Human-tractable**: ~2.5 minutes. Discovery of the
    tri-state cell as a third mechanic happens when the
    player clicks something whose row/col includes (2, 2)
    twice and observes that (2, 2) goes light-grey →
    magenta → light-blue (instead of toggling). Planning
    then proceeds by composing rook flips to set the binary
    skeleton and exactly two bishop flips to deliver the
    tri-state state-2 outcome.
  - **(c) Planning depth (post-discovery)**: **challenging
    even for an attentive human**. After full discovery,
    the post-discovery decision space at level start is
    ≥ 25 (any of 25 cells). A trivial heuristic that fails:
    *"greedy-toward-target — for each cell mismatched
    against the target, click that cell to flip its row+col
    in the hope of getting closer"*. Walking that
    heuristic from the start state (all dark) toward the L3
    target: the first mismatched cell scanned in
    row-major order is (0, 1) (target lit). Greedy clicks
    (0, 1) → flips row 0 + col 1, which OVER-flips (1,1)
    (a bishop tile, but the click is on a rook tile so
    the row 1 part of the rook flip lights (1,1)). Then
    (0, 3) is still dark in the target (it's actually
    lit `0 1 0 1 1`)... wait target (0, 3) = 1, after the
    greedy first click (0, 1) we have row 0 lit
    `0 1 1 1 1` (note (0,0) flipped by col-1 too: col 1's
    flip touches (i,1) for all i, but row 0's flip touches
    (0, j) for all j; so (0, 0) is in row 0 → flipped to 1,
    not 0 as target needs). Greedy diverges at click 1
    already. The heuristic and the witness disagree at the
    very first step — greedy clicks (0, 1) (a non-witness
    cell), the witness clicks (0, 4). Greedy never
    recovers in 60 clicks because each row-major-mismatch
    fix re-creates earlier mismatches; ahead-of-time
    reasoning over the linear-algebra structure (the
    target's row-parity vector tells you which rooks must
    fire; the diagonal-parity tells you which bishops; the
    tri-state count tells you how many clicks must touch
    (2, 2)) is required.
  - **(d) Step budget**: 60 (≥ 50, the L2 budget; never
    shrinking).

## 5. Action mapping

`available_actions = [6]` (CLICK only).

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click at pixel `(x, y)`; converted to cell `(col, row)`; clicked tile's *type* (rook / bishop / tri-state) determines the click rule applied | always; out-of-grid clicks are no-ops (no state change, no step consumed) |

Click rule per cell type:

- **Rook tile clicked**: toggle state mod 2 of every tile in row `row`
  OR col `col`. The *clicked tile is included* in the flip (it's in
  both its own row and col but in the set-union, gets flipped exactly
  once). The tri-state cell at (2, 2) in L3, when touched by a rook
  click whose row+col includes (2, 2), advances its mod-3 cycle by 1.
- **Bishop tile clicked**: toggle state mod 2 of every tile on the
  main diagonal through `(col, row)` (`i − j = col − row`) OR the
  anti-diagonal through `(col, row)` (`i + j = col + row`). The
  clicked tile gets flipped once (set-union). The tri-state cell at
  (2, 2) in L3, when touched by a bishop click whose flip-region
  contains (2, 2), advances its mod-3 cycle by 1.
- **Tri-state tile clicked**: **no-op** (no state change). The step
  counter still decrements by 1 — this is the only "wasted-click
  punishment" in the game and is intentional; tri-state tiles are
  designed to be observed and reasoned about, not directly clicked.
  In all 3 levels, the witness solution never clicks the tri-state
  tile directly.

Slot 5 (the freedom-slot verb) is intentionally absent — the
distinctive verb of qf8m is encoded into ACTION6 by the choice
of WHICH cell type the player clicks. This follows the
"distinctive verb on ACTION6" pattern from `action-enum.md`,
observed in lp85 / vc33 / ft09. Slot 7 (undo) is omitted: there
is no in-game undo verb. (Each binary click is self-inverse
under Z₂ — re-clicking the same cell undoes it on binary tiles
— but tri-state cells in L3 are not self-inverse, so a "true"
undo would need explicit history. Since the puzzle structure is
forgiving (60-click budget vs 4-click witness), undo is not
required.)

## 6. HUD and per-game state

### HUD (`RenderableUserDisplay`)

- **`StepCounterHud`** — paints row 63 across the full 64-px
  width: `current_steps / max_steps` proportion in palette 6
  (magenta), the rest in palette 4 (off-black). Decrements 1
  per non-RESET action. Re-armed in `on_set_level` to
  `level.get_data("step_budget")`.

### Per-game internal state

- `_grid_state: dict[(col, row) → int]` — current state of every
  cell. `0` for dark in binary tiles, `1` for lit in binary
  tiles, `0/1/2` for tri-state.
- `_target_state: dict[(col, row) → int]` — target state for
  each cell, populated in `on_set_level` from a per-level
  `target_pattern` data dict.
- `_cell_kind: dict[(col, row) → "rook" | "bishop" | "tristate"]`
  — the click-rule selector for each cell, populated in
  `on_set_level` from each level's sprite layout.
- `_rook_sprite_at: dict[(col, row) → tuple[Sprite, Sprite]]`
  — `(dark_sprite, lit_sprite)` pair for each rook cell, used
  by the two-sprite-swap idiom (interaction TANGIBLE/REMOVED
  swap) when state changes. Same for bishop.
- `_tristate_sprites_at: dict[(col, row) → tuple[Sprite,
  Sprite, Sprite]]` — `(s0, s1, s2)` triple for the tri-state
  cell, swapped via the same idiom.
- `_max_steps: int`, `_steps_remaining: int` — budget bookkeeping.

`_get_hidden_state` returns a 5×5 int16 array packing the
current `_grid_state` so the engine's `(frame, hidden_state)`
graph hash distinguishes states that render identically when
the hidden tri-state cycle has progressed (e.g., a state-1
tri-state cell vs an off-by-one mirror situation).

## 7. Win condition

After every action, compare `_grid_state` cell-by-cell to
`_target_state`. If equal for every cell, call
`self.next_level()`. After L3's `next_level()`, the engine's
default behaviour fires `self.win()` (3-level cap reached).

## 8. Lose condition

`_steps_remaining` reaches 0 with `_grid_state ≠
_target_state`. Call `self.lose()`. There is no instant-fail
hazard, no soft-lock pathway: every binary click is
self-inverse (re-clicking the same cell undoes it), and every
tri-state click can be re-cycled through state 2 by two more
flips. The budget is the sole pressure.

## 9. Novelty note

### Closest entries in `taxonomy-of-25-games.md`

- **`ft09` — `stamp-3x3-paint`**. Distinguishing rule: ft09's
  flip-region is a tunable 3×3 stamp (configurable mid-puzzle
  by clicking template tiles), and its win predicate is local
  constraint-graph satisfaction (each constraint sprite encodes
  equality/inequality rules for its 8 boundary cells). qf8m's
  flip-region is a fixed (2N−1)-cell rook-cross (no template
  switching), and its win predicate is target-image equality
  over the full grid.
- **`lp85` — `row-col-shift-grid`**. Distinguishing rule:
  lp85 permutes token POSITIONS along a row/column on each
  click; qf8m TOGGLES tile STATES. lp85 has external arrow
  buttons; qf8m has none — clicks land directly on grid cells.
- **`vc33` — `row-slide-pull-tab`**. Distinguishing rule:
  vc33 slides one row OR one column positionally per click on
  a tab; qf8m flips one row AND one column simultaneously per
  click on a cell. Position-shift vs state-flip; one-axis vs
  two-axis.
- **`hp9c` — `pinwheel-cell-rotate`**. Distinguishing rule:
  hp9c rotates a 4-cell ring around a clicked cell (cyclic
  positional permutation, local); qf8m flips a (2N−1)-cell
  rook-cross (parity change of states, global reach).

### Closest entries in `prior-games/index.md`

- **`tm5x` — `thermal-aura-imprint`**. Distinguishing rule:
  tm5x stamps a local 5-cell plus-shape (centre + 4 cardinal
  neighbours) when the avatar fires; qf8m flips the entire
  (2N−1)-cell row+column rook-cross when a cell is clicked.
  Local 5-cell stamp vs global (2N−1)-cell rook-cross; pawn-
  carried stamp via avatar movement vs click-anywhere on a
  static grid; thermal value imprint vs state toggle.
- **`gh4r` — `repulsion-herd-corral`**. Distinguishing rule:
  gh4r aligns a warden along a row/col to *push* drifters one
  cell along that axis; qf8m clicks a cell to *flip the state*
  of the row+col. Positional motion vs state toggle. gh4r
  involves autonomous drifter agents; qf8m has no agents —
  every state change is player-driven by clicks.
- **`qx7p` — `column-shift-row-align`** (also a taxonomy
  near-miss). Distinguishing rule: qx7p slides band columns
  positionally past a horizontal scan line; qf8m flips
  row+column states in place at the clicked cell. Position
  shift vs state flip; one-axis vs two-axis click effect.
- **`rk7x` — `live-switch-routing`**. Distinguishing rule:
  rk7x toggles a junction blade's orientation (a per-cell
  rotation, local); qf8m flips state of every tile in row+col
  (global reach, 2N−1 cells per click). rk7x has an
  autonomous courier walking the grid; qf8m has no agents.

No prior matches qf8m on (family, primary action, primary
constraint, win type) jointly. The negative-similarity check
(8 dimensions vs ft09 / lp85 / vc33 / tm5x) was walked in
`mechanic-pick.md`; max shared-dimension count was 2 (vs
ft09), well under the 3+ rejection threshold, with all three
named principles (palette, pixel grain, core dynamic)
diverging cleanly.

---

## Notes (derivation of the targets — for critique self-check, not part of the spec contract)

### L1 target derivation
Starting from all-zero grid. Click rook(1,1) flips cells with
i = 1 OR j = 1. Click rook(3,3) flips cells with i = 3 OR
j = 3. Cell (i, j)'s final state = (i ∈ {1, 3}) XOR (j ∈
{1, 3}). Tabulating:

| i\j | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 1 |
| 2 | 0 | 1 | 0 | 1 | 0 |
| 3 | 1 | 0 | 1 | 1 | 1 |
| 4 | 0 | 1 | 0 | 1 | 0 |

Witness verified: 2 actions, target produced.

### L2 target derivation
Click rook(2,2): cells with i = 2 OR j = 2 → row 2 + col 2 lit.
Click bishop(1,1): cells on main `i − j = 0` ∪ anti `i + j = 2`
→ {(0,0),(1,1),(2,2),(3,3),(4,4),(0,2),(2,0)}.
Click bishop(3,3): cells on main `i − j = 0` ∪ anti `i + j = 6`
→ {(0,0),(1,1),(2,2),(3,3),(4,4),(2,4),(4,2)}.
XOR all three:

- Cells in row 2 from rook only: (2,1),(2,3) → 1 each.
- Cells in col 2 from rook only: (1,2),(3,2) → 1 each.
- Centre (2,2): rook + bishop1 (main) + bishop2 (main) = 3 → 1.
- Diagonal cells (0,0),(1,1),(3,3),(4,4): bishop1 + bishop2 =
  2 each → 0.
- Anti-2 extras (0,2),(2,0): rook(j=2 / i=2) + bishop1 (anti) =
  2 each → 0.
- Anti-6 extras (2,4),(4,2): rook(i=2 / j=2) + bishop2 (anti) =
  2 each → 0.

Lit cells: (1,2),(2,1),(2,2),(2,3),(3,2). 5-cell plus.

### L3 target derivation
Click rook(0,4) flips i=0 OR j=4. Click rook(4,0) flips i=4 OR
j=0. Click bishop(1,1) flips i−j=0 OR i+j=2. Click bishop(3,3)
flips i−j=0 OR i+j=6.

Per-cell flip count, mod 2 for binary cells, mod 3 for the
tri-state cell at (2,2):

| (i,j) | rook(0,4) | rook(4,0) | b(1,1) | b(3,3) | total | state |
|---|---|---|---|---|---|---|
| (0,0) | 1 (i=0) | 1 (j=0) | 1 (main) | 1 (main) | 4 | 0 |
| (0,1) | 1 (i=0) | 0 | 0 | 0 | 1 | 1 |
| (0,2) | 1 (i=0) | 0 | 1 (anti=2) | 0 | 2 | 0 |
| (0,3) | 1 (i=0) | 0 | 0 | 0 | 1 | 1 |
| (0,4) | 1 (i=0,j=4) | 0 | 0 | 0 | 1 | 1 |
| (1,0) | 0 | 1 (j=0) | 0 | 0 | 1 | 1 |
| (1,1) | 0 | 0 | 1 (main) | 1 (main) | 2 | 0 |
| (1,2) | 0 | 0 | 0 | 0 | 0 | 0 |
| (1,3) | 0 | 0 | 0 | 0 | 0 | 0 |
| (1,4) | 1 (j=4) | 0 | 0 | 0 | 1 | 1 |
| (2,0) | 0 | 1 (j=0) | 1 (anti=2) | 0 | 2 | 0 |
| (2,1) | 0 | 0 | 0 | 0 | 0 | 0 |
| **(2,2) tri** | 0 | 0 | 1 (main) | 1 (main) | **2** | **state 2** |
| (2,3) | 0 | 0 | 0 | 0 | 0 | 0 |
| (2,4) | 1 (j=4) | 0 | 0 | 1 (anti=6) | 2 | 0 |
| (3,0) | 0 | 1 (j=0) | 0 | 0 | 1 | 1 |
| (3,1) | 0 | 0 | 0 | 0 | 0 | 0 |
| (3,2) | 0 | 0 | 0 | 0 | 0 | 0 |
| (3,3) | 0 | 0 | 1 (main) | 1 (main) | 2 | 0 |
| (3,4) | 1 (j=4) | 0 | 0 | 0 | 1 | 1 |
| (4,0) | 0 | 1 (i=4,j=0) | 0 | 0 | 1 | 1 |
| (4,1) | 0 | 1 (i=4) | 0 | 0 | 1 | 1 |
| (4,2) | 0 | 1 (i=4) | 0 | 1 (anti=6) | 2 | 0 |
| (4,3) | 0 | 1 (i=4) | 0 | 0 | 1 | 1 |
| (4,4) | 1 (j=4) | 1 (i=4) | 1 (main) | 1 (main) | 4 | 0 |

Final grid:
```
0 1 0 1 1
1 0 0 0 1
0 0 [2] 0 0
1 0 0 0 1
1 1 0 1 0
```
Witness verified: 4 actions, target produced. Tri-state cell
ends in state **2** ✓.
