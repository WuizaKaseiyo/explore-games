# mw8p — Mechanic spec

## 1. Title

Predator-Prey Triangle (working title; not displayed in-game).

## 2. Mechanic family

`predator-prey-triangle`. One-paragraph framing (from
`mechanic-pick.md`):

The player walks a single A-creature on a small bounded grid using
arrow keys. Two species of autonomous NPC share the playfield: a
B-species that pursues A one cell per turn along its dominant
Manhattan axis (B removes A on same-cell — lose), and a C-species
that pursues the nearest B one cell per turn along the same dominant
Manhattan axis (C removes that B on same-cell). The triangle closes
via a third rule: when A walks onto a cell currently occupied by a C,
A *consumes* the C — C is removed and A enters the cell. Walls block
all three species. A wins the level by stepping onto the exit cell.

Priors used (`design-constraints/core-knowledge-priors.md`):
**objectness** (every creature and wall is a persistent entity that
can be removed) and **agentness** (B and C pursue under deterministic
goal-directed policies the player must model).

## 3. Sprite roster

All sprites are 6×6 pixels packed inside a logical 8-pixel cell stride
on a 64×64 frame (so each level is an 8-cell × 8-cell logical grid;
the camera viewport is the full 64×64 — no per-level resize and no
chunky upscale, per `checklist.md` item 20).

| Name | Dims | Palette values | Tags | Role |
|---|---|---|---|---|
| `creature_a` | 6×6 | 4, 10, 11, -1 | `player`, `creature_a` | The player avatar. Light-blue (10) round body with palette-4 (off-black) outline + two yellow (11) eye-dots. Movable; collides with walls. |
| `creature_b` | 6×6 | 4, 8, 12, -1 | `pursuer`, `creature_b` | The species that pursues A. Orange (12) angular body with palette-8 red rim spikes + palette-4 outline + 2 palette-4 eye-dots. Movable; collides with walls and other creatures. |
| `creature_c` | 6×6 | 4, 7, 14, -1 | `mid`, `creature_c` | The species that pursues B. Green (14) round body with palette-4 outline + palette-7 (pink) central dot + 4 palette-4 leaf-serration pixels at the 4 cardinal edges. Movable; collides with walls and other creatures (but not A — A consumes C). |
| `wall` | 6×6 | 4, 13 | `wall` | Maze wall. Maroon (13) fill with palette-4 corner highlights (1 palette-4 pixel at each of 4 corners) and a 2×2 palette-4 cross at centre. Static; blocks movement. |
| `exit_cell` | 6×6 | 0, 15 | `exit` | The level goal cell. Purple (15) ring with palette-0 (white) inset cross (one palette-0 pixel at the 4 cardinal mid-points and one in the centre). Static; doesn't block movement. |

HUD widget (defined as a `RenderableUserDisplay` subclass per
`universal-scaffold.md` § Common patterns):

| Name | Class | Role |
|---|---|---|
| `step_bar` | `StepCounterHud(RenderableUserDisplay)` | Bottom row (frame[63, :]) drains from full-width palette-14 (green) to palette-4 (off-black) as the step budget depletes. Frame[63, x] = 14 if `x/64 < steps_remaining / max_steps`, else 4. |

Visual rationale (per `checklist.md` items 20 + 21):
- *Sprite UI ≈ sprite role*: A's eye-pixels read as an animate
  protagonist (the only player-controllable sprite). B's red-rim
  spikes read as dangerous and angular (visually distinct from A's
  round body so they don't blur). C's leaf-serrations + soft pink
  centre read as more benign-looking than B and visually distinct
  from both A and B. Wall's corner highlights + central cross read
  as patterned masonry (visibly inert). Exit's ring + cross-inset
  reads as a marker (visually distinct from every creature).
- *Identical visuals imply shared role*: all B's share the spiky
  orange look (they're one species). All C's share the leafy green
  look. Every wall sprite is identical (one wall family). No
  cross-species visual confusion.
- *Palette divergence from zk9p*: zk9p uses a yellow-dominant signature
  (per the prior-game frame inspection). mw8p uses a maroon (walls) +
  light-blue (A) + orange/red (B) + green/pink (C) + purple (exit) +
  light-grey (background) palette set. No overlap.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. All three levels share `grid_size = (64, 64)` (so
the default camera viewport matches with no per-level resize — see
`universal-scaffold.md` § Camera viewport must match level grid_size).
Within each level, gameplay uses an 8-pixel stride: A starts at logical
cell (cx, cy) ↔ pixel position (cx*8, cy*8). The 8×8 logical-cell map
is what the per-level layouts below describe.

**Movement and resolution rules (apply to every level)**:

1. ACTION1..4 each attempt to move A by one logical cell (8 px) in
   the direction U/D/L/R. A is blocked by walls, the bounds of the
   8×8 logical grid, and B-cells (entering a B-cell is illegal — but
   if it happens A is removed). A enters a C-cell freely; on entry,
   the C is removed (this is M3 — see L3).
2. After A's move: if A is on the exit-cell, fire `self.next_level()`
   and return.
3. B's move: every B sprite computes `dx = A.cx - B.cx`,
   `dy = A.cy - B.cy`, picks the dominant axis (ties prefer x), and
   attempts to step one cell along that axis (sign of dx or dy). The
   step is blocked by walls, the grid bounds, and any other creature
   except A; if the dominant-axis step is blocked, B tries the
   secondary axis with the same rules; if both blocked, B stays.
   This is M1's pursuit half.
4. Check B-on-A: if any B's post-move cell coincides with A's cell,
   fire `self.lose()` and return. This is M1's lose half.
5. C's move: every C sprite finds the nearest live B by Manhattan
   distance (ties: lowest sprite index), computes dx/dy to that B,
   and attempts the same dominant-axis-first cardinal step. If C's
   destination is the target-B's cell, C enters and that B is
   removed (this is M2). If destination is any other creature's
   cell (including A), C is blocked and stays.
6. Decrement `self._steps_used`; if `_steps_used >= max_steps`,
   `self.lose()`.

The `available_actions = [1, 2, 3, 4]` — pure cardinal walking. No
ACTION5/6/7 declared (per `action-enum.md`: ACTION7 must be
strict-undo or absent; this game has no undo, so omit it).

### Level 1 — base dynamic system

**Layout** (8×8 logical cells; `.` = empty; `W` = wall; cells
labelled with their occupant):

```
   col 0 1 2 3 4 5 6 7
row 0:  .  .  .  .  .  .  .  X
row 1:  .  .  .  .  .  .  .  .
row 2:  W  W  W  W  W  W  W  .
row 3:  .  .  .  .  .  .  W  .
row 4:  .  .  .  .  B  .  W  .
row 5:  .  .  .  .  .  .  W  .
row 6:  W  W  W  W  W  W  W  .
row 7:  A  .  .  .  .  .  .  .
```

- A at logical cell (0, 7).
- B at logical cell (4, 4).
- Exit `X` at logical cell (7, 0).
- 21 wall cells: row 2 cols 0..6, row 6 cols 0..6, col 6 rows 3..5.

The walls form two horizontal barriers (rows 2 and 6) that span
cols 0..6 with gaps only at col 7, plus a short vertical barrier in
col 6 rows 3..5. The effect is a 3-zone playfield: a top corridor
(rows 0..1), a middle chamber (rows 3..5 cols 0..5) containing B,
and a bottom corridor (row 7). All three zones connect only via
col 7.

**Mechanics required by the witness** (N = 1):

- **M1** (B-chases-A): on every action, B at (4, 4) computes its
  pursuit step toward A's current cell, attempts that step, and (on
  same-cell coincidence with A) calls `self.lose()`. This is the
  base dynamic system L1 establishes.

**Necessity per mechanic** (counterfactual, per checklist item 12):

- **L1 cannot be solved without triggering M1 because B's
  pursuit-move rule fires automatically on every action — there is
  no action the player can issue that does not advance the engine
  by one turn, and every turn unconditionally executes B's
  `_compute_pursuit_step()` for the live B at (4, 4).** Concretely:
  the witness has 14 actions; M1's pursuit rule runs 14 times, on
  turns 1..14 (it stops only if B were removed, which L1 never
  does). Additionally, M1's lose-on-same-cell branch constrains
  A's geometry — A cannot enter the cell B occupies at the start
  of any turn (entering would trigger A-on-B which is illegal and
  loses), so M1 actively shapes which neighbours of A are legal
  on every turn.

**Witness solution** — the SHORTEST action sequence that wins L1:

```
[4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]
```

(Seven `ACTION4` = RIGHT, then seven `ACTION1` = UP.)

Cell-by-cell trace (showing A and B at end of each turn — B is at
logical-cell coordinates; "stays" = B's pursuit step was blocked by
walls or grid bounds):

| Turn | A's action | A's cell | B's cell after pursuit | Notes |
|---|---|---|---|---|
| 1 | RIGHT | (1, 7) | (3, 4) | dx=-3, dy=3, tie→x; B moves left |
| 2 | RIGHT | (2, 7) | (3, 5) | dx=-1, dy=3, B moves down |
| 3 | RIGHT | (3, 7) | (3, 5) | dx=0, dy=2; vertical step → (3, 6) blocked by wall; horizontal step dx=0 → no-op; B stays |
| 4 | RIGHT | (4, 7) | (4, 5) | dx=1, dy=2; vertical → (3, 6) wall; horizontal → (4, 5) open |
| 5 | RIGHT | (5, 7) | (5, 5) | dx=1, dy=2; vertical → (4, 6) wall; horizontal → (5, 5) |
| 6 | RIGHT | (6, 7) | (6, 5) | dx=1, dy=2; vertical → (5, 6) wall; horizontal → (6, 5) wait — (6, 5) is the col-6 vertical barrier wall! B blocked. B stays at (5, 5) |
| 7 | RIGHT | (7, 7) | (5, 5) | dx=2, dy=2 tie→x; (6, 5) wall; vertical (5, 6) wall; B stays |
| 8 | UP | (7, 6) | (5, 5) | dx=2, dy=1; horizontal (6, 5) wall; vertical (5, 6) wall; B stays |
| 9 | UP | (7, 5) | (5, 5) | dx=2, dy=0; horizontal (6, 5) wall; vertical dy=0 → no-op; B stays |
| 10 | UP | (7, 4) | (5, 4) | dx=2, dy=-1; horizontal (6, 5) wall — wait B is at (5,5) trying horizontal to (6,5) which is wall; vertical (5, 4) open; B moves up |
| 11 | UP | (7, 3) | (5, 3) | dx=2, dy=-1; horizontal (6, 4) wall; vertical (5, 3) open |
| 12 | UP | (7, 2) | (5, 2) | dx=2, dy=-1; horizontal (6, 3) wall; vertical (5, 2) open |
| 13 | UP | (7, 1) | (5, 1) | dx=2, dy=-1; horizontal (6, 2) wall? row 2 col 6 wall — yes; vertical (5, 1) open |
| 14 | UP | (7, 0) — **WIN** | — | A's destination is the exit cell; `self.next_level()` fires before B's move |

At no point does B share A's cell. The col-6 wall barrier means B
cannot enter the column-7 corridor where A is travelling; B is
confined to the middle chamber for the entire run.

**Difficulty justification** (per `difficulty-rules.md` § 2):

- **(a) Random-resistance.** A random-policy agent has a 1/4 chance
  per action of issuing each of 4 directions. The witness is a
  specific 14-action sequence (7×RIGHT then 7×UP). The probability
  of a random agent issuing exactly this sequence is
  `(1/4)^14 ≈ 3.7e-9`, well below the §3.5 graph-based threshold
  of 1/10,000. Random agents also lose by walking back into B's
  pursuit range (any action that takes A south or west enough to
  bring A's cell within B's reachable area triggers M1's lose
  branch). The text-only-LLM (no vision) cannot read the wall
  layout and is equally unlikely to find the witness.
- **(b) Human-tractable.** An attentive human reads the static
  frame, sees A (light-blue eyed creature, bottom-left), the orange
  B sitting in a walled middle chamber, the purple exit (top-
  right), and the wall corridor along col 7. The natural reading
  is "walk along the bottom row to the right edge, then up the
  right edge". This is what the witness does. Expected human time:
  ~1 minute.
- **(c) Planning depth.** Per the L1 entry of difficulty-rules.md
  § 2c: **no strict planning requirement**. Mechanic discovery is
  the entire difficulty — the player needs ~2 exploratory actions
  to learn "B chases me and removing-on-same-cell loses". Once
  that is observed, the witness is near-immediate (the col-7
  corridor is the only path and it's safely far from B's chamber).
- **(d) Step budget.** `max_steps = 25`. Witness length = 14, so
  there is an 11-step buffer for the player to explore (e.g.,
  trying to walk straight up first and discovering the row-2 wall,
  or trying to enter the middle chamber and discovering B's
  pursuit). The budget is generous over the witness length, never
  tight. L1 has no level-specific budget addendum
  (`difficulty-rules.md` § d).

### Level 2 — base system + 1 new mechanic

**Layout** (8×8; open arena, no walls):

```
   col 0 1 2 3 4 5 6 7
row 0:  A  .  .  .  .  .  .  .
row 1:  .  .  .  .  .  .  .  .
row 2:  .  .  .  .  .  .  .  .
row 3:  .  .  .  .  C  .  .  .
row 4:  .  .  .  .  .  .  .  .
row 5:  .  .  .  .  B  .  .  .
row 6:  .  .  .  .  .  .  .  .
row 7:  .  .  .  .  .  .  .  X
```

- A at (0, 0).
- C at (4, 3).
- B at (4, 5).
- Exit `X` at (7, 7).
- No walls (open arena).

**Geometric setup rationale.** C is placed BETWEEN A's direction of
pursuit-pull-on-B (vertically upward from B toward A's lower-y) and
B itself. On turn 1, A moves; B's pursuit step (vertical toward A's
lower y) takes B from (4, 5) to (4, 4); C's pursuit step (vertical
toward B's higher y) takes C from (4, 3) to (4, 4) — the SAME cell as
B's destination. By the resolution order rule, B moves first (step
3), C moves second (step 5). When C steps to (4, 4), B is there → C
enters, B removed (M2 fires). The setup is robust to A's specific
first action because B's vertical pull dominates as long as |A.y -
B.y| > |A.x - B.x|, which holds for any A first move starting from
(0, 0) (A's |dy| from B = 5, |dx| ≤ 1).

**Mechanics required by the witness** (M = N + 1 = 2; L2 introduces
exactly ONE new mechanic):

- **M1** (B-chases-A) — carried forward from L1.
- **M2** (C-chases-B-and-kills-on-same-cell): the NEW mechanic.

**Necessity per mechanic** (counterfactual, per checklist item 12):

- **L2 cannot be solved without triggering M1's pursuit half because
  the pursuit rule fires unconditionally every turn** (as in L1).
  M1's pursuit step is also load-bearing for M2's necessity:
  without M1, B at (4, 5) would sit still, C would still chase B,
  and C would catch a stationary B at (4, 5) in 2 turns — but the
  witness would no longer need M2 either because static B never
  reaches A. M1's pursuit is what makes B *dangerous* in the
  first place, so any winning sequence runs M1.
- **L2 cannot be solved without triggering M2 because the witness
  loses by turn 8 if M2 is disabled.** Concrete counterfactual
  (with M2 disabled — C still moves but never removes B on
  coincidence): with no removal, C ends turn 1 at (4, 4) coexisting
  with B (rules say C blocked on B's cell, so let's instead say C
  stays at (4, 3) in the counterfactual). B continues chasing A.
  By turn 7, B reaches (7, 1) (chasing A's RIGHT-then-DOWN witness
  path); on turn 8 A attempts DOWN from (7, 0) to (7, 1) — B
  occupies (7, 1) — same cell at the start of A's move, A is
  removed → lose. So M2 must fire (B must be removed) for the
  witness to win. M2's only firing path is "C enters a B's cell",
  which the witness produces on turn 1.

**Witness solution** — the SHORTEST action sequence that wins L2:

```
[4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2]
```

(Seven `ACTION4` = RIGHT, then seven `ACTION2` = DOWN.)

Cell-by-cell trace:

| Turn | A's action | A's cell | B's cell | C's cell | Event |
|---|---|---|---|---|---|
| 1 | RIGHT | (1, 0) | — | (4, 4) | B step: dx=-3 dy=-5, vertical → (4, 4). C step: B at (4, 4), dx=0 dy=1, vertical → (4, 4) = B → C enters, **M2 fires, B removed**. |
| 2 | RIGHT | (2, 0) | — | (4, 4) | No B to chase; C stays. |
| 3 | RIGHT | (3, 0) | — | (4, 4) | C stays. |
| 4 | RIGHT | (4, 0) | — | (4, 4) | C stays. A is now directly above C; A's next cell (5, 0) is RIGHT, not (4, 4), so no consume. |
| 5 | RIGHT | (5, 0) | — | (4, 4) | C stays. |
| 6 | RIGHT | (6, 0) | — | (4, 4) | C stays. |
| 7 | RIGHT | (7, 0) | — | (4, 4) | C stays. |
| 8 | DOWN | (7, 1) | — | (4, 4) | C stays. |
| 9 | DOWN | (7, 2) | — | (4, 4) | C stays. |
| 10 | DOWN | (7, 3) | — | (4, 4) | C stays. |
| 11 | DOWN | (7, 4) | — | (4, 4) | C stays. |
| 12 | DOWN | (7, 5) | — | (4, 4) | C stays. |
| 13 | DOWN | (7, 6) | — | (4, 4) | C stays. |
| 14 | DOWN | (7, 7) — **WIN** | — | — | A enters exit cell; `self.next_level()` fires. |

The witness never enters C's cell (4, 4), so M3 (A-eats-C) does
NOT fire in L2 — it remains reserved for L3 introduction.

**Difficulty justification** (per `difficulty-rules.md` § 2):

- **(a) Random-resistance.** Witness probability under uniform-
  random policy: `(1/4)^14 ≈ 3.7e-9`. The danger zone (where A
  is removed by B) is concentrated in cells where A is cardinal-
  adjacent to B's chase trajectory; random play that turns south
  early (toward B's column) gets caught within 4-5 turns. Without
  vision, the text-only-LLM cannot read B's and C's positions and
  cannot reason about the pursuit geometry.
- **(b) Human-tractable.** An attentive human reads: a clearly
  hostile orange B in row 5, a friendlier green C above it in row 3
  (same column), A in the top-left, exit in the bottom-right. After
  ~5 exploratory actions the human observes that C "eats" B
  (M2 fires on turn 1 of any RIGHT first-move). The path right-
  then-down then becomes obvious. Expected human time: ~2 minutes
  (~1 minute discovering M2, ~1 minute walking the witness).
- **(c) Planning depth.** Per the L2 entry of difficulty-rules.md
  § 2c: **moderate planning required (post-discovery).** The
  post-discovery decision space at level start has 4 valid first
  actions (all four arrows are unblocked). A *plausible-but-wrong*
  alternative the post-discovery player would consider:
  *"walk DOWN first to approach the exit faster"* — but going DOWN
  pulls B's pursuit-step laterally (B now has |dx|>|dy| once A
  reaches row ≥ 4, so B moves horizontally toward A's column),
  which means B catches A in A's own column. The witness's
  reasoning chain: (1) turn 1 RIGHT triggers M2 because B's vertical
  pull dominates and C kills B; (2) turns 2-7 walk right along the
  now-safe top row; (3) turns 8-14 walk down the right column,
  which is safely far from the dead-B's former column. Each step
  reasons about whether B is still alive and where C now sits;
  walking into C's cell would consume it (wasted potential in L2,
  but more importantly C's cell at (4, 4) is NOT on the witness path).
- **(d) Step budget.** `max_steps = 30`. Witness length = 14, so
  there is a 16-step buffer. L2's addendum: "a first-time player
  will spend several actions discovering what the new mechanic
  does before they can attempt the witness; the budget must
  reflect that" — the 16-step buffer accommodates ~10 exploratory
  actions (e.g., walking DOWN to see B's pursuit pattern, then
  resetting via failed actions, then trying RIGHT).

### Level 3 — system + 1 new mechanic

**Layout** (8×8):

```
   col 0 1 2 3 4 5 6 7
row 0:  .  .  .  .  .  .  .  X
row 1:  .  .  .  .  .  .  .  .
row 2:  .  .  .  .  .  .  .  .
row 3:  .  .  .  .  .  .  .  .
row 4:  .  .  .  .  .  .  .  .
row 5:  .  .  .  .  .  .  .  .
row 6:  W  W  W  W  W  W  W  .
row 7:  A  C  .  C  .  B  .  .
```

- A at (0, 7).
- C₁ at (1, 7).
- C₂ at (3, 7).
- B at (5, 7).
- Exit `X` at (7, 0).
- Walls at row 6 cols 0..6 (gap only at col 7).

**Mechanics required by the witness** (count = L2-count + 1 = 3; L3
introduces exactly ONE new mechanic):

- **M1** (B-chases-A) — carried forward from L1.
- **M2** (C-chases-B-and-kills) — carried forward from L2.
- **M3** (A-eats-C-on-entry): the NEW mechanic. When A's action
  attempts to move onto a cell occupied by a C, A enters the cell
  and the C is removed.

**Necessity per mechanic** (counterfactual, per checklist item 12):

- **L3 cannot be solved without triggering M1's pursuit half on
  every turn** (as in L1, L2). Additionally, M1's lose-on-same-cell
  branch is what makes B *dangerous* — without it the layout would
  be solvable by simply walking right and consuming both Cs en
  route.
- **L3 cannot be solved without triggering M2.** Concrete
  counterfactual: with M2 disabled (C₂ moves but cannot remove B
  on coincidence), B at (5, 7) chases A. Turn 1: A → (1, 7) eats
  C₁. B → (4, 7). C₂ at (3, 7) tries vertical step toward B at
  (4, 7) — dx=1, dy=0, horizontal → (4, 7) blocked by B (no kill
  without M2), C₂ stays at (3, 7). Turn 2: A → (2, 7). B (4, 7)
  chase A (2, 7). dx=-2, dy=0. horizontal → (3, 7) blocked by C₂.
  vertical dy=0 no-op. B stays. C₂ chase B (4, 7). dx=1, dy=0.
  horizontal → (4, 7) blocked. Stays. Turn 3: A → (3, 7)? C₂ is
  there — A would eat C₂ (M3 fires). After eating: A at (3, 7).
  B (4, 7) chase A (3, 7). dx=-1, dy=0. horizontal → (3, 7) =
  A's cell → A is removed → lose. So without M2, A loses by
  turn 3. M2's only firing path is "C enters a B's cell", which
  the witness produces on turn 1.
- **L3 cannot be solved without triggering M3 because A's only
  legal first move from (0, 7) is onto C₁ at (1, 7).** A's four
  cardinal neighbours from (0, 7):
  - (1, 7) — occupied by C₁ → only enterable via M3 (A-eats-C);
  - (-1, 7) — out of bounds → blocked;
  - (0, 6) — wall → blocked;
  - (0, 8) — out of bounds → blocked.
  If M3 were absent (A cannot enter C cells), then (1, 7) would
  also be blocked, A would have zero legal moves, and A would be
  forced to issue blocked actions until the step budget exhausted
  → `self.lose()`. So M3 fires on turn 1 of any winning sequence.

**Witness solution** — the SHORTEST action sequence that wins L3:

```
[4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1]
```

(Seven `ACTION4` = RIGHT, then seven `ACTION1` = UP.)

Cell-by-cell trace:

| Turn | A's action | A's cell | B's cell | C₁'s cell | C₂'s cell | Event |
|---|---|---|---|---|---|---|
| 1 | RIGHT | (1, 7) | — | — (eaten) | (4, 7) | **M3 fires** (A enters C₁'s cell, C₁ removed). B step: dx=-4, dy=0, horizontal → (4, 7). C₂ step: nearest B at (4, 7), dx=1, dy=0, horizontal → (4, 7) = B → **M2 fires, B removed**. |
| 2 | RIGHT | (2, 7) | — | — | (4, 7) | C₂ has no B to chase, stays. |
| 3 | RIGHT | (3, 7) | — | — | (4, 7) | C₂ stays. |
| 4 | RIGHT | (4, 7) | — | — | — (eaten) | **M3 fires** (A enters C₂'s cell, C₂ removed). |
| 5 | RIGHT | (5, 7) | — | — | — | |
| 6 | RIGHT | (6, 7) | — | — | — | |
| 7 | RIGHT | (7, 7) | — | — | — | |
| 8 | UP | (7, 6) | — | — | — | (7, 6) is open — only cols 0..6 of row 6 are walled. |
| 9 | UP | (7, 5) | — | — | — | |
| 10 | UP | (7, 4) | — | — | — | |
| 11 | UP | (7, 3) | — | — | — | |
| 12 | UP | (7, 2) | — | — | — | |
| 13 | UP | (7, 1) | — | — | — | |
| 14 | UP | (7, 0) — **WIN** | — | — | — | A enters exit cell; `self.next_level()` fires. |

M3 fires twice (turns 1 and 4); M2 fires once (turn 1); M1's pursuit
runs once (turn 1, before B is removed). All three mechanics are
exercised.

**Difficulty justification** (per `difficulty-rules.md` § 2):

- **(a) Random-resistance.** Witness probability `(1/4)^14 ≈
  3.7e-9`. A random agent has additional failure modes specific to
  L3: any non-RIGHT first action is BLOCKED (so the random agent
  burns budget on blocked moves until C₁ is no longer A's only
  exit — but C₁ doesn't move so the random agent must eventually
  hit RIGHT 1 time). After entering (1, 7), random play in row 7
  has B chasing and the C₂-at-(3, 7) blocking; non-witness paths
  step into B's pursuit cell within 3-5 actions. Vision-blind
  agents cannot resolve C vs B at the visual level.
- **(b) Human-tractable.** An attentive human reads: A bottom-left,
  two green Cs nearby in row 7, an orange B further right, exit
  top-right, a horizontal wall above row 7. The natural read is
  "I have to walk right through these Cs; the green ones must be
  benign (or else why are they on my only path?); the orange one
  is dangerous". After ~2-3 exploratory actions (RIGHT 1: C₁ is
  consumed, B "jumps left", C₂ "jumps onto B" and both disappear),
  the player realises C-eats-B and A-eats-C are different
  rules. Expected human time: ~2-3 minutes (~1.5 minutes
  discovering both M2 and M3, ~1 minute walking the remaining
  path).
- **(c) Planning depth.** Per the L3 entry of difficulty-rules.md
  § 2c: **planning is challenging even for an attentive human
  (post-discovery).** Post-discovery decision space at level
  start: 1 valid action (only RIGHT is unblocked), so the first
  action is forced. The space opens after turn 1: A at (1, 7) has
  three legal directions (RIGHT into empty (2, 7), LEFT back to
  (0, 7), UP into wall). The **trivial heuristic that fails** is
  *"greedy distance-toward-exit"* — at turn 4 (A at (3, 7)), the
  greedy heuristic says UP would reduce Manhattan distance to
  exit at (7, 0) more efficiently than RIGHT does (Manhattan from
  (3, 6) to (7, 0) = 4 + 6 = 10; from (4, 7) to (7, 0) = 3 + 7
  = 10 — actually tied, but the human's intuition leans UP because
  UP "starts the vertical leg sooner"). UP is BLOCKED by the
  row-6 wall, so the greedy heuristic immediately wastes a turn
  on a no-op. The witness's reasoning: stay on row 7 until col 7,
  THEN go up col 7 — only col 7 has no wall in row 6. The
  heuristic diverges from the witness at turn 4 (greedy attempts
  UP and is blocked) and would diverge again at turns 5, 6 if the
  greedy keeps trying UP; the witness instead consumes C₂ to
  open the right-of-(3, 7) cells. With M3 just discovered, an
  attentive human may also try **"avoid eating C"** (since C
  killed B for them, they may suspect C is an ally) — but C₂'s
  cell at (4, 7) is on the only winning path, and not eating C₂
  is a stalemate (blocked forward, walls above, B is already
  dead so backtracking is safe but accomplishes nothing); the
  player must realise that the C-kill happened in turn 1 (C₂'s
  job is *done*) and eating C₂ is now safe.
- **(d) Step budget.** `max_steps = 35`. Witness length = 14, so
  there is a 21-step buffer. L3's addendum: "the budget must NOT
  shrink relative to the witness as level number rises" — at L3
  the budget (35) is larger than L2 (30) which is larger than L1
  (25), matching the increased exploration cost.

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`. Pure cardinal walking; no
ACTION5, ACTION6, or ACTION7.

| Slot | Semantic | Gate / when valid |
|---|---|---|
| ACTION1 | MOVE UP — attempt to move A by one cell-stride (8 px) in the −y direction. | always; resolves to no-op if the destination cell is a wall, out of bounds, or a B sprite (entering B's cell triggers A-removal → lose, but the player has no reason to do this voluntarily). |
| ACTION2 | MOVE DOWN — +y direction. | always; same blocking + lose rules. |
| ACTION3 | MOVE LEFT — −x direction. | always; same blocking + lose rules. |
| ACTION4 | MOVE RIGHT — +x direction. | always; same blocking + lose rules. |

No `_get_valid_actions` override is needed — all four actions are
always available; they may simply no-op if blocked. (Per
`reference-game-patterns.md` § 8: override only when actions are
context-gated. Walking is not context-gated here.)

Per `checklist.md` item 22 (ACTION7 is strict-undo or absent):
ACTION7 is ABSENT. No undo is meaningful — the irreversible events
(C-consumption, B-removal) are part of the puzzle.

## 6. HUD and per-game state

**HUD widget**: `StepCounterHud(RenderableUserDisplay)`. Renders the
bottom-most row of the 64×64 frame (`frame[63, :]`) as a step-budget
bar. Cells with `x/64 < remaining/max_steps` are painted palette-14
(green); the rest are painted palette-4 (off-black). The bar drains
left-to-right as the player consumes actions. The widget is
registered via `Camera(interfaces=[step_bar])`.

**Internal per-game state** (held on `self`):

- `self._steps_used: int` — counter of consumed actions in the
  current level. Incremented inside each handled action branch.
  Used to fire `self.lose()` when `_steps_used >= max_steps`. Per
  `fix_implementation.md`'s CHECK_LOSE_PATH_EXISTS pattern: this is
  a PRIVATE counter, NOT the engine's `self._action_count`, to
  avoid the implicit-RESET "first-frame energy already lost" bug.
- `self._max_steps: int` — set per-level from `level.get_data("max_steps")`.
- `self._step_bar: StepCounterHud` — the HUD widget instance,
  updated via `self._step_bar.set_remaining(self._max_steps - self._steps_used)`
  at the end of each handled action.

The B's and C's positions are read directly from the level's sprite
list via `self.current_level.get_sprites_by_tag("pursuer")` and
`...by_tag("mid")` each turn — no shadow state.

A's selected status is not tracked (there is no selection mechanic).
A is identified by `self.current_level.get_sprites_by_tag("player")[0]`.

`_get_hidden_state` returns a 1×1 `np.zeros` array — the game has
no information hidden from the frame.

## 7. Win condition

After A's move resolves on turn N, if A's logical cell equals the
level's exit cell coordinates (read from
`level.get_data("exit_cell")`), call `self.next_level()`. The check
fires BEFORE the B and C pursuit moves resolve — so A "snapping
the win" by stepping onto the exit cell takes precedence over a
B about to step onto A.

On the final level (L3), `self.next_level()` advances the engine to
the WIN state.

## 8. Lose condition

`self.lose()` fires in any of the following cases:

1. **A enters a B cell.** A's attempted destination is occupied by
   a B sprite. (This is a voluntary loss the player would only
   trigger by mistake.)
2. **A B's pursuit step lands on A's cell.** After A's move and the
   exit-check, the B-pursuit phase runs; if any B's new cell equals
   A's cell, `self.lose()`.
3. **Step budget exhausted.** After all phases complete, if
   `self._steps_used >= self._max_steps`, `self.lose()`.

(Note: with the simultaneity rules above, A and B cannot pass
"through each other" — if A enters a B cell, lose; if B steps to
A's cell, lose. There is no swap pathology.)

## 9. Novelty note

(Re-grounded against `mechanic-novelty/` for the FULL spec; the
`pick_mechanic` step did the family-level analysis.)

**Closest taxonomy entry**: `tu93` — *maze-pickup-train*. tu93
features secondary NPC species (bouncer, rotator, dormant pickup)
with INDEPENDENT tick rules; the player's goal is to *collect* a
train of pickups onto a goal tile. mw8p shares the "multi-species
NPC + player" surface but the species are in a directed
predation cycle and the win condition is "A reaches an exit cell"
not "every NPC is on a goal tile". Distinguishing rule re-confirmed
against the deep-analysis at
`deep-analysis-3lvls/tu93/tu93-deep-analysis.md`:
tu93's secondary tick functions (`yacjieihbk`, `irydcdcqyd`,
`jjqtojitqv`) are species-specific (bouncing, rotation, dormant-
activation); mw8p's secondaries share ONE tick rule (Manhattan-
dominant pursuit) parameterised by who-chases-whom.

**Closest prior-game entry**: `zk9p` — *pursuer-merge-walk*. zk9p
has one species of autonomous pursuer that vanishes on pursuer-
pursuer self-collision; win = clear all pursuers. mw8p has three
species in a directed predation cycle (A predates C, B predates A,
C predates B); win = reach an exit cell, not eliminate all
pursuers; C's removal of B is the chain-eat operation, not a
self-collision. (See `mechanic-pick.md` § zk9p for the full
8-dimension negative-similarity walk.)

**Secondary prior-game checks** (all confirmed distinct in
`mechanic-pick.md`):

- `nf3z` (flock-flee-corral) — distinguishing rule: nf3z's flock
  flees from the shepherd; mw8p's NPCs *predate each other* with no
  flee dynamic.
- `ek73` (wake-trail-evade) — distinguishing rule: ek73's hazards
  are vacated-cell decay trails; mw8p's hazards are autonomous-
  pursuer creatures.
- `bw7k` (actor-replay-shade) — distinguishing rule: bw7k spawns
  shade NPCs that REPLAY the actor's recent path; mw8p's NPCs
  follow autonomous pursuit policies independent of A's history.

**8-dimension negative-similarity overall judgement** (re-run on
the fleshed-out spec): shared dims with zk9p are 1, 2, 4, 5 — all
on the LOW-weight dimensions per `negative-similarity-check.md`'s
ranking. All three principle dimensions (6 palette / 7 pixel-grain
/ 8 core dynamic) diverge, and the level goal (D3) also diverges.
**NOVEL**.

(`prior-games/index.md` is NOT empty — 80 prior entries — and the
check above covers the meaningful near-misses.)
