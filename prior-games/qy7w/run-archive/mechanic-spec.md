# qy7w — mechanic spec

## 1. Title
Strand-Twist Permutation (working title only; not visible in-game).

## 2. Mechanic family
Vertical coloured strands run from a row of START caps at the top of
the playfield to a row of END slots at the bottom. Toggleable CROSSING
sprites between adjacent (or, at L2+, non-adjacent) strand columns
swap which column carries which strand. The cumulative permutation of
strands top-to-bottom is determined by the current set of
PASS/TWIST crossings; the level wins when each strand's bottom
endpoint sits in the END slot whose colour matches its top cap (with
L3's colour-shift cell potentially remapping a strand's colour
mid-route). Core-knowledge priors used: **basic geometry & topology**
(permutations, over/under threading) primary; **objectness**
(persistent strand and crossing identities) secondary; **basic
physics** (colour "carried" past a dye station — like fluid through a
filter) at L3 only.

## 3. Sprite roster

Strand columns occupy three vertical lanes centred at screen-x = 17,
33, 49. Strand-segment width is 3 pixels (lanes [16..18], [32..34],
[48..50]). Native 64×64 grid. No upscaling.

Static sprites placed once per level:

- `top_cap_red`: 5×5, palette {8 red filled, 4 off-black border},
  tags `[start_cap]`. Role: visible top endpoint declaring strand 0's
  starting colour.
- `top_cap_blue`: 5×5, palette {9 blue, 4 border}, tags `[start_cap]`.
- `top_cap_yellow`: 5×5, palette {11 yellow, 4 border}, tags `[start_cap]`.
- `bottom_slot_red`: 5×6, hollow frame palette {8 red, 4 border, -1
  centre}, tags `[end_slot]`. Role: visible bottom target (frame
  colour shows required strand colour).
- `bottom_slot_blue`: same shape, palette 9.
- `bottom_slot_yellow`: same shape, palette 11.
- `bottom_slot_green`: same shape, palette 14 — **L3 only**.
- `crossing_binary`: 19×7, two sprite variants `crossing_binary_pass`
  and `crossing_binary_twist`; the active variant is swapped via
  `set_interaction(REMOVED)` per click. PASS = two parallel 3-pixel
  vertical bars (matching the two strand lanes' colours); TWIST = X-
  shape where each strand's colour bridges from its incoming column
  to the OTHER outgoing column, with a 1-pixel break on the under-
  strand at the X centre. Tags `[crossing, pair=<col_low>-<col_high>]`.
  Role: clickable toggle that swaps two adjacent strand columns at
  this row.
- `crossing_long`: 35×7 — **L2 onward**. Two variants
  `crossing_long_pass` and `crossing_long_twist`. PASS = three parallel
  3-pixel vertical bars. TWIST = wide X spanning columns 0 and 2,
  with column-1's strand passing straight through the centre as a
  vertical bar (rendered behind the X). Tags `[crossing, pair=0-2]`.
  Role: clickable toggle that swaps strands at columns 0 and 2 in a
  single move, leaving column 1 unchanged.
- `blocker_yellow`: 4×4 — **L2 onward**. Pixels `[3,3,3,3]` row 0,
  `[3,11,11,3]` row 1, `[3,11,11,3]` row 2, `[3,3,3,3]` row 3 — a
  yellow square inside a grey frame. Tags `[blocker, colour=11]`.
  Role: passive cell. If the strand routed through this cell has
  colour 11 (yellow) at this y, the run loses.
- `blocker_blue`: 4×4 — **L3 only** (an additional blocker). Tags
  `[blocker, colour=9]`.
- `shift_green`: 6×6 — **L3 only**. A green-filled square with a
  small 4-pixel inner crosshatch (palette 14 outer, 5 inner pattern).
  Tags `[shift, new_colour=14]`. Role: passive cell. Any strand
  routed through this cell has its colour remapped to palette 14
  (green) for the segment below this y.
- `strand_canvas`: 64×54 — large dynamic sprite (one per level). Its
  `pixels` array is fully rewritten in `step()` after every action
  to depict each strand's current routed colour at every (col, y).
  Tags `[strand_canvas]`. Layer 0 (below all overlays). Role: the
  visible strand bodies the player perceives.

Two HUD-only widgets:

- `StepCounterHud(RenderableUserDisplay)`: paints row 63 with a bar
  shrinking from left as steps deplete (palette 7 pink fill, palette
  4 background).

## 4. Level progression, mechanic enumeration, and witness solutions

Three levels, all using `grid_size=(64, 64)` (native; no scaling).

### Level 1 — base dynamic system

**Setup.**
- Top caps at strand-cols (0, 1, 2): red(8), blue(9), yellow(11).
- Bottom slots at cols (0, 1, 2): yellow(11), red(8), blue(9).
- Crossings (initial state PASS for all):
  - C1 = `crossing_binary` between cols 0-1 at y=18.
  - C2 = `crossing_binary` between cols 1-2 at y=30.
  - C3 = `crossing_binary` between cols 0-1 at y=42.

**Mechanics required by the witness** (N=1):

- **M1: BINARY-CROSSING TOGGLE.** Clicking a binary crossing flips
  it between PASS (strands go straight through) and TWIST (the two
  strand columns it spans swap below this row). The strand canvas
  re-routes accordingly.

**Necessity per mechanic.**
- *L1 cannot be solved without triggering M1 because* the initial
  configuration (all PASS) routes strands straight down to bottom
  cols (red, blue, yellow), but the slots demand (yellow, red, blue);
  no configuration with all PASS satisfies the win predicate, and the
  only player-controlled state mutation is BINARY-CROSSING TOGGLE.

**Witness solution.** ACTION6 click coordinates target each
crossing's centre.
1. ACTION6 @ (33, 33) — toggles C2 to TWIST. Strands at y>30 become
   (red, yellow, blue).
2. ACTION6 @ (25, 45) — toggles C3 to TWIST. Strands at y>42 become
   (yellow, red, blue). Bottom matches slots → next_level().

(Click coordinates are crossing-sprite centres in display pixels.)

**Difficulty justification.**
- (a) Random-resistance: random clicks land on the 64×64 grid, but
  `_get_valid_actions` exposes only the 3 crossing-centre clicks, so
  random play walks a 3-bit hypercube. Of the 8 binary states, exactly
  one wins. Random play with a step budget of 30 has a high probability
  of stumbling — that is acceptable per `difficulty-rules.md` § 1 for
  a tutorial.
- (b) Human-tractable: ~90 seconds for an attentive human to register
  the click-toggle effect, infer that strands re-route, and arrive at
  the matching configuration via 2–3 toggles.
- (c) Planning depth: **no strict planning requirement** at L1. Once
  the mechanic is understood, the search space is 8 states and the
  next-correct move is locally legible (look at which strand is in the
  wrong column and toggle the crossing between).
- (d) Step budget: 30. Generous over the 2-click witness; ample room
  to experiment with all 3 crossings and recover from mis-toggles.

### Level 2 — base system + 1 new mechanic

**Setup.**
- Top caps: red, blue, yellow (cols 0, 1, 2).
- Bottom slots: yellow(11), red(8), blue(9).
- Crossings (initial all PASS):
  - C1 = `crossing_binary` cols 0-1 @ y=14.
  - C2 = `crossing_long` cols 0-2 @ y=22.
  - C3 = `crossing_binary` cols 1-2 @ y=30.
  - C4 = `crossing_binary` cols 0-1 @ y=46.
- Constraint: `blocker_yellow` placed at (col=1, y=36).

**Mechanics required by the witness** (count = 2 = L1's 1 + 1):

- **M1: BINARY-CROSSING TOGGLE** (carried from L1). Same rule.
- **M2: LONG-CROSSING TOGGLE.** Clicking a long crossing flips it
  between PASS and TWIST. PASS leaves all three columns unchanged;
  TWIST swaps strands at cols 0 and 2 in a single move (col 1
  unchanged). One click effects a long-distance transposition that
  binary toggles can only build up via three sequenced toggles
  (σ_a σ_b σ_a in braid-group terms).

`blocker_yellow` is a **spatial constraint, not a player-exercised
mechanic**: it never moves and is not clicked. The player learns of
it by routing a yellow-coloured strand through it on a wrong attempt
and seeing the run fail; the witness avoids it by routing differently.
It is documented under "Lose condition" rather than as a mechanic.

**Necessity per mechanic.**
- *L2 cannot be solved without triggering M1 because* the only
  configurations that achieve the σ_a σ_{0-2} (or σ_{0-2} σ_b)
  permutation required for slots (yellow, red, blue) are
  (c1=1, c2=1, c3=0, c4=0) and (c1=0, c2=1, c3=1, c4=0). Both flip
  exactly one binary crossing. Without any binary toggle, with c2 at 0
  or 1, the bottom is (red, blue, yellow) or (yellow, blue, red)
  respectively — neither matches slots (yellow, red, blue).
- *L2 cannot be solved without triggering M2 because* the only
  binary-only configuration that reaches bottom (yellow, red, blue)
  is (c1=0, c2=0, c3=1, c4=1) (= σ_b σ_a). Tracing: at y=36 between
  C3 and C4, this routing places strand_R at col=1, but every other
  binary-only configuration that *might* match the target also routes
  a yellow-coloured strand through (col=1, y=36) — which the
  `blocker_yellow` cell blocks, firing `lose()`. Specifically
  (c1=0, c2=0, c3=1, c4=1) trace at y=36: strands at cols (red,
  yellow, blue). Col 1 = yellow → `blocker_yellow` matches → lose.
  Hence every binary-only winning candidate is killed by the blocker;
  reaching the goal requires at least one LONG toggle to re-route
  yellow away from (col=1, y=36).

**Witness solution.**
1. ACTION6 @ (25, 17) — toggles C1 to TWIST.
2. ACTION6 @ (33, 25) — toggles C2 to TWIST.

After step 1, strands at y∈(14, 22): (blue, red, yellow). After step
2, strands at y∈(22, 30): (yellow, red, blue). C3 = PASS, so unchanged
through y=30. At y=36 col 1 = red (not yellow) → blocker passes.
C4 = PASS. Bottom (yellow, red, blue) → win.

**Difficulty justification.**
- (a) Random-resistance: 4 binary-toggle slots × 2 states = 16
  configurations; the step budget cap and the blocker-on-failed-paths
  combine to make blind random play very unlikely to win — most random
  trajectories hit the blocker and `lose()` triggers immediately, ending
  the run before it could stumble into the 2 winning configurations.
- (b) Human-tractable: ~2 minutes. The player learns the long
  crossing's wider visual signals a "longer reach" swap; realises after
  one or two failed binary-only attempts that the blocker forbids
  yellow at the centre; then routes via a long toggle.
- (c) Planning depth (post-discovery): the player faces 4 valid first
  clicks (C1..C4). Of those, two — C3 (col 1 immediately becomes
  yellow at y=36, a colour the blocker forbids by inference from
  prior failed runs) and C4 — lead to dead-ends; the LONG toggle
  (C2) is on the witness path. The plausible-but-wrong alternative is
  "I'll just toggle C3 and C4 since they're the binary equivalent" —
  the player rejects it because they remember the blocker. Reasoning
  chain at each step: "click C1 to send blue into col 0 above the
  long crossing; now click C2 so the long swap routes yellow to col
  0, red stays on col 1 (avoiding the blocker), and blue ends up on
  col 2."
- (d) Step budget: 24. Generous over the 2-click witness; allows the
  player a few exploratory mis-toggles before committing.

### Level 3 — system + 1 more new mechanic

**Setup.**
- Top caps: red(8), blue(9), yellow(11) at cols 0, 1, 2.
- Bottom slots: green(14), red(8), blue(9) at cols 0, 1, 2.
- Crossings (initial all PASS):
  - C1 = `crossing_binary` cols 0-1 @ y=14.
  - C2 = `crossing_long` cols 0-2 @ y=22.
  - C3 = `crossing_binary` cols 1-2 @ y=30.
  - C4 = `crossing_binary` cols 0-1 @ y=46.
  - C5 = `crossing_binary` cols 1-2 @ y=54.
- Constraints / fixed cells:
  - `shift_green` at (col=0, y=38).
  - `blocker_yellow` at (col=1, y=42).

**Mechanics required by the witness** (count = 3 = L2's 2 + 1):

- **M1: BINARY-CROSSING TOGGLE** (carried from L1, L2).
- **M2: LONG-CROSSING TOGGLE** (carried from L2).
- **M3: COLOUR-SHIFT CELL.** A passive sprite at a fixed (col, y).
  Any strand routed through this cell has its colour set to the cell's
  declared colour for the segment below this y. The player observes
  this by clicking a crossing that routes a strand through the cell
  and seeing the strand visibly change colour from that y down. The
  win predicate compares the strand's bottom-segment colour, not its
  top-cap colour, against the slot.

**Necessity per mechanic.**
- *L3 cannot be solved without triggering M1 because* the only
  winning configurations route a strand through the `shift_green` cell
  at (col=0, y=38) — and no configuration with c1=c3=c5=0 (no binary
  toggle) reaches a winning routing. Specifically, at y=38 with c2=0
  the strand at col=0 is red (→ shifts to green) but bottom col 1 is
  blue (≠ red, slot mismatch); at y=38 with c2=1 the strand at col=0
  is yellow (→ shifts to green) but bottom cols 1 and 2 are blue and
  red, while slots demand red and blue (mismatch). At least one binary
  toggle (C1 or C3 or C5) is required to align the col-1 and col-2
  strands with slots.
- *L3 cannot be solved without triggering M2 because* without a long
  toggle (c2=0), the strand at col=0 at y=38 is whichever strand was
  at col=0 above C3 — i.e., red (if c1=0) or blue (if c1=1) — and
  after `shift_green` becomes green. To leave col=0 at the bottom (no
  C4 toggle, since c4=1 would move col=0 strand to col=1 and break
  the green-at-bottom-col-0 result), the strand carries green to the
  bottom. Independently, slots demand col 1 = red and col 2 = blue.
  Enumerating all 8 binary-only states (c1, c3, c5) with c2=c4=0:
  (0,0,0)→col1=blue; (0,0,1)→col1=blue; (0,1,0)→col1=yellow; etc. None
  produces (col 1 = red AND col 2 = blue) simultaneously. At least one
  long toggle is required.
- *L3 cannot be solved without triggering M3 because* none of the
  three top-cap colours is green, and no binary or long toggle alters
  a strand's *colour* — only `shift_green` introduces green into the
  scene. Slot 0 demands green; without routing a strand through
  `shift_green`, slot 0 is unreachable.
- *L3 cannot be solved while triggering `blocker_yellow` because* the
  blocker fires `lose()` if any yellow-coloured strand is routed
  through (col=1, y=42). The witness routes the yellow strand through
  col=0 at y=38 (where it shifts to green), so by y=42 the strand at
  col=1 is the strand_R (carrying colour red), not yellow. Without
  this routing, the yellow strand would pass through col=1 at y=42 in
  most binary-only attempts and trigger `lose()`. (The blocker is
  spatial constraint, not a triggered mechanic; the witness avoids it
  by mechanic M3's presence enabling a routing that diverts yellow
  to col 0.)

**Witness solution.**
1. ACTION6 @ (25, 13) — toggles C1 to TWIST.
2. ACTION6 @ (33, 25) — toggles C2 to TWIST.

After step 1, strands at y∈(14, 22): (blue, red, yellow). After step
2, strands at y∈(22, 30): (yellow, red, blue). C3..C5 = PASS, so the
routing stays (yellow, red, blue) through y=58. At y=38 col=0 has
strand_Y (the originally-yellow strand), passing through `shift_green`
→ strand_Y's colour becomes green from y=38 down. At y=42 col=1 has
strand_R (red, not yellow) → blocker passes. Bottom (col 0 = green
via strand_Y; col 1 = red via strand_R; col 2 = blue via strand_B)
matches slots (green, red, blue) → win.

**Difficulty justification.**
- (a) Random-resistance: 5 binary toggles × 2 + the long toggle = 32
  toggleable configurations; only 3 of these are winning configs (per
  the analysis under "Necessity per mechanic"), and 2 of the 3 require
  the long toggle. Most random trajectories that touch the long
  crossing also enable the blocker by routing yellow to col=1 at y=42
  via wrong binary choices, triggering `lose()`. Random play within a
  step budget of 22 has near-zero chance of stumbling into a winning
  config without prior mechanic understanding.
- (b) Human-tractable: ~3 minutes once the strand-routing model is
  internalised from L1 and L2. The new dye-station mechanic announces
  itself visually (green dot on a strand path) and the colour-shift
  is observable on first toggle. The interaction between dye-station
  and blocker requires reasoning about which strand ends up at each
  cell at each y — this is the level's main planning task.
- (c) Planning depth (post-discovery): 5 valid first clicks on
  crossings + (effectively) the dye-station and blocker as inferred
  constraints. **Trivial heuristic that fails: "toggle the binary
  crossings in the order they appear top-to-bottom (greedy resolution
  of the obvious permutation σ_b σ_a, ignoring the long crossing)".**
  This greedy heuristic walks (c1=0, c2=0, c3=1, c4=1) — an attempt at
  σ_b σ_a — but at y=42 col 1 is occupied by strand_R *or* strand_Y
  depending on intermediate choices, and the trace shows it routes
  strand_Y through (col=1, y=42) → blocker → `lose()`. **Where the
  heuristic diverges from the witness:** at the very first toggle. The
  heuristic clicks C3 (binary cols 1-2 at y=30) thinking it can build
  σ_b at y=30, but that places strand_Y at col=1 from y=30 downward,
  and the blocker at (col=1, y=42) catches it. The witness instead
  clicks C1 (binary cols 0-1 at y=14) followed by C2 (long), routing
  strand_Y to col=0 *above* the dye station so by y=38 the right
  strand has the right colour and by y=42 col 1 is occupied by
  strand_R (not strand_Y). The post-discovery player has to reason
  ahead about which strand will be where at y=42, given the blocker —
  not just compose generators left-to-right.
- (d) Step budget: 22. Generous over the 2-click witness; comparable
  to L2's 24 (does not shrink at L3 per `difficulty-rules.md` § d's
  per-level addendum — slightly tighter is fine, "shrinking" means
  significantly tighter than the witness, which 22 is not).

## 5. Action mapping

`available_actions = [6]`. Pure click. No movement keys, no ACTION5
freedom verb, no ACTION7 (per `action-enum.md` § Slot 7 is strict
undo: this game has no meaningful undo, and ACTION7 must therefore be
omitted entirely).

- **ACTION6**: CLICK at `(x, y)` in display coordinates. The click
  is converted via `camera.display_to_grid(int(x), int(y))` to grid
  coordinates `(gx, gy)` and dispatched to
  `level.get_sprite_at(gx, gy, tag="crossing")`. If a crossing sprite
  is hit, its state toggles between PASS and TWIST (achieved by
  swapping which of the two pre-cloned variants has
  `InteractionMode.TANGIBLE`). If no crossing sprite is hit, the
  click is a no-op (still consumes one step, which is fine — it's a
  natural penalty for click misses).

`_get_valid_actions` returns one ACTION6 input per crossing centre
(3 inputs at L1, 4 at L2, 5 at L3) so an enumerating agent never has
to guess pixel coordinates.

## 6. HUD and per-game state

**HUD widgets (`RenderableUserDisplay` subclasses):**
- `StepCounterHud`: paints row 63 of the frame as a depleting bar.
  `current = max - action_count`. Bar pixels in palette 7 (pink)
  while `current > 0`, fade to palette 4 (off-black) as it depletes.

**Internal state (`Game` instance attributes):**
- `self.crossings: dict[str, Crossing]` — mapping from crossing-id to
  a small dataclass holding `(pair_low, pair_high, y, type, state)`.
  `type` ∈ {`binary`, `long`}; `state` ∈ {`PASS`, `TWIST`}.
- `self.shifts: list[ShiftCell]` — `(col, y, new_colour)`. Empty for
  L1, L2; one entry at L3.
- `self.blockers: list[BlockerCell]` — `(col, y, colour)`. Empty for
  L1; one entry at L2; one or two entries at L3.
- `self.start_caps: list[(col, colour)]` — set per-level from sprite
  positions.
- `self.end_slots: list[(col, colour)]` — set per-level.
- `self.canvas: Sprite` — reference to the dynamic strand canvas
  sprite, repainted every step.
- `self.fail_pending: bool` — set when a strand routes through a
  matching blocker; consumed at end of `step()` to call `lose()`.
- No "selected sprite" handle — there is no select operation.
- No undo stack — ACTION7 is intentionally absent.
- No animation phase counters — every action's effect is rendered
  in the same step (state changes are local 1-cell snaps; no
  long-distance teleport that would require multi-frame animation).

## 7. Win condition

After every action, after recomputing strand routing and repainting
the canvas, evaluate:

```
def _check_win(self) -> bool:
    for end_slot in self.end_slots:
        col, slot_colour = end_slot
        strand_at_bottom = self._strand_at(col, y=self.bottom_y)
        if strand_at_bottom is None:
            return False
        if strand_at_bottom.current_colour != slot_colour:
            return False
    return True
```

If True, call `self.next_level()` (which on the last level triggers
`self.win()` automatically per the engine's contract).

## 8. Lose condition

Two paths:

1. **Step-budget exhaustion**: `self._action_count >= step_budget`
   (per-level: 30 / 24 / 22) → `self.lose()`.
2. **Blocker hit**: when re-routing computes that a strand carrying
   colour C is routed through a blocker cell whose `colour == C`,
   `self.fail_pending = True` and at end of `step()` →
   `self.lose()`.

No "soft-lock" state. The player cannot enter a configuration from
which the win is unreachable but `lose()` does not fire — every wrong
state is recoverable by toggling crossings back. (The blocker fires
`lose()` immediately on the turn the blocker is triggered; the game
does not make the player wait out the step budget after a blocker hit.)

## 9. Novelty note

**Closest taxonomy entries** (full distinguishing rules in
`workspace/mechanic-pick.md` § Similarity check vs taxonomy of 25):

- **vc33 — row-column-swap-stripe**: vc33 click-marker swaps
  *stones* across a marker on a single row/column. qy7w never moves
  any sprite — toggling a crossing flips a state-bit that re-routes
  every strand from that y down through the rest of the level.
- **lp85 — row-col-shift-grid**: lp85 buttons sit *outside* the grid
  and apply pre-tabulated cell-permutations. qy7w crossings sit *on*
  the routing graph and each encodes one fixed adjacent-column
  transposition. Visual unrelated.

**Closest prior-game entries** (full rules in `workspace/mechanic-
pick.md` § Similarity check vs prior-games corpus):

- **jx5k — constellation-edge-link**: jx5k builds a graph from
  scratch by pair-clicking nodes; qy7w toggles crossings on a fixed
  pre-built strand structure.
- **vy3k — region-swap-arrange**: swaps quadrants of the playfield;
  qy7w toggles single transpositions of strand columns.
- **rk7x — live-switch-routing**: routes one autonomous courier
  through toggleable junctions; qy7w has no mobile entity, all three
  strands route simultaneously top-to-bottom on each step.

`negative-similarity-check.md` walked the 8 dimensions against vc33,
lp85, jx5k, qf8m, mz6t, rk7x. No prior shares ≥3 dimensions with
qy7w (full table in `mechanic-pick.md`).
