# vd3g — `valley-dig-roll` spec

## 1. Title
Mound-and-Marble Routing (working title; not visible in-game).

## 2. Mechanic family
Click on a playfield cell to toggle its binary terrain state
HIGH↔LOW. After every click, marbles flow downhill along the
gradient: a marble on a HIGH cell with at least one cardinal LOW
neighbour rolls into that neighbour (priority N→E→S→W); a marble
on a LOW cell stays put. Two marbles cannot share a cell. Walls
are immutable HIGH cells; targets are immutable LOW cells with a
coloured ring matching one marble's hue. Linked-anchor pairs
(L3) toggle together regardless of distance. Priors used:
**physics** (gravity along a local gradient), **objectness**
(persistent identity-bearing marbles), and **topology** at L2/L3
(walls and remote-linked cells).

## 3. Sprite roster

All sprites are 4×4 display pixels (one logical cell). The
playfield is a single 64×64 `terrain` sprite whose pixels are
mutated each turn to reflect cell types; marble sprites are
4×4 movable overlays placed at multiples of 4. The game uses
grid_size `(16, 16)` for all three levels — the camera is
re-sized to `(16, 16)` in `on_set_level` so its 4× internal
scale produces a rich-pixel 64×64 frame; cells are NOT
flat-coloured blocks (every cell type has internal palette
variation, satisfying checklist item 20).

- **`terrain`** — a 16×16 cell-pattern canvas (rendered by
  stamping 4×4 cell patterns into the sprite's `pixels` array;
  one canvas sprite, layer 0). Always tangible. `tags=["terrain"]`.
  Pixel patterns drawn into the canvas per cell type:

  - LOW (basin): `[[12,11,11,12],[11,1,1,11],[11,1,1,11],[12,11,11,12]]`
    — orange rim with cream interior; reads as "shallow basin /
    cleared ground".
  - HIGH (mound): `[[4,3,3,4],[3,2,2,3],[3,2,2,3],[4,3,3,4]]` —
    grey stone bump with darker corners; reads as "raised
    terrain / un-walkable hump for a marble that has nowhere
    to roll".
  - WALL (immutable HIGH): `[[5,5,5,5],[5,4,4,5],[5,4,4,5],[5,5,5,5]]`
    — solid black with off-black inner; visually heavier and
    distinct from HIGH. Player learns it cannot be toggled.
  - TARGET-LOW for each marble hue C (red 8, blue 9, green 14,
    yellow 11, purple 15): `[[C,C,C,C],[C,1,1,C],[C,1,1,C],[C,C,C,C]]`
    — coloured ring around cream interior; reads as "the home
    basin for the matching-coloured marble".
  - ANCHOR-LOW with cap colour D (magenta 6 or pink 7):
    `[[D,11,11,12],[11,1,1,11],[11,1,1,11],[12,11,11,12]]` — basin
    with a single tinted top-left corner pixel.
  - ANCHOR-HIGH with cap colour D:
    `[[D,3,3,4],[3,2,2,3],[3,2,2,3],[4,3,3,4]]` — stone bump
    with a single tinted top-left corner pixel. Two anchors
    sharing the same cap colour are linked — toggling one
    auto-toggles the other.

- **`marble_red`**: 4×4 with palette 8 (red) and one palette-1
  off-white sparkle pixel.
  `[[-1,8,8,-1],[8,1,8,8],[8,8,8,8],[-1,8,8,-1]]`. Tag `marble`,
  layer 1. Carries identity attribute "red" for target matching.
- **`marble_blue`**: same shape, palette 9.
  `[[-1,9,9,-1],[9,1,9,9],[9,9,9,9],[-1,9,9,-1]]`.
- **`marble_green`**: palette 14. (Used at L3.)
  `[[-1,14,14,-1],[14,1,14,14],[14,14,14,14],[-1,14,14,-1]]`.

(L1 uses red only; L2 uses red only; L3 uses red and blue.)

**Marble-hue ↔ target-ring-hue is the load-bearing visual pairing
across all three levels** [**Revision Issue 4**: explicit per
checklist item 21(2) — identical visuals imply correlated roles].
The player learns at L1 that the red marble seeks the red ring;
at L2 the same pairing carries forward (red marble → red ring
target); at L3 the rule generalises (each marble seeks its
matching-hue ring). The hue is the primary visual channel for the
"this marble belongs to this target" correlation — no other cue is
needed.

Sprite roles:
- `terrain` — passive canvas; mutated on every click.
- Marbles — movable identity-bearing pawns with target affinity.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels use `grid_size=(16, 16)`. The outer ring
(cells where col∈{0,15} or row∈{0,15}) is WALL on every level
to enforce a clean playfield border.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N=1):
  1. **dig-toggle + roll-to-low** — clicking a cell toggles its
     binary terrain state HIGH↔LOW; immediately afterwards each
     marble on a HIGH cell with an adjacent LOW cell rolls into
     that LOW neighbour (priority N→E→S→W); marbles on LOW cells
     stay put.

- **Necessity per mechanic**:
  - L1 cannot be solved without triggering the dig-toggle +
    roll-to-low mechanic because the marble starts at (col=5,
    row=5) on a HIGH cell entirely surrounded (N, E, S, W) by
    HIGH cells; without toggling at least one cell to LOW, the
    marble has no possible move and can never reach the
    target ring at (col=5, row=9). The target itself is a LOW
    cell but is 4 cells away — the marble must traverse three
    intermediate cells, each of which only becomes traversable
    via the toggle action.

- **Layout** (cells (col, row) where (0..15, 0..15)):
  - WALL: outer ring (col∈{0,15} or row∈{0,15}) — 60 cells.
  - TARGET-LOW (red ring): (5, 9).
  - HIGH (default): every other cell of the inner 14×14 area
    — 14×14 − 1 (target) = 195 cells.
  - Marble red: starts at (5, 5).

- **Witness solution** (6 actions, ≤ step budget 16):
  1. `ACTION6@display_grid(5, 6)` — toggles cell (5, 6) HIGH→LOW.
     Marble at (5, 5) HIGH; neighbour (5, 6) LOW. Marble rolls
     S to (5, 6). Settled (LOW).
  2. `ACTION6@(5, 6)` — toggles cell (5, 6) LOW→HIGH. Marble at
     (5, 6) HIGH; all four neighbours HIGH. Stays.
  3. `ACTION6@(5, 7)` — toggles (5, 7) HIGH→LOW. Marble at
     (5, 6) HIGH; (5, 7) LOW. Rolls S to (5, 7). Settled.
  4. `ACTION6@(5, 7)` — toggles (5, 7) LOW→HIGH. Marble stays
     (no LOW neighbour).
  5. `ACTION6@(5, 8)` — toggles (5, 8) HIGH→LOW. Marble (5, 7)
     HIGH → (5, 8) LOW. Rolls S to (5, 8).
  6. `ACTION6@(5, 8)` — toggles (5, 8) LOW→HIGH. Marble at
     (5, 8) HIGH; (5, 9) target LOW. Rolls S onto target.
     Settled (on target). WIN.

  (Click coordinate `(c, r)` is the logical cell; the agent
  produces display pixels via the camera scale of 4× — the
  game converts via `camera.display_to_grid` → `(col, row)` —
  any display pixel `(c*4..c*4+3, r*4..r*4+3)` maps to the
  same logical cell. ACTION6 click data carries `x` and `y`
  in display pixels.)

- **Difficulty justification**:
  - **(a) Random-resistance.** A vision-blind random clicker
    has 14×14 ≈ 196 candidate cells per ACTION6 and would need
    to hit a 6-step exact sequence (forward cell, raise, next
    forward cell, raise, etc.) to win in 6 clicks; the hit rate
    for any one click being the "correct next click" is at most
    1/196, so a random sequence solving L1 in ≤ 16 clicks is
    vanishingly small.
  - **(b) Human-tractable.** ~1.5 minutes for an attentive
    human: the L1 layout has only one obvious destination (the
    target ring) and one obvious direction (south); the
    discovery is just learning the dig-and-raise rhythm from
    2-3 trial clicks.
  - **(c) Planning depth.** L1 has *no strict planning
    requirement* per `difficulty-rules.md` § 1: once the
    mechanic is understood (which is the point of L1), the
    correct path is the straight-line column 5 from the
    marble to the target.
  - **(d) Step budget.** 16 — 2.6× the witness length, leaving
    comfortable room for exploration clicks while learning the
    rule.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (N+1 = 2; introduces
  exactly 1 new mechanic over L1):
  1. **dig-toggle + roll-to-low** (carried forward from L1).
  2. **walls** — cells of WALL type cannot be toggled and
     marbles never enter them. Walls force a detour.

- **Necessity per mechanic**:
  - L2 cannot be solved without triggering dig-toggle + roll-to-
    low because the marble starts at (3, 4) on a HIGH cell
    surrounded by HIGH cells; reaching the target at (12, 4) is
    impossible without converting cells along the route to LOW.
    The L2 layout has no pre-dug LOW path; every LOW cell on
    the route must be created by the player.
  - L2 cannot be solved without engaging the walls mechanic
    because column 7 from row 1 to row 14 is filled with WALL
    cells with the only gap at (7, 8); any path from the
    marble's start (3, 4) to the target (12, 4) requires the
    marble to detour south to row 8, traverse the wall gap at
    (7, 8), and turn back north — every alternate route hits
    WALLs that the player cannot toggle (rows 0 and 15 are
    outer-ring walls; row 1 is now sealed by the column 7 wall;
    no row-1, row-15, or interior alternate corridor exists),
    so the gap-row-8 detour is forced.

- **Layout** (16×16 grid, outer ring walls) [**Revision Issue 1**:
  wall column extended to row 1]:
  - WALL: outer ring + a vertical bar in column 7 from row 1 to
    row 14, with one gap at (7, 8). 60 (outer ring) + 14 (col 7
    rows 1..14) − 1 (gap) = 73 wall cells. The wall column
    extends to row 1, sealing what would otherwise be a row-1
    corridor escape — there is no upper-edge bypass.
  - HIGH (default): all remaining inner cells.
  - TARGET-LOW (red): (12, 4).
  - Marble red: starts at (3, 4).

- **Witness solution**: the witness routes the marble south
  along column 3 to row 8, east along row 8 through the gap to
  column 12, then north along column 12 to row 4. Path cells
  (col, row): (3,4) → (3,5) → (3,6) → (3,7) → (3,8) → (4,8) →
  (5,8) → (6,8) → (7,8) → (8,8) → (9,8) → (10,8) → (11,8) →
  (12,8) → (12,7) → (12,6) → (12,5) → (12,4). Path length 18
  cells = 16 intermediate cells + start + target. Witness
  expands to 32 clicks: each of the 16 non-target intermediate
  cells receives a dig (HIGH→LOW) click followed by a raise
  (LOW→HIGH) click, for 16 × 2 = 32 clicks; the final raise
  click on (12, 5) is what rolls the marble onto the target
  cell (12, 4) (target stays LOW immutably). For brevity, the
  action sequence is:

  ```
  click (3,5), click (3,5),  ← marble (3,4)→(3,5); raise
  click (3,6), click (3,6),  ← marble (3,5)→(3,6); raise
  ... (six more dig+raise pairs along col 3 to row 8) ...
  click (3,8), click (3,8),  ← marble (3,7)→(3,8); raise
  click (4,8), click (4,8),  ← marble (3,8)→(4,8); raise
  ... (continue east through (5..11, 8)) ...
  click (12,8), click (12,8),  ← marble (11,8)→(12,8); raise
  click (12,7), click (12,7),  ← marble (12,8)→(12,7); raise
  click (12,6), click (12,6),  ← marble (12,7)→(12,6); raise
  click (12,5),                ← marble (12,6)→(12,5); LAST
  click (12,5)                 ← raise; marble (12,5)→target.
  ```

  Total: 32 clicks. Step budget 50.

- **Difficulty justification**:
  - **(a) Random-resistance.** Random clicker faces 16×16 = 256
    candidate cells; reaching the target requires a 17-cell
    route through a wall-gap; chance of stumbling onto the
    correct sequence is essentially zero. Crucially, the wall
    gap is a 1-cell-wide bottleneck — if the marble enters a
    wrong LOW cell off-route, you typically have to raise it
    again before progressing, reinforcing the planning
    requirement.
  - **(b) Human-tractable.** ~2 minutes for an attentive
    human: the wall column is visually obvious (heavy black
    sprites), the gap is the only break in the wall, and the
    target is north-east — the route is "down to the gap, across,
    up to target". The dig-and-raise rhythm is already known
    from L1.
  - **(c) Planning depth (post-discovery).** Light-moderate
    [**Revision Issue 2**: rewritten to be honest and post-
    discovery]. With the mechanic and wall layout fully
    understood, a fully-informed player at L2's start has 196
    inner non-wall cells (256 grid cells minus 73 walls plus or
    minus a target) plus 60 outer-ring wall cells to click — any
    cell is a valid first action (wall clicks are no-ops but
    consume one step). The route is essentially uniquely
    determined: the gap at (7, 8) is the only column-7 crossing,
    so the marble must detour through it. The post-discovery
    planning amounts to (1) measuring marble-row=4 against
    gap-row=8 (a four-cell southward dip), (2) recognising that
    walls have a visually heavier render (palette 5+4 outer with
    no inner grey, vs HIGH cells' palette 4+3 corners with
    palette 2+3 inner) and so cannot be confused with toggleable
    HIGH cells, (3) committing to the L-shaped detour. The
    plausible-but-wrong post-discovery action is **assuming
    walls are toggleable like HIGH cells and clicking on (7, 4)
    or (7, 5) trying to "dig open" the wall column at row 4 to
    save the south detour** — a click on a wall is a no-op (the
    cell stays a wall) but still consumes a step; a player who
    spends 4-5 clicks attempting this before realising the visual
    distinction has wasted ~5 steps. The witness reasoning
    chain is "wall column at col 7 has unique gap at (7, 8);
    target is at (12, 4) east of column 7; marble at (3, 4) is
    on the west side; therefore L-detour: south to (3, 8), east
    through (7, 8), continue east to (12, 8), north to (12, 4)".
  - **(d) Step budget.** 50 — 1.56× the witness length, generous
    over the 32-click witness. Does not shrink relative to L1.

### Level 3 — system + 1 new mechanic

- **Mechanics required by the witness** (L2-count + 1 = 3;
  introduces exactly 1 new mechanic over L2):
  1. **dig-toggle + roll-to-low** (from L1).
  2. **walls** (from L2).
  3. **anchor-link pairs** — two specific cells visually banded
     by a shared corner-cap colour. Toggling one cell auto-
     toggles its partner regardless of partner's location, so
     every anchor click has a remote side-effect.

- **Necessity per mechanic**:
  - L3 cannot be solved without dig-toggle + roll-to-low
    because both marbles start on HIGH cells and their targets
    are 9 cells away in opposite-axis directions; only the
    toggle action makes any cell LOW.
  - L3 cannot be solved without walls because column 8 from
    row 1 to row 14 is solid WALL except for the two anchor
    cells at (8, 6) and (8, 9). The walls force every route
    between marble and target to cross column 8 only at one
    of the two anchor cells.
  - L3 cannot be solved without the anchor-link mechanic
    because both marbles must cross column 8, and they must
    cross at different rows (RED via (8, 6) and BLUE via
    (8, 9)) due to mutual-occupancy exclusion. The anchor at
    (8, 6) is paired with the anchor at (8, 9): toggling
    either toggles both. There is no other gap in column 8
    that the player could open separately. Therefore solving
    L3 requires the player to (1) recognise the corner-cap
    colour-banding that signals the link, and (2) plan around
    it — both anchor cells become LOW with a single click.
    A trivial heuristic that ignores the link (e.g., trying
    to toggle the two anchor cells independently) just
    re-flips both back, undoing progress.

- **Layout** (16×16 grid, outer ring walls):
  - WALL: outer ring + column 8 from row 1 to row 14 EXCEPT
    cells (8, 6) and (8, 9). 60 + 14 − 2 = 72 wall cells.
  - ANCHOR-HIGH (cap colour magenta=6): (8, 6) and (8, 9). Linked.
  - HIGH: all other inner cells.
  - TARGET-LOW (red ring): (12, 6).
  - TARGET-LOW (blue ring): (3, 9).
  - Marble red: starts at (3, 6).
  - Marble blue: starts at (12, 9).

- **Witness solution**: route RED east via (8, 6) anchor; route
  BLUE west via (8, 9) anchor. The single anchor-link click
  exposes both crossing cells simultaneously.

  Action sequence (paths in (col, row); transitions are dig+raise
  pairs except the last in each path which is dig only;
  the anchor click is one ACTION6 — both cells flip):

  ```
  ── walk RED to anchor approach (3,6)→(7,6):
  click (4,6), (4,6),   ← marble red (3,6)→(4,6)
  click (5,6), (5,6),   ← marble red (4,6)→(5,6)
  click (6,6), (6,6),   ← marble red (5,6)→(6,6)
  click (7,6), (7,6),   ← marble red (6,6)→(7,6); raise

  ── walk BLUE to anchor approach (12,9)→(9,9):
  click (11,9), (11,9), ← marble blue (12,9)→(11,9); raise
  click (10,9), (10,9), ← marble blue (11,9)→(10,9); raise
  click (9,9), (9,9),   ← marble blue (10,9)→(9,9); raise

  ── trigger the anchor-link to open BOTH crossing cells:
  click (8,6),         ← cells (8,6) and (8,9) both HIGH→LOW.
                        After settling pass:
                          RED at (7,6) HIGH, neighbour (8,6) LOW
                            → rolls E to (8,6). Settled (LOW).
                          BLUE at (9,9) HIGH, neighbour (8,9) LOW
                            → rolls W to (8,9). Settled (LOW).

  ── re-trigger the anchor-link to free both marbles:
  click (8,6),         ← (8,6) and (8,9) both LOW→HIGH.
                        Both marbles now on HIGH (their cells were
                        the anchors that just flipped). Each looks
                        for adjacent LOW: RED at (8,6) sees
                        (7,6)=HIGH, (9,6)=HIGH (yet undug),
                        (8,5)=wall, (8,7)=wall — stays. BLUE
                        at (8,9) sees (7,9)=HIGH, (9,9)=HIGH
                        (was raised earlier), (8,8)=wall,
                        (8,10)=wall — stays.

  ── walk RED to target (8,6)→(12,6):
  click (9,6), (9,6),   ← marble red (8,6)→(9,6); raise
  click (10,6), (10,6), ← marble red (9,6)→(10,6); raise
  click (11,6),         ← marble red (10,6)→(11,6) (LOW); 
  click (11,6),         ← raise; marble red (11,6)→(12,6)
                        target. Settled. RED done.

  ── walk BLUE to target (8,9)→(3,9):
  click (7,9), (7,9),   ← marble blue (8,9)→(7,9); raise
  click (6,9), (6,9),   ← marble blue (7,9)→(6,9); raise
  click (5,9), (5,9),   ← marble blue (6,9)→(5,9); raise
  click (4,9),          ← marble blue (5,9)→(4,9) (LOW)
  click (4,9),          ← raise; marble blue (4,9)→(3,9)
                        target. Settled. BLUE done. WIN.
  ```

  Total: 8 (RED to gap) + 6 (BLUE to gap) + 2 (anchor click +
  anchor re-click) + 6 (RED to target) + 8 (BLUE to target)
  = 30 clicks.

- **Difficulty justification**:
  - **(a) Random-resistance.** Two marbles, ~256 cells, two
    target cells with distinct hue rings, a single corner-cap
    colour signalling the anchor link — random clicking has
    near-zero chance of solving L3 within the step budget.
    Crucially, a random clicker doesn't know to use the same
    anchor click to pass BOTH marbles through the bottleneck
    on the SAME settling pass.
  - **(b) Human-tractable.** ~2.5 minutes for an attentive
    human: the wall layout is obvious; the corner-cap coloured
    dot links are visually salient (clicking one cell with
    that cap and seeing both linked cells flip teaches the
    rule in one trial). The dig-and-raise rhythm is already
    known.
  - **(c) Planning depth (post-discovery).** Moderate
    [**Revision Issue 3**: reframed honestly — the wrong
    heuristic delays rather than fails, but the planning IS
    post-discovery]. With every mechanic understood, a
    fully-informed player at L3's start has 256 grid cells of
    which most are toggleable; the post-discovery decision is
    "in what ORDER to dig, and when to trigger the anchor
    pair". The plausible-but-wrong post-discovery heuristic is
    **"route the closer marble (RED) all the way to its target
    first, including the anchor crossing, then handle BLUE
    separately"**. Tracing this approach: RED to (7, 6) HIGH
    [8 clicks], anchor click [1; RED rolls to (8, 6) LOW],
    anchor click [1; flips back, RED stays at (8, 6) HIGH no
    LOW adj], dig (9, 6) and onward [6 clicks; RED reaches
    (12, 6) target]. RED done in 16 clicks. Now BLUE: walk
    (12, 9) → (9, 9) [6 clicks], anchor click [1; BLUE rolls
    to (8, 9) LOW; RED at target unaffected since target is
    LOW immutable], anchor click [1; flips both back, BLUE at
    (8, 9) HIGH], walk (8, 9) → (3, 9) target [8 clicks]. BLUE
    done in 16 clicks. Total: 16 + 16 = 32 clicks. The
    witness's pre-position-both approach takes 30 clicks (8 +
    6 + 2 + 6 + 8). The optimisation is 2 clicks via
    co-positioning both marbles BEFORE the first anchor click,
    so a single anchor toggle ferries both through their
    respective anchor cells in one settling pass. Both
    approaches succeed within the 80-click budget; the planning
    discriminator is realising the link makes a parallel-cross
    strategy strictly cheaper. The witness reasoning chain is
    **"the anchor pair flips both cells together — pre-position
    both marbles adjacent to their respective anchors and then
    spend ONE click on the anchor to ferry both through, then
    one click to re-raise the anchors and dig forward
    independently"**.
  - **(d) Step budget.** 80 — 2.6× the witness length, generous
    over a longer witness. Does not shrink relative to L2.

## 5. Action mapping

`available_actions = [6]` — pure-click. ACTION6 click coordinate is
the only player input.

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click at display (x, y); engine converts via `camera.display_to_grid` to logical (col, row); if the cell is HIGH, LOW, or ANCHOR-HIGH/ANCHOR-LOW (i.e. NOT a wall and NOT a target), toggle its terrain state. If anchor, also toggle its partner. After the toggle, run the marble settling pass. | always |

Walls and targets cannot be toggled — clicking them is a
no-op (the click counts against the step budget but produces no
state change, mirroring how the reference games handle invalid
clicks via the action-counter increment).

## 6. HUD and per-game state

**HUD widget**: one `RenderableUserDisplay` subclass —
`StepCounterHud(RenderableUserDisplay)` — paints a horizontal
bar across the top frame row (row 0). Bar fills proportional to
`current_steps / max_steps` with palette 14 (green) for the
remaining portion and palette 4 (off-black) for the spent
portion. (Mirrors the universal HUD pattern observed in 25/25
reference games.)

**Per-game internal state** (across actions, recreated in
`on_set_level`):
- `self.heights` — `np.ndarray` of shape `(16, 16)`, dtype int8;
  `0` = LOW, `1` = HIGH. Used for the marble settling rule.
- `self.cell_kind` — `np.ndarray` of shape `(16, 16)`, dtype int8;
  `0` = NORMAL, `1` = WALL, `2` = TARGET-RED, `3` = TARGET-BLUE,
  `4` = TARGET-GREEN, `5` = ANCHOR-MAGENTA, `6` = ANCHOR-PINK.
  Used to filter what's toggleable and what's a target.
- `self.anchor_pairs` — `dict[(col, row), (col, row)]`, mapping
  one anchor cell to its partner. Symmetric.
- `self.marble_targets` — `dict[Sprite, (col, row)]`, maps each
  marble sprite to its destination cell.
- `self._step_counter` — int counting actions remaining.
- `self.terrain_sprite` — the 64×64 canvas sprite; mutated each
  turn by `_repaint_terrain()`.

**No hidden state per checklist item 19**: every cell's height
is rendered into the terrain canvas pixels (LOW vs HIGH have
distinct 4×4 patterns), every wall is rendered as a heavier
black pattern, every anchor is rendered with its corner-cap
dot. Each marble's identity is encoded in its sprite hue. The
step counter is rendered as an HUD bar. No mutable game state
exists that the player must track without a corresponding
visual cue.

The marble's "next target" is declared by the matching-hue ring
visible on the target cell from level start; the player can
read which marble belongs to which target by hue match.

## 7. Win condition

After the marble settling pass completes following any ACTION6
click, evaluate: every marble's `(col, row)` equals
`self.marble_targets[marble]`. If true, call
`self.next_level()`. After Level 3 completes, the engine's
default `next_level()` advances past the last level and calls
`self.win()`.

## 8. Lose condition

After every ACTION6 (including no-op clicks on walls or
targets), decrement `self._step_counter` by 1. When the counter
reaches 0 without the win predicate being true, call
`self.lose()`. There is no instant-fail collision; only step
exhaustion ends the run.

## 9. Novelty note

### Closest entries in the 25-game taxonomy
- `ka59` (sokoban-explode-chase): both involve clicking + moving
  pawns to colour-matched targets in a walled arena. **Distinguishing
  rule**: ka59 SLIDES the active block on direction press and
  pushes neighbours via detonation chains; vd3g has no direction
  press at all (only ACTION6 click), no detonation, and no
  push — marbles flow purely via cell-local height gradient. The
  player edits TERRAIN, not block-positions.
- `m0r0` (mirror-orb-merge): both involve coordinating multiple
  pawns to merge / settle. **Distinguishing rule**: m0r0's pawns
  move on direction press with per-quadrant mirrored axes (one
  press moves four avatars simultaneously); vd3g pawns move on
  ACTION6 click with each marble independently checking its
  4-neighbourhood — no mirroring, no symmetric-axis input.
- `tu93` (maze-pickup-train): both have multiple agents
  navigating a walled maze. **Distinguishing rule**: tu93's
  agents move on direction press in lockstep and the floor is
  immutable; vd3g's marbles move automatically each click via
  gradient flow and the floor cells are PLAYER-EDITED.

### Closest entries in `prior-games/index.md`
- `tg6w` (settle-pile-tilt): both have pawns settling under a
  gravity-like rule. **Distinguishing rule**: tg6w tilts the
  WHOLE playfield's down-direction (one global vector) and lets
  blocks slide multi-cell to the rim; vd3g has per-cell binary
  height (a heightmap) with marbles stepping exactly one cell
  per click toward an adjacent low neighbour. Different
  operating principle (global tilt vs. local-gradient field) and
  different settling rule (slide-to-rim vs one-cell-step).
- `kn58` (anchor-pull-magnet): both have pawns moving toward
  player-marked cells. **Distinguishing rule**: kn58 places a
  SINGLE global anchor that pulls every pawn one cell along its
  dominant Manhattan axis; vd3g has NO attractor — marbles
  inspect their immediate 4-neighbourhood for a low cell and
  step accordingly. The player edits the TERRAIN, not the
  attractor; and the response is per-marble local, not
  global-Manhattan.
- `kp9z` (grain-accumulate-topple): both involve cells changing
  state via clicks and propagating effects. **Distinguishing
  rule**: kp9z has cells that ACCUMULATE counts and overflow at
  capacity 4 to all 4 cardinals; vd3g has BINARY cell state
  (HIGH or LOW) with no accumulation, no capacity, no overflow.
  The two are fundamentally different cellular models: count-
  based sandpile vs. binary terrain.
- `mr5q` (polarity-attract-discharge): both have toggleable
  per-element state. **Distinguishing rule**: mr5q toggles
  PAWN polarity (yang/yin) and pawns walk toward nearest
  same-colour opposite on ACTION5; vd3g toggles CELL height
  and marbles flow on every click via local gradient. mr5q's
  dynamics live on the pawns; vd3g's live on the terrain.

### Negative similarity check (the 8 dimensions)
Walked against the 4 closest priors above. Each shares ≤ 2
dimensions with vd3g (and only on the universal-trivial axes:
step-counter death, click input, pawn-to-target goal). On the
heavy axes (visual signature, sprite grain, core dynamic) every
prior diverges. No 3+-dimension overlap with any single prior.

### Verdict
NOVEL on both axes (taxonomy + prior-games corpus), with
concrete distinguishing rules articulated per closest neighbour.
