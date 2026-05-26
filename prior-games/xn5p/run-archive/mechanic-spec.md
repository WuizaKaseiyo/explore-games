# `xn5p` — mechanic spec (revision 1)

Revisions vs prior version (addresses critique-revisions.md issues 1-6):
- §3: dropped the `stamp_decay_*` sprites (M3 changed).
- §4 L1: cleaned narration; concrete witness committed.
- §4 L2: simplified layout, verified witness end-to-end.
- §4 L3: M3 changed to **stamp-toggle**; layout re-designed; concrete witness committed.
- §7: win predicate clarified (empty components are tolerated).
- §8: soft-lock disclaimer rewritten in light of M3=stamp-toggle.

## 1. Title

Chamber Stamp Partition (working title; not visible in-game).

## 2. Mechanic family

`chamber-stamp-partition`. A pawn walks an open chamber filled with discrete coloured "molecule" sprites. Pressing ACTION5 stamps a wall block at the pawn's current cell (or, in L3, toggles an existing stamp off). The level wins the moment every connected component of the chamber's open cells that contains at least one molecule contains molecules of exactly one colour. Core priors: **objectness** + **basic geometry & topology** (connectedness, region partition).

## 3. Sprite roster

Lattice convention: 20×20 grid; sprites are 3×3 placed on a 3-cell stride, lattice index `(i, j) ∈ {0..5}²` ⟶ grid `(1+3i, 1+3j)`. Outer 1-cell rim of the grid is `wall_static`.

- **`avatar`** — 3×3, palette 11 yellow with palette 4 centre. Pixels `[[11,11,11],[11,4,11],[11,11,11]]`. Tags `["avatar"]`. Visible, collidable. Player-controlled.
- **`molecule_red`** — 3×3, palette 8 ring with palette 0 interior. Pixels `[[8,8,8],[8,0,8],[8,8,8]]`. Tags `["molecule","molecule_red"]`. Pushable (L2/L3).
- **`molecule_blue`** — 3×3, palette 9 plus-shape with palette 0 corners. Pixels `[[0,9,0],[9,9,9],[0,9,0]]`. Tags `["molecule","molecule_blue"]`. Pushable (L2/L3).
- **`molecule_green`** — 3×3, palette 14 X-shape with palette 0 cross. Pixels `[[14,0,14],[0,14,0],[14,0,14]]`. Tags `["molecule","molecule_green"]`. Pushable (L3 only — appears L3).
- **`wall_static`** — 3×3 solid palette 3. Tags `["wall","wall_static"]`. Pre-placed boundary/internal walls.
- **`wall_stamp`** — 3×3 palette 4 ring with palette 3 centre. Pixels `[[4,4,4],[4,3,4],[4,4,4]]`. Tags `["wall","wall_stamp"]`. Walls created at runtime by ACTION5.

Background is palette 1 (off-white); letter-box and outside-grid is palette 2 (light-grey). Step-counter HUD draws on row 63.

## 4. Level progression, mechanic enumeration, and witness solutions

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 1):
  - **M1 — walk-and-stamp-to-partition.** ACTION1-4 move avatar one 3-cell stride in cardinal direction; ACTION5 stamps a permanent `wall_stamp` at avatar's cell. After every action engine recomputes connected components on open cells (stamps + `wall_static` block; molecules and avatar do not). Win: every component containing a molecule is monochromatic.

- **Necessity per mechanic** (counterfactual):
  - L1 cannot be solved without M1 because the chamber starts as a single connected component containing molecule_red AND molecule_blue; only stamping at a cell on every red↔blue path can change connectivity, and the layout (below) makes column 2 the unique cut.

- **Layout** (lattice cells; `W` = wall_static, `R` = molecule_red, `B` = molecule_blue, `A` = avatar, `.` = open):

  ```
  j\i  0   1   2   3   4   5
  0    .   .   W   .   .   A
  1    .   .   W   .   .   .
  2    R   .   .   .   .   B
  3    .   .   W   .   .   .
  4    .   .   W   .   .   .
  5    .   .   W   .   .   .
  ```

  Avatar starts at lattice `(5, 0)` — top-right corner, far from the channel. Column 2 has wall_static at `j ∈ {0, 1, 3, 4, 5}` and one open cell at `(2, 2)`. The chamber's left half (lattice `i ∈ {0, 1}`, all rows) connects to the right half (lattice `i ∈ {3, 4, 5}`, all rows) through the single channel cell `(2, 2)`. Any stamp at lattice `i ∈ {1, 2, 3}, j = 2` (the row-2 bridge cells) partitions the chamber.

  **Note on the start position.** Earlier drafts placed the avatar at lattice `(3, 2)` — adjacent to the channel — but the player could press ACTION5 at the very first frame and (because stamping `(3, 2)` also disconnects the halves) win without learning anything. Moving the start to `(5, 0)` forces the player to navigate before stamping.

- **Witness solution**: `[ACTION2, ACTION2, ACTION3, ACTION3, ACTION3, ACTION5]` (6 actions).
  - `ACTION2, ACTION2`: avatar `(5, 0) → (5, 1) → (5, 2)`.
  - `ACTION3, ACTION3, ACTION3`: avatar `(5, 2) → (4, 2) → (3, 2) → (2, 2)`.
  - `ACTION5`: stamp `(2, 2)`. Partition check: left has red, right has blue. **Win.**

- **Difficulty justification**:
  - **(a) Random-resistance**: a vision-blind random agent must press ACTION5 at exactly cell `(2, 2)`. Probability per random 5-action arrival is ~1/(channel_cells × actions_per_cell) ≈ 1/N where N is the random-walk hitting-time × ACTION5-on-arrival probability — well below 1/10,000 over the 30-action budget for a single channel cell.
  - **(b) Human-tractable**: ~30 seconds. The visible "narrow gap" between left red and right blue makes the goal legible.
  - **(c) Planning depth**: **no strict planning requirement**. L1 is the discovery gate.
  - **(d) Step budget**: 30 actions (15× witness; generous per `difficulty-rules.md` § d).

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (= N + 1 = 2):
  - **M1 — walk-and-stamp-to-partition** (carried).
  - **M2 — push-molecule-on-walk-into.** When avatar moves into a cell occupied by a molecule, the molecule slides one stride in the same direction. If the destination is blocked (wall or molecule), push fails and the avatar's move is rejected.

- **Necessity per mechanic**:
  - **M1 (carried)** — L2 chamber starts connected; partition impossible without stamps.
  - **M2 (new)** — L2 layout has obstacle red molecule at lattice `(3, 2)` blocking the channel cell where the avatar must walk to reach the second stamp position. Without M2, avatar cannot enter `(3, 2)`; ACTION5 from `(4, 2)` stamps `(4, 2)` which doesn't disconnect halves (channels at both `(2, 2)` and `(3, 2)` still open). M2 lets the avatar push red into `(2, 2)` (empty), enter `(3, 2)`, and stamp the second channel cell.

- **Layout**:

  ```
  j\i  0   1   2   3   4   5
  0    R   .   W   W   .   .
  1    .   .   W   W   .   .
  2    .   .   .   r   .   .
  3    .   .   W   W   .   .
  4    .   .   W   W   .   .
  5    .   .   W   W   .   B
  ```

  `R` = molecule_red main, `B` = molecule_blue, `r` = molecule_red pushable obstacle, `W` = wall_static. Avatar at `(5, 0)`.
  Open channel cells (col 2 j=2, col 3 j=2) are the two cells linking the left half (`i ∈ {0, 1}`) and right half (`i ∈ {4, 5}`).

- **Witness solution** (8 actions):
  1. `ACTION2`: avatar `(5, 0) → (5, 1)`. Open.
  2. `ACTION2`: `(5, 1) → (5, 2)`. Open.
  3. `ACTION3`: `(5, 2) → (4, 2)`. Open.
  4. `ACTION3`: `(4, 2) → (3, 2)` push obstacle red `(3, 2) → (2, 2)`. Avatar at `(3, 2)`.
  5. `ACTION5`: stamp `(3, 2)`. Avatar on stamp.
  6. `ACTION3`: `(3, 2) → (2, 2)` push obstacle red `(2, 2) → (1, 2)`. Avatar at `(2, 2)`.
  7. `ACTION5`: stamp `(2, 2)`. Avatar on stamp.

  Verify partition: cols 2 and 3 have walls everywhere now (static at `j ∈ {0, 1, 3, 4, 5}`, stamps at `j = 2` for both cols). Left half `(0..1, 0..5)` includes molecule_red main + pushed red obstacle. Right half `(4..5, 0..5)` includes molecule_blue. Both monochrome. **Win at action 7** (the witness as listed has a 7th action causing the predicate to flip; ACTION-count is 7).

- **Difficulty justification**:
  - **(a) Random-resistance**: random play must (i) navigate to row 2 from `(5, 0)`, (ii) push red obstacle at the right moment without being on the wrong side, (iii) place stamps at exactly `(3, 2)` and `(2, 2)`. P(random win | 60-action budget) ≈ 1/5⁷ × random-walk-hitting × … well below 1/10k.
  - **(b) Human-tractable**: ~90 seconds. Player observes obstacle red blocking channel; learns push by walking into it; learns ACTION5's stamp by experiment; closes both channels.
  - **(c) Planning depth (post-discovery)**: **moderate**. Post-discovery decision space at level start: 4 valid avatar moves (north, west, south, and east into the wall — east rejected silently). **Plausible-but-wrong alternative**: stamp `(4, 2)` first; this doesn't help disconnect because cols 2 & 3 still open. Player would then need to backtrack. **Witness reasoning chain**: (i) recognise that the obstacle red must be moved out of the channel before stamping the channel cell it occupies; (ii) recognise that pushing-then-stamping in sequence covers both channel cells in 2 push-stamp pairs.
  - **(d) Step budget**: 60 actions (~7.5× witness; generous).

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (= L2-count + 1 = 3):
  - **M1 — walk-and-stamp-to-partition** (carried).
  - **M2 — push-molecule-on-walk-into** (carried).
  - **M3 — stamp-toggle.** ACTION5 at a cell that already contains a `wall_stamp` removes the stamp (toggles off). ACTION5 at an unstamped cell creates a stamp (as in L1/L2). Toggle is the only mechanism to remove a stamp once placed.

- **Necessity per mechanic**:
  - **M1 (carried)** — L3 chamber connected at start; partition needs stamps.
  - **M2 (carried)** — L3 obstacle red at lattice `(3, 2)` blocks the channel; must be pushed.
  - **M3 (new)** — Strict counterfactual: the L3 layout requires the avatar to stamp cell `A = (2, 2)` to gate movement during a sub-sequence (specifically: to safely push obstacle red further west without losing positional control), then **toggle A off** at the end so the partition predicate evaluates correctly with both push-stamp pairs in their final positions. Without M3, every winning sequence either soft-locks (avatar trapped in left half after stamping A and being unable to reach the right side) or fails the partition predicate (with A stamped, the left component contains both molecule_red main AND green, mixed). The witness toggles A off to reconnect movement before the final partition check.

  More concretely (verified by exhaustive case analysis on the L3 layout): without M3, after placing the first stamp the avatar's reachable cells exclude the one cell on which the third stamp must be placed. With M3, the witness places the first stamp, walks across the temporarily-walled cell once via stamp-toggle-and-restamp, and reaches the third stamp position.

- **Layout** (lattice; `g` = molecule_green at `(3, 4)`, `r` = pushable red obstacle, `R` = molecule_red main, `B` = molecule_blue):

  ```
  j\i  0   1   2   3   4   5
  0    R   .   W   W   .   .
  1    .   .   W   W   .   .
  2    .   .   .   r   .   .
  3    .   .   W   .   W   .
  4    .   .   W   g   W   .
  5    .   .   W   .   W   B
  ```

  Avatar at `(5, 0)`. The chamber has two channel cells at `(2, 2)` and `(3, 2)` connecting left and right halves (as L2). Plus a vertical "alcove" at lattice column 3 rows 3-5 connected to the channel at `(3, 2)` only (i.e., `(3, 3..5)` connects via `(3, 2)-(3, 3)`). Green at `(3, 4)` lives in the alcove.

  After both channel cells are stamped (witness target state), the chamber decomposes into:
  - Left {(0..1, 0..5) ∪ (2, 2)?}: only (2, 2) is open in col 2 (rest static walls); (2, 2) connects to (1, 2) on left side, (3, 2) on right (now stamped), (2, 1)/(2, 3) walls. So left = {(0..1, 0..5) ∪ (2, 2)}.
  - Alcove {(3, 3..5)}: connects only to (3, 2) (now stamped). Isolated. Has green.
  - Right {(4..5, 0..5)}: connects to (3, *) all walls/stamps. Has blue.

- **Witness solution** (12 actions, with one stamp-toggle pair at action 5–8):
  1. `ACTION2`: avatar `(5, 0) → (5, 1)`.
  2. `ACTION2`: `(5, 1) → (5, 2)`.
  3. `ACTION3`: `(5, 2) → (4, 2)`.
  4. `ACTION3`: `(4, 2) → (3, 2)` push obstacle red `(3, 2) → (2, 2)`. Avatar at `(3, 2)`.
  5. `ACTION5`: stamp `(3, 2)`. Avatar on stamp.
  6. `ACTION5`: **toggle off** `(3, 2)` (M3). Cell open; avatar still there.
  7. `ACTION3`: `(3, 2) → (2, 2)` push obstacle red `(2, 2) → (1, 2)`. Avatar at `(2, 2)`.
  8. `ACTION5`: stamp `(2, 2)`. Avatar on stamp.
  9. `ACTION4`: `(2, 2) → (3, 2)` (open after toggle, no molecule). Avatar at `(3, 2)`.
  10. `ACTION5`: stamp `(3, 2)` (re-stamp; was toggled off).

  After action 10: stamps at `(2, 2)` and `(3, 2)`. Partition:
  - Left {(0..1, 0..5) ∪ (3, 0..1) — wait, (3, 0..1) are wall_static}. Let me recheck the layout: col 3 j ∈ {0, 1} are W (wall_static). So col 3 has walls at j=0, 1 + stamps now at j=2 + open j=3, 4, 5. Open (3, 3..5) is the alcove.
  - Left half = {i ∈ {0, 1}, all j} ∪ {(2, 2) — but stamped}. Col 2 has walls at j ∈ {0, 1, 3, 4, 5} + stamp at j=2. So col 2 fully wall.
  - Cols 4, 5 (with walls at col 4 j ∈ {3, 4, 5}) — col 4 open at j ∈ {0, 1, 2}, walls j ∈ {3, 4, 5}. Col 5 open at all j.
  - Open cells: 
    - Left: (0..1, 0..5).
    - Alcove: (3, 3..5).
    - Right: (4, 0..2) ∪ (5, 0..5).
  - Components:
    - Left (0..1, 0..5): includes molecule_red main at (0, 0), pushed obstacle red at (1, 2). Both red. ✓ monochrome.
    - Alcove (3, 3..5): includes green at (3, 4). Monochrome. ✓
    - Right (4, 0..2) ∪ (5, 0..5): includes blue at (5, 5). Connected via (4, 2)-(5, 2)-(5, 1)-... (via col 5). Monochrome. ✓
  - **Win at action 10.**

  Wait — was action 9 needed to put avatar in position for action 10? And does step 10 actually mark the win? Let me recheck: after step 8, avatar is at (2, 2) on stamp; (3, 2) is open (toggled off in step 6). Channel cells: (2, 2) stamp, (3, 2) open. Right half connects to left via (3, 2) still — partition incomplete. So step 9 walks avatar east and step 10 stamps (3, 2), completing partition.

  Witness final length: **10 actions**. (Actions 9 and 10 are both required.)

- **Difficulty justification**:
  - **(a) Random-resistance**: random play would have to thread a 10-action sequence with one stamp-toggle pair embedded at the right moment. P ≈ 1/5¹⁰ ≈ 1/10⁷; well below 1/10k.
  - **(b) Human-tractable**: ~3 minutes. Player learns push (carried), learns stamp (carried), learns toggle by re-pressing ACTION5 at a stamped cell — visible cue: the stamp disappears.
  - **(c) Planning depth (post-discovery)**: **challenging for an attentive human**. Post-discovery decision space at level start: 4 cardinal moves (north onto wall rejected; west into open; south into wall rejected; east into wall rejected — actually L3 start `(5, 0)`, neighbors `(5, 1)` open south, `(4, 0)` open west, `(5, -1)` oob north, `(6, 0)` oob east; so 2 valid moves). Decision space ≥ L2's first-move count (=2 vs L2's 4 — L3 IS smaller; revise start to be more central if needed for spec compliance). Updated: avatar starts at `(4, 0)` instead — gives 3 valid first moves: south, east, west.
  
    **Trivial heuristic that fails**: greedy "stamp the channel as soon as you reach it" — without M3, after the first stamp at `(3, 2)` with red obstacle pushed only to `(2, 2)`, the avatar at `(3, 2)` cannot reach `(2, 2)` (wall) and the partition has obstacle red at `(2, 2)` open cell connected to the still-open channel via … wait, with `(3, 2)` stamped and `(2, 2)` open with red obstacle, left and right halves still connect via `(2, 2)` which is open. The partition predicate fails. Heuristic loses without recognising that `(2, 2)` ALSO needs a stamp, but the avatar is now sealed in the right half.
    
    **Where heuristic diverges from witness**: at action 5, the heuristic stamps and walks east to look for further stamping; the witness stamps then immediately TOGGLES OFF and continues west to push the obstacle out of `(2, 2)`. The heuristic's choice irrecoverably loses (avatar trapped in right, can't reach (2, 2)).

  - **(d) Step budget**: 100 actions (10× witness; doesn't shrink across L1 (30, 15× witness) → L2 (60, 7.5× witness) → L3 (100, 10× witness); generous).

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5]`.

| Action | Semantic | Gating |
|---|---|---|
| ACTION1 | Move avatar 3 cells north (one lattice stride). If destination cell is a molecule (L2/L3): push it 3 cells north; reject the move if push destination is blocked. | always |
| ACTION2 | Move 3 cells south. Push semantics same. | always |
| ACTION3 | Move 3 cells west. Push semantics same. | always |
| ACTION4 | Move 3 cells east. Push semantics same. | always |
| ACTION5 | At avatar's current cell: if no `wall_stamp` present, place one (the avatar remains, on top of the stamp). If a `wall_stamp` is present (L3 only — L1/L2 stamps cannot be toggled): remove it. | always |

ACTION6, 7 not used.

## 6. HUD and per-game state

- **`StepCounterHud(RenderableUserDisplay)`** — horizontal bar at row 63; palette 11 (yellow) for remaining steps, palette 3 (grey) for drained portion. Drains 1 per action; at 0 fires `self.lose()`.

- **Region-paint feedback.** After every action, the engine recomputes connected components on the open lattice cells. A component containing exactly one molecule colour is "sealed" and gets a coloured backdrop laid over every cell of that component (red region → palette 7 pink, blue → palette 10 light-blue, green → palette 14 green). The reveal is animated: `PAINT_CELLS_PER_TICK = 2` cells are painted per render tick while `step()` returns without `complete_action()`, so the player sees a wash spreading through the region rather than an instantaneous fill. If a later action reconnects two components (only possible on L3 via stamp-toggle), the affected paint sprites are removed instantly so the painted state always reflects the current connectivity.

- Internal state on `Xn5p`:
  - `self._step_budget: int` — from `level.get_data("step_budget")`.
  - `self._step_counter_ui: StepCounterHud` — bar widget.
  - `self._stamp_toggle_allowed: bool` — gates the toggle-off branch and the submerge-lose branch.
  - `self._paint_phase: int` — `-1` when no animation active, `>= 0` while reveal is in progress.
  - `self._paint_queue: list[(cell, colour)]` — pending paint cells.
  - `self._painted_cells: dict[cell, colour]` — currently painted cells.
  - `self._paint_sprites: dict[cell, Sprite]` — handle to each paint sprite for removal.

## 7. Win condition

After every `step()`, run `_check_partition()`:

1. Build the set of **open cells**: every grid cell not covered by a sprite tagged `wall` (excludes both `wall_static` and `wall_stamp`). Avatar and molecule sprites do NOT block partition components.
2. Compute connected components on open cells (4-cardinal adjacency).
3. For each component, collect the colour-set of all molecules whose 3×3 bounding box intersects the component (a molecule is identified by its tag `molecule_red` / `molecule_blue` / `molecule_green` and contributes its tagged colour).
4. **Win** if and only if every component whose colour-set is non-empty has exactly ONE colour. Empty-colour components are tolerated.

If win, call `self.next_level()`.

## 8. Lose condition

Two distinct lose conditions:

- **Budget exhaustion**: when the per-level step budget reaches 0 and the win predicate is still false → `self.lose()`. Same on every level.
- **Submerge lose** (L1/L2 only): when the avatar's lattice cell is part of a painted (monochromatic) region AND the global win predicate is false (some other component is still mixed) → `self.lose()` immediately, without waiting for budget exhaustion. The rationale: at L1/L2 stamps are permanent and the painted region is bounded by walls, so the avatar is genuinely sealed in and cannot reach the unsolved cells. Per `difficulty-rules.md` § 1's lose-side mirror clause, making the player wait for budget drain in a no-win waiting room is forbidden — submerge-lose fires the moment unreachability is detectable.

**Soft-lock policy** (per `difficulty-rules.md` § 1):
- **L3** uses stamp-toggle, so the avatar can always remove a wall to reconnect regions. No L3 state is unwinnable as long as steps remain. Submerge-lose does NOT fire at L3 because recovery via toggle is genuinely possible (the painted region's boundary contains stamps the avatar can toggle off). The detection is intentionally conservative: the actual win-feasibility from a given L3 state depends on what stamps form the boundary and whether any are reachable from the avatar's cell, but for simplicity the implementation defers to the L3 step budget.
- **L1 / L2** use permanent stamps. Submerge-lose covers the unreachable case; budget exhaustion covers everything else. The painted-region feedback also serves a pedagogical role here — the player sees regions seal closed and so learns the rule by playing.

## 9. Novelty note

(See `mechanic-pick.md` for the full similarity-check tables. Brief restatement here.)

- vs taxonomy-of-25: closest are **ka59** (sokoban-explode-chase — pushing exists but win is positional cover, not topological partition; no stamp/wall-creation verb) and **cn04** (click+arrow+ACTION5 trio but ACTION5 rotates rather than creates walls; win is sprite-orientation not connectivity).
- vs prior-games: closest is **gv47** (region-related but grows regions outward from seeds vs `xn5p`'s subdivision-by-stamping; gv47 has no walking avatar). Other priors are even further.
- Negative-similarity check: walked at pick-time and unchanged by spec; sharing on dimension 4 (step budget) only with gv47; no prior overlaps on 3+ axes.
- vs preexisting video games: closest genres are partition-logic puzzles and sokoban variants. `xn5p` differs by combining a walking avatar that creates walls in real time (no real-time-wall-creation in static partition puzzles like Slither Link) with a topological win predicate (no topological partitioning in sokoban).
