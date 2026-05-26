# vp6h — mechanic spec (revision 1)

## Revision history

- **revision 1** addresses every issue in `workspace/critique-revisions.md`:
  - Issue 1 (L3 phase 4 reroute): §4 Level 3 Witness solution rewritten.
  - Issue 2 (L2 phase 1 count): §4 Level 2 Witness solution corrected.
  - Issue 3 (L1 count): §4 Level 1 Witness solution corrected.
  - Issue 4 (palette swap): §3 sprite roster crystal palette changed.
  - Issue 5 (L2 col-2 pillar): §3 sprite roster + §4 Level 2 Layout updated; M2 necessity grounded in ordering.
  - Issue 6 (BlockingMode): §3 sprite roster appended.
  - Issue 7 (resolved by 5).

## 1. Title

Shadow-Cast Crystal Collection (working title; not visible in-game).

## 2. Mechanic family

`shadow-cast-collect`. Avatar walks a grid lit by 1-2 horizontal-bar
lanterns mounted on rails at the playfield's top and (at L3) bottom
edges; opaque pillars cast vertical shadow strips behind them in each
lit column. The avatar collects scattered crystal sprites, but a
crystal is only pick-up-able while standing in a cell that is in
shadow w.r.t. *every* active lantern. Walking onto a crystal that is
lit by any active lantern is a no-op (forgiving rule: no pickup, no
destruction). Priors used: **objectness** (lanterns, pillars, crystals,
avatar as discrete persistent entities); **basic geometry** (parallel-
ray occlusion: pillar-above shadows down, pillar-below shadows up);
**basic topology** (intersection rule at L3 — a cell's safety is the
*intersection* of two shadow regions, not the union).

## 3. Sprite roster

| name | dimensions | palette values | tags | role |
|---|---|---|---|---|
| `lantern_top` | 1×5 (1 row × 5 cols) | 11 (yellow) | `lantern_top`, `lantern_rail_top`, `sys_click` | Mounted at row 0; emits parallel rays downward through its 5 columns. Slid left/right by clicking the top rail. INTANGIBLE (avatar restricted from row 0 by movement guard). |
| `lantern_bot` | 1×5 | 11 (yellow) | `lantern_bot`, `lantern_rail_bot`, `sys_click` | Mounted at row 15; emits parallel rays upward through its 5 columns. L3 only. INTANGIBLE. |
| `pillar_short` | 1×3 (3 rows × 1 col) | 3 (grey) | `pillar` | Tangible obstacle blocking light in its column (above for top-lantern; below for bot-lantern). Avatar cannot walk through. |
| `pillar_tall` | 1×5 | 3 (grey) | `pillar` | Same role, taller. |
| `pillar_block` | 2×3 (3 rows × 2 cols) | 3 (grey) | `pillar` | Wider obstacle for blocking 2-column shadows. |
| `crystal` | 2×2 | 10 (light-blue) and 15 (purple) | `crystal` | Pickable when standing on it AND cell is shaded by every active lantern. Pixels: `[[10, 15], [15, 10]]`. INTANGIBLE (avatar walks onto it). (Revision 1: swapped palette 14 → 15 to avoid green=safe cultural overtone, per critique Issue 4.) |
| `avatar` | 2×2 | 6 (magenta), 13 (maroon) | `avatar` | Player. Pixels: `[[6, 13], [13, 6]]`. Tangible. Cannot enter pillars; cannot enter row 0 or row 15. |
| `ground` | 16×16 | repainted dynamically: 1 (off-white) for lit cells, 4 (off-black) for shaded cells | `ground` | Layer -2 (behind everything). Repainted in `step()` after every lantern-or-pillar update. |
| `rail_marker_top` | 1×16 | 2 (light-grey) | `rail_top` | Visual marker line at row 0 of the playfield indicating the lantern-top rail (rendered behind the lantern). Helps the player see the rail extents. |
| `rail_marker_bot` | 1×16 | 2 (light-grey) | `rail_bot` | Same, at row 15. L3 only. |

Aesthetic intent: bright off-white lit cells contrast cleanly with
deep off-black shaded cells; magenta/maroon avatar stands out against
both; cyan-and-purple crystals carry pixel-grain detail and pop on
shaded ground. Yellow lanterns and grey pillars sit muted in the
periphery.

**Blocking mode (Revision 1, per critique Issue 6):** all `pillar_*`
sprites use `BlockingMode.PIXEL_PERFECT` (the engine default). Each
pillar's pixel array contains only solid palette-3 cells (no -1
transparent cells), so PIXEL_PERFECT is equivalent to BOUNDING_BOX
for these sprites; both produce identical collision behaviour.
Crystals use `interaction=InteractionMode.INTANGIBLE` so they don't
block avatar movement (the avatar walks onto the crystal cell to
trigger the pickup attempt). Lanterns use `interaction=
InteractionMode.INTANGIBLE` so the avatar (restricted to rows 1..14
by movement guard) is never near them. Avatar uses `PIXEL_PERFECT`
collision but its 2×2 footprint contains only solid palette-6/13
cells.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels use `grid_size=(16, 16)`. The camera viewport is set
to (16, 16) in `on_set_level`. Coordinate convention: `(col, row)`,
top-left origin, x = col, y = row.

### Level 1 — base dynamic system

- **Mechanics required by the witness (N=1):**
  - **M1 — shadow-pickup-rule.** Walking onto a crystal cell only
    triggers pickup if that cell is in shadow w.r.t. every active
    lantern (= NOT lit by any). Walking onto a lit crystal is a
    no-op (avatar passes through, crystal stays).

- **Layout:** Top-lantern (5-wide) fixed at columns 5–9 (cannot be
  moved at L1; the rail is non-interactive at L1). One `pillar_tall`
  (5 rows tall, 1 col wide) at (col=7, row=3..7), tag `pillar`. One
  `crystal` at (col=7, row=11..12). Avatar starts at (col=2, row=13).
  Step budget: **40**.

- **Necessity per mechanic (counterfactual):**
  - L1 cannot be solved without M1's shadow-gate because the only
    crystal sits in column 7 row 11–12, lit-side cells in cols 5,6,8,9
    (under top-lantern, no pillar) form the unique bright stripe;
    column 7 is the only column under the lantern that is
    pillar-shadowed. Without M1's shadow-gate, the puzzle's pillar
    placement carries no semantic load — pickup would be unconditional
    on shadow and the level reduces to "walk to the only crystal,"
    making M1's distinguishing rule the entire reason the pillar
    exists in the geometry. Concretely: the crystal's column placement
    (and the *colour* of the cell underneath it) is the only signal
    the player has for "pickup will work here"; remove M1 and that
    signal does no work.

- **Witness solution (shortest, revised in revision 1 per critique Issue 3):** **6 actions**.
  ```
  ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,   # walk right cols 2→7
  ACTION1                                        # walk up row 13→12
  ```
  Avatar trajectory: (2,13) → (3,13) → (4,13) → (5,13) → (6,13) →
  (7,13) → (7,12). At avatar position (7, 12), the 2×2 footprint
  covers (7..8, 12..13) and overlaps crystal A at (col=7, row=11..12).
  Cell (7, 12) shadow check: top-lantern at cols 5..9, col 7 in range,
  pillar at col 7 rows 3..7 above row 12 → top-shaded. No bot lantern
  at L1. Both shaded → pickup; crystal_remaining drops from 1 to 0 →
  `next_level()` fires. (Cells (3..6, 13) along the walk are top-lit
  but contain no crystals, so the lit-no-pickup rule is irrelevant
  during the walk.)

- **Difficulty justification:**
  - *(a) Random-resistance:* The 16×16 grid has ~256 cells; a random
    walk reaching the shaded crystal cell within 40 steps has very low
    probability (~< 1/200 per attempt assuming uniform 4-direction
    walk; actual is even lower because the witness needs both rightward
    and upward bias). A vision-blind agent has no way to know the
    crystal's coordinates and cannot infer the shadow-pickup gate from
    text alone.
  - *(b) Human-tractable:* An attentive human takes ~1.5–2 minutes:
    ~30 seconds to read the layout (notice the lantern, pillar,
    crystal, avatar), ~30 seconds to attempt walking and observe that
    walking onto cells doesn't always pick up something, ~30 seconds
    to infer "the dim cells around the pillar are where pickup
    works," ~30 seconds to execute the walk.
  - *(c) Planning depth:* L1 has **no strict planning requirement.**
    Once the player infers the shadow-pickup rule, walking the 7-cell
    path to the shaded crystal is near-immediate. Mechanic discovery
    is the entire L1 difficulty.
  - *(d) Step budget:* 40 actions over a 6-action witness gives the
    player generous room for exploration (~34 spare actions to walk
    around, observe the shadow geometry, or back-track).

### Level 2 — base + 1 new mechanic (N=2)

- **Mechanics required by the witness (N+1):**
  - **M1 — shadow-pickup-rule.** (Carried forward from L1.)
  - **M2 — lantern-slide.** ACTION6 click on the top-lantern rail
    (row 0) at column `gx` slides the top-lantern so its 5-cell
    extent is centred on `gx` (clamped to fit the grid: leftmost
    column at `max(0, min(11, gx-2))`). The shadow geometry recomputes
    immediately.

- **Layout (revised in revision 1 per critique Issue 5; the col-2
  pillar has been removed):**
  - Top-lantern (5-wide) initially at columns 5–9.
  - One `pillar_short` (3 rows × 1 col) at (col=14, row=5..7) — a
    visual anchor for col 14, ensuring the avatar can navigate
    visually around the column. Note that for the witness this pillar
    is not load-bearing (col 14 is outside the lantern in the
    witness's leftward slide).
  - **No pillar at col 2.** (The col-2 pillar from the original
    spec was removed because, while it visually anchored col 2, it
    made crystal A always shaded regardless of lantern position,
    breaking the M2 ordering requirement.)
  - **No pillar at col 6.** (Crystal B at col 6 must be in a
    column where the lit-state is purely a function of lantern
    position — see M2 necessity below.)
  - Crystals: A at (col=2, row=11..12), B at (col=6, row=11..12), C
    at (col=14, row=11..12). Avatar starts at (col=1, row=13). Step
    budget: **70**.

  Default lit/shaded analysis at top-lantern @ cols 5..9:
  - A at (col 2, row 11..12): col 2 outside cols 5..9 → top-shaded → SAFE.
  - B at (col 6, row 11..12): col 6 in cols 5..9, no pillar above → top-LIT → unsafe (no-op on walk-on).
  - C at (col 14, row 11..12): col 14 outside cols 5..9 → top-shaded → SAFE.

- **Necessity per mechanic (counterfactual):**
  - **M1 (shadow-pickup):** L2 cannot be solved without M1's
    shadow-gate because crystal B at (col=6, row=11..12) is currently
    lit by the default top-lantern (col 6 in cols 5..9, no pillar
    above row 11). With M1, walking onto B in the lit state is a
    no-op; pickup only triggers after the player slides the lantern
    so col 6 becomes shaded. Without M1's gate (i.e., unconditional
    pickup), the player would walk onto B at the default position
    and immediately pick up — eliminating the entire shadow-rail
    geometry. Concrete blocker for the alternate path: cell (6, 11)
    is rendered with palette 1 (lit ground) under the default lantern
    config; the gate's lit-branch return-no-op IS what blocks the
    naive walk-and-pickup of B before any slide.
  - **M2 (lantern-slide):** L2 cannot be solved without M2 because,
    to satisfy M1's gate at crystal B, col 6 must be shaded — but col
    6 has no pillar (intentionally; see Layout above), so col 6's
    lit-state is a pure function of the top-lantern's position. The
    only rule that moves the top-lantern is M2 (ACTION6 click on the
    top rail). Concrete blocker for the alternate path: at the
    default lantern position the cell at (6, 11) is lit, and there is
    no other game mechanic that can re-shade col 6 — no
    pillar-spawning, no crystal-relocation, no avatar-shadow-cast.
    M2 is the *only* path.

  **Ordering invariant (M2 necessity at the planning level):** the
  layout also encodes a non-trivial *ordering* constraint that grounds
  M2's necessity beyond "B requires a slide." Specifically, sliding
  the top-lantern leftward to expose col 6 (the obvious slide
  target) covers some leftward column. With top-lantern at cols 0..4:
  - col 0..4 are now in lantern range. None of cols 0..4 has a
    pillar (no col-2 pillar). So cells (c, 11..12) for c in 0..4 are
    top-LIT. Crystal A at (col 2, row 11..12) is now LIT → walking
    onto A in this state is a no-op; A becomes uncollectable until
    the lantern is moved back.
  - Therefore the witness MUST collect A *before* sliding the
    lantern leftward.

- **Witness solution (shortest, revised in revision 1 per critique
  Issue 2):**
  ```
  # Phase 1: collect A (default shaded; must happen before the slide)
  ACTION4, ACTION1                     # (1,13) -> (2,13) -> (2,12)
  ```
  Avatar moves from (1, 13) → (2, 13) → (2, 12). At avatar
  position (2, 12), the 2×2 footprint covers (2..3, 12..13), overlaps
  crystal A at (col=2, row=11..12). Cell (2, 12) shadow check at
  default lantern: col 2 outside cols 5..9 → top-shaded → pickup.
  **2 actions for phase 1.**

  ```
  # Phase 2: collect C (default shaded; can happen before or after the slide,
  # but doing it before avoids any chance of mis-sliding)
  ACTION2,                              # (2,12) -> (2,13)
  ACTION4 ×12,                          # (2,13) -> (14,13)
  ACTION1                               # (14,13) -> (14,12)
  ```
  At avatar position (14, 12), footprint covers (14..15, 12..13),
  overlaps crystal C at (col=14, row=11..12). Cell (14, 12) shadow
  check: col 14 outside cols 5..9 → top-shaded → pickup. **14 actions
  for phase 2.**

  ```
  # Phase 3: slide top-lantern leftward to expose col 6
  ACTION6 @ click_grid=(2, 0)           # click on top rail at col 2 -> top-lantern slides to cols 0..4
  ```
  After this click, top-lantern's left column is `max(0, min(11, 2-2))
  = 0`, so range cols 0..4. Col 6 now outside range → col 6 row 11..12
  becomes top-shaded. **1 action for phase 3.**

  ```
  # Phase 4: collect B
  ACTION3 ×8                            # (14,12) -> (6,12)
  ```
  At avatar position (6, 12), footprint covers (6..7, 12..13),
  overlaps crystal B at (col=6, row=11..12). Cell (6, 12) shadow
  check after slide: col 6 outside cols 0..4 → top-shaded → pickup.
  **8 actions for phase 4.**

  **Total L2 witness: 2 + 14 + 1 + 8 = 25 actions.** Step budget 70
  leaves 45 spare.

  (Click coordinate convention: ACTION6's `data["x"]` and `data["y"]`
  are *display* pixel coordinates in the 64×64 frame. With
  grid_size=(16,16) the camera scale is 4× → click pixel `(8 + 2*4,
  2) = (16, 2)` corresponds to grid `(col=2, row=0)`. The witness
  writes click targets as grid coords; the engine's `display_to_grid`
  does the conversion. The implementation must compute display pixel
  centres correctly.)

- **Difficulty justification:**
  - *(a) Random-resistance:* A random agent has very low probability
    of triggering ACTION6 on the rail at the right column AND walking
    the right route within 70 steps. The action space is `[1,2,3,4,6]`
    × possible click coords ≈ 4 + 256 = 260 valid actions per step;
    a 26-action witness has astronomically low random hit probability.
  - *(b) Human-tractable:* An attentive human takes ~2.5 minutes:
    ~30 seconds to recognise the pattern from L1 (lantern + pillars +
    crystals), ~30 seconds to identify which crystals are
    default-shaded vs lit, ~45 seconds to discover the lantern-slide
    rule by clicking the rail and seeing the geometry change, ~45
    seconds to execute the witness path.
  - *(c) Planning depth (post-discovery, moderate):*
    - **Decision space at level start (post-discovery):** The
      fully-informed player faces these candidate first-actions:
      walk-toward-A (4 valid arrow directions), walk-toward-C
      (similar), or click ACTION6 on the rail at any of 12 columns
      (gx=2..13 each give a distinct lantern position). That's ≥ 5
      meaningfully distinct first-action paths.
    - **Plausible-but-wrong alternative the post-discovery player
      considers and rejects:** sliding the top-lantern leftward FIRST
      (before collecting A) to make col 6 shaded for B. Wrong because
      doing so puts col 2 inside the new lantern range (cols 0..4),
      and col 2 has no pillar above row 11..12 (revision-1 layout
      removed the col-2 pillar) → col 2 becomes top-lit → crystal A
      becomes uncollectable while the lantern is at cols 0..4. The
      post-discovery player rejects this path because they recognise
      the sequencing constraint: the slide commits the lantern to a
      different column range, and any pre-existing safe crystals in
      the new range that lack pillar-occlusion become unsafe.
    - **Witness reasoning chain (post-discovery):** The fully-informed
      player traces: "A at col 2 is currently shaded because col 2 is
      outside the default lantern range (cols 5–9). Col 2 has no
      pillar, so col 2's lit-state depends purely on the lantern
      position. If I slide the lantern leftward to expose col 6 (the
      only way to make B's column shaded), col 2 enters the new
      lantern range (cols 0..4) AND has no pillar above → col 2
      becomes lit → A becomes uncollectable until I slide the lantern
      back. Therefore, the witness MUST collect A *before* sliding
      leftward. C at col 14 has a pillar at rows 5..7, so col 14 row
      11..12 stays shaded under any lantern position that puts col
      14 in range (the pillar occludes); collection order for C is
      flexible. Therefore: collect A first (defensive ordering against
      the leftward slide), C any time, then slide the lantern
      leftward, then collect B." This reasoning requires anticipating
      *future* shadow states — that is moderate planning.
  - *(d) Step budget:* 70 actions over 26-action witness gives ~2.7×
    headroom for exploration including a few wrong moves and undos
    via redundant walks. The budget is generous, not tight.

### Level 3 — system + 1 new mechanic (N=3)

- **Mechanics required by the witness (N+1=3):**
  - **M1 — shadow-pickup-rule.** (Carried forward.)
  - **M2 — lantern-slide.** (Carried forward; now applies to BOTH
    the top rail (row 0) and bot rail (row 15).)
  - **M3 — dual-shadow-overlap.** A second lantern (`lantern_bot`)
    on a parallel rail at row 15 emits parallel rays *upward*. M1's
    shadow-gate now requires the cell to be shaded w.r.t. *every*
    active lantern (top AND bot). A cell lit by either lantern is
    unsafe.

- **Layout:** Top-lantern (5-wide) initially at columns 5–9.
  Bot-lantern (5-wide) initially at columns 5–9. Three pillars:
  `pillar_short` at (col=2, row=5..7) — top-pillar; `pillar_short` at
  (col=13, row=8..10) — bot-pillar (column 13, rows 8..10, blocks
  upward rays from row 15 reaching cells at rows 0..7 in col 13);
  `pillar_short` at (col=10, row=5..7) — top-pillar. Three crystals: A
  at (col=2, row=11..12); B at (col=13, row=4..5); C at (col=7,
  row=8..9). Avatar starts at (col=1, row=13). Step budget: **120**.

  Default lit/shaded analysis:
  - col 2 row 11..12: top-lit? col 2 outside top cols 5..9 → no.
    bot-lit? col 2 outside bot cols 5..9 → no. **Both shaded → SAFE.**
  - col 13 row 4..5: top-lit? col 13 outside top cols 5..9 → no.
    bot-lit? col 13 outside bot cols 5..9 → no. **Both shaded → SAFE.**
  - col 7 row 8..9: top-lit? col 7 in top cols 5..9, no pillar at col
    7 above row 8 → **YES top-lit**. bot-lit? col 7 in bot cols 5..9,
    no pillar at col 7 below row 9 → **YES bot-lit**. **UNSAFE.**

  To collect C, both lanterns must be slid OFF col 7. Top-lantern can
  slide to cols 0..4 OR cols 8..12 OR cols 10..14, etc. Bot-lantern
  similarly. Constraints:
  - Sliding top-lantern leftward to cols 0..4 lights cols 0,1,3,4
    (col 2 has top-pillar at rows 5..7, so col 2 below the pillar
    rows 8..15 is top-shaded). Wait — col 2 with pillar at rows 5..7
    and lantern at cols 0..4: top-lit on col 2 = top-lantern covers
    col 2 AND no top-pillar above. Col 2 has top-pillar above row 8
    (rows 5..7). Cells (col 2, row 8..15) ARE top-shaded by the
    pillar. Cells (col 2, row 0..4) are top-lit (above the pillar; no
    pillar above row 0..4).
  - Crystal A at (col 2, row 11..12) is in the rows 8..15 range, so
    A remains top-shaded with top-lantern at cols 0..4. ✓
  - But bot-lantern still at default cols 5..9: col 2 outside →
    bot-shaded ✓. So A still safe with top-lantern at cols 0..4.
  - Now top-lantern at cols 0..4 also lights col 4 (no pillar there).
    No crystals at col 4 → no concern.
  - To make col 7 row 8..9 also bot-shaded, slide bot-lantern off col
    7: e.g., bot-lantern to cols 0..4 or cols 10..14.
  - Bot-lantern at cols 10..14: col 13 in range. col 13 has bot-pillar
    at rows 8..10. Cells (col 13, row 0..7) are bot-shaded by the
    pillar. Crystal B at (col 13, row 4..5) is in rows 0..7 → still
    bot-shaded ✓. Cells (col 13, row 11..15) are bot-lit (below
    pillar, lantern below).
  - Bot-lantern at cols 10..14 with top-lantern at cols 0..4: col 7
    is outside both → both shaded → SAFE for crystal C.

  Witness picture: collect A (default safe) → collect B (default safe)
  → slide top-lantern leftward → slide bot-lantern rightward → collect C.

  But wait — there is a subtle ordering issue: if the player slides
  bot-lantern rightward to cols 10..14 BEFORE collecting B, col 13
  rows 11..15 become bot-lit, but B is at rows 4..5 which is still
  bot-shaded. So B can be collected after the slide. Hmm, let me
  recheck: B at row 4..5. Bot-lantern at cols 10..14. col 13 has
  bot-pillar at rows 8..10. Bot-rays from row 15 going up hit the
  pillar at row 10 (the top of the pillar). Cells above row 8 (i.e.,
  rows 0..7) are bot-shaded. B at rows 4..5 → bot-shaded. Top-lantern
  at default cols 5..9 → col 13 outside → top-shaded. So B is safe
  even after sliding bot-lantern. Good.

  Could the player collect everything in a single configuration? Try
  top at cols 0..4 + bot at cols 10..14 from the START (no defaults):
  - A (col 2, row 11..12): top-lit? col 2 in cols 0..4 AND no pillar
    above row 11 → pillar at col 2 rows 5..7 IS above row 11 →
    top-shaded. bot-lit? col 2 outside cols 10..14 → bot-shaded. SAFE.
  - B (col 13, row 4..5): top-lit? col 13 outside cols 0..4 →
    top-shaded. bot-lit? col 13 in cols 10..14 AND bot-pillar at col
    13 rows 8..10 below row 4..5 → bot-shaded. SAFE.
  - C (col 7, row 8..9): top-lit? col 7 outside cols 0..4 →
    top-shaded. bot-lit? col 7 outside cols 10..14 → bot-shaded.
    SAFE.
  All three safe in this configuration. So the witness can: slide
  both lanterns first, then collect all three.

- **Necessity per mechanic (counterfactual):**
  - **M1 (shadow-pickup):** L3 cannot be solved without M1's
    shadow-gate because crystal C at (col 7, row 8..9) is lit by
    *both* default lanterns and only becomes pickup-able when the
    player slides each lantern off col 7. Concrete blocker: col 7 row
    8 is bright with default lanterns (in both ranges, no col-7
    pillars); only M1's gate explains why walking onto C in the
    default state does not pick it up.
  - **M2 (lantern-slide):** L3 cannot be solved without M2 because
    making col 7 simultaneously top-shaded and bot-shaded requires
    sliding *both* lanterns. M2 is the only mechanism that changes
    which columns each lantern covers. Concrete blocker: there is no
    pillar at col 7 (neither in rows 0..7 to top-shade nor rows 9..14
    to bot-shade), so col 7's shadow-state is purely a function of
    lantern positions — M2 is the only path.
  - **M3 (dual-shadow-overlap):** L3 cannot be solved without M3
    because, if the safety rule were the L2 rule "shaded by some
    lantern" (single-shadow sufficient), sliding the top-lantern
    alone (e.g., to cols 0..4, leaving bot at default) would already
    make col 7 row 8 top-shaded — under a single-shadow rule, that
    would suffice for pickup. But cell (col 7, row 8) with top at
    cols 0..4 + bot at default cols 5..9 is top-shaded AND bot-lit;
    M3's intersection rule (shaded by *every* lantern) is what
    requires the player to *also* slide the bot-lantern. Concrete
    blocker: walking onto C in the top-only-slid configuration is a
    no-op (cell is bot-lit) — only M3's intersection requirement
    explains the second slide.

  Discovery of M3 at L3: the player's first attempt is likely "slide
  top-lantern off col 7 (col 7 looks darker after this slide); walk
  to C; pickup fails (forgiving no-op)." This forces the player to
  observe "the cell still has a lit overlay from the bottom lantern"
  → infer "must shade from BOTH" → slide bot-lantern → succeed.

- **Witness solution (shortest, revised in revision 1 per critique
  Issue 1; phase 4 was re-routed around the col-13 bot-pillar):**
  ```
  # Phase 1: pre-position both lanterns
  ACTION6 @ click_grid=(2, 0)     # click top rail col 2 -> top-lantern slides to cols 0..4
  ACTION6 @ click_grid=(12, 15)   # click bot rail col 12 -> bot-lantern slides to cols 10..14
  ```
  2 actions. After both clicks: top@cols 0..4, bot@cols 10..14. A, B, C
  all simultaneously double-shaded (verified per the layout analysis
  above).

  ```
  # Phase 2: collect A
  ACTION4, ACTION1                # (1,13) -> (2,13) -> (2,12) — pickup A
  ```
  At avatar (2, 12), footprint (2..3, 12..13) overlaps crystal A at
  (col=2, row=11..12). Cell (2, 12) shadow check: top@cols 0..4 → col
  2 in range, top-pillar at col 2 rows 5..7 above row 12 → top-shaded.
  bot@cols 10..14 → col 2 outside → bot-shaded. Both shaded → pickup.
  **2 actions.**

  ```
  # Phase 3: collect C
  ACTION2,                         # (2,12) -> (2,13)
  ACTION4 ×5,                      # (2,13) -> (7,13)
  ACTION1 ×4                       # (7,13) -> (7,9)
  ```
  10 actions. Each step's avatar footprint is checked:
  - (3, 13)..(7, 13): footprint (c..c+1, 13..14); no pillars at row 13
    or 14 in any column → walkable.
  - (7, 12): footprint (7..8, 12..13); no pillars at col 7 or 8 at
    rows 12, 13 → walkable.
  - (7, 11): footprint (7..8, 11..12); no pillars in cols 7, 8 at
    rows 11, 12 → walkable.
  - (7, 10): footprint (7..8, 10..11); no pillars → walkable.
  - (7, 9): footprint (7..8, 9..10); no pillars → walkable.
  
  At (7, 9) avatar overlaps crystal C at (col=7, row=8..9). Cell (7,
  9) shadow check: top@cols 0..4 → col 7 outside → top-shaded.
  bot@cols 10..14 → col 7 outside → bot-shaded. Both shaded → pickup.
  **10 actions.**

  ```
  # Phase 4: collect B (re-routed around col-13 bot-pillar at rows 8..10)
  ACTION4 ×4,                      # (7,9) -> (11,9)
  ACTION1 ×5,                      # (11,9) -> (11,4)
  ACTION4 ×2                       # (11,4) -> (13,4)
  ```
  Each step's avatar footprint:
  - (8, 9): footprint (8..9, 9..10); col 8/9 no pillar at rows 9..10
    → walkable.
  - (9, 9): footprint (9..10, 9..10); col 10 has top-pillar at rows
    5..7 — does that block (10, 9..10)? No: pillar is at rows 5..7,
    not rows 9..10. Walkable.
  - (10, 9): footprint (10..11, 9..10); col 10 no pillar at rows 9
    or 10. Walkable.
  - (11, 9): footprint (11..12, 9..10); col 11/12 no pillar at rows
    9, 10. Walkable.
  - (11, 8): footprint (11..12, 8..9); col 13 has bot-pillar at rows
    8..10 but col 11/12 do not. Walkable.
  - (11, 7): footprint (11..12, 7..8); col 10 has top-pillar at rows
    5..7 but col 11/12 do not. Walkable.
  - (11, 6): footprint (11..12, 6..7); col 11/12 no pillar at rows
    6, 7. Walkable. (Col 10 pillar at rows 5..7 covers (10, 5..7) — not
    in footprint.)
  - (11, 5): footprint (11..12, 5..6); col 11/12 no pillar. Walkable.
  - (11, 4): footprint (11..12, 4..5); col 11/12 no pillar. Walkable.
  - (12, 4): footprint (12..13, 4..5); col 13 row 4..5 — bot-pillar
    is at rows 8..10, not rows 4..5 → walkable. Pickup attempt: avatar
    overlaps crystal B at (col=13, row=4..5) — cell (13, 4) and (13,
    5) overlap. Avatar's reference cell is (12, 4); shadow check at
    (12, 4): top@cols 0..4 → col 12 outside → top-shaded. bot@cols
    10..14 → col 12 in range, no pillar in col 12 → bot-LIT. Cell is
    lit by bot → no pickup. (The pickup attempt fires but fails the
    shadow check; avatar continues walking.)
  - (13, 4): footprint (13..14, 4..5); walkable. Pickup attempt:
    avatar overlaps B; cell (13, 4) shadow check: top@cols 0..4 → col
    13 outside → top-shaded. bot@cols 10..14 → col 13 in range,
    bot-pillar at col 13 rows 8..10. Bot-rays from row 15 going up
    encounter the pillar at row 10; cells above row 10 (i.e., rows
    0..7) are bot-shaded by the pillar. Row 4 is in 0..7 → bot-shaded.
    Both shaded → **pickup B**. ✓

  **11 actions for phase 4.**

  **Total L3 witness: 2 + 2 + 10 + 11 = 25 actions.** Step budget 120
  leaves 95 spare.

- **Difficulty justification:**
  - *(a) Random-resistance:* The action space at L3 is `[1,2,3,4,6]`
    with ACTION6 having 2 valid rails × 12 valid columns = 24 distinct
    valid clicks per step, plus 4 walks → ~28 valid actions per step.
    A 25-action witness with both rails clicked at specific columns
    has random-policy probability ≪ 1/10⁴. Vision-blind agents cannot
    infer the dual-shadow rule from text.
  - *(b) Human-tractable:* An attentive human takes ~3 minutes:
    ~30 seconds to recognise pattern, ~60 seconds to discover the
    intersection rule (walk onto C with one lantern slid, observe
    no-op, slide the other lantern), ~90 seconds to plan and execute
    the dual-slide config and the route. Total environment time across
    L1+L2+L3 ≈ 6.5 min, hitting the ~6 min target.
  - *(c) Planning depth (post-discovery, challenging):*
    - **Decision space at level start (post-discovery):**
      4 walk directions × walking distances + 12 columns × 2 rails for
      ACTION6 = 28 distinct meaningful first-actions.
    - **Trivial heuristic that fails (greedy / monotone-progress):**
      the greedy-toward-target player picks "move toward the nearest
      crystal" first. Nearest by Manhattan distance from (1, 13) is A
      at (2, 12) (distance 2). Greedy-walking to A: ACTION4, ACTION1
      → A picked up. Now the greedy player wants to walk to the next
      nearest crystal, B at (13, 5) (distance from (2, 12) is ~22) or
      C at (7, 9) (distance ~9). Greedy picks C. Walks to C: but C
      is unsafe (default lanterns). Walking onto C is no-op → greedy
      heuristic stalls.
    - **Where the heuristic diverges from the witness:** at action 3.
      The witness slides lanterns BEFORE walking to C. The greedy
      heuristic walks toward C without the slide and discovers the
      cell is unsafe. The greedy player would then need to back-track
      and slide both lanterns (~2 extra clicks plus re-walking ~7
      cells back to the C-vicinity), wasting 16+ actions. Within step
      budget 120 the heuristic-then-correction approach still
      eventually wins, but at a much worse action-count → low RHAE
      score, which confirms the puzzle rewards planning.
    - **Why ahead-of-time reasoning is needed:** to find the SHORT
      witness, the player must see (post-discovery of M3): "C at col 7
      requires both lanterns off col 7. Sliding one lantern is
      necessary but not sufficient. The pre-position-both-lanterns
      config is also compatible with picking up A (col 2 has pillar
      → still top-shaded under top@cols 0..4) and B (col 13 has
      bot-pillar → still bot-shaded under bot@cols 10..14). This is a
      multi-constraint satisfaction step requiring the player to
      check three crystal cells against two lantern positions
      simultaneously."
  - *(d) Step budget:* 120 actions over a 25-action witness gives
    4.8× headroom. The budget does not shrink relative to L2's witness
    ÷ L2 budget ratio (L2: 26 / 70 ≈ 0.37; L3: 25 / 120 ≈ 0.21), so
    the L3 budget gives MORE relative room — consistent with
    `difficulty-rules.md` § d's L3 addendum (budget should not shrink
    as level number rises, since later levels add discovery cost).

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 6]`. ACTION5 and ACTION7 unused (and
not in the available list, so the agent never sees them as options).

| Slot | Verb |
|---|---|
| ACTION1 | Avatar moves up (row -= 1) if walkable. |
| ACTION2 | Avatar moves down (row += 1) if walkable. |
| ACTION3 | Avatar moves left (col -= 1) if walkable. |
| ACTION4 | Avatar moves right (col += 1) if walkable. |
| ACTION6 | Click at `(x, y)` (display pixels) → grid `(gx, gy)`. If `gy == 0`, slide top-lantern so it spans `[max(0, min(11, gx-2)) .. that+4]`. If `gy == 15` and bot-lantern is active (L3 only), slide bot-lantern similarly. Other clicks are no-ops. |

Walkability rules:
- Avatar can occupy any cell `(c, r)` with `0 ≤ c ≤ 14` (since avatar
  is 2×2, it occupies cols `c..c+1`) and `1 ≤ r ≤ 13` (rows 0 and 15
  are rails; row 14 is the bottom-most walkable since avatar height
  is 2).
- A cell is blocked if any pillar pixel intersects the avatar's
  destination 2×2 footprint.

Avatar walking onto a crystal:
- Compute the avatar's 2×2 footprint after move.
- If any cell of the footprint overlaps a crystal sprite's bounding
  box AND the cell at the avatar's top-left position is in shadow
  w.r.t. all active lanterns, fire pickup: set the crystal's
  interaction to REMOVED, decrement `crystals_remaining`.
- If the cell is lit by any active lantern: no-op (avatar still moves
  onto the cell, but the crystal is not picked up).

## 6. HUD and per-game state

**HUD widgets:**
- `StepCounterHud(RenderableUserDisplay)`: paints frame[63, :] —
  proportional bar of palette 12 (orange) for steps remaining and
  palette 4 (off-black) for steps consumed.

**Per-game state (per level):**
- `top_lantern_x_left: int` — leftmost column covered by the top
  lantern. Defaults vary per level (see §4).
- `bot_lantern_x_left: int | None` — leftmost column for bot lantern;
  `None` when the level has no bot lantern (L1, L2).
- `has_bot_lantern: bool` — set in `on_set_level`.
- `lit_top: set[tuple[int, int]]` — cells lit by top-lantern,
  recomputed each step.
- `lit_bot: set[tuple[int, int]]` — cells lit by bot-lantern (empty
  set at L1/L2).
- `crystals_remaining: int` — count of un-collected crystals.
- `step_counter: int` — actions remaining this level.

**Hidden state vector** (`_get_hidden_state`): a 4×4 int16 array with
`[0,0] = step_counter`, `[0,1] = top_lantern_x_left`, `[0,2] =
bot_lantern_x_left or -1`, `[0,3] = crystals_remaining`. Lets the
engine's graph-identity hashing distinguish states with the same
pixel rendering but different internal config (e.g., two cells
visited in different orders).

## 7. Win condition

`crystals_remaining == 0` at the end of `step()` → call
`self.next_level()`. Concrete predicate: after every action, check
`level.get_sprites_by_tag("crystal")` filtered to those with
`interaction == InteractionMode.TANGIBLE`; if empty, win.

## 8. Lose condition

`step_counter <= 0` after decrement → call `self.lose()`. There is no
other lose condition — walking onto a lit crystal is a no-op (forgiving
rule), so a player can never make a level structurally unwinnable
through bad walking.

## 9. Novelty note

(Re-grounded against `mechanic-novelty/`; mirrors `mechanic-pick.md`
and re-validates after the spec is fully fleshed out.)

### Closest reference: lq5x (prior) — `lantern-cone-illuminate`

- **Geometry inversion.** lq5x's safe zone is the *interior* of a
  player-carried directional cone. vp6h's safe zone is the
  *occlusion* — the shadow cast by an obstacle, away from a
  stationary edge-mounted lantern.
- **Light field topology.** lq5x: 3-wide directional wedge that
  rotates around the avatar via ACTION5. vp6h: parallel-ray field
  emitted from a 5-cell-wide rail-mounted bar; no rotation, no
  cone.
- **Lantern locus.** lq5x: avatar-carried (cone apex follows
  avatar). vp6h: stationary on a 1D edge rail; repositioned by
  ACTION6 click on the rail. Avatar and lantern are decoupled.
- **Win condition.** lq5x: tinting target rings with cone-colour
  (match-by-tint). vp6h: collect every crystal sprite (collect-all,
  no colour-tinting).
- **L3 mechanic.** lq5x L3 modifies the single-cone (wax extends
  range, filters re-tint). vp6h L3 introduces a SECOND lantern and
  the dual-shadow intersection rule — a compositional change in the
  safety-rule itself, not a per-cone modification.

After fleshing out the spec, the negative-similarity walk against
lq5x's `level_1.png` confirms the visual signature divergence:
lq5x's L1 is mostly dark with bright sparse elements; vp6h's L1
will render mostly bright (lit cells = palette 1 off-white) with a
single vertical dark strip in column 7 (where the pillar's shadow
falls). Inverse visual signature.

### Other near-misses (already disposed in `mechanic-pick.md`):

- **bx84 (prior, beam-mirror-reflect).** Single beam routed via
  clickable mirrors vs vp6h's parallel rays + occlusion + no
  mirrors.
- **lf52 (reference, fog-of-war-sokoban).** Avatar-centric fog of
  war + sokoban push vs vp6h's lantern-driven shadow + no push.
- **kn58 (prior, anchor-pull-magnet).** Click-to-place anchor +
  pawn slide vs vp6h's click-to-slide-lantern + no pawn movement
  beyond the avatar's own walk.
- **gv47 (prior, seed-grow-surround-dissolve).** Region growing
  via seed click vs vp6h's geometric occlusion field.
- **fz5j (prior, phase-step-tile).** Auto-pulsing tile schedule vs
  vp6h's player-controlled lantern position; no per-cell schedule.

### Negative-similarity-check (per `negative-similarity-check.md`)

Walked at pick-time against lq5x level_1.png. Sharing dimensions:
- (1) On-board cast — both have lantern + avatar + walls + collectibles. Shared.
- (4) Loss — both step-counter. Shared (universal).
- (5) Supporting elements — universal (walls + targets). Shared.

Diverging dimensions:
- (2) Verb — lq5x: walk + ACTION5-rotate-cone; vp6h: walk + ACTION6-click-rail. Different.
- (3) Goal — lq5x: cone-tinting; vp6h: collect-all. Different.
- (6) Visual signature — lq5x: dark-mostly with bright cone; vp6h: light-mostly with vertical dark strips. Inverted.
- (7) Pixel grain — vp6h's crystals are 2×2 with internal `10/14` pattern; avatar 2×2 with `6/13` checker. lq5x's L1 sprites are uniform-colored frames.
- (8) Core dynamic — opposite (light=hostile vs light=safe).

Three shared dimensions (1, 4, 5) — at threshold but all on the
"universal-ish" side. Heavy axes (6, 7, 8) diverge cleanly. **Verdict:
NOVEL.**
