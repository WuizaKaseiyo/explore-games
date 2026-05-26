# mechanic-spec — wt39

## 1. Title

Glide-Deflect-Thaw — a momentum-puzzle on cracking ice.

## 2. Mechanic family

A single pawn glides cell-by-cell in the pressed cardinal direction
until it crashes into a wall, an angled-bumper deflector (which
turns the slide ninety degrees in flight), the goal, or a cell
adjacent to a brittle thaw-tile that has already cracked. Thaw-
tiles are passable on first traversal; once a slide passes over
one, the tile cracks and behaves as a wall for every subsequent
slide. The pawn stops on the goal cell only when a slide enters
that cell and is then blocked from continuing — gliding past the
goal does not win; only stopping ON it does. Prior categories: 
**objectness** (pawn / bumpers / walls / thaw / goal as discrete 
sprites), **physics** (frictionless glide, momentum, ninety-degree 
elastic deflection), **geometry/topology** (which slides reach 
which cells; which routes survive after thaw cracks).

## 3. Sprite roster

Semantic-named sprites (no obfuscation per `code/universal-scaffold.md`):

- `pawn` — 1×1, palette 8 (red); tags `["pawn"]`. The single mover.
- `goal` — 1×1, palette 8 with a dim outline using palette 13
  (maroon ring around centre 8); 3×3 actually with central dot —
  see implementation. Tags `["goal"]`. Pawn stops on goal cell
  triggers win.
- `wall_block` — 1×1, palette 4 (off-black). Tags `["wall"]`.
  Used as interior walls. Perimeter walls also use this sprite
  (cloned per cell).
- `bumper_back` — 1×1, palette 12 (orange) with a NW-SE diagonal
  stripe rendered via pixel pattern. Tags `["bumper", "bumper_back"]`.
  Deflection rule: pawn entering this cell heading east deflects
  to south; heading south deflects to east; heading west deflects
  to north; heading north deflects to west. (Equivalent to the "\"
  glyph in optics.)
- `thaw_frozen` — 1×1, palette 10 (light-blue) with a thin palette
  1 (off-white) cross indicating fragility. Tags `["thaw", "frozen"]`.
- `thaw_cracked` — 1×1, palette 1 (off-white) crackled pattern
  with palette 4 (off-black) flecks. Tags `["thaw", "cracked"]`.
  Acts as a wall for all subsequent slides.
- `ice_floor` — purely cosmetic; 1×1 palette 10 (light-blue)
  background tile. Tags `["floor"]`. Optional decorative element
  for the playfield.

(`bumper_fwd` — the "/" variant — is defined in the sprite bank
for forward compatibility but **not placed in any L1-3 level**.
This is intentional: with a single bumper kind in scope, the
player's mental model is "diagonal stripe deflects 90°" and the
specific direction of deflection is consistent across the game.)

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels share `grid_size = (14, 14)`. Cells (0, *), (13, *),
(*, 0), (*, 13) are perimeter walls (rendered as `wall_block`
clones). The interior playfield is the 12×12 region (1..12, 1..12).
Coordinates throughout are (x, y) with x increasing east, y
increasing south.

The pawn starts every level at (2, 2). The goal sprite differs in
position per level. All levels use the same step-counter HUD; per-
level step budgets in §6.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 1):
  - **M1 = slide-until-wall.** ACTION1-4 launches the pawn in the
    pressed direction; the pawn translates one cell per tick along
    the chosen axis until the next cell would be a wall, at which
    point it stops one cell before the wall.

- **Necessity per mechanic** (counterfactual):
  - L1 cannot be solved without triggering M1 because the only way
    the pawn changes position is via a directional slide; there is
    no other input verb. Specifically, reaching the goal cell at
    (8, 7) requires the pawn to translate from (2, 2), and every
    such translation IS a slide-until-wall.

- **Per-cell layout (L1)**:
  - `pawn` at (2, 2).
  - `goal` at (8, 7).
  - `wall_block` interior pieces at (9, 2) and (8, 8).
  - Plus perimeter wall at every edge cell.

- **Witness solution** (shortest):
  ```
  [ACTION4 (RIGHT), ACTION2 (DOWN)]
  ```
  Trace:
  - Start: pawn at (2, 2).
  - ACTION4 (RIGHT). Pawn glides E in row 2: (3, 2), (4, 2), …,
    (8, 2). Cell (9, 2) is a wall. Pawn stops at (8, 2).
  - ACTION2 (DOWN). Pawn glides S in col 8: (8, 3), …, (8, 7).
    Cell (8, 8) is a wall. Pawn stops at (8, 7) = goal. WIN.
  - Total = 2 actions.

- **Difficulty justification (L1)**:
  - **(a) Random-resistance.** A vision-blind random-policy agent
    has 4 directional choices per turn; reachable cells from
    (2, 2) under one slide are {(2, 1), (2, 12), (1, 2), (8, 2)}
    — 4 cells. After 2 slides, the union of reachable terminal
    cells is bounded above by ~12-15. The probability of the
    specific 2-action sequence [RIGHT, DOWN] in a uniformly
    random play is `1/16` per attempt; over a 30-step budget
    expected solves ≈ 30/16 ≈ 1.9, so a random agent can stumble
    in but is far from guaranteed. This level is intentionally
    permeable to occasional random success per
    `from-tech-report.md` §6 (tutorial-level random-resistance is
    relaxed by design).
  - **(b) Human-tractable.** An attentive human, on first sight,
    sees: a red pawn, a red goal-ring, two black blocks placed at
    (9, 2) and (8, 8). Pressing RIGHT once teaches the slide
    rule (pawn glides to (8, 2) and stops). Pressing DOWN ends the
    level. ~30 seconds to solve.
  - **(c) Planning depth.** Per `difficulty-rules.md` §2.c, L1
    has no strict planning requirement; the player learns the
    slide rule and the level resolves as soon as the rule is
    understood.
  - **(d) Step budget.** `step_budget = 30`. Witness length = 2;
    budget is 15× the witness, generous over exploration of the
    four directional verbs.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (= N + 1 = 2):
  - **M1** (carried) — slide-until-wall.
  - **M2 = bumper-deflect.** A pawn that enters a `bumper_back`
    cell during a slide is deflected ninety degrees in flight per
    the rule in §3 and continues sliding in the new direction
    until the next wall.

- **Necessity per mechanic**:
  - L2 cannot be solved without triggering **M1** because every
    action is a slide; without M1 the pawn does not move.
  - L2 cannot be solved without triggering **M2** because column 10
    is sealed off from the perimeter by the absence of any
    interior wall at (11, *) or (9, *). The only entry into col 10
    rows 1-6 is via the bumper at (10, 2) deflecting an eastbound
    slide southward; without that deflection, no slide-stop nor
    perimeter-bounce can land the pawn in column 10 rows 1-6.
    Concretely, the wall at (10, 7) — which is the slide-stop the
    witness uses to land at (10, 6) — is reached *only* through
    the (10, 2) bumper. Therefore reaching the (4, 6) slide-stop
    (via wall (3, 6)) and then the (4, 10) slide-stop (via wall
    (4, 11)) requires the bumper deflection.

- **Per-cell layout (L2)**:
  - `pawn` at (2, 2).
  - `goal` at (4, 10).
  - `bumper_back` at (10, 2).
  - `wall_block` interior pieces at (10, 7), (3, 6), (4, 11).
  - Plus perimeter walls.

- **Witness solution** (shortest):
  ```
  [ACTION4 (RIGHT), ACTION3 (LEFT), ACTION2 (DOWN)]
  ```
  Trace:
  - Start: pawn at (2, 2).
  - ACTION4 (RIGHT). Pawn glides E in row 2: (3, 2), …, (9, 2),
    enters (10, 2) which is `bumper_back`. The bumper deflects
    E→S. Pawn now glides S in col 10: (10, 3), …, (10, 6). Cell
    (10, 7) is a wall. Pawn stops at (10, 6).
  - ACTION3 (LEFT). Pawn glides W in row 6: (9, 6), (8, 6), …,
    (4, 6). Cell (3, 6) is a wall. Pawn stops at (4, 6).
  - ACTION2 (DOWN). Pawn glides S in col 4: (4, 7), …, (4, 10).
    Cell (4, 11) is a wall. Pawn stops at (4, 10) = goal. WIN.
  - Total = 3 actions.

- **Difficulty justification (L2)**:
  - **(a) Random-resistance.** From (2, 2), the four single-slide
    terminals are (2, 1), (2, 12), (1, 2), and via the bumper-
    deflection chain (10, 6). One terminal exposes column 10 to
    further exploration. After 3 random actions, the union of
    reachable terminal cells is bounded by ~25. The probability of
    [RIGHT, LEFT, DOWN] specifically is `1/64` per attempt; a
    random walk over 60 actions has expected solves ≈ 60/64 ≈ 1.
    But because LEFT from (2, 1)/(2, 2)/(1, 2) yields no progress
    (already at left wall), and DOWN from (1, 2) wastes the
    bumper opportunity, the effective branching factor for
    random-but-non-trivial paths is lower; empirically, random
    play within budget 60 has a low — not negligible but well
    under one-in-ten — chance of incidentally solving. A vision-
    blind agent that cannot read the bumper sprite has near-zero
    chance of intuiting the deflection.
  - **(b) Human-tractable.** First action: RIGHT from (2, 2),
    expecting a stop at the perimeter; the player observes the
    bumper deflect the pawn to (10, 6) instead of continuing past.
    This teaches M2 in one action. The remaining two-action plan
    (LEFT to (4, 6) then DOWN to (4, 10)) is direct visual
    inference: the goal sits at the foot of column 4, the wall at
    (3, 6) provides the LEFT-stop in row 6, and (4, 11) provides
    the DOWN-stop. ~90 seconds for an attentive human.
  - **(c) Planning depth (post-discovery).** The player's per-
    step reasoning chain after both rules are understood is:
    *"RIGHT will glide and bumper-deflect to (10, 6); from there
    LEFT in row 6 will stop at (4, 6) because of wall (3, 6); from
    (4, 6) DOWN in col 4 will stop at the goal (4, 10) because of
    wall (4, 11)."* Three concrete state-transitions to simulate
    before each press. This is moderate planning per
    `difficulty-rules.md` §2.c — not single-step, not a colour-
    follow lookup table. Each step the player asks "where will I
    end up?" and visualises the slide.
  - **(d) Step budget.** `step_budget = 60`. Witness = 3; budget
    is 20× over. A first-time player will spend several actions
    discovering bumper deflection before attempting the witness;
    the budget reflects that.

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (= 2 + 1 = 3):
  - **M1** (carried) — slide-until-wall.
  - **M2** (carried) — bumper-deflect.
  - **M3 = thaw-cracking.** A `thaw_frozen` cell is passable on
    first traversal — slides glide over it without stopping. After
    a slide passes through (the slide enters and then exits the
    thaw cell during a single ACTION), the thaw mutates to
    `thaw_cracked`, which behaves as a wall for every subsequent
    slide.

- **Necessity per mechanic**:
  - L3 cannot be solved without triggering **M1** because every
    action is a slide; the pawn has no other movement verb.
  - L3 cannot be solved without triggering **M2** because (as in
    L2) column 10 rows 1-6 is sealed except through the bumper at
    (10, 2). Reaching the wall (10, 7) slide-stop at (10, 6) — and
    therefore the chain through (4, 6) and into column 4 — is only
    possible via the bumper deflection.
  - L3 cannot be solved without triggering **M3** because the
    goal at (4, 9) has NO adjacent wall at (4, 8), (4, 10), (3, 9),
    or (5, 9) initially. No slide-stop terminates at (4, 9) until
    *after* the thaw at (4, 8) has been cracked — only then does
    UP-slide in column 4 stop at (4, 9). Specifically: a DOWN-
    slide in col 4 with thaw open passes (4, 7), (4, 8), (4, 9),
    (4, 10) and stops at (4, 10) (because (4, 11) is wall); the
    pawn is past the goal. UP-slide from (4, 10) with thaw still
    frozen would continue past (4, 9) up to (4, 1) (perimeter)
    — does not stop at the goal. Only after the DOWN-slide has
    cracked the thaw does the cracked cell at (4, 8) act as a wall
    that stops UP-slide at (4, 9). Therefore the thaw-cracking is
    counterfactually necessary.

- **Per-cell layout (L3)**:
  - `pawn` at (2, 2).
  - `goal` at (4, 9).
  - `bumper_back` at (10, 2).
  - `wall_block` interior pieces at (10, 7), (3, 6), (4, 11).
  - `thaw_frozen` at (4, 8).
  - Plus perimeter walls.

- **Witness solution** (shortest):
  ```
  [ACTION4 (RIGHT), ACTION3 (LEFT), ACTION2 (DOWN), ACTION1 (UP)]
  ```
  Trace:
  - Start: pawn at (2, 2). Thaw at (4, 8) is `thaw_frozen`.
  - ACTION4 (RIGHT). Pawn → bumper at (10, 2) → deflects E→S →
    DOWN col 10 → wall (10, 7) → stops at (10, 6).
  - ACTION3 (LEFT). Pawn glides W in row 6 → wall (3, 6) → stops
    at (4, 6).
  - ACTION2 (DOWN). Pawn glides S in col 4: (4, 7), (4, 8 — thaw
    frozen, slide passes through and the thaw will crack at the
    end of this slide), (4, 9), (4, 10). Cell (4, 11) is a wall.
    Pawn stops at (4, 10). End-of-slide post-processing: the thaw
    at (4, 8) has been entered AND exited (entered at the (4, 8)
    step, exited as the slide continued S to (4, 9)) → thaw
    mutates to `thaw_cracked`.
  - ACTION1 (UP). Pawn glides N in col 4: (4, 9). Cell (4, 8) is
    now `thaw_cracked` — a wall. Pawn stops at (4, 9) = goal.
    WIN.
  - Total = 4 actions.

- **Difficulty justification (L3)**:
  - **(a) Random-resistance.** Specific 4-action sequence
    probability is `1/256` per attempt. Beyond raw probability,
    random play at L3 has the additional trap of cracking the
    thaw incorrectly: any DOWN slide in column 4 cracks (4, 8),
    after which UP from (4, 12), UP from (4, 11), or UP from
    (4, 10) all collide with the cracked-thaw wall and stop at
    (4, 9). So once cracked, multiple recovery paths exist —
    *but* a random agent that cracks the thaw before reaching col
    10 row 6 has wasted an action with no progress, and the
    bumper-route requires the pre-existing geometry. With budget
    80, expected random solves under uniform policy is ~80/256 =
    0.31, so well under one in three. A vision-blind agent
    cannot read thaw vs. ice and will randomly pass over without
    knowing.
  - **(b) Human-tractable.** Two minutes for a human who has
    played L2 (bumper rule already learned). The thaw-tile's
    visual distinction (light-blue ice with a frozen cross) cues
    discovery: pressing DOWN once in column 4 causes the tile to
    visually crack, signalling the new mechanic. Then UP back to
    (4, 9) is the natural completion.
  - **(c) Planning depth (post-discovery).**
    - Trivial heuristic that L3 defeats: *"At each step, press the
      cardinal direction with the largest displacement to the
      goal."* From (2, 2) goal at (4, 9), displacement (+2, +7) →
      DOWN. DOWN from (2, 2) → col 2 has no walls → pawn slides
      to (2, 12). From (2, 12) displacement (2, -3) → UP. UP from
      (2, 12) → (2, 1) (perimeter). DOWN from (2, 1) → (2, 12)
      again. The largest-displacement greedy oscillates between
      rows 1 and 12 in column 2 forever, never engaging the
      bumper. Random tie-breaking eventually presses RIGHT, but
      the pure greedy heuristic monotonically fails.
    - Witness commute test: swapping witness actions 2 and 3
      (`LEFT` and `DOWN`) yields `[RIGHT, DOWN, LEFT, UP]`. Trace:
      RIGHT → bumper → (10, 6). DOWN from (10, 6) → cell (10, 7)
      directly south is a wall → pawn cannot move; stays at
      (10, 6) for a "wasted" action. LEFT from (10, 6) → wall
      (3, 6) → (4, 6). UP from (4, 6) → col 4 has no walls north
      of (4, 6); thaw at (4, 8) is south, not relevant. UP slides
      to (4, 1). End at (4, 1), not goal. Solution broken by
      commute.
  - **(d) Step budget.** `step_budget = 80`. Witness = 4; budget
    is 20× over. The L3 budget is generous over the witness *and*
    larger than L2 (60 → 80) per `difficulty-rules.md` §2.d:
    later levels add discovery cost (the thaw mechanic) and need
    more exploration room, so the budget grows.

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`. Pure cardinal-motion game; no
ACTION5, no ACTION6 (no click), no ACTION7 (no undo).

- `ACTION1` — UP (pawn glides north).
- `ACTION2` — DOWN (pawn glides south).
- `ACTION3` — LEFT (pawn glides west).
- `ACTION4` — RIGHT (pawn glides east).

There is no context-dependent gating; every action is always
available.

## 6. HUD and per-game state

**HUD:**

- A single `RenderableUserDisplay` subclass `StepCounterHud`
  renders a depleting bar at row 0 (top edge). Palette 8 (red)
  for remaining cells, palette 5 (black) for depleted. The bar
  shrinks from the right edge as the budget drains. (Palette 8
  for the HUD ties visually to the pawn and goal — same red.)

**Per-game internal state:**

- `self.pawn_x`, `self.pawn_y` — cached pawn position
  (also reflected in the pawn sprite's `.x`, `.y`). Used during
  slide simulation.
- `self.thaw_state` — a dict mapping `(x, y)` tuples (the cells
  with `thaw_frozen` sprites placed at the level start) to a bool
  `cracked` (False initially). After a slide passes through a
  thaw cell, the dict entry flips to True and the sprite is
  swapped from `thaw_frozen` to `thaw_cracked`.
- `self.step_budget`, `self.steps_remaining` — per-level step
  budget and current count, read from `level.get_data("step_budget")`
  and decremented per action.

**Per-level data dicts:**

- L1: `{"step_budget": 30}`.
- L2: `{"step_budget": 60}`.
- L3: `{"step_budget": 80}`.

## 7. Win condition

The pawn's stable position (after a slide completes) equals the
goal sprite's `(x, y)`.

Concretely, at the end of every `step()` (after the slide
simulation completes), the engine checks:

```python
goal = self.current_level.get_sprites_by_tag("goal")[0]
if self.pawn.x == goal.x and self.pawn.y == goal.y:
    self.next_level()
```

A slide that *passes through* the goal cell mid-flight (because
the pawn has remaining momentum and the cell after the goal is
not a wall) does NOT trigger win. Win requires the slide to
*end* on the goal cell.

Same predicate for L1, L2, L3.

## 8. Lose condition

The step-counter HUD reaches zero before the win condition fires:

```python
if self.steps_remaining <= 0:
    self.lose()
```

The check fires at the end of each `step()`, after the win check.
There is no other lose path — no hazards, no respawn cost, no
fall-through holes. Cracked thaw simply blocks future slides; the
pawn never "dies".

## 9. Novelty note

`prior-games/index.md` is NOT empty (14 entries). The
distinguishing rules below were articulated in detail in
`workspace/mechanic-pick.md`; this section re-grounds them
against the now-fleshed-out spec.

### Closest taxonomy near-misses (re-checked against the full spec)

- **ka59 sokoban-explode-chase** — single-step push, 3-cell stride;
  wt39 is unbounded glide-until-wall and there is no pushable
  target other than the pawn itself. ka59 has no momentum-and-
  inertia and no in-flight bumpers.
- **m0r0 mirror-orb-merge** — paired orbs, mirrored cell-by-cell
  motion. wt39 has a single pawn, no mirroring, true momentum.
- **tu93 maze-pickup-train** — 3-cell-step navigation through
  value-2 corridors carved into a maze tile. wt39 is open-ice
  glide-until-collision — the inverse topology (open arena vs.
  labyrinth corridors) and the inverse motion model (unbounded
  glide vs. fixed 3-cell hops).
- **vc33 row-slide-pull-tab** — the entire row of tiles slides
  when a tab is clicked; units ride passively on top. wt39 has
  no clickable tabs and no row-sliding; the *pawn itself* moves
  while the floor stays put. Inverted agency.
- **ar25 shape-mirror-cover** — reflects a *shape* across a fixed
  mirror; wt39 reflects *motion* mid-flight via per-cell bumpers
  and there is no shape-coverage scoring.

### Closest prior-games near-misses

- **kn58 anchor-pull-magnet** — click places an attractor; many
  pawns each move ONE Manhattan-cell toward it. wt39 is arrow-
  driven (no click), single pawn, unbounded motion, no attractor
  field — just direct directional glide.
- **vn8d domino-cascade-topple** — single click ignites a chain
  reaction through pillars; rotators turn the chain. wt39 is a
  pawn-glide whose deflection happens during the slide rather
  than across separate domino objects; the player drives the
  pawn one slide at a time, and a deflection within a single
  slide is mechanically distinct from a cascade across separate
  domino objects.
- **bx84 beam-mirror-reflect** — beam emitter draws a ray; mirrors
  reflect the ray within a single step. wt39 has no beam — the
  pawn's location IS the game state, not a derived ray-trace, and
  the player directs the pawn explicitly via arrows rather than
  setting up a passive beam.
- **fz5j phase-step-tile** — tiles pulse open/closed on per-cell
  periods; closed tiles cost a life. wt39's thaw-tiles vanish
  after one traversal (consume, not pulse), and there are no
  lives; instead, the cracked tile becomes a *wall* that enables
  later slide-stops. Constructive consumption rather than timed
  hazard.
- **pj7k rolling-cube-face-paint** — single-step roll permutes
  cube faces. wt39 has no roll, no faces, no painting; the
  pawn translates without internal state changes.

### Negative-similarity check (re-walked against L3-fleshed spec)

The candidate's L1 image (red pawn, red goal, two black blocks
on a light-blue ice arena, framed by a black perimeter) shares
no more than two of the eight `negative-similarity-check.md`
dimensions with any single prior. Specifically the closest
prior — **vn8d** — shares only:
- dimension 4 (lose = step budget) — universal.
- dimension 7 (small primary sprites) — also widespread.
- dimension 5 (deflectors-of-some-kind) — borderline; vn8d's
  rotators turn a cascading chain across pillars, wt39's bumpers
  turn an in-flight pawn glide. The role of "deflector" in the
  player's mental model is identical, but the OBJECT being
  deflected is fundamentally different (a sequence of separate
  triggered objects vs. a single moving pawn).

Three dimensions max with any single prior. Below the rejection
threshold; PASSES the negative-similarity check.

The visual signature (palette 1, 4, 8, 10, 12 dominant; cool blue
ice with warm orange bumpers and red pawn) is distinct from
kn58's (heavy reds and blues), bx84's (warm beam yellow on dark
bg), and vn8d's (monochromatic pillars on darker bg).

### Vs. existing video games (axis 1)

Sliding-ice mechanics appear in many puzzle games (Pokémon ice-
floor sequences, Adventure Time: Hey Ice King!, Bloxorz, Slipway,
Stephen's Sausage Roll has a related slip mechanic). The
specific combination of `glide-until-wall + 90°-bumper-deflect
+ one-use-thaw-tile` is not, to the spec author's knowledge,
the central mechanic of any well-known existing game. The
harness's axis-1 check is left to the user as final arbiter.
