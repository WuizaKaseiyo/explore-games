# Game `kj82` — full spec (revision 2)

This revision addresses the two issues raised in
`workspace/critique-revisions.md`:

- **Issue 1 (chevron-as-arrow)** is fixed in §3 (new symmetric
  `spring` sprite design) and §4 (M4 redefined so direction
  inherits from the underlying plank's orientation, not from
  the spring sprite's pixel pattern).
- **Issue 2 (low-resolution grid)** is fixed by bumping every
  level's grid_size to 32×32 (camera scale = 64/32 = 2 — every
  grid cell renders as 2×2 display pixels) and making planks
  2 cells thick × N cells long. All coords and witness
  sequences in §4 are updated to the rescaled layout.

## 1. Title

**Plank-Pivot Crossing** (working title; not visible in-game).

## 2. Mechanic family

`plank-pivot-walk` — a path-walking puzzle on a plane of long
**plank** sprites pinned at one end by a fixed **anchor**. The
player has a tiny pawn avatar that walks one cell per arrow-press
on plank cells only, and an active-plank verb that pivots the
selected plank 90° clockwise around its anchor end (sweeping the
plank's tip across a quarter-arc of cells); a pawn standing on a
non-anchor cell of the active plank rides the plank to the new
cell that maintains its offset-from-anchor in the new orientation.

**Core-knowledge priors used:** objectness (plank as rigid body,
pawn as persistent agent, post and spring as objects); basic
geometry and topology (rotation around fixed pivot point,
quarter-arc geometry, plank-cell connectivity for walking); basic
physics (anchor-constrained rotation, post-blocked rotation,
spring-launch-along-plank-axis).

## 3. Sprite roster

(Tag legend: `sys_click` is the engine's "this sprite responds
to clicks" tag — same convention the 25 reference games use.)

| Name | Pixel matrix dims (cells) | Palette values | Tags | Role |
|---|---|---|---|---|
| `plank_l8` | 2×8 | `12` orange (top row), `13` maroon (bottom row), with the leftmost 2×2 cells being palette `5` outer ring + palette `11` yellow pip (the anchor fixture baked into the plank sprite) | `sys_click`, `plank` | A length-8 horizontal plank with the anchor fixture at the leftmost 2×2 region. Internal pattern (orange/maroon stripes) reads as a wood plank at scale 2. Cloned for L1 and L3's `plank_delta`. |
| `plank_l13` | 2×13 | same palette pattern as `plank_l8`, anchor at leftmost 2×2 | `sys_click`, `plank` | Length-13 plank. Cloned for L2's `plank_alpha` & `plank_beta` and L3's `plank_gamma`. |
| `pawn` | 3×3 | `8` red ring + `0` white pip in centre + `5` black eye dots at corners | `pawn` | The player avatar. One per game. At scale 2 renders as a 6×6-pixel character. |
| `goal_tile` | 4×4 | `6` magenta on the outer 12 cells (ring), `0` white pip in the centre 2×2, `5` black 1-pixel accent | `goal` | Destination cell. One per level. Renders as 8×8 pixels at scale 2 — clear ring with internal pip. |
| `post_blocking` | 3×3 | `4` dark-grey solid centre (3×3 of `4`), with `5` black 1-cell ring around the perimeter | `sys_click`, `post`, `post_blocking` | A solid post — blocks plank rotations whose arc would sweep through any of its 9 cells. Pawn cannot walk onto a `post_blocking` cell (decorative obstacle). |
| `post_permeable` | 3×3 | `4` dark-grey ring outline only (perimeter), `0` white interior — visible "hollow" version of the post | `sys_click`, `post`, `post_permeable` | The toggled-open form. Plank rotations may pass through any of its cells. Pawn still cannot walk onto a `post_permeable` cell (post is decorative-obstacle to the avatar regardless of state). |
| `spring` | 3×3 | symmetric: `14` green ring on the outer 8 cells of a 3×3, `0` white pip at the centre, `5` black 1-pixel accents at the 4 corners. **No directional bias** — the visual is symmetric under all 4 rotations. | `spring` | A pawn-launcher pad. When the pawn ends a turn ON a spring's centre cell, the spring fires automatically: pawn is translated 5 cells **in the direction the underlying plank extends from its anchor** (i.e., the spring inherits its launch direction from the orientation of the plank it currently sits on). Launch teleports the pawn across intermediate cells; the destination must be a plank cell or the goal cell or the launch is rejected (pawn stays on spring). The spring is anchored to a specific plank at level construction; it moves with that plank during rotations (a child sprite). |
| `anchor_halo` | 3×3 | `14` green ring (8 outer cells), `-1` transparent interior | `halo` | A separate overlay sprite positioned ON TOP of the active plank's anchor cell (the leftmost 2×2 of the plank's east orientation, but the halo is 3×3 to extend slightly beyond the plank's bounds — visually unambiguous). `InteractionMode.INTANGIBLE` so it doesn't block collision. When no plank is active, `InteractionMode.REMOVED`. The halo signals which plank is currently selected for ACTION5. |

Step counter HUD (a `RenderableUserDisplay` subclass) is declared
in §6 — not in the sprite dict.

**Style note:** all sprite names, tags, helper-class names,
helper-method names, and module-level constants use meaningful
semantic English. The ID `kj82` is opaque per §3.4; semantic
names elsewhere are appropriate because the game is a prototype.

**Visual signature:** background = palette 10 (light-blue);
letter-box = palette 1 (off-white). Active palette values used
in the playfield: `1, 4, 5, 8, 10, 11, 12, 13, 14, 6` (10 distinct
values, including background/letter-box). Diverges from the
grey-dominant signature of recent priors (jd4q, ek73, vd3g, lv4k,
kp9z).

## 4. Level progression, mechanic enumeration, and witness solutions

Mechanic key (definitions used uniformly across the three levels;
"plank cells" means the full 2-cells-thick × N-cells-long set
covered by the plank's current orientation):

- **M1 — pawn-walk-on-plank.** ACTION1/2/3/4 step the pawn one
  cell up/down/left/right. The step is rejected (no-op, action
  consumed) if the destination cell is not part of any plank's
  current cell-set.
- **M2 — select-and-pivot-with-carry.** ACTION6 on a plank cell
  sets that plank as the active plank (visualised by repositioning
  `anchor_halo` over its anchor cell). ACTION5 with an active
  plank rotates that plank 90° clockwise around its anchor — east
  → south → west → north → east. The plank's body cells recompute
  accordingly, and any child `spring` sprite attached to that
  plank moves with it. **Pivot-carry**: if the pawn was on a
  non-anchor cell of the active plank at the moment of pivot,
  the pawn moves to the cell at the same offset-from-anchor in
  the new orientation (90° CW transformation: offset (dx, dy) →
  (-dy, dx)). If the pawn was on the anchor 2×2 region, the pawn
  stays put. ACTION5 with no active plank, with the rotation
  blocked by a post (M3), or with the rotation taking any plank
  cell off-grid, is a consumed no-op.
- **M3 — post-toggle-controls-rotation.** ACTION6 on a `post_*`
  cell toggles the post between `post_blocking` and
  `post_permeable` (swaps the `InteractionMode` of the two
  co-positioned twin sprites). A plank's pivot is **blocked**
  when any cell its body would occupy after the rotation
  coincides with any cell of a `post_blocking`. Once toggled to
  `post_permeable`, the same cell no longer blocks rotations.
- **M4 — spring-launch-along-plank-axis.** When the pawn ends a
  turn (after the action's `complete_action()` resolves) on a
  `spring`'s centre cell, the spring fires automatically: the
  pawn is translated 5 cells in the direction the spring's
  underlying plank extends from its anchor. (E.g., if the plank
  is in east orientation, spring fires east; if south, fires
  south; etc.) The launch is a **teleport**, ignoring intermediate
  cells, but is rejected if any `post_blocking` lies along the
  intermediate cells (a `post_permeable` along the path does
  NOT block) or if the destination is not a plank cell or goal
  cell — in which case the pawn stays on the spring. Spring
  firing does NOT consume an additional action; it resolves at
  the end of the triggering action's step.

### Level 1 — base dynamic system

**Grid size:** 32×32. **Camera scale:** 2 (= 64/32). **Step budget:** 30.

**Sprite layout:**
- `plank_main` = `plank_l8` clone, anchor at (10, 10), oriented
  east. Plank cells (the full 2-cells-thick set):
  (10,10), (11,10), (12,10), (13,10), (14,10), (15,10), (16,10), (17,10),
  (10,11), (11,11), (12,11), (13,11), (14,11), (15,11), (16,11), (17,11).
  (16 cells total — a 2-thick × 8-long plank.)
- `pawn` at (13, 10) — non-anchor cell of `plank_main` (offset
  (3, 0) east of the anchor's top-left cell).
- `goal_tile` at (10, 17).
- `anchor_halo`: REMOVED at level start (no plank active).

No posts, no springs. Background = palette 10; letter-box = palette 1.

**Mechanics required by the witness (N = 2):**

- **M1** (pawn-walk-on-plank).
- **M2** (select-and-pivot-with-carry).

**Necessity per mechanic** (per checklist item 12):

- **M1.** *L1 cannot be solved without M1 because, after the
  only useful pivot of `plank_main` (south, by 1 ACTION5), the
  pawn ends up at (10, 13) — pivot-carry of offset (3, 0) east →
  offset (-0, 3) = (0, 3) south. The goal at (10, 17) is 4 cells
  further south on the plank's south body; only ACTION1-4
  advance the pawn's grid position, and (10, 17) is reachable by
  walking on plank cells (which are now (10,10)..(10,17) plus
  (11,10)..(11,17)).*
- **M2.** *L1 cannot be solved without M2 because `plank_main`
  initially extends east-only (rows 10-11 from x=10 to x=17);
  the goal cell (10, 17) is not a plank cell of any reachable
  configuration without rotating the plank. Furthermore the pawn
  begins at non-anchor cell (13, 10); without pivot-carry the
  pawn would end up at (13, 10) after the rotation — a cell that
  is no longer a plank cell after the rotation — leaving the
  pawn stranded off-plank with no walkable path to the goal.*

**Verification by enumeration of plausible alternates (per item 12):**

- *Alternate strategy A: walk east without pivoting.* From (13, 10)
  the pawn can step east to (14, 10), (15, 10), (16, 10), (17, 10),
  then is blocked at (18, 10) (not a plank cell). Cannot reach
  (10, 17). **FAILS.**
- *Alternate strategy B: skip the click-select, just press
  ACTION5.* No plank active at level start; ACTION5 is a consumed
  no-op. **FAILS.**
- *Alternate strategy C: rotate multiple times to a non-south
  orientation.* Plank rotations cycle east → south → west → north.
  Each requires a separate ACTION5. South 1×: cells include
  (10,17). West 2×: cells (10,10)..(3,10) on-grid (x≥0), pawn
  carried to offset (-3, -0) = (-3, 0) which is off-grid.
  Actually more carefully: after 2× CW from east, offset (3, 0)
  → (-3, 0) → (-3, -0) = (-3, 0). The pawn would be at (10-3,
  10) = (7, 10). On-grid. But goal (10, 17) is not a plank cell
  of west-orientation. **FAILS.** Similarly north (3× CW): pawn
  at (10, 7), goal not on plank. **FAILS.**
- *Alternate strategy D: click goal cell directly.* No clickable
  sprite at (10, 17) → no-op. **FAILS.**

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 (walk) | no | After pivot deposits pawn at (10, 13) and goal is at (10, 17); only ACTION1-4 advance the pawn's grid position — 4 walking steps required. |
| L1 | M2 (pivot+carry) | no | Goal (10, 17) is not a member of `plank_main`'s east-orientation cell set; only after pivoting south does any plank cell cover (10, 17). And without pivot-carry the pawn at (13, 10) ends up off-plank after rotation. |

**Witness solution (6 actions):**

`[ACTION6@(13, 10), ACTION5, ACTION2, ACTION2, ACTION2, ACTION2]`

(ACTION6 click coords are display-pixel coords. With camera
scale 2 and the camera centred on the 32×32 grid, the
display-to-grid translation maps display (26, 20) ≈ grid (13, 10).
For spec purposes I list grid coords; the implementation converts
via `camera.display_to_grid`.)

Step-by-step:
1. ACTION6 at (13, 10) → `plank_main` becomes active;
   `anchor_halo` moves to (10, 10).
2. ACTION5 → `plank_main` pivots 90° CW. New cells (south):
   x=10 column rows 10-17, plus x=11 column rows 10-17 (the
   thickness extends one cell east of the anchor column after
   south rotation). Wait, let me re-derive. Plank east cells:
   (10..17, 10) ∪ (10..17, 11). After 90° CW around anchor cell
   (10, 10): each cell (10+i, 10+j) → (10 + (-j), 10 + i). So
   (10+0, 10+0) → (10, 10) [anchor stays]. (10+7, 10+0) →
   (10, 17) [east tip → south tip]. (10+0, 10+1) → (9, 10)
   [bottom-row of anchor → west-of-anchor]. (10+7, 10+1) →
   (9, 17) [bottom-east-tip → south tip's west-side neighbour].
   So the south plank covers cells (10, 10)..(10, 17) AND
   (9, 10)..(9, 17) — 16 cells total, a 2-thick south plank
   that extends one column WEST of the anchor (column x=9).
   Pawn was at (13, 10) = offset (3, 0) east; after CW, offset
   (0, 3) south → cell (10, 13).
3. ACTION2 → pawn (10, 13) → (10, 14).
4. ACTION2 → (10, 14) → (10, 15).
5. ACTION2 → (10, 15) → (10, 16).
6. ACTION2 → (10, 16) → (10, 17). Pawn on `goal_tile`;
   `next_level()` fires.

**Difficulty justification (per `difficulty-rules.md` § 2):**

- **(a) Random-resistance.** A vision-blind / random-policy agent
  must specifically click somewhere on the plank (which occupies
  16 of 1024 grid cells, ~1.6% click hit rate), then ACTION5,
  then ACTION2 four times. Combined random-policy 6-step win
  probability is well under 0.001%. No spam-one-verb wins:
  spamming ACTION1-4 stays on the east-oriented plank without
  ever reaching (10, 17); spamming ACTION5 with no active plank
  is a no-op; spamming ACTION6 randomly rarely clicks plank
  cells.
- **(b) Human-tractable.** A human reading the screen sees a tiny
  red pawn standing on an orange-and-maroon plank with a yellow-
  pip anchor at its left end, and a magenta-ringed goal tile
  diagonally below-left. Estimated time: **~90 seconds**
  including discovery (try walking → fails to reach goal; try
  clicking the plank then pressing ACTION5 → discovers rotation;
  walks to goal).
- **(c) Planning depth.** **No strict planning required.** L1 is
  the discovery gate; once "click plank + ACTION5 rotates + pawn
  rides" is understood, the win is one rotation + four walk steps
  away.
- **(d) Step budget.** **30** actions. Witness length 6;
  budget = 5× witness, generous over the witness for exploration.

### Level 2 — base system + 1 new mechanic

**Grid size:** 32×32. **Step budget:** 50.

**Sprite layout:**
- `plank_alpha` = `plank_l13` clone, anchor at (4, 6), oriented
  east. Cells:
  (4,6)..(16,6) (top row, 13 cells) + (4,7)..(16,7) (bottom row).
  Total 26 cells (2 thick × 13 long).
- `plank_beta` = `plank_l13` clone, anchor at (4, 18), oriented
  east. Cells: (4,18)..(16,18) + (4,19)..(16,19). Total 26 cells.
- `pawn` at (8, 6) — offset (4, 0) east of `plank_alpha`'s anchor.
- `goal_tile` at (16, 18) — east tip of `plank_beta`.
- `post_blocking` at (4, 12) (centre cell). The post sprite is 3×3
  cells, so it covers cells (3,11)..(5,13). The cell (4, 12)
  specifically lies along `plank_alpha`'s south arc (south body
  would cover x=4 column rows 6-18 plus x=3 column rows 6-18; the
  post's 9-cell footprint at (3-5, 11-13) overlaps both.
- `post_permeable` at (4, 12) co-positioned, REMOVED initially.
- `anchor_halo`: REMOVED at level start.

**Mechanics required by the witness (N+1 = 3):**

- **M1** (pawn-walk-on-plank). Carried forward from L1.
- **M2** (select-and-pivot-with-carry). Carried forward from L1.
- **M3** (post-toggle-controls-rotation). Newly introduced at L2.

(L2 introduces 1 new mechanic.)

**Necessity per mechanic** (per checklist item 12):

- **M1.** *L2 cannot be solved without M1 because the witness
  must walk the pawn (a) south from (4, 10) — where pivot-carry
  drops it after `plank_alpha`'s south rotation — to (4, 18)
  where `plank_beta`'s anchor sits (8 ACTION2 steps), and (b)
  east from (4, 18) to the goal at (16, 18) along `plank_beta`'s
  east body (12 ACTION4 steps). No pivot can take the pawn
  directly to (16, 18); only walking can.*
- **M2.** *L2 cannot be solved without M2 because `plank_alpha`'s
  east-orientation cells are at y∈{6, 7} and `plank_beta`'s
  east-orientation cells are at y∈{18, 19} — the two planks share
  no cell in their initial configuration. Only after pivoting
  `plank_alpha` 90° CW (south) do its body cells include
  (4, 18) and (3, 18), the cells where `plank_beta`'s anchor
  region overlaps — providing the bridge.* Pivot-carry is also
  strictly necessary: pawn at (8, 6) (offset (4, 0)) ends up at
  offset (0, 4) south = (4, 10) after rotation; if pawn-carry
  didn't happen, the pawn at (8, 6) would not be on any plank
  cell after rotation (since (8, 6) is no longer a plank cell
  post-pivot).
- **M3.** *L2 cannot be solved without M3 because the post's
  9-cell footprint at (3-5, 11-13) intersects `plank_alpha`'s
  south arc (south body covers x=4 column from y=6 to y=18 plus
  x=3 column same range; the post at (4, 12) and (3, 12) is in
  both columns). The pivot is rejected (any plank cell
  coinciding with a `post_blocking` cell vetoes the rotation).
  Without toggling the post to `post_permeable` first, the
  pivot cannot succeed; `plank_alpha` is permanently stuck at
  east; the bridge to `plank_beta` cannot form.*

**Verification by enumeration of plausible alternates (per item 12):**

- *Alternate strategy A: ignore the post; click `plank_alpha`,
  ACTION5.* Rotation rejected (post at (4, 12) is in the
  south-arc cell-set). Plank stays east. **FAILS.**
- *Alternate strategy B: spam ACTION5 hoping to bypass the
  blocked rotation.* Each rotation attempt fails for the same
  reason — the south rotation always tries the same arc. ACTION5
  always rotates by 90° CW from current orientation; if blocked,
  the plank stays in the current orientation. The plank is
  permanently stuck at east unless the post is toggled.
  **FAILS.**
- *Alternate strategy C: walk along `plank_alpha` east edge
  without rotating.* From (8, 6) the pawn can step east to (16, 6)
  along plank_alpha's east cells, then stuck (no plank cell at
  (17, 6) or (16, 5) or (16, 8)). Cannot reach `plank_beta`.
  **FAILS.**
- *Alternate strategy D: click `plank_beta` first.* `plank_beta`
  east → south rotation: cells (4-5, 18)..(4-5, 30). On-grid
  (max y=30 < 32). Pawn isn't on `plank_beta` — clicking it just
  selects it without moving the pawn. After plank_beta south
  rotation, pawn at (8, 6) still at (8, 6) (not on plank_beta) —
  still on `plank_alpha`'s east body. Doesn't help bridge.
  **FAILS.**
- *Alternate strategy E: rotate `plank_alpha` to other
  directions hoping to bypass post.* East → west requires going
  through south first (each ACTION5 = +90° CW). South is blocked.
  Cannot reach west. **FAILS.**

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L2 | M1 (walk) | no | After pivot-carry deposits pawn at (4, 10), pawn must walk to (4, 18) (8 cells south) and then to (16, 18) (12 cells east); only ACTION1-4 advance grid position. |
| L2 | M2 (pivot+carry) | no | Plank_alpha east-body and plank_beta east-body share no cells; only south pivot creates the bridge cells (4, 18) and (3, 18). Pawn at (8, 6) ends off-plank without pivot-carry. |
| L2 | M3 (post-toggle) | no | Post_blocking footprint at (3-5, 11-13) is in plank_alpha's south arc; pivot is rejected unless toggled to permeable first. |

**Witness solution (22 actions):**

`[ACTION6@(4, 12), ACTION6@(8, 6), ACTION5, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]`

Step-by-step:
1. ACTION6 at (4, 12) → `post_blocking` ↔ `post_permeable` swap.
2. ACTION6 at (8, 6) → `plank_alpha` active; halo at (4, 6).
3. ACTION5 → plank_alpha pivots south. Cells: x=4 column rows
   6-18 + x=3 column rows 6-18 (26 cells). Pawn rides from
   (8, 6) (offset (4, 0)) to (4, 10) (offset (0, 4)).
4-11. ACTION2 ×8 → pawn walks south from (4, 10) to (4, 18).
12-23. ACTION4 ×12 → pawn walks east from (4, 18) to (16, 18)
   on `plank_beta`. Goal reached; `next_level()` fires.

**Difficulty justification:**

- **(a) Random-resistance.** Random-policy agent must (1) click
  on the post (9 of 1024 cells = 0.88%), (2) click on plank_alpha
  (26 of 1024 = 2.5%), (3) ACTION5, (4) walk a specific 20-step
  pattern. Total probability under 10⁻⁹ for the action
  sequence; under 10⁻¹⁵ when click-target precision is included.
- **(b) Human-tractable.** ~2 minutes including discovery loop
  (try plank-pivot, fails; click post; try again, succeeds).
  The post's solid-square sprite invites a click; the wood-plank
  visual reads as "object that maybe rotates around its anchor";
  the magenta goal ring is the destination cue.
- **(c) Planning depth (post-discovery).** Moderate.

  **Decision space at level start (post-discovery):** distinct
  useful first actions —
  (a) ACTION6 on post_blocking (3-5, 11-13),
  (b) ACTION6 on plank_alpha (any of 26 cells → all equivalent
      = 1 distinct action),
  (c) ACTION6 on plank_beta (any of 26 cells = 1 distinct),
  (d) ACTION4 (walk east from (8, 6) to (9, 6) — only walking
      direction that lands on a plank cell).
  ACTION5 is no-op (no active plank). ACTION1/2/3 try to leave
  the plank, all rejected.
  Total post-discovery first-action useful choices: **4**. Per
  checklist item 18 (d) L2: "If < 2, the level is a 1-action-
  lookup-table by definition → reject." 4 ≥ 2 ✓.

  **Plausible-but-wrong alternative the post-discovery player
  considers:** click `plank_alpha` first, then ACTION5 (the
  "more direct" sequence, fewer clicks). The pivot fails because
  the post is still blocking. The plank doesn't move; the player
  must then click the post and re-pivot. The witness avoids this
  one wasted action by clicking the post first.

  **Witness reasoning chain (post-discovery):**
  - Step 1's reason: I see the dark post in the path of
    plank_alpha's south arc; pivoting before toggling costs an
    extra action (a failed pivot) — toggle first.
  - Step 2's reason: select plank_alpha to make ACTION5 target
    it.
  - Step 3's reason: south is the only useful rotation direction
    (east is the current orientation; west and north don't bridge
    to plank_beta).
  - Steps 4-11: walk south to bridge cell.
  - Steps 12-23: walk east on plank_beta to goal.
- **(d) Step budget.** **50** actions. Witness length 22; budget
  ≈ 2.3× witness, generous over the witness for the discovery
  loop. Generous over witness, never tight.

### Level 3 — system + 1 new mechanic

**Grid size:** 32×32. **Step budget:** 60.

**Sprite layout:**
- `plank_gamma` = `plank_l13` clone, anchor at (4, 8), oriented
  east. Cells: x=4..16, y=8..9 (26 cells).
- `plank_delta` = `plank_l8` clone, anchor at (4, 20), oriented
  east. Cells: x=4..11, y=20..21 (16 cells).
- `pawn` at (8, 8) — offset (4, 0) east of `plank_gamma`'s anchor.
- `post_blocking` at (4, 14) (centre cell; 3×3 footprint
  (3-5, 13-15)). Initial TANGIBLE; lies in `plank_gamma`'s
  south-arc body.
- `post_permeable` at (4, 14) co-positioned; REMOVED initially.
- `spring` at (11, 20) — east tip of `plank_delta` (the spring is
  registered as a child of `plank_delta` and follows its
  rotations). 3×3 sprite centred on (11, 20) (footprint
  (10-12, 19-21)).
- `goal_tile` at (16, 20) — 5 cells east of the spring's centre
  cell, the spring's launch destination when plank_delta is in
  east orientation.
- `anchor_halo`: REMOVED at level start.

**Mechanics required by the witness (L2-count + 1 = 4):**

- **M1, M2, M3.** All carried forward from L2.
- **M4** (spring-launch-along-plank-axis). Newly introduced.

(L3 introduces 1 new mechanic.)

**Necessity per mechanic** (per checklist item 12):

- **M1.** *L3 cannot be solved without M1 because the witness
  must walk the pawn south from (4, 12) (post-pivot landing) to
  (4, 20) (8 cells), and east from (4, 20) to (11, 20) (7 cells)
  to reach the spring. ACTION1-4 are the only way to advance the
  pawn cell-by-cell.*
- **M2.** *L3 cannot be solved without M2 because plank_gamma's
  east-body and plank_delta's east-body share no cells; only
  pivoting plank_gamma south creates the bridge cell at (4, 20)
  (and (3, 20)) where plank_delta's anchor region sits.
  Pivot-carry is required to keep the off-anchor pawn on a
  plank cell post-rotation.*
- **M3.** *L3 cannot be solved without M3 because the post at
  (4, 14) (footprint (3-5, 13-15)) is in plank_gamma's south
  arc; pivot rejected unless toggled to permeable.*
- **M4.** *L3 cannot be solved without M4 because the goal cell
  (16, 20) is not a member of any plank's reachable-cell set:
  - plank_gamma length 13 anchor (4, 8): east covers (4-16, 8-9);
    south covers (3-4, 8-20); west and north both go off-grid.
    None of these cover (16, 20).
  - plank_delta length 8 anchor (4, 20): east covers (4-11,
    20-21); south covers (3-4, 20-27); west goes off-grid (would
    extend to x=-3); north covers (3-4, 13-20). None of these
    cover (16, 20).
  So no walking path reaches (16, 20). The spring is the only
  mechanism that translates the pawn to (16, 20): when the pawn
  is on the spring at (11, 20) and plank_delta is in east
  orientation, the spring fires a 5-cell-east teleport to
  (16, 20).*

**Verification by enumeration of plausible alternates (per item 12):**

- *Alternate strategy A: skip the spring; walk to the goal.*
  As shown above, no plank cell covers (16, 20). Walking
  exclusively cannot reach it. **FAILS.**
- *Alternate strategy B: walk into the spring without first
  toggling the post.* To reach the spring at (11, 20) the pawn
  must be on plank_delta. To get on plank_delta, plank_gamma
  must pivot south. The pivot is blocked by the post. **FAILS.**
- *Alternate strategy C: rotate plank_delta to extend its
  reach east instead of using the spring.* No plank_delta
  rotation covers (16, 20) per the per-orientation enumeration
  above. **FAILS.**
- *Alternate strategy D: rotate plank_delta to change the
  spring's launch direction.* If plank_delta rotates south
  (1× CW), the spring (child sprite) moves to (4, 27) and the
  launch direction becomes south; launch from (4, 27) south 5
  cells = (4, 32), off-grid → rejected. If plank_delta rotates
  north (3× CW = 1× CCW; via 3 ACTION5s the player can reach
  north orientation by rotating east → south → west → north,
  but west is off-grid for plank_delta length 8 from anchor
  (4, 20): cells x=-3..4 — rejected at the west rotation
  attempt). So plank_delta cannot reach north via successive
  ACTION5s. The only achievable orientations for plank_delta
  are east and south. South sends the spring's launch off-grid
  → rejected. East sends to (16, 20) = goal — the witness
  configuration. **FAILS for any orientation other than east.**
  This actually CONFIRMS M4's necessity, not negates it: the
  spring at east is the ONLY combination that works, and it
  IS the spring mechanism doing the work.
- *Alternate strategy E: use plank_gamma's spring (no such
  spring exists at L3 — only plank_delta has one).* **N/A.**
- *Alternate strategy F: walk east on plank_gamma to its tip,
  pivot, then ride.* From (8, 8) walk east to (16, 8) (8 ACTION4
  steps). At (16, 8), click plank_gamma, ACTION5. South pivot:
  cells (4-3, 8-20). With pivot-carry, pawn at offset (12, 0) →
  offset (0, 12) south = (4, 20). Pawn lands on plank_delta's
  anchor. From (4, 20) walk east to (11, 20) (7 ACTION4 steps);
  at the spring, fire east; launch to (16, 20) = goal. **This
  works but is longer than the witness AND it still uses ALL
  of M1, M2, M3, M4.** Different witness, all four mechanics
  still required.

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L3 | M1 (walk) | no | Pawn must traverse plank_gamma south body (~8 cells) and plank_delta east body (~7 cells) to reach the spring. ACTION1-4 are the only walk verb. |
| L3 | M2 (pivot+carry) | no | Plank_gamma east and plank_delta east share no cells; only plank_gamma south pivot bridges. Pivot-carry needed for off-anchor pawn. |
| L3 | M3 (post-toggle) | no | Post at (3-5, 13-15) blocks plank_gamma's south rotation arc unless toggled. |
| L3 | M4 (spring) | no | Goal (16, 20) not on any plank. Spring east-launch from (11, 20) is the only path to (16, 20); per the enumeration, no other plank rotation reaches goal, and only east-orientation plank_delta + spring fires to goal. |

**Witness solution (18 actions):**

`[ACTION6@(4, 14), ACTION6@(8, 8), ACTION5, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]`

Step-by-step:
1. ACTION6 at (4, 14) → post_blocking ↔ post_permeable swap.
2. ACTION6 at (8, 8) → plank_gamma active; halo at (4, 8).
3. ACTION5 → plank_gamma pivots south. Cells: x=4 column y=8-20
   plus x=3 column y=8-20 (26 cells). Pawn rides from (8, 8)
   (offset (4, 0)) to (4, 12) (offset (0, 4)).
4-11. ACTION2 ×8 → pawn walks south from (4, 12) to (4, 20).
12-18. ACTION4 ×7 → pawn walks east from (4, 20) along
   plank_delta (east body) to (11, 20). The 18th action lands
   the pawn ON the spring's centre cell (11, 20). At end-of-turn,
   spring fires automatically: launch direction = east
   (plank_delta in east orientation), range 5 — pawn translates
   from (11, 20) east through (12-15, 20) (no posts in path) to
   (16, 20) = `goal_tile`. `next_level()` fires.

**Difficulty justification:**

- **(a) Random-resistance.** Random-policy agent must produce a
  ~17-action sequence with two specific ACTION6 click targets,
  one ACTION5 in the right position, and walk patterns. Total
  probability under 10⁻⁹. Plus the agent must visually
  distinguish the spring sprite from the post and goal — the
  spring's symmetric green ring is distinct from the dark-grey
  post and the magenta goal.
- **(b) Human-tractable.** ~2.5 minutes once L1 and L2 are
  understood. The new spring sprite invites stepping onto it
  to discover its launch behaviour. The chain "goal off-plank →
  must use spring → must reach plank_delta → must bridge from
  plank_gamma → must toggle post" is reasoned through in ~30 s
  of planning.
- **(c) Planning depth (post-discovery).** **Challenging even
  for an attentive human.**

  **Decision space at level start (post-discovery):** distinct
  useful first ACTION6 targets —
  (a) post_blocking footprint (3-5, 13-15),
  (b) plank_gamma (any of 26 cells = 1 distinct),
  (c) plank_delta (any of 16 cells = 1 distinct).
  Plus ACTION4 (walk east on plank_gamma).
  **Total 4 distinct useful first-actions** — equal to L2's
  count (4). Per checklist item 18 (d) L3: "count ≥ L2's, never
  smaller." 4 ≥ 4 ✓.

  **Trivial post-discovery heuristic that fails: greedy /
  monotone-progress toward goal.** Pawn at (8, 8); goal at
  (16, 20). A greedy strategy walks east+south whenever
  possible. From (8, 8): east is on-plank (plank_gamma east
  body); walk east. (8,8) → (9,8) → (10,8) → ... → (16,8)
  (8 ACTION4 steps). Now at plank_gamma's east tip; (17, 8) is
  not a plank cell. Try south? (16, 9) is plank cell (top-row
  of plank); step south. Try further south? (16, 10) is not a
  plank cell — blocked. Greedy gets stuck at (16, 9) with no
  way to make further monotone progress toward (16, 20). The
  pawn is stranded at the east tip; greedy cannot back-track
  and try a different mechanism. **Greedy walks to a
  dead-end at (16, 9).**

  **Where the heuristic diverges from the witness:** at
  step 1 the heuristic picks ACTION4 (walk east, monotone
  progress); the witness picks ACTION6 at the post (the
  WEST-of-pawn cell at (4, 14) — opposite direction from goal).
  The first 8 walk-east steps put the pawn at (16, 9); the
  witness's first 3 steps reconfigure plank_gamma's orientation
  so a non-monotone path through the south body of plank_gamma
  becomes available.

  **Why ahead-of-time reasoning is needed:** the player must
  reason backward from the goal — (a) goal is off-plank, only
  spring reaches it; (b) spring is on plank_delta's east tip,
  pawn must walk plank_delta to reach it; (c) plank_delta is
  separate from plank_gamma, requires bridge; (d) bridge
  requires plank_gamma south pivot; (e) south pivot requires
  post toggle. Five layers of "X requires Y first." Greedy
  toward goal-coord fails immediately; only a multi-step plan
  that starts west-of-pawn with a post-toggle wins.
- **(d) Step budget.** **60** actions. Witness length 18;
  budget = 3.3× witness. **Budget does not shrink relative to
  L2's 50.** Per the difficulty rule "L3: the budget must NOT
  shrink relative to the witness as level number rises" —
  60 ≥ 50 ✓.

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5, 6]`

| Action | Semantic | Gating |
|---|---|---|
| ACTION1 | Walk pawn 1 cell up. | Destination must be a plank cell. Otherwise no-op. |
| ACTION2 | Walk pawn 1 cell down. | Same. |
| ACTION3 | Walk pawn 1 cell left. | Same. |
| ACTION4 | Walk pawn 1 cell right. | Same. |
| ACTION5 | Pivot active plank 90° CW around its anchor, with pivot-carry. | Requires `_active_plank` set; rotation rejected if any new plank cell coincides with a `post_blocking` or goes off-grid. Action consumed regardless. Spring child sprites move with their plank. |
| ACTION6 | Click at display (x, y). Engine converts via `camera.display_to_grid(x, y)`. Hits exactly one tagged sprite at that grid cell (priority: post > plank > others). On a `post_*`: toggle blocking ↔ permeable. On a `plank` cell: set `_active_plank` to that plank, position `anchor_halo`. Click on `_active_plank`'s anchor: deselect (`_active_plank = None`, halo REMOVED). Off-target: no-op. | Always available. |

ACTION7 (undo) intentionally not declared (matches 19/25
reference games that don't use undo).

## 6. HUD and per-game state

**HUD:** `StepCounterHud` — a `RenderableUserDisplay` subclass
that renders a 32-cell-wide depleting bar at the bottom row of
the 64×64 frame. Filled palette = 11 (yellow), unfilled = 5
(black). Bar shrinks right-to-left as budget drains. Pattern
modeled on `cn04`'s `qdcvayjdkm`.

**Per-game state on the `Kj82` instance** (set/reset in
`on_set_level`):
- `self._active_plank: Sprite | None` — currently selected plank.
- `self._planks: list[Sprite]` — all plank instances this level.
- `self._plank_anchors: dict[str, tuple[int, int]]` — sprite name
  → anchor cell (top-left of the 2×2 anchor region for the east
  orientation; this cell stays fixed across rotations).
- `self._plank_orientations: dict[str, int]` — name → 0/1/2/3
  (east/south/west/north).
- `self._plank_lengths: dict[str, int]` — name → length.
- `self._posts: list[tuple[Sprite, Sprite]]` — (blocking,
  permeable) twin pairs at the same cell.
- `self._springs: list[Sprite]` — every spring this level.
- `self._spring_owner: dict[str, Sprite]` — spring name → owning
  plank sprite (used to read launch direction from the plank's
  current orientation).
- `self._spring_offsets: dict[str, tuple[int, int]]` — spring
  name → offset-from-anchor in the plank's east-orientation
  frame (used to recompute spring position after plank rotation).
- `self._step_counter_ui: StepCounterHud`.
- `self._pawn: Sprite`.
- `self._goal: Sprite`.
- `self._anchor_halo: Sprite`.
- `self._max_steps: int` — read from `level.get_data("step_budget")`.
- `self._spring_pending: bool` — True when pawn ends a step on a
  spring; spring fires before `complete_action()` returns.

**No-hidden-state visual cues** (per checklist item 19):
- *Active plank*: `anchor_halo` overlay on its anchor.
- *Post state*: two-sprite-swap (filled vs. hollow visual).
- *Pawn position*: rendered directly.
- *Step budget*: depleting yellow-on-black bar.
- *Plank orientation*: visible from anchor's position relative
  to plank body.
- *Spring direction*: implicit from the underlying plank's
  orientation (anchor-end vs. tip-end), which is visible on
  the plank itself; the spring's symmetric pixel pattern
  carries no directional bias of its own.

No internal state is hidden behind pixel-mutation. All state
mutations have a corresponding persistent visual cue.

## 7. Win condition

> `_check_win()` returns True iff the pawn's grid cell exactly
> equals the goal_tile's grid cell.

When True, `self.next_level()` fires. Same predicate at all 3
levels. After L3 wins, the engine auto-calls `self.win()`.

## 8. Lose condition

> If `self._action_count >= self._max_steps`, call `self.lose()`
> at the top of `step()` and return early.

No collision-based instant-fail. The pawn cannot die by
walking-into-wall (just doesn't move). Posts and springs are
not lethal. Step-budget exhaustion is the only lose path —
consistent with the universal step-counter convention.

## 9. Novelty note

(Unchanged from revision 1; the spring sprite redesign and grid
rescaling do not affect the mechanic-novelty argument.
Cross-references and distinguishing rules vs. taxonomy and
prior-games entries below are restated for completeness.)

### Closest taxonomy entries

- **`cn04` (rotate-translate-jigsaw)**. cn04 rotates a piece in
  place around the piece's centre; kj82 rotates a plank around a
  fixed anchor end with sweep-arc geometry. cn04's verb set is
  {select, translate, rotate}; kj82's is {select, rotate, walk-
  pawn} — translation is not a verb in kj82, the planks are
  pinned. Win conditions disjoint.

- **`ar25` (shape-mirror-cover)**. ar25 has reflectors and
  mirror-image gameplay; kj82 has neither. Rotation in ar25 is
  in-place around centre; kj82's is anchor-pinned.

### Closest prior-games entries

- **`pz4t` (anchor-pivot-place)**. pz4t is a tiling puzzle with
  user-chosen placement anchors and free piece translation; kj82
  has level-author-fixed anchors and pinned planks. Goals
  disjoint (tile-region vs. path-walk).

- **`bx84` (beam-mirror-reflect)**. No beam in kj82; planks are
  walkable platforms.

- **`wt39` (glide-deflect-thaw)**. wt39's pawn glides under
  physics; kj82's pawn walks discrete cells.

- **`pj7k` (rolling-cube-face-paint)**. pj7k has a cube-as-
  avatar that rolls; kj82's avatar is a separate small pawn that
  walks on planks without permuting any face.

- **`xn5p` (chamber-stamp-partition)**. xn5p stamps walls; kj82
  does not stamp or modify walls.

### Negative-similarity check

Per `mechanic-pick.md`'s 8-dimension walk: shared-dimension count
with each closest prior is ≤ 1 (the universal step-budget lose-
condition). Threshold for rejection is 3+; pass.

`prior-games/index.md` is non-empty (29 entries); all flagged
near-misses have explicit distinguishing rules above.

---

**End of revision 2.**
