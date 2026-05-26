# Mechanic pick

## Game ID
`qy7w`

(Verified opaque — no English meaning. Not in 25-game reserved list. Not in
`prior-games/index.md` (66 tracked rows) or untracked dirs gh4r/hp9c/lz7q/
qd6n/tc8s/tx4q/vk6m/vw3p/xv4n.)

## Mechanic-family tag
`strand-twist-permute`

## One-paragraph description

Several vertical coloured strands run from a row of START caps at the top of the
playfield down to a row of END slots at the bottom. Between consecutive vertical
levels there are CROSSING markers that connect two adjacent strand columns; each
crossing is in one of two visual states: PASS (strands go straight through) or
TWIST (strands swap columns at that crossing, rendered as an explicit X with one
strand visibly going over). Clicking a crossing toggles its state. Each strand's
actual rendered path is recomputed live: starting from its top cap, it descends
column-by-column, and at every TWIST it crosses to the adjacent column; at PASS
it stays in its current column. The level wins when each strand's bottom endpoint
sits in the END slot whose colour matches its top cap. Action palette: ACTION6
only (click a crossing). Mechanics layered across L1→L3 are: (1) the basic
twist-toggle that permutes strand endpoints; (2) LOCK markers on certain crossings
that freeze them until a strand of a particular colour passes through a separate
KEY tile elsewhere on the board; (3) COLOUR-SHIFT cells embedded mid-strand that
remap a strand's colour for the segment below them, so the win predicate compares
each END slot's colour against the *bottom-segment* colour of the strand resting
on it.

## Core-knowledge prior categories used

- **Basic geometry & topology** — primary. The mechanic is fundamentally about
  permutations and threading. The over/under visual at twists is a topology cue
  (strand A goes "over" B); the routing is a strict permutation operation.
- **Objectness** — strands and crossings are persistent entities the player
  manipulates.
- **Basic physics** — secondary, only for the colour-shift cell at L3 (a strand
  "carries" colour past a junction in one direction, like a fluid passing
  through a dye station).

## Action mapping (preview)

- ACTION6: click a CROSSING marker to toggle PASS/TWIST.
  (At L2 some crossings are LOCKED and a click is rejected silently with a brief
  visual flash; the rejection itself is part of the discovery channel.)
- (No ACTION5, no arrow keys, no ACTION7. `available_actions=[6]`.)

## Similarity check vs taxonomy of 25

Walked every row in `taxonomy-of-25-games.md`. The candidate's family-level
tag `strand-twist-permute` shares no first-two-words prefix with any taxonomy
row. Description-level analysis identifies the closest near-misses:

- **vc33 — row-column-swap-stripe.** WIN: stones over matching colour slots.
  PRIMARY ACTION: click a marker that swaps neighbour stone groups across it.
  Distinguishing rule: vc33 swaps *stripes of stones* across a marker that
  sits between two rail neighbour groups; the swap is a one-shot rearrangement
  on the single row/column the marker lives on. **qy7w never moves stones**:
  the strands are continuous lines whose entire route below a crossing
  changes when that crossing toggles, propagating the consequence through
  every later crossing the rerouted strand encounters. The "swap" in qy7w is
  a permutation generator σ_i acting on the cumulative permutation; in vc33
  it is a one-shot stone reshuffle. Visual signature also diverges (vc33 is
  horizontal stripes of stones flanked by rails; qy7w is vertical parallel
  strands with X markers).

- **lp85 — row-col-shift-grid.** WIN: every key sprite over a goal sprite.
  PRIMARY ACTION: click a button outside the grid; clicking applies a fixed
  per-button permutation on the cell sprites. Distinguishing rule: lp85's
  buttons are *outside* the grid and each encodes a per-button level-tabulated
  permutation table that swaps cell *positions*; qy7w's crossings are *on* the
  grid and each encodes a single fixed adjacent-column transposition that
  composes deterministically with every other crossing's state. Lp85 is
  "click a button to apply a saved permutation"; qy7w is "click a crossing
  *in the routing graph itself* to add or remove a single elementary
  transposition". Visual is also unrelated (lp85 has many buttons around a
  small cell grid; qy7w has none).

- **cn04 — rotate-translate-jigsaw.** Different action verb (move/rotate vs
  click-toggle); different win (boundary-pixel coincidence vs end-slot colour
  match). No real overlap.

- **tn36 — program-shape-buttons.** Different — tn36 builds a tape of opcodes
  that morph a single shape; qy7w has no instruction tape, no morphing.

- **sk48 — paired-trail-match.** Different — sk48 walks heads, paints trails,
  matches paired trails colour-by-colour. No strand crossings.

- **r11l — tethered-throw-placement.** Different — leg/head centroid throw.

No taxonomy entry shares the candidate's WIN + PRIMARY ACTION + PRIMARY
CONSTRAINT triple. NOVEL vs taxonomy.

## Similarity check vs prior-games corpus

Walked every row in `prior-games/index.md` (66 entries) plus the 9 untracked
dirs (gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n) by reading their
metadata. Closest near-misses:

- **lp85 already covered above** (reference, not prior).

- **jx5k — constellation-edge-link.** WIN: per-node target degrees met by
  pair-clicked edges; PRIMARY ACTION: pair-click coloured nodes to add edges.
  Distinguishing rule: jx5k builds a graph from scratch by adding edges; qy7w
  *toggles* a fixed pre-placed crossing between two adjacent existing
  strand columns — there is no graph construction, just permutation
  generators, and the strands always exist. Different "what is on the board"
  (4 floating crystal nodes vs vertical parallel strand bundle).

- **vy3k — region-swap-arrange.** WIN: avatar in target quadrant + objects
  arranged. PRIMARY ACTION: click+ACTION5 to swap or rotate quadrants.
  Distinguishing rule: vy3k swaps *2D quadrants of the playfield itself*;
  qy7w toggles single elementary transpositions between *two columns of
  strands*. The "what permutes" is fundamentally different (whole regions
  vs individual strands), and qy7w has no avatar.

- **mz6t — majority-vote-stabilize.** Click cells to cycle states; ACTION5
  ticks majority vote. Different — qy7w has no cellular automaton, no
  voting, no global tick.

- **qf8m — rook-cross-toggle.** Click flips a (2N-1)-cell row+col cross.
  Different mechanism — qf8m operates on a single 2D grid via cross-
  pattern toggles; qy7w operates on a 1D sequence of permutation
  generators acting on N strand columns.

- **gx7m — gear-mesh-cascade.** Rotation propagation across cardinal mesh.
  Different — no rotations in qy7w.

- **rk7x — live-switch-routing.** Toggle junction blades to route an
  autonomous courier. Distinguishing rule: rk7x has *one* mobile entity
  routed through a network of junctions, each junction picks one outgoing
  direction; qy7w has *N* strands simultaneously, each crossing is a
  binary swap-or-not between *two specific strands*, and the routing is
  computed in one pass top-to-bottom. Surface signature also distinct
  (rk7x has a maze with a courier-pawn; qy7w has parallel vertical lines
  with no avatar).

- **lp85, vc33** would also be in the prior-games novelty corner if they
  were prior-game entries — already covered above.

No prior-game entry shares the candidate's full triple. NOVEL vs prior-games.

## Negative similarity check (per `negative-similarity-check.md`)

Walked the 8 dimensions against the most-likely-overlapping priors and ref
games (vc33, lp85, jx5k, qf8m, mz6t, rk7x). Mental L1 render: a 64×64 frame
with three vertical 2-pixel-wide coloured strand-bars from y≈4 down to y≈58,
in palette colours {8 red, 9 blue, 11 yellow}; two crossing-X markers at
y≈22 and y≈38, each marker a 4×4 sprite with a clear "X" pattern in palette
{3 grey, 5 black}. Top has a row of small coloured caps; bottom has 3 small
coloured slots. Step-counter HUD at row 0 or 63.

Compared dimensions vs each likely-overlap prior:

| Prior   | (1) board | (2) input | (3) goal | (4) lose | (5) cast | (6) palette | (7) grain | (8) dynamic |
|---------|-----------|-----------|----------|----------|----------|-------------|-----------|-------------|
| vc33    | NO (vertical lines vs horizontal stripes) | NO (click crossing vs click marker) | partial (colour-match goal — generic) | YES (step counter, universal) | NO (strands vs stones+rails) | NO ({8,9,11,3,5} vs vc33's palette) | NO (2-pixel strands+X vs 6-pixel stones) | NO (permute strands vs swap stones) |
| lp85    | NO | partial (click) | partial (colour-match) | YES | NO | NO | NO | NO |
| jx5k    | NO | partial (click) | NO | YES | NO | NO | NO | NO |
| qf8m    | NO (1D vs 2D grid) | partial (click) | NO | YES | NO | NO | NO | NO (permutation vs cell flip) |
| mz6t    | NO | partial (click) | NO | YES | NO | NO | NO | NO |
| rk7x    | NO (parallel lines vs maze with courier) | partial (click) | partial (terminal) | YES | NO | NO | NO | NO (multi-strand permute vs single-courier route) |

No prior shares 3+ named dimensions. The strongest overlap is vc33 on
"colour-match win condition" + "click to permute" — only 2 of 8, and the
visual signature (dimension 6+7) and core dynamic (dimension 8) are fully
different.

PASSES negative similarity check.

## Vs preexisting video games (manual axis)

Braid puzzles exist in academic mathematics and a handful of indie puzzlers
(e.g. "Knot Puzzle" mobile apps). None of these are mainstream video games
and the qy7w execution — toggling pre-placed crossings to produce a target
endpoint permutation, with composition-layer locks and colour-shift cells —
is its own concrete realisation. The §3.4 manual-novelty bar is "avoid
similarities with existing games"; braid mathematics being public is not the
same as a popular video game with this mechanic. The user is the final
arbiter on this axis, but the candidate is not a clone of any major game I
am aware of.
