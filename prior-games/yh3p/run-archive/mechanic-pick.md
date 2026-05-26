# mechanic-pick — yh3p (vine-branch-bloom)

## 1. Game ID
`yh3p` — verified absent from the 25 reference IDs and from
`prior-games/index.md` (66 prior entries scanned). 4 lowercase
alphanumeric characters, not a recognisable English word.

## 2. Mechanic family tag
`vine-branch-bloom`

## 3. One-paragraph mechanic description

The player nurses a single rooted vine across the playfield. Arrow
keys (ACTION1/2/3/4) extend the vine's active glowing tip one cell
in that direction; the cell the tip leaves becomes a permanent
green stalk segment, and growth into walls or onto existing vine is
blocked. ACTION6 (click any existing stalk segment or the root)
**re-anchors the active tip to that cell**, so the next arrow press
sprouts a new branch from there — the vine grows as a tree, not a
single path. ACTION5 **blooms** the active tip into a permanent
flower if and only if the tip is currently sitting on a target
flower-bud cell *and* the tip's "facing" (the direction of its most
recent extending arrow press, shown by the asymmetric tear-drop
silhouette of the tip sprite) matches the target's notch — each
bud has one open petal-side and the vine must arrive into that
side. Targets that bloom successfully turn solid; targets blooming
without a notch match (or without a bud underneath) do nothing and
the action consumes no step. The level wins when every bud has
bloomed before the step counter drains. Levels add mechanics: L1
introduces extend-tip on a single bud, L2 adds click-to-rebranch
across walls, L3 adds the directional bloom-commit so blossoming
order and approach direction now both matter.

## 4. Core-knowledge prior coverage

Drawn from the four allowed §3.4 categories:

- **Objectness** — vine cells are persistent, additive entities;
  walls and buds are persistent objects.
- **Basic geometry & topology** — the vine forms a *tree* (no
  cycles, branches sprout from a chosen cell); reachability under
  the no-cross rule is a topological constraint. The L3 notch-
  direction match is rotational geometry.
- **Basic physics** — minimal; growth is one-cell-per-action with
  no momentum.
- **Agentness** — none. No NPCs, no autonomous motion. Pure
  player-driven growth.

(Pairs objectness + topology + light geometry — the same family as
several reference games but with a verb structure no reference game
uses.)

## 5. Action subset

`available_actions=[1, 2, 3, 4, 5, 6]`. ACTION7 is omitted (no undo
verb); per `action-enum.md` § Slot 7 is strict-undo, the slot must
be absent rather than overloaded with a non-undo verb. ACTION5
carries the distinctive "bloom" verb (the freedom-slot verb, where
novelty lives). ACTION6 is "click stalk to re-anchor tip".

## 6. Similarity check vs the 25-game taxonomy

Walked every row of `taxonomy-of-25-games.md`. Family-level tag
overlap (per `similarity-check.md` § 1) found ZERO matches —
"vine-branch-bloom" shares no first-two-words after hyphen-split
with any taxonomy entry. The closest description-level near-misses,
each with concrete distinguishing rule:

- **sk48 paired-snake-trail** — two heads with mirrored bodies, the
  level wins when their colour-trails match cell-by-cell. Both
  involve "arrow growth leaves a permanent trail". Distinguishing:
  sk48 has *two heads in lockstep mirroring* and the win condition
  is *trail-colour parity between head-pairs*; yh3p has a single
  rooted vine that *branches* (one root, many tips reachable via
  click-rebranch) and the win condition is *covering and blooming
  every bud*. sk48 has no branching; yh3p has no mirror coupling.
- **tn36 program-pawn-trace** — click-program a path-tracing
  programme via instruction buttons. Both end with "the player's
  trace must hit certain cells". Distinguishing: tn36 is a
  *deferred-execution programme* assembled with click; yh3p is
  *direct-manipulation* incremental growth via arrows; tn36 has no
  branching topology, yh3p has explicit click-to-rebranch.
- **ls20 cycler-attribute-match** — pawn collects shape-coloured
  pellets in sequence with cyclers along the way. Both involve
  arrow movement to targets. Distinguishing: ls20 has a *single
  walking pawn* whose state mutates via cycle-tiles; yh3p has a
  *growing tree* whose tip moves but leaves a permanent stalk. ls20
  has no trail, no branching, and uses attribute-match (shape /
  colour / rotation triplet) instead of approach-direction-match.
- **wa30 carry-pickup-drop** — single carrier walks, picks up
  passengers, drops on destinations. Both have arrow movement +
  ACTION5 commit-verb. Distinguishing: wa30's commit is *pick-up /
  drop* of a separate movable sprite; yh3p's commit is *bloom* of
  the active tip on a same-cell bud with directional matching, and
  the moving entity itself (the vine) is permanent. No carry, no
  drop, no separate-sprite tether in yh3p.

## 7. Similarity check vs `prior-games/index.md`

Walked every prior. Detailed near-miss analysis:

- **ek73 wake-trail-evade** — avatar walks; vacated cells become
  decaying hazards. SHARED: arrow-walk + leaves-trail.
  DISTINGUISHING: ek73's trail is a *decaying hazard the player
  must avoid*; yh3p's stalk is a *permanent helpful structure the
  player keeps building on*. ek73 has no branching, no commit verb,
  no targets-with-direction. The core dynamic is opposite — ek73 is
  evade-your-trail, yh3p is grow-using-your-trail.
- **jd4q echo-trail-teleport** — avatar walks, leaves fading
  echoes, click teleports back consuming trail. SHARED: arrow-walk
  + trail. DISTINGUISHING: jd4q's click *consumes-and-teleports*;
  yh3p's click *re-anchors-the-active-tip-to-an-existing-cell*. No
  teleport in yh3p; jd4q has no branching topology, no commit verb.
- **bw7k actor-replay-shade** — actor walks; coloured anchors spawn
  shades that replay the actor's recent path. SHARED: arrow-walk +
  leaves-trail. DISTINGUISHING: bw7k's trail spawns *autonomous
  ghost replayers*; yh3p has *no autonomous motion* — the vine is
  static once placed. bw7k's verb is anchor-step-to-spawn-replay;
  yh3p's verbs are click-to-rebranch and bloom-commit.
- **tj4n walk-trail-loop-enclose** — walk a single closed loop;
  enclosure captures interior targets. SHARED: arrow-walk + trail.
  DISTINGUISHING: tj4n requires the trail to *form a closed
  loop*, and the win predicate is *interior-enclosure*; yh3p
  forbids self-cross and never closes loops (it's a tree). yh3p's
  win is *per-target bloom-commit with direction-match*, not
  enclosure.
- **sk48 paired-snake-trail** (also in taxonomy, repeated for
  completeness) — see above.
- **jx5k constellation-edge-link** — pair-click coloured nodes to
  build a multigraph satisfying degree targets. SHARED: builds a
  graph-like structure. DISTINGUISHING: jx5k uses *pair-click on
  pre-placed nodes*; yh3p uses *arrow-growth from a single root*.
  jx5k's edges are abstract straight-line links; yh3p's stalks are
  cell-by-cell grown segments. jx5k allows multigraph cycles; yh3p
  enforces tree topology by no-cross.
- **wb6n tether-pin-wrap** — pawn on fixed-length leash to a stake;
  ACTION5 plants pins to re-anchor the rope. SHARED: ACTION5
  changes the geometry of a structure rooted at a fixed point.
  DISTINGUISHING: wb6n's structure is a *stretchy single-segment
  rope* and the verb is *plant a re-anchor pin*; yh3p's structure
  is a *grown tree of permanent cells* and the verb is *bloom a
  tip on a target*.
- **ds5q wall-erode-chain** — avatar walks 8-pixel hops, chips
  same-colour walls at coloured pads. SHARED: arrow movement +
  state change in the world. DISTINGUISHING: ds5q is *destroy walls
  to make passable*; yh3p is *grow stalk to fill cells*. Opposite
  direction of state change.
- **fz5j phase-step-tile** — avatar walks tiles that pulse
  open/closed on per-cell periods. SHARED: avatar moves on a grid.
  DISTINGUISHING: fz5j has *time-varying gates* the avatar passes
  through; yh3p has *static walls* and the player builds a
  permanent vine.
- **lt7m ell-jump-tour-block** — click an L-shape-reachable cell to
  jump; visit all targets. SHARED: visit all targets. DISTINGUISHING:
  lt7m is *click-jumping in chess-knight L-shapes*; yh3p is
  *cell-by-cell arrow growth with branching*. lt7m has no growing
  trail; yh3p has no jumping.

No prior shares 3+ dimensions per the negative-similarity-check.

## 8. Negative-similarity check (per `negative-similarity-check.md`)

Mentally rendered yh3p L1 (small green-bulb root, growing
yellow-tipped vine, single notched-rim flower target on light-grey
playfield, walls in dark grey, step bar at top in 7=pink) and
walked the 8 dimensions against the closest priors.

| Dimension | yh3p | ek73 | jd4q | bw7k | tj4n | jx5k |
|---|---|---|---|---|---|---|
| 1. What's on the board | grown vine + flowers + walls | avatar + decaying hazards + walls | avatar + echoes + doors | actor + colour anchors + shades | avatar + closed loop + inner targets | pre-placed coloured nodes + edges |
| 2. What player does | extend-tip + click-rebranch + bloom | walks + uses clearer pads | walks + clicks teleport | walks + steps on anchors | walks a closed loop | pair-clicks nodes |
| 3. What level asks | bloom every bud (notch-matched) | reach goal avoiding own wake | reach goal | reach goal with shade | enclose targets in loop | satisfy node-degree targets |
| 4. What kills | step counter | step counter + own wake | step counter + closing doors | step counter | step counter + pursuer | step counter |
| 5. Cast of supports | walls, notched buds, root | wake-erasers, warp pads | doors, eraser, echoes | colour anchors | pursuer at L3 | nodes, edges |
| 6. Visual signature | green-vine + multicolor blossoms on grey | grey-walked-cell hazards on dark | echo-fade trail | shade ghosts | closed loop trace | thin colour segments graph |
| 7. Pixel grain | bulb + segmented stalk + petal-rings | block avatar + filled cells | block avatar | block avatar | block avatar | thin lines |
| 8. Core dynamic | grow-tree-then-bloom | evade-own-wake | walk-and-rewind | walk-and-replay | trace-and-enclose | choose-edges-to-add |

Maximum overlap with any single prior: 2 dimensions (ek73 / jd4q
share dim 2 partial — arrow walking — and dim 4 step counter, which
is universal). Below the 3-dimension reject threshold.

The three named principles also pass:

- **Pixel-detail richness** — primary sprites have internal
  pattern: root is a 5×5 segmented bulb with hatching, stalk
  segments are 3×3 with vertical-stripe internal pattern, blossoms
  are 5×5 ring-of-petals with notched hollow centre, walls are
  patterned blocks. No bare 1×1 pawns.
- **Palette diversity** — dominant palette is `{2 light-grey
  background, 4 wall, 14 green stalk, 11 yellow tip, 6 magenta
  bloom, 12 orange bud, 7 pink HUD}`. Green-stalk + magenta-bloom
  is not the dominant signature of any prior in the index (kf42-
  era `{4,8,9}` palette pattern is avoided).
- **Core dynamic divergence** — "build a tree of growth and
  selectively commit terminal cells with directional matching"
  does not appear in any prior. Nearest neighbour is the
  walk-and-leave-trail family (ek73/jd4q/bw7k/tj4n) but those
  treat the trail as either hazard, history, or boundary; none
  treat it as a *constructive substrate* the player can re-anchor
  on.

## 9. ID collision check

Ran `grep yh3p` against both
`skills/code/id-generation.md` (reserved 25-list) and
`prior-games/index.md`. Zero hits. ID `yh3p` is free.

## 10. Verdict

**NOVEL.** Proceeding to `write_spec` with mechanic-family =
`vine-branch-bloom`, game id = `yh3p`.
