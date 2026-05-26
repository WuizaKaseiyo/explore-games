# Mechanic pick

## Game ID
`zd7m`

Verified: not in the 25 reserved reference IDs, not in `prior-games/index.md`'s 19 entries, lowercase alphanumeric, not an English word. Pascal class will be `Zd7m`.

## Seed
None (autonomous mode — no run input provided).

## Mechanic family tag
`cohort-step-route`

## One-paragraph description

Every movable pawn on the board steps one cell in the pressed
arrow direction simultaneously. A pawn moves if its destination
cell is empty (not a wall, not an anchored block, not a target,
and not a fellow pawn whose own destination is occupied);
otherwise it stays put for the turn while the rest of the cohort
moves. There is no avatar, no selection, no click — the player
operates on the *whole population* of pawns each press. Each
pawn carries one of N palette colours and the goal is for every
pawn to end the level standing on a target tile of its own
colour. The geometry of walls, immovable anchored blocks, and
the relative starting positions of the colour-distinct pawns
combine to make naive "all-go-east, then all-go-south" routing
fail in the L2/L3 layouts; the player has to plan an arrow
sequence that respects which pawns are blocked together and
which can be peeled off the cohort by stepping into a lane an
anchor seals behind them.

## Action vocabulary

`available_actions=[1, 2, 3, 4]`. Pure-arrow palette per the
soft-norm in `skills/global/action-enum.md` — the distinctive
verb lives on ACTION1-4 (the arrow press is itself the unusual
move because it moves *every* pawn, not one). ACTION5/6/7 are
intentionally absent — adding them would create slots the game
does nothing distinctive with, which the action-enum doc
explicitly flags as wasteful.

## Mechanic count per level (preview for write_spec)

- **L1** — base dynamic system: cohort-step + colour-matching
  (N = 2 mechanics required by the witness).
- **L2** — +1: colour-locked floor cells that only let same-
  coloured pawns pass through (N+1 = 3 mechanics).
- **L3** — +1: portal pairs that teleport a pawn from portal A
  to portal B on landing (N+2 = 4 mechanics).

Both promotions add exactly 1 new mechanic; every L1 mechanic
is carried into L2 and L3, every L2 mechanic is carried into
L3 — compliant with `composition-and-tutorial.md` § "No hidden
mechanics; one or two new mechanics per level".

## Positive similarity check (per `mechanic-novelty/similarity-check.md`)

Walking the full taxonomy and the prior-games index. For each
near-miss I name the concrete distinguishing rule.

### Taxonomy near-misses

| Near-miss | Win-condition match | Primary-action match | Distinguishing rule |
|---|---|---|---|
| **ka59 sokoban-explode-chase** | Yes (cover targets). | Partial (arrows move pieces). | ka59 selects ONE active pawn at a time via click and that pawn steps 3 cells per arrow, recursively *pushing* other pawns. zd7m has no selection and no pushing — every pawn moves 1 cell simultaneously, and pawn-pawn collisions cause the blocked pawn to stay put rather than push. Plus zd7m has no chaser. |
| **m0r0 mirror-orb-merge** | Different (m0r0 = merge each pair into one cell; zd7m = each pawn on its own colour target). | Partial (arrows move all pawns). | m0r0 is exactly two mirror-paired orbs whose horizontal axis is *anti-coupled* (LEFT moves one left and the other right). zd7m's pawns are *isotropically coupled* — every pawn translates identically in the pressed direction. Different number of pawns, different coupling rule. |
| **vc33 row-slide-pull-tab** | Same shape (deliver units to colour-matched cells). | Different (vc33 click; zd7m arrow). | vc33 affects a *single row* per click; zd7m affects every pawn on the entire grid per arrow. Verb cardinality is "one row" vs "all pawns". |
| **lp85 row-col-shift-grid** | Similar (tokens onto matching tiles). | Different (lp85 click row/col arrow buttons). | lp85 shifts the contents of one row or column per click; zd7m moves every pawn one cell in a cardinal direction per arrow. |
| **wa30 lock-drag-crate** | Different (deliver crates into goal frames). | Different (arrows move avatar; ACTION5 latches crate). | wa30 has a single avatar with a lock-key; crates only move when latched and dragged. zd7m has no avatar — every pawn moves freely each turn under the same arrow. |
| **dc22 colour-cycle-walk** | Different (match a target ring of cycled wedges). | Different (single pawn walks). | dc22 has one pawn walking and stepping on triggers; zd7m moves every pawn simultaneously without any avatar. |

### Prior-games index near-misses (cumulative corpus, 19 entries)

| Prior | Distinguishing rule |
|---|---|
| **kn58 anchor-pull-magnet** | kn58 is click-only: click any cell to plant an anchor and every coloured pawn slides one cell along its dominant Manhattan axis *toward* the click. zd7m is arrow-only: press arrow and every pawn slides one cell in the pressed cardinal direction (no click, no anchor cell, no Manhattan-axis projection). The verb lives on different action slots and the direction is global rather than per-pawn-toward-point. Visual signature also diverges — zd7m uses 5×5 patterned tiles on a non-grey background, kn58 uses 3×3 sparse blocks on grey. |
| **wt39 glide-deflect-thaw** | wt39 has a single avatar pawn that glides in the pressed direction until it hits a wall or bumper. zd7m has no avatar — every coloured pawn on the board steps one cell each press and stops on the next cell (no glide-to-wall). Different number of moving entities (1 vs N) and different motion model (glide-until-collision vs step-one-cell). |
| **m0r0 / kf42 / qb84 (paired-pawn moves)** | All three priors involve coupled motion of small pawn populations. zd7m involves an arbitrary number of independent same-rule pawns whose only "coupling" is that the same arrow press fires for all — there is no pair invariant, no swap, no tether. |
| **ka59 (already covered above)** | n/a |
| **vc33 / lp85 row-shift-style references** | row-or-column-at-a-time vs whole-grid-at-a-time, as above. |

## Negative similarity check (per `mechanic-novelty/negative-similarity-check.md`)

L1 PNGs of the closest candidates were opened: `kn58/level_1.png`,
`wt39/level_1.png`, `pz4t/level_1.png`, `rk7x/level_1.png`,
`vp6h/level_1.png`. Walking the eight dimensions against each:

### vs **kn58 anchor-pull-magnet**

| # | Dimension | Shared? | Notes |
|---|---|---|---|
| 1 | What's on the board | yes | Both: blocks + targets. |
| 2 | What player physically does | **no** | kn58: click a cell. zd7m: press an arrow. |
| 3 | What level asks for | yes | Deliver each pawn to a target. |
| 4 | What kills the player | yes | Step budget. |
| 5 | Cast of supporting elements | yes | Coloured pawns + same-colour targets + walls. |
| 6 | Visible visual signature | **no** | kn58: pale-grey field with small orange anchors. zd7m: distinct palette (planned: deep navy field with bright pastels — pink/yellow/green) and richer 5×5 patterned pawns instead of kn58's 3×3 sparse ones. |
| 7 | Pixel grain of primary sprites | **no** | kn58 uses 3×3 sparse plain blocks; zd7m planned 5×5 with internal motifs (ring + cross centre for pawns; pin-cross for anchors; portal-ring for portals). |
| 8 | Core dynamic | **no** | kn58: "click a point, all pawns are attracted toward it one cell along their dominant axis." zd7m: "press a direction, all pawns step that way as a synchronised cohort." Polar inverse — point-source attractor vs global-direction translation. |

Shared: 1, 3, 4, 5 (the four most generic dimensions). Different: 2,
6, 7, 8 — the three "heavier" axes (per the rule that 6/7/8 weigh
more) plus the verb. Verdict: PASS the negative test.

### vs **wt39 glide-deflect-thaw**

| # | Dimension | Shared? | Notes |
|---|---|---|---|
| 1 | What's on the board | partly | wt39: single avatar + walls + bumpers + target. zd7m: many movable pawns + walls + anchors + targets. Cast cardinality differs. |
| 2 | What player physically does | partly | Both press arrows; wt39 moves one entity, zd7m moves all entities. |
| 3 | What level asks for | partly | wt39 deliver one avatar to one target; zd7m match every pawn to its colour target. |
| 4 | What kills the player | yes | Step budget. |
| 5 | Cast of supporting elements | partly | Walls + targets + obstacles is universal; cardinality differs. |
| 6 | Visible visual signature | **no** | wt39: white background, dark-grey 2-3-cell flat blocks, single red avatar, single maroon target. zd7m: navy/dark background, multi-colour 5×5 patterned pawns, multiple targets. |
| 7 | Pixel grain | **no** | wt39 sprites are 2×2/3×3 plain solids; zd7m planned 5×5 with internal motifs. |
| 8 | Core dynamic | **no** | wt39: "I plan a path for ONE piece bouncing between bumpers." zd7m: "I plan an arrow sequence that herds MANY pieces simultaneously into colour-matched targets." |

Shared cleanly: 4. Partial overlap: 1, 2, 3, 5. Different: 6, 7, 8.
Verdict: PASS.

### vs **pz4t anchor-pivot-place**

pz4t is a jigsaw click-pivot mechanic on solid coloured rectangles
inside a single dark-grey region. Different verb (click-pivot
+ rotate vs arrow), different goal (tile a region), different
cast (puzzle pieces vs free pawns). Shared dimensions: 4 (step
budget). PASS trivially.

### vs **rk7x live-switch-routing**

rk7x has an autonomous courier pawn walking grey routing tracks;
clicks toggle junction blades. zd7m has no courier, no track
network, no junction toggling — pawns move under arrow, not under
autonomy. Shared dimensions: 4. PASS trivially.

### vs **vp6h shadow-cast-collect**

vp6h has a single avatar walking lit cells under rail-mounted
lanterns to collect crystals. zd7m has no avatar, no light cones,
no collection. Shared dimensions: 4. PASS trivially.

### Negative-test summary

No prior shares ≥3 of the seven dimensions with `cohort-step-route`
when the heavier axes (6, 7, 8) are weighted as the rule requires.
The closest single overlap is kn58 on the four generic dimensions
(board, ask, kill, cast), differentiated cleanly on verb and on
all three heavy axes. Verdict for the candidate: NOVEL by both
the positive and negative novelty tests.

## What `write_spec` will need

- ID `zd7m`, family `cohort-step-route`.
- Action subset `[1, 2, 3, 4]`.
- L1: cohort-step + colour-matching with 3-4 pawns and 3-4
  same-colour targets. No anchors yet (pure free routing).
- L2: add colour-locked floor (cells that only allow same-coloured
  pawns to pass through; act as walls for non-matching colours).
- L3: add portal pairs (a pawn landing on portal A teleports to
  portal B and stops on the same turn — visible animation).
- Determinism: pawn-pawn conflict resolution is deterministic
  (process pawns in row-then-column order; a pawn moves only if
  its destination is currently empty after earlier pawns have
  resolved).
- Visual signature: deep navy / off-black background, palette
  emphasising bright pastels (pink, yellow, light-blue, green) for
  pawns + targets, off-white for colour-locked floor cells.
  5×5 sprite roster with internal ring motif (pawn = filled centre
  with paired-pixel halo; target = hollow ring of pawn colour;
  anchor = dark frame with a "+" cross centre; portal = double
  concentric ring).
