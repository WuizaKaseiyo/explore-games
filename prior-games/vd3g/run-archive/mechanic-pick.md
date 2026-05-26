# Mechanic pick

## Game ID
`vd3g`

Verified non-colliding:
- Not in the 25 reserved reference IDs (ar25, bp35, cd82, cn04, dc22,
  ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26,
  sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30).
- Not in the 27 prior-games rows (kf42, qz73, kx14, qb84, lq5x, gv47,
  hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x,
  gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w, tg6w).
- Not an English word; lowercase alphanumeric; 4 chars.

## Mechanic family
`valley-dig-roll`

## One-paragraph description
The board is a binary HEIGHTMAP — every playfield cell is either a
HIGH bump (raised stone) or a LOW valley (cleared ground). Coloured
marble-pawns are placed on the board; each marble's win cell is a
matching-colour low-tile target. The player's only verb is
ACTION6 — click a cell to TOGGLE its height (high↔low). Immediately
after every click, every marble on a HIGH cell rolls one cell into
an adjacent LOW cell using a fixed cardinal priority (N→E→S→W); a
marble already on a LOW cell stays put (settled). If no adjacent
LOW cell exists, a marble on HIGH stays where it is. Two marbles
cannot occupy the same cell — a marble whose intended destination
is occupied yields and stays. The puzzle is to pick a click sequence
that channels every marble down through the dug-out valleys onto
its matching target without trapping any marble in the wrong valley.
A step-counter HUD is the lose trigger; ACTION6 is the only action
across L1; L2 introduces immutable WALL cells that can never be
toggled (and which marbles never enter); L3 introduces LINKED
ANCHOR pairs — two cells visually banded by a shared corner-cap
colour, where toggling one ALSO toggles its partner regardless of
distance, so every dig has a remote side-effect the player must plan
around. Mechanic uses physics priors (gravity-along-local-gradient
flow; deterministic step-by-step settling) plus objectness (discrete
marble pawns with identity).

## Core knowledge priors used
- **Physics**: gravity along a local height gradient — marbles roll
  to the adjacent lower cell (intuitive water-runs-downhill).
- **Objectness**: pawns are persistent identity-holding entities; two
  pawns cannot occupy the same cell.
- **Topology** (L2): walls are immutable barriers — pawns cannot
  enter wall cells regardless of height (impassable).

No agentness needed (no autonomous NPCs); no acquired symbolic
knowledge needed (high-vs-low reads from shading; targets read from
colour matching).

## Similarity check (positive — `similarity-check.md`)

Family-level scan over the 25 reference taxonomy + 27 prior-games
index. The candidate's family tag (`valley-dig-roll`) does not match
any prior family. Description-level near-misses examined:

### `tg6w` — settle-pile-tilt (prior-games index)
Description: "arrow press tilts the playfield's down direction;
loose blocks slide multi-cell to settle, with colour-permeable rim
walls and one-shot sticky-pads."
- Win condition: tg6w wants blocks to settle in particular
  rim-positions after multi-cell slides; vd3g wants marbles on
  matching-colour valley targets after one-cell-per-click rolls.
  **Different.**
- Primary action: tg6w uses ACTION1-4 arrow keys to tilt the entire
  playfield; vd3g uses ACTION6 click on a SPECIFIC cell to toggle
  that cell's height. **Different verb** (global press vs targeted
  click).
- Primary constraint: tg6w blocks slide as far as physics allow until
  colliding with rim-walls or settled blocks; vd3g marbles step
  exactly one cell per click into an adjacent low neighbour. **Very
  different settling rule** — multi-cell slide vs one-cell-step.
- **Distinguishing rule:** tg6w couples one player input to *global
  reorientation of gravity* and a multi-cell slide-to-rim physics
  resolution; vd3g couples one player input to *editing one cell of
  a heightmap* and a one-cell local-gradient step. The player edits
  the *playfield* in vd3g; the player edits *gravity direction* in
  tg6w.

### `kn58` — anchor-pull-magnet (prior-games index)
Description: "click any cell to place a single magnetic anchor;
every coloured pawn slides one cell along its dominant Manhattan
axis toward it."
- Win condition: both want pawns at coloured target cells. Same.
- Primary action: kn58 places a single global ANCHOR; one anchor
  influences every pawn. vd3g toggles a single cell's HEIGHT; the
  toggled cell influences only marbles whose adjacency includes it.
  **Different mechanism** — global attractor vs local terrain edit.
- Primary constraint: in kn58 the dominant-Manhattan-axis-toward-
  anchor rule is universal; in vd3g each marble independently
  inspects its 4-neighbourhood for a low cell. **Different** —
  global vector vs local lookup.
- **Distinguishing rule:** kn58 has ONE attractor whose location the
  player keeps re-placing; vd3g has NO attractor at all — the
  marbles flow according to local terrain that the player physically
  reshapes one cell at a time. A heightmap is a structural object;
  a magnetic anchor is a singular point-attractor.

### `kp9z` — grain-accumulate-topple (prior-games index)
Description: "click sources to drop grains; cells overflow at
capacity 4 to 4 cardinals; sinks absorb; click-rotatable redirectors
forward one grain in their oriented direction."
- Win condition: kp9z wants target counts at sinks; vd3g wants
  marbles at matching-colour targets. Different.
- Primary action: kp9z clicks SOURCES (sand-pile dispensers) and
  REDIRECTORS (rotators); vd3g clicks any cell to toggle terrain.
  **Different.**
- Primary constraint: kp9z is a sandpile model — overflow when
  capacity ≥ 4 cascades to neighbours; vd3g has no accumulation, no
  capacity, no cascade — single-step movement per pawn per click.
  **Very different.**
- **Distinguishing rule:** kp9z is a count-based cellular automaton
  with capacity overflow; vd3g is a binary-terrain field whose
  marble pawns step deterministically by one cell. Different state
  representation, different propagation rule.

### `mr5q` — polarity-attract-discharge (prior-games index)
Description: "pawns flip yang/yin via click; per ACTION5 each walks
toward nearest same-colour opposite; same-colour adjacency
discharges."
- Different: mr5q toggles PAWN polarity, vd3g toggles CELL height.
  Pawns are passive in vd5q (move on ACTION5) vs active per click in
  vd3g. mr5q has discharge interactions between adjacent pawns;
  vd3g pawns interact only via mutual exclusion of cell occupancy.
  **Distinguishing rule:** mr5q dynamics live on the pawns; vd3g
  dynamics live on the terrain.

### `m0r0` — mirror-orb-merge (reference)
Both involve directing multiple pawns toward target cells. m0r0 has
mirrored-axis controls (one input moves all four with reflected
axes). vd3g has independent local-gradient pawn motion. Player
verb: m0r0 ACTION1-4 directional, vd3g ACTION6 click. **Different**.

### `vc33` — row-slide-pull-tab, `lp85` — row-col-shift-grid
(reference)
Both move pawns indirectly by manipulating row/column elements.
vd3g manipulates per-cell binary state, not row/column groups.
**Different**.

### Verdict
NOVEL on family-level (no shared family tag). On
description-level, every flagged near-miss has a concrete
distinguishing rule articulated above; none shares all three of
(win condition, primary action, primary constraint).

## Negative similarity check (`negative-similarity-check.md`)

Walked the 8 dimensions against the 5 closest priors (tg6w, kn58,
kp9z, mr5q, fz5j). The dimensions:

| # | Dimension | vs tg6w | vs kn58 | vs kp9z | vs mr5q | vs fz5j |
|---|---|---|---|---|---|---|
| 1 | What's on the board | DIFF (heightmap+marbles vs blocks+rim+sticky) | DIFF (heightmap vs anchor+pawns) | DIFF (heightmap vs sources+sinks+redirectors) | DIFF (heightmap vs polarised pawns) | DIFF (heightmap vs phase-pulse tiles) |
| 2 | Player physical input | DIFF (click cell vs press arrow) | SAME (click cell) | DIFF (click cell vs click source) | SAME (click pawn) | SAME (click cell) |
| 3 | What the level asks for | DIFF (route marbles to colour targets vs settle blocks at rim) | SAME (pawns to coloured targets) | DIFF (marbles vs target counts at sinks) | DIFF (no discharge target) | DIFF (no avatar) |
| 4 | What kills the player | SAME (step counter) | SAME (step counter) | SAME (step counter) | SAME (step counter) | DIFF (lives + step counter) |
| 5 | Cast of supporting elements | DIFF (walls, anchors vs rim, sticky) | DIFF (walls, anchors vs single anchor) | DIFF (walls, anchors vs sources/sinks/redirectors) | DIFF | DIFF |
| 6 | Visible visual signature | DIFF (binary stone/valley field) | DIFF | DIFF (no count pips) | DIFF (no yang/yin marks) | DIFF (no pulsing tiles) |
| 7 | Pixel grain of primary sprites | DIFF | DIFF | DIFF | DIFF | DIFF |
| 8 | Core dynamic ("what is the player thinking?") | "shape the terrain" vs "tilt the world" — DIFF | "shape the terrain" vs "place an attractor" — DIFF | "shape the terrain" vs "fill the sandpile" — DIFF | DIFF | DIFF |

No prior shares 3+ dimensions on the heavy axes (6, 7, 8). The
shared dimensions are universal-trivial (step counter, click input,
pawn-to-target goal, walls). Pass.

## Verdict
NOVEL. Proceed to `write_spec` with game ID `vd3g` and family
`valley-dig-roll`.
