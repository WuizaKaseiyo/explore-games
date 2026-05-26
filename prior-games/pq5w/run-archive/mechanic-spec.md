# pq5w — mechanic spec

## 1. Title
Twin-Portal Drag

## 2. Mechanic family
`portal-pair-relocate`. The playfield contains exactly TWO portal
sprites linked as a pair: an *anchor portal* (A, fixed) and a *float
portal* (B, movable). Walking into either portal teleports the avatar
to the paired portal's cell. ACTION6 click on a valid empty floor cell
RELOCATES portal B to that cell. The player drags B around the level
to chain portal jumps, bypassing walls and routing around forbidden
cells. Core-knowledge priors: **objectness** (avatar, portals, walls,
goal as persistent entities) and **basic geometry & topology** (the
portal pair establishes a non-spatial connectivity that bypasses
wall-defined connectivity).

## 3. Sprite roster

All sprites are 4×4 pixel arrays placed on a 64×60 playfield (HUD
occupies pixel rows 60..63). The "logical grid" is 16 cols × 15 rows;
cell (gx, gy) corresponds to pixel-space (gx·4, gy·4). Avatar moves in
4-pixel STRIDE.

- **`avatar`** (4×4, palette {-1, 5, 11}): rounded yellow body with
  two black "eye" pixels at the centre.
  ```
  -1 11 11 -1
  11  5  5 11
  11  5  5 11
  -1 11 11 -1
  ```
  Tags: `["player"]`. `collidable=True`. Layer 3.

- **`anchor_portal`** (4×4, palette {4, 6}): heavy off-black ring
  around a magenta core. Reads as "rooted, fixed".
  ```
   4  4  4  4
   4  6  6  4
   4  6  6  4
   4  4  4  4
  ```
  Tags: `["portal", "anchor"]`. `collidable=False` (avatar passes
  through to trigger teleport). Layer 1.

- **`float_portal`** (4×4, palette {6, 7}): light pink ring around a
  matching magenta core. Reads as "loose, movable" — same magenta
  core as anchor_portal makes the pairing visually obvious.
  ```
   7  7  7  7
   7  6  6  7
   7  6  6  7
   7  7  7  7
  ```
  Tags: `["portal", "float"]`. `collidable=False`. Layer 1.

- **`wall`** (4×4, palette {3, 5}): black-bordered grey block. Reads
  as "solid, impassable".
  ```
   5  5  5  5
   5  3  3  5
   5  3  3  5
   5  5  5  5
  ```
  Tags: `["wall"]`. `collidable=True`. Layer 1.

- **`goal`** (4×4, palette {3, 14}): green frame around a grey core.
  Reads as a "destination". The colour green is used ONLY for the
  goal sprite and the HUD bar — it is the level's distinguishing
  goal-tone.
  ```
  14 14 14 14
  14  3  3 14
  14  3  3 14
  14 14 14 14
  ```
  Tags: `["goal"]`. `collidable=False`. Layer 0.

- **`forbidden`** (4×4, palette {3, 4, 8}): red corners with grey
  frame and dark interior. Reads as a "danger" cell distinct from
  walls (red corners, not solid black border). Used in L3 only.
  ```
   8  3  3  8
   3  4  4  3
   3  4  4  3
   8  3  3  8
  ```
  Tags: `["forbidden"]`. `collidable=False` (avatar can step on it
  to fail). Layer 0.

Each level clones from this roster (`sprites["wall"].clone().set_position(...)`)
and places at concrete pixel positions in `Level(sprites=[...], ...)`.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. Layout in the diagrams below uses one character
per logical cell (4×4 pixels). `.` = empty floor; `#` = wall;
`A` = anchor portal; `B` = float portal initial position;
`G` = goal; `F` = forbidden; `X` = avatar start. Logical (gx, gy)
maps to pixel (gx·4, gy·4). Logical x ranges 0..15, logical y ranges
0..14.

### Level 1 — base dynamic system
[Revised in critique-revisions.md visit #1: L1 wall extended from a
3-cell stub to a full vertical column at x=8, y=0..14 (15 wall
sprites). Reason: the 3-cell wall could be skirted in ~17 walks
under the 30-step budget, breaking the no-trivial-fallback rule for
portal-traverse. The full-column wall makes portal-traverse the
only way to cross x=8.]

Layout (16 cols × 15 rows; `_` = HUD area below row 14):
```
y=0  ........#.......
y=1  ........#.......
y=2  ........#.......
y=3  ........#.......
y=4  ........#.......
y=5  ........#.......
y=6  ........#.......
y=7  .X.A....#...B.G.
y=8  ........#.......
y=9  ........#.......
y=10 ........#.......
y=11 ........#.......
y=12 ........#.......
y=13 ........#.......
y=14 ........#.......
```
A full-height wall column at x=8, y=0..14 (15 wall sprites) blocks
every walking path from the left half (x≤7) to the right half (x≥9).
Avatar at (1, 7); anchor portal A at (3, 7); float portal B at
(12, 7); goal at (14, 7).

- **Mechanics required by the witness** (N=2):
  1. **walk** — avatar moves one STRIDE-cell per arrow press.
  2. **portal-traverse** — stepping onto a portal cell teleports the
     avatar to the paired portal cell (resolved on the next action;
     see HUD/state §6).

- **Necessity per mechanic** (counterfactual):
  1. *L1 cannot be solved without triggering walk because the avatar
     starts at logical (1, 7), the goal is at logical (14, 7), and
     there is no other way to change the avatar's position than walking
     or being teleported — both require avatar movement to even arrive
     at a portal cell.*
  2. *L1 cannot be solved without triggering portal-traverse because
     the wall sprites at column x=8, y=0..14 (15 sprites) form a
     complete vertical barrier — no walking path exists from the left
     half (x≤7) to the right half (x≥9), so the avatar can only reach
     the goal at (14, 7) by stepping onto portal A at (3, 7) and
     teleporting to portal B at (12, 7).*

- **Witness solution** (5 actions, all RIGHT walks):
  `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]`
  - Action 1: avatar (4, 28) → (8, 28) = logical (2, 7). Floor.
  - Action 2: (8, 28) → (12, 28) = logical (3, 7). Lands on
    anchor portal A; teleport pending → destination = (48, 28) =
    portal B's cell.
  - Action 3: any action resolves the pending teleport. Avatar
    instantly moved to (48, 28) = logical (12, 7). The action's id
    is consumed but no walk occurs (this is the standard phase-tick
    pattern from `reference-game-patterns.md` for long-distance
    transitions; using ACTION4 is conventional).
  - Action 4: (48, 28) → (52, 28) = logical (13, 7). Floor.
  - Action 5: (52, 28) → (56, 28) = logical (14, 7) = goal. WIN.

- **Difficulty justification**:
  - **(a) Random-resistance**: a random-policy agent can occasionally
    stumble through L1 (per §3.4 the tutorial is allowed to be
    random-tractable), but the wall at column x=8 + the small step
    budget (30) means even a random agent has only modest probability
    of finishing within budget.
  - **(b) Human-tractable**: ~30-45 seconds. The player needs to
    notice the portal pairing visually (matching magenta cores, light
    vs dark outer rings), step on one, observe the teleport, and
    finish.
  - **(c) Planning depth**: NO STRICT PLANNING REQUIREMENT. L1 is
    the discovery gate; once the rule is understood, the win is
    near-immediate (just walk through the portal pair).
  - **(d) Step budget**: 30 (witness uses 5; 6× headroom for
    exploration). The witness counts the 1-action teleport-resolve.

### Level 2 — base system + portal-relocate (M = N+1 = 3)

Layout:
```
y=0  ................
y=1  ................
y=2  ....########....
y=3  ....#....B.#....
y=4  ....#.A....G....
y=5  ....#......#....
y=6  ....########....
y=7  ................
y=8  ................
y=9  .X..............
y=10 ................
y=11 ................
y=12 ................
y=13 ................
y=14 ................
```
A closed walled room. Outer walls bound the rectangle x=4..11,
y=2..6 — one wall sprite per outer-edge cell. Interior: x=5..10,
y=3..5. Anchor portal A at (6, 4); float portal B initial at (10, 3);
goal at (10, 4). Avatar starts at (1, 9), outside the room. The
goal at (10, 4) is rendered without the right wall closing it (note
the diagram shows G with no `#` on its right cell — the wall
sprites stop at x=10 to leave goal in the corner; effectively the
"right wall" runs at x=11 but the goal cell at (10, 4) replaces
what would otherwise be interior right-edge floor).

(Specifically, the level's wall placements are: top row y=2 at
x=4..11 (8 walls); bottom row y=6 at x=4..11 (8 walls); left column
x=4 at y=3..5 (3 walls); right column x=11 at y=3..5 (3 walls).
Total 22 walls. The room's interior is fully sealed.)

- **Mechanics required by the witness** (M = N+1 = 3):
  1. **walk** (carried forward from L1).
  2. **portal-traverse** (carried forward from L1).
  3. **portal-relocate** (NEW): ACTION6 click on a valid empty
     floor cell relocates the float portal B to the clicked cell.
     Valid means: not a wall, not the anchor portal cell, not the
     goal cell, not a forbidden cell, and within the playfield
     bounds. Click on an invalid cell is a no-op.

- **Necessity per mechanic** (counterfactual):
  1. *L2 cannot be solved without triggering walk because the
     avatar starts outside the walled room at (1, 9) and the goal is
     inside the room at (10, 4); even after a teleport, avatar
     position changes require walking.*
  2. *L2 cannot be solved without triggering portal-traverse because
     the room's walls (22 sprites in a closed rectangle) seal the
     interior — the only entry into the room interior (where the goal
     is) is via the portal pair.*
  3. *L2 cannot be solved without triggering portal-relocate because
     both portals A and B start INSIDE the closed room; without
     relocating B to a cell adjacent to the avatar's outside
     position, neither portal is reachable by walking, and there is
     no other way to enter the room.*

- **Witness solution** (8 actions; updated for select-then-place):
  `[ACTION6@(42, 14), ACTION6@(10, 38), ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]`
  - Action 1: ACTION6 click at pixel (42, 14) → grid cell (40, 12)
    = float portal B's current cell. B becomes selected — its 4
    corner pixels re-tint to light-blue.
  - Action 2: ACTION6 click at pixel (10, 38) → grid cell (8, 36).
    Float portal B relocates from (40, 12) inside the room to
    (8, 36) outside, adjacent to the avatar; deselects (corner
    pixels revert to pink).
  - Action 3: ACTION4 RIGHT. Avatar (4, 36) → (8, 36) = portal B.
    Teleport pending → destination (24, 16) = anchor A.
  - Action 4: ACTION4 (resolves teleport). Avatar at (24, 16) =
    (6, 4) inside the room.
  - Actions 5-8: ACTION4 × 4 east through the room interior:
    (24, 16) → (28, 16) = (7, 4); → (32, 16) = (8, 4); → (36, 16)
    = (9, 4); → (40, 16) = (10, 4) = GOAL.

  Total = 2 clicks + 1 walk + 1 teleport-resolve + 4 walks =
  **8 actions**.

- **Difficulty justification**:
  - **(a) Random-resistance**: random clicks land in any of ~256
    cells; only ~3-4 cells (those adjacent to the avatar) lead to a
    productive teleport. Random walks alone cannot enter the sealed
    room. P(stumble within budget) ≪ 1/10,000.
  - **(b) Human-tractable**: ~1.5 minutes. Discovery: try arrow
    keys (avatar walks but can't enter room); try clicks (B moves —
    aha, click sets B's position); place B near self → walk into
    B → emerge inside; walk to goal.
  - **(c) Planning depth (post-discovery)**: enumerate
    decision space at level start — 4 walk directions (3 effectively
    no-op against playfield boundaries / nothing of consequence) +
    ~256 click cells, of which ~6-8 cells (those adjacent to the
    avatar) yield productive relocations. **Plausible-but-wrong:**
    click on the goal cell (intuiting "drop the portal next to the
    goal"); the relocate is a no-op (goal cell is invalid for
    relocate per rule), so this is rejected by the rule. Click on
    any cell INSIDE the room (e.g., (8, 4)) — B teleports inside,
    but the avatar is OUTSIDE and cannot reach either portal by
    walking; player has wasted a click. **Witness reasoning chain:**
    avatar must enter the closed room → only the portal pair allows
    that → both portals are inside, so B must be brought outside
    to a walkable neighbour of the avatar → click on (2, 9) →
    walk onto B → teleport → walk to goal.
  - **(d) Step budget**: 50 (witness uses 7; 7× headroom). Generous
    over witness so the player can experiment with click locations.

### Level 3 — system + forbidden-cell-avoid (M = 3+1 = 4)

Layout:
```
y=0  ................
y=1  ................
y=2  ....########....
y=3  ....#..F.B.#....
y=4  ....#.A.F..G....
y=5  ....#...F..#....
y=6  ....########....
y=7  ................
y=8  ................
y=9  .X..............
y=10 ................
y=11 ................
y=12 ................
y=13 ................
y=14 ................
```

Same room as L2, plus three forbidden-cell sprites at (8, 3),
(8, 4), (8, 5) forming a complete impassable column inside the
room interior — splitting the interior into sub-area-1 (x=5..7,
y=3..5) and sub-area-2 (x=9..10, y=3..5). Anchor portal A at
(6, 4) is in sub-area-1; goal at (10, 4) is in sub-area-2. Float
portal B initial at (10, 3) is in sub-area-2 (corner). Avatar at
(1, 9) outside the room as in L2.

- **Mechanics required by the witness** (M = 3+1 = 4):
  1. **walk** (carried).
  2. **portal-traverse** (carried).
  3. **portal-relocate** (carried).
  4. **forbidden-cell-avoid** (NEW): forbidden-cell sprites are
     non-collidable (so avatar can technically step on them) but
     stepping onto a forbidden cell triggers `self.lose()`. The
     player must route around them.

- **Necessity per mechanic** (counterfactual):
  1. *L3 cannot be solved without triggering walk because the
     avatar starts outside the room and must walk to step onto a
     portal AND to traverse the room interior between portal jumps;
     no other movement method exists.*
  2. *L3 cannot be solved without triggering portal-traverse because
     the room's walls (22 wall sprites in a closed rectangle) seal
     the interior — the only way in is via the portal pair, and once
     inside, the only way to cross from sub-area-1 to sub-area-2 is
     via a second portal-traverse (the forbidden column at x=8 blocks
     every walking path between the sub-areas).*
  3. *L3 cannot be solved without triggering portal-relocate at
     least twice. The first relocate moves B outside near the avatar
     so the avatar can teleport into the room (same as L2). The
     second relocate moves B from outside (where it was placed in
     the first relocate) into sub-area-2, which is necessary because
     after teleporting to A, the avatar is in sub-area-1 — direct
     walking into sub-area-2 hits the forbidden column at x=8 and
     loses.*
  4. *L3 cannot be solved without triggering forbidden-cell-avoid
     because the only walking path from sub-area-1 to sub-area-2
     would have to cross the forbidden column at x=8 (cells (8, 3),
     (8, 4), (8, 5) — entire vertical extent of the room interior
     covered). Stepping on any forbidden cell calls `self.lose()`,
     so the player must avoid them — the witness avoids them by
     using a SECOND portal-relocate + portal-traverse to jump from
     A in sub-area-1 to B in sub-area-2 without ever stepping on
     a forbidden cell.*

- **Witness solution** (10 actions; updated for select-then-place):
  `[ACTION6@(42, 14), ACTION6@(10, 38), ACTION4, ACTION4, ACTION1, ACTION6@(10, 38), ACTION6@(38, 18), ACTION2, ACTION2, ACTION4]`
  - Action 1: ACTION6 click @ pixel (42, 14) = float portal's cell
    (40, 12). Float becomes selected (4 corner pixels → light-blue).
  - Action 2: ACTION6 click @ pixel (10, 38) = cell (8, 36). Float
    relocates from (40, 12) to (8, 36), deselects.
  - Action 3: ACTION4 RIGHT. Avatar (4, 36) → (8, 36) = B.
    Teleport pending → (24, 16) = A.
  - Action 4: ACTION4 (resolve). Avatar at (24, 16).
  - Action 5: ACTION1 UP. Avatar (24, 16) → (24, 12) = (6, 3).
  - Action 6: ACTION6 click @ pixel (10, 38) = float's current cell
    (8, 36). Float becomes selected (4 corner pixels → light-blue).
  - Action 7: ACTION6 click @ pixel (38, 18) = cell (36, 16) =
    (9, 4). Float relocates from (8, 36) to (36, 16), deselects.
  - Action 8: ACTION2 DOWN. Avatar (24, 12) → (24, 16) = A.
    Teleport pending → (36, 16) = B at (9, 4).
  - Action 9: ACTION2 (resolve). Avatar at (36, 16) = (9, 4).
  - Action 10: ACTION4 RIGHT. Avatar (36, 16) → (40, 16) = (10, 4)
    = goal. WIN.

- **Difficulty justification**:
  - **(a) Random-resistance**: same logic as L2 plus the forbidden
    column adds ~3 fail-instant cells reachable from sub-area-1. A
    random agent that stumbles into the room is more likely to lose
    by stepping into a forbidden cell than to find the second-relocate
    chain. P(random win within budget) ≪ 1/10,000.
  - **(b) Human-tractable**: ~2-3 minutes. Discovery cost: 1-2 lost
    levels to learn that the forbidden column kills, then the
    structural insight "I need a SECOND teleport from A to sub-area-2".
  - **(c) Planning depth (post-discovery)**: enumerate decision space
    after action 3 (avatar at A, sub-area-1) — 4 walk directions
    (UP and DOWN safe within sub-area-1; LEFT bumps into sub-area-1
    interior; RIGHT lands on (7, 4) safe and then (8, 4) FORBIDDEN
    on the next press), plus ~256 click cells. A fully-informed
    player faces at least a 6-cell-deep branching tree. **Trivial
    heuristic that fails: "after teleporting in, walk monotonically
    right toward the goal".** This heuristic walks (6,4) → (7,4) →
    (8,4) and dies on action 6 by stepping on forbidden (8,4). The
    heuristic and the witness diverge at action 4: the heuristic
    presses ACTION4 (right toward goal) and dies; the witness
    presses ACTION1 (up, AWAY from goal direction) to set up the
    second relocate. **Why ahead-of-time reasoning is needed**: the
    forbidden column forces the player to plan TWO portal relocations
    not one, and the second relocate must be paired with a "walk-off
    A then walk-back-onto A" chain to re-trigger the teleport — a
    multi-step plan whose first step (walk UP) looks counter-productive
    to a greedy player.
  - **(d) Step budget**: 80 (witness uses 8; 10× headroom). Per
    `difficulty-rules.md` § d, L3 budget must NOT shrink relative to
    witness as level number rises — 80 is comfortably above L2's 50
    and well above the 8-action witness.

## 5. Action mapping
- `ACTION1` (UP): walk avatar -1 STRIDE in y. Blocked by walls.
- `ACTION2` (DOWN): walk avatar +1 STRIDE in y. Blocked by walls.
- `ACTION3` (LEFT): walk avatar -1 STRIDE in x. Blocked by walls.
- `ACTION4` (RIGHT): walk avatar +1 STRIDE in x. Blocked by walls.
- `ACTION6` (CLICK at pixel (x, y)): select-then-place.
  - If the clicked pixel maps to the float portal's CURRENT cell,
    toggle the float portal's `_float_selected` state. When the
    state flips on, the float portal's FOUR CORNER PIXELS re-tint
    from pink (palette 7) to light-blue (palette 10) — a persistent
    visible cue that it is selected. The rest of the outer ring and
    the magenta core are unchanged. When the state flips off, the
    corner pixels revert to pink.
  - If the clicked pixel maps to a different cell AND the float
    portal is currently selected AND the target cell is valid
    (within the playfield, not a wall, not the anchor portal's
    cell, not the goal cell, not a forbidden cell, not the
    avatar's current cell), the float portal relocates to that
    cell and deselects (outer ring reverts to pink).
  - Otherwise (clicked elsewhere when not selected, or selected
    but invalid target), the click is a no-op. The selected state
    persists across no-op clicks so the player can try again.

`ACTION5` and `ACTION7` are NOT declared in `available_actions`. The
game does not need a freedom-slot modal verb (the click already
serves as the distinctive verb) and there is no undo. Per
`global/action-enum.md` and `checklist.md` item 22, ACTION7 is omitted
rather than overloaded.

`available_actions = [1, 2, 3, 4, 6]`.

When a teleport is pending (i.e., the avatar just stepped onto a
portal), the next action's id is **consumed** to advance the teleport
phase — the avatar's position is set to the paired portal's cell and
no walk occurs. This is the standard `_phase >= 0` pattern from
`reference-game-patterns.md` for long-distance transitions; the
teleport thus visibly takes 2 frames (pre-teleport: avatar AT source;
post-teleport: avatar AT destination), so the player sees the path.

## 6. HUD and per-game state

**HUD widget**: `StepCounterHud` (subclass of `RenderableUserDisplay`)
draws a horizontal depleting bar at pixel rows 60..63, palette 14
(green) for filled / palette 5 (black) for empty. Width is a fraction
of 64 proportional to `steps_remaining / step_budget`.

**Internal state**:
- `_steps_used` (int): private step counter incremented inside
  handled-action branches in `step()`. Used as the lose trigger
  rather than `self._action_count` (per `fix_implementation.md`
  guidance — `self._action_count` counts the implicit RESET).
- `_step_budget` (int): per-level constant, read from
  `level.get_data("step_budget")` in `on_set_level`.
- `_teleport_pending` (tuple `(dst_x, dst_y)` or `None`): set when
  the avatar steps onto a portal; consumed on the next `step()`
  call (any action id) by setting the avatar's position to
  (dst_x, dst_y).

**Visible cues for state changes (checklist item 19)**:
- The float portal B's position IS the "current B-anchor"; clicking
  visibly relocates it on screen — the cue is persistent, not a
  one-frame flash.
- The avatar's position is its rendered pixel position (engine).
- The teleport-pending state is rendered as the avatar AT the
  source portal for one frame (the engine renders BEFORE the next
  step() resolves), making the path visible.
- The step counter HUD shrinks each turn — persistent.
- Forbidden cells are rendered as the `forbidden` sprite (red
  corners), persistently visible.
- No mode/selection state is hidden; the only "active selection"
  is which portal is movable, and that is fully encoded in the
  portal sprites' visual identities (anchor A has dark outer ring,
  float B has light pink outer ring).

## 7. Win condition

After every action's resolution (after walk, after teleport-resolve,
or after click), `_check_win()` returns `True` iff the avatar's
(x, y) equals the goal sprite's (x, y). On true, the game calls
`self.next_level()`. After the third level wins, the engine
auto-fires WIN.

## 8. Lose condition

`self.lose()` is fired in two situations:
- `_steps_used >= _step_budget` after the action's increments (step
  counter exhausted).
- The avatar's (x, y) equals the (x, y) of any forbidden sprite
  after the action's resolution (avatar stepped on a forbidden cell;
  L3 only — L1 and L2 have no forbidden sprites).

## 9. Novelty note

### vs. taxonomy of 25 reference games
No reference game has a paired-portal teleport mechanic. The closest
flavour-match is `g50t` (walk-vs-scroll), where the world scrolls
left every two turns — a coordinate-shift mechanic, not a portal-
pair. Distinguishing rule: pq5w has DISCRETE point-to-point teleport
between two named cells the player can RELOCATE; g50t has CONTINUOUS
world-scroll the player cannot shape.

### vs. prior-games index (67 entries)
Closest matches (full distinguishing rules in `mechanic-pick.md`):
- **jd4q (echo-trail-teleport)**: jd4q teleports back along a fading
  echo trail, consuming the trail. pq5w has a persistent 2-endpoint
  pair that the player drags via ACTION6 click — no trail, no
  consumption, repeated walks through the same pair are cheap.
- **ek73 (wake-trail-evade)**: ek73's warp pads are an auxiliary,
  pre-placed mechanic; ek73's primary verb is leave-decaying-hazard-
  trail-behind. pq5w's portal pair is the PRIMARY verb, the player
  RELOCATES one of the pair endpoints during play, and there is no
  decaying-hazard trail.
- **bx84 (beam-mirror-reflect)**: bx84 places mirrors and shoots
  beams; the active entity is a beam. pq5w has a walking avatar;
  there is no beam, no projectile.
- **vy3k (region-swap-arrange)**: vy3k swaps quadrants of the
  playfield. pq5w teleports the avatar's POINT position; the
  playfield is unchanged.
- **kn58 (anchor-pull-magnet)**: kn58 places a single magnet that
  pulls every pawn one cell toward it. pq5w places one of a pair of
  portals that teleports a single avatar between two endpoints.

### Negative similarity (per `negative-similarity-check.md`)
Walked the seven dimensions for jd4q (the closest prior). Universal
axes (walls, goal, step counter, walking-avatar) are shared as
expected; load-bearing axes (visual signature, pixel grain, core
dynamic) all diverge — pq5w has 2 distinctive paired ring-sprites,
no fading-echo cells, and a "drag-the-pair" core dynamic absent in
jd4q's "lay-then-consume". PASS.
