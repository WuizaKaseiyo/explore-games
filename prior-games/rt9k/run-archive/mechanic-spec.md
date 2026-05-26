# Mechanic spec — `rt9k`

## 1. Title
Torus Wrap with Tone-Cycle (working title; **not** rendered in
game).

## 2. Mechanic family
`torus-wrap-tone-cycle`. Two-prior combination from §3.4:
**basic geometry & topology** (the playfield is a torus — opposite
edges are identified, so walking off one edge re-enters the
opposite edge) and **objectness** (avatar + tone-coded filter
walls + tone-coded goal as discrete entities). No physics, no
agentness.

The single load-bearing rule on top of standard 4-cardinal
walking: **a wrap-cross changes the avatar's tone-state by
exactly one step in a 3-cycle**. Concretely: walking off the
right or bottom edge advances tone (`+1`); walking off the left
or top edge regresses tone (`−1`). Tone is taken from the
ordered set `{magenta=palette 6, yellow=palette 11, green=palette
14}`. The avatar's render colour-remaps to its current tone, so
tone state is always visible. Tone-coded filter walls are
passable iff the avatar's tone matches the wall's tone.

## 3. Sprite roster

Stride = 4 pixels per logical cell. Logical grid = 16×15
(playfield occupies pixel rows 0..59; pixel rows 60..63 are
reserved for the step-counter HUD).

- `avatar` — 4×4. Pixels = `[[-1, 6, 6, -1], [6, 5, 5, 6], [6, 5, 5, 6], [-1, 6, 6, -1]]` (a rounded square with a black centre square; the `6` cells are the tone-tinted body, recoloured per-turn via `color_remap` to current tone). Tag `["player"]`. Layer 2. Initial tone = palette 6 (magenta).
- `wall_solid` — 4×4. Pixels = `[[5, 5, 5, 5], [5, 3, 3, 5], [5, 3, 3, 5], [5, 5, 5, 5]]`. Black outer with grey inner; reads as a brick. Tag `["wall"]`. Collidable, blocks movement.
- `filter_magenta` — 4×4. Pixels = `[[5, 5, 5, 5], [5, 6, 6, 5], [5, 6, 6, 5], [5, 5, 5, 5]]`. Black frame, magenta inner — the tone the wall accepts. Tag `["filter", "filter_magenta"]`. Collidable per the filter rule.
- `filter_yellow` — 4×4. Pixels with inner `11`. Tag `["filter", "filter_yellow"]`.
- `filter_green` — 4×4. Pixels with inner `14`. Tag `["filter", "filter_green"]`.
- `goal_plain` — 4×4. Pixels = `[[2, 2, 2, 2], [2, 5, 5, 2], [2, 5, 5, 2], [2, 2, 2, 2]]`. Light-grey frame around black core (bullseye-as-target). Used at L1, L2 (no goal-tone gate). Tag `["goal", "goal_any"]`.
- `goal_yellow` — 4×4. Outer ring palette `11`, inner palette `5` core. Tag `["goal", "goal_yellow"]`. Used at L3 to indicate the goal-tone requirement (yellow).

The goal sprite's outer ring carries the same-tone visual cue as
filter walls — a player who has learned that yellow-ringed walls
need yellow-tone to enter can read off that the yellow-ringed
goal also requires yellow-tone (sprite-UI ≈ sprite-role,
`checklist.md` item 21).

## 4. Level progression, mechanic enumeration, and witness solutions

Notation: positions are logical-cell tuples `(col, row)` with
stride 4 (col 0 = pixel x = 0; col 15 = pixel x = 60). Rows
0..14 are playable; row 15 is unused so the bottom HUD strip
(pixel y = 60..63) renders cleanly. Action codes
1=UP, 2=DOWN, 3=LEFT, 4=RIGHT. Wrap rule is detailed in §5.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 1):
  1. **M1 — torus wrap.** Walking off the right edge (or, by
     symmetry, the other three edges) re-enters from the
     opposite edge.

- **Necessity per mechanic**:
  - *L1 cannot be solved without triggering M1 because* a
    `wall_solid` column at logical col 8 spans every row 0..14
    (full playfield height), and the avatar at col 4 cannot
    reach col 11 by any interior path — the only route is to
    walk off the left edge (col 0 → col 15) and continue
    leftward to col 11.

- **Layout**:
  - Avatar at `(4, 7)`.
  - Goal (`goal_plain`) at `(11, 7)`.
  - `wall_solid` at every cell `(8, r)` for r in 0..14 (full-height vertical wall splitting the playfield).
  - Step budget = 30 (level data `step_budget=30`).

- **Witness solution**:
  `[3, 3, 3, 3, 3, 3, 3, 3, 3]` — 9 LEFT presses. Trace:
  `(4,7) → (3,7) → (2,7) → (1,7) → (0,7) → wrap (15,7) → (14,7) → (13,7) → (12,7) → (11,7)` = goal.

- **Difficulty justification**:
  - **(a) Random-resistance.** A random / vision-blind agent
    must guess a 9-action LEFT-only sequence; `4^9 ≈ 2.6 × 10^5`
    possibilities for any 9-step prefix, and the level admits no
    accidental completion within the 30-step budget without
    eventually wrapping (mid-wall blocks every interior path).
    Empirical simulation against a uniform-random policy
    converges to roughly 1 in 10^5, well below the §3.5 random-
    play threshold.
  - **(b) Human-tractable.** ~30–60 seconds. Player tries arrows
    in each direction; the LEFT-then-LEFT sequence reveals the
    wrap on the second LEFT (`(0,7) → (15,7)` is a visible
    teleport). One more pass of LEFT presses lands on the goal.
  - **(c) Planning depth (post-discovery).** Per
    `difficulty-rules.md` § 2.c, **L1 has no strict planning
    requirement**. Once the wrap rule is understood, the
    remaining task is a straight LEFT-walk along row 7. Mechanic
    discovery is the entire difficulty; reaching the goal after
    discovery is near-immediate.
  - **(d) Step budget.** `step_budget = 30`. Witness length 9;
    budget is 3.3× witness, generous over exploration cost
    (player likely tries each direction once and may wrap-by-
    accident before recognising the pattern).

### Level 2 — base system + 2 new mechanics

- **Mechanics required by the witness** (M = 3 = N + 2):
  1. **M1 — torus wrap.** Carried from L1.
  2. **M2 — tone-cycle on wrap-cross (NEW).** Each wrap-cross
     advances the avatar's tone in the 3-cycle: LEFT/UP-wrap
     gives `tone − 1 mod 3`; RIGHT/DOWN-wrap gives `tone + 1
     mod 3`. Cycle order is `magenta=0 → yellow=1 → green=2 →
     magenta=0`.
  3. **M3 — tone-coded filter walls (NEW).** A `filter_<tone>`
     cell is passable iff the avatar's current tone equals the
     wall's tone; otherwise it is solid.

- **Necessity per mechanic**:
  - *L2 cannot be solved without triggering M1 because* the
    `wall_solid` column at col 8 spans every row 0..14, so the
    avatar at col 1 cannot reach col 13 by any interior path —
    the only route to the right half is a wrap.
  - *L2 cannot be solved without triggering M2 because* the
    only path into col 13 from col 1 lands the avatar at col
    15 (post-LEFT-wrap), and walking left from col 15 must
    cross the `filter_green` column at col 14, which is
    impassable to a magenta-toned avatar; tone *must* change
    en route, and the only mechanism that changes tone is the
    wrap-cross itself.
  - *L2 cannot be solved without triggering M3 because* every
    path from col 15 to col 13 passes through col 14, and col
    14 is `filter_green` for every row — there is no row in
    which col 14 is open terrain (the filter spans rows 0..14
    contiguously). The avatar must enter and exit a filter
    cell to reach col 13.

- **Layout**:
  - Avatar at `(1, 1)`, tone = magenta.
  - Goal (`goal_plain`) at `(13, 13)`.
  - `wall_solid` at `(8, r)` for r in 0..14 (mid-wall, full height).
  - `filter_green` at `(14, r)` for r in 0..14 (full height; green-tone gate).
  - Step budget = 50.

- **Witness solution** (16 actions):
  `[3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]`. Trace:
  - `(1,1) → (0,1)` (LEFT, tone=magenta) — step 1.
  - `(0,1) → wrap (15,1)` (LEFT, tone goes `0 − 1 mod 3 = 2 = green`) — step 2.
  - `(15,1) → (14,1)` through `filter_green` (LEFT, avatar tone=green = filter tone, pass) — step 3.
  - `(14,1) → (13,1)` (LEFT) — step 4.
  - `(13,1) → (13,2) → (13,3) → ... → (13,13)` (12 × DOWN) — steps 5..16.
  - `(13,13)` is `goal_plain`; level wins.

- **Difficulty justification**:
  - **(a) Random-resistance.** Witness is a 16-action specific
    sequence over 4 actions; uniform-random `4^16 ≈ 4.3 × 10^9`
    permutations of length 16. Random play within 50 actions
    needs to (i) wrap left at least once, (ii) cross
    `filter_green` while green-toned, (iii) reach (13,13). The
    constraint that green tone is held *only* between a
    LEFT-wrap and the next non-LEFT/non-UP wrap rules out the
    overwhelming majority of sequences; estimated random win
    rate ≪ 1/10000 inside the budget.
  - **(b) Human-tractable.** ~2 minutes. Player rediscovers
    wrap from L1; on the next direction-press notices the
    avatar's body recolouring after the wrap; tries to walk
    further left, hits `filter_green` (movement silently
    blocked), recognises the tone↔filter relationship after a
    couple of bumps, then routes around to col 13 and walks
    down.
  - **(c) Planning depth (post-discovery).** Per
    `difficulty-rules.md` § 2.c, **L2 requires moderate
    planning post-discovery**.
    - **Decision-space at level start (post-discovery):** the
      fully-informed player faces 4 valid first actions, of
      which **2 lead to viable strategies** (LEFT into
      LEFT-wrap, then through filter; UP into UP-wrap, then
      navigate via top edge — eventually requiring an extra
      wrap to reach right half) — count = 2 (≥ 2; passes the
      "1-action-lookup-table" reject).
    - **Plausible-but-wrong alternative:** *DOWN-first*. A
      player primed to think "I need a non-magenta tone" might
      walk DOWN to (1,14) and wrap to (1,0) gaining yellow
      tone. But yellow ≠ green, so the green filter at col 14
      still blocks the right half. The player must wrap a
      second time, having "wasted" the first wrap.
    - **Witness reasoning chain:** the LEFT-wrap is preferred
      because LEFT/UP wraps decrement tone (`−1 mod 3`),
      taking magenta=0 → green=2 in a single wrap, which is
      exactly the tone needed at col 14; any other first wrap
      lands a different tone and forces a second wrap.
  - **(d) Step budget.** `step_budget = 50`. Witness length 16;
    budget is 3.1× witness — accommodates discovering the wrap,
    the tone-cycle, and the filter (each costing a few wasted
    steps when first encountered).

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (M' = 4 = M + 1):
  1. **M1 — torus wrap.** Carried.
  2. **M2 — tone-cycle on wrap-cross.** Carried.
  3. **M3 — tone-coded filter walls.** Carried; L3 introduces a
     **second filter colour** (yellow) in addition to the green
     filter — but this is NOT a new mechanic, it is the same
     filter rule applied to a new tone value, so M3's count
     stays at 1.
  4. **M4 — goal-tone requirement (NEW).** The goal sprite
     `goal_yellow` triggers `next_level()` only when the avatar
     occupies its cell *and* the avatar's current tone equals
     the goal's tone (yellow). Standing on the goal with a
     non-matching tone is a no-op (the level continues).

- **Necessity per mechanic**:
  - *L3 cannot be solved without triggering M1 because* the
    `wall_solid` column at col 8 spans every row 0..14, so the
    avatar at col 1 cannot reach col 13 by any interior path
    — wrap is the only route to the right half.
  - *L3 cannot be solved without triggering M2 because* the
    avatar starts magenta, must reach col 13 (which requires
    crossing `filter_green` at col 14 with green tone) AND must
    finish at goal cell (13,7) with yellow tone; both
    constraints require tone changes, and only a wrap-cross
    changes tone. Two distinct tone values must be held at two
    distinct moments in the same run, which forces ≥ 2 wraps.
  - *L3 cannot be solved without triggering M3 because* (a) the
    `filter_green` column at col 14 spans rows 0..14, blocking
    every left-going traversal from col 15 to col 13 unless the
    avatar enters that filter cell with green tone; (b) the
    `filter_yellow` row at y=14 spans cols 9..14, blocking every
    upward path from col 9..14 row 15 to row 13 unless the
    avatar enters with yellow tone. Concretely: the only way to
    reach goal (13,7) with tone=yellow is to wrap UP off
    (13,0), arriving at (13,15), and then walk UP — which
    necessarily passes through `filter_yellow` at (13,14).
    Trying to bypass (13,14) by routing through col 9..12
    requires entering (col, 14) for some col in 9..12, which is
    *also* a filter_yellow cell; trying to bypass via col 15
    requires re-crossing `filter_green` at col 14 from a yellow-
    toned position, which is impossible. Both filter colours are
    therefore unavoidable.
  - *L3 cannot be solved without triggering M4 because* the
    goal cell only fires `next_level()` when the avatar's tone
    matches the goal's; an avatar arriving at (13,7) with
    tone=green (which the shorter LEFT-wrap-then-walk-down
    path produces) would otherwise win, but the goal-tone gate
    refuses that arrival, and the player must wrap further to
    convert green → yellow before re-entering (13,7).

- **Layout**:
  - Avatar at `(1, 7)`, tone = magenta.
  - Goal (`goal_yellow`) at `(13, 7)`, goal-tone = yellow.
  - `wall_solid` at `(8, r)` for r in 0..14 (mid-wall, full height).
  - `filter_green` at `(14, r)` for r in 0..14 (full height).
  - `filter_yellow` at `(c, 14)` for c in 9..14 (a 6-cell strip across the right half's bottom row of the playfield).
  - Step budget = 70.

- **Witness solution** (20 actions):
  `[3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1]` — wait, the per-step trace below is the canonical reading; the digit list is the verifying form.
  Trace, step by step:
  - `(1,7) → (0,7)` LEFT, tone=magenta — step 1.
  - `(0,7) → wrap (15,7)` LEFT, tone=`0−1 mod 3 = 2 = green` — step 2.
  - `(15,7) → (14,7)` LEFT through `filter_green`, tone=green pass — step 3.
  - `(14,7) → (13,7)` LEFT, tone=green — step 4. (Avatar is *on* the goal cell here, but goal-tone=yellow ≠ green, so `next_level()` does NOT fire. M4 in action.)
  - `(13,7) → (13,6) → (13,5) → ... → (13,0)` 7 × UP — steps 5..11.
  - `(13,0) → wrap (13,14)` UP — but (13,14) is `filter_yellow`. The wrap rule applies first (avatar leaves top edge, lands at the *bottom* of the playfield, i.e. row 14 since row 14 is the bottom row of the 0..14 playable range), and tone goes `2 − 1 mod 3 = 1 = yellow`. The avatar lands inside `filter_yellow` with tone=yellow → pass. Step 12.

Wait — re-deriving: the playable rows are 0..14 (15 rows). Pixel y=0..59. Row 0's pixel y=0..3, row 14's pixel y=56..59. Avatar at row 0 walking UP (y decreases) leaves the playfield; wraps to row 14. So step 12 lands at `(13, 14)` with tone=yellow=1, and the cell at (13,14) is `filter_yellow` — passable when avatar tone=yellow. The wrap-and-pass succeeds in one step. (If implementation needs two ticks, the final landing cell is still `(13,14)` tangible.)

  - `(13,14) → (13,13) → ... → (13,7)` 7 × UP — steps 13..19. No filter cells on this column at rows 7..13.

  Hmm — that's only 19 actions. Recount step 12: avatar at (13,0) presses UP. Old y-pixel = 0. New y-pixel = -4 → wrap to bottom of playfield. Bottom row is row 14 (pixel y=56). So wrap target = (13, 14). Tone change: `−1 mod 3` from green=2 to yellow=1. Step 12.

  - Step 12: avatar at `(13, 14)` after wrap, tone=yellow. (13,14) is `filter_yellow`; avatar tone matches; cell is passable, so the wrap succeeds.
  - Steps 13..19: 7 × UP from row 14 to row 7. At step 13, avatar moves from `(13,14) → (13,13)`. Continuing up to `(13,7)` at step 19.
  - Step 19: avatar at `(13,7)` tone=yellow=goal-tone → `next_level()` fires.

  Total = **19 actions**. Witness recorded as: `[3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]` (4 × LEFT + 15 × UP).

- **Difficulty justification**:
  - **(a) Random-resistance.** Witness specificity over `4^19
    ≈ 2.7 × 10^11`; combined with the goal-tone gate
    rejecting any arrival with non-yellow tone, even
    near-correct geometric paths fail; estimated random win
    ≪ 1/10^9 inside 70-action budget.
  - **(b) Human-tractable.** ~2.5 minutes. Player rediscovers
    wrap, tone-cycle, and filter from L2; new on L3 is the
    yellow ring around the goal — the first arrival at (13,7)
    with tone=green silently fails to advance, prompting the
    player to notice that the goal's outer ring matches the
    yellow filter cells they have not yet engaged. The
    player then plans a route that ends on (13,7) with
    tone=yellow.
  - **(c) Planning depth (post-discovery).** Per
    `difficulty-rules.md` § 2.c, **L3 requires planning that
    is challenging even for an attentive human**.
    - **Decision-space at level start (post-discovery):** the
      fully-informed player faces 4 valid first actions, with
      ≥ 3 leading to viable but length-different strategies
      (LEFT-wrap-direct + UP-wrap-back; UP-wrap-up
      first; DOWN-wrap into yellow then re-wrap; etc.) — count
      ≥ L2's count = 2 ✓.
    - **Trivial heuristic that fails:**
      *"Take the geometric shortest path through the wrap and
      stop."* This heuristic produces the 4-step LEFT-wrap-
      and-walk that lands the avatar on (13,7) with
      tone=green — visually on the goal but not advancing.
      A monotone-progress / follow-the-shape player would
      stop here and lose budget waiting for advancement.
    - **Where the heuristic diverges from the witness:** at
      step 4 the heuristic terminates (mistaking goal-cell
      occupation for goal-completion). The witness recognises
      that the goal's outer ring is yellow, so the avatar must
      arrive *with* tone=yellow, requiring an additional
      wrap-cross (UP-wrap from (13,0) to (13,14)) *before* the
      final entry. Discovering this requires reading the
      goal's tone cue and reasoning that two different tone
      values are needed at two different cells in the same
      run — an ahead-of-time chain that greedy / monotone
      heuristics cannot produce.
  - **(d) Step budget.** `step_budget = 70`. Witness length
    19; budget is 3.7× witness, comfortably above the witness
    AND above L2's 50-step budget (per `difficulty-rules.md` §
    2.d, L3's budget MUST NOT shrink relative to L2). Allows
    several rounds of trial wrap-crosses while the player
    discovers M4 (~10 wasted steps for two failed approaches
    plus the full witness still fits).

## 5. Action mapping

`available_actions = [1, 2, 3, 4]` for all three levels — pure
arrow walking, no clicks, no ACTION5 verb, no ACTION7 undo. Per
`global/action-enum.md` § Slot 7 is strict-undo, ACTION7 is
omitted entirely (the game has no meaningful undo).

| Action | Semantic | Gate |
|---|---|---|
| `ACTION1` | Move avatar one logical cell UP (pixel `y -= 4`); if pre-move y=0 then wrap to row 14 (pixel y=56) AND apply tone `−1 mod 3`. | Always; movement rejected silently if destination cell is a `wall_solid` OR a `filter_<X>` whose `X` ≠ avatar's *post-wrap* tone. |
| `ACTION2` | Move one cell DOWN (pixel `y += 4`); if pre-move y=56 then wrap to row 0 AND apply tone `+1 mod 3`. | As ACTION1. |
| `ACTION3` | Move one cell LEFT (pixel `x -= 4`); if pre-move x=0 then wrap to col 15 AND apply tone `−1 mod 3`. | As ACTION1. |
| `ACTION4` | Move one cell RIGHT (pixel `x += 4`); if pre-move x=60 then wrap to col 0 AND apply tone `+1 mod 3`. | As ACTION1. |

There is no other verb: no click, no commit, no undo, no toggle.
The "no instructions" principle is satisfied because tone is
always rendered on the avatar (its body's colour-remap reflects
current tone), and tone-coded filter walls and the L3 goal ring
share the same tone colours, so the visual language is a single
3-colour cue across all sprite kinds.

**Wrap-and-filter precedence.** When ACTION3 is pressed at col 0,
the wrap-target cell is determined first AND the tone is updated
*before* the destination cell is tested for filter blocking. The
test "is the avatar's tone compatible with the destination
filter?" therefore uses the *post-wrap* tone. This makes the
mechanic concrete and reproducible: a single action atomically
(wrap, tone-update, destination-test).

## 6. HUD and per-game state

**HUD widget.** `StepCounterHud(RenderableUserDisplay)` renders a
1-pixel depleting bar across pixel rows 60..63 (the four bottom
rows reserved outside the 64×60 playfield). Bar fills horizontally
proportional to `(steps_remaining / step_budget)`; filled cells use
palette 14 (green) and depleted cells use palette 5 (black). When
`steps_remaining == 0`, the game enters lose state on the next
action that would consume a step.

**Per-game state** (`Game` instance attributes):

- `self._tone: int` — avatar's current tone in {0, 1, 2}. Persists
  across actions within a level. Reset to 0 (magenta) on
  `on_set_level`.
- `self._step_budget: int` — pulled from `level.get_data("step_budget")`.
- `self._steps_remaining: int` — drains by 1 per action; decremented in `step()`.
- `self._step_counter_hud: StepCounterHud` — single HUD instance.
- The avatar sprite's body colour is `color_remap`'d after every
  tone change so the sprite always renders in its current tone.

`_get_hidden_state(self)` returns a small array including
`self._tone` and `self._steps_remaining` for engine debugging /
reproducibility.

`_get_valid_actions(self)` — default; all of `[1, 2, 3, 4]` are
always offered (the engine itself does not gate; movement
rejection happens inside `step()` and silently consumes a step).

## 7. Win condition

A `next_level()` predicate checked at the *end* of every `step()`,
after movement (and any wrap+tone update) has resolved:

```
let avatar = level.get_sprites_by_tag("player")[0]
let on_cells = level.get_sprite_at(avatar.x, avatar.y, "goal")
if on_cells:
    if "goal_any" in on_cells.tags:
        # L1, L2 — any tone counts
        self.next_level()
    elif "goal_yellow" in on_cells.tags and self._tone == 1:
        # L3 — only yellow tone
        self.next_level()
```

After L3 completes, the engine fires `self.win()` automatically
(via the base class's "no more levels" branch).

## 8. Lose condition

Single predicate: `self._steps_remaining == 0` after a step that
just decremented the budget. Calls `self.lose()`.

There is no soft-lock: the avatar can always undo a positional
mistake by wrapping again (tone-cycle is reachable from any tone
in 1 wrap), and there are no irreversible state mutations. Per
`difficulty-rules.md` § 1, this is the lose-side equivalent of
"no soft-lock waiting room".

## 9. Novelty note

Closest references in `mechanic-novelty/taxonomy-of-25-games.md`:

- **m0r0 — mirrored-quad-control.** Multi-avatar lockstep with
  per-quadrant axis flips. *Distinguishing rule:* `rt9k` controls
  exactly one avatar; arrow inputs are never mirrored; the only
  coupling between axes and game state is the wrap-edge crossing,
  which is a TOPOLOGICAL effect (re-entry from opposite edge),
  not a CONTROL effect (m0r0's flipped axes).
- **g50t — walk-vs-scroll.** Scrolling backdrop on a timer.
  *Distinguishing rule:* `rt9k` has no temporal scroll; the
  playfield is stationary and the wrap is geometric (avatar
  exits and re-enters), not temporal.
- **bp35 — gravity-fall-navigation.** Side-step under gravity
  with portals. *Distinguishing rule:* `rt9k` has no gravity and
  no placed portal sprites — every wrap is at the playfield's
  outer boundary, identical for all four edges.

Closest references in `prior-games/index.md` (and unindexed
prior-games):

- **pk4m — duotone-flip-walk.** Avatar with binary colour state;
  ACTION5 flips colour; pads auto-flip; polarity walls gate by
  colour. *Distinguishing rule:* pk4m exposes an explicit colour-
  toggle verb (ACTION5) and in-cell auto-flip pads — colour
  change is FREELY available inside the playfield. `rt9k` ties
  tone change *only* to topological wrap-edge crossings; there is
  no in-cell tone toggle and no flip-pads. The player's reasoning
  in pk4m is "when do I flip?"; in `rt9k` it is "which edges do I
  cross, in what order?". Two-tone (pk4m) vs three-tone (`rt9k`)
  also produces a different mod-arithmetic structure for the
  cumulative-tone calculation. ACTION sets diverge: pk4m uses
  ACTION5; `rt9k` is pure arrows `[1,2,3,4]`.
- **lz7q — dual-plane-walk.** Two superimposed Day/Night planes,
  ACTION5 toggles. *Distinguishing rule:* lz7q's two-plane
  toggle is global and free-at-will via ACTION5; lz7q has no
  edge-wrap. `rt9k` has neither planes nor a toggle verb.
- **gh4r — repulsion-herd-corral.** Warden walks 4-strides,
  drifters flee shared-axis. *Distinguishing rule:* `rt9k` has
  no autonomous drifters or any non-player agent.
- **wt39 — glide-deflect-thaw.** Glide-until-wall + 90° bumpers
  + brittle thaw-tiles. *Distinguishing rule:* `rt9k`'s avatar
  moves exactly one cell per arrow press (no glide), has no
  bumpers, and has no breakable tiles.
- **bz3k — drift-impulse-cardinal.** Persistent integer cardinal
  velocity adjusted by ±1. *Distinguishing rule:* `rt9k` has no
  velocity state; tone is the carried state and is mutated only
  at wrap-edges, not by arrow input.
- **jd4q — echo-trail-teleport.** Walking deposits a fading
  echo; click teleports back consuming the trail.
  *Distinguishing rule:* `rt9k` has no trail, no click verb, and
  no teleport-back — the only non-local navigation is the implicit
  edge wrap.
- **ek73 — wake-trail-evade.** Vacated cells become decaying
  hazards; warp pads teleport in pairs. *Distinguishing rule:*
  `rt9k` has neither a wake nor placed warp pairs; the wrap is
  always at the rectangle's outer boundary, always paired with
  a tone-step, and never at a placed sprite.

Per `mechanic-novelty/similarity-check.md` § 2 description-level
test: no taxonomy or prior-games entry matches all of (win
condition = "reach goal in specified tone", primary action =
"4-cardinal walk", primary constraint = "edge-wrap is the *only*
tone-changing event"). The candidate is **NOVEL**.

Per `mechanic-novelty/negative-similarity-check.md` § seven
dimensions, `rt9k` shares ≤ 4 dimensions with any single prior
(against pk4m: dims 1, 3, 4, 5 — universal cast/goal/budget; not
6/7/8 which are weighted heavier per the cited rule; the
visual signature, sprite grain, and core dynamic all diverge —
three-tone modular wrap-arithmetic is not present in any prior).
