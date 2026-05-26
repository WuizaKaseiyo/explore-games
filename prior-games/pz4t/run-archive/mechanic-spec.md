# pz4t — mechanic spec

## 1. Title

Anchor-Pivot Jigsaw (working title; not visible in-game).

## 2. Mechanic family

**`anchor-pivot-place`**. Two-phase click verb: clicking a component
in the palette picks it up AND records the clicked-pixel as the
anchor; clicking a cell on the board places the held component such
that the anchor cell lands on the clicked cell. Drawn from §3.4
priors **objectness** (components and targets as persistent named
sprites) and **basic geometry** (placement is a 2D translation by
`click − anchor`; rotation is a 90° group action; flip is a
reflection).

## 3. Sprite roster

| Name | Dimensions | Palette values | Tags | Role |
|---|---|---|---|---|
| `comp_red_bar3` | 3 × 1 | 8 | `["component", "red", "sys_click"]` | Red 3-cell horizontal bar (L1 + L2 component). |
| `comp_yellow_bar2` | 1 × 2 | 11 | `["component", "yellow", "sys_click"]` | Yellow 2-cell vertical bar (L1 component). |
| `comp_red_vbar3` | 1 × 3 | 8 | `["component", "red", "sys_click"]` | Red 3-cell vertical bar (L2 starting orientation). |
| `comp_yellow_L` | 2 × 2 (L-tromino) | 11 + -1 | `["component", "yellow", "sys_click"]` | Yellow L-tromino (3 cells). |
| `comp_green_bar2` | 2 × 1 | 14 | `["component", "green", "sys_click"]` | Green 2-cell horizontal bar. |
| `comp_red_Z` | 3 × 2 (Z-tetromino) | 8 + -1 | `["component", "red", "sys_click"]` | Red Z-tetromino (4 cells; chiral). |
| `comp_yellow_S` | 3 × 2 (S-tetromino) | 11 + -1 | `["component", "yellow", "sys_click"]` | Yellow S-tetromino. |
| `comp_green_T` | 3 × 2 (T-tetromino) | 14 + -1 | `["component", "green", "sys_click"]` | Green T-tetromino. |
| `comp_magenta_bar2` | 2 × 1 | 6 | `["component", "magenta", "sys_click"]` | Magenta 2-cell horizontal bar. |
| `target_shadow` | 1 × 1 | 3 | `["target", "shadow"]` | Mid-grey-darker shadow cell — placed at every cell of every target outline (one sprite per target cell). |
| `anchor_marker` | 1 × 1 | 1 | `["anchor"]` | Off-white 1×1 marker showing the anchor pixel of the held component (visible only while a component is held). |

Background palette = 2 (light-grey). Letterbox = 4 (off-black).
Visible palette set across L1-L3: {1, 2, 3, 4, 6, 8, 11, 14} +
`-1` transparency. 8 distinct visible values.

## 4. Level progression, mechanic enumeration, and witness solutions

### Level 1 — base dynamic (10×10 grid)

**Mechanics required (N = 1):**
1. **Anchor-pivot place**: click pixel on component → records
   anchor offset; click on board → places component such that
   anchor cell aligns with click.

**Necessity**: without this verb, no component can move from
palette to board; L1 unsolvable.

**Layout** (10×10):
- Board zone: rows 0..6 (7 rows). Palette zone: rows 7..9.
- Components in palette:
  - `comp_red_bar3` at base (1, 8) (occupies (1..3, 8)).
  - `comp_yellow_bar2` at base (6, 7) (occupies (6, 7..8)).
- Target shadow cells (sprites tagged `target`):
  - Red target shadow at (2, 2), (3, 2), (4, 2).
  - Yellow target shadow at (7, 3), (7, 4).
- Step budget = 16.

**Witness (4 actions):**
```
1. ACTION6 @ click cell (1, 8)  # pick up red bar; anchor=leftmost
2. ACTION6 @ click cell (2, 2)  # place; bbox top-left at (1, 2) -- wait recompute. anchor relative = (0, 0). place = click - anchor = (2, 2) - (0, 0) = (2, 2). bbox at (2..4, 2). ✓ red lands on shadow.
3. ACTION6 @ click cell (6, 7)  # pick up yellow bar; anchor=top
4. ACTION6 @ click cell (7, 3)  # place; bbox at (7, 3..4). ✓ yellow on shadow.
```

**Difficulty justification:**
- (a) Random-resistance: Each click is a 1-of-100 cell; correct
  anchor + correct target = (1/100)² per attempt; witness needs
  4 specific clicks ⇒ random expected ~1e-8. Step budget 16
  bounds attempts to 16; combinatoric << 1/10000.
- (b) Human-tractable: ~60s for first-time learner to discover
  the click-to-pick + click-to-place pattern.
- (c) Planning depth: near-zero; mechanic discovery is the
  difficulty (anchor convention learned in 1-2 trial placements).
- (d) Step budget: 16 = 4× witness; ample for trial-and-error.

### Level 2 — base + rotation (12×12 grid)

**Mechanics required (N + 1 = 2):**
1. Anchor-pivot place (carried forward).
2. **Rotate held**: ACTION5 rotates the held component 90° CW;
   the anchor offset rotates with the pixels so the clicked
   physical pixel remains the anchor.

**Necessity**:
- Anchor-pivot place still required (else nothing moves).
- Rotate held: `comp_red_vbar3` is initially vertical (1×3) but
  the red target shadow is HORIZONTAL (3×1). No anchor choice
  alone can rotate the component; only ACTION5 does. Removing
  ACTION5 → red component cannot fit horizontal target → L2
  unsolvable. STRICTLY REQUIRED.

**Layout** (12×12):
- Board zone: rows 0..8. Palette zone: rows 9..11.
- Components:
  - `comp_red_vbar3` at base (1, 9) (occupies (1, 9..11)).
  - `comp_yellow_L` at base (4, 9). L pixels:
    `[[11, -1], [11, 11]]` — covers (4,9), (4,10), (5,10).
  - `comp_green_bar2` at base (8, 10) (occupies (8..9, 10)).
- Target shadows:
  - Red target horizontal at (3, 2), (4, 2), (5, 2).
  - Yellow L target at (8, 4), (8, 5), (9, 5) (matches L shape).
  - Green target at (3, 7), (4, 7).
- Step budget = 28.

**Witness (8 actions):**
```
1. ACTION6 @ (1, 9)        # pick red vbar; anchor=(0,0) of bbox (the top cell at col 1 row 9 absolute → bbox-relative (0,0)).
2. ACTION5                 # rotate 90° CW; bbox now 3×1 horizontal. The pixel that was at relative (0,0) — top of vertical — is now at relative (2, 0) — rightmost of horizontal.
3. ACTION6 @ (5, 2)        # place; bbox at (5-2, 2-0) = (3, 2). bar at (3..5, 2). ✓ matches red target.
4. ACTION6 @ (4, 9)        # pick yellow L; anchor=(0,0).
5. ACTION6 @ (8, 4)        # place; bbox at (8, 4). L at (8,4),(8,5),(9,5). ✓.
6. ACTION6 @ (8, 10)       # pick green bar; anchor=(0,0).
7. ACTION6 @ (3, 7)        # place; bbox at (3, 7). bar at (3,7),(4,7). ✓.
   (no action 8 needed — only 7 actions, witness is 7)
```

Witness = 7 actions.

**Difficulty justification:**
- (a) Random-resistance: 3 components × ~3 clicks each + 1
  rotation; combinatoric << 1/10000 in a 144-cell grid.
- (b) Human-tractable: ~2 minutes; rotation discovered by trial.
- (c) Planning depth: non-trivial multi-step. Per-step reasoning
  chain: (1) identify which target is unfilled; (2) pick the
  matching-color component from palette; (3) determine if the
  component's current orientation matches the target; (4) if
  not, plan rotation count (1, 2, or 3 ACTION5 presses); (5)
  pick anchor pixel and target click pixel that align after
  rotation. Trivial heuristic that fails: "click center of
  component, click center of target, never rotate" — the red
  vertical bar never matches the horizontal target without
  rotation. Spam-ACTION5 fails because rotation has no effect
  unless a component is held.
- (d) Step budget: 28 = 4× witness; generous.

### Level 3 — base + rotation + flip (14×14 grid)

**Mechanics required (N + 2 = 3):**
1. Anchor-pivot place.
2. Rotate held (carried forward).
3. **Flip held horizontally**: ACTION7 mirrors the held component
   across its vertical centre axis; anchor mirrors with the pixels.

**Necessity**:
- Anchor-pivot place: required (else nothing moves).
- Rotate held: `comp_green_T` starts in one orientation; its
  target shadow is in another orientation that requires
  rotation (1, 2, or 3 quarter-turns).
- **Flip held**: `comp_red_Z` (Z-tetromino) is chiral: no rotation
  produces an S-tetromino shape from a Z. The red target shadow
  is shaped like an S-tetromino. Removing ACTION7 → no path
  produces S from Z → L3 unsolvable. STRICTLY REQUIRED.

**Layout** (14×14):
- Board zone: rows 0..10. Palette zone: rows 11..13.
- Components:
  - `comp_red_Z` at base (1, 11). Z pixels:
    `[[8, 8, -1], [-1, 8, 8]]` — cells (1,11),(2,11),(2,12),(3,12).
  - `comp_yellow_S` at base (5, 11). S pixels:
    `[[-1, 11, 11], [11, 11, -1]]` — cells (6,11),(7,11),(5,12),(6,12).
  - `comp_green_T` at base (9, 11). T pixels:
    `[[14, 14, 14], [-1, 14, -1]]` — cells (9,11),(10,11),(11,11),(10,12).
  - `comp_magenta_bar2` at base (1, 13).
- Target shadows on board:
  - Red target SHADOW shaped like S-tetromino at:
    (2, 3), (3, 3), (1, 4), (2, 4) — the S shape. Red component
    needs to be FLIPPED to match.
  - Yellow target shaped like S at (8, 3), (9, 3), (7, 4),
    (8, 4) — matches yellow component directly (yellow is
    already S-shaped).
  - Green target shaped like T-rotated:
    (3, 7), (4, 7), (3, 8), (3, 9) — actually let me make it a
    rotated T. Specifically: T rotated 270° CW is `[. T .], [T T .], [. T .]` but vertical. Use:
    (4, 6), (3, 7), (4, 7), (4, 8) — a T rotated 90° CW (vertical T pointing left).
    Rotation needed: green starts as T pointing down. 90° CW gives T pointing left.
  - Magenta target at (10, 9), (11, 9). Direct match.
- Step budget = 40.

**Witness (10 actions):**
```
1. ACTION6 @ (1, 11)       # pick red Z; anchor=(0,0).
2. ACTION7                 # flip horizontal. Anchor mirrors.
3. ACTION6 @ click on red target → places red as flipped Z (= S shape) on red shadow.
4. ACTION6 @ (5 or 6, 11)  # pick yellow S directly.
5. ACTION6 @ click on yellow target → place.
6. ACTION6 @ (10, 11)      # pick green T.
7. ACTION5                 # rotate 90° CW.
8. ACTION6 @ click on green target → place.
9. ACTION6 @ (1, 13)       # pick magenta bar.
10. ACTION6 @ click on magenta target → place.
```

10 actions. (Coordinates of target clicks chosen consistent with
each component's bbox after transformation.)

**Difficulty justification:**
- (a) Random-resistance: 4 components, each requiring specific
  click + transformation + click. Combinatoric << 1/10000.
- (b) Human-tractable: ~3 minutes including flip-discovery.
- (c) Planning depth: strictly deeper than L2. New decision per
  component: does this need a flip? Flip + rotate combinations
  produce 8 distinct orientations (chirality × rotation); player
  must identify which orientation matches the target. Trivial
  heuristic that L3 defeats: "always rotate, never flip". The Z
  component cannot reach S via rotation alone — proof: rotations
  of Z are {Z, Z-rotated-90, Z, Z-rotated-90} (only 2 distinct
  orientations because Z has 180° symmetry); none match S.
  Adjacent-action commute test: in the witness, **actions 1 and
  2** (pick Z, flip) cannot be commuted — flip with nothing
  held is a no-op (the flip mechanic is a no-op without a held
  component), so swapping leaves Z unflipped. Swapping actions
  2 and 3 places UNFLIPPED Z on the S target → mismatch → not a
  win.
- (d) Step budget: 40 = 4× witness; ≥ L2's budget of 28 (per
  non-shrinking rule).

## 5. Action mapping

`available_actions = [5, 6, 7]`

| Action | Effect | Gating |
|---|---|---|
| ACTION5 | If a component is held, rotate it 90° CW (the anchor offset rotates with the pixels). If nothing held, no-op. | Always offered. Always consumes 1 step. |
| ACTION6 | Click. If nothing held: find any sprite tagged `component` whose pixels overlap the clicked grid cell — pick it up and record anchor relative to the sprite's bbox. If a component is held: place it at `(click_x - anchor_col, click_y - anchor_row)`, update its position, then drop it (held = None). | Always offered. Always consumes 1 step. |
| ACTION7 | If a component is held, flip it horizontally (mirror across its vertical centre); the anchor offset mirrors with the pixels. If nothing held, no-op. | Always offered. Always consumes 1 step. |

## 6. HUD and per-game state

- `StepCounterHud`: bottom-row depleting bar.
- Per-game state on `self`:
  - `self.held_component: Optional[Sprite]`.
  - `self.anchor_offset: tuple[int, int]` (col, row relative to
    held bbox).
  - `self.steps_left: int`.

## 7. Win condition

Each level seats one *target shadow group* per component (matched
by colour tag, e.g. all `target_red` cells form the red target).
A component is "fitted" when its current pixel cells (post-
transformations, at its current sprite.x/y) exactly equal the
set of cells of its matching target group. Win = every component
is fitted. Predicate runs after every ACTION6 placement.

## 8. Lose condition

`self.steps_left <= 0` ⇒ `self.lose()`.

## 9. Novelty note

Closest taxonomy: **sb26** (`tile-place-commit`) — click-tile-then-
click-slot. Distinguishing rule: sb26 places a tile in a discrete
fixed slot index; pz4t places a multi-cell sprite at a free 2D
translation determined by `click − anchor`. sb26 has no rotation,
no flip, no anchor pixel.

Closest prior: **ng52** (`multiset-signature-classify`) — click
objects then click bin then ACTION5 commit. Distinguishing rule:
ng52 partitions a pool into bins by multiset signature, no
geometric assembly; pz4t is a free-translation jigsaw assembly
with rotation + flip transformations.

`prior-games/index.md` is non-empty (10 entries including vn4j).
None matches the anchor-pivot-place family.
