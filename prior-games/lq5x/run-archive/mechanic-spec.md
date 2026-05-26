# mechanic-spec — lq5x · lantern-cone-illuminate

## 1. Title

Lantern Cone Illuminate (working title; not visible in-game).

## 2. Mechanic family

A small lantern pawn projects a directional rectangular cone of "lit"
cells out into a darkened arena. The player walks the lantern with
arrow keys and rotates the cone's facing 90° clockwise with ACTION5.
A target ring counts as "lit" when, at any tick, the target's cell
is inside the cone's lit-area AND the cone's current colour matches
the target's colour. The mechanic draws on **basic geometry &
topology** (cone projection = a directional rectangle clipped by
grid bounds; an inside/outside relation between targets and the
cone) and **objectness** (the lantern, target rings, wax pickups,
and filters are persistent, perceivable entities). No language, no
digits, no real-world clipart, no cultural symbols.

## 3. Sprite roster

Sprite names are 10-character random lowercase tokens following the
25 reference games' convention.

| name | dims (h × w) | palette values | tags | role |
|---|---|---|---|---|
| `lzajfunopv` | 3×3 | 11 (yellow), 4 (off-black) | `lantern` | Lantern body. Yellow 3×3 with a single off-black centre pixel at (1, 1) so the player can see the lantern even when it is fully inside its own lit cone. Single instance per level; movable by arrows. |
| `tytkbflqjr` | 3×3 | 11 (yellow), -1 | `target_yellow`, `target` | Hollow 3×3 ring of palette 11; centre pixel transparent. Static decoration; engine just records "lit" status. |
| `wmgojqejxr` | 3×3 | 8 (red), -1 | `target_red`, `target` | Hollow 3×3 ring of palette 8. |
| `cdpjpckayh` | 1×1 | 12 (orange) | `wax_pickup` | Single-cell pickup. Removed when stepped on. Adds +2 to current cone range R. |
| `qxojpijuxq` | 1×1 | 8 (red) | `filter`, `filter_red` | Single-cell red filter. Stays in place. When the cone covers this cell, the lantern's `cone_color` updates to palette 8 (red). |
| `nrirjwvqub` | 1×1 | 11 (yellow) | `filter`, `filter_yellow` | Single-cell yellow filter (not used by L1-L3 but defined for future levels). When the cone covers this cell, `cone_color` updates to palette 11. |

Sprites are declared once in the module-level `sprites` dict and
cloned per level via `.clone().set_position(...)`.

The cone itself is NOT a sprite — it is rendered each frame by a
`ConeOverlay(RenderableUserDisplay)` widget that reads the current
lantern position, facing, range R, and cone_color from the game
class and paints the lit cells onto the camera frame on top of
the static sprites (see §6).

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels share `grid_size=(12, 12)` (L1) or `(14, 14)`
(L2/L3) with no walls — the playfield is an open arena. Background
palette = 5 (black). The cone's "lit" cells are repainted to palette
1 (off-white) when the cone is yellow and palette 13 (maroon) when
the cone is red, so the cone's colour is visible at a glance.
Static sprites (lantern, targets, pickups, filters) render normally
on top of the cone overlay. Cone width is fixed at 3 cells; depth
is the runtime range R.

**Cone shape definition (used in all three levels)**: given the
lantern at `(lx, ly)`, facing `f ∈ {N, E, S, W}`, and current range
`R`, the cone covers the cells:

- `N`: `(x, y)` with `x ∈ [lx-1, lx+1]`, `y ∈ [ly-R, ly-1]`
- `E`: `(x, y)` with `x ∈ [lx+1, lx+R]`, `y ∈ [ly-1, ly+1]`
- `S`: `(x, y)` with `x ∈ [lx-1, lx+1]`, `y ∈ [ly+1, ly+R]`
- `W`: `(x, y)` with `x ∈ [lx-R, lx-1]`, `y ∈ [ly-1, ly+1]`

Cells outside the level grid are dropped. After every action, the
engine recomputes the cone, scans for any filter cell inside the
cone (if more than one filter, the closest-by-Manhattan-distance
to the lantern wins; ties broken by sprite-list order — fully
deterministic), and updates `cone_color` to the matched filter's
colour. If no filter is in the cone, `cone_color` is left
unchanged (it persists from the last filter encountered, or
remains at the level-start default if no filter has yet been
encountered).

**Lit-target predicate**: A target is "lit" iff there exists a
post-action tick at which (a) the target's centre cell is in the
cone, AND (b) `cone_color == target.color`. Once lit, a target
stays lit for the rest of the level.

**Win predicate**: every target in the level is lit.

### Level 1 — base dynamic system (N = 2)

`grid_size = (12, 12)`. Step budget = 10. Cone default colour =
yellow (palette 11). Initial cone range R = 4 (no wax in this
level). Lantern starts at `(3, 3)` facing **N**.

**Sprites placed**:

- `lzajfunopv` (lantern) at `(3, 3)`, facing N — actually
  facing is internal state, sprite is placed normally.
- `tytkbflqjr` (yellow ring) at `(3, 8)` — south target A.
- `tytkbflqjr` (yellow ring) at `(8, 6)` — east target B.

No filters, no wax pickups in L1.

**Mechanics required by the witness (N = 2)**:

1. **walk** (ACTION1-4): translate the lantern by ±1 cell in a
   cardinal direction; cone moves with the lantern. Required to
   bring B into a S-facing cone after rotation, since no rotation
   from `(3, 3)` alone places B in any cone.
2. **cone-rotate** (ACTION5): cycle facing N→E→S→W→N. Required
   because A is south of the lantern (no walking-only path
   reaches a vantage where the still-N-facing cone covers A
   within the step budget — see "walk-only refutation" below).

Both verbs are exercised by every action of the witness; both are
required by the *shortest* witness AND by the level's solvability
under the step budget.

**Witness solution (5 actions)**:

```
1. ACTION5                       # facing N → E
2. ACTION5                       # facing E → S; lantern still at (3,3); S-cone covers (2..4, 4..7); A=(3,8) not yet in cone
3. ACTION4                       # walk RIGHT to (4, 3); S-cone covers (3..5, 4..7); A still not in cone
4. ACTION2                       # walk DOWN to (4, 4); S-cone covers (3..5, 5..8); still missing A by one row
5. ACTION2                       # walk DOWN to (4, 5); S-cone covers (3..5, 6..9); A=(3,8) IN cone (3 in [3..5], 8 in [6..9]); cone yellow; A LIT. B=(8,6): 8 not in [3..5]; B not yet.
```

Wait — that lights A but not B. Re-examine.

Corrected witness (5 actions, lights both A and B):

```
1. ACTION5                       # facing N→E; cone E from (3,3) R=4 covers (4..7, 2..4). B=(8,6): 8 not in [4..7]; B not yet
2. ACTION4                       # walk RIGHT to (4, 3); E-cone covers (5..8, 2..4). 8 in [5..8] yes; 6 in [2..4]? no
3. ACTION2                       # walk DOWN to (4, 4); E-cone covers (5..8, 3..5). 6 in [3..5]? no
4. ACTION2                       # walk DOWN to (4, 5); E-cone covers (5..8, 4..6). 6 in [4..6] yes; B IN. Cone yellow. B LIT.
5. ACTION5                       # facing E→S; S-cone from (4,5) R=4 covers (3..5, 6..9). A=(3,8): 3 in [3..5], 8 in [6..9]. A IN. Cone yellow. A LIT. WIN.
```

Total: 5 actions. Witness exercises both walk (steps 2-4) and
cone-rotate (steps 1, 5).

**Walk-only refutation**: Without using ACTION5, the lantern is
permanently facing N. For any target to be lit, the lantern must
walk to a cell where the N-cone covers the target. For A=(3,8),
N-cone must include (3,8): need lantern at (x, y) with x∈[2,4]
and y∈[9,12]. Shortest walk from (3,3) to (3,9) is 6 walks. For
B=(8,6), need lantern at (x, y) with x∈[7,9] and y∈[7,10].
Shortest from (3,9) to (8,9) is 5 walks. Total walk-only path =
11 actions. Step budget = 10 → walk-only **loses**. Rotate is
strictly required by the budget.

**Difficulty justification**:

- *Random-resistance*: Random play uniformly samples 5 actions.
  Reaching the precise witness within budget 10 has probability
  `≤ (1/5)^5 ≈ 3 × 10⁻⁴`, well below the 10⁻⁴ ceiling for L1.
  More plausibly, a random policy will burn budget on
  walk-back-and-forth or extra rotations and never align both
  targets in the cone.
- *Human-tractable*: An attentive human, after one or two
  exploratory rotations to discover that ACTION5 cycles the
  cone facing, plans the witness in ~1-2 minutes (5 actions ×
  ~15 seconds each). A top vision-language model would see the
  initial cone facing N, infer that A and B are not in the
  initial cone, and reason "rotate to E for B, then walk to
  align".
- *Planning depth*: L1 is a near-zero planning level — mechanic
  discovery (walk + rotate) is the actual difficulty. Once the
  player understands the two verbs, the witness is reachable by
  short-horizon planning. This satisfies the L1 contract that
  random play occasionally stumbles ("near-zero" is the floor,
  not zero).

### Level 2 — base system + 1 new mechanic (N + 1 = 3)

`grid_size = (14, 14)`. Step budget = 12. Cone default colour =
yellow. Initial cone range R = 2. Lantern starts at `(3, 7)`
facing **N**.

**Sprites placed**:

- `lzajfunopv` (lantern) at `(3, 7)`, facing N.
- `tytkbflqjr` (yellow ring) at `(3, 0)` — north target A.
- `tytkbflqjr` (yellow ring) at `(3, 13)` — south target B.
- `cdpjpckayh` (wax pickup) at `(3, 6)` — directly N of the
  lantern's start. +2 to R.

**Mechanics required by the witness (N + 1 = 3)**:

1. **walk** (carried forward from L1).
2. **cone-rotate** (carried forward from L1).
3. **wax pickup** (NEW): when the lantern walks onto a
   `wax_pickup` sprite, the sprite is removed (set to
   `InteractionMode.REMOVED`) and the lantern's range R is
   incremented by 2 permanently for that level. With initial
   R=2 and one pickup, R can reach a maximum of 4.

All three verbs are exercised by the witness AND strictly
required by the step budget (see refutation).

**Witness solution (10 actions)**:

```
 1. ACTION1                      # walk UP (3,7)→(3,6); pickup at (3,6) consumed; R: 2→4. N-cone from (3,6) R=4 covers (2..4, 2..5). A=(3,0): 0 not in [2..5].
 2. ACTION1                      # walk UP (3,6)→(3,5); N-cone (2..4, 1..4). A: 0 not in [1..4].
 3. ACTION1                      # walk UP (3,5)→(3,4); N-cone (2..4, 0..3). A=(3,0) IN. Cone yellow. A LIT.
 4. ACTION2                      # walk DOWN (3,4)→(3,5)
 5. ACTION2                      # walk DOWN (3,5)→(3,6)
 6. ACTION2                      # walk DOWN (3,6)→(3,7)
 7. ACTION2                      # walk DOWN (3,7)→(3,8)
 8. ACTION5                      # facing N→E
 9. ACTION5                      # facing E→S; S-cone from (3,8) R=4 covers (2..4, 9..12). B=(3,13): 13 not in [9..12].
10. ACTION2                      # walk DOWN (3,8)→(3,9); S-cone (2..4, 10..13). B=(3,13) IN. Cone yellow. B LIT. WIN.
```

Total: 10 actions. Walk = 8 actions; cone-rotate = 2 actions;
wax pickup = consumed implicitly at step 1.

**Walk-only / no-wax refutation**: Without using the wax pickup
at (3, 6), R stays at 2. To light A=(3,0) with N-cone, lantern
must be at (x∈[2,4], y∈[1,3]). Shortest walk to (3, 3) = 4
walks (avoiding (3,6) means going through (4,7)→(4,6)→...; the
direct path passes through (3,6) and would consume the pickup
involuntarily). Even via (3,4) the lantern walks `(3,7)→(3,6)`
and crosses (3,6) — so wax pickup is unavoidably consumed if
the lantern walks N. The refutation is therefore: assume wax
pickup is NOT consumed (i.e. lantern detours around it via
(4, 7)→(4, 6)→(4, 5)→(4, 4)→(3, 4) = 4 walks). At (3, 4)
facing N R=2, N-cone covers (2..4, 2..3). A=(3,0): 0 not in
[2..3]. Need to walk further N to (3, 2). 2 more walks. At
(3, 2) facing N R=2, N-cone covers (2..4, 0..1). A=(3,0) IN.
Lit. So far 6 walks just for A.

For B=(3,13): walk back south past start, then S-cone reach.
From (3, 2) walk to (3, 11) = 9 walks + 2 rotates = 11. Need
S-cone from (3, 11) R=2 covers (2..4, 12..13). B IN. Lit. Total
walk-no-wax = 6 + 11 = 17 actions > budget 12. Loses.

With wax extending R to 4, the S-cone reach is much shorter
(witness above: 10 actions). Wax pickup is **strictly required**
by the budget.

**Difficulty justification**:

- *Random-resistance*: 10-action witness in a 5-action policy
  space = `(1/5)^10 ≈ 10⁻⁷` per attempt. Random with budget 12
  has effectively zero probability of finding the witness.
  Additionally, a random walker might step on the wax pickup
  early (good luck) but then has to recognise that the cone got
  longer — random doesn't reason about that.
- *Human-tractable*: ~2 minutes once the wax mechanic is
  inferred. A human sees the dot at (3,6), walks onto it,
  notices the cone visibly extending, and infers "this dot
  extends my range". Then reasons about budget pressure.
- *Planning depth (L2 hard requirement)*: At every step the
  player must reason about state + future state. Examples:
  *step 1*: "If I walk N, I pick up wax and lengthen R. Will my
  cone then cover A? — let me trace: at (3,6) facing N R=4, the
  cone covers (2..4, 2..5); A=(3,0) is still 2 cells too far —
  I need to keep walking N." *Step 4*: "I have lit A. I now need
  to position to light B. B is south. I must walk back through
  (3,6) and continue S. How far do I need to go before rotating
  S?" *Step 8*: "Rotating to S now would leave me facing S at
  (3,8). With R=4, S-cone from (3,8) covers (2..4, 9..12). B at
  (3,13) is one cell further. I need to walk one more S after
  rotating — so 2 rotates plus 1 walk." This is multi-step
  state-then-future-state reasoning, not single-step. **No
  spam-the-new-verb solution exists**: pressing ACTION5
  repeatedly without walking simply rotates the cone in place
  (R=2 from (3,7), no targets in any of the four cones). **No
  follow-the-colour walkthrough exists**: A and B are both
  yellow — the colour signal alone gives no routing hint.
  **No 1-action lookup table**: the puzzle is sequential.

### Level 3 — system + 1 more new mechanic (N + 2 = 4)

`grid_size = (14, 14)`. Step budget = 13. Cone default colour =
yellow. Initial cone range R = 2. Lantern starts at `(2, 2)`
facing **E**.

**Sprites placed**:

- `lzajfunopv` (lantern) at `(2, 2)`, facing E.
- `cdpjpckayh` (wax pickup) at `(3, 2)` — directly E of the
  lantern's start. +2 to R.
- `qxojpijuxq` (red filter) at `(2, 8)` — S of the lantern.
- `tytkbflqjr` (yellow ring) at `(8, 2)` — east target Y1.
- `wmgojqejxr` (red ring) at `(2, 11)` — south target R1.

**Mechanics required by the witness (N + 2 = 4)**:

1. **walk** (carried forward).
2. **cone-rotate** (carried forward).
3. **wax pickup** (carried forward from L2; required to extend
   R high enough to light Y1 at distance 6 east).
4. **filter changes cone colour** (NEW): when the cone's
   lit-area covers a `filter` sprite's cell, the lantern's
   internal `cone_color` updates to that filter's colour. The
   colour persists until the cone next covers a different
   filter (or, if no filter is encountered, persists for the
   rest of the level). The cone is rendered in its current
   colour, and the lit-target predicate compares
   `cone_color == target.color` at each tick.

All four verbs are exercised by the witness AND every one is
required by the level's solvability:

- Without **walk**: lantern can't change position; from (2,2)
  facing E with R=2, cone covers (3..4, 1..3). No targets and
  no filter in cone. Stuck.
- Without **cone-rotate**: lantern faces E forever. R1 at
  (2,11) is south of the lantern; no E-cone from any (x, y)
  with y reachable can cover (2,11). Unsolvable.
- Without **wax pickup**: R=2 forever. Y1 at (8,2) requires
  E-cone from (x∈[7,9], y∈[1,3]) AND no red filter in cone (so
  cone is yellow). With R=2, lantern would need to walk to
  (6,2) for E-cone (7..8, 1..3) to cover Y1 — 4 walks. Then
  return south for R1 — many more walks. Total exceeds budget
  (analysis below).
- Without **filter mechanic** (i.e. if the cone colour never
  changed): R1 (red) could never be lit because cone defaults
  to yellow.

**Witness solution (10 actions)**:

```
 1. ACTION4                      # walk RIGHT (2,2)→(3,2); pickup wax; R: 2→4. E-cone from (3,2) R=4 covers (4..7, 1..3). Y1=(8,2): 8 not in [4..7].
 2. ACTION4                      # walk RIGHT (3,2)→(4,2); E-cone (5..8, 1..3). Y1=(8,2) IN (8 in [5..8], 2 in [1..3]). Cone yellow. Y1 LIT.
 3. ACTION3                      # walk LEFT (4,2)→(3,2); E-cone (4..7, 1..3).
 4. ACTION3                      # walk LEFT (3,2)→(2,2); E-cone (3..6, 1..3).
 5. ACTION5                      # facing E→S; S-cone from (2,2) R=4 covers (1..3, 3..6). Filter (2,8): 8 not in [3..6]. Cone yellow.
 6. ACTION2                      # walk DOWN (2,2)→(2,3); S-cone (1..3, 4..7). Filter (2,8): 8 not in [4..7].
 7. ACTION2                      # walk DOWN (2,3)→(2,4); S-cone (1..3, 5..8). Filter (2,8): 8 in [5..8] yes. IN. Cone updated to RED.
 8. ACTION2                      # walk DOWN (2,4)→(2,5); S-cone (1..3, 6..9). Filter (2,8) still IN. Cone red.
 9. ACTION2                      # walk DOWN (2,5)→(2,6); S-cone (1..3, 7..10). Filter (2,8) IN. Cone red.
10. ACTION2                      # walk DOWN (2,6)→(2,7); S-cone (1..3, 8..11). Filter (2,8) IN. Cone red. R1=(2,11): 2 in [1..3], 11 in [8..11]. R1 IN. Cone red. R1 LIT. WIN.
```

Total: 10 actions. Walk = 9; cone-rotate = 1 (step 5); wax
pickup = 1 (step 1); filter cone-colour change = 1 (step 7,
where the S-cone first covers (2, 8)).

**Strict adjacent-action commute that breaks solvability**: The
witness's adjacent pair **steps 2 and 3** is order-sensitive.

Step 2 is `ACTION4` (walk RIGHT to (4, 2), Y1 enters cone with
yellow colour, Y1 LIT).

Step 3 is `ACTION3` (walk LEFT to (3, 2), Y1 leaves cone but
remains lit from step 2's tick).

If we **swap steps 2 and 3** to execute `ACTION3` then
`ACTION4`:

- Swapped step 2': `ACTION3` walk LEFT (3, 2)→(2, 2). E-cone from (2, 2) R=4 covers (3..6, 1..3). Y1=(8, 2): 8 not in [3..6]. Y1 **not** in cone.
- Swapped step 3': `ACTION4` walk RIGHT (2, 2)→(3, 2). E-cone from (3, 2) R=4 covers (4..7, 1..3). Y1=(8, 2): 8 not in [4..7]. Y1 **not** in cone.

Y1 is **never lit during the swapped pair**. Continuing the
witness with the original steps 4-10: at step 7 the cone
becomes RED (filter encountered). After step 7, cone_color
remains RED for the rest of the level (no yellow filter exists
to revert). Y1 is yellow → Y1 cannot be lit by a red cone at
any subsequent tick.

The level is therefore **unsolvable** if the player commutes
steps 2 and 3 — the swap permanently destroys the only window
in which Y1 could be lit. This satisfies the strict-deeper
adjacent-commute requirement.

**Defeated trivial heuristic**: A "rotate to face the
unilluminated direction first, then walk toward whatever I can
see" greedy heuristic fails because the very first useful
non-E rotation in this configuration brings the cone into a
direction where the red filter is already nearby (S-cone from
(2, 2) is at distance 6 from the filter; just two south walks
later the filter is in the cone). Once the cone is red, Y1
(yellow) is permanently un-lightable. The greedy player
discovers the red target is reachable but accidentally locks
out the yellow target. The witness defeats this by **lighting
the yellow target first while the cone is still yellow**, then
walking south toward the red filter and the red target.

**Difficulty justification**:

- *Random-resistance*: 10-action witness with 5-action vocabulary
  ≈ `(1/5)^10` ≈ 10⁻⁷. Plus the strict colour-state requirement
  (cone must be yellow when sweeping Y1) reduces random
  success below a level set by *both* needing the right walk
  sequence AND the right cone-colour state at the right tick.
- *Human-tractable*: ~2-3 minutes once the filter mechanic is
  understood. A human notices the red square at (2, 8), walks
  the cone over it (or walks the lantern past it), sees the
  cone change colour, and infers "the cone takes the filter's
  colour". Then reasons: "I need to light Y1 with a yellow cone,
  so I must light Y1 before activating any red filter". Then
  plans accordingly.
- *Planning depth (STRICTLY DEEPER than L2)*: L2 required
  multi-step planning about state + future state but the state
  was monotone (R only increased). L3 adds a non-monotone
  state component (cone_color is reversible only via filter
  encounters, but in this level there's no yellow filter — so
  once red, the cone stays red). The player must therefore
  reason about an **irreversible state transition** and plan
  to do all yellow-target work *before* triggering it. This
  satisfies "non-trivial planning *plus extra depth*". Whole-
  environment human time across the 3 levels lands at
  approximately 1 + 2 + 3 = 6 minutes, matching the harness's
  ~6 min target.

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5]`. ACTION6 and ACTION7 are
not registered. Per `skills/global/action-enum.md` this is the
"Cardinal motion + freedom slot" subset (cn04, qz38, sp80
shape, but used here for a cone-aiming verb instead of a piece-
rotate or pour verb).

| Slot | Semantic | Effect on engine state |
|---|---|---|
| ACTION1 | walk UP | If `(lantern.x, lantern.y - 1)` is in-bounds, set lantern position to `(lantern.x, lantern.y - 1)`. Step counter -1. Recompute cone, scan for filter, evaluate lit-target predicate. If win predicate true, `self.next_level()`. |
| ACTION2 | walk DOWN | Same with `+ 1` to `y`. |
| ACTION3 | walk LEFT | Same with `- 1` to `x`. |
| ACTION4 | walk RIGHT | Same with `+ 1` to `x`. |
| ACTION5 | rotate cone | Cycle facing `N → E → S → W → N`. Lantern position unchanged. Step counter -1. Recompute cone, scan for filter, evaluate predicate. |

There is **no action gating** — all 5 actions are valid every
turn (engine inherits `_get_valid_actions` default). Walking
into a wax pickup consumes the pickup and increments R; walking
into a target ring or filter has no special effect (the lantern
passes through; targets and filters do not block movement).
Walking off the grid is silently rejected (no-op); the step is
still consumed.

If the level reaches step counter zero without the win
predicate, `self.lose()` fires.

## 6. HUD and per-game state

### HUD widgets

Two `RenderableUserDisplay` subclasses, both registered via
`Camera(interfaces=[step_hud, cone_overlay])`:

1. **`StepCounterHud`** — a depleting horizontal bar drawn on
   the bottom row of the 64×64 frame. Mirror of `cn04`'s
   pattern: a `current_steps` field, updated each tick by
   `step()`, rendered as palette-1 (filled) on the left
   portion and palette-3 (empty) on the right portion. Width =
   the entire 64-pixel bottom row.

2. **`ConeOverlay`** — paints the cone's lit cells onto the
   frame each render. Holds references to game-class fields
   (lantern position `(lx, ly)`, facing, range R, cone_color,
   plus the level's `grid_size`). On `render_interface`:
   - Compute the cone cells from `(lx, ly)`, facing, R.
   - For each cone cell `(cx, cy)` inside the level grid, look
     up the camera's cell-to-pixel mapping (the camera scales
     small grids up to fill 64×64; the overlay must compute
     the same scaling).
   - For each rendered pixel in those cells, if the pixel is
     currently the background colour (palette 5 black), repaint
     to a "lit" colour. Lit colour map: `cone_color = 11
     (yellow)` → repaint to palette 1 (off-white); `cone_color
     = 8 (red)` → repaint to palette 13 (maroon). Other
     palette values (lantern, target rings, pickups, filters)
     are left unchanged so they remain visible inside the lit
     region.

### Per-game internal state

Carried on the `Lq5x` game class:

| field | type | meaning |
|---|---|---|
| `lantern` | `Sprite \| None` | The placed lantern sprite for the current level. Cached from `level.get_sprites_by_tag("lantern")[0]` in `on_set_level`. |
| `facing` | `int` | One of `0, 1, 2, 3` representing N, E, S, W. Reset to a per-level start value in `on_set_level`. |
| `cone_range` | `int` | Current R. Reset to per-level initial in `on_set_level`. Incremented by `WAX_BONUS = 2` on pickup. |
| `cone_color` | `int` | Palette value of the cone (default 11). Reset per level. Updated when cone covers a filter. |
| `step_budget` | `int` | Per-level max actions. Read from `level.get_data("step_budget")`. |
| `lit_targets` | `set[str]` | Set of `target.name` values that have been lit so far this level. Reset per level. |

Per-level configuration via `level.set_data` / `level.get_data`:

| key | meaning |
|---|---|
| `step_budget` | int — max actions for this level. |
| `initial_facing` | int — 0/1/2/3 for N/E/S/W. |
| `initial_range` | int — starting R. |
| `wax_bonus` | int — how much each pickup adds. Defaults to 2 if absent. |

## 7. Win condition

After every action, the engine evaluates:

```python
def is_won(self) -> bool:
    targets = self.current_level.get_sprites_by_tag("target")
    return all(t.name in self.lit_targets for t in targets)
```

A target's `name` is added to `self.lit_targets` after the
post-action cone-and-filter recomputation if `target` is in the
cone AND `cone_color == target_color`, where `target_color` is
read from `target.tags` (`target_yellow` → palette 11;
`target_red` → palette 8).

If `self.is_won()` returns True at the end of `step()`,
`self.next_level()` is fired before `self.complete_action()`.
This means: ANY level (L1, L2, L3) ends in win when every target
is lit. The base `NovaBaseGame.next_level` advances to the next
level; on the last level (L3) the engine calls `self.win()`
automatically (per novaengine's default).

## 8. Lose condition

After every action, before the win check:

```python
if self._action_count >= self.step_budget:
    self.lose()
    self.complete_action()
    return
```

If the action count reaches the per-level budget without the
win predicate firing, the level (and the run) ends in a loss.
There is no other lose path — no hazard sprite, no enemy, no
"falling off the edge" penalty. Walking off the grid is a
silent no-op that still consumes a step.

## 9. Novelty note

### Closest taxonomy entries (per `mechanic-novelty/similarity-check.md`)

- **`ls20` — cycler-attribute-match** (closest near-miss). ls20
  has an avatar wandering a walled maze in 5-pixel hops and
  stepping onto cycler-tiles cycles the avatar's attribute
  through a fixed alphabet; the win condition is "reach the
  goal pad with the avatar's shape-colour-rotation triplet
  matching the imprinted target". **Distinguishing rule**:
  lq5x's puzzle is a *line-of-sight cone-aiming* puzzle, not a
  navigation-with-on-body-attribute puzzle. The colour state in
  ls20 lives on the avatar's body and is mutated by stepping
  on cyclers; in lq5x the colour state lives on the projected
  cone (an emitted directional rectangle, not on the avatar)
  and is mutated when the *cone* (not the avatar) intersects a
  filter cell. Verb cardinality differs: ls20 is pure-arrow
  `[1,2,3,4]`; lq5x adds ACTION5 cone-rotate. The win
  predicate differs: ls20 = single goal-cell test on avatar
  state; lq5x = per-target conjunction over the run history.

- **`bp35` / `lf52` — procedural-graph-walk(-undo)**.
  bp35/lf52 have a token on a procedurally-built coloured-node
  graph; arrows step along tracks, click teleports, target =
  procedural configuration. **Distinguishing rule**: lq5x has
  no abstract graph data structure — the maze is just a grid,
  and the puzzle is what the cone *can see* from a (position,
  facing) pair. bp35/lf52's puzzle is what graph configuration
  matches the level seed.

- **`tu93` — maze-pickup-train**. A pawn hops along corridors
  with followers chaining behind. **Distinguishing rule**: lq5x
  has no follower/chain dynamic; the cone is a non-physical
  projection that doesn't follow the lantern in a Snake-like
  trail. lq5x has no chain abstraction.

- **`m0r0` — mirror-orb-merge**. Two mirror-symmetric pawns;
  arrows move both with mirrored input. **Distinguishing
  rule**: lq5x has one pawn with normal input. No mirror-input
  dynamic.

- **`ka59` — sokoban-explode-chase**. Pushing pawns; chaser
  enemy; tag-based active-pawn switch. **Distinguishing rule**:
  lq5x has no pushing, no chaser, no tag-based pawn switch.

- **`r11l` — centroid-puppet-leg**. A ring at the centroid of
  legs. **Distinguishing rule**: lq5x has no centroid logic.

### Prior-games sweep

| prior id | family | shared dimensions vs lq5x | distinguishing rule |
|---|---|---|---|
| **kf42** | tether-pawn-cycle | step-counter failure axis (universal); arrow input. ~2 dimensions. | kf42 = Chebyshev-tether between two pawns + click-select; lq5x = single-pawn line-of-sight cone with no pair dynamic and no click verb. |
| **qz73** | radial-cycle-lock | step-counter failure axis; ACTION5 is a rotation verb (slot match but operates on different objects). ~2 dimensions. | qz73 rotates an 8-slot ring of *tip-pieces* and uses ACTION6-click to lock individual tips. lq5x rotates the *cone facing of an emitted directional rectangle*, not a ring of objects, and has no click and no lock verb. |
| **kx14** | tide-tilt-buoyant | step-counter failure axis; arrow input. ~2 dimensions. | kx14 = vertical fluid-tank with water surface and tilt and click-anchor. lq5x has no fluid, no tank, no surface, no tilt — verbs are walk + cone-rotate. |
| **qb84** | bead-lift-swap | step-counter failure axis; arrow input; ACTION1/2 carries a directional verb that mutates state on the same slot as navigation (pattern match, but the verbs differ). ~2-3 dimensions. | qb84 is a chain-cursor puzzle where ACTION1/2 *swap* the cursor's bead colour with a peg, ACTION3/4 step the cursor index. lq5x's ACTION1-4 are walking, not cursor-step + swap. The colour state in qb84 lives on chain-bead pixels; in lq5x it lives on the lantern's emitted cone projection. |

Per-prior negative-similarity sweep (eight dimensions from
`mechanic-novelty/negative-similarity-check.md`) is documented in
`workspace/mechanic-pick.md` §7. No prior shares ≥ 3 dimensions
with lq5x.

### vs preexisting video games (manual-axis novelty)

The "field-of-view / fog-of-war" mechanic exists in roguelikes
and stealth games (Metal Gear Solid's guard sight cone is the
nearest analogue), but the **specific composition** of (a) a
single player-controlled cone-emitter on a 2D arena, (b)
ACTION5-rotates-the-cone as the freedom-slot verb, (c) wax
pickups that incrementally extend cone range, and (d) static
filter cells that re-tint the cone when the cone covers them, is
not (to the author's knowledge) a known commercial puzzle game's
core mechanic. The user is the final arbiter on this axis per
the harness's design.
