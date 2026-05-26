# Mechanic pick

## 4-character game ID

**hb5n**

Verified non-colliding: not in the 25 reference IDs (ar25, bp35, cd82,
cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5,
sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30) and not in
`prior-games/index.md` (81 indexed entries)
nor in the uncommitted prior-game directories (gh4r, hp9c, lz7q, qd6n,
tc8s, tx4q, vk6m, vw3p, xv4n). Opaque, lowercase, 4 chars, not a word.

## Mechanic family

**polyomino-walker-rotate** — an irregular-shape walking avatar (a
rigid polyomino) that translates with arrow keys and rotates 90°
clockwise about its anchor cell with ACTION5. The whole avatar moves
as a rigid body; the player must thread its footprint through gaps in
the maze that demand correct orientation.

## One-paragraph mechanic description

The player avatar is a connected L- or T-shaped polyomino (3-4 cells)
rendered in one bright primary colour with internal pixel detail. The
avatar's first cell is its **anchor** — the rotation centre and
position-of-record. Arrow keys translate the entire polyomino 1 cell
in their direction; the move is rejected if any non-anchor cell of
the polyomino would collide with a maze wall, an obstacle, or fall
off-grid. ACTION5 rotates the polyomino 90° clockwise about the
anchor cell (the anchor stays fixed; the other cells revolve); the
rotation is rejected if any post-rotation cell would collide. The
maze contains coloured narrow corridors and bends; the only way to
get a non-axially-aligned polyomino through a bend is to time a
rotation at the right cell. The level wins when the avatar's
silhouette occupies a target SLOT sprite whose dim outline matches
the avatar's current shape AND orientation. The mechanic is built
on the *geometry/topology* prior (rigid-body rotation, congruence,
fitting a shape through gaps) and the *objectness* prior (the
avatar as a coherent entity that moves and collides). Per-level
additions: L2 introduces **growth-pickups** (single-cell sprites
the avatar absorbs on contact, extending its polyomino by one cell
in a marked direction — the avatar's shape grows mid-level); L3
introduces **rotation-lock cells** (cells whose pattern indicates
ACTION5 is disabled while the anchor stands on them — the player
must move the anchor off the lock before rotating).

## Distinguishing rules — near-misses in the reference taxonomy

### vs cn04 (rotate-translate-jigsaw)
cn04 has the player CLICK-SELECT one of several jigsaw-piece sprites,
then translate/rotate the SELECTED piece with arrows/ACTION5; all
pieces sit on a flat board and the win is connector-snapping between
two pieces' boundaries. **hb5n has no selection model and no
multi-piece board** — there is exactly one polyomino (the avatar)
and it walks through a maze rather than being placed alongside
peers. The win is silhouette-match-at-target, not connector-snap
between pieces. No "8-connector" pixels, no two-piece adjacency
test. The maze walls (absent in cn04) are the load-bearing
constraint.

### vs ar25 (reflection-rotation-fit)
ar25 also has click-select-then-arrows-and-ACTION5, plus reflector
lines that mirror-copy the selected shape across an axis; the win
is mutual-boundary-match. **hb5n has no reflectors and no
mirror-copies.** The avatar is a single concrete instance with no
shadow / mirrored counterpart on the board. The maze + rotation +
slot-silhouette match is the only mechanic.

### vs tu93 (lockstep-multi-maze)
tu93 has primary agents that walk a maze constrained by a
walkable-underlay tag, with secondary species moving per their own
rules. **hb5n has a single avatar, no autonomous NPCs, no lockstep
multi-agent dynamic.** tu93's avatars are 1-cell or fixed-orientation
multi-cell pieces with no rotation verb; hb5n's avatar is a single
multi-cell polyomino with the rotation-around-anchor verb as the
distinguishing dynamic.

### vs sp80 / wa30 / many walkers
None of the 25 reference games' walking avatars rotate themselves
(ACTION5 in walking games is reserved for pour/commit/lock/cycle —
see `skills/global/action-enum.md`). hb5n is the first to make
ACTION5 = "rotate the avatar's body" rather than "rotate a piece I
selected".

## Distinguishing rules — near-misses in `prior-games/index.md`

### vs xv4n (cavity-nest-fit)
xv4n has the player click-lift irregular pieces and click-drop them
into matching cavities; ACTION5 rotates the *held* piece. The
verb-set is `{ACTION5, ACTION6}` — no walking, no avatar. **hb5n
has no lift/drop, no held-piece state, no clicks.** The verb-set is
`{ACTION1, ACTION2, ACTION3, ACTION4, ACTION5}` (cardinal walk +
rotate). The polyomino IS the player, not a thing the player
carries; it moves continuously through the maze. xv4n's shapes are
placed in cavities by teleportation; hb5n's avatar must thread
gaps step-by-step.

### vs zw91 (inflate-fit-burst)
zw91 has a single avatar whose footprint cycles three discrete sizes
(1×1, 2×2, 3×3 — all squares); ACTION5 grows/pushes/bursts; the goal
is fitting the avatar into a same-size socket. **hb5n's avatar is
an irregular L or T polyomino, not a square; ACTION5 rotates rather
than resizes; the avatar's shape does not cycle through a fixed
3-state size enum.** L2's growth-pickup is one-shot per pickup
sprite (the avatar grows by one cell with a specific orientation),
not a 1↔2↔3 cycle. The matching target is silhouette+orientation,
not size.

### vs nz3v (rotor-pivot-walk)
nz3v has a 2×2 SQUARE avatar straddling a wedge boundary, with
ACTION5 rotating the *wedge* (the world's lit sector), not the
avatar. **hb5n's avatar is irregular (not square), and ACTION5
rotates the AVATAR (rigid body), not the world.** No wedge, no
lives, no "must be in lit sector" predicate; the gating is purely
geometric (shape fits between walls or it doesn't).

### vs pz4t (anchor-pivot-place jigsaw)
pz4t has the player click a pixel on a coloured component to set
its placement anchor, then use arrows-reflect and ACTION5-rotate
to fit it into a dark-grey region. **pz4t has no walking** — the
component is placed by selection rather than physically traversing
the field. hb5n has no anchor-click verb and no flat-region tiling
goal; the avatar walks through a maze.

### vs nb6t (hinge-chain-reach)
nb6t has three rod-segments at independent hinges; rotate / extend /
cycle-active; carry-and-drop. **hb5n's avatar is a SINGLE rigid
polyomino, not a chain of hinged segments.** No hinge state, no
extend/retract, no per-segment selection. nb6t's articulated reach
deforms; hb5n's polyomino is rigid (rotates as a unit, never bends).

### vs lt7m (L-jump-tour-block)
lt7m has an L-SHAPED JUMP (knight-tour mechanic — pawn jumps in
L-patterns to reach targets). **hb5n's L-shape is the avatar's
BODY, not the avatar's MOVE shape.** lt7m's pawn is a single cell
that jumps in L-patterns; hb5n's avatar IS an L-shape that walks
1-cell-at-a-time. Completely different mechanic.

## Negative-similarity check (per `negative-similarity-check.md`)

Walked the 8 dimensions against the three closest priors (xv4n,
zw91, nz3v) and the two closest references (cn04, ar25). No single
prior overlaps on 3+ of the named principles. Specifically:

- **What's on the board**: a maze (walls + corridors) + a single
  multi-cell avatar + a target silhouette-slot. References cn04
  and ar25 have a flat board of jigsaw pieces, no maze.
  Priors xv4n and pz4t have a placement panel, no maze. zw91 has a
  pocket-grid with sockets, no maze. nz3v has a rotor + wedge,
  not a polyomino + maze.
- **What the player physically does**: walk + rotate-self. Most
  walking priors (kn58, jd4q, ek73, tj4n, tc8s, vk6m, pk4m, etc.)
  walk a 1-cell avatar with no rotation verb. Rotation-of-self is
  novel.
- **What the level asks for**: silhouette-and-orientation match
  at a target slot. Distinct from collect-targets (most priors),
  paint-canvas (re86, hl4n, fw8c), connect-network (jx5k, gx7m),
  fill-vessel (pn5d, xv2b, vw3p), thread (qy7w).
- **What kills the player**: step budget — universal.
- **Cast of supporting elements**: maze walls + growth pickups +
  rotation-lock cells + target slot. Combination is fresh.
- **Visual signature**: a single bold L-shape polyomino against a
  high-contrast maze (palette aimed at e.g. `{1 wall-grey, 8 red
  avatar, 14 green pickup, 4 lock-pattern, 0 background}` — not
  the over-used `{4 wall, 8 red, 9 blue}` signature).
- **Pixel grain of primary sprites**: avatar's body uses internal
  pattern (centre-dot, segmented colour bands) so the rotation
  state is legible from the static frame. Walls use a brick-like
  texture. Slot is a dim outline (palette 3) of the target
  silhouette.
- **Core dynamic**: "thread a rigid irregular shape through narrow
  gaps by rotating + walking". I have not found this dynamic in
  any of the 25 reference games or 90 prior games. The corpus
  rotates *selected pieces on a placement board* (cn04, ar25,
  s5i5, pz4t, xv4n, cd82) or rotates *the world / wedge / camera*
  (nz3v, sp80, xz5g) — never rotates *the walking avatar's own
  body*.

Verdict: NOVEL.
