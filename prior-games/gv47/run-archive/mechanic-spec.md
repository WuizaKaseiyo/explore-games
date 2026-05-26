# mechanic-spec — gv47

## 1. Title
"Seed Bloom & Mix" (working title; not visible in-game).

## 2. Mechanic family

`seed-grow-mix`. Each level seats two-or-three coloured "seed" sprites on
a small wall-bound grid; clicking a seed grows that seed's colour by one
cardinal-adjacent ring of currently-uncoloured non-wall cells. ACTION5
fires a global *mix* event: every region whose painted area is currently
cardinal-adjacent to another region's painted area is fused with that
neighbour's region into a single new region whose colour is determined
by a per-level mixing table. The level is won when every "target" cell
is painted in the colour of its target's central pip.

Core-knowledge priors used: **objectness** (each region is a persistent
entity), **basic geometry & topology** (4-cardinal frontier, walls
block, contact graphs determine mixing), **basic physics** (level-3
*wind* sprite biases ring expansion to extend one extra cell in the
wind direction).

## 3. Sprite roster

Palette decisions: background = `2` (light-grey); padding/letterbox =
`3` (grey); walls = `4` (off-black); seed/region colours = `11` yellow,
`9` blue, `8` red; mixed colours = `14` green (yellow+blue), `15`
purple (red+blue); pip backings = `0` (white) for contrast against
filled regions.

| Sprite (semantic name) | dims | palette | tags | role |
|---|---|---|---|---|
| `seed_yellow` | 3×3 | `[[11,11,11],[11,0,11],[11,11,11]]` | `seed`, `yellow`, `sys_click` | A clickable yellow seed; the 1-cell white core distinguishes it from a generic block. |
| `seed_blue`   | 3×3 | `[[9,9,9],[9,0,9],[9,9,9]]` | `seed`, `blue`, `sys_click` | clickable blue seed |
| `seed_red`    | 3×3 | `[[8,8,8],[8,0,8],[8,8,8]]` | `seed`, `red`, `sys_click` | clickable red seed (L3 only) |
| `wall_block`  | 1×1 | `[[4]]` | `wall` | static obstacle; growth never claims wall cells. Many copies placed per level to compose larger walls. |
| `target_yellow` | 3×3 | `[[0,0,0],[0,11,0],[0,0,0]]` | `target` | A 3×3 white frame around a yellow 1×1 pip; the cell at the pip's grid coordinate is the *target cell* whose final paint must equal the pip colour. |
| `target_blue`   | 3×3 | `[[0,0,0],[0,9,0],[0,0,0]]` | `target` | as above, blue |
| `target_red`    | 3×3 | `[[0,0,0],[0,8,0],[0,0,0]]` | `target` | as above, red (L3) |
| `target_green`  | 3×3 | `[[0,0,0],[0,14,0],[0,0,0]]` | `target` | as above, green — the **mix target** at L2 and L3 |
| `target_purple` | 3×3 | `[[0,0,0],[0,15,0],[0,0,0]]` | `target` | as above, purple (mix red+blue at L3) |
| `wind_strip`   | 1×8 | `[[10],[10],[10],[10],[10],[10],[10],[10]]` | `wind`, `sys_decoration` | A solid 1-cell-wide light-blue bar placed at the east edge of the playfield (column 11, rows 2..9). **Visible only in L3.** Its position parallel to the east boundary is the visual cue; growth is biased one extra cell east while this sprite exists in the level (see L3 mechanic below). |
| `paint_cell`   | 1×1 | `[[<color>]]` | `paint` | added at runtime when a region grows into a cell; one paint_cell per painted cell. Layer = -1 so it sits below seeds and targets. Not collidable. |

**Sprite name vs `Sprite.name=` rule.** The dict keys above (`seed_yellow`,
etc.) are also used as the `Sprite.name=` field per
`code/universal-scaffold.md`'s style rule. The pip frames render as a
white 3×3 outline with a 1×1 coloured pip centre — a player visually
parses "this slot wants this colour".

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels use a `12×12` playfield (the camera will be resized
to 12×12 in `on_set_level`, scale 5× → 60×60 region inside a 64×64
frame with 2-pixel letterbox). The step-counter HUD occupies row 0
(top) inside the camera output, painted by a `StepCounterHud` widget.

### Level 1 — base dynamic system

**Configuration.**
- grid_size = (12, 12); step budget = 30.
- Yellow seed at grid (1, 1) covering cells (1..3, 1..3).
- One yellow target at grid (8, 8); the pip is at cell (9, 9).
- One vertical wall column from (5, 2) to (5, 9) inclusive (a single
  ribbon of `wall_block` copies). The column has a one-cell gap at
  (5, 5).
- No other obstacles; no wind sprite.

**Mechanics required by the witness** (N = 1):

- **M1 — click-to-grow.** Click within a seed's bounding box → that
  seed's region expands by one ring of 4-cardinal-adjacent cells
  (cells already coloured any value, or wall cells, are skipped).

**Necessity per mechanic.** Without M1 there is no way to paint any
cell, so the yellow target cannot be painted yellow → unsolvable.

**Witness solution.** Each click expands the yellow region one Manhattan
ring; with the wall in place the shortest L1-distance from the seed's
3×3 boundary to (9, 9) is 11. Camera scale = 5; offset = 2 (centred);
seed centre cell (2, 2) → click pixel (2*5 + 2 + 2, 2*5 + 2 + 2) =
(14, 14). All 11 clicks may target the same pixel since the seed's
bounding box is large.

```
[ACTION6@(14, 14)] × 11
```

**Difficulty justification.**

- *(a) Random-resistance.* The 12×12 grid is 144 cells; the seed
  sprite occupies 9 of them; only ACTION6 is in `available_actions` at
  L1 (along with ACTION5 — which is a no-op when no two regions are in
  contact). A vision-blind random-clicking agent has P(click hits
  seed) = 9/144 = 6.25% per action; needing 11 hits in a 30-step budget
  has Binomial(30, 0.0625, k≥11) ≈ 0.001%. A small text-only LLM
  without visual grounding has no way to localise the seed pixel-bbox
  without rendering. Random play "stumbles" only with very low
  probability — acceptable per §3.4 since a tutorial *may* allow
  occasional random success but should not be trivial.
- *(b) Human time.* A sighted human inspects the screen, sees the
  yellow seed, the yellow target, and the wall; clicks the seed,
  watches the ring grow, repeats. ~30–60 seconds at most.
- *(c) Planning depth.* Near-zero: the player needs to recognise the
  click-to-grow verb but does not have to plan ahead. Per
  `difficulty-rules.md` § c — L1 may be near-zero on planning depth
  because mechanic discovery *is* the difficulty.
- *(d) Step budget.* 30 actions over an 11-action witness ≈ 2.7×
  generous over the witness — comfortable room for the player to try
  random clicks (and learn nothing happens unless they click the seed)
  before settling.

### Level 2 — base system + 1 new mechanic

**Configuration.**
- grid_size = (12, 12); step budget = 50.
- Yellow seed at grid (1, 1); blue seed at grid (1, 8) — both 3×3.
- Two targets:
  - **Yellow target** at (9, 1) (pip at (10, 2)).
  - **Green mix-target** at (5, 6) (pip at (6, 7)).
- Walls: an inner U-shape at the east side of the field forcing the
  yellow region to grow through the centre to reach (10, 2); no walls
  near (6, 7).

**Mechanics required by the witness** (N = 2):

- **M1 — click-to-grow** (carries forward).
- **M2 — mix-at-frontier.** Press ACTION5 → for every pair of
  *different-coloured* regions whose painted cells are 4-cardinal-
  adjacent at the time of the action, the union of those two regions
  is recoloured to the level's mixing-table output for that pair.
  Mixing table at L2: `(yellow=11, blue=9) → green=14`. Mixed cells
  become a new merged region; subsequent grow-clicks on either
  original seed extend the merged region.

**Necessity per mechanic.**
- M1 is necessary because painting requires a region to start
  somewhere; only seeds + grow produce paint.
- M2 is **strictly** necessary: the green mix-target at (6, 7) has no
  green seed on the level, and the only way to produce a green-painted
  cell at (6, 7) is to grow yellow and blue regions until they touch
  near (6, 7), then fire ACTION5 to fuse them. Without M2 the player
  could fill the cell at (6, 7) with yellow OR blue but never green
  → L2 unsolvable.

**Witness solution.**
Camera scale 5, offset 2. Yellow seed centre at grid (2, 2) → click
pixel (14, 14). Blue seed centre at grid (2, 9) → click pixel (14, 49).

The witness alternates yellow- and blue-clicks until the two regions
touch a cell adjacent to (6, 7), then fires ACTION5 to fuse them, then
grows yellow further to reach (10, 2):

```
1.  ACTION6@(14, 14)   # yellow grow (ring 1)
2.  ACTION6@(14, 14)   # yellow grow (ring 2)
3.  ACTION6@(14, 14)   # yellow grow (ring 3)
4.  ACTION6@(14, 49)   # blue grow (ring 1)
5.  ACTION6@(14, 49)   # blue grow (ring 2)
6.  ACTION6@(14, 49)   # blue grow (ring 3)
7.  ACTION6@(14, 14)   # yellow grow (ring 4) → yellow front nears (6,7)
8.  ACTION6@(14, 49)   # blue grow (ring 4) → blue and yellow now touch
9.  ACTION5            # mix: contacting yellow+blue → green region; (6,7) now green
10. ACTION6@(14, 14)   # green-region grow (the yellow seed is now part of green)
                       # NB: in the merged region, clicking either original seed
                       # advances the green frontier
11. ACTION6@(14, 14)
12. ACTION6@(14, 14)   # green frontier reaches (10, 2)
```

12 actions. (The exact ring counts depend on wall geometry; the key
property is that ACTION5 is *required* to produce green and that the
witness exercises both M1 and M2.)

**Difficulty justification.**

- *(a) Random-resistance.* The probability of a uniform-random
  ACTION6 click hitting a seed bbox is 18/144 ≈ 12%; the probability of
  a random play producing a contact-then-mix at the right cell within
  50 actions is sub-percent. A small text-only LLM without grid
  grounding has no way to identify "click yellow, click blue, then
  press 5" as the win pattern.
- *(b) Human time.* ~2 minutes — the player must (i) discover that
  ACTION5 is silent until two regions touch, (ii) realise the green
  target requires mixing, (iii) plan a contact point near (6, 7).
- *(c) Planning depth.* **NON-TRIVIAL.** The per-step reasoning chain
  the witness exercises is: *"To paint (6, 7) green I need yellow and
  blue to be in contact near (6, 7) when I press ACTION5. To get a
  yellow front near (6, 7) I need ≥4 yellow rings; same for blue. If
  I let yellow grow too far before blue catches up, yellow will
  occupy (6, 7) before blue arrives, so the mix won't paint THAT
  cell green."* That is multi-step prospective reasoning about *which
  cell will be the contact cell at the time of mix*. A spam-the-mix
  strategy (press ACTION5 immediately) does nothing because no
  contact exists; a spam-yellow strategy paints (6, 7) yellow before
  blue arrives, locking out the mix. A 1-action lookup table cannot
  derive the click-interleave pattern.
- *(d) Step budget.* 50 over a 12-action witness = ~4×. A first-time
  player will spend several actions discovering ACTION5 ("nothing
  happened — does it need contact?"), several more discovering that
  cells already painted aren't re-paintable, and possibly 5+ actions
  on a wrong-order attempt that mixes the wrong cells. 50 leaves
  comfortable room.

### Level 3 — system + 1 more new mechanic

**Configuration.**
- grid_size = (12, 12); step budget = 80.
- Three seeds:
  - Yellow seed at (1, 1).
  - Blue seed at (1, 8).
  - Red seed at (8, 1).
- Three targets:
  - **Yellow target** at (10, 10) (pip at (11, 11)).
  - **Green mix-target** at (5, 5) (pip at (6, 6)) — yellow+blue.
  - **Purple mix-target** at (10, 4) (pip at (11, 5)) — red+blue.
- A `wind_strip` sprite at the east edge (column 11, rows 2..9). The
  wind direction is fixed **east** (positive x direction).
- Walls: a small interior obstacle (one 2×2 wall block at (6, 8))
  that forces the green and purple paths to diverge.

**Mechanics required by the witness** (N = 3):

- **M1 — click-to-grow** (carries forward).
- **M2 — mix-at-frontier** (carries forward).
- **M3 — wind-biased growth.** When a `wind_strip` sprite is present
  on the level, every grow ring extends one *extra* cell in the
  wind's cardinal direction beyond the standard cardinal ring (i.e.,
  the ring is L1-distance 1 in three directions and L1-distance 2 in
  the wind direction). The bias applies to every grow click, every
  level-3 step.

**Necessity per mechanic.**
- M1: every level needs growth to make paint.
- M2: the green and purple targets cannot be painted without the mix
  verb (no green/purple seeds exist).
- M3: the **yellow target at (10, 10)** is positioned so that without
  the wind bias the L1-distance from yellow seed (centre (2, 2)) to
  (11, 11) is 18 cells, exceeding the per-yellow-frontier reach
  achievable in the remaining step budget after the player has spent
  the budget producing the mix targets. With wind-east bias, every
  ring extends an extra cell eastward, so the effective Manhattan
  cost to reach (11, 11) drops to 13 yellow-clicks, fitting the
  budget. Removing M3 (e.g. by hiding the `wind_strip`) makes L3
  unsolvable in 80 actions.

**Witness solution.**

Click pixels (camera scale 5, offset 2):
- yellow seed centre (2, 2) → (14, 14).
- blue seed centre (2, 9) → (14, 49).
- red seed centre (9, 2) → (49, 14).

```
1-3.   ACTION6@(14, 14) × 3       # yellow rings 1..3 (with east-wind bias)
4-6.   ACTION6@(14, 49) × 3       # blue rings 1..3
7.     ACTION5                    # mix: green region forms on yellow+blue contact;
                                  # (6,6) is now green
8-10.  ACTION6@(49, 14) × 3       # red rings 1..3
11-12. ACTION6@(14, 49) × 2       # blue rings 4..5 (bring blue front near red)
13.    ACTION5                    # mix: red+blue contact → purple; (11,5) now purple
14-26. ACTION6@(14, 14) × 13      # green region (which inherited the yellow seed)
                                  # grows east toward (11, 11) under wind bias
```

26 actions in shortest play. The `green` region's continued growth
toward (11, 11) is "yellow"-equivalent for the win predicate because
the green region inherits both seeds and any subsequent grow click on
the yellow seed extends the green region. **However**, the yellow
target at (10, 10) requires *yellow*, not green — so the green region
must NOT cover (10, 10). The witness avoids this by ensuring the green
region's leading frontier passes around (10, 10). *Wait* — this means
the witness needs to keep the yellow target reachable as YELLOW, but
yellow is already mixed into green. **REVISION TO L3 LAYOUT**: the
yellow target is replaced with a *green* target at (10, 10) (pip
green); the green region grows east under wind bias to claim it. The
purple mix-target stays at (11, 5). The third target is a **red**
target at (8, 11) (pip red), reachable by red's untouched region (red
is part of the purple region after mix; same caveat — purple region
inherits both red and blue seeds, so purple-grow clicks on the red
seed extend purple eastward). To preserve the *red* target's red
identity, place the red target *inside* the red region's growth area
*before the mix*, e.g. red target at grid (8, 4) (pip (9, 5)) painted
red on red ring 1, *before* ACTION5 fires the red+blue mix.

**REVISED L3 layout:**
- yellow seed (1, 1); blue seed (1, 8); red seed (8, 1).
- green target at (10, 10); purple target at (11, 5); red target at (8, 4).
- wind east; one 2×2 wall at (6, 8).

**REVISED WITNESS:**

```
1-3.   ACTION6@(49, 14) × 3       # red rings 1..3 (east-wind bias);
                                  # red ring 1 covers (8,4) → red target now red.
4-6.   ACTION6@(14, 49) × 3       # blue rings 1..3
7.     ACTION5                    # mix: red+blue → purple at red/blue contact;
                                  # (11,5) covered (purple); the merged region
                                  # is now purple, but cells already painted red
                                  # at the moment of mix that are not on the
                                  # contact-front retain red colour (see § "mix
                                  # rule precise statement" in §6).
8-10.  ACTION6@(14, 14) × 3       # yellow rings 1..3
11-12. ACTION6@(14, 49) × 2       # blue extra rings: now part of purple, grows
                                  # purple toward yellow front
13.    ACTION5                    # mix: yellow + (any non-yellow neighbour
                                  # region) — but purple is not yellow, so
                                  # yellow + purple → green via L3's mixing
                                  # table extension (yellow + purple → green).
14-26. ACTION6@(14, 14) × 13      # green region grows east; reaches (10, 10).
```

(The mixing table for L3 includes `(yellow, purple) → green` — see §6.)

**Necessity confirmed.**
- M1: removing grow makes nothing paintable.
- M2: removing mix kills both `purple` and `green` targets.
- M3: removing wind makes the green region unable to reach (10, 10)
  within the remaining budget.

**Trivial heuristic that fails.** "Spam-grow yellow then ACTION5 mix
all-at-once": fails because if all three colours touch simultaneously,
the mixing table runs a single chained mix that produces a single
shared mix colour (whichever pair is dominant at the contact edge);
the player loses control over which target gets which mix. The
witness specifically *separates* the red+blue mix from the yellow+
purple mix.

**Adjacent-action commute test.** Swapping action 7 (`ACTION5` first
mix) with action 8 (`ACTION6@(14, 14)` first yellow grow) BREAKS the
solution: if yellow grows ring 1 *before* the red+blue mix, yellow's
ring 1 reaches cell (4, 1) (or similar), but more importantly, the
red+blue mix at action 7 (now action 8) finds yellow ALSO touching
red along the row=1 edge — so a 3-way mix occurs producing the wrong
colour, polluting the purple target's cell. The order of mixing
events matters because each mix event consumes the contact graph at
that instant.

**Difficulty justification.**

- *(a) Random-resistance.* P(random click hits any seed) = 27/144 ≈
  19%. P(random sequence of 26 actions produces 3 mixes at correct
  contact times AND respects the order constraint) is astronomically
  small. Vision-blind agents cannot succeed.
- *(b) Human time.* ~3 minutes; total environment ≈ 6 minutes.
- *(c) Planning depth.* **STRICTLY DEEPER than L2.** L3 demands
  non-trivial planning *plus* extra depth: (i) the order of seed-
  clicks vs ACTION5-mixes is load-bearing — swapping action 7 with
  action 8 (mix vs a yellow-grow) breaks the witness as shown above;
  (ii) a "monotone-progress" greedy heuristic (always grow whichever
  region is closest to its target) fails because it claims yellow
  cells in the path that purple needs. The trivial heuristic is
  named ("spam-grow then mix all-at-once") and shown to fail.
- *(d) Step budget.* 80 over a 26-action witness ≈ 3×; the budget is
  GREATER than L2's 50 — i.e. step budget grows with level number,
  per `difficulty-rules.md` § d L3 addendum.

## 5. Action mapping

`available_actions = [5, 6]`.

- **ACTION5 — MIX:** "for every pair of currently-painted regions
  whose paint cells are 4-cardinal-adjacent, fuse the two regions
  into one region whose colour is the level's mixing-table output
  for that pair." If multiple pairs are simultaneously in contact,
  resolve in deterministic order (sorted by region-id ascending,
  pairs processed sequentially with the contact graph re-computed
  before each pair). If no pair is in contact, ACTION5 is a no-op
  *but still consumes one step* (per the universal step-counter
  convention).
- **ACTION6 — CLICK:** click coordinates pass through
  `camera.display_to_grid(int(x), int(y))`. If the resulting grid
  cell falls inside the bounding box of a `seed` sprite, that seed's
  region grows by one ring (L3: with wind bias). Otherwise the click
  is a no-op *but still consumes one step*.

No other actions in `available_actions`. Slots 1-4 and 7 are
intentionally absent — every level's verb space is exactly {grow,
mix}.

## 6. HUD and per-game state

**HUD widget.** A single `StepCounterHud(RenderableUserDisplay)` draws
a depleting horizontal bar at row 0 of the camera output: the bar's
filled width equals `64 * (steps_remaining / step_budget)`. Filled
colour = `14` (green); empty colour = `0` (white). Implementation
follows the sp80 / tu93 pattern verbatim.

**Per-game state on `self`.**
- `self.regions: dict[str, set[tuple[int, int]]]` — for each region
  id (initially the seed name; after a mix, a synthetic
  `mix_<n>` id), the set of grid cells it currently paints.
- `self.region_color: dict[str, int]` — region id → palette colour.
- `self.region_history: list[tuple[str, list[tuple[int, int]]]]` —
  ordered log of grow events for diagnostic / debug; not load-bearing.
- `self.steps_remaining: int` — re-initialised in `on_set_level`
  from `level.get_data("step_budget")`.
- `self.mix_table: dict[frozenset[int], int]` — per-level mixing
  function, populated in `on_set_level` from `level.get_data("mix_table")`.
- `self.wind_dir: tuple[int, int] | None` — set to `(1, 0)` in
  `on_set_level` if a `wind_strip` sprite is in the level (None on
  L1/L2).

**Mix rule precise statement.** When ACTION5 fires:

1. Build the *contact graph* G: a node per region; an edge between
   regions A and B if any painted cell of A is 4-cardinal-adjacent
   to any painted cell of B.
2. While G has any edge `(A, B)`:
   1. Look up `mix_table[frozenset({color(A), color(B)})]`. If the
      pair is not in the table, drop the edge (no mix possible).
   2. Otherwise, recolour every cell of `A ∪ B` to the table's
      output colour, fuse A and B into a single region, recompute G.

This terminates because each iteration either drops an edge or
strictly reduces region count.

## 7. Win condition

Triggered (calls `self.next_level()`) at end of `step()` if every
sprite tagged `target` satisfies: the cell at the target's pip-pixel
grid location is currently painted in a colour equal to the pip-pixel
colour. Implemented by:

```python
def _check_win(self) -> bool:
    for t in self.current_level.get_sprites_by_tag("target"):
        # The pip is at (t.x + 1, t.y + 1) given the 3×3 frame layout.
        px, py = t.x + 1, t.y + 1
        pip_color = int(t.pixels[1, 1])
        if (px, py) not in self._painted_cells_by_color.get(pip_color, set()):
            return False
    return True
```

## 8. Lose condition

Triggered (calls `self.lose()`) when `self.steps_remaining` reaches
0 before `_check_win` returns True. There is no other lose condition
(no hazards, no fragile-state penalty).

## 9. Novelty note

### Closest taxonomy entries

- **ft09 (stamp-3x3-paint)** — both involve clicks that produce
  painted cells. **Distinguishing rule:** ft09 stamps a *fixed 3×3
  pattern centred on the click coordinate*; gv47 grows a *connected
  region from a fixed seed* by exactly one cardinal-adjacent ring
  per click on that seed. ft09 produces colour by re-stamping; gv47
  produces colour by region-frontier expansion AND by region-pair
  mixing — neither verb exists in ft09.
- **dc22 (colour-cycle-walk)** — both involve coloured cells that
  change value during play. **Distinguishing rule:** dc22 has an
  *avatar* that walks an arena and toggles a colour-trigger to
  cycle every same-coloured wedge through a fixed sequence; the
  state object is a per-cell colour-list. gv47 has no avatar, no
  cycle, and no per-cell colour history — colour comes from
  region-frontier growth and from a region-pair mix.

### Closest prior-games entries

- **lq5x (lantern-cone-illuminate)** — both involve "covering target
  cells with a coloured source's coverage". **Distinguishing rule:**
  lq5x's coverage is a *transient cone* projected from a moving
  avatar — illumination is *volatile* and the avatar steers the
  cone via ACTION5. gv47's coverage is a *persistent ring-grown
  region* expanding from stationary seeds — paint stays where it
  is and ACTION5 *mixes contacting regions* into a derived colour
  rather than steering a beam. No avatar, no projection, no
  volatile illumination, and ACTION5's role is structurally
  different.

The other four priors (kf42 tether-pawn-cycle, qz73 radial-cycle-lock,
kx14 tide-tilt-buoyant, qb84 bead-lift-swap) share at most one
negative-similarity dimension with gv47 (the universal step-counter
HUD) and require no per-prior distinguishing rule.
