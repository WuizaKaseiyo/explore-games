# mechanic-pick — Run #01

## Game ID
`kf42`

Generation procedure (per `code/id-generation.md`): random 2-letter
prefix `kf` + random 2-digit suffix `42`; checked against the
reserved 25 reference IDs (`ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59
lf52 lp85 ls20 m0r0 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36
tr87 tu93 vc33 wa30`) — no collision; checked against
`prior-games/index.md` — that file was created header-only at the
start of this state (it did not previously exist on disk), so no
collision is possible. `kf42` is not a recognisable English word.

## Mechanic family tag
`tether-pawn-cycle`

## Seed (one-line user input)
empty — autonomous mode.

## One-paragraph description
Two coloured pawns share a fixed-maximum tether (Chebyshev distance
≤ L cells, level-specific). The player clicks one pawn to make it
"active"; arrow keys step the active pawn one cell. The inactive
pawn does not move on its own — but if a step by the active pawn
would stretch the tether past length L, the inactive pawn is dragged
one cell along the line that minimises tether strain (toward the
active pawn). Walls of the maze cancel either move. From level 2
onward, walking the active pawn onto a coloured cycler-pad cycles
that pawn's body colour one notch through a fixed three-colour
alphabet (red → yellow → blue → red), affecting only the pawn that
stepped on it. The level is solved when each pawn simultaneously
sits on a target pad whose colour matches that pawn's *current*
body colour. Priors used: **objectness** (two persistent pawns +
target pads), **basic geometry & topology** (Chebyshev-distance
constraint, walls of the maze define connectivity / slack-region),
**basic physics** (the tether's maximum-length constraint
propagates a drag impulse), and **agentness** *not* used (the
inactive pawn is purely reactive — no autonomous goal-seeking).

## Novelty check (per `mechanic-novelty/similarity-check.md`)

### Against `taxonomy-of-25-games.md`

Family-level near-misses are entries whose family tag overlaps any
of the words `tether`, `pair`, `cycle`, `pawn`, plus broader
"two-coupled-things" candidates. Four taxonomy rows escalate to the
description-level check:

#### Near-miss 1: `m0r0` — `mirror-orb-merge`
Read both `taxonomy-of-25-games.md` row and the deep-analysis
(plus the source, which I read in full during `study`). Win
condition: each mirrored pair walks into the same cell and merges.
Primary action: pressing UP moves *both* pawns up; pressing LEFT
moves one left while pulling the other right (a per-axis mirror
transform on every keypress). Primary constraint: walls + spike
tiles + post-stones.
**Distinguishing rule.** In `m0r0` *every* key affects *both*
pawns simultaneously through a fixed mirror transform, with no
notion of "active" pawn — the two are always coupled-rigid. In
`kf42` only the *active* pawn moves on a key; the inactive pawn
is decoupled and reactive — it moves *only* when the
maximum-distance tether would otherwise be exceeded. The win
predicate also differs: `m0r0` requires the two pawns to occupy
the *same* cell (merge); `kf42` requires them to occupy *different*
cells, each matching its colour-pad target.

#### Near-miss 2: `r11l` — `centroid-puppet-leg`
Win condition: every pink-eyed ring sits inside its same-coloured
target ring. Primary action: click a footprint, click a
destination — the footprint is dragged across a corridor and
slides the centroid ring with it. Primary constraint: corridor
walls + cyan no-go zones + 5-strike hazard tolerance + step
budget.
**Distinguishing rule.** `r11l` couples objects through their
*centroid* (the ring tracks the average position of the legs);
`kf42` couples through a *maximum-distance constraint* (the
inactive pawn is unaffected until the constraint binds). `r11l`
has three or four legs per ring with a centred virtual ring that
the level scores; `kf42` has exactly two physical pawns and no
virtual sprite. `r11l`'s motion is click-to-drag (one footprint
slides across the corridor in a single action); `kf42`'s motion
is one cell per arrow press. The win predicate scopes differ:
"each ring inside its target ring" (a containment relation
between virtual and concrete sprites) vs. "each pawn on its
colour-matched target pad" (an equality relation between two
physical sprite positions and a colour predicate).

#### Near-miss 3: `sk48` — `paired-snake-trail`
Win condition: every segment of one snake covers a tile whose
colour matches the corresponding segment-tile of the other snake.
Primary action: arrows grow or retract the active snake's body
one segment at a time; click switches active snake; perpendicular
keys shimmy the body sideways past an anchor stone.
**Distinguishing rule.** `sk48` is a snake-growth puzzle: the
"pair" is two whole bodies of arbitrary length that PHYSICALLY
TILE the floor; the win is a positional colour-match between
corresponding *segments*. `kf42` is a two-point puzzle: each
pawn is a single cell; nothing extends; the tether is invisible
geometry, not occupied tiles. The action effect differs in kind:
sk48 changes a snake's *length* on every press; kf42 changes a
pawn's *position* by one cell on every press. The win predicates
are unrelated.

#### Near-miss 4: `ls20` — `cycler-attribute-match`
The closest taxonomy match for kf42's L2 colour-cycle pad sub-
mechanic. Win condition: the avatar's shape-colour-rotation
triplet matches the target imprinted on the goal pad. Primary
action: arrows step a single avatar in five-pixel hops; cycler
tiles cycle the avatar's shape OR hue OR rotation by one notch.
Primary constraint: maze walls + step budget + life count + goal
predicate over a triplet.
**Distinguishing rule.** `ls20` has a *single* avatar and a *triplet*
predicate (shape × colour × rotation, all on the same avatar) —
the puzzle is "navigate the same actor through the right
sequence of cyclers". `kf42` has *two* avatars under a tether
constraint and a *pair-of-equalities* predicate (each pawn's
colour matches its colour-pad's colour, simultaneously) — the
puzzle is "coordinate two avatars while keeping a pair of colour
identities aligned". The colour-cycler sub-mechanic in L2 of
kf42 is a means to an end (you may need to swap which pawn
matches which target), not the central mechanic. ls20 has no
tether; kf42 has no shape or rotation cycling; kf42's "active
selector via click" is absent in ls20 (which uses only arrows).

### Against `prior-games/index.md`
Empty (header-only) — `prior-games/index.md` was created by this
state because the file did not previously exist on disk. Per
`prior-games-index-format.md`'s "Initial state" clause, the
similarity check against prior-games trivially passes.

### Verdict
**NOVEL.** No taxonomy row matches all three of (win condition,
primary action, primary constraint). The four near-misses each
fail on at least one axis as articulated above. Prior-games index
is empty. The mechanic-family tag is fresh.
