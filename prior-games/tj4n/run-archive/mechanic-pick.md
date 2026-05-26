# Mechanic pick — `tj4n`

**4-character ID:** `tj4n` (non-colliding: not in 25 reference IDs, not in `prior-games/index.md`'s 45 entries; opaque non-word).

**Mechanic family:** `walk-trail-loop-enclose`

## One-paragraph description

A single avatar walks a 16×16-cell arena leaving a coloured "trail" cell on every cell it leaves. When the avatar steps back onto its own existing trail, the loop closes; every TARGET sprite whose centre lies strictly inside the closed polygon (Jordan-curve interior, ray-cast point-in-polygon) is captured (consumed and added to a per-colour tally), the trail clears, and the avatar continues from the closure cell. FORBIDDEN sprites enclosed by any closure cost a strike (3 strikes = lose). At L1 the goal is the simple "walk a loop around the targets" tutorial. L2 introduces a SECOND COLOUR of forbidden sprite the player must NEVER enclose, plus a SECOND COLOUR of target whose own forbidden-set differs — so closures must be small, sequential, and selective. L3 adds a single autonomous PURSUER sprite that walks one cell toward the avatar each turn — the pursuer counts as a third target colour the player must capture (lasso the pursuer in a closure) before it adjacent-attacks the avatar; AND, after each closure in L3, the closed-trail cells solidify into permanent walls, so loop ordering matters (small loops first, big loops impossible if walled).

## Action subset

`available_actions = [1, 2, 3, 4, 7]` — arrows step the avatar one cell; ACTION7 is strict-undo of the most recent move (rolls back trail deposition + any captures from a just-closed loop). No ACTION5 (no commit verb — closure happens automatically when the avatar steps onto its own trail). No ACTION6 (no clicks).

## Mechanic count and progression

- **L1**: M1 (walk-deposits-trail) + M2 (closing-loop-captures-interior). Witness exercises both — the player must walk a full loop and step back onto the trail.
- **L2**: +M3 (forbidden-exclusion: enclosing a forbidden sprite strikes; 3 strikes = lose) + M4 (multi-colour targets requiring multiple separate closures, since one big loop would also enclose forbiddens). +2 mechanics.
- **L3**: +M5 (autonomous pursuer that BFS-walks one cell toward avatar per turn, must be captured by a closure before adjacent contact — adjacent contact = lose) + M6 (post-closure trail solidifies into walls, blocking future avatar movement). +2 mechanics.

Mechanic counts per level: L1=2, L2=4, L3=6. Each promotion adds exactly 2. Every prior-level mechanic remains required at later levels.

## Similarity check (positive — `similarity-check.md`)

### Vs 25-game taxonomy

No taxonomy entry's `mechanic_family` matches `walk-trail-loop-enclose` even at the first-two-words level after hyphen-splitting. Nearest taxonomy entries by surface-feature overlap (sub-thresholds for the family check):

- **sk48 paired-snake-trail** — also has trail-deposit-while-walking. WIN/PRIMARY-ACTION/PRIMARY-CONSTRAINT comparison: sk48's win is per-cell-colour-match between two mirrored heads' trails (no enclosure); ours is target-strictly-inside-Jordan-curve (enclosure detection). sk48's primary action is two-head-with-mirrored-axes movement; ours is single-head walk. sk48's constraint is cell-level colour match; ours is polygon-interior-membership. Different across all three. NOT FLAGGED.
- **ek73 wake-trail-evade** (prior, not taxonomy — covered below).
- **ar25 shape-mirror-cover** — shape-mirroring on reflectors; does NOT involve walking-trail or closed-loop interior detection. NOT FLAGGED.

### Vs `prior-games/index.md` (45 entries)

The closest near-miss is **qm4t convex-pen-trap**. Read its `mechanism-detail.md`:

- **qm4t WIN**: capture all `tally` critters by enclosing them inside the convex hull of placed posts; commit via ACTION5; 3 wrong-colour captures = lose.
- **tj4n WIN**: capture all required-colour targets by enclosing them inside an arbitrary (possibly non-convex) closed walking polygon; closure is automatic when avatar steps onto its own trail; 3 forbidden-enclosures = lose.

Three-question family check:
- WIN CONDITION (capture-by-enclosure): SHARED concept.
- PRIMARY ACTION: qm4t = ACTION6 click-drop-post + ACTION5 commit; tj4n = ACTION1-4 walk-step-with-trail. **DIFFERENT** modality.
- PRIMARY CONSTRAINT (step budget + strikes): SHARED.

Two of three shared (win-class + constraint), one differs (primary action). FLAGGED for distinguishing rule.

**Concrete distinguishing rule (qm4t vs tj4n):** qm4t's pen is the convex hull of click-dropped posts; the player thinks in terms of "where to drop posts so the hull boundary excludes/includes the right critters". The pen is ALWAYS CONVEX (Andrew's monotone chain). tj4n's polygon is the avatar's literal walked path; it can be **arbitrarily non-convex** (concave, U-shaped, comb-shaped). The player must walk a connected adjacency-path that loops back on itself, and the cognitive task is route-planning a connected curve, not picking 3-8 discrete vertices. Crucially: tj4n REQUIRES adjacency-connected boundary cells (the avatar can only step to adjacent cells), so the polygon's edge length is bounded by the step budget — making walking-distance an explicit cost. qm4t has no such adjacency constraint; the pen can have arbitrarily long edges between vertices that are very far apart.

A spec attempting to convert qm4t to tj4n by "use ACTION6 to walk instead of clicking" wouldn't reproduce the mechanic; it would lose the per-step trail-deposition rule and the bounded-by-walk-cost feel.

Other prior-games near-misses checked and dismissed:

- **sk48-style trails**: ek73 wake-trail-evade (ek73 trail KILLS player; tj4n trail forms boundary), jd4q echo-trail-teleport (jd4q trail enables teleport-back; tj4n trail forms boundary), zd7m cohort-step (no trail), zk9p pursuer-merge (no trail).
- **enclosure-class**: only qm4t.
- **toggle-class**: qf8m rook-cross-toggle (clicks flip a fixed 2N-1-cell row+col cross — TOTALLY DIFFERENT from arbitrary polygon interior). NOT FLAGGED.
- **cell-painting-class**: re86 flood-fill (per-step paint deposit), gv47 seed-bloom (region growth from click), dc22 colored-doors (no trail). All have their primary win as canvas-pattern-match, not enclosure of discrete sprites. tj4n's win is enclose-discrete-sprites, not paint-canvas. NOT FLAGGED.
- **graph-class**: jx5k constellation edge-link (pair-click distant nodes to build multigraph; no spatial path requirement). NOT FLAGGED.

### Vs negative similarity (the 8 dimensions vs qm4t — `negative-similarity-check.md`)

1. **What's on the board.** qm4t: scattered critters + post markers + tally chips + (L3) patrollers, mostly empty arena. tj4n: avatar + glowing trail behind it + targets + forbiddens + (L3) pursuer + (L3) wall residue. Object cast is **DIFFERENT** — tj4n's central object is the GROWING TRAIL behind a moving pawn, qm4t's is a SET OF DROPPED POSTS that doesn't grow per turn.
2. **What the player physically does on input.** qm4t: clicks empty cells then commits with spacebar. tj4n: presses arrows to walk one cell at a time. **DIFFERENT** modality.
3. **What the level is asking for.** Both: enclose target-coloured sprites inside a region. SHARED.
4. **What kills the player.** Both: 3 strikes / step budget exhaustion. SHARED.
5. **The cast of supporting elements.** qm4t: tally chips on the side, patrollers, posts visible as discrete dots. tj4n: trail (continuous walked line), pursuer NPC. **DIFFERENT** — tj4n introduces a moving NPC at L3 that qm4t does not have.
6. **Visible visual signature.** qm4t L1: posts dropped at scattered positions in an arena, hull rendered as faint outline. tj4n L1: a small avatar in an arena leaving a glowing pink/cyan trail behind it as it walks. **DIFFERENT** visual pulse — the player SEES the trail GROW per step, vs qm4t where there's no per-step visual change between click and commit.
7. **Pixel grain of primary sprites.** qm4t's primary sprites are critters with internal pixel detail and 1-pixel posts. tj4n's primary sprites are: a 4×4 avatar pawn with internal directional cross + 4×4 ringed-trail cells + 4×4 target diamonds + 4×4 forbidden squared-Xs + 4×4 pursuer with distinct internal pattern. **DIFFERENT** sprite kit.
8. **The core dynamic.** qm4t: "where do I drop 3-5 posts to convex-fence the right critters". tj4n: "what walking path connects me back to my own trail while including target cells and excluding forbidden cells". The cognitive task is **DIFFERENT** — qm4t is convex-hull placement (choose 3-5 vertices), tj4n is connected-curve route planning (choose a sequence of N adjacent steps).

Shared dimensions: 3, 4. (Two of eight.) Below the 3-dimension threshold for rejection. NEGATIVE CHECK PASSES.

### Axis-1 note (vs preexisting video games — manual judgment)

The mechanic has a family resemblance to the 1981 arcade game **Qix** ("draw closed polygons to claim territory"). The differences:
- Qix is played from grid edges (line-drawing constrained to lattice edges); tj4n has a free-roaming avatar in an open arena (any cell reachable by 4-connected walk).
- Qix's enemy is a bouncing geometric shape ("the Qix"); tj4n L3 has a BFS pursuer NPC, not a free-bouncing shape.
- Qix's win is ≥75% territory claimed; tj4n's win is capture all required-colour targets via enclosure.
- Qix has "stix" guards along the partial line; tj4n has no along-the-line hazards.

Stating this for the user's axis-1 review since the harness can't auto-check vs preexisting games. The mechanic is presented as a fresh re-application of the Jordan-curve-interior idea in the NovaPlay sprite/turn model rather than a port of Qix's full feature set.

## §3.4 prior categories drawn from

- **Basic geometry & topology**: Jordan-curve interior detection (point-in-polygon) is the load-bearing topology mechanic. Inside-vs-outside is the primary geometric concept.
- **Objectness**: targets, forbiddens, and the L3 pursuer are coherent persistent sprites that get captured/struck.
- **Agentness** (L3 only): the pursuer pursues the avatar via greedy BFS — it acts with intent toward a goal.

(No basic physics — no gravity / momentum / friction — keeping the prior-set focused.)
