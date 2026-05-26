# mechanic-pick

- **game_id**: `wt39`
- **mechanic_family**: `glide-deflect-thaw`

## One-paragraph description

A small pawn rests on a tiled ice arena bordered by walls. Pressing
a cardinal arrow (ACTION1-4) launches the pawn gliding in that
direction; it slides cell-by-cell along the ice and only stops
when it crashes into a wall, the arena edge, or another solid
piece. Scattered across the ice are angled-bumper tiles whose
diagonal stripe deflects an incoming slide ninety degrees clockwise
or counter-clockwise (encoded by the stripe's orientation), and
brittle thaw-tiles that crack and disappear immediately after the
pawn glides off them. The level is solved when the pawn comes to
rest on the same-coloured goal-ring; the pawn must be guided by
choosing slide directions whose stopping points and bumper-
deflections route it onto the goal, and on later levels a path may
require crossing thaw-tiles in a particular order so that no
necessary route is severed before it has been used.

Prior categories used (per `core-knowledge-priors.md`):

- **Objectness** — pawn, bumpers, thaw-tiles, walls, goal are
  persistent entities.
- **Basic physics** — momentum-based gliding, friction-zero on ice,
  collision-stop on walls, ninety-degree elastic deflection on
  bumpers.
- **Basic geometry / topology** — connectedness of post-thaw paths
  determines whether a route remains viable; bumper orientation is
  a rotational symmetry choice.

## Per-level composition (preview for write_spec)

- **L1** — base dynamic: pawn + walls + goal. The arena geometry
  forces 2-3 slides through stopping cells to reach the goal.
  No bumpers, no thaw-tiles.
- **L2** — base + **angled bumpers** (M2): the goal is positioned
  so no straight-shot slide stops on it; the pawn must glide into
  a bumper to deflect off-axis at least once.
- **L3** — base + bumpers + **brittle thaw-tiles** (M3): every
  candidate route crosses at least one thaw-tile; each thaw-tile
  cracks after one traversal, so the order of slides matters and
  greedy / forward-only planning fails.

## Action mapping (preview)

- ACTION1-4: slide UP / DOWN / LEFT / RIGHT.
- No ACTION5, no ACTION6, no ACTION7. Pure cardinal-motion game.

## Novelty — concrete distinguishing rules

`prior-games/index.md` is NOT empty (14 entries). Walked the
positive `similarity-check.md` against the 25 taxonomy entries
and the 14 priors. The closest near-misses and their concrete
distinguishing rules:

### Taxonomy (25 reference games)

| near-miss | rule that distinguishes wt39 |
|---|---|
| **vn8d-prior** (out of taxonomy but listed below) | — |
| **ar25 shape-mirror-cover** | ar25 reflects a SHAPE across a static mirror line and the player nudges either shape or mirror; wt39 reflects MOTION (a sliding pawn's path) and there is no mirror sprite — only bumpers that deflect a transient trajectory. The agent that "moves" in ar25 is a copy-shape; in wt39 the pawn itself moves and stops. No shape-coverage scoring. |
| **ka59 sokoban-explode-chase** | ka59 moves the active pawn ONE 3-cell step per arrow press (push-style); wt39 moves the pawn UNCONDITIONALLY UNTIL collision (glide-style). ka59 has no momentum, no bumper deflection, and no fragile tiles. |
| **m0r0 mirror-orb-merge** | m0r0 moves two paired orbs in mirrored directions one cell per press; wt39 has a single pawn that glides indefinitely. m0r0's mechanic is "press LEFT moves one orb left, the other right"; wt39 has no mirroring of input — only physical inertia. |
| **pj7k rolling-cube-face-paint** (prior, see below) | — |
| **tu93 maze-pickup-train** | tu93 hops the pawn 3 cells per press through a value-2 corridor maze; wt39 glides until obstruction along an open arena. tu93 has no inertia, no bumpers, no fragile tiles. The arena topology in wt39 (open ice with sparse obstacles) inverts tu93's labyrinth-of-corridors. |
| **vc33 row-slide-pull-tab** | vc33's "slide" is the entire ROW of tiles sliding when the player clicks a tab; the units ride passively. wt39's "slide" is the PAWN itself moving while the floor stays put. Different agency, different cardinality (row-of-tiles vs single-pawn), different input (click-tab vs arrow-press). |

### Prior-games (14 entries)

| near-miss | rule that distinguishes wt39 |
|---|---|
| **kn58 anchor-pull-magnet** (most recent prior in family of "single action causes far-reaching motion") | kn58 click places a magnet anchor; every coloured pawn slides ONE cell along its dominant Manhattan axis toward it. Three differences: (a) wt39's input is a directional ARROW (not a click), (b) the move is UNBOUNDED (until wall), not one cell, (c) there is one pawn, not many. |
| **vn8d domino-cascade-topple** | vn8d's single click triggers a deterministic chain reaction through pillars; the player chooses WHICH chain to ignite. wt39's slide is a single physical glide, not a chain reaction; rotators in vn8d turn the cascade direction whereas wt39's bumpers deflect a single moving pawn. vn8d has burst-pads that splay 4 directions; wt39 has no splaying — deflection is 90° one-way. |
| **pj7k rolling-cube-face-paint** | pj7k rolls a 6-faced cube one step per press, permuting which face is bottom and depositing colour. wt39's pawn does not roll, has no faces, deposits no colour. Mechanic is glide-stop, not roll-and-stamp. |
| **fz5j phase-step-tile** | fz5j has tiles that pulse open/closed on per-cell periods, costing a life on a closed tile. wt39's thaw-tiles vanish after ONE traversal (consume, not pulse), and there are no lives — the pawn cannot fall through (instead the route becomes blocked for future slides). The constraint is "this route is single-use" vs "this tile is timed". |
| **bx84 beam-mirror-reflect** | bx84's deflection is on a BEAM (geometric ray drawn from an emitter); the player drops mirrors on empty cells and the beam follows them in the same step. wt39's deflection is on a PHYSICAL pawn that the player drives one slide at a time — the pawn's location is the game state, not a derived ray-trace. bx84 has no momentum and no fragile tiles. |
| **kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pz4t** | All clearly orthogonal — see `prior-games/index.md` descriptions; none involve directional unbounded motion of a single pawn. |

### Negative-similarity check (per `negative-similarity-check.md`)

Walking the 8 dimensions against the closest priors — **kn58
anchor-pull-magnet** and **vn8d domino-cascade-topple** — each:

vs **kn58**:
1. What's on the board: kn58 = many coloured pawns + click; wt39 = single pawn + ice arena + bumpers + thaw-tiles. **Different.**
2. Player input: kn58 = click; wt39 = arrow. **Different.**
3. What level asks: kn58 = every pawn on its goal pad; wt39 = single pawn on its goal-ring. **Different.**
4. What kills: both = step budget. **Same.**
5. Cast: kn58 = pawns + pads; wt39 = pawn + bumpers + thaw + goal. **Different.**
6. Visual signature: kn58 = bright coloured pawns on darker bg; wt39 = pale-blue ice + orange bumpers + sparse pawn. **Different.**
7. Pixel grain: both single-cell or 2x2 small. **Similar.**
8. Core dynamic: kn58 = "pick a magnet location to herd many pawns"; wt39 = "pick a glide direction to skate one pawn into goal". **Different.**

Shared dimensions: 4 (lose), 7 (grain). Two dimensions, threshold ≥ 3 → PASSES.

vs **vn8d**:
1. Board: vn8d = pillars + cascade-pads; wt39 = single pawn + ice + bumpers. **Different.**
2. Input: vn8d = click; wt39 = arrow. **Different.**
3. Level ask: vn8d = topple all pillars; wt39 = pawn on single goal. **Different.**
4. Kills: both step budget. **Same.**
5. Cast: vn8d = pillars + burst-pads + rotators; wt39 = pawn + bumpers + thaw. The rotator/bumper analogy is real but the rotators turn a cascading chain, not a moving pawn. **Different but adjacent.**
6. Visual: vn8d = monochrome pillars on darker bg; wt39 = pale-blue ice + warm bumpers. **Different.**
7. Grain: both small primaries. **Similar.**
8. Core dynamic: vn8d = "ignite a chain reaction"; wt39 = "skate one pawn through deflections". **Different.**

Shared dimensions: 4, 7, possibly 5 (deflectors-of-some-kind). Two-three dimensions, threshold ≥ 3 → BORDERLINE but PASSES on principle 3 (core dynamic): vn8d's player thinks about combinatorial chain ignition, wt39's player thinks about momentum-and-stopping-cells. The 8th dimension is the heaviest and they diverge there.

## ID generation

- Process: random 2-letter prefix `wt`, random 2-char suffix `39`.
- Collision check vs reserved 25: not in
  `{ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85,
    ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15,
    tn36, tr87, tu93, vc33, wa30}`. ✓
- Collision check vs prior-games index: not in
  `{kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t,
    vn8d, fz5j, kn58, bx84}`. ✓
- Not a recognisable English word. ✓
- Final: `wt39`.
