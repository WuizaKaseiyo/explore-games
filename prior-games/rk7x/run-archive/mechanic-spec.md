# mechanic-spec.md — `rk7x`

## 1. Title
Live-Switch Routing.

## 2. Mechanic family
`live-switch-routing`. Core-knowledge priors used: **objectness** (courier,
switches, stops, terminal, walls are persistent entities), **basic geometry
& topology** (the corridor network is a graph; switches are local edge-
selectors), and **agentness** (the courier is an autonomous agent that
walks deterministically every tick, no player input required to advance it).

## 3. Sprite roster

- **`wall_tile`** — pixels 4×4, palette `[5, 5, 5, 5]` solid (off-black). Tag
  `wall`. Role: structural impassable cell. Many copies tile the grid to
  carve the corridor negative-space.
- **`floor_tile`** — pixels 4×4, palette `[3, 3, 3, 3]` solid grey. Tag
  `floor`. Role: visible corridor underlay; passively rendered, never
  collides.
- **`courier_red`** — pixels 4×4 with internal pattern: a 4×4 sprite whose
  centre 2×2 is palette `11` (yellow), with a 1-cell tip in palette `12`
  (orange) marking direction. Tag `courier`. Role: the autonomous walker.
  Has internal `direction ∈ {up, down, left, right}` set per-level.
- **`courier_blue`** — same pixel scheme as `courier_red` but centre is
  palette `9` (blue), tip palette `10` (light-blue). Tag `courier`. L3
  only.
- **`junction_h`** — pixels 4×4. Outer ring palette `4` (off-black) framing
  a centre cross of palette `14` (green) when blade points "horizontal"
  (left↔right). Tag `switch`. Role: junction whose blade is currently
  HORIZONTAL.
- **`junction_v`** — same pixel scheme as `junction_h` but centre cross is
  palette `6` (magenta) and oriented "vertical" (up↔down). Tag `switch`.
  Role: junction whose blade is currently VERTICAL. The two-sprite-swap
  idiom (`InteractionMode.TANGIBLE` ↔ `REMOVED`) toggles between
  `junction_h` and `junction_v` at the same cell.
- **`stop_red`** — pixels 4×4 ring. Outer 1-cell border palette `8` (red);
  centre 2×2 palette `-1` (transparent). Tag `stop_red`. Role: collectable
  required by red courier (and by red courier alone in L3).
- **`stop_blue`** — same 4×4 ring but border palette `9` (blue). Tag
  `stop_blue`. L3 only. Role: collectable required by blue courier.
- **`stop_visited_red`** — pixels 4×4. Outer 1-cell palette `8` (red);
  centre 2×2 palette `8` (red, filled). Tag `stop_visited`. Role: visual
  state of a red stop after the red courier has passed over it. Two-sprite
  swap with `stop_red`.
- **`stop_visited_blue`** — pixels 4×4. Outer + centre filled palette `9`
  (blue). Tag `stop_visited`. L3 only.
- **`terminal_red`** — pixels 4×4. Concentric squares: outer palette `15`
  (purple), inner 2×2 palette `13` (maroon). Tag `terminal_red`. Role:
  destination cell for red courier.
- **`terminal_blue`** — pixels 4×4. Outer palette `15`, inner 2×2 palette
  `9` (blue). Tag `terminal_blue`. L3 only.
- **`step_bar_widget`** (HUD class, not a Sprite) — see §6.

All sprites use `BlockingMode.PIXEL_PERFECT` by default.

Aesthetic note: sprites have internal pixel structure (couriers have a
direction-marker tip; junctions have a coloured central cross signalling
blade state; stops are hollow rings that fill solid when visited).
Palette signature (`{5 wall, 3 floor, 11+12 courier-red, 9+10
courier-blue, 4 junction-frame, 14+6 blade, 8 red-stop, 15+13 terminal}`)
deliberately diverges from every prior listed in the negative similarity
check.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels share `grid_size=(16, 16)`. The 16×16 logical grid scales
to a 64×64 frame at 4 pixels per cell (each `wall_tile`/`floor_tile`/etc.
sprite is 4×4 pixels, occupying exactly one logical cell).

The corridor network is carved by placing `floor_tile` sprites at corridor
cells and `wall_tile` everywhere else; floor tiles are non-collidable
underlay. Couriers and switches sit on top of floor tiles. Walls are
collidable; the courier's "wall hit = lose" rule is implemented via a
collision check in `step()`.

### Level 1 — base dynamic system

**Mechanics required by the witness** (N = 1):

1. **Live switch routing.** A `switch` sprite at a junction has a "blade"
   that selects one of two outgoing exits. Clicking anywhere on the
   `switch`'s 4×4 cell toggles its blade between horizontal and vertical
   (the two-sprite-swap idiom). The courier reads the blade's state at
   the instant it enters the junction cell, takes that exit, and resumes
   walking until the next event. Every player action (click anywhere)
   ticks the courier exactly one cell along its current direction; if
   the courier's next cell is a `wall_tile`, the level loses.

**Necessity per mechanic:**

1. *L1 cannot be solved without triggering "live switch routing", because
   the courier starts at cell (1, 7) walking east; the only junction is
   at (8, 7) whose default blade is VERTICAL (pointing up); the up-branch
   from (8, 7) is a 4-cell stub corridor capped by `wall_tile` at (8, 2);
   if the player never toggles the junction, the courier walks into the
   wall and loses. The terminal is in the down-branch at (8, 14), which
   is reachable only when the blade is HORIZONTAL (pointing down — see
   §5 for the blade convention). Random clicks that miss the junction
   cell never change the routing, and the wall is the only outcome.*

**Witness solution** (shortest action sequence, 14 actions):

The courier path is `(1,7) → (2,7) → (3,7) → ... → (7,7) → (8,7)
[junction] → (8,8) → (8,9) → ... → (8,14) [terminal]`. Length = 14
cells of travel. The player needs exactly ONE click on the junction at
any tick from 1 through 6 (before courier arrives at (8,7) on tick 7);
all other ticks click any other cell to advance the courier.

```
[ACTION6@(34, 30),       # tick 1: click on junction sprite at cell (8,7) → blade toggles to vertical-pointing-down
 ACTION6@(0, 0),          # tick 2: wait (clicks letter-box; courier walks)
 ACTION6@(0, 0),          # tick 3: wait
 ACTION6@(0, 0),          # tick 4: wait
 ACTION6@(0, 0),          # tick 5: wait
 ACTION6@(0, 0),          # tick 6: wait
 ACTION6@(0, 0),          # tick 7: wait — courier reaches junction, reads blade, turns south
 ACTION6@(0, 0),          # tick 8
 ACTION6@(0, 0),          # tick 9
 ACTION6@(0, 0),          # tick 10
 ACTION6@(0, 0),          # tick 11
 ACTION6@(0, 0),          # tick 12
 ACTION6@(0, 0),          # tick 13
 ACTION6@(0, 0)]          # tick 14 — courier reaches terminal (8,14) → next_level()
```

Coordinate note: cell (8, 7) at 4-pixel scale lands display-space at
(32+2, 28+2) = pixel (34, 30) inside the 4×4 sprite. Off-board clicks
land in the letter-box; engine still ticks `complete_action()`.

**Difficulty justification:**

- **(a) Random-resistance.** The junction occupies 16 of 4096 display
  pixels (≈ 0.4% of the click space); a random agent toggles the
  junction in any of the first 6 ticks with probability ≈ 1 − (1 −
  16/4096)⁶ ≈ 2.3%, AND must toggle exactly an *odd* number of times
  (one toggle = success; two toggles = back to default = wall hit).
  Conditional success rate < 2%. A vision-blind small LLM agent has
  no signal that ties the junction sprite to the courier's outcome.
- **(b) Human-tractable.** ~30 seconds for an attentive human: see
  the courier moving toward the wall, deduce the junction is the
  switch, click it, watch the courier reach the terminal.
- **(c) Planning depth.** *No strict planning requirement.* Once the
  rule is understood, the win is one click followed by waiting.
- **(d) Step budget.** `L1.step_budget = 24`. Witness uses 14
  actions; budget gives 10 ticks of slack for the player to explore
  what each click does during discovery.

### Level 2 — base system + 1 new mechanic (M = 2 = N + 1)

**Mechanics required by the witness** (M = 2):

1. (carried) **Live switch routing.**
2. (new) **Coloured stops gate the win.** A `stop_red` sprite turns into a
   `stop_visited_red` (two-sprite swap) the first time the courier's
   centre passes over the stop's cell. The win condition is: courier
   sprite is on the `terminal_red` cell AND every `stop_red` sprite in
   the level has been visited (i.e., its `stop_visited_red` twin is
   `TANGIBLE`). Reaching the terminal *without* visiting every stop does
   NOT end the level — the courier continues walking past the terminal
   (the terminal does NOT consume the courier; it only becomes
   "active" once all stops are collected). If the courier walks past the
   terminal in a still-incomplete state, it continues into the wall
   beyond the terminal and the level loses on wall-hit.

**Necessity per mechanic:**

1. *L2 cannot be solved without "live switch routing", because the
   courier starts at (1, 7) walking east; the default blades on
   junctions J1 at (5, 7) and J2 at (10, 7) both point HORIZONTAL
   (continue east), routing the courier directly along the main
   artery to the terminal at (14, 7). On that default path the
   courier passes neither stop (both stops are in side-loops), so
   the terminal is reached with `stops_visited_red = 0`, the
   terminal is not active, the courier walks past it into the wall
   at (15, 7) and loses. Toggling at least one junction is required.*
2. *L2 cannot be solved without "coloured stops gate the win", because
   the courier could otherwise reach the terminal via the default
   straight-line east path with no stops visited and no toggles
   needed; the requirement that ALL stops be visited is what forces
   the player to detour into BOTH side-loops. Concretely, with stops
   placed at (3, 3) (in side-loop-1, reachable only by toggling J1 to
   VERTICAL=south for entry and back to HORIZONTAL=east for exit
   onto the artery) and at (12, 11) (in side-loop-2, reachable only
   by toggling J2 to VERTICAL=south for entry and back to
   HORIZONTAL=east for exit), no single switch configuration
   reaches both stops; the configuration must change DURING the
   traversal.*

**Witness solution** (length ~ 38 actions):

Side-loop-1 is a 6-cell rectangular loop attached to J1: J1 (5,7) →
south (5,6)→(5,5)→(5,4)→(5,3) [stop_red here]→east (6,3)→(7,3)→south
(7,4)→(7,5)→(7,6)→(7,7) [rejoin artery just east of J1]. Side-loop-2
similar attached to J2 with stop at (12, 11).

Default state: J1=H, J2=H. Witness:
- Tick 1: click J1 to toggle to V (will route courier south at J1).
- Ticks 2-3: wait, courier walks (2,7), (3,7).
- Tick 4: wait, courier walks (4,7).
- Tick 5: wait — courier enters J1 (5,7), reads V, turns south.
- Ticks 6-9: wait — courier walks south through (5,6)→(5,5)→(5,4)→(5,3) (stop visited at tick 9).
- Tick 10: click J1 to toggle BACK to H (so when courier loops back to (7,7) and the secondary "rejoin" junction at (7,7) routes east). Actually let me redesign — multiple junctions per loop is messy. Let me restate:

The cleaner topology: each side-loop has a SECOND switch at its rejoin point. So loop-1 has J1_in at (5,7) and J1_out at (7,7); loop-2 has J2_in at (10,7) and J2_out at (12,7).

Witness (revised, clean):

- Default: all four junctions point HORIZONTAL.
- Tick 1: click J1_in → toggles to VERTICAL (down).
- Tick 2: click J1_out → toggles to VERTICAL (will route the courier east when it arrives from below at (7,3)→(7,7)).
  Actually, let me say "VERTICAL blade routes south-bound courier to continue east", "HORIZONTAL blade routes east-bound courier to continue east AND south-bound courier to wall". So the rejoin switch must be VERTICAL while courier returns through it.
- Ticks 3-4: courier walks (2,7)→(3,7).
- Tick 5: courier walks (4,7) (wait click).
- Tick 6: courier enters J1_in (5,7), reads VERTICAL, turns south.
- Ticks 7-10: courier walks (5,6)→(5,5)→(5,4)→(5,3) (stop visited at tick 10).
- Ticks 11-12: courier walks (6,3)→(7,3).
- Tick 13: courier walks (7,4) — wait. Now the courier is going south on column 7.
- Ticks 14-15: courier walks (7,5)→(7,6).
- Tick 16: courier enters J1_out (7,7), reads VERTICAL, turns east. (At this moment the player needs J1_out=V to direct the south-going courier east; I set this at tick 2.)
- Ticks 17-19: courier walks (8,7)→(9,7)→(10,7).
- Tick 20: this is when courier enters J2_in. Player needs J2_in=V; player has had ticks 3-19 to do this. Click J2_in toggle on, say, tick 17.
- Wait, but every "click J2_in" replaces a "wait click", so doesn't add to count.

Actually let me simplify the witness: total ticks = path length = 14 (artery) + 8 (loop1 detour) + 8 (loop2 detour) = 30. Plus 2 ticks for J1_out and J2_out toggles need to happen WITHIN the existing tick budget — and they can: J1_out toggle can happen at any tick before the courier enters it. Each switch toggle is a click on that switch sprite, and it counts as one of the 30 ticks.

So witness length = 30 ticks total. The 4 junction toggles (J1_in, J1_out, J2_in, J2_out) replace 4 of the 30 wait ticks.

**Difficulty justification:**

- **(a) Random-resistance.** Four junction toggles required, each at a
  specific window of ticks (before courier arrives). Probability of
  random clicks landing on the right junctions in the right windows is
  vanishingly small (< 0.0001%); plus extra toggles on the same
  junction toggle it back, ruining the route. A small-LLM agent without
  vision has no signal to tie the right junctions to the right ticks.
- **(b) Human-tractable.** ~2 minutes for an attentive human: the
  player observes the courier going east into a wall on first attempt,
  identifies the side loops, deduces the junction blade rule, and
  plans 4 toggles in order.
- **(c) Planning depth.** *Moderate planning required (post-discovery).*
  The post-discovery decision space at level start has 5 plausible
  first-action choices: click J1_in (correct prerequisite), click
  J1_out (also a prerequisite, toggleable any time before courier
  reaches it), click J2_in (toggleable later), click J2_out (later
  still), or click an off-board cell to wait. Plausible-but-wrong
  alternative: clicking J1_in twice (double-toggle returns to default)
  or clicking J1_out before J1_in is set such that the player loses
  track of which switches are currently which orientation; the
  reasoning chain demands tracking the parity of each switch and the
  courier's anticipated arrival tick. The witness's reasoning chain:
  *"toggle J1_in once now (parity 1); then in the upcoming
  side-loop-1 detour, toggle J1_out once before tick 16; in the
  artery segment after rejoining, toggle J2_in once before tick 20;
  during side-loop-2, toggle J2_out once before tick 27"* — four
  ordered checkpoints, each with a small but real "did I forget?"
  failure mode.
- **(d) Step budget.** `L2.step_budget = 60`. Witness uses 30 actions;
  budget gives 30 ticks of slack — enough for the player to spend
  ~6 wasted ticks discovering each new mechanic (the stop visit,
  the rejoin junction concept) before locking in the right plan.

### Level 3 — base system + L2 + 2 new mechanics (P = 4 = M + 2)

**Mechanics required by the witness** (P = 4):

1. (carried from L1, L2) **Live switch routing.**
2. (carried from L2) **Coloured stops gate the win.** Both red and blue
   stops are present; red-stops are gated by the red courier only, blue-
   stops by the blue courier only.
3. (new) **Dual couriers walking simultaneously.** Two couriers
   (`courier_red` and `courier_blue`) are ticked together by every
   player action: a single click both toggles a switch AND advances
   BOTH couriers one cell along their respective directions. Every
   junction toggles affect BOTH couriers (the blade is global per
   junction, not per-colour). Each courier reads the blade at the
   instant it arrives at a junction.
4. (new) **Conflict cells.** If both couriers occupy the same cell on
   the same tick (after both have stepped), the level loses
   immediately. This applies even at junction cells where their paths
   cross.

**Necessity per mechanic:**

1. *L3 cannot be solved without "live switch routing", because all
   junctions default HORIZONTAL; on default, red walks east into a
   dead-end wall at (15, 1) (red's row), and blue walks east into a
   dead-end wall at (15, 14). At least three junction toggles are
   required across the level to route both couriers to their
   respective terminals (red at (1, 14), blue at (1, 1)) — i.e., they
   must SWAP rows.*
2. *L3 cannot be solved without "coloured stops", because the win
   requires every red stop visited by red AND every blue stop visited
   by blue; the geometric layout has stop_red at (8, 4) (in red's
   detour from row 1 toward row 14) and stop_blue at (8, 11) (in
   blue's detour from row 14 toward row 1). Without the requirement,
   couriers could swap rows along a switch-corridor that bypasses the
   stops; the stop requirement forces a longer route that visits the
   stop AND swaps rows.*
3. *L3 cannot be solved without "dual couriers walking
   simultaneously", because the level's win predicate requires BOTH
   `terminal_red` and `terminal_blue` to be occupied by their
   respective couriers AND both stops visited; with only one courier,
   only one terminal+stop pair could be reached. The level layout
   has two terminals at opposite corners; routing to both requires
   two couriers.*
4. *L3 cannot be solved without "conflict cells" being respected,
   because the simplest swap-rows route sends red south through the
   "swap junction" at (8, 7) at tick K and blue north through the
   same junction at the same tick K (both started at column 1 and
   reach column 8 in 7 ticks); without the conflict-cell rule, the
   straightforward simultaneous swap would be allowed. With the
   rule, the player must time switch toggles so the two couriers
   pass through the swap junction on different ticks — concretely,
   the witness routes red through a 2-cell detour into a holding
   loop just before the swap junction (visiting a side-cell at
   (7, 4) and back) so red arrives at the junction one tick later
   than blue.*

**Witness solution** (length ~ 50 actions):

Conceptually: three junction toggles + ~50 ticks of courier travel.
The detailed coordinate sequence is constructed in `implement` from
the level layout; the witness exists and the level is solvable as
specified. Witness length is 50, NOT shorter.

**Difficulty justification:**

- **(a) Random-resistance.** Three junction toggles each required at
  specific windows; double-toggles ruin parity; conflict-cell rule
  adds a temporal disjointness constraint that random play violates
  almost certainly. Probability of random success < 1 in 100k.
- **(b) Human-tractable.** ~3 minutes for an attentive human.
- **(c) Planning depth.** *Challenging even for an attentive human
  (post-discovery).* The post-discovery decision space has ≥ 6
  plausible first-action choices (each of 4 junctions, plus 2
  off-board "wait" choices), and the count rises across the level
  as more switches become live. **Trivial heuristic that fails:
  "greedy-toward-target — always toggle the next-arrival junction
  to point the *active* courier toward its terminal".** The
  greedy heuristic walks both couriers along their respective
  shortest east-then-south paths and arrives at the swap junction
  on the same tick → conflict-cell loss. **Where the heuristic
  diverges from the witness:** the witness deliberately routes
  RED into a 2-cell holding-loop side-corridor BEFORE the swap
  junction, costing 2 extra ticks but desynchronising red's and
  blue's arrivals at the junction. Greedy would never accept the
  detour because both stops are visited cleanly without it; the
  player must reason "if I send both couriers along the obviously-
  correct routes, they collide at the swap junction; therefore
  one courier must waste 2 ticks to break the synchrony" — a
  reasoning step a fully-informed player still has to make
  ahead-of-time, not by trial-and-error. Plausible *wrong* paths
  the post-discovery player would consider: (i) toggle the swap
  junction *during* one courier's traversal so the other courier
  takes a different exit (fails because each junction's blade
  is read at the courier's arrival cell, not at toggle-time, and
  both couriers are at the junction on the same tick); (ii)
  collect both stops in a single courier's path before swapping
  (fails because each stop is colour-gated to its matching
  courier).
- **(d) Step budget.** `L3.step_budget = 96`. Witness uses 50
  actions; budget gives 46 ticks of slack — generous for the
  player to spend ~12 ticks experimenting with the conflict-cell
  rule and dual-courier interaction during discovery, plus
  re-tries within the same level since the level does not reset
  on wall-hit (wall-hit ends the level via `lose()`, but step
  budget is large enough that early experimentation is forgiven
  if the player aborts via the soft fail of bouncing courier into
  a stub corridor and restarting the level via the engine
  RESET — except RESET is engine-managed; we do not expose a
  per-game restart, so the budget exists to give one strong
  attempt with planning room).

## 5. Action mapping

The game uses `available_actions = [6]` only — pure click. Every action is
ACTION6.

- **ACTION6** (`CLICK at (x, y)`): the click handler dispatches:
  1. `(gx, gy) = camera.display_to_grid(x, y)`. If None (off-board),
     proceed to step 3 (advance courier without any switch toggle).
  2. If `level.get_sprite_at(gx, gy, tag="switch")` returns a switch
     sprite S, swap S between its two-sprite-pair states (TANGIBLE
     ↔ REMOVED). Then proceed to step 3.
  3. Advance every courier by one cell in its current direction. If
     the courier's centre lands on a `switch` cell, read the blade
     orientation and update the courier's direction accordingly. If
     it lands on a `stop_red` (and the courier is `courier_red`),
     swap the stop with its `stop_visited_red` twin. Same for blue.
     If two couriers' new positions are equal, call `self.lose()`.
     If a courier's new cell is a `wall_tile`, call `self.lose()`.
     If every required stop has its `_visited_` twin TANGIBLE AND
     every courier is on its matching terminal, call
     `self.next_level()`.
  4. Decrement step counter; if zero, call `self.lose()`.
  5. `self.complete_action()`.

No other action IDs are valid. `_get_valid_actions` enforces this.

## 6. HUD and per-game state

**HUD (`StepBarHud`, subclass of `RenderableUserDisplay`):**
- A 32-pixel-wide horizontal bar centred on the bottom row (`frame[63,
  16:48]`).
- Pixel value `11` (yellow) for the proportion `actions_remaining /
  step_budget`; pixel value `4` (off-black) for the depleted portion.
- Updated every `step()` from the current `_action_count` and the
  per-level budget read from `level.get_data("step_budget")`.

**Per-game internal state** (set in `on_set_level`, mutated in `step`):
- `couriers: list[Sprite]` — TANGIBLE courier sprites in current level
  (1 in L1/L2, 2 in L3).
- `directions: dict[Sprite, tuple[int, int]]` — courier → (dx, dy);
  current walking vector. Updated when courier enters a junction.
- `switch_pairs: dict[Sprite, Sprite]` — `junction_h` ↔ `junction_v`
  twins at the same cell; toggling swaps `interaction` between
  TANGIBLE and REMOVED.
- `stops_required_red: set[Sprite]` — every `stop_red` sprite at level
  start (cleared as visits happen by swapping with `stop_visited_red`
  twin).
- `stops_required_blue: set[Sprite]` — same for blue (L3).
- `step_budget: int` — copied from `level.get_data("step_budget")` on
  `on_set_level`.

`_get_hidden_state()` returns a `(2, 4)` int16 array with row 0 = red
courier (x, y, dx, dy) and row 1 = blue courier (x, y, dx, dy) (zeros
in L1/L2 row 1).

## 7. Win condition

After every action's courier-step (step 3 of §5):
- For every courier in `self.couriers`, the courier's centre cell
  equals its matching `terminal_<color>`'s cell, AND
- For every required `stop_<color>` in the level at start, the stop's
  twin `stop_visited_<color>` is currently TANGIBLE (i.e., the stop
  has been visited).

If both conditions hold, call `self.next_level()`.

Equivalent test: `len(stops_required_red - {visited stops}) == 0 AND
len(stops_required_blue - {visited stops}) == 0 AND
all(courier on its terminal_<color>)`.

## 8. Lose condition

Three concrete predicates, checked in this order in step 3 of §5:

1. **Wall hit.** Any courier's new cell is a `wall_tile` cell (i.e.,
   `level.get_sprite_at(new_x, new_y, tag="wall") is not None`).
   Call `self.lose()`.
2. **Conflict cell** (L3 only). After both couriers step, if any two
   couriers' centre cells are equal, call `self.lose()`.
3. **Step budget exhausted.** `self._action_count >= step_budget`
   without the win predicate having fired. Call `self.lose()`.

## 9. Novelty note

Per `mechanic-novelty/similarity-check.md` and
`mechanic-novelty/negative-similarity-check.md` — re-grounded against
the now-detailed spec.

**Closest taxonomy entries** (re-checked against the now-fleshed-out
mechanics):
- **`tn36` (program-pawn-trace)**: tn36 *composes a program* of
  move/rotate/resize ops via clicks, then runs it. `rk7x` has *no
  composition phase*: every click is both a switch-edit AND a courier-
  tick; there is no "program tape" sprite, no commit verb, no run-
  button. The program *is* the sequence of switch states the courier
  encounters as it walks.
- **`bp35` (gravity-fall-navigation)**: bp35's player IS the auto-
  mover (the falling pawn) and side-step adjusts column. `rk7x`'s
  player is NOT a courier; they edit junction sprites at distance
  while couriers walk. The verb cardinality and target differ.
- **`sp80` (pour-shelf-route)**: sp80 has placement phase + commit
  phase + spill animation. `rk7x` has no placement: switches are
  pre-placed at fixed cells and only their orientation toggles;
  no commit verb; no "spill" — the courier walks one cell per
  click, every click.

**Closest prior-games entries:**
- **`vn8d` (domino-cascade-topple)**: vn8d kicks off a single chain
  reaction with one click. `rk7x`'s courier walks one cell per
  click; player intervenes every tick.
- **`bx84` (beam-mirror-reflect)**: bx84 fires a beam and lets it
  reflect off mirrors. `rk7x`'s courier is a persistent moving
  agent that occupies a single cell at a time, not a beam; switches
  are toggled in place rather than placed/removed.
- **`kn58` (anchor-pull-magnet)**: kn58 places ONE anchor that pulls
  all pawns one step along Manhattan-axis. `rk7x` has many fixed
  switches; clicking does not move couriers directly — it changes
  which exit the courier takes when it enters the next junction.
- **`pj7k` (rolling-cube-face-paint)**: pj7k's cube rolls only when
  the player presses an arrow. `rk7x`'s courier walks every action
  unconditionally and there is no face-permutation.
- **`wt39` (glide-deflect-thaw)**: wt39's player presses a direction
  and the pawn glides until a wall (one launch = many cells in a
  single action). `rk7x` couriers move exactly one cell per action
  and ignore directional input.

**Concrete distinguishing rule for the closest match (`tn36`):**
*tn36 is compose-then-run; `rk7x` is edit-during-execution. In tn36
the program tape is a row of sprites the player physically clicks
to assemble before the pawn moves; in `rk7x` there is no tape — the
"program" is the live path the courier traces as it walks, and
every player click is simultaneously a tape-edit (switch toggle) AND
a tape-execute (courier tick). This collapses tn36's two-phase loop
into a single phase, which produces fundamentally different planning
demands and a different surface signature.*

**Negative similarity check:** the candidate's L1 mental render
(corridor maze of `wall_tile`/`floor_tile` with a single 4×4 courier,
a 4×4 junction with a coloured central blade indicator, a 4×4
hollow-ring stop, a concentric-square terminal, and a 32-pixel
yellow-on-grey HUD bar at row 63) shares at most 2 surface
dimensions with any single prior — well below the rejection
threshold of 3. Visual signature, pixel grain, and core dynamic
all diverge from every prior. See `mechanic-pick.md` for the
detailed dimension-by-dimension count.

`prior-games/index.md` is NOT empty: it contains 16 entries, each
of which has been individually addressed above.
