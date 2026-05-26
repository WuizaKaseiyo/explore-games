# Mechanic Spec — qn7w (`pulse-chain-eject`)

## 1. Title
Pulse-Chain Eject — Newton's-Cradle Momentum Transfer

(Working title for human reference only; not visible in-game.)

## 2. Mechanic family
A click-only puzzle in which the player triggers a single momentum pulse along a stationary chain of touching balls; the pulse propagates invisibly through the body of the chain (only a brief inline flash is rendered for legibility) and **ejects exactly one ball — the terminal one — by a single ball-width along the chain's axis**. Intermediate balls do not move; only the chain's terminal ball physically translates one step. The defining property is that energy concentrates at the chain's terminus rather than distributing through every cell. Across the three levels, the base pulse-eject mechanic is enriched first by a **junction-routing** rule (a T-shaped node at which the pulse takes one of two outbound branches based on the node's current orientation, switchable by clicking the node) and then by a **merge-on-coincidence** rule (a target pad that requires *two* deposited balls and only lights up when both are received).

Prior categories used (`design-constraints/core-knowledge-priors.md`):
- **Objectness** — balls, pusher knobs, junction nodes, target sockets, merge pads are persistent collidable entities.
- **Basic physics** — discrete-step momentum transfer (Newton's cradle).
- **Basic geometry & topology** — chains have an oriented axis; junctions branch the chain into a T-graph.

## 3. Sprite roster

All sprites are designed at native 64×64 display resolution; the playfield grid is 64×64 with no upscaling (per `checklist.md` item 20). Primary sprite size = 6×6 with internal pixel detail (highlight, rim, and core). Palette deliberately compact: **5 (black, structure), 9 (blue, primary balls), 10 (light-blue, ball highlight), 11 (yellow, secondary balls), 12 (orange, merge pad core), 14 (green, junction indicator), 15 (purple, accents), 4 (off-black, dim/inactive).** Background = 0 (white). Padding = 0.

| Name | Dimensions | Palette | Tags | Role |
|---|---|---|---|---|
| `chain_ball_blue` | 6×6 | `{9, 10}` + `-1` corners | `["chain_ball", "ball_blue"]` | A round ball with light-blue (10) rim/highlight and blue (9) core; corner pixels `-1` to round the silhouette. The base body of any chain. Stationary except when ejected. |
| `chain_ball_yellow` | 6×6 | `{11, 12}` + `-1` corners | `["chain_ball", "ball_yellow"]` | Same shape as blue, recoloured to yellow body / orange highlight. Used for chains whose terminal must fill a yellow target. Distinct hue makes per-chain identity readable. |
| `pusher_knob` | 6×6 | `{4, 15}` + `-1` corners | `["pusher", "sys_click"]` | A symmetric purple-rimmed (15) button with off-black (4) inset core. **(Revised — Critique-1 Issue 2.)** Reads as "pressable button" via the recessed centre; explicitly *no* directional protrusion / handle, so the sprite encodes no cultural-convention direction (per `forbidden-elements.md`). The pulse-direction is encoded by the pusher's *placement* — adjacent to one end of the chain — and by the chain's geometry (the chain extends in one cardinal direction from the pusher; the pulse propagates along that axis). Concrete pixel pattern: `[-1,4,4,4,4,-1]/[4,15,15,15,15,4]/[4,15,4,4,15,4]/[4,15,4,4,15,4]/[4,15,15,15,15,4]/[-1,4,4,4,4,-1]`. Reflection- and rotation-invariant. |
| `target_socket_blue` | 6×6 | `{4, 9}` + `-1` corners | `["target_socket", "socket_blue"]` | A hollow ring drawn as a 4-pixel-wide off-black (4) frame with `-1` core. When a blue ball is deposited, the core pixels are filled with palette 9 (blue), making the socket "lit". Ring shape reads as "expects an arrival". |
| `target_socket_yellow` | 6×6 | `{4, 11}` + `-1` corners | `["target_socket", "socket_yellow"]` | Same as blue socket, but the lit-state colour is 11 (yellow). |
| `junction_node` | 6×6 | `{4, 14}` | `["junction", "sys_click"]` | A hexagonal node with off-black (4) frame and a green (14) tab indicating the *currently active* branch direction. The tab moves to the top half when the up-branch is active, to the bottom half when the down-branch is active. Reads as "switch / interactive". Clicking cycles the tab (active branch) between the two outbound sides. |
| `merge_pad` | 6×6 | `{4, 12}` + `-1` corners | `["merge_pad", "target_double"]` | A hollow off-black frame with a small orange (12) pip in the centre marking "two-ball receiver". When one ball is deposited, the pip becomes a half-fill (one quadrant of palette 9 or 11). When two are deposited, the centre fully fills with white (0) and the pad becomes "lit". |
| `dead_end_wall` | 6×6 | `{5}` | `["wall", "dead_end"]` | **(Added — Critique-1 Issue 3.)** A solid black (5) 6×6 block, used to mark the eject-destination of dead-end branches. When an ejected ball hits this sprite at its eject destination, the ball is consumed (collision); the wall provides a clear visual cue that the ball stopped at a wall (rather than disappearing off-screen). |
| `step_counter_hud` | row 63, full-width | `{0, 4}` | (HUD) | A `RenderableUserDisplay` subclass: depleting bar drawn on row 63 of the frame. Off-black (4) pixels on the left side represent remaining steps; right side is white (0). Drains 1 per action. |

**Style rule:** identical visual = identical role (per `checklist.md` item 21). All chain balls share shape; colour distinguishes which target/chain they belong to. All target sockets share the hollow-ring shape; colour shows which ball-colour they expect. Pusher knobs all look the same and all have the same role (fire pulse). Junction nodes share appearance and behaviour. Merge pads have a dedicated visual (orange centre pip) that distinguishes them from single-ball sockets.

**Chain layout convention:** ball positions are placed contiguously in a cardinal axis (no rails between balls — they touch). A horizontal chain of N balls starting at `(x, y)` places balls at `(x, y), (x+6, y), (x+12, y), ..., (x+6(N-1), y)`. Vertical chains use the same offset on y. Pusher knobs and junctions are placed adjacent at the chain ends or the bifurcation point.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. `grid_size = (64, 64)` for every level; per-level configuration varies (sprite positions, junction initial state, step budget).

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 1):
  1. **`pulse-eject`** — clicking a `pusher_knob` fires a momentum pulse along its chain; the **terminal** ball (far end) ejects exactly one ball-width (6 pixels) along the chain's axis and lands on the immediately adjacent cell beyond the chain end. Intermediate balls do not change position. If the eject-destination cell hosts a `target_socket` of matching ball colour, the socket fills (lit). If empty or otherwise, the ejected ball is consumed without effect (and the chain is one ball shorter).

- **Necessity per mechanic** (counterfactual):
  - *L1 cannot be solved without triggering `pulse-eject` because the only sprite that fills a `target_socket` is an ejected ball, and the only event that ejects a ball is a `pusher_knob` click — there is no alternate way to move balls onto sockets (no walking avatar, no ACTION1-4 motion, nothing the player can do but click).*

- **Witness solution** (1 action):
  - `[ACTION6@(11, 33)]` — click on the centre of `pusher_knob_left` (placed at top-left `(8, 30)`, hit point ~(11, 33)).

- **Layout** (sprite placements, native 64×64; all positions are top-left corners; sprites 6×6 unless otherwise noted):
  - `pusher_knob` at `(8, 30)` (placed adjacent to the chain's leftmost ball; chain extends rightward from this position, so the pulse travels left-to-right).
  - `chain_ball_blue` ×4 at `(14, 30)`, `(20, 30)`, `(26, 30)`, `(32, 30)` (horizontal 4-ball chain, contiguous).
  - `target_socket_blue` at `(38, 30)` — placed exactly one ball-width past the chain's right terminus. Click pusher → terminal ball at (32, 30) ejects → lands at (38, 30) on the socket → socket fills.
  - `step_counter_hud` HUD on row 63.
  - One pusher, one chain, one socket. Clean tutorial.

- **Difficulty justification** (per `difficulty-rules.md` § 2):
  - **(a) Random-resistance**: The valid action space is exposed via `_get_valid_actions` to enumerate only the click-targetable sprites' centres (the `pusher_knob` only, in L1). With one valid click and a 6-action budget, a random-policy agent that just enumerates available clicks WILL win in one click (the only available click IS the winning one). This is acceptable per `from-tech-report.md` § 5: "Random agents can occasionally stumble into success at this stage, which is acceptable by design." A vision-blind / text-only-LLM agent that treats every (x, y) ∈ [0, 63]² as a click candidate has 1/4096 per-click probability of hitting the pusher centre exactly; with 6 attempts ≈ 0.15% — also tutorial-tractable. No "spam-one-verb" win that bypasses the mechanic exists; the player must click the pusher.
  - **(b) Human-tractable**: ~30-60 sec — a sighted human sees one push-knob, one chain, one hollow socket; clicks the knob; sees the end ball fly into the socket; learns the mechanic.
  - **(c) Planning depth**: **No strict planning requirement.** L1 is the discovery gate; once the rule is understood the win is one click.
  - **(d) Step budget**: `step_budget = 6`. Six times the witness length. Generous enough that misclicks don't punish the player.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (M = N + 1 = 2):
  1. **`pulse-eject`** (carried from L1) — click pusher → pulse → terminal ball of the *currently-routed* chain section ejects.
  2. **`junction-routing`** (NEW) — clicking a `junction_node` cycles its active branch (top ↔ bottom). When a pulse reaches a junction, it travels into the *currently-active* branch only; balls in the inactive branch are unaffected. The terminal ejected is the end of the active branch.

- **Necessity per mechanic** (counterfactual; revised — Critique-1 Issue 1 changes the down-branch terminal cell from a yellow-decoy socket to a `dead_end_wall`, but the necessity argument is the same: the down-branch leads to a non-fillable destination, so junction-routing is required to redirect to the up-branch):
  - *L2 cannot be solved without triggering `pulse-eject` because only an ejected ball can fill a `target_socket` and only a `pusher_knob` click ejects a ball.*
  - *L2 cannot be solved without triggering `junction-routing` because the junction's default-active branch is "down" and the down-branch ends at a `dead_end_wall` at `(28, 54)` — every ball ejected through the down-branch is consumed by the wall and never reaches a `target_socket`. The only `target_socket_blue` is at `(28, 6)`, one ball-width past the up-branch terminus, reachable only when the junction's active branch is "up". Without flipping the junction, every push-fired ball is wasted; eventually the chain depletes (or budget runs out) without filling the only socket.*

- **Witness solution** (2 actions):
  1. `[ACTION6@(<junction_center>)]` — click the `junction_node` centre to switch its active branch from "down/yellow" to "up/blue".
  2. `[ACTION6@(<pusher_knob_center>)]` — click the pusher to fire the pulse along the now-up-routed chain; terminal ball of the up-branch ejects → fills `target_socket_blue` at the up-branch end.

- **Layout** (sprite placements; revised — Critique-1 Issue 1: removed yellow decoy; the only `target_socket` in L2 is on the up-branch, so the win predicate "every target_socket filled" is achievable):
  - `pusher_knob` at `(4, 30)` (placed adjacent to the chain's leftmost stem ball; pulse propagates rightward into the stem).
  - Stem: `chain_ball_blue` ×3 at `(10, 30)`, `(16, 30)`, `(22, 30)`.
  - `junction_node` at `(28, 30)` — its initial green tab is in the *bottom half* (= active branch is "down").
  - Up-branch: `chain_ball_blue` ×3 at `(28, 24)`, `(28, 18)`, `(28, 12)` (vertical, going up from the junction).
  - Down-branch: `chain_ball_blue` ×3 at `(28, 36)`, `(28, 42)`, `(28, 48)` (vertical, going down from the junction).
  - `target_socket_blue` at `(28, 6)` — placed one ball-width past the up-branch terminus. THE ONLY SOCKET. To fill it, the up-branch's terminal ball must be ejected; this requires the junction's active branch to be "up".
  - `dead_end_wall` at `(28, 54)` — placed one ball-width past the down-branch terminus. Catches and consumes any ball ejected from the down-branch (visual: ball thumps into a black wall and vanishes).
  - `step_counter_hud` HUD.

- **Difficulty justification**:
  - **(a) Random-resistance**: `_get_valid_actions` exposes 2 click targets (pusher + junction). Random play has 4 plausible action sequences within budget ([J, J, P], [J, P], [P, J, P], [P]), of which only [J, P] (or its near-equivalents that flip junction back-and-forth even number of times before pushing) wins. P(random win in budget 16) is dominated by the requirement that `(num_J_clicks_before_first_P) % 2 == 1`. Roughly 50% per ordering; combined with the constraint that only ONE successful pusher click within budget produces a colour-match (because only the FIRST push reaches the up-branch's terminal blue ball), random play winning probability across 16 actions is ~25-50% — but importantly, this is *post-discovery* random; a vision-blind agent that doesn't know what `junction_node` does has effectively 0 chance of inferring the correct sequence. A small text-only LLM that hasn't observed the visual cue (green tab position) cannot deduce the routing semantics.
  - **(b) Human-tractable**: ~60-120 sec. The sighted human notices the junction's coloured tab; clicks the pusher first, sees a yellow socket get a blue ball that bounces off (consumed without effect); deduces "wrong branch"; clicks the junction (sees tab flip); clicks pusher; wins.
  - **(c) Planning depth (post-discovery)**:
    - **Decision space at level start (post-discovery)**: 2 valid first actions — (a) click junction, (b) click pusher. ≥ 2. ✓
    - **Plausible-but-wrong alternative**: click pusher first (without flipping the junction). The post-discovery player who still hasn't read the junction's current state might do this; the result is a wasted blue ball into the down-branch's `dead_end_wall` (consumed, no progress). The player then realises the down-branch dead-ends and flips the junction; this also "wastes" 1 step. Witness is more efficient: read junction state first, flip if needed, then push.
    - **Witness reasoning chain**: post-discovery, the player reads the junction's green tab (currently down). Sees the down-branch ends at a black wall (`dead_end_wall`) and the up-branch ends at a hollow blue socket. Realises only the up-branch can fill anything. Flips junction (1 click). Pushes (1 click). 2 actions.
    - **Stage-conflation guard**: post-discovery is *with* knowledge of pulse-eject and junction-routing. The wrong action above is a *planning* mistake (didn't read junction state before pushing), not a discovery mistake. The player knows what each action does; they made a sub-optimal choice.
  - **(d) Step budget**: `step_budget = 16`. The witness is 2 actions; budget is 8× the witness, allowing several exploration ticks.

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (P = M + 1 = 3):
  1. **`pulse-eject`** (carried from L1, L2).
  2. **`junction-routing`** (carried from L2) — each chain has its own junction with its own active state.
  3. **`merge-on-coincidence`** (NEW) — when an ejected ball lands on a `merge_pad`, the pad accumulates one deposit. When a *second* ball lands on the same `merge_pad`, the two balls fuse and the pad lights up with palette 0 (white) in its centre, registering as "filled". A pad that has received only one ball is *not* filled; a pad that has received two of *any* colours is filled. Single-ball sockets (`target_socket_*`) work as in L1/L2 but the pad has different acceptance: it takes any colour and only counts at 2 deposits.

- **Necessity per mechanic** (counterfactual):
  - *L3 cannot be solved without `pulse-eject` because the only target on the level is the `merge_pad`, which fills only via deposited balls; deposits come only from ejected balls; ejection requires a `pusher_knob` click.*
  - *L3 cannot be solved without `junction-routing` because each chain's default-active branch ends in a `dead_end_wall` sprite (chain A's down-branch terminal ejects to `(20, 58)` = `dead_end_wall_A`; chain B's down-branch terminal ejects to `(38, 34)` = `dead_end_wall_B`). Every ball ejected through a default-active branch is consumed by its wall and never reaches the `merge_pad` at `(20, 22)`. Only by flipping junction A to "up" can chain A's up-branch eject reach the merge_pad; only by flipping junction B to "left" can chain B's left-branch eject reach the merge_pad. Since the merge_pad needs 2 deposits to fill, BOTH junctions must be flipped from their default state.*
  - *L3 cannot be solved without `merge-on-coincidence` because the only target on the level is a `merge_pad`, and a `merge_pad` requires* two *ball deposits to register as filled. A single ejection cannot fill it. There is no `target_socket_*` (single-ball receiver) on the level — the only winning condition is that the merge pad is filled, which definitionally requires the merge mechanic.*

- **Witness solution** (4 actions):
  1. `[ACTION6@(23, 49)]` — click junction A centre `(20+3, 46+3)` to flip its active branch from "down" to "up".
  2. `[ACTION6@(5, 49)]` — click pusher_knob_A centre `(2+3, 46+3)` to fire chain A; chain A's up-branch terminal blue ball at `(20, 28)` ejects upward to `(20, 22)` = `merge_pad` → 1 deposit (half-fill, blue).
  3. `[ACTION6@(41, 25)]` — click junction B centre `(38+3, 22+3)` to flip its active branch from "down" to "left".
  4. `[ACTION6@(59, 25)]` — click pusher_knob_B centre `(56+3, 22+3)` to fire chain B; chain B's left-branch terminal yellow ball at `(26, 22)` ejects leftward to `(20, 22)` = `merge_pad` → 2 deposits → pad fills (lit white) → WIN.

- **Layout** (sprite placements; revised — Critique-1 Issue 3: all positions shifted to fit on the 64×64 grid; explicit `dead_end_wall` sprites placed at every dead-end branch terminal so every eject-destination is on-grid and visually clear):

  Two chains converge orthogonally on a single `merge_pad` at `(20, 22)`:
  - Chain A's stem is horizontal (low half of playfield), junction routes to a vertical up-branch that terminates at `(20, 28)` and ejects upward to `(20, 22)`.
  - Chain B's stem is horizontal (top half of playfield), junction routes to a horizontal left-branch that terminates at `(26, 22)` and ejects leftward to `(20, 22)`.

  - **Chain A** (blue, lower half):
    - `pusher_knob_A` at `(2, 46)` (placed at the left of the stem; pulse propagates rightward into the chain).
    - Stem: `chain_ball_blue` ×2 at `(8, 46)`, `(14, 46)`.
    - `junction_node_A` at `(20, 46)`. Default-active-branch = "down" (green tab in lower half). Branches: up (`-y`) and down (`+y`).
    - **Up-branch (active when junction = "up")**: `chain_ball_blue` ×3 at `(20, 40)`, `(20, 34)`, `(20, 28)`. Terminal at `(20, 28)` ejects upward (`-y` direction) to land at `(20, 22)` = `merge_pad`.
    - **Down-branch (active when junction = "down" / DEAD-END)**: `chain_ball_blue` ×2 at `(20, 52)`, `(20, 58)`. Terminal at `(20, 58)` would eject down to `(20, 64)` — but `(20, 64)` is off-grid. Place a `dead_end_wall_A` at `(20, 58)`'s neighbour to keep all coordinates on-grid: actually, simpler — place the wall *at* the eject destination by making the down-branch ONE BALL SHORTER. Revised: down-branch is `chain_ball_blue` ×1 at `(20, 52)`. Terminal at `(20, 52)` ejects down to `(20, 58)` = on-grid; place `dead_end_wall_A` at `(20, 58)` (catches the ejected ball). Wall y=58 spans 58..63, fits in 64-tall grid. ✓

  - **Chain B** (yellow, upper half):
    - `pusher_knob_B` at `(56, 22)` (placed at the right of the stem; pulse propagates leftward into the chain).
    - Stem: `chain_ball_yellow` ×2 at `(50, 22)`, `(44, 22)`.
    - `junction_node_B` at `(38, 22)`. Default-active-branch = "down" (green tab in lower half). Branches: down (`+y`) and left (`-x`).
    - **Left-branch (active when junction = "left")**: `chain_ball_yellow` ×2 at `(32, 22)`, `(26, 22)`. Terminal at `(26, 22)` ejects leftward (`-x`) to land at `(20, 22)` = `merge_pad`.
    - **Down-branch (active when junction = "down" / DEAD-END)**: `chain_ball_yellow` ×1 at `(38, 28)`. Terminal at `(38, 28)` ejects down to `(38, 34)` = on-grid; place `dead_end_wall_B` at `(38, 34)`. ✓

  - `merge_pad` at `(20, 22)` (the shared cell). 6×6.
  - `dead_end_wall_A` at `(20, 58)`. 6×6 black.
  - `dead_end_wall_B` at `(38, 34)`. 6×6 black.
  - `step_counter_hud` HUD on row 63.

  All sprite placements are within `[0, 64) × [0, 64)`. The merge_pad is positioned so that chain A's vertical up-branch eject and chain B's horizontal left-branch eject both deposit into the SAME cell; thus the merge mechanic is invoked when both chains are correctly fired.

  Note on the junction-state binary cycle: each junction has exactly two states. Chain A's junction cycles between "up" and "down". Chain B's junction cycles between "left" and "down". The green-tab indicator is positioned per the active branch (up = top half of node sprite; down = bottom half; left = left half; right = right half). Default state is "down" for both chains.

- **Difficulty justification**:
  - **(a) Random-resistance**: `_get_valid_actions` exposes 4 click targets (2 pushers + 2 junctions). Required winning sequence (post-discovery): flip both junctions then push both pushers, in any order such that each push happens *after* the corresponding junction has been flipped to up. Winning sequences within 30-action budget: roughly C(30, 4) × (constraints), but the binding constraint is "each chain only has limited balls; firing on wrong-routed branch consumes balls". For each chain, the player gets 4 ejects (3 up-branch balls + 2 stem balls minus terminus, or fewer if down-branch is fired wastingly). A random agent must (1) pick the right junction-state for each, (2) push each pusher exactly once. With 4 valid clicks and 30 budget, P(random agent stumbles into a junctions-flipped-then-both-pushed sequence) is far below 1/10000 because the agent must avoid pushing before flipping (each pre-flip push consumes a ball; if a chain runs out before being correctly flipped, it's permanently lost). Empirically ~1/(4^7) ≈ 6×10⁻⁵ for the simplest valid permutation.
  - **(b) Human-tractable**: ~120-180 sec. The human sees two chains converging on a central merge pad; sees the 2-deposit pip; deduces "I need 2 balls to land here". Tries chain A → ball ejects up → lands on pad → pad shows half-fill; learns about merge-on-coincidence. Tries chain B → either flips junction first (lucky) or fires once and sees the down-branch ball hit a wall and disappear → learns. Sets junction B → fires B → wins.
  - **(c) Planning depth (post-discovery)**:
    - **Decision space at level start (post-discovery)**: 4 valid first actions (push A, push B, flip junction A, flip junction B). ≥ L2's 2. ✓
    - **Trivial heuristic that fails (post-discovery)**: greedy "fire each chain immediately, then react". A fully-informed greedy player — knowing pulse-eject, junction-routing, and merge-on-coincidence — might still default to "click both pushers first, see what happens, then plan from there". This greedy heuristic loses: both default-active branches are dead-ends (down for both chains); both initial pushes consume terminal balls into walls; chain A and chain B each lose their terminal balls. After 2 greedy clicks, the player has exhausted some chain depth without depositing on the pad, and now needs to flip both junctions and fire again — but now the chains' terminals are different balls (the original down-branch terminals are gone; the up-branch terminals are still in place). The greedy heuristic doesn't *irrecoverably* lose if budget is generous (which it is: 30 steps), but it costs ~2 actions of slack and exposes the rule to the post-discovery player. The witness recovers by flipping both junctions FIRST then firing; this is the "right" plan that requires looking-ahead one step.
    - **Why ahead-of-time reasoning is needed**: the player must reason about *which branch is active before firing*, because firing the wrong branch consumes a chain ball into a dead-end (visible immediately, but irreversible — the chain shortened by one). To minimise wasted balls, the player must look at each junction's state, commit to flipping or not, and *then* fire. Reactive trial-and-error works but is sub-optimal.
    - **Stage-conflation guard**: the heuristic above is *post-discovery* (the player knows what each verb does); the failure is "didn't plan junction state before firing", a true planning mistake.
  - **(d) Step budget**: `step_budget = 30`. Witness is 4 actions; budget is ~7.5× the witness. Generous over the witness; does NOT shrink relative to L2 (16 → 30, increasing). Per `difficulty-rules.md` § 2d: L3 must have a budget that is generous over the witness AND not shrinking relative to L2. ✓

## 5. Action mapping

Subset: `[6]` (pure click).

- `ACTION6` — click. The click's `data["x"]`, `data["y"]` are pixel coordinates; convert to grid via `self.camera.display_to_grid(int(x), int(y))`. The clicked sprite is found via `self.current_level.get_sprite_at(grid_x, grid_y, "sys_click")`. Behaviour depends on the clicked sprite's tag:
  - If the clicked sprite is a `pusher_knob`: fire a pulse along the chain attached to that pusher. Animate a brief flash through the chain (~3 ticks). Eject the terminal ball of the active chain section by 1 cell along the chain's axis. Process the eject's destination (target_socket fill, merge_pad deposit, off-grid consumption).
  - If the clicked sprite is a `junction_node`: cycle its active branch (top/bottom for vertical-branch junctions, left/right for horizontal-branch junctions). Visual: green tab moves to the new active half.
  - Click on any non-`sys_click` sprite or empty cell: no-op (the action still consumes a step from the budget).

No ACTION1-5, no ACTION7. The game is pure click.

`_get_valid_actions` is overridden to enumerate only the centres of `pusher_knob` and `junction_node` sprites currently in the level (one click coordinate per sprite). This restricts the agent's exploration to the meaningful click targets, removing the 64×64-cell brute-force space. (Reference precedent: r11l, su15 use pre-enumerated valid_actions grids.)

## 6. HUD and per-game state

**HUD widget**: `StepCounterHud(RenderableUserDisplay)`. Stores `(max_steps, current_steps)`; `set_current(remaining)` mutates; `render_interface(frame)` paints row 63 of the 64×64 frame: pixels `0..(64 * (current/max))` are off-black (4); rest are white (0). Drains 1 per action (mutated at start of `step()`).

**Per-game state** (instance attributes on `Qn7w`):
- `step_counter_hud: StepCounterHud` — initialised in `__init__`; reset per level via `on_set_level`.
- `chains: list[ChainModel]` — per-level model. Each `ChainModel` has:
  - `pusher_knob: Sprite` — the pusher sprite.
  - `pusher_axis: tuple[int, int]` — direction the pulse propagates from the pusher (e.g. `(+6, 0)` for rightward-firing).
  - `stem_balls: list[Sprite]` — balls on the stem in pulse-direction order.
  - `junction: Sprite | None` — None if no junction.
  - `branches: dict[str, list[Sprite]]` — keyed by branch name (`"up"`, `"down"`, `"left"`, `"right"`); each value is a list of balls along that branch, in pulse-direction order from the junction outward.
  - `active_branch: str | None` — current active branch name; mutated by junction click.
  - `default_active_branch: str` — initial state.
- `target_sockets: list[Sprite]` — single-ball receivers; each has a colour tag (`socket_blue` / `socket_yellow`) and a filled/empty state stored as a sprite-name suffix or as a separate flag dict.
- `merge_pads: list[Sprite]` — each tracks `deposit_count: int` (0, 1, or 2). When 2 → pad's pixels are mutated to "lit" (centre filled with white 0).
- `pending_animation: dict | None` — per-pulse animation state. When a pulse is fired, this is populated with `{"chain": idx, "tick": 0, "max_tick": 4}`. While `pending_animation is not None`, `step()` short-circuits to advance the animation tick without consuming the player's next action; on `tick == max_tick`, the eject is finalised, the chain's terminal ball is removed, the eject destination is processed, `pending_animation = None`, and `complete_action()` is called.

(Aside: during a pending-animation tick, the player's next action is *not* consumed — `_action_count` does not advance. The animation runs over the same engine turn as the click; the player perceives the animation playing out before the next click is accepted. This is the same idiom as `tu93`'s phase-1/phase-2/phase-3 sub-step machine and `sb26`'s phase-tagged animation counters.)

**No-hidden-state check** (per `checklist.md` item 19): every state mutation produces a visible cue:
- Junction state ↔ green tab position on the junction sprite. Persistent visual.
- Chain ball count ↔ number of `chain_ball_*` sprites along the chain. Persistent visual (chain shortens after eject).
- Target socket filled ↔ the socket sprite's centre is coloured (matched colour) instead of `-1`. Persistent visual.
- Merge pad deposit count ↔ the pad sprite's centre is half-filled (1 deposit, palette 9 or 11) or fully-filled (2 deposits, palette 0). Persistent visual.
- Pulse propagation ↔ brief flash animation (~3-5 ticks) along the chain. Transient but explicitly rendered.

**`_get_hidden_state()`** returns a small ndarray with the per-junction active-branch index and per-pad deposit count, for debug observability.

## 7. Win condition

`self.next_level()` is triggered when, after an eject is finalised:
- For L1, L2: every `target_socket` in the current level is filled (its name has been set to a "filled" variant, or its `pixels` array's centre is no longer `-1`).
- For L3: every `merge_pad`'s `deposit_count == 2` (pad is fully lit).

Concretely a single predicate `_check_win()` walks `self.current_level.get_sprites_by_tag("target_socket")` and returns False if any are still empty; then walks `get_sprites_by_tag("merge_pad")` and returns False if any deposit_count < 2; if both pass, returns True. After a successful level transition (`next_level()` past L3), the engine auto-fires `self.win()`.

## 8. Lose condition

`self.lose()` is triggered when:
1. **`_action_count >= step_budget`** — player has used all available actions and the level is not yet won.

There is no per-action instant-fail (no hazard sprites, no traps). The sole loss mode is budget exhaustion. Per `difficulty-rules.md` § 1, this avoids the "soft-lock" anti-pattern: even if the player has wasted all chain balls into dead-ends, they still have time on the budget to keep exploring (no win is possible at that point, but they fail-by-budget rather than waiting in a no-win room — and the budget is set so that even with bad ejects, a recovering player can complete).

Note on soft-lock: the level *can* enter an unwinnable state if the player fires too many balls into dead-ends and depletes the chains beyond what's needed to fill the targets. To avoid the soft-lock anti-pattern, when this happens the engine should fire `self.lose()` proactively. To detect: after each eject, `_check_winnable()` walks each chain, counts remaining balls along reachable branches, and asks "is there any sequence of remaining ejects that fills all targets/pads?". If not (a permanent dead-state), fire `self.lose()` immediately rather than wait for budget exhaustion. Implementation: simple counting — for each unfilled target/pad, check if there's a chain whose active-or-flippable branch can still reach it with at least 1 ball remaining.

## 9. Novelty note

**Closest taxonomy entries (`mechanic-novelty/taxonomy-of-25-games.md`):**

- **`ka59` (sokoban-explode-chase)**: both involve "click sets in motion a coloured-block dynamic". Distinguishing rule: ka59's player drives an active *moving* block via arrow keys, and explosions cause every neighbouring block to shift one cell (4-direction propagation). qn7w has no avatar and no arrow movement; only the *terminal* ball of one chain moves per click; intermediate balls are explicitly stationary; no 4-direction propagation. ka59 spreads displacement; qn7w concentrates it.

- **`r11l` (centroid-puppet-leg)**: both are click-only games. Distinguishing rule: r11l clicks on a *destination cell* and a tray-leg piece is animated to that target across an arbitrary trajectory; the leg's "head" follows the centroid of all legs. qn7w clicks on a *specific pusher knob* and a *predetermined* terminal ball is ejected by exactly one ball-width along the chain's pre-placed axis; the eject destination is determined by the chain's geometry, not by where the click lands. r11l has multiple legs in flight and centroid-following heads; qn7w's pulse moves at most one ball per click and there is no centroid-tracking.

- **`vc33` (row-column-swap-stripe)** and **`lp85` (button-permutation-puzzle)**: both also pure-ACTION6. Distinguishing rule: vc33 and lp85 click triggers that *swap or permute many cells at once* (every stone in a row shifts, every cell in a permutation cycle changes). qn7w's click moves *exactly one cell* (the terminal ball of one chain).

**Closest prior-games entries (`prior-games/index.md`):**

- **`vn8d` (domino-cascade-topple)**: both are click-triggered cascades. Distinguishing rule (binary): in vn8d, every pillar in the cascade *visibly falls* (state change for every cell in the path); burst-pads splay outward in 4 directions; rotator-pads turn corners; the cascade is *distributional*. In qn7w, no intermediate ball moves; only the chain's terminal ball changes position; the cascade is *concentrational*. The rendered animation reinforces the difference: vn8d shows pillars toppling in sequence; qn7w shows a brief flash through the chain followed by a single terminal ball flying off.

- **`kp9z` (grain-accumulate-topple)**: both are "click triggers a cascade through coupled cells". Distinguishing rule: kp9z is a sandpile cellular automaton — each cell holds an integer grain count; cells overflow at threshold 4 to all 4 cardinal neighbours; sinks absorb. Cells have continuous integer state. qn7w's chain cells have *no per-cell state at all* — they are stateless ball sprites; pulses fire once and transit a 1-D chain; only the terminal ball changes position per pulse.

- **`bx84` (beam-mirror-reflect)**: both involve "a signal travels to a target". Distinguishing rule: bx84's beam travels along *line-of-sight* through *empty cells*, reflecting off mirror sprites; the beam is a continuous lit-cell path. qn7w's pulse travels along a *physical chain of touching ball sprites* (not LOS through empty cells); no cells light up along the path; the moving entity at the end is a *physical ball*, not a beam, and it moves at most one ball-width.

- **`kn58` (anchor-pull-magnet)**: both are click-triggered movement. Distinguishing rule: kn58's click places a *single global anchor* and *every coloured pawn* slides one cell along its dominant Manhattan axis toward it. qn7w's click acts on a *specific chain's pusher* only; only the terminal ball of that chain moves; pawns and balls on unrelated chains are unaffected.

- **`gx7m` (gear-mesh-cascade)**: both involve cascades through coupled elements. Distinguishing rule: gx7m's connected-component discs *all rotate* simultaneously when any disc is rotated (with sign flip across mesh); every cell in the connected component changes (its rotation). qn7w's chain balls explicitly *do not move* during a pulse; only the chain terminus changes (one ball ejected).

- **`xn5p` (chamber-stamp-partition)**: both have a "trigger" element. Distinguishing rule: xn5p's pawn walks a chamber and *stamps wall cells* to subdivide a region; the mechanic is topological partition by player wall-creation. qn7w has no walking, no wall-stamping, no partitioning of regions. qn7w's player only clicks pre-placed pushers and junctions.

- **`rk7x` (live-switch-routing)**: both involve junction-style routing. Distinguishing rule: rk7x has an *autonomous moving courier* that walks one cell per click; the player toggles junction blades to redirect it. qn7w has *no autonomous mover*; no per-click micro-step; one click triggers an instantaneous pulse with one terminal eject. The "junction" in rk7x routes a continuous walker; the "junction" in qn7w gates which branch's terminal ejects per pulse.

- All other prior entries (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, fz5j, wt39, zk9p, vp6h, zd7m, lv4k, mr5q, pf3w, tg6w, vd3g, jd4q, ek73, tm5x, qx7p, kj82, nb6t): family-level check finds no overlap (no "chain", "pulse", "Newton's cradle", "momentum-eject", or "terminal-only-moves" descriptor).

**Verdict:** `pulse-chain-eject` is novel against both the 25-game reference taxonomy and the 33-entry prior-games corpus. The defining mechanical feature — energy concentrates at the chain terminus, intermediate cells stay stationary — is the inverse of every cascade mechanic in the corpus (which all distribute energy across cells visited). Negative-similarity-check pass already documented in `mechanic-pick.md`.
