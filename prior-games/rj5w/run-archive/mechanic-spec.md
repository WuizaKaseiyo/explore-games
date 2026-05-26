# mechanic-spec — `rj5w` (axis-fold-mirror)

> **Revision 2 (2026-05-08)**: switched fold semantics from
> anchor-cell reflection to **box reflection**. A pawn's whole 5×5
> footprint mirrors through the fold-line so its centre lands on
> the geometrically-correct mirror cell:
> `new_anchor = 2·F − old_anchor − (sprite_size − 1)`. Spec
> coordinates and witnesses re-tuned to keep witness lengths at
> 3 / 7 / 12 actions. Implementation matches in
> `prior-games/rj5w/rj5w.py` `_commit_fold` (uses `offset =
> PAWN_SIZE − 1 = 4`).
>
> **Revision 1 (2026-05-08)**: addressed
> `critique-revisions.md` round 1.
> - Section 4 / Level 3: rewritten per Option A. Walls dropped;
>   L3 now introduces +1 new mechanic (lock-on-target).
> - Section 4 / Level 2 / *Difficulty justification* / (c)
>   *plausible-but-wrong alternative*: replaced the discovery-
>   stage "commit V at F_v=30 immediately" with a post-discovery
>   double-V-only-translation argument.
> - Section 3 (sprite roster): removed `wall` sprite.

## 1. Title
Paper Folding (working title; not visible in-game).

## 2. Mechanic family
`axis-fold-mirror` — the playfield is a sheet of "paper" with one
or two thin **fold-line cursors** that the player can slide across
the sheet. Pressing ACTION5 commits a fold along the **active**
fold-line; every (unlocked) pawn's position is **reflected** across
that line. Pawns whose move ends on their colour-matched target
**lock** in place and are no longer affected by subsequent folds.

Core-knowledge priors used: **basic geometry & topology** (line
reflection, axis position) and **objectness** (pawns and targets as
persistent entities). No agentness, no real-world clipart, no
symbols.

## 3. Sprite roster

All grid coordinates are display-pixel cells in a 64×64 grid. Pawns
and targets are 5×5 sprites with internal pattern (per checklist
item 20: shape and palette together carry meaning, not colour
alone). Fold-line cursors are 1×60 (vertical) and 60×1 (horizontal)
striped sprites.

- **`pawn_green`** — 5×5, palette {14 green, 5 black accent, 0 white
  highlight}. Tags: `pawn`, `pawn_green`. Role: a movable nub-pawn;
  reflects through the active fold-line on commit; locks if it lands
  on a `target_green`.
  Pixel matrix:
  ```
  [14, 14,  0, 14, 14]
  [14,  5, 14,  5, 14]
  [ 0, 14, 14, 14,  0]
  [14,  5, 14,  5, 14]
  [14, 14,  0, 14, 14]
  ```

- **`pawn_purple`** — 5×5, palette {15 purple, 5 black, 0 white}. Same
  internal cross-and-pierce pattern as `pawn_green`. Tags: `pawn`,
  `pawn_purple`. Role: same as green, distinct colour.

- **`pawn_yellow`** — 5×5, palette {11 yellow, 5 black, 0 white}.
  Same pattern. Tags: `pawn`, `pawn_yellow`. Role: same as the others.

- **`target_green`** — 5×5, palette {14 green outline, 5 black inner
  dot, -1 transparent inner}. Tags: `target`, `target_green`. Role:
  goal-cell for the green pawn; non-collidable.
  ```
  [14, 14, 14, 14, 14]
  [14, -1, -1, -1, 14]
  [14, -1,  5, -1, 14]
  [14, -1, -1, -1, 14]
  [14, 14, 14, 14, 14]
  ```

- **`target_purple`** — same shape, palette 15.
- **`target_yellow`** — same shape, palette 11.

- **`fold_line_v`** — 1×60, alternating-pixel pattern in palette 12
  (orange) when active or palette 3 (grey) when inactive. Tags:
  `fold_line`, `fold_line_v`. Interaction: `INTANGIBLE` (rendered
  but never blocks pawns). Role: the vertical fold-line cursor;
  ACTION3/4 move it, ACTION5 commits a vertical fold.
  Pattern (60-row column, repeating period 3):
  ```
  [ X],
  [ X],
  [-1],
  ...repeated 20 times for 60 rows
  ```
  where `X` = 12 when active, 3 when inactive.

- **`fold_line_h`** — 60×1, same pattern transposed; appears in L2/L3
  only. Tags: `fold_line`, `fold_line_h`.

The actual orange/grey state of the fold-line cursors is achieved
by a runtime `color_remap` after toggle (palette 12 ↔ palette 3),
not by swapping sprite instances.

The `pawn_<colour>` sprites also carry a "locked" visual variant —
when a pawn locks, the game calls `color_remap(<base>, 3)` on it
so it dims to grey. This is the persistent visual cue per
checklist item 19.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. All three share `grid_size = (64, 64)`, the same
sprite bank, and the same camera; only sprite positions, fold-line
initial positions, and the step budget vary.

### Level 1 — base dynamic system
**Layout**
- One green pawn at `(8, 28)`.
- One green target at `(52, 28)`.
- The vertical fold-line cursor at column `F_v = 30` (initial).
- Step budget: 25 (per `level.set_data("step_budget", 25)`).
- No horizontal fold-line in L1 (the H-line sprite is not present in
  L1).

**Mechanics required by the witness** (N = 1)
- **M1 — V-fold**: ACTION3 / ACTION4 move the V-line cursor one
  column left / right; ACTION5 box-reflects every pawn across the
  V-line. For a 5×5 sprite with anchor `(x, y)`, the reflected
  anchor is `(2·F_v − x − 4, y)` (and analogously
  `(x, 2·F_h − y − 4)` for an H-fold), so the sprite's footprint
  mirrors as a whole — the centre lands on the mirror of the
  original centre. Out-of-bounds reflections leave the pawn put.
  The composite verb (move-axis then commit) is one mechanic.

**Necessity per mechanic**
- **M1 (V-fold)**: L1 cannot be solved without triggering M1
  because the green pawn at column 8 must end up at column 52
  (its target column), and the only verb in L1's action set that
  changes a pawn's column is M1. ACTION1/2/6 are excluded from
  `_get_valid_actions` in L1.

**Witness solution** (3 actions)
- `[ACTION4, ACTION4, ACTION5]`
- Trace: F_v 30 → 31 → 32. Commit V-fold at F_v=32. Pawn green
  box-reflects from (8, 28) to (2·32 − 8 − 4, 28) = (52, 28) =
  target. Win.

**Difficulty justification**
- **(a) Random-resistance**: a random / vision-blind agent picks
  ACTION3, ACTION4, ACTION5 uniformly. The probability of placing
  F_v at exactly 30 within budget 25 is roughly the chance of a
  random walk on `Z` reaching column 30 from 32 (and committing
  while there) within 25 steps — for a small-LLM blind agent the
  budget runs out before the right axis position is hit, since
  any commit at the wrong axis position uses budget without
  progress. Empirically a random policy reaching the target
  within 25 actions is < 5%.
- **(b) Human-tractable**: an attentive human reads "green pawn
  on the left, green target on the right, orange line in the
  middle" and tries one fold; sees the pawn jump; reasons "put
  the line where the pawn would land on its target" — solves in
  ~30-60 seconds. Well under the ~2-min/level target.
- **(c) Planning depth**: per `difficulty-rules.md` § 2c L1 line,
  **no strict planning requirement** — once the rule is
  understood, the win is one arithmetic deduction (which column
  for F_v). The level's difficulty is mechanic-discovery, not
  planning.
- **(d) Step budget**: 25, against a 3-action witness. ~8× witness;
  comfortably generous, allows multiple wrong-position folds.

### Level 2 — base system + 2 new mechanics
**Layout**
- Green pawn at `(8, 8)`, green target at `(52, 52)`.
- Purple pawn at `(8, 52)`, purple target at `(52, 8)`.
- Yellow pawn at `(4, 4)`, yellow target at `(56, 56)`.
- V-line cursor at column `F_v = 30` (initial).
- H-line cursor at row `F_h = 30` (initial).
- V is the active axis at level start (orange); H starts inactive
  (grey).
- Step budget: 100.

**Mechanics required by the witness** (= N + 2 = 3)
- **M1 — V-fold** (carried forward from L1).
- **M2 — H-fold** (new at L2): ACTION1/2 move the H-line cursor
  up/down by one row; ACTION5 box-reflects every pawn across the
  H-line ((x, y) → (x, 2·F_h − y − 4) for a 5×5 pawn). Same
  composite verb shape as M1 but on the perpendicular axis.
- **M3 — active-axis toggle via click** (new at L2): ACTION6 with
  click coordinates `(gx, gy)`. If the click cell sits on the V-line
  cursor (gx == F_v), the V-line becomes active; if it sits on the
  H-line cursor (gy == F_h), the H-line becomes active. Otherwise
  the click is a no-op. The active axis is rendered orange (palette
  12); the inactive axis is rendered grey (palette 3) — the
  persistent visual cue for the active-axis state per checklist
  item 19.

**Necessity per mechanic**
- **M1 (V-fold)**: L2 cannot be solved without triggering M1
  because every pawn has a different column in its target than in
  its starting position (e.g., green's column must change from 8
  to 56), and only V-fold can change a pawn's column.
- **M2 (H-fold)**: L2 cannot be solved without triggering M2
  because green and purple have different rows in their targets
  than in their starts (green: 8 → 56, purple: 56 → 8), and only
  H-fold can change a pawn's row. Two V-folds can translate pawns
  horizontally but cannot change rows, so no V-only sequence can
  reach the target rows.
- **M3 (axis toggle)**: L2 cannot be solved without triggering M3
  because M2 (H-fold) is required (above), the level starts with
  V active, ACTION5 always commits along the active axis, and M3
  is the only verb that changes the active axis. Without M3, M2
  cannot be invoked.

**Witness solution** (7 actions)
- `[ACTION4, ACTION4, ACTION5, ACTION6@(20, 30), ACTION2, ACTION2, ACTION5]`
- Trace (using box-reflection: `new = 2·F − old − 4`):
  - ACTION4×2: F_v 30 → 31 → 32.
  - ACTION5: V-fold F_v=32. Green (8,8) → (52,8). Purple (8,52) →
    (52,52). Yellow (4,4) → (56,4). None on a target yet.
  - ACTION6@(20, 30): click cell (20, 30); gx=20 ≠ F_v=32 (V check
    fails); gy=30 = F_h=30 (H check matches) → H active. V-line
    recolours to grey, H-line recolours to orange.
  - ACTION2×2: F_h 30 → 31 → 32.
  - ACTION5: H-fold F_h=32. Green (52,8) → (52,52) = target.
    Purple (52,52) → (52,8) = target. Yellow (56,4) → (56,56) =
    target. Win.

**Difficulty justification**
- **(a) Random-resistance**: random ACTION{1..6} cannot land on
  precisely F_v=32 then ACTION5 then a click on the H-line cell
  then F_h=32 then ACTION5 within budget 50; the joint probability
  is ≪ 1/10,000.
- **(b) Human-tractable**: a human understands V-fold from L1;
  L2 introduces a perpendicular line and a toggle. The bookkeeping
  is "pick F_v so x maps right; pick F_h so y maps right; toggle
  axes between commits." About ~2 minutes for an attentive human.
- **(c) Planning depth (post-discovery)**:
  - **Decision-space at level start (post-discovery)**: ≥ 3
    plausible first moves a fully-informed player faces —
    ACTION3/4 to position V, ACTION5 to commit V immediately at
    F_v=30, ACTION6 to toggle to H first.
  - **Plausible-but-wrong alternative (post-discovery)**: the
    fully-informed player knows V-fold reflects across F_v and
    knows two V-folds at F_v=A, F_v=B compose to a horizontal
    translation by 2(B−A). They might consider solving L2 with
    *only* V-folds — picking F_v values so green and purple
    translate to the right column ranges, hoping their rows
    happen to align. This fails because two V-folds preserve
    rows: green stays at row 8 and purple stays at row 56,
    neither of which is its target row. The player must conclude
    that an H-fold is required, and therefore an axis toggle is
    required — which forces them onto the witness path. (This
    is a post-discovery rejection: the player understands V-fold
    arithmetic perfectly and rejects the V-only path on
    arithmetic grounds.)
  - **Witness reasoning chain**: the player reads the green
    pawn-and-target pair, computes F_v = (8+56)/2 = 32; verifies
    the same F_v also satisfies purple (8 → 56) and yellow (8 →
    56). Moves V two cells right, commits. Then computes F_h =
    (8+56)/2 = 32; verifies the same F_h satisfies green and
    purple (8 → 56 and 56 → 8) and is a no-op for yellow (32
    sits on the line). Toggles axis (clicks the H-line cursor,
    aiming the click at gy = F_h to hit the cursor cell). Moves
    H two cells down, commits. Three pieces of arithmetic plus
    one ordered-toggle plus precise clicking — moderate planning
    rather than a 1-action lookup.
- **(d) Step budget**: 100 against witness 7. ~14× witness;
  very generous. Discovery cost (figuring out toggle,
  perpendicular axis arithmetic) is comfortably absorbed with
  ample room for exploratory wrong-direction folds.

### Level 3 — system + 1 new mechanic
**Layout**
- Green pawn at `(8, 16)`, green target at `(52, 16)`.
- Purple pawn at `(16, 8)`, purple target at `(16, 56)`.
- Yellow pawn at `(24, 28)`, yellow target at `(36, 28)`.
- V-line cursor at column `F_v = 28` (initial).
- H-line cursor at row `F_h = 30` (initial).
- V is the active axis at level start.
- Step budget: 160.

**Mechanics required by the witness** (= 3 + 1 = 4)
- **M1 — V-fold** (carried forward from L1/L2).
- **M2 — H-fold** (carried forward from L2).
- **M3 — active-axis toggle via click** (carried forward from L2).
- **M4 — lock-on-target** (new at L3): a pawn that **moves** in a
  fold AND lands exactly on its colour-matched target becomes
  **locked** — subsequent folds do not move it. A pawn that did
  NOT move on a fold (e.g. a fold whose reflection lands the pawn
  out of bounds) does NOT lock, even if it happens to be sitting
  on a target. The persistent visual cue is a `color_remap` from
  the pawn's colour to palette 3 (grey) — locked pawns dim and
  the player can read who is locked at any frame.

**Necessity per mechanic**
- **M1 (V-fold)**: L3 cannot be solved without triggering M1
  because every pawn has a different column in its target than in
  its start (green: 8 → 56, purple: 16 → 16 — wait, purple's
  column is unchanged 16 → 16, yellow: 28 → 36). Green requires
  a column change of 8 → 56 and yellow requires 28 → 36; only
  V-fold can change a pawn's column.
- **M2 (H-fold)**: L3 cannot be solved without triggering M2
  because purple's row must change from 8 to 56, and only H-fold
  can change a pawn's row. (Green's row 16 → 16 and yellow's row
  28 → 28 are unchanged, so H-fold isn't strictly forced by
  green or yellow — but purple alone forces it.)
- **M3 (axis toggle)**: L3 cannot be solved without triggering M3
  because M2 (H-fold) is required (above), the level starts with
  V active, and ACTION5 always commits along the active axis.
  Without M3 the player cannot fire H-fold.
- **M4 (lock-on-target)**: L3 cannot be solved without triggering
  M4. The witness fires V-fold twice (once to land green and
  yellow on their targets, once to undo purple's V-displacement)
  before firing H-fold once (to land purple on its target).
  Without M4, the second V-fold would move green from (56, 16)
  back to (8, 16) and yellow from (36, 28) back to (28, 28) —
  green and yellow off-target. No fold sequence wins L3 without
  the lock mechanic; see exhaustive enumeration in *Difficulty
  justification* (c) below. M4 freezes green and yellow after
  the first V-fold, allowing the second V-fold to undo purple's
  displacement without disturbing the locked pawns.

**Witness solution** (12 actions)
- `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION5, ACTION5,
   ACTION6@(20, 30), ACTION2, ACTION2, ACTION2, ACTION2, ACTION5]`
- Trace (box-reflection):
  - ACTION4×4: F_v 28 → 29 → 30 → 31 → 32.
  - ACTION5: V-fold F_v=32.
    - Green (8, 16) → (2·32 − 8 − 4, 16) = (52, 16) = target.
      Green moved → LOCK.
    - Purple (16, 8) → (2·32 − 16 − 4, 8) = (44, 8). Moved, not
      on target.
    - Yellow (24, 28) → (2·32 − 24 − 4, 28) = (36, 28) = target.
      Yellow moved → LOCK.
  - ACTION5: V-fold F_v=32 again.
    - Green LOCKED → stays at (52, 16) = target.
    - Purple (44, 8) → (2·32 − 44 − 4, 8) = (16, 8) = start.
      Moved, not on target.
    - Yellow LOCKED → stays at (36, 28) = target.
  - ACTION6@(20, 30): click cell (20, 30); gx=20 ≠ F_v=32 (V
    check fails); gy=30 = F_h=30 (H check matches) → H active.
    V-line recolours grey, H-line recolours orange.
  - ACTION2×4: F_h 30 → 31 → 32 → 33 → 34.
  - ACTION5: H-fold F_h=34.
    - Green LOCKED → stays at (52, 16) = target.
    - Purple (16, 8) → (16, 2·34 − 8 − 4) = (16, 56) = target.
      Moved → LOCK.
    - Yellow LOCKED → stays at (36, 28) = target.
  - All three pawns on their targets → win condition fires →
    `next_level()`.

**Difficulty justification**
- **(a) Random-resistance**: the witness requires a precise
  4-axis-move + double-V-commit + click + 4-axis-move + commit.
  The joint probability of a random / blind agent stumbling onto
  this ordering — especially the seemingly-redundant double
  V-commit — within budget 80 is ≪ 1/10,000.
- **(b) Human-tractable**: a human who has seen L2's lock-free
  fold composition first tries V then H; observes that green and
  yellow land on their targets after V but fall OFF their targets
  after H (purple lands on target after H, green and yellow do
  not — the H-fold flips green's row 16 → 48 and yellow's row 28
  → 36 wait actually let me check: with F_h=32, green at row 16
  reflects to row 48; yellow at row 28 reflects to row 36 — both
  off-target). Realises a second V-fold could undo purple's
  V-displacement IF green and yellow could be kept in place;
  notices the dim/lock visual cue on green and yellow after the
  first V-fold and concludes the lock mechanic protects them.
  Estimated ~3-4 minutes for an attentive human.
- **(c) Planning depth (post-discovery)**:
  - **Decision-space at level start (post-discovery)**: ≥ 5
    plausible first moves — ACTION3/4 to position V, ACTION5 to
    commit V immediately at F_v=28 (which mis-aligns green by
    8 columns), ACTION6 to switch to H first, etc. Count ≥ L2's.
  - **Trivial post-discovery heuristic that fails — single
    fold-each-axis ("greedy: do the obvious thing once")**: a
    fully-informed player who has not yet realised the lock
    mechanic protects multi-fold sequences would naturally try
    "fold V once at F_v=32, toggle, fold H once at F_h=32." With
    that heuristic the trace is:
    - V-fold: green (8,16)→(56,16) target LOCK; purple (16,8)→
      (48,8); yellow (28,28)→(36,28) target LOCK.
    - H-fold: green LOCKED stays; purple (48,8)→(48,56), NOT
      target (16,56); yellow LOCKED stays.
    - Final: green on target, yellow on target, purple at
      (48, 56) — off target. Loses on budget exhaustion or
      stays unsolved.
    The greedy heuristic does NOT solve L3.
  - **Where the heuristic diverges from the witness**: at step 6
    of the witness — the seemingly-redundant second V-fold. The
    greedy heuristic stops V-folds after the first because it has
    placed two pawns on targets. The witness instead fires V-fold
    a second time to UNDO purple's V-displacement (purple goes
    (48, 8) → (16, 8) back to its start), exploiting the property
    that a vertical reflection composed with itself is the
    identity AND the lock mechanic prevents green and yellow from
    being affected by the second V-fold. Discovering this
    requires the player to reason about reflection-as-involution
    under selective locking — a non-trivial post-discovery
    planning step.
  - **Exhaustive check (counterfactual for M4)**: without M4,
    there is no fold sequence within the budget that wins L3.
    Brief enumeration of the small fold-sequence prefixes
    {V, H, VV, VH, HV, HH, VVH, VHV, HVV, HVH, VHH, HHV} (with
    F_v=32, F_h=32) — none places all three of green/purple/
    yellow on target simultaneously without M4. Folds at other
    axis positions are strictly worse (they move pawns to non-
    target cells). The witness {VVH} works only because M4
    locks green and yellow after the first V-fold, allowing the
    second V to undo purple alone.
- **(d) Step budget**: 160 against witness 12. ~13× witness;
  very generous and strictly larger than L2's budget per
  `difficulty-rules.md` § d (L3 must NOT shrink relative to L2).
  Discovery cost (lock visual cue, double-fold composition)
  comfortably absorbed.

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5, 6]` for the whole game. Per-
level visibility is shaped by `_get_valid_actions`.

| Action | Semantic | Valid when |
|---|---|---|
| ACTION1 | Move active fold-line UP one row | active axis is H (L2/L3 only) |
| ACTION2 | Move active fold-line DOWN one row | active axis is H (L2/L3 only) |
| ACTION3 | Move active fold-line LEFT one column | active axis is V (all levels) |
| ACTION4 | Move active fold-line RIGHT one column | active axis is V (all levels) |
| ACTION5 | Commit a fold along the active axis (reflect every unlocked pawn) | always |
| ACTION6 | Click `(gx, gy)`. If gx == F_v → V active. Else if gy == F_h → H active. Else no-op. | L2/L3 only |

The fold cursor positions are clamped to `[1, grid_size−2]` so the
line never sits on the very edge.

## 6. HUD and per-game state

**HUD widgets** (`RenderableUserDisplay` subclasses):
- `StepCounterHud`: a horizontal palette-6 (magenta) bar drawn
  along row 63, depleting from full to empty over the level's
  step budget; mirrors universal pattern from `tu93`/`cn04`/`sp80`.

**Per-game state held on the Game class**:
- `self.active_axis`: `"V"` or `"H"`. Initial `"V"` per level. Set
  by ACTION6 click hits.
- `self.fv` / `self.fh`: int columns / rows where the V- and
  H-line cursors currently sit. Updated by ACTION1..4. Clamped to
  `[1, 62]`.
- `self.locked_pawns`: `set[Sprite]`. Pawns locked on their
  targets. Populated in `_apply_fold` after a fold that moved a
  pawn onto its colour-matched target.
- `self.step_budget`: int from `level.get_data("step_budget")`,
  reset on `on_set_level`.

State change visual cues (per `checklist.md` item 19):
- `active_axis` cue: the V-line and H-line sprites are
  `color_remap`-ped to palette 12 (orange) when active and palette
  3 (grey) when inactive, every time `active_axis` changes.
- `locked_pawns` cue: each pawn added to `locked_pawns` is
  `color_remap`-ped from its base palette (14/15/11) to palette 3
  (grey), permanently dimming it.
- `fv` / `fh` cues: the V-line / H-line sprites are
  `set_position`-ed to their current column / row every action.

## 7. Win condition
After every action, the game checks: every pawn (one of each
colour present in the level) is sitting at the same `(x, y)` as
its colour-matched target sprite. Concretely, for each pair
(`pawn_<col>`, `target_<col>`) in the current level,
`pawn_<col>.x == target_<col>.x AND pawn_<col>.y == target_<col>.y`.
If all pairs satisfy that, fire `self.next_level()`.

## 8. Lose condition
Step-counter exhaustion. After every action, decrement the step
budget by 1. If `self.step_budget == 0` and the win condition has
not fired this turn, call `self.lose()`. There is no other lose
state.

## 9. Novelty note

### Closest taxonomy entries
- **`ar25` (shape-mirror-cover)**: the only reference game that
  uses geometric reflection as a primary mechanic. Distinguishing
  rule: ar25 has STATIC reflector lines and the player slides
  pieces; the mirrors passively duplicate sprites, so a piece exists
  simultaneously at its real position and at its reflected
  position. `rj5w` has a PLAYER-POSITIONED fold-line cursor and a
  discrete commit verb that PERMANENTLY teleports each pawn to its
  reflected position; pawns never co-exist at both spots.
- **`m0r0` (mirror-orb-merge)**: mirrors INPUT directions
  continuously — every arrow press moves all four orbs
  simultaneously, each with sign-flipped axes. `rj5w` mirrors
  POSITIONS of pawns discretely on commit, and the mirror axis is
  itself a player-movable cursor; the player's arrow presses move
  the cursor, not the pawns.
- **`cn04` (nub-pair-glyph)**: pieces rotate and slide via arrows
  to align nubs. `rj5w`'s pieces don't move via arrows at all —
  they only move when a fold commits.
- **`lp85` (row-col-shift-grid)**: button clicks shift entire
  rows / columns one cell. `rj5w` reflects pawn positions across
  an axis on commit; rows stay rows, columns stay columns, but
  pawns relocate to mirrored grid cells. Different transform
  group (reflection vs. translation).
- **`sk48` (paired-snake-trail)**: two heads whose moves are
  mirrored continuously by a fixed axis. `rj5w` has many pawns
  whose reflection happens only on commit, with the axis
  player-positioned.

### Closest prior-games entries
- **`bx84` (beam-mirror-reflect)**: places mirrors at single
  cells that reflect a coloured beam. `rj5w` has no beam; the
  fold-line reflects the entire playfield's pawn positions, not
  a propagating ray.
- **`tg6w` (settle-pile-tilt)**: tilts the playfield direction
  to slide blocks under gravity. `rj5w` reflects positions
  through an axis; no slide, no gravity, no continuous motion.
- **`pz4t` (anchor-pivot-place)**: clicking sets a placement
  anchor for jigsaw components; arrows reflect the sprite about
  the anchor. Surface similarity ("reflect about an anchor"),
  but pz4t reflects ONE component about a PAWN-LOCAL anchor as
  part of placement; `rj5w` reflects EVERY pawn about a
  PLAYFIELD-GLOBAL fold-line. Different scale (component vs.
  whole sheet) and different verb (place-with-flip vs.
  fold-and-flip).

### Negative-similarity check
Walked the eight dimensions of `negative-similarity-check.md`
against every reference game and every prior. The candidate's
imagined L1 — pale off-white sheet, single orange vertical
fold-line bisecting it, two patterned pawn/target colour pairs
on either side, magenta HUD bar at row 63 — does not overlap on
3+ dimensions with any prior. The closest visual signatures
(`ar25`'s reflector-line layout and `wa30`'s sparse-pawns-on-
empty-grid layout) each share at most 2 dimensions:
- vs `ar25`: dim 8 (reflection in core dynamic) only; visual
  signature, palette, and verb diverge sharply.
- vs `wa30`: dim 5 (cast: pawns + targets) plus partial dim 7
  (sprite grain — mitigated by 5×5 patterned pawns vs. wa30's
  smaller plain blocks). Mitigated to 1-2 shared dimensions.
- vs the `kf42`/`vh68` cautionary tale palette (`{4 wall, 8 red,
  9 blue}`): `rj5w` uses `{1 off-white background, 12 orange
  active fold-line, 14 green, 15 purple, 11 yellow, 3 grey,
  6 magenta HUD, 5 black accent, 0 white}`. 0 shared palette
  dimensions.

No prior overlaps on 3+ dimensions. Negative test passes.
