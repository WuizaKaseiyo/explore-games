# Mechanic Pick — kp9z

## ID
`kp9z` — 4 lowercase chars, alphanumeric, opaque, not a recognisable English word.
Verified absent from reserved 25-game IDs and from `prior-games/index.md` (26 entries).

## Mechanic family tag
`grain-accumulate-topple`

## One-paragraph description

Each cell of the level grid carries an integer "grain count" 0..3. The player's
verb is **drop**: ACTION6 click on a cell adds 1 grain to that cell. When a
cell's grain count would exceed its **capacity** (default = 3), the cell
**topples**: its count resets to 0 and 1 grain is delivered to each of its
four cardinal neighbours, which may in turn topple, producing a deterministic
cascade. Grain count is rendered as a sub-cell pip pattern (3×3 sprite: 0
grains = empty centre, 1/2/3 grains = pip-pattern with that many filled
corner pixels). The level wins when every "target" cell holds the exact
target grain count printed on it (target shown as a faint frame ring whose
inner pip layout matches the desired count). Variant cells extend the system
across levels: at L2 some cells are **sinks** that absorb every grain
delivered without re-emitting; at L3 some cells have **reduced capacity 1**,
so they topple after the very first delivered grain. Player must reason about
where to drop, in what order, so that the cascade delivers exactly the right
count to every target while avoiding overshoot (over-toppling a target loses
its grains forever).

## Core knowledge prior coverage
Draws from §3.4 categories:
- **Objectness** — grains are persistent countable entities at each cell.
- **Basic geometry & topology** — cardinal-neighbour distribution; cascade
  reachability follows grid topology; sinks puncture the topology.
- **Basic physics** — overflow (capacity-exceeded) is a discrete physics
  analogue of fluid spillover; cascading conservation of grains (except at
  sinks) is a deterministic flow rule.
No agentness needed (no autonomous NPCs).

## Action enum (intended for spec)
- ACTION6 (click) — drop one grain on the clicked cell. (Click outside the
  grid is a no-op.)

That is the only required action at L1. (See spec for L2/L3 additions; the
core mechanic of L1 is mono-action click-to-drop, which exercises the full
discovery story: drop → see pip increase → drop again → see topple → see
cascade. ACTION5 may be added at a later level for an "advance time without
dropping" verb if needed; deferred to spec.)

## Novelty: positive `similarity-check.md` walk

For each near-miss family, I read the deeper evidence at
`deep-analysis-3lvls/<id>/<id>-deep-analysis.md`
or the prior-games entry's `mechanism-detail.md`.

### Taxonomy near-misses
None of the 25 reference games employ per-cell integer-counter overflow
redistribution. Closest analogue (description-level) is **dc22**
("colour-cycle-walk": stepping on a trigger cycles every wedge of that
colour to its next state in a fixed sequence). dc22 cycles a global state
on step; kp9z **accumulates a per-cell count whose cardinality drives a
threshold-overflow cascade**. Concrete distinguishing rule: dc22 is a
GLOBAL state cycle on a tag-group (every wedge of colour X cycles); kp9z
is a LOCAL per-cell counter that only redistributes when its OWN value
crosses a threshold, with the redistribution then potentially triggering
neighbours in turn.

No match on family tag; no match on description-level (win/action/constraint).

### Prior-games near-misses

**vn8d (domino-cascade-topple)** — Family-tag word "topple" overlaps. Read
`prior-games/vn8d/mechanism-detail.md` if more detail is needed; from the
index description: "Single click triggers a chain reaction through pillars;
burst-pads splay 4 ways, rotator-pads turn corners". The verb is *trigger
the cascade by knocking the first pillar*; the cascade is a binary
domino-state propagation where each pillar's tip-direction is a fixed
property determining which neighbour it knocks next.

Concrete distinguishing rules:
1. **State cardinality**: vn8d's cells are binary (standing / fallen);
   kp9z's cells are integer-valued (0/1/2/3) and the count itself is the
   rendered, reasoned-about state.
2. **Trigger**: vn8d toppling is triggered by a single mechanical knock —
   one click and the chain runs to completion. kp9z toppling is
   automatically triggered by a cell's own count crossing capacity, after
   any number of preceding drops accumulate; the player drops MANY grains
   over MANY clicks, each tracking how the integer landscape evolves.
3. **Direction**: vn8d's domino tips have a directional pose (which way
   they fall) — a structural authoring choice baked into each pillar.
   kp9z topples symmetrically to all four cardinal neighbours — the
   player cannot pre-choose the direction; topology of the grid is the
   only routing handle.
4. **Verb cardinality**: vn8d wants a single chain-runner click;
   kp9z wants many drops, each chosen for its incremental effect on the
   integer landscape. Player thinking is "where does this 1 grain end up?"
   not "which cascade do I trigger?".
5. **Failure mode (overshoot)**: kp9z has a unique failure mode where
   over-dropping causes a target cell to topple past its win-count and
   lose its grains; vn8d has no equivalent — toppling is monotone.

These five rules are concrete, not vague. Spec §9 will record them.

**gx7m (gear-mesh-cascade)** — Discs propagate rotations across mesh.
Distinguishing: gx7m propagates *rotations* (signed scalar that flips
across mesh). kp9z propagates *integer grain counts* (non-negative
quantity that disperses to 4 neighbours). Different state space (rotation
phase vs grain count) and different propagation law (sign flip vs split
into 4 pieces).

**gv47 (seed-grow-surround-dissolve)** — Click coloured seeds to grow
regions; surround a same-coloured pip with paint and the ring auto-
dissolves; ACTION5 globally mixes contacting region pairs into a derived
colour. Distinguishing: gv47 is *region growth and dissolution*, manifest
as continuous paint area expanding and decoupling. kp9z is *integer
accumulation*, manifest as per-cell pip-count changes that occasionally
discharge. There's no "region" concept in kp9z; grains are local
quantities, not contiguous areas. No mixing in kp9z; targets check a
specific count, not a hue.

**fz5j (phase-step-tile)** — Tiles pulse open/closed on per-cell periods
2/3/4. Distinguishing: fz5j is a *time-driven schedule* where each cell
follows a fixed periodic clock; the player's interaction is timing-the-
walk. kp9z is *count-driven*: cells change state only when actively
poked by drops/topples; nothing happens "on its own clock". Player
interaction is selecting where/when to deposit, not synchronising with
a metronome.

**hr8q (pair-blend-recipe)** — Click two ingredients to fill a formula
widget. kp9z has no widget, no recipe; targets are landscape positions
that need the right count. Family is unrelated.

No other prior-game family is a near-miss. The grain-accumulate-topple
core dynamic is unique in the corpus.

## Novelty: negative `negative-similarity-check.md` walk

Walking the eight dimensions vs the closest priors (vn8d, gv47, gx7m,
fz5j) and a few reference-game candidates with click-only verbs (lp85,
ft09, vc33, sb26):

| Dim | Description | vn8d | gv47 | gx7m | ft09 | lp85 |
|---|---|---|---|---|---|---|
| 1 | What's on the board | pillars in toppling pose | seed-spots growing into regions | gear-mesh of discs | empty 32×32 canvas with ref pattern in corner | tokens inside a Rubik-grid frame |
| 2 | Player input verb | click first domino | click seed; ACTION5 mix | click cluster; arrows | click cell to stamp 3×3 | click row/column shift buttons |
| 3 | Win condition | reach end markers | match target colour layout | match target rotations | match target canvas pattern | each token on matching target |
| 4 | Lose | step budget | step budget | step budget | step budget | step budget |
| 5 | Cast | pillars + bursts + rotators + targets | seed-pips, ringed pips, regions | discs, ratchets, clutches | 3×3 stamp pattern + canvas | 16×16 token grid + L/R buttons |
| 6 | Visual signature | dark backdrop + bright pillars | seed-spots + spreading paint | gear discs in a mesh layout | flat colour stamp canvas | tile-grid in cube-frame |
| 7 | Pixel grain | bursts as 3×3 stars | round seed pips | round disc sprites | flat 1×1 stamps | flat 1×1 tokens |
| 8 | Core dynamic | one-click cascade through pre-poseed pillars | continuous region grow + dissolve + mix | rotation propagation across mesh | repeated stamp to converge canvas | row/column shift to align |

kp9z dimensions:
1. What's on the board: a small grid where each cell shows a sub-cell
   pip pattern indicating its grain count, with a few cells visually
   distinguished as "target frames" with target counts inside.
2. Player input: ACTION6 click on a cell adds 1 grain.
3. Win condition: every target cell's grain count equals the target's
   declared count, simultaneously.
4. Lose: step budget.
5. Cast: a uniform grid of pip-cells, target frames, sinks (L2),
   rapid-topple cells (L3). No avatar, no walls, no projectile, no
   widget, no other gameplay objects.
6. Visual signature: pip patterns inside cells (sub-cell internal
   detail). Likely uses palette {2 light-grey backdrop, 4 dark-grey
   cell border, 11 yellow grain pip, 13 maroon target frame, 9 blue
   sink, 12 orange rapid-topple cell, 9 blue HUD bar}. This is a fresh
   palette signature — very different from {4 wall, 8 red, 9 blue} or
   the dark "pillar" backdrops of vn8d.
7. Pixel grain: each cell renders as a 3×3 pip sprite with the four
   corner pixels reserved for grain pips and the centre pixel reserved
   for cell-type indication (empty for plain, dot for sink, ring for
   rapid-topple). Internal structure that survives sub-cell resolution
   tests.
8. Core dynamic: per-cell integer counter with automatic 4-way
   redistribution on capacity-exceeded. Distinct from binary cascade
   (vn8d), region growth (gv47), rotational propagation (gx7m), time-
   driven pulse (fz5j), and any reference-game family.

Sharing tally vs each prior/reference candidate (universal step-budget
on dim 4 excluded from the count of "shared"; click-as-input on dim 2
counted as shared only when verb is conceptually similar):

- vs vn8d: dim 8 (cascade-y) is a soft share via "topple" word. Dims
  1, 2, 3, 5, 6, 7 all differ. Total shared: 1.
- vs gv47: zero strong shares; gv47's regions and mixing have no
  analogue here. Total shared: 0.
- vs gx7m: zero strong shares; mesh propagation is rotation, not
  count. Total shared: 0.
- vs fz5j: zero strong shares; cells don't pulse on a clock here.
  Total shared: 0.
- vs ft09 (stamp-3×3-paint): both are pure-click-paint games on a
  small grid. Dim 2 is shared (click-to-modify-cell). Dim 3 differs
  (stamp matches the canvas pattern; kp9z matches per-cell counts).
  Dim 5/6/7 differ. Dim 8 differs (stamp pattern vs accumulate-and-
  topple). Total shared: 1.
- vs lp85 (row-col-shift): completely different verbs and cast.
  Total shared: 0.

No prior shares 3+ dimensions with kp9z. Negative check passes.

## Discoverability check
- Drop → cell pip-count goes up by 1. Visible delta on every action.
  L1 within 4 actions a player will see a cell go 0 → 1 → 2 → 3 → topple,
  understanding the threshold. Both visual cue (pip increase) and
  cascade (multiple cells flicker) make the rule legible without text.
- Sinks (L2): hovering over a target cell, dropping shows pip increase;
  hovering over a sink cell shows... no pip-increase. Visual cue: sink
  cell has a centre dot from the start, distinct from plain cells.
  After a few drops the player infers "sink absorbs without count".
- Rapid-topple (L3): visually distinct centre ring on these cells from
  the start. After one drop cell topples → player infers "this cell
  has lower threshold". Frame-by-frame legible.

No symbol/letter/number-glyph used. Pip patterns are purely visual count
indicators (1, 2, or 3 corner pips), not digits.

## Final ID & summary
- ID: `kp9z`
- Family tag: `grain-accumulate-topple`
- One-line: "Click cells to drop grains; cells overflow at capacity 3
  and split one grain to each cardinal neighbour, cascading; reach
  target counts on every target cell without overshooting."
