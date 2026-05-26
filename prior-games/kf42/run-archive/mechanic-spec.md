# mechanic-spec — `kf42` (revision 2)

> Revision 2 addresses all 5 items raised in
> `workspace/critique-revisions.md`. Sections that changed are marked
> `[REVISED — addresses Issue N]` at their head and quote the issue
> they fix.

## 1. Title
**Tether-Pair with Colour-Set Pads** *(internal working title; the
in-game ID is the opaque `kf42`)*. *(Title sub-clause changed from
"Colour-Cycle" to "Colour-Set" to reflect the unified single-step
semantics — see Issue 3.)*

## 2. Mechanic family

[REVISED — addresses Issue 3.]
*Quote of the issue:* "Unify cycler semantics to **direct
colour-set across both levels** … walking the active pawn onto a
cycler pad whose visible colour is `c_pad` sets the active pawn's
body colour to `c_pad` (single visit; idempotent)."

Two single-cell pawns on a walled grid are coupled by an *invisible
maximum-length tether* (Chebyshev distance ≤ L cells, level-specific
L). The player clicks one pawn to designate it active, then arrows
move the active pawn one cell. The inactive pawn is dragged exactly
one cell along the line that minimises tether strain *only* when an
active-pawn step would otherwise cause distance-to-inactive to
exceed L. From level 2 onward, walking the active pawn onto a
**colour-set pad** sets that pawn's body colour to the pad's visible
colour (single-visit; the operation is idempotent on a second
visit). The level wins when each pawn simultaneously sits on a
target pad whose colour equals that pawn's *current* body colour.

The family-tag `tether-pawn-cycle` is retained because "cycle"
captures the moment-of-walk colour change; the cycler is now a
direct-set rather than an alphabet-walker. (This *strengthens* the
distinguishing rule against `ls20` — see §9.)

Priors used: **objectness** (two persistent pawns + persistent
target pads + persistent set-pads), **basic geometry & topology**
(grid walls + Chebyshev-distance constraint), **basic physics**
(maximum-length tether transmits a one-cell drag impulse).
**Agentness is not used.**

## 3. Sprite roster

[REVISED — addresses Issues 1 and 2.]
*Quote of Issue 1:* "Replace with a 3×3 *diamond-cross* — four
pixels at the edge midpoints, four transparent corners, transparent
centre."
*Quote of Issue 2:* "Replace with a 3×3 *solid filled square* — no
asymmetry."

| name | dimensions | palette values | tags | role |
|---|---|---|---|---|
| `wrytkfvuvc` | 1×1 | 8 (recoloured 8/9/11 per pawn instance) | `pawn`, `sys_click` | pawn (single cell, click-selectable) |
| `qmjvbnpkrt` | 3×3 | 8 (also 9 / 11 per instance) + `-1` transparent | `target` | colour-target pad (4-pixel diamond-cross around a transparent centre) |
| `xbjhuofwzg` | 3×3 | 8 (also 9 / 11 per instance) | `cycler` | colour-set pad (3×3 solid filled square) |
| `npbflzrxqj` | 1×1 | 4 | `wall` | wall block (off-black) |
| `gtnzphmkmw` | 1×1 | 5 | `bg-stripe` | optional decorative tick (palette 5, layer 0) |

**`wrytkfvuvc.pixels`** (pawn — single cell):
```
[[8]]
```
Recoloured per instance via `clone().color_remap(None, c)` where
`c ∈ {8 red, 9 blue, 11 yellow}`.

**`qmjvbnpkrt.pixels`** (target pad — diamond-cross frame; revised):
```
[-1,  c, -1],
[ c, -1,  c],
[-1,  c, -1],
```
Pixel `c` is the pad's instance colour. The four solid pixels sit at
the edge-midpoints; the centre cell is transparent (`-1`); the four
corners are transparent. The pawn lands on the (1, 1) centre cell;
the diamond-cross frames the pawn on all four sides without
overlap. Set `interaction=InteractionMode.INTANGIBLE` so the pad
is rendered but does not block movement onto its centre cell. The
silhouette is a 4-fold-rotation symbol — not a digit, letter, or
real-world clipart.

**`xbjhuofwzg.pixels`** (colour-set pad — solid filled; revised):
```
[c, c, c],
[c, c, c],
[c, c, c],
```
Pixel `c` is the pad's instance colour. Set
`blocking=BlockingMode.NOT_BLOCKED` and
`interaction=InteractionMode.INTANGIBLE` so the pawn can occupy
any of the 9 cells visually on top. Trigger detection: when the
pawn moves to `(x, y)`, query `level.get_sprite_at(x, y,
tag="cycler")`; if any 3×3-cycler-pad sprite covers `(x, y)`, set
the active pawn's colour to that pad's `c`.

**`npbflzrxqj.pixels`** (wall — single cell, palette 4):
```
[[4]]
```
Tag `wall` is queried by movement to gate steps.

## 4. Level progression sketch (EXACTLY 3 levels)

[REVISED in L3 only — addresses Issue 3 (cycler unification).]

### Level 1 — tutorial (tether mechanic alone, on an open arena)
*(unchanged from rev. 1.)*
- `grid_size = (12, 12)`. Border walls only; interior is empty.
- Two pawns: red at `(2, 6)`, blue at `(3, 6)`.
- Two target pads (diamond-cross frames): red at `(8, 5)`
  (centre = (9, 6)), blue at `(7, 5)` (centre = (8, 6)).
- Tether L = 4 (Chebyshev). Step budget 30. NO cycler pads.
- Solvable in ~14 actions: click red, RIGHT × 7 (red ends at (9,6);
  blue is dragged from (3,6) to (5,6) when the constraint binds at
  distance 4), click blue, RIGHT × 3 (blue ends at (8,6)).
- Random-policy solubility: large budget (30) vs ~14 optimal across
  a 5-action search space — occasional stumble-success is plausible
  per §3.4 tutorial expectation.

### Level 2 — second mechanic (one colour-set pad)
*(small adjustment — pads now follow the unified set-semantics.)*
- `grid_size = (14, 14)`. Border walls + a short interior wall at
  column 7, rows 4-6.
- Two pawns at `(2, 7)` and `(3, 7)`, both starting **red** (8).
- Two target pads (diamond-cross frames): red at `(10, 4)`
  (centre = (11, 5)), **blue** at `(10, 8)` (centre = (11, 9)).
- One **blue** colour-set pad (3×3 solid, palette 9) at `(6, 8)`
  (covers cells (6,8)..(8,10)).
- Tether L = 5. Step budget 50.
- Solving: walk exactly ONE pawn through the blue pad to convert
  it red → blue, then route both onto their colour-matched targets.
  The tether complicates this — the cycler is positioned such that
  a naive route drags the inactive pawn onto the cycler too.
  Click-switching active mid-route is required.

### Level 3 — composition (tether + two colour-set pads + maze) [REVISED]
*Quote of Issue 3 (L3 portion):* "Replace the L3 description's
'yellow → red' / 'yellow → blue' cyclic-arrow language with 'red
cycler (sets to red)' / 'blue cycler (sets to blue)'. The pawn's
starting colour at L3 should change accordingly."

- `grid_size = (16, 16)`. Border walls + interior walls forming
  two narrow corridors. The maze layout (placement of `npbflzrxqj`
  blocks):
  - row 8: walls at columns 4..6 and 9..11 (a narrow horizontal
    barrier with two gaps at columns 3 and 7-8 on either side
    of the cyclers).
  - column 7: walls at rows 5..6 and 10..12 (forming a vertical
    spine that separates the two cyclers and a "meeting" channel).
- Two pawns at `(2, 13)` and `(2, 14)`, starting **red** (pawn 0)
  and **blue** (pawn 1).
- Two target pads (diamond-cross frames):
  - **blue** target at `(13, 4)` centre = (14, 5).
  - **red** target at `(13, 11)` centre = (14, 12).
  Note that pawn 0 (red) must end up on the *red* target and pawn 1
  (blue) on the *blue* target — but the targets are swapped in
  Y-position relative to the pawns' starting Y. That is, the red
  pawn must reach the upper region (top row of the screen) and the
  blue pawn must reach the middle-lower region. With the tether
  constraint and the maze layout, the natural corridor for each
  pawn forces it into the *opposite* colour cycler first — so the
  player must route each pawn through a cycler that *changes* its
  colour (red → blue and blue → red) and *then* through a second
  cycler that changes it back, picking up the right routing in the
  process.
- Two colour-set pads:
  - **red** colour-set pad (3×3 solid palette 8) at `(6, 4)` —
    covers (6,4)..(8,6); centre row in upper corridor.
  - **blue** colour-set pad (3×3 solid palette 9) at `(6, 11)` —
    covers (6,11)..(8,13); centre row in lower corridor.
- Tether L = 6. Step budget 80.
- Composition: the maze geometry forces the upper corridor to be
  reachable only by the lower-starting pawn first crossing through
  the red cycler (which sets it to red — fine for the eventual red
  target), and the lower corridor by the upper-starting pawn first
  crossing through the blue cycler (setting it to blue — fine for
  the blue target). However, doing both simultaneously violates
  the tether: a click-switch mid-route is required so neither
  pawn drags the other into the wrong colour-set pad. Two
  mechanics (tether + colour-set) are jointly necessary; neither
  alone clears the level.

## 5. Action mapping
*(unchanged from rev. 1.)*

The game uses **5 of 7 action slots** — `[1, 2, 3, 4, 6]`.

| slot | semantics |
|---|---|
| `GameAction.ACTION1` | move active pawn UP one cell (decrement y by 1). |
| `GameAction.ACTION2` | move active pawn DOWN one cell (increment y by 1). |
| `GameAction.ACTION3` | move active pawn LEFT one cell (decrement x by 1). |
| `GameAction.ACTION4` | move active pawn RIGHT one cell (increment x by 1). |
| `GameAction.ACTION6` | click `(data["x"], data["y"])`; if it lands on a `pawn`-tagged sprite, that pawn becomes active. |

Context-dependent gating (via `_get_valid_actions`):
- ACTION1..4 are not offered before the first ACTION6 selection;
  only ACTION6 is offered until a pawn is selected. This idiom
  matches sb26 (`game_sources/sb26/.../sb26.py:1129`).
- After the first selection, ACTION1..4 and ACTION6 are
  always-valid (each costs one step from the budget regardless
  of whether the move was blocked).

## 6. HUD and per-game state

[REVISED — addresses Issue 4 (hidden-state encoding).]
*Quote:* "Specify the layout explicitly: `[[active_pawn_index,
remaining_steps], [pawn[0].colour, pawn[1].colour]]`."

### HUD widgets (`RenderableUserDisplay` subclasses)
- **`StepBarHud`** — a one-row depleting bar at `frame[63, :]`.
  Holds `(self.max_steps, self.current_steps)`. `render_interface`
  paints the leftmost `64 * current/max` cells in palette 6
  (magenta) and the rest in palette 0 (white). Mirrors tu93's
  `klmvbszflr`.
- **`ActiveMarkerHud`** — a 1-pixel "selection L-bracket" drawn
  at the corners of the active pawn's display cell each frame.
  Reads `self.game.active_pawn`. (When no pawn is selected, the
  widget paints nothing.)

### Per-game state (held on the game class)
- `self.pawns: list[Sprite]` — exactly two entries; populated in
  `on_set_level`.
- `self.active_pawn: Sprite | None` — the currently active pawn,
  or `None` before the first ACTION6 selection. Reset to `None` at
  level start.
- `self.tether_length: int` — read from `level.get_data("Tether")`
  in `on_set_level`.
- `self.target_pads: list[tuple[Sprite, int]]` — `(pad_sprite,
  pad_colour)` for each pad in the level.
- `self.cycler_pads: list[tuple[Sprite, int]]` — `(pad_sprite,
  destination_colour)` for each colour-set pad (empty in L1).
- The HUD's `current_steps` counter is the only depleting resource;
  `on_set_level` calls `step_bar.reset(level.get_data("StepCounter"))`.

`level.data` shape (per level):
```python
data = {
    "StepCounter": <int>,    # action budget for this level
    "Tether":      <int>,    # max Chebyshev distance between pawns
}
```

### Hidden state (`_get_hidden_state`) [REVISED]
Returns a `(2, 2) np.int16` array with explicit layout:

```
[[active_pawn_index,  remaining_steps],
 [pawn[0].colour,     pawn[1].colour]]
```

Where:
- `active_pawn_index ∈ {-1, 0, 1}`. `-1` before the first selection.
- `remaining_steps` = `self.step_bar.current_steps`.
- `pawn[0].colour, pawn[1].colour` are the current palette values
  of pawn 0 and pawn 1 respectively (typed `int16`-safe; palette is
  0..15).

This guarantees that two states whose rendered frames are
identical but whose *active selection* or *colour state* differs
hash to distinct nodes (per §3.5.2 of the tech-report's graph-
identity invariant).

## 7. Win condition

[REVISED — addresses Issue 5 (win-condition formalisation).]
*Quote:* "WIN ⇔ ∃ a bijection f: pawns → target_pads s.t. for each
pawn p: (p.x, p.y) == f(p).centre AND p.colour == f(p).colour."

Each level has exactly two target pads with distinct centre cells.
`self.next_level()` is called at the end of `step()` iff there
exists a bijection `f: pawns → target_pads` such that, for each
pawn `p`:

- `p.x == f(p).centre_x` AND `p.y == f(p).centre_y`, AND
- `p.colour == f(p).colour`.

Concretely: both pawns occupy distinct pad centres; both
colour-matches hold simultaneously. Any state in which the two
pawns occupy the same cell automatically fails the predicate
(they cannot occupy distinct pad centres).

The implementation enumerates the two pawns, attempts to map each
to a target pad via position-equality, and confirms colour-equality
on the matched pad. If exactly two distinct matches exist, the
level is solved.

## 8. Lose condition
*(unchanged from rev. 1.)*

`self.lose()` is called at the end of any `step()` in which:
- `self.step_bar.current_steps == 0` AND the win predicate is
  false.

There are no other lose states. There are no hazards or chasing
agents. (Aligned with the dominant pattern in 23/25 reference games:
step counter is the only losing condition.)

## 9. Novelty note

[Slightly revised — see Issue 3 effect on `ls20`.]

### Closest taxonomy near-misses + concrete distinguishing rules

- **`m0r0` (`mirror-orb-merge`).** m0r0 couples its two pawns by
  a per-key MIRROR transform (every keypress moves both pawns,
  one mirroring the other on each axis). `kf42` couples its two
  pawns by a MAX-DISTANCE TETHER (only the active pawn moves on
  a key; the inactive pawn moves only when the constraint binds);
  there is no transform — only a slack region. m0r0's win is
  pair-merge into the same cell; `kf42`'s win is two pawns on two
  *distinct* colour-matched pads.
- **`r11l` (`centroid-puppet-leg`).** r11l uses a CENTROID coupling
  (a virtual ring tracks the average of the legs' positions and is
  what scores). `kf42` uses a MAX-DISTANCE TETHER between two
  CONCRETE pawns; there is no virtual sprite. r11l moves a leg by
  click-and-drag (one action covers a corridor); `kf42` steps a
  pawn one cell at a time. Win predicates differ (containment vs.
  positional+colour equality).
- **`sk48` (`paired-snake-trail`).** sk48 grows / retracts a snake's
  BODY one segment per arrow press; the win is a colour match
  between corresponding body-segment-tiles of two snakes. `kf42`
  keeps each pawn at one cell and never extends a body; the action
  effect is positional, not metric.
- **`ls20` (`cycler-attribute-match`).** ls20 cycles the AVATAR's
  shape, hue, OR rotation one notch via cycler tiles (an
  *alphabet walker*); win is a triplet match on a goal pad. `kf42`'s
  cycler is a *destination-setter* — walking onto a colour pad
  sets the pawn's colour to that pad's colour directly (single
  visit). `kf42` also has TWO avatars under a tether constraint and
  a *pair-of-equalities* predicate (each pawn's colour matches
  its colour-pad's colour, simultaneously) — neither the tether
  nor the dual-avatar nor the click-to-select-active is in ls20.
  After the rev-2 unification, the distinguishing rule becomes
  even sharper: ls20 advances by `+1 mod alphabet`, kf42
  assigns directly.

### vs `prior-games/index.md`
Empty (header-only, created by `pick_mechanic`). Trivially passes.

### Composition with other 25 entries
A "single program could solve `kf42` and reference game X with at
least 50% code-sharing" comparison fails for every reference game:
the tether-distance solver, the click-to-select bookkeeping, the
direct-colour-set pad triggering, and the simultaneous-occupancy-
plus-colour-equality win predicate are not jointly present in any
of the reference games' solvers.

**Verdict (re-checked at full-spec scope, post-revision): NOVEL.**
