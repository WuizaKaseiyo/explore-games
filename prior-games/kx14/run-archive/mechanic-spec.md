# mechanic-spec — kx14 (`tide-tilt-buoyant`)

## 1. Title
**Tide-Tilt Buoyant** *(working title; not visible in-game).*

## 2. Mechanic family
The playfield is a vertical cross-section of a fluid tank: light-blue
water fills cells from a movable surface row down to the bottom, off-white
air fills the cells above. Buoyant balls float on the water surface; the
player moves them by raising/lowering the water level (vertical
displacement) and by applying horizontal **tilt** nudges. Solid platforms
inserted into the tank shape the path. An anchor toggle pins individual
balls in place against both tide and tilt. Win = every coloured ball
matches its same-coloured target ring.

§3.4 prior categories used: **basic physics** (buoyancy, water-surface
inertia, tilt-as-impulse), **objectness** (balls/platforms/targets as
persistent entities), **basic geometry/topology** (platforms partition
the tank into vertically-routed compartments). Agentness is deliberately
absent — there are no autonomous antagonists.

## 3. Sprite roster

All sprites use 1 cell = 5 pixels (grid_size = 12×12 → camera scale = 5×).

| Name | Dims (px) | Palette values | Tags | One-line role |
|---|---|---|---|---|
| `wkkqxbjzye` | 60×60 | {10, −1} | `["water"]` | Water bulk. Pixels mutated each tide change so cells `y >= water_level` (in cell-space) are palette-10, others transparent. Layer −1 (renders below balls/platforms). |
| `dmzpvavhuh` | 5×5 | {12, 4, −1} | `["ball"]` | Floating ball. Default colour palette-12 (orange); per-instance `color_remap(12, target_color)` for green / other. Inner 3×3 is palette-4 (off-black) with a palette-12 centre dot. Outer ring is the ball colour. |
| `vqfwzbpxir` | 5×5 | {12, 5, −1} | `["ball", "anchored"]` | Anchored variant: same outer ring shape, but inner 3×3 is solid palette-5 (black). Used together with `dmzpvavhuh` via `InteractionMode.TANGIBLE`/`REMOVED` swap (per universal-scaffold's "Two-sprite swap" pattern). One pair per placed ball. |
| `xqgntpsmcy` | 5×5 | {14, −1} | `["target"]` | Hollow target ring; default palette-14 (green); per-instance `color_remap` for orange / other. Outer ring solid colour, inner 3×3 transparent so the matching-coloured ball "fits inside" and the colour-match is visually crisp. |
| `obgtbrhmfd` | 15×5 | {3, 5} | `["platform"]` | 3-cell-wide horizontal solid platform: palette-5 black top edge (1 px), palette-3 grey 3-px body, palette-5 black bottom edge (1 px). Spans 3 cells in one row. Static; no per-instance recolour. |

The 25-game library convention is satisfied: opaque 10-character random
names, internal patterns on every sprite (no plain 1×1/2×2/3×3 colour
rectangles per the kf42→vh68 cautionary tale).

## 4. Level progression, mechanic enumeration, and witness solutions

Grid size: 12×12 cells across all three levels. Camera width/height set
to 12 (cells) in `on_set_level`, scale = 5 px/cell, viewport = 60×60
centred in the 64×64 frame with a 2-pixel letterbox of palette-3 grey.
Row 0 of the frame is the top letterbox; the HUD step-bar lives there.

The water surface row is `water_level` (an int in `[0, 11]`). Cells with
`row >= water_level` are water (palette-10); cells with `row <
water_level` are air (palette-1, the camera background). Balls float at
`water_level` by default; platforms can pin a ball above its desired
floating row, leaving the ball "submerged" (below the water surface in
its column). Re-projection runs after every action that changes the
playfield state — see §6 for the formal rule.

### Level 1 — base dynamic system (N = 2 mechanics)

- **Layout.** `water_level = 8` (rows 8–11 are water). One **orange
  ball** at cell `(3, 8)` (column 3, row 8 = floating on surface). One
  **orange target ring** at cell `(8, 4)`. No platforms. No anchor
  available (anchor disabled in L1 — only ACTION6 clicks on balls in
  L1 are no-ops). Step budget = **25**.
- **Mechanics required by the witness.**
  1. **M1 — water-level control.** ACTION1 raises `water_level` by 1
     (water surface moves up); ACTION2 lowers it by 1. Buoyant balls
     follow the surface unless blocked.
  2. **M2 — tilt.** ACTION3 nudges every un-anchored ball one cell left
     (in tilt order top-to-bottom, left-to-right); ACTION4 nudges every
     un-anchored ball one cell right (in reverse tilt order). A ball
     blocked by another ball or a platform-cell or the grid boundary
     stays put.
  Both mechanics required: the witness raises water (M1) AND tilts
  right (M2) — the ball cannot reach the target with one alone.
- **Witness solution (9 actions).**
  ```
  ACTION1, ACTION1, ACTION1, ACTION1,            # water 8→4, ball (3,8)→(3,4)
  ACTION4, ACTION4, ACTION4, ACTION4, ACTION4    # tilt right ×5, ball (3,4)→(8,4)
  ```
  L1 win predicate fires after the 9th action (orange ball at (8,4)
  collides with orange target ring at (8,4); colour-match passes).
- **Difficulty justification.**
  - *Random-resistance.* The ball must travel from (3,8) to (8,4) — a
    delta of `Δcol=+5, Δrow=-4`. With a 25-step budget and an action
    space of 4 directionally-meaningful keys (raise / lower / tilt-left
    / tilt-right), a uniform-random policy chooses correctly with
    probability `(1/4)^9 = 4×10⁻⁶` per 9-action prefix; over 25-step
    trajectories the expected number of solutions ≪ 1. A vision-blind /
    text-only LLM cannot infer that the un-named arrow keys do raise /
    lower / tilt without seeing the rendered consequences.
  - *Human-tractable.* An attentive human or top vision-language model,
    on first sight of the screen, sees a ball, a hollow ring at a
    different cell, and a step-counter; pressing UP a few times reveals
    the rising water surface and ball, pressing RIGHT reveals tilt.
    Solve time once mechanic is understood: ~30 seconds. Solve time
    including discovery: ~2 minutes.
  - *Planning depth.* Near-zero — mechanic discovery IS the difficulty.
    Once both verbs are understood, the action sequence is direct.

### Level 2 — base system + 1 new mechanic (N+1 = 3 mechanics)

- **Layout.** `water_level = 9`. **Orange ball** at `(1, 9)`. **Orange
  target ring** at `(10, 3)`. **One platform** at row 6, columns 0–2
  (occupies cells `(0,6)`, `(1,6)`, `(2,6)`). Step budget = **30**.
- **Mechanics required by the witness.**
  1. M1 (water-level control) — *carried forward from L1.*
  2. M2 (tilt) — *carried forward from L1.*
  3. **M3 — platform-block.** A platform-cell occupied by sprite-pixel
     palette-3 or palette-5 blocks both vertical re-projection (a ball
     in the same column whose target row would cross the platform stops
     at platform-row + 1 when rising or platform-row − 1 when falling)
     and horizontal tilt (a ball cannot tilt into a platform-cell).
  All three mechanics required: the witness goes UP into the platform's
  blocking row and is forced to tilt right past the platform's
  rightmost column before continuing the rise (M3 forces the
  intermediate tilt that the no-platform witness would not need).
- **Witness solution (15 actions).**
  ```
  ACTION1, ACTION1, ACTION1,            # water 9→6, ball (1,9)→(1,7) (blocked at platform row 6)
  ACTION4, ACTION4,                     # tilt right ×2, ball (1,7)→(3,7) (past platform's right edge)
  ACTION1, ACTION1, ACTION1,            # water 6→3, ball (3,7)→(3,3) (col 3 has no platform)
  ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4   # tilt right ×7, ball (3,3)→(10,3)
  ```
  L2 win predicate fires after the 15th action.
- **Difficulty justification.**
  - *Random-resistance.* Action sequence has length 15 with internal
    structure (raises must be interleaved with tilts at the right
    moments). A spam-the-new-verb agent that just presses ACTION1
    repeatedly stalls the ball at row 7 (platform blocks further rise);
    a spam-tilt-right agent never lifts the ball off row 9 (target row
    3 is unreachable without raising water). Per `(1/4)^14 ≈ 4×10⁻⁹`
    probability for any specific 14-action prefix.
  - *Human-tractable.* Once the player has experienced the platform
    block (one stuck press), the route is visible: tilt past the
    platform's right edge, then raise the water. ~2 minutes including
    the brief "why won't it rise" exploration.
  - *Planning depth.* Deliberate multi-step sequencing: the player must
    notice that columns 0–2 are blocked at row 6 and CHOOSE to deflect
    to column 3 BEFORE raising further. A monotone-progress strategy
    ("always press UP toward the goal") fails on the platform.

### Level 3 — system + 1 more new mechanic (N+2 = 4 mechanics)

- **Layout.** `water_level = 9`. **Orange ball** at `(3, 9)`, **green
  ball** at `(8, 9)`. **Orange target ring** at `(8, 5)`, **green
  target ring** at `(3, 5)`. (The two balls must SWAP horizontal sides
  while landing at row 5.) **One platform** at row 6, columns 4–6
  (cells `(4,6)`, `(5,6)`, `(6,6)`). Step budget = **45**.
- **Mechanics required by the witness.**
  1. M1 (water-level control) — *carried forward.*
  2. M2 (tilt) — *carried forward.*
  3. M3 (platform-block) — *carried forward.*
  4. **M4 — anchor toggle.** ACTION6 click `(x, y)` is converted via
     `camera.display_to_grid(x, y)` to a grid cell. If a ball occupies
     that cell, swap its `dmzpvavhuh` (float) and `vqfwzbpxir`
     (anchored) sprite pair via `set_interaction(InteractionMode.…)`.
     Anchored balls (a) do not follow water-level changes, (b) do not
     move on tilts, (c) act as obstacles for other balls' tilt motion
     and re-projection. Misclicks (no ball under the click) do not
     consume a step.
  All four mechanics required: M4 specifically is needed because two
  balls cannot pass each other (they cannot swap via tilt alone — tilt
  moves both in the same direction). Anchoring one ball while the
  other moves around it is the ONLY way to swap the pair.
- **Witness solution (21 actions; addresses critique-revisions.md
  Issue 1 — single canonical witness, aborted-draft block removed).**
  ```
   1. ACTION6@(3,9)*    # anchor orange ball at (3,9)
   2. ACTION1           # water 9→8; orange pinned at (3,9); green (8,9)→(8,8)
   3. ACTION1           # water 8→7; green (8,8)→(8,7)
   4. ACTION1           # water 7→6; green (8,7)→(8,6) (col 8 clear at row 6, platform is cols 4–6)
   5. ACTION1           # water 6→5; green (8,6)→(8,5)
   6. ACTION3           # tilt left; green (8,5)→(7,5) (row 5 clear, platform at row 6)
   7. ACTION3           # tilt left; green (7,5)→(6,5)
   8. ACTION3           # tilt left; green (6,5)→(5,5)
   9. ACTION3           # tilt left; green (5,5)→(4,5)
  10. ACTION3           # tilt left; green (4,5)→(3,5) — green at its target
  11. ACTION6@(3,5)*    # anchor green at (3,5) so it stays through the rest
  12. ACTION6@(3,9)*    # unanchor orange; orange re-projects upward in col 3,
                        # blocked by anchored green at (3,5); lands at (3,6)
  13. ACTION2           # water 5→6; orange at (3,6) is now at the surface (no motion)
  14. ACTION2           # water 6→7; orange falls to (3,7) following the surface
  15. ACTION4           # tilt right; orange (3,7)→(4,7) (row 7 below platform at row 6 — clear)
  16. ACTION4           # tilt right; orange (4,7)→(5,7)
  17. ACTION4           # tilt right; orange (5,7)→(6,7)
  18. ACTION4           # tilt right; orange (6,7)→(7,7)
  19. ACTION4           # tilt right; orange (7,7)→(8,7)
  20. ACTION1           # water 7→6; orange re-projects to (8,6) (col 8 clear past platform)
  21. ACTION1           # water 6→5; orange re-projects to (8,5) — orange at its target
  ```
  L3 win predicate fires after action 21 (orange at (8,5) = orange
  target; green at (3,5) = green target; both colour-matched).
  *(`*` denotes ACTION6 with click coords that fall on a ball; click
  coords in display pixels are `(grid_col*5 + 2, grid_row*5 + 2)` —
  the centre of the cell. So `ACTION6@(3,9)*` translates to the
  display click `(3*5+2, 9*5+2) = (17, 47)`.)*

  Mechanic exercise check:
  - **M1 used:** ACTION1 in steps ②–⑤ (raise) and ⑳–㉑ (raise);
    ACTION2 in steps ⑬–⑭ (lower). BOTH directions exercised.
  - **M2 used:** ACTION3 in steps ⑥–⑩ (tilt-left); ACTION4 in steps
    ⑮–⑲ (tilt-right). BOTH directions exercised.
  - **M3 used:** the platform at row 6 cols 4–6 forces the orange
    ball's detour (steps ⑬–⑭ lower water so orange falls to row 7,
    BELOW the platform row, before tilting right; without the
    platform, orange could simply tilt right at row 5 directly).
  - **M4 used:** anchor in step ① (orange anchored at start so the
    raise in ②–⑤ doesn't lift it), step ⑪ (green anchored at its
    target so subsequent water lowering doesn't move it back), and
    step ⑫ (unanchor orange so the second-half witness can move it).
- **Difficulty justification.**
  - *Random-resistance.* The witness depends on the ORDER of anchor
    operations — anchoring the wrong ball at the wrong time leaves no
    feasible continuation. A 21-action witness with an anchored-state
    branch makes random-policy success ≪ 1/10000 over the 45-step
    budget.
  - *Human-tractable.* ~2 minutes for an attentive human once the
    anchor mechanic is understood. The whole-environment time
    (L1+L2+L3 played end-to-end) lands at ~5–6 minutes total — within
    the §3.4 ≤ 6 minutes guidance for our 3-level cap.
  - *Planning depth (strictly deeper than L2).* L3 defeats the greedy
    "raise water + tilt right" strategy that solved L1 — both balls
    cannot be at the same row simultaneously without one obstructing
    the other's tilt path. A monotone-progress strategy that always
    moves both balls up and right fails because the SAME tilt moves
    both balls in the SAME direction (parallel motion); only by
    anchoring one ball (introducing asymmetry into the motion model)
    can the swap be achieved. Order matters: anchoring the wrong ball
    at the wrong tide level produces no feasible solution.

## 5. Action mapping

Action subset: `[1, 2, 3, 4, 6]`. ACTION5 and ACTION7 deliberately
unused — the game's distinctive verbs are tide and tilt, which fit
naturally on cardinal arrows (UP/DOWN raise/lower, LEFT/RIGHT tilt).

| Slot | Verb | Side effect |
|---|---|---|
| ACTION1 | UP — raise water surface by 1 row (towards row 0). | Re-project every un-anchored ball: those whose new floating row would be the new surface row rise upward unless blocked by a platform in the same column at an intermediate row. Decrements step counter. Step counter never goes below 0. |
| ACTION2 | DOWN — lower water surface by 1 row (towards row 11). | Re-project every un-anchored ball: a ball above the new surface falls until it hits the new surface OR a platform in the same column. Decrements step counter. |
| ACTION3 | LEFT — tilt left. | Iterate balls in row order top-to-bottom, then column order left-to-right; each un-anchored ball attempts to move into `(col-1, row)`; succeeds iff in-bounds and no platform-cell and no other ball at that destination. Decrements step counter. |
| ACTION4 | RIGHT — tilt right. | Same as ACTION3 with `(col+1, row)`, iterating right-to-left to avoid collision artefacts. Decrements step counter. |
| ACTION6 | CLICK at `(x, y)` (pixel coords). | Convert via `camera.display_to_grid(int(x), int(y))`. If the resulting cell holds a ball (any colour), toggle that ball's anchor state (swap `InteractionMode.TANGIBLE` between the float and anchored sprite variants). If the cell holds NO ball, no-op (no step consumed). Anchor disabled in L1 (clicks always no-op there). |

## 6. HUD and per-game state

### HUD
Single `RenderableUserDisplay` subclass — `bekzbtmcoz` (StepBar):
- Constructor takes `max_steps: int`.
- `update(remaining: int)` setter called at the top of each `step()`
  via `remaining = max_steps - self._action_count`.
- `render_interface(frame)` paints `frame[0, 2:62]` (the 60-pixel-wide
  top letterbox row): a fraction `remaining / max_steps` of the row
  is palette-12 (orange); the rest is palette-5 (black). Distinct
  from priors' bottom-row HUDs.

### Per-game state (Game class)

| Attribute | Type | Lifecycle |
|---|---|---|
| `self.water_level` | `int` | Initialised in `on_set_level` from `level.get_data("WaterLevel")`. Mutated by ACTION1/2. |
| `self.water_sprite` | `Sprite` | The `wkkqxbjzye` instance for the current level; pixels mutated by `_redraw_water()` after every state change. |
| `self.balls` | `list[tuple[Sprite, Sprite, int, int]]` | One tuple per placed ball: `(float_sprite, anchor_sprite, current_col, current_row)`. The two sprites share the same display cell at any time; only one is `TANGIBLE`. |
| `self.anchored_set` | `set[int]` | Indices into `self.balls` of currently-anchored balls. |
| `self.platforms` | `list[tuple[int, int, int]]` | `(col_start, col_end_inclusive, row)` per platform — used for collision queries. |
| `self.targets` | `list[tuple[int, int, int]]` | `(col, row, colour)` per target ring. |
| `self.max_steps` | `int` | Per-level budget from `level.get_data("StepCounter")`. |
| `self.step_bar` | `bekzbtmcoz` | The HUD widget. |

### Hidden state
`_get_hidden_state()` returns a 4×4 `np.int16` matrix:
```
[[water_level, max_steps - _action_count, num_anchored, 0],
 [ball0_col,   ball0_row,                ball0_anchored, ball0_color],
 [ball1_col,   ball1_row,                ball1_anchored, ball1_color],
 [0, 0, 0, 0]]
```
Captures water surface, remaining steps, and per-ball position +
anchor + colour. The engine's `(frame, hidden_state)` graph hash will
distinguish two configurations that render identically but differ in
anchor state or remaining budget.

### Re-projection rule (canonical implementation reference)

After ACTION1, ACTION2, ACTION3, ACTION4, or ACTION6 with anchor
state change, run `_reproject_balls()`:

```python
for i, (float_s, anchor_s, c, r) in enumerate(self.balls):
    if i in self.anchored_set:
        continue                                  # anchored balls don't move
    new_r = self.water_level                      # default float on surface
    # Look for blocking platform in column c on the path.
    if r > self.water_level:
        # Ball was below new surface; rises buoyantly.
        # Coord system: row 0 = top, row 11 = bottom. The platform that
        # blocks the rise is the one CLOSEST to the ball from below —
        # the largest-row platform in the path range [water_level, r-1].
        P = self._max_platform_row_in_col_in_range(c, self.water_level, r - 1)
        if P is not None:
            new_r = P + 1                          # rest just below platform
    elif r < self.water_level:
        # Ball was above new surface (in air); falls to surface.
        # The platform that blocks the fall is the one CLOSEST to the
        # ball from above — the smallest-row platform in the path range
        # [r+1, water_level].
        P = self._min_platform_row_in_col_in_range(c, r + 1, self.water_level)
        if P is not None:
            new_r = P - 1                          # rest just above platform
    else:
        new_r = r                                  # already at surface

    # Adjust if another ball already at target cell.
    while self._cell_occupied_by_other_ball(c, new_r, exclude=i):
        if r > self.water_level:                   # was rising
            new_r += 1                             # back off downward
        elif r < self.water_level:                 # was falling
            new_r -= 1
        else:
            break                                  # already at surface, can't escape collision
    self.balls[i] = (float_s, anchor_s, c, new_r)
    float_s.set_position(c * 5, new_r * 5)
    anchor_s.set_position(c * 5, new_r * 5)
```

For tilts (ACTION3/ACTION4), iterate balls in order so the leading
ball moves first; each ball checks `(new_c, r)` against grid bounds,
platform-cells in that column row, and other balls' cells before
moving. After all tilts complete, run `_reproject_balls()` to allow
buoyant rise into newly-vacated cells.

## 7. Win condition

Per level, after the action's effects are committed (re-projection
plus collision resolution), evaluate:

```python
def _check_win(self) -> bool:
    for col, row, target_color in self.targets:
        match = False
        for i, (float_s, _, c, r) in enumerate(self.balls):
            if c == col and r == row:
                ball_color = self._color_of_ball(i)
                if ball_color == target_color:
                    match = True
                    break
        if not match:
            return False
    return True
```

If True, call `self.next_level()`. After L3's win, the engine's
`next_level()` last-level branch fires `self.win()` automatically.

The win predicate is colour-strict — an orange ball on a green target
ring does NOT satisfy that target (the sprite-collision must be
colour-matched). This rules out the "any-ball on any-target" trivial
solve.

## 8. Lose condition

Single fail mode: step-counter exhaustion.

```python
if self._action_count >= self.max_steps and not self._check_win():
    self.lose()
```

Evaluated AFTER win-check so a final-action-completes-the-puzzle
case wins instead of losing. No hazards, no chasers, no
instant-fail-on-collision. The kf42 / qz73 priors have the same
single-fail-mode design (step-counter only).

## 9. Novelty note

Closest entries in `mechanic-novelty/taxonomy-of-25-games.md`:

- **`sp80` — pour-shelf-route.** sp80 has water as an
  instantaneously-firing cascade event triggered by ACTION5, with a
  4-pour budget per level; the player's primary verb is to *arrange
  the cascade path* by clicking and sliding shelves. kx14's water is
  a continuous bidirectionally-controlled persistent surface that the
  player raises/lowers each turn; there is no "pour" event and no
  pour-attempt budget. Distinguishing rule: sp80's player builds a
  cascade-path BEFORE a discrete water release; kx14's player IS the
  water by manipulating its surface every turn.
- **`g50t` — walk-vs-scroll.** g50t's playfield change (the leftward
  scroll every other turn) is the antagonist; in kx14 the playfield
  change is the player's verb. Direction of agency reversed.
- **`m0r0` — mirror-orb-merge.** m0r0 has two pawns coupled by mirror
  semantics (UP moves both up; LEFT pulls them apart). kx14's tilt
  acts on every un-anchored ball *uniformly* — no inversion, no
  mirror-coupling. m0r0's win merges two pawns into one cell; kx14's
  win places each ball on its same-coloured target ring.
- **`ar25` — shape-mirror-cover.** ar25 has a fixed mirror line and
  the player nudges shape-or-mirror; kx14 has no mirror at all.
- **`ka59` — sokoban-explode-chase.** ka59's primary verb is
  arrow-slide-with-recursive-push from a clicked active pawn; kx14's
  arrows control the *environment* (water level + tilt impulse), not
  a selected pawn. ka59 has chasers; kx14 has none.

Closest entries in `prior-games/index.md`:

- **`kf42` — tether-pawn-cycle.** Distinguishing rule: kf42 has a
  directly-steered pawn (clicked then moved by arrows within a tether
  constraint); kx14 has NO directly-steered actor. Visual signature
  diverges on palette (kf42 dark walled `{4, 8, 9}` vs kx14
  `{1, 10, 12, 14}` air-water cross-section), sprite grain (kf42
  1-cell pawns vs kx14 5×5 internally-patterned balls + 15×5
  platforms), and core dynamic (steer-an-actor vs manipulate-the-
  carrier). The kf42→vh68 cautionary tale (small coloured pawns on
  dark walled grid) is explicitly avoided.
- **`qz73` — radial-cycle-lock.** Distinguishing rule: qz73's lock
  pins individual tips against an ACTION5 ring rotation (tip is a
  participant in a global rotation; lock removes it from
  participation). kx14's anchor pins balls against BOTH tide AND
  tilt; additionally, an anchored ball that is exposed by the
  receding tide stays in *air* (the tide receded past it, leaving it
  on a dry cell) — an outcome qz73's lock has no analogue for.
  Topology (radial dial vs vertical tank cross-section) and visual
  signature differ entirely.

The candidate has been re-walked through `mechanic-novelty/negative-
similarity-check.md` against both priors and the four closest
25-game entries; no prior shares ≥ 3 of the eight named dimensions
(see `mechanic-pick.md` for the matrix).

`prior-games/index.md` is NOT empty (two priors) — both have been
addressed above.
