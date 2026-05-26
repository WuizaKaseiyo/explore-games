# Mechanic pick

## Game ID

`mw8p`

ID-generation check (per `code/id-generation.md`):
- 4 lowercase alphanumeric characters.
- Not an English word.
- Not in the 25 reference IDs (ar25, bp35, cd82, cn04, dc22, ft09, g50t,
  ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80,
  su15, tn36, tr87, tu93, vc33, wa30).
- Not in `prior-games/index.md` (verified by grep against all 80 prior
  rows, and against the in-progress prior-games directories: bw7k, bx84,
  bz3k, cv5b, dj5h, ds5q, ek73, fw8c, fz5j, gh4r, gv47, gx7m, hk7v, hl4n,
  hp9c, hr8q, jd4q, jx5k, kf42, kj82, kn58, kp9z, kv8w, kw8t, kx14, lq5x,
  lt7m, lv4k, lz7q, mr5q, mz6t, nb6t, nf3z, ng52, nh4w, nz3v, pf3w, pj7k,
  pk4m, pn5d, pq5w, pv5q, pz4t, qb84, qd6n, qf8m, qj4r, qm4t, qn7w, qx7p,
  qy7w, qz73, rj5w, rk7x, rs8n, rt9k, tc8s, tg6w, tj4n, tk6n, tm5x, tx4q,
  vd3g, vk6m, vp6h, vt6q, vw3p, vy3k, wb6n, wj7d, wm6q, wq3m, wt39, xn5p,
  xv2b, xv4n, xz5g, yh3p, zd7m, zk9p, zw91).

## Run input

Autonomous run — no user seed.

## Mechanic family tag

`predator-prey-triangle`

## One-paragraph description

The player controls a single A-creature that walks the cardinal grid
(arrows). Two other species share the playfield: B-creatures pursue A
one cell per turn along their dominant Manhattan axis and remove A if
they end up cardinal-adjacent (lose); C-creatures pursue the nearest B
one cell per turn along their dominant Manhattan axis and *remove the
B* the instant they end up cardinal-adjacent. The triangle closes
because the A-creature *consumes* a C-creature when A walks onto the
C's cell — C vanishes, A occupies the cell. The avatar otherwise
cannot step on a B-cell (B kills it) or pass through walls. Every
level is a small bounded chamber: A starts in one region, the exit
cell sits in another, B's stand between A and the exit, and C's are
the only tool that can clear B's from blocking cells. The puzzle is
to orchestrate the C-population (which species the player both
recruits and consumes) so that C's drift onto the B's that block A's
shortest path before A is itself caught. The game uses no on-screen
text and the role of each species is communicated entirely through
sprite shape + colour and the visible deaths during the first few
exploratory moves.

Priors drawn (per `core-knowledge-priors.md`):
- **Objectness** — every creature and wall is a persistent entity
  with position and removal-on-event behaviour.
- **Agentness** — B-creatures pursue A with a deterministic chase
  policy and C-creatures pursue B's with the same policy; the
  player must reason about the goal-directed behaviour of other
  agents.

(No physics or geometry/topology beyond grid-cardinal movement —
this game leans hard on the agentness prior, which is one of the
less-explored corners of the four priors per
`conventions/reference-game-patterns.md` § Open questions.)

## Similarity check — taxonomy

Comparison against the 25 rows of
`mechanic-novelty/taxonomy-of-25-games.md`. For every near-miss
flagged below, the deeper view at
`deep-analysis-3lvls/<id>/<id>-deep-analysis.md`
and the `mechanism-details/<id>.md` summary were re-consulted.

### tu93 — maze-pickup-train

> "A 3-cell-tall pawn hops three pixels at a time along value-2
> corridors carved into a maze-shaped tile; coloured arrows it
> walks past either fall in step behind it like ducklings, march
> one corridor-cell every turn on their own purple-clockwork, or
> wait dormant until brushed red; lead the whole train onto the
> goal-marker tile."

**Distinguishing rule.** tu93's secondary species (the bouncer, the
rotator, the dormant-then-active pickup) move per their own
INDEPENDENT tick rules; none preys on or eliminates another. The
player's goal is to **collect** the train onto a single tile. mw8p's
core dynamic is the **cyclic three-way predation** (A eats C, B eats
A, C eats B) — the secondary species are not collectibles but
players in a rock-paper-scissors loop whose interactions remove each
other. mw8p's win condition is "A reaches a goal cell unaccompanied",
not "every secondary lands on the goal".

### ka59 — sokoban-explode-chase

> "Click switches the active pawn among coloured pawns scattered in
> a walled arena; arrows slide the active pawn three cells and
> recursively push other pawns; explode-tiles spray neighbouring
> pawns outward; a chaser shuffles toward the active pawn each turn;
> cover every coloured target square."

**Distinguishing rule.** ka59 is *sokoban-and-detonate* with a single
generic chaser. mw8p has no pushing, no detonation, no
target-cell-covering, no pawn-selection (the player only ever
controls A). The chaser-mechanic is shared in spirit (a hostile
auto-mover catches the player on adjacency), but ka59 has *one*
generic chaser whose role is to add pressure; mw8p has *two
interacting species* whose mutual predation is the puzzle.

### m0r0 — mirrored-quad-control

> "Four avatars are placed on the board ... A single direction press
> moves all four simultaneously, but each one's axes are sign-flipped
> relative to the canonical (top-left) direction ... bring pairs of
> avatars onto the same cell (they merge and become intangible)."

**Distinguishing rule.** m0r0 has a single player controlling four
co-moving avatars with sign-flipped axes; mw8p has a single player
controlling ONE avatar (A), and two species of NPCs that move
autonomously. m0r0's win condition is pair-merger of player-
controlled avatars; mw8p's win is the SOLE player avatar reaching an
exit cell. No mirroring, no co-movement.

## Similarity check — prior-games index

The prior-games index has 80 rows. Walked every row; the meaningful
near-misses are flagged below. (Skipped: 75+ priors whose mechanic
family is unrelated — beam mirrors, fold-mirror, vessel-equalise,
lever-balance, gear-mesh, fluid-flow, etc.)

### zk9p — pursuer-merge-walk

> "walk an avatar to lure autonomous AI pursuers into self-
> collisions; merged pursuers vanish; level wins when none remain."

This is the closest prior in the corpus. Walking the eight-dimension
negative-similarity check (`negative-similarity-check.md`):

| Dim | zk9p | mw8p | Shared? |
|---|---|---|---|
| 1 What is on the board | avatar + autonomous pursuers + walls | avatar + autonomous B's + autonomous C's + walls | **yes (coarse)** |
| 2 Player physical input | arrow-walk only | arrow-walk only | **yes** |
| 3 Level goal | clear every pursuer | reach an exit cell as A | **NO** (different win condition) |
| 4 Lose | pursuer reaches you | B reaches A | **yes (dynamic)** |
| 5 Supporting cast | walls + pursuers | walls + B's + C's + exit | **yes (similar)** |
| 6 Visible visual signature | (to be diverged — see below) | (to be diverged) | NO |
| 7 Pixel grain of primary sprites | (to be diverged) | (to be diverged) | NO |
| 8 Core dynamic | lure same-species pursuers into self-collisions to remove them | use third species C as a tool that eliminates B's on adjacency, while A separately consumes C's it walks onto | **NO** (substantively different) |

Coarse-axis shared count: 4 (D1, D2, D4, D5). All four are LOW-weight
dimensions per `negative-similarity-check.md`'s explicit ranking
(*"sharing on dimensions 6, 7, or 8 is heavier than sharing on the
others, because those are the named principles"*). All three high-
weight principle dimensions (D6, D7, D8) DIVERGE, and the level goal
(D3) also diverges.

**Distinguishing rule.** zk9p's pursuers cancel out by colliding with
*each other* (one species, self-collision). mw8p has *three* species
in a directed predation cycle: only the C-species cancels B's, and
the player simultaneously consumes C's (the consumed-C count is a
resource the puzzle uses against the player). zk9p has no eat-by-
walking mechanic. The puzzle texture is fundamentally different — zk9p
asks "where do I stand so two pursuers walk into each other?"; mw8p
asks "how do I orchestrate the C-population to clear B's I can't
walk past, while keeping enough C's alive to finish the work?".

**Concrete divergence plan on D6 (palette) and D7 (pixel grain).**
- D6 palette: zk9p's prior render uses (yellow + black + small
  accent). mw8p will use a distinctly different palette — base
  background palette-2 light-grey, walls palette-13 maroon, A in
  palette-10 light-blue with palette-4 outline + palette-11 yellow
  eye-pixels, B in palette-12 orange with palette-8 red rim, C in
  palette-14 green with palette-7 pink centre, exit cell palette-15
  purple with palette-0 white inset. No overlap with zk9p's
  dominant signature.
- D7 pixel grain: each creature sprite is 6×6 px with internal
  detail — A has 2 eye-pixels + outlined body; B has 4 spike
  perimeter pixels and a triangular maw motif; C has 4 leaf
  serrations and a central core dot. zk9p's pursuers (per the
  prior-game catalogue's reference-frames) are simpler solid shapes.

Per `negative-similarity-check.md` § decision rule: judgment is
warranted here. The candidate diverges on the three principle
dimensions (D6, D7, D8) and on the level-goal axis (D3); the four
shared coarse dimensions are the unavoidable consequence of *being
an avatar-on-grid game with autonomous-NPC opposition* (a generic
shape that zk9p, ka59, tu93, nf3z, wa30, ek73, jd4q, su15 all
share at this coarse level). Accept the candidate.

### nf3z — flock-flee-corral

> "shepherd avatar walks; flock NPCs flee away from shepherd along
> dominant Manhattan axis; ACTION5 toggles ATTRACT mode; lambs latch
> in matching-colour pens."

**Distinguishing rule.** nf3z's NPCs are uniformly *afraid* of the
shepherd; the shepherd ATTRACTS or REPELS the whole flock as one. There
is no inter-species predation. mw8p has no flock — the NPC populations
(B and C) interact with *each other* under the predation cycle, and
they relate to the avatar via a different rule each (B is predator of
A, C is consumed by A). There is no toggle of attract/repel; species
behaviour is fixed at design time.

### ek73 — wake-trail-evade

> "avatar walks one cell per arrow-press; vacated cells become decaying
> hazards behind the player; clearer pads erase wake; warp pads
> teleport in pairs."

**Distinguishing rule.** ek73's hazards are vacated-cell decay (self-
generated trail behind the player). mw8p's hazards are *moving NPCs*
(B-creatures that walk toward the player each turn). No trail
mechanic, no warp pads, no clearer pads.

### Other priors walked

The remaining 76 priors lie outside mw8p's mechanic family. The
broadest sweep: jd4q (echo-trail-teleport), bw7k (actor-replay-shade),
tu93-style multi-agent maze priors are absent from the prior-games
corpus; ka59 is in the taxonomy not the prior-games index. su15-style
recipe-collect priors are absent. lq5x lantern-cone-illuminate is
distinct (vision-based, not predation). nf3z is the only flock-style
prior; ek73, wt39, jd4q, bw7k all involve trails or wakes (different
from autonomous-NPC predation). Confirmed clear.

## Negative-similarity overall verdict

Per `negative-similarity-check.md` § application: walk the candidate's
mental rendering of L1 alongside the prior near-misses' rendered
frames. mw8p's L1 is a small 8-cell-stride playfield (10 cells across,
sprites 6×6 with internal detail) with palette-13 maroon walls,
palette-2 light-grey background, palette-10/12/14 creature trio. This
visual signature is distinct from zk9p's yellow-dominated trail field
(seen via prior-games image inspection) and from the taxonomy
near-misses' renders inspected during study. NOVEL.
