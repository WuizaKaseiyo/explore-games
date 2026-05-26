# mechanic-spec.md — qm4t (convex-pen-trap) — v2

> **Revision pass v2.** Addresses every issue raised in
> `critique-revisions.md`:
> - §3 — `strike_marker` redesigned (Issue 3).
> - §3 — `vertex_post` simplified to a 3-tall vertical bar (Issue 4).
> - §3 — `critter_*` and `patroller_purple` shapes diverged
>   visually so they do not share appearance with different roles
>   (spec-quality note from critique).
> - §4 / L2 — maroon count bumped 2 → 4, layout revised, trivial-
>   fallback closed (Issue 1).
> - §4 / L3 — patroller count bumped 1 → 3 with synced cycle,
>   layout revised, trivial-fallback closed (Issue 2).

## 1. Title
Convex Pen Trap (working title — never visible in-game).

## 2. Mechanic family
**convex-pen-trap.** The player places `vertex_post` sprites by
clicking empty cells; the engine computes and renders the convex
hull of all currently placed posts as a 1-pixel outline (plus a
faint inside-tint). ACTION5 *commits* the pen: every critter or
patroller sprite whose centre lies STRICTLY INSIDE the convex
hull is consumed; if the consumed sprite is a target-colour
critter, one matching tally-dot is also removed; otherwise a
`strike_marker` is added (cap 3, third strike → `lose()`). After
commit all `vertex_post`s are removed from the level and the
overlay is cleared. Win = empty tally; lose = 3 strikes or step
budget exhausted.

Priors used (per `core-knowledge-priors.md`):
- **Geometry & topology** (load-bearing): convex-hull
  construction and inside/outside testing.
- **Objectness**: critters and posts are persistent coherent
  sprites that move on/off the level.
- **Agentness** (L3 only): patrollers walk a fixed loop
  independent of the player.

## 3. Sprite roster

All sprites use palette 0..15 only (`-1` = transparent). All
sprites are designed at the display-pixel level on a 64×64
canvas (no upscaling; full default camera viewport).

### `vertex_post` — 1 × 3
```
[[6],
 [6],
 [6]]
```
- Palette: `{6 magenta}`. Tags: `["sys_click"]`.
- Role: a stake / marker. Click an empty cell to place;
  click an existing post to remove. Vertical bar of 3 cells
  is explicitly OK per `forbidden-elements.md` ("a vertical
  bar of 3 cells is fine").

### `critter_green` — 5 × 4 (rounded blob with central hole)
```
[[-1, 14, 14, 14, -1],
 [14, 14,  0, 14, 14],
 [14, 14, 14, 14, 14],
 [-1, 14, 14, 14, -1]]
```
- Palette: `{14 green, 0 white, -1}`. Tags:
  `["critter", "critter_green"]`.
- Role: a target creature. Captured if its centre is inside
  the pen at commit; capture matches green tally-dots.

### `critter_yellow` — 5 × 4 (same shape, yellow)
```
[[-1, 11, 11, 11, -1],
 [11, 11,  0, 11, 11],
 [11, 11, 11, 11, 11],
 [-1, 11, 11, 11, -1]]
```
- Palette: `{11 yellow, 0 white, -1}`. Tags:
  `["critter", "critter_yellow"]`.
- Role: target creature for yellow tally-dots.

### `critter_maroon` — 5 × 4 (same shape, maroon)
```
[[-1, 13, 13, 13, -1],
 [13, 13,  0, 13, 13],
 [13, 13, 13, 13, 13],
 [-1, 13, 13, 13, -1]]
```
- Palette: `{13 maroon, 0 white, -1}`. Tags:
  `["critter", "critter_maroon"]`.
- Role: **forbidden creature.** Capture costs 1 strike. Visual
  signature: same body shape as `critter_green` /
  `critter_yellow` *because they share the role-class
  "target-or-anti-target by colour"*; only the colour
  distinguishes target from forbidden. (Per
  `reference-game-patterns.md` § Discoverability: "Identical
  visuals imply shared or correlated roles" — these three
  sprites ARE correlated, all "critters of one colour
  matters" — the colour is the type label.)

### `patroller_purple` — 5 × 5 (tapered diamond, single eye)
```
[[-1, -1, 15, -1, -1],
 [-1, 15, 15, 15, -1],
 [15, 15,  0, 15, 15],
 [-1, 15, 15, 15, -1],
 [-1, -1, 15, -1, -1]]
```
- Palette: `{15 purple, 0 white, -1}`. Tags: `["patroller"]`.
- Role: forbidden mobile creature. Walks a fixed cycle (one
  cell per turn). Different SHAPE from the critter family
  (taller diamond + single central eye + no flat-rectangle
  body) so the player reads patrollers as a *different kind
  of thing* even though it shares "creature" gestalt.
- (Note: not tagged `sys_click` — the player can't pick up a
  patroller via click, only enclose-and-capture via pen.)

### `tally_dot_green` — 3 × 3
```
[[14, 14, 14],
 [14,  0, 14],
 [14, 14, 14]]
```
- Palette: `{14 green, 0 white}`. Tags:
  `["tally", "tally_green"]`. `interaction=INTANGIBLE` (HUD —
  shouldn't block anything).
- Role: outstanding green-required count. One per critter the
  player still needs. Removed individually on green capture.

### `tally_dot_yellow` — 3 × 3 (same structure, palette 11)
```
[[11, 11, 11],
 [11,  0, 11],
 [11, 11, 11]]
```
- Tags: `["tally", "tally_yellow"]`.

### `strike_marker` — 3 × 3 (filled red square)
```
[[8, 8, 8],
 [8, 8, 8],
 [8, 8, 8]]
```
- Palette: `{8 red}`. Tags: `["strike_hud"]`.
  `interaction=INTANGIBLE`.
- Role: one added per strike, up to 3, in the HUD strike band.
  Solid red 3×3 — uniform fill, no internal pattern. Not a
  letter, digit, or culturally-conventional glyph.

### `pen_overlay` — 64 × 64
- Palette pixels written at runtime: `1 off-white` for hull
  boundary cells, `2 light-grey` for hull interior cells,
  `-1` elsewhere. Initial pixels: all `-1`.
- Tags: `["pen_overlay"]`. `interaction=INTANGIBLE`. `layer=5`.
- Role: pen visualisation. Recomputed at end of every step.

`BACKGROUND_COLOR = 5` (black). `PADDING_COLOR = 5`.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels use `grid_size=(64, 64)` and the default 64×64
camera viewport. HUD bands: rows 0–3 (tally row), rows 59–61
(strike chips columns 50..61), row 63 (step-counter HUD bar).
Playfield occupies rows 4–58.

### Level 1 — base dynamic system

**Mechanics required by the witness** (N = 2):
- **M1.** *Place vertex posts on empty cells via ACTION6.*
  Each ACTION6 click on an empty cell adds a `vertex_post` at
  that cell. The convex hull of all currently-placed posts is
  rendered into the `pen_overlay` at end-of-step.
- **M2.** *Commit the pen via ACTION5.* On commit: for every
  `critter` or `patroller` sprite whose centre is strictly
  inside the convex hull, remove the sprite. For each removed
  critter whose colour has an outstanding tally-dot, also
  remove one matching tally-dot. For each removed
  non-matching critter or patroller, append one
  `strike_marker`. Then remove every `vertex_post` and clear
  the overlay.

**Necessity per mechanic:**
- *L1 cannot be solved without triggering M1*, because the
  game class never adds posts via any code path other than
  the ACTION6 placement branch — without M1 the post list
  stays empty, the hull algorithm returns "fewer than 3
  points → no polygon", `pen_overlay.pixels` stays all `-1`,
  and ACTION5 finds no critter inside the (non-existent)
  hull.
- *L1 cannot be solved without triggering M2*, because the
  only function in the game class that calls
  `level.remove_sprite` on a critter is `_commit_pen` (the
  ACTION5 handler). Critters do not auto-decay, and there is
  no walk-into-them mechanic.

**Sprite layout** (centre-of-bbox cell coordinates):
- `critter_green` × 3 at `(20, 20)`, `(40, 22)`, `(30, 40)`.
- `tally_dot_green` × 3 at `(20, 0)`, `(28, 0)`, `(36, 0)`.
- Step counter HUD across row 63, max=30.
- No maroons, no patrollers.

**Witness solution** (length 4):
1. `ACTION6 @ (15, 15)` (display-pixel coords; grid coord
   `(15, 15)` at default 64×64 camera) — places post 1 at
   the upper-left of the green cluster.
2. `ACTION6 @ (50, 15)` — places post 2 at upper-right.
3. `ACTION6 @ (30, 50)` — places post 3 at lower-centre. The
   triangle defined by these three posts strictly contains
   each of `(20, 20)`, `(40, 22)`, `(30, 40)` (verified by
   ray-casting test against the triangle).
4. `ACTION5` — commit. All 3 greens are inside; all 3 are
   captured; all 3 tally-dots removed. Tally empty →
   `next_level()`.

**Difficulty justification:**
- **(a) Random-resistance.** A random/vision-blind agent
  has no spatial bias; the chance that 3 random cells form
  a triangle strictly enclosing the 3 specific green centres
  is ≪ 1/10⁴ within a 30-step budget.
- **(b) Human-tractable.** ~1 minute. Tally dots match
  critter colours; appearance of an outline polygon after 3
  clicks makes the ritual quickly discoverable.
- **(c) Planning depth.** **No strict planning requirement.**
  L1 is the discovery gate; once the rule is understood, the
  win is near-immediate (place 3 posts surrounding the
  cluster, commit).
- **(d) Step budget = 30.** Generous over the 4-action
  witness (~7×).

### Level 2 — base system + 1 new mechanic

**Mechanics required by the witness** (M = N + 1 = 3):
- M1, M2 (carried forward from L1).
- **M3 (new). *Selective subset choice via colour-aware shape
  sizing.*** L2 contains target critters (green) AND
  forbidden critters (maroon, 4 of them). Capturing each
  forbidden critter adds one `strike_marker`; 3 strikes
  trigger `lose()`. Therefore an "all-encompassing pen"
  captures 3 targets + 4 forbidden → 4 strikes → `lose()`,
  before tally clears. The witness MUST place posts forming
  a small enough triangle to *exclude* enough of the
  forbidden critters. With 4 maroons positioned at the
  playfield corners and the greens clustered in the centre,
  the only viable triangles are those whose all 3 vertices
  sit strictly between the green cluster and the corner
  maroons.

**Necessity per mechanic:**
- *L2 cannot be solved without triggering M1*, because (as
  in L1) zero posts means no hull and ACTION5 is a no-op.
- *L2 cannot be solved without triggering M2*, because (as
  in L1) the only critter-removal pathway is the commit
  handler.
- *L2 cannot be solved without triggering M3*, because the
  layout below has 4 maroons at `(5, 5)`, `(58, 5)`,
  `(5, 58)`, `(58, 58)` and 3 greens centrally clustered. A
  pen vertex placed at any of `{(0..4, ·), (·, 0..4),
  (59..63, ·), (·, 59..63)}` puts at least one maroon
  inside the hull (the maroon is between the vertex and the
  green cluster); that vertex is also necessary to surround
  the greens unless the triangle is *strictly between* the
  greens' bounding box `[(15..45) × (15..45)]` and the
  corner maroons. Concretely: enumerate "cover-everything"
  triangles like `(0,0), (63,0), (32,63)` — captures all 4
  maroons, 4 strikes, lose. Enumerate "tight-around-greens"
  triangles like `(13,13), (47,13), (30,50)` — captures 0
  maroons, 3 greens. The witness's forced shape is the
  tight one; the trivial-fallback path is closed.

**Sprite layout:**
- `critter_green` × 3 at `(20, 20)`, `(40, 25)`, `(30, 45)`
  (centre cluster).
- `critter_maroon` × 4 at `(5, 5)`, `(58, 5)`, `(5, 58)`,
  `(58, 58)` (playfield corners — outside any reasonable
  green-enclosing triangle).
- `tally_dot_green` × 3 at `(20, 0)`, `(28, 0)`, `(36, 0)`.
- Step counter HUD row 63, max=50.

**Witness solution** (length 4):
1. `ACTION6 @ (12, 15)` — post 1, upper-left of green
   cluster but inside the corner-maroon's row/column.
2. `ACTION6 @ (52, 15)` — post 2, upper-right of cluster.
3. `ACTION6 @ (32, 55)` — post 3, lower-centre of cluster.
4. `ACTION5` — commit. The triangle `(12,15)-(52,15)-(32,55)`
   strictly contains each green centre `(22.5, 22)`,
   `(42.5, 27)`, `(32.5, 47)` and none of the 4 corner
   maroons. All 3 greens captured, tally empty →
   `next_level()`.

  - Maroon `(5, 5)`: x=5 is left of the triangle's leftmost
    edge x ≥ 13 at y=5 → outside.
  - Maroon `(58, 5)`: x=58 is right of triangle's rightmost
    edge x ≤ 50 at y=5 → outside.
  - Maroon `(5, 58)`: y=58 is below triangle's bottom edge
    (which ends at y=52) → outside.
  - Maroon `(58, 58)`: same → outside.

**Difficulty justification:**
- **(a) Random-resistance.** Same triangle-hits-all-3-greens
  geometric fraction as L1, AND the trivial-fallback paths
  (large triangles) now actively lose. Below 1/10⁴.
- **(b) Human-tractable.** ~2 minutes. The player sees
  green dots in the tally row, maroon critters at the
  corners; observes that a small triangle around the green
  cluster wins, while a big triangle accumulates strikes and
  loses. Discovery + planning are both quick.
- **(c) Planning depth (post-discovery).** **Moderate.** At
  L2's start with the mechanic understood, the player faces
  several plausible 3-click triangles (the greens are at
  three centre cells; the maroons sit at four corners).
  Plausible *wrong* paths a fully-informed player would
  consider and reject: (i) "pick the green centres themselves
  as posts" — the triangle's vertices would coincide with
  the greens, but a triangle's *interior* is strictly inside
  the vertices, so this excludes the very greens that are
  the vertices; the player rejects this. (ii) "use the four
  playfield corners as posts" — captures 4 maroons and
  loses. (iii) "use 5 posts to draw a pentagon and avoid
  every maroon" — adds posts inside the existing hull, which
  doesn't change the shape (convex hull is monotone in
  vertex set); player must instead place posts JUST OUTSIDE
  each green. Witness reasoning chain: post 1 must be at
  some `(x, y)` with `x < 20 and y < 20` (outside the
  upper-left green's bounding box) but `x > 5 and y > 5`
  (right and below the upper-left maroon) — `(13, 13)` is in
  that band. Same logic for posts 2 and 3.
- **(d) Step budget = 50.** Generous over the 4-action
  witness (~12×). Patroller-style timing is not active at L2
  so most of the budget goes to revisions and recovery.

### Level 3 — system + 1 more new mechanic

**Mechanics required by the witness** (= L2-count + 1 = 4):
- M1, M2, M3 (carried forward from L2).
- **M4 (new). *Patroller-timing.*** L3 contains 3 patrollers,
  each with the same 8-step cycle and synchronised at
  level-start. The shared cycle is engineered so that during
  phases 0..3 every patroller sits at a cell *inside* any
  reasonable witness pen, and during phases 4..7 every
  patroller sits at a cell *outside* the same pen. Because
  capturing 3 patrollers in one commit is 3 strikes →
  `lose()`, ACTION5 fired during phases 0..3 always loses;
  ACTION5 fired during phases 4..7 is safe. The witness
  must therefore *count* its own placement actions modulo 8
  and time the commit to land on a phase ≥ 4.

**Necessity per mechanic:**
- *L3 cannot be solved without triggering M1*, because (as
  in L1, L2) no posts ⇒ no hull ⇒ ACTION5 captures nothing.
- *L3 cannot be solved without triggering M2*, because (as
  in L1, L2) `_commit_pen` is the only critter-removal
  pathway in the game class.
- *L3 cannot be solved without triggering M3*, because the
  level has 3 maroons at `(8, 32)`, `(58, 32)`, and
  `(32, 4)`. A trivial all-encompassing pen (e.g. vertices
  `(0,0)-(63,0)-(32,63)`) captures all 3 maroons → 3 strikes
  → `lose()`, before the tally clears. Even smaller pens
  that include any single maroon plus the patrollers (if
  M4 is also skipped) yield 1 + 3 = 4 strikes. The witness
  must place vertices in a band BETWEEN the cluster
  `(15..50, 15..50)` and the maroons (which sit at x ≤ 8 OR
  x ≥ 58 OR y ≤ 4) so that all 3 maroons are excluded. A
  formal verification at the witness pen `(10,10)-(56,12)-
  (38,56)-(8,56)`: the top edge runs from y=10 at x=10 to
  y=12 at x=56, so at x=32 the top edge is at y ≈ 10.7,
  meaning the maroon at `(32, 4)` lies at y=4 < 10.7 —
  ABOVE the top edge — outside. The other two maroons are
  excluded by the left and right edges (verified in §4 / L3
  / Witness solution).
- *L3 cannot be solved without triggering M4*, because the
  3 patrollers' cycle has cells `[(28, 28), (28, 32),
  (32, 32), (32, 28),  (8, 8), (8, 56), (56, 56), (56, 8)]`.
  Phases 0..3 are inside the witness pen (centre 4-cell
  loop); phases 4..7 are at the four corners (outside any
  reasonable green-and-yellow-enclosing pen). Capturing 3
  patrollers = 3 strikes = lose. Therefore committing on a
  phase 0..3 always loses regardless of pen geometry. The
  witness MUST place posts so that the action-count after
  the final placement (i.e. the commit's phase) lands in
  phase 4..7.

**Sprite layout:**
- `critter_green` × 3 at `(15, 15)`, `(50, 18)`, `(32, 50)`.
- `critter_yellow` × 2 at `(20, 32)`, `(45, 32)`.
- `critter_maroon` × 3 at `(8, 32)`, `(58, 32)`, `(32, 4)`.
- `patroller_purple` × 3, each starting at cycle phase 0.
  Cycle (shared across all 3 patrollers — a single list in
  level data; each patroller has its own offset within the
  list):
  ```
  cycle = [(28, 28), (28, 32), (32, 32), (32, 28),
           (8, 8),   (8, 56),  (56, 56), (56, 8)]
  patroller_starts = [0, 1, 2]   # phase offsets
  ```
  Phase index advances by 1 every action (any action). At
  any time `t = self._action_count`, patroller `i`'s
  position is `cycle[(t + i) mod 8]`.
  - Wait — for *synced* in-vs-out behaviour, all 3
    patrollers must be inside on phases 0..3 and outside on
    phases 4..7 simultaneously. If they have offset starts
    they de-synchronise. Use the SAME start phase for all 3
    (`patroller_starts = [0, 0, 0]`); position them at
    *different* cycle cells visually by placing them at
    different cells of the inside-loop initially, all of
    which transition into the outside-corner loop together.

  Final patroller setup:
  - Patroller A starts at `cycle[0] = (28, 28)`, on phase 0.
    Advances through phases 0..7 cell-by-cell.
  - Patroller B starts at `cycle[1] = (28, 32)`, on phase 0
    (i.e. its `position_index = (action_count + 1) mod 8`).
  - Patroller C starts at `cycle[2] = (32, 32)`, on phase 0
    (`position_index = (action_count + 2) mod 8`).

  At any action count `t`:
  - A is at `cycle[t mod 8]`.
  - B is at `cycle[(t + 1) mod 8]`.
  - C is at `cycle[(t + 2) mod 8]`.

  For all three to be on inside-cells (cycle indices 0..3),
  we need `{t, t+1, t+2} mod 8 ⊆ {0, 1, 2, 3}`. The only
  `t mod 8` satisfying this is `t mod 8 = 0` or `1` (then
  the maximum offset 2 lands on indices 2 or 3, still
  inside). For `t mod 8 = 2`, A=2, B=3, C=4 — C is outside.
  So A and B inside, C outside. Mixed.

  This is getting tangled. **Simplify**: have a SINGLE
  `patroller_phase` integer that advances every action;
  each patroller's position is read from a SINGLE master
  cycle and the patrollers share the same phase. The 3
  patrollers' positions at phase `p` are
  `[cycle[p], cycle_b[p], cycle_c[p]]` where `cycle_b` and
  `cycle_c` are shifted but **synchronously enter/leave**
  the inside region.

  **Final patroller cycle (synced)** — use 3 SEPARATE
  parallel cycles so that all 3 patrollers transition
  simultaneously between "all inside" and "all outside":
  ```
  cycle_A = [(28,28), (28,30), (30,30), (30,28), (4,4),  (4,8),  (8,8),  (8,4) ]
  cycle_B = [(34,28), (34,30), (36,30), (36,28), (4,55), (4,59), (8,59), (8,55)]
  cycle_C = [(28,34), (28,36), (30,36), (30,34), (55,4), (55,8), (59,8), (59,4)]
  ```
  Phase 0..3: each patroller is on cells in the centre band
  `(28..36, 28..36)` — all inside the witness pen (centre).
  Phase 4..7: each patroller is on cells in a different
  playfield corner — all outside the witness pen.
- `tally_dot_green` × 3 at `(15, 0)`, `(23, 0)`, `(31, 0)`.
- `tally_dot_yellow` × 2 at `(40, 0)`, `(48, 0)`.
- Step counter HUD row 63, max=80.

**Witness solution** (length 5):
1. `ACTION6 @ (12, 13)` — post 1, upper-left. Action count →
   1; patroller phase 1 (cells `(28,30)`, `(34,30)`,
   `(28,36)` — all centre band, all inside any reasonable
   pen). 1 post on board — no hull yet.
2. `ACTION6 @ (54, 13)` — post 2, upper-right. Action count
   → 2; phase 2. 2 posts — no hull (need ≥ 3).
3. `ACTION6 @ (54, 54)` — post 3, lower-right. Action count
   → 3; phase 3. 3 posts — triangle hull renders. **Phase
   3 is still inside; do not commit yet.**
4. `ACTION6 @ (12, 54)` — post 4, lower-left. Action count
   → 4; phase 4. The 4 posts form an axis-aligned
   rectangle `[12..54] × [13..54]` whose interior contains
   the 3 greens (`(15,15)`, `(50,18)`, `(32,50)`), both
   yellows (`(20,32)`, `(45,32)`), and neither maroon
   (maroon at `(8,32)` is left of x=12; maroon at `(58,32)`
   is right of x=54; maroon at `(32,4)` is above y=13).
   Patroller phase 4 — all 3 patrollers at corner cells
   (`(4,4)`, `(4,55)`, `(55,4)`), all outside the rectangle.
5. `ACTION5` — commit. All 5 required critters captured
   (3 greens + 2 yellows); zero maroons captured; zero
   patrollers captured. Tally empty → `win()` (since L3
   is the last level).

  Geometry verification (witness pen = axis-aligned rectangle
  vertices `(12, 13)`, `(54, 13)`, `(54, 54)`, `(12, 54)`):
  Each test point's inside-ness follows from
  `12 < x < 54 AND 13 < y < 54`. Verified by the engine's
  ray-casting test:
  - Green centres (sprite is 5×4, so centre at top-left
    + (2.5, 2)): `(17.5, 17)`, `(52.5, 20)`, `(34.5, 52)` —
    all inside.
  - Yellow centres: `(22.5, 34)`, `(47.5, 34)` — both
    inside (x range `[22.5, 47.5]` ⊂ `(12, 54)`, y=34 ∈
    `(13, 54)`).
  - Maroon centres: `(10.5, 34)` — outside (x=10.5 < 12);
    `(60.5, 34)` — outside (x=60.5 > 54); `(34.5, 6)` —
    outside (y=6 < 13).
  - Patroller centres at phase 4 (sprite is 5×5, centre at
    top-left + (2.5, 2.5)): `(6.5, 6.5)`, `(6.5, 57.5)`,
    `(57.5, 6.5)` — all outside (each fails at least one
    bound test).

**Difficulty justification:**
- **(a) Random-resistance.** Combined L2-style geometric
  selection AND L3 patroller-timing constraint: a random
  agent's chance of accidentally placing 4 posts in the
  right band AND committing on a phase 4..7 of an
  8-cycle is ≪ 1/10⁴ even within the 80-step budget.
- **(b) Human-tractable.** ~3 minutes — the player sees
  the patrollers walk a small loop, observes that they
  spend half the cycle in the centre and half at the
  corners, and times the commit accordingly.
- **(c) Planning depth (post-discovery).** **Challenging
  even for an attentive human.** **Trivial heuristic that
  fails:** *"Place a small triangle (or quadrilateral)
  around the required-colour cluster and commit
  immediately"* — this is precisely the L2 strategy. Fails
  at L3 because the patrollers are at phase 0 (inside the
  pen) at level start; committing at action 3 (the
  earliest commit-able phase if the player places exactly
  3 posts) gives `_action_count = 3`, phase 3 — still
  inside. Capturing 3 patrollers = 3 strikes = lose. The
  witness diverges at action 4: instead of committing
  after 3 posts, it places a *4th* post at `(8, 56)`,
  pushing `_action_count` to 4 and phase to 4 (corners,
  outside). Ahead-of-time reasoning required: the player
  must (i) observe that patrollers are mobile and have a
  cycle, (ii) track the cycle length (8), (iii) plan their
  post-placement count so the immediately-following ACTION5
  fires on a corner-phase. The post-discovery decision space
  at level start: 4 valid first posts (any of 4 outside-of-
  cluster regions), ≥ 4 valid 2nd-3rd posts each, plus the
  decision of whether to commit at 3-post-count or place a
  4th post for timing. Plausible wrong action paths: (i)
  3-post tight commit at action 3 (loses, phase 3 inside);
  (ii) 4-post quad with the 4th post placed *inside* the
  existing 3-post triangle (4th post is interior; convex
  hull unchanged; commit fires at phase 4 — wins, but a
  fully-informed player should recognize this is a
  "wasteful" 4th post; the witness uses an outside-the-
  current-hull 4th post which actively reshapes).
- **(d) Step budget = 80.** Does NOT shrink relative to
  L2; the patroller-timing exploration costs additional
  turns during discovery. Generous (~16× the witness).

## 5. Action mapping

`available_actions = [5, 6]`. Pure click + commit family.

- **ACTION5 — `commit_pen`.** Always valid. Behaviour:
  - If fewer than 3 posts placed, no-op.
  - Otherwise compute the convex hull of all current post
    positions (using monotone-chain Andrew's algorithm —
    O(N log N), with N ≤ 8); for each `critter` and
    `patroller` sprite whose centre lies strictly inside the
    hull, remove the sprite. For each removed `critter`
    whose colour has an outstanding `tally_dot_<colour>`
    sprite, also remove one matching tally-dot. For each
    removed non-matching critter or patroller, add one
    `strike_marker` (capped at 3). After consumption, remove
    every `vertex_post` sprite and clear the `pen_overlay`
    pixels to all `-1`. Increment `_action_count`. Increment
    patroller `phase` by 1 (only at L3).
- **ACTION6 — `click(x, y)`.** Always valid. Behaviour:
  - Convert click coords to grid coords via
    `self.camera.display_to_grid(int(x), int(y))`. If `None`
    (out of frame), no-op.
  - If the grid cell is occupied by a `vertex_post`, remove
    that post.
  - Else if the grid cell is in the playfield region (rows
    4..58 inclusive, AND not on top of an existing critter,
    patroller, or HUD sprite) AND `len(posts) < MAX_POSTS =
    8`, place a new `vertex_post` at the click cell.
  - Else no-op.
  - Increment `_action_count` once. Increment patroller
    `phase` (L3 only).
  - Recompute `pen_overlay`.

## 6. HUD and per-game state

**HUD (always visible):**
- **Tally band (rows 0..2).** A row of `tally_dot_<colour>`
  sprites (3×3 each) placed at columns starting `(15, 0)` and
  spaced 8 cells apart for legibility. Implemented as ordinary
  `Sprite` instances on the level, so individual capture maps
  to `level.remove_sprite`.
- **Strike band (rows 59..61, columns 50..62).** Up to 3
  `strike_marker` sprites at `(50, 60)`, `(56, 60)`, `(62, 60)`
  (3×3 each, gap of 3). Added one-by-one as strikes accrue.
- **Step-counter HUD (row 63).** A `StepCounterHud`
  (subclass of `RenderableUserDisplay`) painting palette `14
  green` for the remaining proportion and palette `5 black`
  for depleted, computed as `round(64 * remaining /
  max_steps)`. Updated at end-of-step.
- **Pen overlay.** `pen_overlay` Sprite (64×64,
  `interaction=INTANGIBLE`, `layer=5`) — pixels recomputed at
  end-of-step.

**Per-game state held on the `Qm4t` instance:**
- `self._step_counter_ui: StepCounterHud`.
- `self._max_steps: int`.
- `self._strikes: int` (0..3).
- `self._max_posts: int = 8`.
- `self._patroller_phase: int` (only used at L3; advanced
  every step).
- `self._patroller_cycles: list[list[tuple[int,int]]]` (per-
  patroller cycle list, set in `on_set_level`).
- `self._patroller_sprites: list[Sprite]` (the 3 active
  patrollers at L3; empty at L1/L2).

## 7. Win condition

After capture-and-strike resolution at end-of-step,
`current_level.get_sprites_by_tag("tally")` is empty →
`self.next_level()`. Triggered identically across L1, L2, L3
(only the initial tally counts differ).

## 8. Lose condition

Two predicates checked at end-of-step:
- `self._strikes >= 3` → `self.lose()`.
- `self._step_counter_ui.current_steps <= 0` → `self.lose()`.

Both fire `lose()`; whichever fires first ends the run.

If a commit captures multiple non-matching critters in one
shot AND the captures push `_strikes` past 3, the
`_strikes >= 3` check fires that step. The win check fires
*after* the lose check, so a single commit that simultaneously
empties the tally AND raises strikes to 3 results in a loss
(intentional — see L2 / L3 trivial-fallback closure
arguments).

## 9. Novelty note

Closest taxonomy entries:
- **su15** (radial-blast-capture). Distinguishing rule:
  qm4t's capture region is a *player-defined convex polygon*
  built across multiple clicks; su15's is a fixed-radius
  disk centred on a single click. su15's planning is
  targeting; qm4t's is geometric vertex selection.
- **ar25** (shape-mirror-cover). Distinguishing rule: ar25
  manipulates a movable SHAPE (one piece at a time, mirrored
  across an axis); qm4t deposits stationary VERTICES whose
  convex hull is queried statically. ar25's win is pixel
  alignment; qm4t's is multiset inclusion.
- **r11l** (centroid-puppet-leg). Distinguishing rule: r11l
  moves a single tethered leg sprite to a target with
  centroid-follow physics; qm4t places stationary posts.

Closest prior-games entries:
- **gv47** (seed-grow-surround-dissolve). Distinguishing rule:
  qm4t's "surround" is a static-geometry convex-hull
  inside-test (no time evolution between commits, no chemistry,
  no growth); gv47's is region growth + contact chemistry.
- **xn5p** (chamber-stamp-partition). Distinguishing rule:
  xn5p modifies TERRAIN to bisect a region; qm4t reads spatial
  containment of a non-modifying polygon.
- **ng52** (multiset-signature-classify). Distinguishing rule:
  ng52's grouping is by per-object click-assignment to bins;
  qm4t's is by spatial inclusion in a player-drawn convex
  hull.
- **kn58** (anchor-pull-magnet). Distinguishing rule: kn58 is
  attraction-with-motion; qm4t is enclosure-with-no-motion-
  until-commit.
- **pz4t** (anchor-pivot-place). Distinguishing rule: pz4t
  fills space with shape-pieces; qm4t classifies points by
  inclusion in a hull.

Negative similarity walk: each named near-miss shares ≤ 2 of
the 8 dimensions in `negative-similarity-check.md`. All below
the 3-dimension reject threshold. Core dynamic — "compute the
convex hull of clicked points, query inside-or-out for the
sprite-set" — has no precedent in either the 25 reference
games or the 34-prior corpus.
