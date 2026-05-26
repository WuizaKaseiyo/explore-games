# wj7d — fold-crease-overlay spec (revised after critique #1)

## 1. Title
Fold-Crease Overlay (working name; not visible in-game).

## 2. Mechanic family
`fold-crease-overlay`. The player consumes coloured **stamps** by
mirror-reflecting them across a single white **crease line**, with
the goal of covering pre-painted **shadow target** cells with the
stamp colour the shadow demands. The crease can move and switch
between horizontal/vertical orientation in late levels.

Core-knowledge priors used (per `core-knowledge-priors.md`):
- **Geometry & topology** — mirror reflection across an axis,
  axis re-orientation H↔V, axis translation.
- **Objectness** — coloured stamps are persistent objects with
  selection state and consumption-on-commit.

## 3. Sprite roster

Stamps are 6×6 sprites with internal pixel pattern; shadows are
6×6 sprites in the dim/lighter palette pair of the matching
stamp colour. Reflection arithmetic: a stamp with top-left at
(x_s, y_s) folded across a horizontal crease at row R has its
reflected top-left at (x_s, 2R − y_s − 5); folded across a
vertical crease at column C, reflected top-left at
(2C − x_s − 5, y_s). Because the stamp width/height is 6, the
constant `−5` enters reflection — see § 4 for the integer-grid
implications.

Sprites declared:

- **`step_counter_hud`** — `RenderableUserDisplay` subclass
  (`StepCounterHud`); not a `Sprite`. Renders row 0 as a 56-px
  depleting bar of palette 14 (green) over palette 4 (off-black),
  centred horizontally with 4 px margin each side.
- **`crease_h`** — 56×1 pixel sprite, all palette 0 (white).
  `tags=["crease"]`. Recoloured to palette 11 (yellow) when
  selected via `color_remap(0, 11)`. Layer 1.
- **`crease_v`** — 1×56 pixel sprite, palette 0 with same
  selection rule. `tags=["crease"]`. Only the H or V variant
  lives in the level at any time; re-orient swaps which is
  `InteractionMode.TANGIBLE` and which is `REMOVED`.
- **`stamp_red_cross`** — 6×6, palette 8 (red) cross + palette 0
  (white) accent. `tags=["stamp", "stamp_red"]`. Used in L1, L2, L3.
- **`stamp_blue_ring`** — 6×6, palette 9 (blue) ring + palette 0
  (white) accent. `tags=["stamp", "stamp_blue"]`. Used in L2, L3.
- **`shadow_red_cross`** — 6×6, palette 7 (pink) where the
  matching `stamp_red_cross` non-transparent pixels would be;
  palette `-1` elsewhere. `tags=["shadow", "shadow_red"]`. Layer
  -1 (under stamps). Pre-placed; never moves.
- **`shadow_blue_ring`** — 6×6, palette 10 (light-blue) for
  matching `stamp_blue_ring` cells. `tags=["shadow", "shadow_blue"]`.
- **`selection_halo`** — 8×8 sprite, hollow 1-px palette-15
  (purple) outline, transparent interior. Non-collidable.
  `tags=["halo"]`. Repositioned each turn around the currently-
  selected stamp; set to `InteractionMode.REMOVED` when no stamp
  is selected.

Concrete pixel patterns:

```
stamp_red_cross / shadow_red_cross  (-1 = transparent;
C = 8 for stamp, 7 for shadow):
[[-1, -1,  C,  C, -1, -1],
 [-1, -1,  C,  C, -1, -1],
 [ C,  C,  C,  C,  C,  C],
 [ C,  C,  C,  0,  0,  C],
 [-1, -1,  C,  C, -1, -1],
 [-1, -1,  C,  C, -1, -1]]

stamp_blue_ring / shadow_blue_ring  (-1 = transparent;
C = 9 for stamp, 10 for shadow):
[[-1,  C,  C,  C,  C, -1],
 [ C,  C, -1, -1,  C,  C],
 [ C, -1,  0, -1, -1,  C],
 [ C, -1, -1, -1, -1,  C],
 [ C,  C, -1, -1,  C,  C],
 [-1,  C,  C,  C,  C, -1]]

selection_halo (8×8, palette 15 outer ring only):
[[15, 15, 15, 15, 15, 15, 15, 15],
 [15, -1, -1, -1, -1, -1, -1, 15],
 [15, -1, -1, -1, -1, -1, -1, 15],
 [15, -1, -1, -1, -1, -1, -1, 15],
 [15, -1, -1, -1, -1, -1, -1, 15],
 [15, -1, -1, -1, -1, -1, -1, 15],
 [15, -1, -1, -1, -1, -1, -1, 15],
 [15, 15, 15, 15, 15, 15, 15, 15]]

crease_h (56×1, all palette 0); crease_v (1×56, all palette 0).
```

The white palette-0 accent in each stamp ensures internal pixel
structure beyond a single uniform colour, satisfying
`checklist.md` items 20 and 21.

## 4. Level progression, mechanic enumeration, and witness solutions

**Common mechanics across all levels.**

- Stamps move 4 pixels per arrow press, snapping their top-left
  to the 4-pixel grid (x, y ∈ {0, 4, 8, 12, ...}).
- Crease moves 4 pixels per arrow press (when crease is selected
  in L3), snapping to the 4-pixel grid for crease position.
- All grids are `(64, 64)` so the camera viewport equals the
  level grid_size (no scaling).

**Reflection-arithmetic / parity constraint.** With 6×6 stamps:
- *Horizontal crease at row R, source top-left y = y_s:*
  reflected top-left y = 2R − y_s − 5.
- *Vertical crease at col C, source top-left x = x_s:*
  reflected top-left x = 2C − x_s − 5.

Because the stamp dimension is even (6) and the −5 constant is
odd, when y_s and R are both on the 4-px grid (multiples of 4),
the reflected top-left y is **odd**. So shadow targets must be
placed at odd y (or odd x) coordinates to match exactly. This
constrains shadow placement but lets stamps stay on the
4-px movement grid.

**Per-level `data` dict** (for `level.set_data(...)` /
`level.get_data(...)`):
```
L1: {"step_budget": 30, "crease_movable": False,
     "crease_orient": "H", "crease_pos": 31,
     "auto_select_stamp": "stamp_red_cross"}
L2: {"step_budget": 50, "crease_movable": False,
     "crease_orient": "H", "crease_pos": 31,
     "auto_select_stamp": None}
L3: {"step_budget": 60, "crease_movable": True,
     "crease_orient": "H", "crease_pos": 31,
     "auto_select_stamp": None}
```

### Level 1 — base dynamic system

**Layout.**
- `crease_h` at row 31 (cols 4..59); `crease_movable=False`.
- `stamp_red_cross` at (x=8, y=8). Auto-selected; halo on.
- `shadow_red_cross` at (x=24, y=45). Pre-placed.

**Reflection check.** Shadow at (24, 45). Required source: y_s
satisfies 2·31 − y_s − 5 = 45 ⇒ y_s = 12. Required source x =
shadow x = 24. So stamp must reach (24, 12).

**Mechanics required by the witness** (N = 2):
- **M1 — MOVE-stamp.** Arrow keys translate selected stamp ±4 px
  along X or Y; bounded by playfield edges and crease (stamp
  may not cross the crease). At L1 the active half is rows
  4..30 (above the row-31 crease, leaving 1-px gap to crease).
- **M2 — FOLD-commit.** ACTION5 reflects every non-transparent
  pixel of the selected stamp across the crease and writes the
  reflected colour into `cells_covered[(x', y')]` for each
  reflected cell (x', y') that is on grid. The stamp is then
  consumed (removed from level via `set_interaction(REMOVED)`).
  Win-check is recomputed; lose-check (unwinnable) is recomputed.

**Necessity per mechanic** (counterfactual):
- *L1 cannot be solved without triggering M1 (MOVE-stamp) because*
  with stamp at (8, 8), its reflection across row 31 lands at
  cols 8..13, rows 53..58. Shadow at cols 24..29, rows 45..50.
  Zero overlap. The only red stamp would be consumed without
  covering the shadow → unwinnable → `lose()`. Player MUST
  move stamp to (24, 12) before folding.
- *L1 cannot be solved without triggering M2 (FOLD-commit)
  because* `cells_covered` only mutates via FOLD; no other
  action affects shadow-coverage state.

**Witness solution (6 actions):**
```
ACTION4 RIGHT  # x: 8 → 12
ACTION4        # 12 → 16
ACTION4        # 16 → 20
ACTION4        # 20 → 24
ACTION2 DOWN   # y: 8 → 12
ACTION5 FOLD   # source (24, 12) → reflected (24, 45);
               # shadow_red_cross at (24, 45) covered → win.
```

**Difficulty justification.**
- (a) **Random-resistance.** The stamp's reachable position grid
  is 14 × 7 = 98 cells; a random-policy agent has ≪ 1/98 chance
  per ACTION5 of being at the correct (24, 12); each wrong fold
  consumes the only stamp → unwinnable → lose. Per-level random
  win probability ≪ 1/1000; well below the 1/10000 §3.5 floor
  if iterated.
- (b) **Human-tractable.** ~1 min. A sighted player observes the
  matching shapes on either side of the crease line, infers
  "fold = mirror this onto that", and pre-positions the stamp.
- (c) **Planning depth.** No strict planning requirement (per
  `difficulty-rules.md` § 2.c — L1 is the discovery gate). Once
  the rule is understood, computing source from shadow is
  one-step arithmetic.
- (d) **Step budget.** 30 actions; witness 6; budget 5×.
  Generous over the witness, never tight per § 2.d.

### Level 2 — base system + 1 new mechanic (M3 = SELECT-among-stamps)

**Layout.**
- `crease_h` at row 31; `crease_movable=False`.
- `stamp_red_cross` at (x=8, y=4).
- `stamp_blue_ring` at (x=24, y=24). Blue's body at cols 24..29
  rows 24..29 overlaps red's required pre-fold destination
  cols 24..29 rows 20..25 on rows 24..25 — so red CANNOT reach
  its destination while blue still occupies its starting cell.
  The player must fold blue first.
- No stamp auto-selected.
- `shadow_red_cross` at (x=24, y=37). Required source: (24, 20).
  (2·31 − 20 − 5 = 37.)
- `shadow_blue_ring` at (x=16, y=41). Required source: (16, 16).
  (2·31 − 16 − 5 = 41.)

**Mechanics required by the witness** (= N+1 = 3; +1 new):
- **M1 — MOVE-stamp** (carried forward).
- **M2 — FOLD-commit** (carried forward).
- **M3 — SELECT-among-stamps.** Click (ACTION6) on a stamp's
  bounding box selects it (halo positioned). Clicking on a
  different stamp switches selection; clicking on empty cells
  deselects (halo hidden, arrows no-op). Default at level
  start: no selection.

**Necessity per mechanic** (counterfactual):
- *L2 cannot be solved without triggering M1 (MOVE-stamp).*
  Red at (8, 4) reflects to cols 8..13 rows 53..58; red shadow
  at cols 24..29 rows 37..42 ⇒ zero overlap. Red consumed
  without coverage → `lose()`. Blue at (24, 24) reflects to
  cols 24..29 rows 33..38; blue shadow at cols 16..21 rows
  41..46 ⇒ zero overlap. Blue consumed without coverage →
  `lose()`. Both stamps require movement.
- *L2 cannot be solved without triggering M2 (FOLD-commit).*
  Same reason as L1.
- *L2 cannot be solved without triggering M3 (SELECT).*
  At level start no stamp is selected; arrows are no-ops.
  Player MUST ACTION6 a stamp before any movement is possible.
  After the first fold consumes a stamp, selection is cleared
  → the player must ACTION6 again to operate on the second
  stamp. Witness contains exactly 2 stamp-selecting clicks;
  removing either drops to a no-op tail and lose.

**Witness solution (16 actions, blue-first to clear red's path):**
```
ACTION6 click(24, 24)  # select stamp_blue_ring
ACTION1 UP             # blue y: 24 → 20
ACTION1                # 20 → 16
ACTION3 LEFT           # blue x: 24 → 20
ACTION3                # 20 → 16
ACTION5 FOLD           # source (16, 16) → reflected (16, 41);
                       # shadow_blue_ring at (16, 41) ✓
ACTION6 click(8, 4)    # select stamp_red_cross
ACTION4 RIGHT          # red x: 8 → 12
ACTION4                # 12 → 16
ACTION4                # 16 → 20
ACTION4                # 20 → 24
ACTION2 DOWN           # red y: 4 → 8
ACTION2                # 8 → 12
ACTION2                # 12 → 16
ACTION2                # 16 → 20  (blue now consumed; collision
                       # cell is clear)
ACTION5 FOLD           # source (24, 20) → reflected (24, 37);
                       # shadow_red_cross at (24, 37) ✓ → win.
```

**Difficulty justification.**
- (a) **Random-resistance.** Joint probability of correct stamp
  selections + correct positionings + two correct folds ≪
  1/10000 per `from-tech-report.md` § 7's per-level floor.
- (b) **Human-tractable.** ~2 min. Player learns SELECT by
  observing initial arrow no-ops and clicking on a stamp; plans
  two folds; discovers the blue-blocks-red collision when red
  fails to move past row 24 and revises ordering.
- (c) **Planning depth (post-discovery).**
  - *Decision-space size at level start.* 2 distinct first
    progressing actions (click red, click blue). ≥ 2; not a
    1-action lookup.
  - *Trivial heuristic that fails (post-discovery).* "Greedy:
    fold the harder stamp first to get it out of the way."
    Red requires 8 movement actions (4 RIGHT + 4 DOWN); blue
    requires 4 (2 UP + 2 LEFT). A fully-informed player who
    knows both folds independently and applies the standard
    "harder-first" heuristic clicks red, presses RIGHT 4 times
    to reach col 24, then DOWN. On the 4th DOWN (y 16 → 20)
    the red body would collide with blue's body (cols 24..29
    rows 24..25 ∩ rows 24..29 = 2 rows × 6 cols = 12 cells of
    overlap); the move-stamp guard (§ 5) rejects the move
    (no-op). The player presses ACTION5 from y=16, source
    (24, 16) → reflected (24, 41); shadow_red at (24, 37..42);
    overlap rows 41..42 (2 rows × 6 cols = 12 cells covered
    of 26 non-transparent shadow pixels) → not full coverage
    → red consumed without covering shadow → unwinnable →
    `lose()`. The post-discovery player must observe the
    body-collision rejection and revise to fold blue first.
  - *Where the heuristic diverges from the witness.* On
    action #8 of the heuristic walk (red's 4th DOWN). The
    heuristic presses DOWN and the move is rejected; the
    witness's first 6 actions instead operate on blue.
  - *Operational test.* Walking the heuristic produces a
    different action prefix from the witness as soon as
    action #1 (heuristic clicks red, witness clicks blue);
    the heuristic continues to a `lose()` rather than
    converging on the witness path. This is a genuine
    post-discovery planning failure (not a discovery-stage
    misstep).
- (d) **Step budget.** 50 actions; witness 16; budget ~3.1×.
  Generous; allows the player to recover from a discovery-
  stage attempt at fold-red-first by retrying the level.

### Level 3 — system + 2 new mechanics (M4 = MOVE-CREASE, M5 = RE-ORIENT-CREASE)

**Layout.**
- `crease_h` at row 31; `crease_movable=True`.
- `stamp_red_cross` at (x=16, y=12).
- `stamp_blue_ring` at (x=40, y=8).
- No stamp auto-selected.
- `shadow_red_cross` at (x=45, y=16). Required setup: V crease
  at col=33, source (16, 16). (2·33 − 16 − 5 = 45; y preserved.)
- `shadow_blue_ring` at (x=40, y=41). Required setup: H crease
  at row=27, source (40, 8). (2·27 − 8 − 5 = 41; x preserved.)

**Why col=33 is the unique correct V-crease position.** The V
crease pivots at the player's click cell during re-orient. For
red's source (16, 16) to reflect to shadow (45, 16), we need
2C − 16 − 5 = 45 ⇒ C = 33. Clicking at any other column
during re-orient gives a wrong V crease and red's fold misses.
Specifically:
- col 32 (the natural visual midpoint of the 64-grid) ⇒
  reflected col = 43, shadow at col 45..50 ⇒ overlap cols
  45..48 (only 4 of 6 cols), partial coverage, lose.
- col 30 (a "round" choice) ⇒ reflected col = 39, no overlap.
- col 40 (where blue was clicked / folded) ⇒ reflected col =
  59, no overlap with shadow at 45.
- col 16 (red's source x — a "click on the stamp's column"
  intuition) ⇒ reflected col = 11, no overlap.

**Mechanics required by the witness** (= L2-count + 2 = 5; +2 new):
- **M1 — MOVE-stamp** (carried forward; red moves DOWN once).
- **M2 — FOLD-commit** (carried forward).
- **M3 — SELECT-among-stamps** (carried forward).
- **M4 — MOVE-CREASE.** With no stamp selected, ACTION6-clicking
  on a crease cell selects the crease. Subsequent arrow presses
  perpendicular to the crease's orientation (UP/DOWN for H;
  LEFT/RIGHT for V) translate the crease ±4 px on the perpendicular
  axis. Bounded between 6..58 (so a target half always exists).
- **M5 — RE-ORIENT-CREASE.** With the crease already selected,
  a SECOND ACTION6 click on a crease cell pivots its
  orientation H↔V at the click cell. (E.g., H crease at row R
  re-oriented by a click at (col=C', row=R) becomes V crease
  at col=C'.) The crease stays selected after re-orient.

(Selection state machine: at most one of {None, "stamp:i",
"crease"}. ACTION6 click resolves: if cell is on a stamp's
bounding box → select that stamp. Else if cell is on the
crease line and crease is NOT selected → select crease. Else
if cell is on the crease line and crease IS selected →
re-orient at that cell. Else → deselect everything. Arrow keys
act on the currently selected target only.)

**Necessity per mechanic** (counterfactual):
- *L3 cannot be solved without triggering M1 (MOVE-stamp).*
  Red stamp at (16, 12). Required source for V@33 fold is
  (16, 16). Without DOWN, fold from (16, 12) → reflected (45,
  12); shadow at (45, 16..21); overlap rows 16..17? Reflected
  rows = source rows = 12..17; shadow rows 16..21; overlap
  rows 16..17 (2 rows × 6 cols = 12 of 26 pixels). Partial
  coverage → red consumed without full coverage → unwinnable
  → `lose()`.
- *L3 cannot be solved without triggering M2 (FOLD-commit).*
  Same reason as L1/L2.
- *L3 cannot be solved without triggering M3 (SELECT-among-
  stamps).* At level start no stamp/crease is selected; arrows
  are no-ops. The player MUST ACTION6 click both the crease
  and each stamp before acting on them. Witness contains 4
  ACTION6 clicks (1 for crease select, 1 for re-orient, 2 for
  stamp selects). Removing any of the 2 stamp-selects breaks
  the witness.
- *L3 cannot be solved without triggering M4 (MOVE-CREASE).*
  Blue at (40, 8). Default H crease at row 31 reflects blue
  to cols 40..45 rows 53..58. Blue shadow at cols 40..45 rows
  41..46 ⇒ zero overlap. The player must MOVE the H crease
  to row 27 (1 ACTION1 press from row 31) so reflection lands
  at rows 41..46.
- *L3 cannot be solved without triggering M5 (RE-ORIENT-CREASE).*
  Red shadow at (45, 16). With ANY horizontal crease at any
  row, reflection preserves x; red's reflected x stays 16;
  shadow x is 45 ⇒ no overlap. The player must RE-ORIENT to
  a vertical crease at col=33. (Any non-vertical orientation
  fails for red.)

**Witness solution (9 actions):**
```
ACTION6 click(32, 31)  # click on crease_h at any col → select crease
ACTION1 UP             # crease H: row 31 → 27
ACTION6 click(40, 8)   # select stamp_blue_ring
ACTION5 FOLD           # source (40, 8) → reflected (40, 41)
                       # shadow_blue_ring at (40, 41) ✓
ACTION6 click(33, 27)  # click on H crease at col=33 row=27 → select
ACTION6 click(33, 27)  # second click on selected crease at the same
                       # cell → re-orient: V at col=33
ACTION6 click(16, 12)  # select stamp_red_cross
ACTION2 DOWN           # red y: 12 → 16
ACTION5 FOLD           # source (16, 16) → reflected (45, 16)
                       # shadow_red_cross at (45, 16) ✓ → win.
```

**Difficulty justification.**
- (a) **Random-resistance.** Joint probability of clicking the
  right crease cell, the right stamps, doing the right arrow
  presses, and folding twice in the right order ≪ 1/10000.
- (b) **Human-tractable.** ~2-3 min. Player carries L1/L2
  knowledge, learns crease selection by clicking on it and
  observing yellow recolour, learns crease MOVE by pressing
  arrows, learns RE-ORIENT by clicking the crease again on a
  selected crease and observing H↔V pivot. Plans two folds
  with crease changes.
- (c) **Planning depth (post-discovery).**
  - *Decision-space size at level start.* 3 distinct first
    progressing actions: click red, click blue, click crease
    cell. ≥ L2's 2; never smaller.
  - *Trivial heuristic that fails (post-discovery).* "Re-orient
    the crease by clicking whichever crease cell is most
    convenient." A fully-informed player who knows the
    re-orient mechanic but has not solved for the exact pivot
    column might click at the natural visual midpoint
    (col=32) or at the column where blue was just folded
    (col=40) or at red's own column (col=16). Each of these
    yields a wrong V crease (at col=32, 40, or 16
    respectively). Following through with the witness's
    remaining steps then produces a fold whose reflected
    footprint either overlaps the red shadow only partially
    (col=32 case: overlap cols 45..48 of shadow's 45..50, 4
    of 6 columns) or not at all (col=40 → reflected col 59;
    col=16 → reflected col 11). Red consumed → red shadow
    not fully covered → unwinnable → `lose()`.
  - *Where the heuristic diverges from the witness.* On
    action #5 of the witness — the click that selects the
    crease for the second re-orient phase. The witness
    requires the click at (33, 27); the heuristic clicks at
    a "convenient" column. The subsequent fold (action #9)
    then misses the shadow.
  - *Operational test.* Walking the convenient-click heuristic
    from a fully-informed start: actions 1–4 are correct
    (move crease H to row 27, fold blue). Action 5 deviates
    (clicks at e.g. (32, 27) instead of (33, 27)). Actions 6–9
    follow the witness skeleton. ACTION5 at action 9 produces
    a partial-coverage fold of red → lose. The action
    sequence DIFFERS from the witness at action 5 → genuine
    post-discovery planning failure.
- (d) **Step budget.** 60 actions; witness 9; budget ~6.7×.
  Generous, never shrinking across levels (L1=30, L2=50,
  L3=60).

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5, 6]`. No undo.

- `ACTION1`: UP. Selected stamp: y −= 4. Selected H crease (L3
  only): row −= 4. Selected V crease: ignored. No-op when
  nothing selected or move would leave grid / cross crease.
- `ACTION2`: DOWN. Selected stamp: y += 4. Selected H crease:
  row += 4. V crease: ignored.
- `ACTION3`: LEFT. Selected stamp: x −= 4. Selected V crease:
  col −= 4. H crease: ignored.
- `ACTION4`: RIGHT. Selected stamp: x += 4. Selected V crease:
  col += 4. H crease: ignored.
- `ACTION5`: FOLD. Reflects the selected stamp across the
  current crease and writes pixel colours into `cells_covered`
  for each on-grid reflected cell; consumes the stamp via
  `set_interaction(REMOVED)`. After fold the engine recomputes
  win-check (every shadow cell covered with matching colour →
  win) and lose-check (any uncovered shadow has zero remaining
  same-colour stamps → lose). No-op + step-counter tick when
  no stamp is selected, or when the crease is selected (folding
  needs a stamp).
- `ACTION6 click(x, y)`: routes through `camera.display_to_grid`
  and applies the SELECT state machine described in § 4 L3
  (which also applies in L1/L2 but with the crease being
  unselectable when `crease_movable=False`).

Movement-guard rules:
- Stamp may not move past playfield outer edges (top-left x ∈
  [0, 58], y ∈ [0, 58] for a 6-wide stamp on a 64-grid).
- Stamp may not cross the crease (the active half stays on the
  same side relative to the crease as the stamp's start
  position; moves that would put any stamp pixel on the crease
  row/col or on the other side are rejected as no-ops).
- Stamp may not collide with another tangible stamp's pixel-
  perfect footprint (move rejected as no-op). This is what
  enforces the L2 ordering twist.
- Crease may not move within 6 px of the playfield edge (H
  crease row ∈ [6, 58]; V crease col ∈ [6, 58]).

## 6. HUD and per-game state

**HUD widget.**

`StepCounterHud(RenderableUserDisplay)` — draws row 0 as a
56-px-wide depleting bar centred at cols 4..59. Filled cells are
palette 14 (green); drained cells are palette 4 (off-black). The
widget reads `current_steps` set in `step()` per cross-cut-
frequencies row 1.

**Persistent visual state cues** (per `checklist.md` item 19).

- *Selected stamp.* `selection_halo` sprite at TANGIBLE,
  positioned (-1, -1) offset from the stamp's top-left so the
  halo's 8×8 outline surrounds the 6×6 stamp body. When no
  stamp selected, halo set to `InteractionMode.REMOVED`.
- *Selected crease (L3 only).* `color_remap(0, 11)` recolours
  the active crease sprite (whichever of crease_h/crease_v is
  TANGIBLE) from white to yellow. Reverts on deselect.
- *Crease orientation.* The active crease sprite is one of
  `crease_h` (1×56 horizontal) or `crease_v` (56×1 vertical);
  the other variant has `interaction=REMOVED`. Visually
  legible from the rendered frame.
- *Crease position.* Where the crease pixel lives on the
  rendered frame.
- *Active vs target half.* Implicit from where stamps live
  (one side of the crease) vs where shadow targets live (the
  other side).
- *Coverage progress.* Each cell that has been folded onto is
  redrawn with its stamped colour value (overrides the dim
  shadow pixel underneath); the player sees shadows turning
  from dim to saturated as folds complete.
- *Step counter.* HUD bar.

**Internal game state** (`self.<...>`):
- `selected_stamp: Sprite | None`.
- `crease_selected: bool`.
- `crease_orient: Literal["H", "V"]`.
- `crease_pos: int` (row for H, col for V).
- `crease_movable: bool` (read from level data once per level).
- `cells_covered: dict[(int, int), int]` — colour value
  written into each cell by past folds.
- `step_remaining: int`.

`_get_hidden_state()` returns a 4×4 int16 array packing
`(selected_stamp_index, orient_flag, crease_pos, covered_count)`
so distinct internal states map to distinct graph nodes.

## 7. Win condition

After every successful `ACTION5` (FOLD), the engine recomputes
`cells_covered`. Then:

> A level wins iff for every cell of every active `shadow`
> sprite, `cells_covered[(world_x, world_y)]` equals the
> matching stamp colour (red shadow ⇄ 8; blue shadow ⇄ 9).

If true: `self.next_level()` (or `self.win()` after the last
level).

## 8. Lose condition

Two `lose()` triggers:

1. **Step budget exhaustion.** At the top of `step()`,
   `step_remaining −= 1`; if `step_remaining < 0` and the
   current level is not won, fire `self.lose()`.
2. **Unwinnable-state detection** (avoids soft-locks). After
   every fold, for each active shadow sprite, check whether
   any uncovered pixel exists AND whether at least one stamp
   of the matching colour still remains in the active half;
   if there is an uncovered shadow whose colour has zero
   remaining stamps, fire `self.lose()` immediately. This
   prevents the player from waiting out the budget after a
   misfold per `difficulty-rules.md` § 1's no-soft-lock rule.

## 9. Novelty note

(Same as the spec's previous version; reproduced for
self-containment after the L2/L3 layout changes — the changes
do not affect the novelty argument.)

**Closest taxonomy entries:**

- **`ar25` (shape-mirror-cover).** Continuous mirror-ghost of a
  single shape that slides whenever the player slides the
  shape; player wins by passing the ghost over scattered dots.
  *Distinguishing rule:* wj7d's ACTION5 (FOLD) is a destructive
  one-shot commit that consumes the stamp; no continuous ghost.
  The crease is also movable and re-orientable (L3); ar25's
  mirror only translates with the shape and never re-orients.
- **`cn04` (nub-pair-glyph).** Click-select then arrow-slide
  then ACTION5-rotate-90. *Distinguishing rule:* wj7d's ACTION5
  reflects across a separate movable crease and consumes the
  stamp; cn04's ACTION5 rotates the selected glyph in-place.
- **`cd82` (orbit-fire-paint).** Fires paint from an orbital
  tank into a fixed central canvas. *Distinguishing rule:*
  cd82 paints a wedge in the loaded swatch colour; wj7d
  reflects a stamp's specific multi-cell pixel pattern across
  a crease.
- **`pz4t` (anchor-pivot jigsaw).** Per-piece reflection /
  rotation anchored at a clicked pixel; tiles a connected
  region. *Distinguishing rule:* wj7d uses one global crease
  shared by all stamps and the targets are scattered shadows
  not a connected region.

**Closest prior-games entries:**

- **`bx84` (beam-mirror-reflect).** Click-placed mirror tiles
  deflect a stepwise-propagating beam. *Distinguishing rule:*
  no beam in wj7d; reflection is a one-shot stamp commit
  across a single global axis sprite.
- **`qz73`, `pj7k`, `kf42`, `kx14`, `qb84`, `lq5x`, `gv47`,
  `hr8q`, `ng52`, `vn8d`, `fz5j`, `kn58`, `wt39`, `zk9p`,
  `rk7x`, `gx7m`, `vp6h`, `kp9z`, `zd7m`, `lv4k`, `xn5p`,
  `mr5q`, `pf3w`, `tg6w`, `vd3g`, `jd4q`, `ek73`, `tm5x`,
  `qx7p`, `kj82`, `nb6t`, `qm4t`, `qn7w`, `zw91`, `fb7t`** —
  none use mirror reflection across a movable axis as a
  discrete consume-fold verb. All distinguishing rules
  centre on this verb.

**Negative-similarity-check (7 dimensions).** Re-walking the
fleshed-out spec against ar25 (closest visual signature):
shared on dims 1 (axis + things-on-each-side), 3 (shadow
coverage), 4 (step-counter lose) — universal dimensions;
divergent on the heavy dims 6 (palette signature: stamps
+ matching dim shadows in pink/light-blue/etc.), 7 (pixel
grain: 6×6 patterned stamps with internal accents, not
sparse pieces), 8 (core dynamic: discrete consume-by-fold
vs continuous ghost-slide). Pass.
