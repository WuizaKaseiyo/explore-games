# mechanic-pick.md

## Game ID
`dh4j`

ID generation: prefix `dh`, suffix `4j`. Four lowercase, alphanumeric, not an English word, not in the 25 reference IDs, not in `prior-games/index.md` or the unindexed (recent) `prior-games/<id>/` folders (verified by listing both).

## Mechanic family tag
`tile-coded-stride`

## One-paragraph description
**Tile-Coded Stride.** A single avatar walks a cell grid where each cell carries a visible *stride code* — three palette accents (small, medium, large pip-marks rendered as 1-, 2-, or 3-pixel pips on the cell tile) that encode how many cells the *next* arrow-press will translate the avatar. The avatar's next-move distance is always read off the cell it currently occupies (not from any HUD); pressing an arrow then translates the avatar by that count in the chosen direction, animating cell-by-cell so the path is legible, halting one cell short if a wall would be crossed (so over-shoot is impossible). The base mechanics are: (a) cell-pip count determines next-move stride, (b) walls (and grid edges) clamp the slide, (c) the goal cell is reached and triggers next-level. Levels compose by adding a *filter cell* at L2 that, when the avatar lands on it, swaps the global pip-code mapping between two pre-shown alternates (so cells that read "1" now move "3" and vice versa), and a *facing pivot cell* at L3 that rotates the next arrow press 90° clockwise from the pressed direction (forcing players to plan their arrow choice with a rotation in mind). L3's witness must use stride, filter, and pivot together to reach a goal that's behind a wall corner unreachable by any single mechanic.

## Core-knowledge prior categories used
- **Objectness**: avatar, walls, target, filter cell, pivot cell are persistent sprites.
- **Basic physics**: discrete momentum/translation by a fixed integer N per press; obstacles (walls) clamp the slide.
- **Basic geometry & topology**: 90° rotation of next-press direction (pivot cell); cardinal-direction encoding.
- **Agentness**: not used — there are no autonomous NPCs.

## Mechanic enumeration (per level)
- **L1**: M1 = cell's pip-count sets the next-move stride (1, 2, or 3); M2 = walls and grid edges clamp the slide partway; M3 = avatar overlapping goal triggers next_level.
- **L2**: M1, M2, M3 + M4 = filter cells, when overlapped, globally swap the pip-code-to-stride mapping between two pre-shown legends (each legend rendered persistently as a HUD strip at the top edge, with one currently highlighted).
- **L3**: M1, M2, M3, M4 + M5 = facing-pivot cells, when overlapped, rotate the *next* arrow press's direction by 90° clockwise (so an UP press from a pivot becomes a RIGHT motion of the cell's stride).

Each level introduces exactly +1 new mechanic (passes the +1/+2 rule).

## Distinguishing rules vs near-miss taxonomy / prior-games entries

Run against `mechanic-novelty/similarity-check.md` (positive) and `negative-similarity-check.md` (eight-dimensional surface-overlap test).

### Taxonomy near-misses

- **bp35 (gravity-fall-navigation)** — auto-falls one row per step; side-step changes column; flippers invert gravity axis. **Distinguish**: bp35 has *implicit constant-direction auto-motion* (gravity) and *side-step* arrows; mine has *per-press explicit-direction* with *variable stride read off the floor*. No auto-motion in mine, and the variable comes from the floor not from a gravity rule.

- **ka59 (sokoban-explode-chase)** — slide active block one cell + chain detonations + chasing enemy. **Distinguish**: ka59 slides *blocks* (not avatar) by 1 cell with detonation chains. Mine has *avatar slide* by N cells (no detonation, no chase). Verb cardinality differs; chain-reaction physics absent.

- **lt7m (ell-jump-tour-block)** — click an L-shape-reachable cell to jump; wake blocks; chaser. **Distinguish**: lt7m's verb is *click-target-L-shape jump* (cell-set lookup); mine is *arrow-direction + floor-stride*. Lt7m has no floor-encoded distance; jump shapes are L-fixed; mine has linear cardinal slide of variable N.

- **ls20 (cycler-attribute-match)** — avatar hops 5-pixel cells; pellets matched by avatar's shape/colour/rotation. **Distinguish**: ls20's hop-distance is *constant* per game; mine's hop-distance is *per-cell variable*. ls20 has avatar attributes; mine has floor attributes.

- **tu93 (lockstep-multi-maze)** — every walkable agent moves one cell per press in lockstep. **Distinguish**: tu93 is fixed-1-cell-per-press, multi-agent. Mine is variable-N-per-press, single agent. Verb cardinality differs (N vs 1) and there's no second agent.

### `prior-games/index.md` near-misses

- **bz3k (drift-impulse-cardinal)** — avatar carries persistent integer velocity; arrows ±1 impulse. **Distinguish**: bz3k's velocity is *carried internally* by the avatar across turns (persistent state); mine has *no velocity state on the avatar* — each press reads the floor and translates that step's count. bz3k's `cap-bands clamp speed` is a different physical metaphor than my walls clamping the slide. The persistent-velocity vs no-velocity distinction is the load-bearing one.

- **fz5j (phase-step-tile)** — per-cell pulse periods 2/3/4; entering a closed tile costs a life. **Distinguish**: fz5j cells *open/close periodically over time*; mine cells *don't change with time*. Fz5j's number is a temporal period; mine's pip-count is a spatial stride. No life mechanic in mine.

- **kn58 (anchor-pull-magnet)** — click any cell to drop magnetic anchor; pawns slide one cell along dominant axis toward it. **Distinguish**: kn58 slides *all pawns* one cell *toward an anchor*; mine slides *the avatar* N cells *in the pressed direction*. Direction is pressed not magnetic-radial. Cardinality (one vs N) and direction-rule (radial-attract vs pressed) both differ.

- **vt6q (grapple-anchor-yank)** — fire a directed cardinal grapple; heavy anchor yanks avatar adjacent. **Distinguish**: vt6q's verb is *fire-grapple* (long-range to first anchor); mine's verb is *floor-coded-stride-slide* (N cells through space). vt6q's distance depends on first encountered anchor; mine's distance depends on origin-cell's pip-code.

- **wt39 (glide-deflect-thaw)** — pawn glides in pressed direction until wall; bumpers deflect 90°; brittle tiles. **Distinguish**: wt39 glides *until wall* (unbounded N) with bumpers that *reflect*; mine has *bounded N from origin cell* and pivots that *rotate the pressed direction* (not reflect the slide mid-air). wt39's L1 has effectively N=∞; mine's L1 has N∈{1,2,3}.

- **ek73 (wake-trail-evade)** — avatar walks one cell per press; vacated cells become decaying hazards. **Distinguish**: ek73 is *1-cell-per-press with hazard wake*; mine is *N-cell-per-press with floor-coded N*. No wake or hazard in mine.

- **pk4m (duotone-flip-walk)** — binary avatar colour; cells gate by polarity match. **Distinguish**: pk4m gates *passability by cell-vs-pawn color match*; mine reads *stride number from cell*. pk4m's binary is per-cell-color; mine's three-state is per-cell-pip-count.

- **lz7q (dual-plane-walk)** — two superimposed planes; ACTION5 toggles active plane. **Distinguish**: lz7q has two whole-grid layers swap on ACTION5; mine has *one playfield with per-cell stride values*. No layer toggle in mine, no ACTION5 verb at all — `available_actions=[1,2,3,4]`.

- **fw8c (pigment-mix-walk)** — carrier accumulates 3-bit pigment subset; pigment-gated doors. **Distinguish**: fw8c accumulates a *carried subset state* over time; mine reads stride from cell each press with *no carried state at all*. fw8c's gates are color-subset-match; mine doesn't gate anything by carried state.

- **vk6m (altitude-grip-climb)** — discrete-altitude topography; grip state required for +1 altitude transitions. **Distinguish**: vk6m gates climbs by *carried grip state*; mine has *no carried state*. vk6m's cell encodes altitude (height-vs-walkability); mine's cell encodes stride (distance-of-next-move).

- **xz5g (arena-pivot-rotate)**, **nz3v (rotor-pivot-walk)** — rotation-around-pivot mechanics. **Distinguish**: my L3's pivot cell *rotates next-press direction 90°* (a per-press, per-cell transform) without rotating sprites or playfield. xz5g and nz3v rotate sprites/playfields; mine rotates only the pressed direction code.

## Negative-similarity-check (eight-dimension surface-overlap test)

Walked against the closest single prior (bz3k drift-impulse-cardinal, as the strongest visual+dynamic near-miss) and the closest reference game (ls20 cycler-attribute-match):

vs **bz3k**:
1. Board: pawn + grid + walls + targets → SHARED.
2. Player action: arrow presses (no click, no ACTION5) → SHARED.
3. Win condition: reach target → SHARED.
4. Killer: step counter exhaustion → SHARED.
5. Supporting elements: cap-bands (bz3k) vs filter/pivot cells (mine) → DIFFERENT.
6. Visual signature: bz3k's avatar visibly shows a velocity arrow accent + cap-bands as palette stripes; mine shows a *per-cell pip-count* (1/2/3 pips painted on each floor tile) which is a fundamentally different rendering style — many small floor accents vs a single drifting arrow. → DIFFERENT.
7. Pixel grain: bz3k uses sparse arrow accents on small avatars; mine uses dense per-cell pip-painting (every walkable tile has a pip cluster). → DIFFERENT.
8. Core dynamic: bz3k = persistent-momentum that arrows ±1 impulse (impulse-into-velocity); mine = floor-coded variable-N stride per press with no velocity state. → DIFFERENT.

Shared dimensions: 1, 2, 3, 4. Four (none of them the named principles 6/7/8). Passes the negative check (threshold is 3+ on the named principles or 5+ overall on a single prior).

vs **ls20**:
1. Board: pawn + maze + targets → SHARED.
2. Player action: arrow presses → SHARED.
3. Win condition: visit pellets / reach target → SHARED.
4. Killer: step counter / lives → SHARED.
5. Supporting elements: ls20 has shape/colour/rotation cyclers + patrol enemies + bullets; mine has filter cells + pivot cells (and no NPCs at all). → DIFFERENT.
6. Visual signature: ls20 features attribute-cycle tiles (shape/colour/rotation triplet) + bullets + patrolling-enemies; mine features uniform floor with per-cell stride pips. → DIFFERENT.
7. Pixel grain: ls20 mixes large maze tiles with bullet streams and patrol AI sprites; mine is calmer with floor-pip detail. → DIFFERENT.
8. Core dynamic: ls20 = *avatar carries shape/colour/rotation indices and matches them to pellets* (carried-state matching); mine = *cell-coded variable stride with no carried state*. → DIFFERENT.

Shared dimensions: 1, 2, 3, 4. Same as above. Passes.

Conclusion: novel mechanic family on both the positive (similarity-check) and negative (eight-dimension) tests. Specifically the *floor-cell-encodes-the-next-move's-translation-distance* dynamic has no analog in either the 25-reference taxonomy or the 80+ prior-games corpus.

## Seed
None (autonomous run).
