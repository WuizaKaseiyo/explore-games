# mechanic-spec — nz3v (revision 2, addresses critique-revisions.md)

Revisions vs draft 1 are concentrated in §3 (sprite roster), §4
(per-level layouts and budgets), §6 (HUD widgets and visual
cues). Each revised section flags the critique issue addressed.

## 1. Title
Rotor-Sweep Walk (working title; not visible in-game).

## 2. Mechanic family
A central rotor sprite at the playfield centre projects a 90°
"lit" angular sector that **auto-rotates one quadrant per agent
action**. The avatar walks the playfield with cardinal arrows;
cells outside the current lit sector are unwalkable (stepping
into a dark cell ends the level). The puzzle is to **time arrow
presses so each step's destination cell is in the lit sector at
that step** — riding the rotating sector to the target.

Priors used (from `core-knowledge-priors.md`): **basic geometry
& topology** (angular sector partitioning the plane around a
centre point; rotational symmetry; sector boundaries), **basic
physics** (deterministic uniform rotation per tick; no
wall-clock dependence; no randomness), **objectness** (rotor
pillar, avatar, target, walls, stop-tile, counter-rotation
switch — all coherent persistent sprites). No agentness. No
symbolic content.

## 3. Sprite roster
*[Revised vs draft 1 to address critique items 1 (avatar
chevron / stop-tile X-cross both read as letters/symbols).]*

The playfield is a 12×12 logical grid (5× scale → 5×5 px per
cell, 60×60 px rendered, centred in 64×64 with 2-px letterbox
on each side). Sprites carry internal pixel structure to
satisfy checklist item 20 — none rely on flat-colour cell-blocks
(see §4 wedge rendering).

- **`rotor`** — 2×2 cells (10×10 px rendered). Pixels:
  - Outer ring: palette 5 (black) frame, 1-px thick.
  - Inner: palette 3 (grey) fill.
  - **Sector notch**: a 2-px palette 11 (yellow) accent on
    the rotor's exterior face that points at the current lit
    sector. Visually communicates which quadrant is lit even
    when the wedge tint is partially obscured by the avatar.
  - **Direction marker**: a 1-px palette 6 (magenta) dot at
    the rotor's clockwise-next-corner position. When direction
    is +1 (clockwise), the dot sits to the clockwise side of
    the notch; when direction is -1 (counter-clockwise), the
    dot moves to the counter-clockwise side. *This is the
    persistent visual cue for `_direction` per checklist item
    19 — addresses critique #2.*
  Tags: `["rotor"]`. Collidable. Placed at (5, 5)..(6, 6) in
  every level.

- **`avatar`** — 1×1 cell (5×5 px). *[Revised: was a "chevron"
  shape that read as letter `V` or `>`; now an "octagonal
  square" with no letter likeness.]* Pixels:
  ```
  -1 10 10 10 -1
  10  0  0  0 10
  10  0 10  0 10
  10  0  0  0 10
  -1 10 10 10 -1
  ```
  i.e., a light-blue (palette 10) outer ring with corner pixels
  removed (transparent palette -1), a white (palette 0) inner
  cell, and a single light-blue centre pixel acting as a
  "core". Reads as a small polygonal figure — distinguishable
  but no letter / digit / clipart association.
  Tags: `["avatar"]`. Collidable.

- **`target`** — 1×1 cell (5×5 px). Pixels: a hollow ring,
  palette 14 (green) at the 4 edge cells and 4 corner cells, a
  palette -1 (transparent) centre so the wedge tint shows
  through. Reads as "destination ring".
  ```
  14 14 14 14 14
  14 -1 -1 -1 14
  14 -1 -1 -1 14
  14 -1 -1 -1 14
  14 14 14 14 14
  ```
  Tags: `["target"]`. Not collidable — avatar walks onto it.

- **`wall`** — 1×1 cell (5×5 px). Pixels: a 5×5 cross-hatch
  with palette 5 (black) at all corners + centre and palette 4
  (off-black) elsewhere — reads as a textured solid block.
  ```
   5  4  5  4  5
   4  4  4  4  4
   5  4  5  4  5
   4  4  4  4  4
   5  4  5  4  5
  ```
  Tags: `["wall"]`. Collidable. Multiple instances per level.

- **`stop_tile`** — 1×1 cell (5×5 px). L2+. *[Revised: was an
  X-cross that read as letter X; now a 4-edge-dot pattern.]*
  Pixels: palette 12 (orange) dots at the 4 edge-centre cells
  (top-edge centre, bottom-edge centre, left-edge centre,
  right-edge centre); palette 4 (off-black) everywhere else.
  ```
   4  4 12  4  4
   4  4  4  4  4
  12  4  4  4 12
   4  4  4  4  4
   4  4 12  4  4
  ```
  Reads as "a 4-direction marker" — topologically a "+" shape
  centered on the cell, which `forbidden-elements.md` explicitly
  permits as a topological symbol. Not a letter / digit.
  Tags: `["stop_tile"]`. Not collidable; one-shot — once
  stepped on, all 4 dots colour-remap from palette 12 (orange)
  to palette 3 (grey) so the player can see the tile is spent.

- **`counter_switch`** — 1×1 cell (5×5 px). L3 only. Pixels: a
  palette 6 (magenta) curl/spiral pattern on a palette 4 base.
  ```
   4 -1 -1 -1  4
  -1  6  6  6 -1
  -1  6  4 -1 -1
  -1  6  6  6 -1
   4 -1  6 -1  4
  ```
  (asymmetric, reads as a curl / loop topology.) Reads as
  "reversal / loop-back" without being a letter or digit.
  Tags: `["counter_switch"]`. Not collidable; one-shot.

Palette set: **{4, 5, 3, 0, 10, 14, 12, 6, 11, 7}**. Ten
palette values; deliberately diverges from the kf42→vh68
cautionary cluster `{4, 8, 9}`. No red, no blue dominance — an
unmistakable signature.

## 4. Level progression, mechanic enumeration, and witness solutions

The 12×12 playfield is partitioned into four quadrant sectors
around the central 2×2 rotor:
- **NW**: gx ≤ 5 AND gy ≤ 5
- **NE**: gx ≥ 6 AND gy ≤ 5
- **SE**: gx ≥ 6 AND gy ≥ 6
- **SW**: gx ≤ 5 AND gy ≥ 6

A cell is walkable iff it is in the **current lit sector** AND
not occupied by the rotor / a wall. The rotor sweeps through
sectors in this default-clockwise sequence: NW → NE → SE → SW
→ NW. The rotation cadence is **K = 6 actions per sector**.

**Lit-cell rendering** *[revised to address critique #4 — flat
fill replaced with textured pattern]*: a
`WedgeOverlay(RenderableUserDisplay)` HUD widget paints, for
every lit cell at the cell's 5×5 rendered position, a palette
11 (yellow) **4-corner-dot pattern** — palette 11 at the cell's
4 corner pixels and one palette 11 pixel at the cell's centre
point; the remaining 20 inner cell pixels stay at the
background palette 4. The wedge area thus reads as a *textured
zone of yellow accents* over a dark background, not a flat-
colour block. This satisfies checklist item 20 (rendered frame
shows internal pixel detail rather than uniform-colour cell
blocks).

**Frozen visual cue** *[new, addresses critique #3]*: when
`_frozen_remaining > 0`, the WedgeOverlay paints with palette 7
(pink) instead of palette 11 (yellow) — same 4-corner-dot
pattern but a different colour. The colour change is visible
across all lit cells simultaneously, an unmissable persistent
cue that freeze is active. When freeze ends (at the rotation
that follows), the colour returns to palette 11.

**Lose-on-dark-step**: when the avatar attempts a move whose
destination is *not* in the lit sector AND *not* a wall AND
*not* the rotor, the avatar moves there and `self.lose()`
fires. Walls and the rotor block the move (action ticks; avatar
stays put — no death); only a free dark cell is fatal.

### Level 1 — base dynamic system

- **Mechanics required by the witness (N = 1)**:
  - **M1: rotor-sweep walkability** — the rotor's lit sector
    auto-rotates one quadrant clockwise per K = 6 actions; only
    the lit sector is walkable; stepping into a free dark cell
    loses.

- **Necessity per mechanic** (counterfactual, item 12):
  - L1 cannot be solved without triggering M1 because **the
    avatar at (1, 1) NW must reach the target at (10, 10) SE
    and the central 2×2 rotor at (5, 5)..(6, 6) blocks the
    direct diagonal**; every move's destination must be in the
    rotor's currently-lit quadrant or the avatar dies. There is
    no path from NW to SE that does not exercise M1.

- **Layout**:
  - Avatar: (1, 1)
  - Target: (10, 10)
  - Walls: none
  - Stop-tiles: none
  - Counter-switches: none

- **Witness solution (18 actions)**:
  ```
  ACTION4 ACTION4 ACTION4 ACTION4 ACTION2 ACTION2
  ACTION4 ACTION4 ACTION2 ACTION2 ACTION4 ACTION4
  ACTION2 ACTION2 ACTION2 ACTION2 ACTION4 ACTION2
  ```
  Step-by-step trace (* = sector at end of action; rotation
  happens at end of actions 6, 12, 18):
  - 1: (1,1)→(2,1) NW ✓
  - 2: (2,1)→(3,1) NW ✓
  - 3: (3,1)→(4,1) NW ✓
  - 4: (4,1)→(5,1) NW ✓
  - 5: (5,1)→(5,2) NW ✓
  - 6: (5,2)→(5,3) NW ✓ — rotation at end of action 6: wedge → NE
  - 7: (5,3)→(6,3) NE ✓
  - 8: (6,3)→(7,3) NE ✓
  - 9: (7,3)→(7,4) NE ✓
  - 10: (7,4)→(7,5) NE ✓
  - 11: (7,5)→(8,5) NE ✓
  - 12: (8,5)→(9,5) NE ✓ — rotation at end of action 12: wedge → SE
  - 13: (9,5)→(9,6) SE ✓
  - 14: (9,6)→(9,7) SE ✓
  - 15: (9,7)→(9,8) SE ✓
  - 16: (9,8)→(9,9) SE ✓
  - 17: (9,9)→(10,9) SE ✓
  - 18: (10,9)→(10,10) SE ✓ — target reached.

- **Difficulty justification**:
  - **(a) Random-resistance**: random uniform-arrow policy has
    ≤ 1/4 of choosing the correct first action; over 18 forced
    actions the chance of stumbling into a witness is (1/4)^18
    ≈ 1.5e-11, far below the §3.5 threshold of 1/10,000.
  - **(b) Human-tractable**: ~1 minute once the mechanic is
    understood. The rule "step only into the lit sector" is
    learnable from 1–2 deaths.
  - **(c) Planning depth**: **no strict planning requirement**.
    Once the player knows the rule, the path is essentially
    forced (one valid arrow per step in the witness). Matches
    `difficulty-rules.md` § 2.c L1 guidance.
  - **(d) Step budget**: **22 actions** *[revised to maintain
    monotone non-decreasing budgets across L1→L2→L3 per
    critique #6]* (witness 18 + 4 slack ≈ 22% margin).
    Generous over the witness; tight enough to stay below
    L2/L3 budgets so the budget non-decreasing rule holds.

### Level 2 — base system + 1 new mechanic (N + 1 = 2)

- **Mechanics required by the witness (M = 2)**:
  - **M1: rotor-sweep walkability** (carried forward).
  - **M2: stop-tile freezes rotor** — stepping on a stop-tile
    pauses the rotation count for K' = 4 additional actions;
    the lit sector stays at the current quadrant for K + K' =
    10 actions instead of 6. After the freeze elapses,
    rotation resumes from where it left off. The wedge tint
    visibly shifts from palette 11 (yellow) to palette 7
    (pink) for the duration of the freeze, returning to yellow
    when freeze ends.

- **Necessity per mechanic** (counterfactual, item 12):
  - L2 cannot be solved without triggering M1 because **every
    move's destination must be in the rotor's currently-lit
    quadrant** — the sweep mechanic gates every step.
  - L2 cannot be solved without triggering M2 because **walls
    at (4, 1), (4, 2), (4, 3) block the gx = 4 column at gy =
    1, 2, 3; the only NW route from (1, 1) to a cell at gx = 5
    (the NW–NE boundary) requires descending to gy = 4 first
    and then crossing east through (3, 4) → (4, 4) → (5, 4)**.
    Manhattan distance from (1, 1) to (5, 4) is 7 (4 east + 3
    south), and any valid wall-detour path requires ≥ 7
    actions. Without M2's freeze, the NW phase is K = 6 actions
    — not enough to reach (gx = 5, gy ≤ 5). At end of action 6
    the rotor rotates to NE; the avatar is at gx ≤ 4 and the
    next move's east-step lands in NW (still gx ≤ 5, now
    dark) or attempts a wall move (no progress). Both
    outcomes lose or stall. The stop-tile at (2, 4) is the
    only sprite that extends the NW phase to 10 actions, just
    enough to complete the 7-action detour.

- **Layout**:
  - Avatar: (1, 1)
  - Target: (10, 1)
  - Walls: (4, 1), (4, 2), (4, 3)
  - Stop-tile: (2, 4)
  - Counter-switches: none

- **Witness solution (15 actions)**:
  ```
  ACTION2 ACTION2 ACTION2 ACTION4 ACTION4 ACTION4
  ACTION4 ACTION1 ACTION1 ACTION1 ACTION4 ACTION4
  ACTION4 ACTION4 ACTION4
  ```
  Step-by-step:
  - 1: (1,1)→(1,2) NW ✓
  - 2: (1,2)→(1,3) NW ✓
  - 3: (1,3)→(1,4) NW ✓
  - 4: (1,4)→(2,4) NW ✓ — **stop-tile (2,4) triggered, freeze K' = 4 armed; wedge tint → palette 7 (pink) starting next action**
  - 5: (2,4)→(3,4) NW (frozen) ✓
  - 6: (3,4)→(4,4) NW (frozen) ✓ (would-be rotation point delayed by freeze)
  - 7: (4,4)→(5,4) NW (frozen) ✓
  - 8: (5,4)→(5,3) NW (frozen) ✓
  - 9: (5,3)→(5,2) NW (frozen) ✓
  - 10: (5,2)→(5,1) NW ✓ — freeze end, rotation triggers: wedge → NE; tint → palette 11 (yellow)
  - 11: (5,1)→(6,1) NE ✓
  - 12: (6,1)→(7,1) NE ✓
  - 13: (7,1)→(8,1) NE ✓
  - 14: (8,1)→(9,1) NE ✓
  - 15: (9,1)→(10,1) NE ✓ — target reached.

- **Difficulty justification**:
  - **(a) Random-resistance**: the random policy must
    simultaneously (1) navigate the wall-detour, (2) hit the
    stop-tile, (3) traverse the NE quadrant within K = 6
    actions of phase 2 to reach the target. P ≪ 1/10,000.
  - **(b) Human-tractable**: ~2 minutes. After M1 is learned in
    L1, the player tries direct east → blocked by wall. They
    detour south → if they don't hit (2, 4) the wedge rotates
    early and they die in NE. They notice the orange-dotted
    sprite at (2, 4) (stop-tile, visually distinct from walls
    and floor); after stepping on it once they observe (i) the
    wedge tint changes from yellow to pink, (ii) the wedge
    does NOT rotate on the next action — both **observable
    cues** that teach M2.
  - **(c) Planning depth**: **moderate post-discovery
    planning**. With M1 + M2 fully understood, the player has
    a count of plausible first actions ≥ 3 in NW: ACTION2 to
    (1, 2) or ACTION4 to (2, 1) or wait by walking east to
    walls — all three start a viable early NW path. The
    reasoning chain: *I must reach gx = 5 by end of NW phase;
    the wall forces me through gy = 4; the stop-tile is at
    (2, 4) so my path must cross (2, 4) to extend NW to 10
    actions*. **A plausible-but-wrong path** the post-discovery
    player would consider and reject: descending via gx = 1
    column (1,1) → (1,2) → (1,3) → (1,4) → (1,5) →
    (2, 5) → (3, 5) → (4, 5) → (5, 5 = rotor blocked)
    skips the stop-tile (which is at (2, 4), not (1, 4) or
    (2, 5)), so freeze never arms; on action 7 wedge → NE
    while avatar is still in NW; loses.
  - **(d) Step budget**: **26 actions** *[revised per critique
    #6]* (witness 15 + 11 slack ≈ 73% margin). Generous —
    accommodates one early death-and-retry attempt within the
    budget while M2 is being learned.

### Level 3 — base system + 1 more new mechanic (M + 1 = 3)

*[Section completely rewritten per critique #5: single
canonical layout and witness; intermediate drafts removed.]*

- **Mechanics required by the witness (3)**:
  - **M1: rotor-sweep walkability** (carried forward).
  - **M2: stop-tile freezes rotor** (carried forward).
  - **M3: counter-rotation switch** — stepping on a
    counter_switch tile **reverses the rotor's rotation
    direction permanently for the rest of the level**. Default
    direction is +1 (clockwise: NW→NE→SE→SW); after the
    switch is triggered, direction is -1 (counter-clockwise:
    NW→SW→SE→NE). The switch is one-shot. The **persistent
    visual cue** is the rotor's direction-marker dot (palette
    6 magenta) which moves to the opposite corner of the
    notch when direction reverses — visible at any frame.

- **Layout** (canonical):
  - Avatar: (1, 1)
  - Target: (1, 10)
  - Walls: (3, 1), (3, 2), (3, 4) — three wall cells in NW
    forming a partial barrier in the gx = 3 column at gy =
    1, 2, 4. (Cell (3, 3) is *not* a wall — it is open
    floor used by the witness.) Cell (3, 5) is also open.
  - Stop-tile: (2, 3)
  - Counter-switch: (4, 5)

- **Necessity per mechanic** (counterfactual, item 12):
  - L3 cannot be solved without triggering M1 because **every
    move's destination must be in the rotor's currently-lit
    quadrant** — same gating as L1 and L2.
  - L3 cannot be solved without triggering M2 because **the
    counter-switch is at (4, 5); Manhattan distance from
    (1, 1) to (4, 5) is 7 (3 east + 4 south); any path
    avoiding walls (3, 1), (3, 2), (3, 4) is ≥ 7 actions long.
    Without M2's freeze, NW phase is 6 actions — too few to
    reach the switch. At end of action 6, rotor rotates
    clockwise to NE while avatar is at gx ≤ 4 inside NW, and
    the next move into NE (gx ≥ 6) is unreachable in one
    step**. The stop-tile at (2, 3) is the only sprite that
    extends NW to 10 actions, enough to traverse to the switch
    and back to a SW-boundary cell. Without M2, the witness
    cannot trigger M3 within the NW phase.
  - L3 cannot be solved without triggering M3 because **under
    the default clockwise direction (NW → NE → SE → SW), the
    avatar must traverse 3 phase-transitions before reaching
    SW where the target sits at (1, 10). The shortest no-M3
    path with M2's freeze is exactly 27 actions** (verified by
    independent path enumeration below). The L3 step budget is
    **26**. Hence M3 is strictly required to halve the
    transition count by reversing direction (NW → SW
    immediately).

  **Counterfactual enumeration** (per item 12: enumerate
  plausible alternates and walk each to its failure):

  Alternate 1 — *clockwise sweep, no M3* (the natural sweep
  with M2 to extend NW): traced action-by-action below.
  - Phase 1 (NW, 1–10 with freeze): (1,1)→(1,2)→(1,3)→(2,3)
    [stop, freeze armed]→(3,3)→(4,3)→(5,3)→(5,2)→(5,1)→
    (5,0) [edge wall-bump → no move, but action ticks]
    → (5,0). End of frozen NW at action 10, avatar at (5, 0)
    or similar; this configuration depends on the player's
    final-action choice. The minimum-cost end-of-NW position
    that allows entering NE is (5, gy) where gy ∈ {0..5} and
    gx = 5. Avatar reaches (5, 1) by action 8; subsequent
    frozen-NW actions (9, 10) must keep avatar in NW for the
    freeze to hold — wall-bumping or doubling back is forced.
  - Phase 2 (NE, 11–16): from (5, 1) the avatar walks east
    and south. Optimum to position for SE entry: end phase 2
    at (gx ≥ 6, gy = 5) so action 17's south-step enters SE.
    11: (6,1). 12: (6,2). 13: (6,3). 14: (6,4). 15: (6,5).
    16: (7,5). End (7, 5).
  - Phase 3 (SE, 17–22): 17: (7,6). 18: (7,7). 19: (7,8).
    20: (7,9). 21: (7,10). 22: (6,10). End (6, 10).
  - Phase 4 (SW, 23–27): 23: (5,10). 24: (4,10). 25: (3,10).
    26: (2,10). 27: (1,10). Target reached on action **27**.

  Total alternate-1 length = **27 actions**, exceeding the L3
  step budget of **26** by 1 action. Alternate 1 fails to fit
  the budget. ✓

  Alternate 2 — *no M2 (skip stop-tile)*: NW phase = 6 actions;
  avatar at end of action 6 is at most (4, gy) with gy ≤ 5 due
  to walls + Manhattan constraint. Action 7's east-step lands
  at gx ≤ 5 (NW); wedge = NE; avatar dies. Cannot transition.

  Alternate 3 — *avoid switch (skip M3) but use M2*: same as
  alternate 1 above; minimum is 27 actions, exceeds budget 26.

  All plausible alternates fail. Strict counterfactual
  necessity holds for M1, M2, AND M3.

- **Witness solution (15 actions)**:
  ```
  ACTION2 ACTION2 ACTION4 ACTION4 ACTION4 ACTION2
  ACTION2 ACTION3 ACTION3 ACTION3 ACTION2 ACTION2
  ACTION2 ACTION2 ACTION2
  ```
  Step-by-step:
  - 1: (1,1)→(1,2) NW ✓
  - 2: (1,2)→(1,3) NW ✓
  - 3: (1,3)→(2,3) NW ✓ — **stop-tile (2,3) triggered**;
    freeze K' = 4 armed; wedge tint → palette 7 (pink).
  - 4: (2,3)→(3,3) NW (frozen) ✓ (cell (3,3) is open floor)
  - 5: (3,3)→(4,3) NW (frozen) ✓
  - 6: (4,3)→(4,4) NW (frozen) ✓ (would-be rotation at end of
    action 6 delayed by freeze)
  - 7: (4,4)→(4,5) NW (frozen) ✓ — **switch (4,5) triggered**;
    direction reversed to -1; rotor's direction-marker dot
    moves from clockwise-corner to counter-clockwise-corner.
  - 8: (4,5)→(3,5) NW (frozen) ✓
  - 9: (3,5)→(2,5) NW (frozen) ✓
  - 10: (2,5)→(1,5) NW ✓ — freeze end; rotation triggers,
    direction = -1 (counter-clockwise), so wedge → SW; tint
    → palette 11 (yellow).
  - 11: (1,5)→(1,6) SW ✓
  - 12: (1,6)→(1,7) SW ✓
  - 13: (1,7)→(1,8) SW ✓
  - 14: (1,8)→(1,9) SW ✓
  - 15: (1,9)→(1,10) SW ✓ — target reached.

  Validity check (each destination must be in lit sector or
  avatar dies):
  - Actions 1–10: wedge = NW (frozen 4-10), all destinations
    are gx ≤ 5 AND gy ≤ 5 (NW) ✓.
  - Actions 11–15: wedge = SW, all destinations are gx ≤ 5 AND
    gy ≥ 6 (SW) ✓.
  - No move attempts a wall cell (walls are (3,1), (3,2),
    (3,4); witness path passes through (1,2), (1,3), (2,3),
    (3,3), (4,3), (4,4), (4,5), (3,5), (2,5), (1,5), and SW
    cells — none coincide with walls).
  - No move attempts a rotor cell (rotor is (5,5)–(6,6); none
    of the witness destinations are in that block).

- **Difficulty justification**:
  - **(a) Random-resistance**: random policy must trigger
    stop-tile, navigate to switch, time the phase transition
    correctly, and walk SW — none of which is stumbled into.
    P ≪ 1/10,000.
  - **(b) Human-tractable**: ~3 minutes. M1 + M2 known from L1
    and L2; the new sprite at (4, 5) (counter-switch — a
    magenta spiral, distinct from the orange-dotted stop-tile)
    is the only non-floor object in the NW interior. Stepping
    on it produces an **observable cue** — the rotor's
    magenta direction-marker dot visibly moves to the
    opposite corner — teaching M3. The player then plans the
    one-quadrant traversal NW → SW.
  - **(c) Planning depth**: **planning is challenging even for
    an attentive human (post-discovery)**. Even with all three
    mechanics fully understood, the post-discovery player
    faces a non-trivial routing decision: visit *both* the
    stop-tile (extends NW phase) *and* the switch (reverses
    direction) AND end at a NW-cell adjacent to the SW
    boundary at gy = 5 (so action 11's south-step enters
    SW). The number of plausible NW paths that visit both
    tiles within 10 frozen-NW actions is small (≈ 3
    distinct routings, all close to the witness), but only
    paths that end at gx ≤ 5 AND gy = 5 succeed in transitioning
    to SW; ending at gy = 4 means action 11's south-step
    lands at gy = 5 still in NW (now dark), losing.

    **Trivial heuristic that fails (post-discovery)**:
    *greedy-toward-target* — "always pick the action that
    minimises Manhattan distance to (1, 10)". From (1, 1),
    greedy picks ACTION2 → (1, 2) repeatedly, then would walk
    south to (1, 5) then south again to (1, 6) — but with no
    stop-tile triggered (greedy never visits (2, 3)), the
    NW phase ends at action 6 with avatar at (1, 6) which is
    *outside NW* (gy = 6 ≥ 6 → SW). Action 6's destination
    is SW while wedge is NW — instant loss. Greedy diverges
    from the witness at action 3 (greedy picks ACTION2 to
    (1, 4); witness picks ACTION4 to (2, 3) — i.e.,
    greedy-toward-target's irrecoverable loss point is action
    6, before the switch is even reachable).

    **Why ahead-of-time reasoning is needed**: the player must
    *plan the entire NW path* before the first action — the
    constraint "visit (2, 3) AND (4, 5) AND end at gy = 5
    boundary inside 10 frozen-NW actions" is not satisfiable
    by a local heuristic that only sees the next move; the
    player must compute the path globally before committing.
  - **(d) Step budget**: **26 actions** (witness 15 + 11
    slack ≈ 73% margin). The budget is set strictly below
    the no-M3 alternate-1 path of 27 actions, *forcing* M3
    use; the budget is ≥ L2's 26 (the rule "L3 must not
    shrink relative to L2"); the witness's 11 actions of
    slack accommodates one death-and-retry attempt.

## 5. Action mapping

`available_actions = [1, 2, 3, 4]` — pure cardinal walk. No
ACTION5, no ACTION6, no ACTION7.

| Action | Semantic | Gating |
|---|---|---|
| ACTION1 | Move avatar one cell up (gy −= 1). Walls and the rotor block (action ticks; no move). Step into a free dark cell loses. | Always offered. |
| ACTION2 | Move avatar one cell down. | Same. |
| ACTION3 | Move avatar one cell left. | Same. |
| ACTION4 | Move avatar one cell right. | Same. |

ACTION7 deliberately omitted per `action-enum.md` strict-undo
rule — this game has no meaningful single-action undo (the
rotor's angular state and freeze counter form coupled state
that's awkward to roll back; the game is solvable without
undo).

`_get_valid_actions` returns the engine default — no
context-dependent gating is exposed.

## 6. HUD and per-game state

**HUD widgets** (in `Camera.interfaces` order):

1. `WedgeOverlay(RenderableUserDisplay)` — paints the lit-cell
   pattern. For every cell `(gx, gy)` whose sector matches the
   current `_rotor_angle`, the overlay paints palette 11
   (yellow) at the cell's 4 corner pixels and centre pixel at
   the cell's 5×5 rendered position. When `_frozen_remaining
   > 0`, the overlay uses palette 7 (pink) instead. Skips
   the rotor cells and the bottom row (which the StepCounter
   covers).

2. `RotorDirectionMarker(RenderableUserDisplay)` *[new for
   critique #2]* — paints a single palette 6 (magenta) pixel
   at the rotor's clockwise-next-corner (when `_direction =
   +1`) or counter-clockwise-next-corner (when `_direction =
   -1`). Rendered into the rotor sprite's bounding rectangle
   so it's always visible. Single-pixel; reads as a "this is
   where the notch goes next" indicator.

3. `StepCounterHud(RenderableUserDisplay)` — bottom row
   (`frame[63, :]`) painted palette 1 (off-white) for steps
   remaining and palette 4 (off-black) for spent. Standard.

The order `[WedgeOverlay, RotorDirectionMarker,
StepCounterHud]` ensures: wedge paints first inside the 60×60
playfield region; the direction marker paints at single pixel
inside the rotor's render area (overrides the wedge if it
happened to touch); the step counter paints last on row 63
which the wedge never touches (wedge stays inside the centred
60×60 area).

**Internal state per game**:
- `_rotor_angle: int ∈ {0, 1, 2, 3}` — current sector. 0 = NW,
  1 = NE, 2 = SE, 3 = SW. Reset to 0 in `on_set_level`.
  Advanced by `+_direction (mod 4)` at end of each action *if*
  `_actions_in_phase >= K` *and* `_frozen_remaining == 0`.
- `_direction: int ∈ {+1, -1}` — rotation direction. +1 =
  clockwise (default); -1 = counter-clockwise. Reset to +1
  in `on_set_level`. Toggled to `-1 * _direction` when avatar
  steps on a counter_switch sprite. Persistent visual cue:
  `RotorDirectionMarker` widget.
- `_actions_in_phase: int` — actions since last rotation.
  Resets to 0 at every rotation. Increments per action *unless*
  frozen.
- `_frozen_remaining: int` — actions remaining in stop-tile
  freeze. Decremented per action while > 0; rotation is
  inhibited (and `_actions_in_phase` does NOT increment) while
  > 0. Set to K' = 4 when avatar steps on a stop-tile.
  Persistent visual cue: WedgeOverlay paints palette 7 (pink)
  instead of palette 11 (yellow) while > 0.
- `_step_budget: int` — per-level countdown for `StepCounterHud`.
- `_actions_taken: int` — increments every action. `self.lose()`
  when `>= _step_budget`.

Per-level configuration via `level.get_data`: `step_budget`,
`avatar_pos`, `target_pos`, `walls` (list of `(gx, gy)` tuples),
`stop_tiles` (list; L2+), `counter_switches` (list; L3 only).

Module constants:
- `K = 6` — actions per sector phase.
- `K_PRIME = 4` — stop-tile freeze duration.
- `BACKGROUND_COLOR = 4`
- `PADDING_COLOR = 3`
- `LIT_TINT_NORMAL = 11` (yellow), `LIT_TINT_FROZEN = 7` (pink).
- `DIRECTION_MARKER_COLOR = 6` (magenta).

## 7. Win condition

Plain English: when the avatar's cell coincides with the
target's cell, the level wins. Fires `self.next_level()`. The
engine fires `self.win()` after the last level transitions.

Predicate (after each action):
```python
target = current_level.get_sprites_by_tag("target")[0]
if avatar.x == target.x and avatar.y == target.y:
    self.next_level()
```

Identical at L1, L2, L3.

## 8. Lose condition

Two predicates evaluated per action:
1. **Step-budget exhausted**: `_actions_taken >= _step_budget`
   → `self.lose()`.
2. **Stepped into free dark cell**: avatar's destination after
   a successful move was not in the lit sector AND was not
   blocked by a wall/rotor → `self.lose()`.

No respawn, no lives — single fatal step ends the run.
Matches `g50t` precedent (cleaner than fz5j's lives system;
the trade-off is harder for the agent but simpler for the
implementation and witness verification).

## 9. Novelty note

(See `mechanic-pick.md` § Novelty defence for full
articulation; summary form below.)

**Closest taxonomy entries** (none of the 25 references is an
exact mechanic match):
- *No reference uses an "auto-rotating angular sector that gates
  walkability" mechanic.* The closest taxonomy member is
  `g50t (walk-vs-scroll)` whose timer is unidirectional linear
  scroll. **Distinguishing rule: g50t's pressure is monotonic
  (the edge always advances); nz3v's pressure is cyclic (every
  angle returns every 4 phases).** Different mental models —
  one-shot race vs cyclical timing.

**Closest prior-game entries**:
- `fz5j (phase-step-tile)` — closest cousin. **Distinguishing
  rule: fz5j has independent per-cell pulse periods; nz3v has
  one global angular phase gating a contiguous quadrant.** The
  player reasons about angular position vs local arithmetic.
- `lq5x (lantern-cone-illuminate)` — directional cone projected
  from a player-carried lantern. **Distinguishing rule: lq5x's
  cone is player-controlled; nz3v's wedge is environment-
  driven and auto-rotates.**
- `vp6h (shadow-cast-collect)` — static pillars, slidable
  lanterns. **Distinguishing rule: vp6h's geometry is fully
  spatial; nz3v's region rotates every action regardless of
  input.**
- `pf3w (wavefront-converge-timing)` — concentric expanding
  circles. **Distinguishing rule: pf3w expands radial circles;
  nz3v rotates 90° angular sectors.**
- `xz5g (arena-pivot-rotate)` — click-to-set pivot, ACTION5
  rotates sprites. **Distinguishing rule: xz5g rotates sprites
  under player command; nz3v rotates a walkable region
  automatically.**
- `qz73 (radial-cycle-lock)` — rotor of tips, lock-to-socket.
  **Distinguishing rule: qz73 is a target-matching shape-
  alignment puzzle; nz3v is a navigation puzzle.**

The negative-similarity 8-dimension test was applied to fz5j
(the closest cousin); heavy axes (cast, visual signature,
pixel grain, core-dynamic flavour, environmental-vs-local
driver) all diverge — the candidate passes per the
`negative-similarity-check.md` rubric.

---

## Revision log (this revision)

Addresses 8 issues from `critique-revisions.md`:

1. **Avatar shape** (was chevron, read as `V`/`>`): redesigned
   to octagon-with-removed-corners. §3 sprite roster.
2. **Direction state cue** (was missing): added
   `RotorDirectionMarker` overlay; persistent magenta dot
   visible on rotor at any frame. §3 (rotor sprite description),
   §6 (HUD widgets).
3. **Frozen state cue** (was missing): WedgeOverlay paints
   palette 7 (pink) instead of palette 11 (yellow) while
   frozen. §4 (lit-cell rendering), §6 (HUD widgets).
4. **Wedge rendering** (was flat fill): now 4-corner-dot +
   centre pattern per cell; reads as textured zone, not
   uniform-colour blocks. §4 (lit-cell rendering).
5. **L3 spec readability** (had inline drafts): rewritten as
   single canonical layout + witness; intermediate drafts
   removed. §4 Level 3.
6. **Budgets non-decreasing** (was 28 → 22 → 22): now 22 → 26
   → 26. L1 reduced from 28 to 22 (witness 18 + 4 slack); L2
   raised to 26; L3 set to 26 (strictly below the no-M3
   alternate-1 path of 27 actions, so M3 strictly forced). §4.
7. **L3 witness verification** (had wall-collisions in prior
   draft): final witness traced action-by-action with explicit
   "wedge ✓" / "wall ✓" / "rotor ✓" checks. §4 Level 3.
8. **Stop-tile shape** (was X-cross): redesigned as 4-edge dots
   (palette 12 at top/bottom/left/right edge centres on
   palette 4 ground). Reads as a topological "+" cross which
   `forbidden-elements.md` explicitly permits. §3 sprite
   roster.
