# mechanic-pick

## Game ID
`gv47`

Verified opaque, lowercase alphanumeric, 4 characters; not an English
word; not in the 25 reserved reference IDs; not in `prior-games/index.md`
(which currently holds kf42, qz73, kx14, qb84, lq5x).

## Mechanic family
`seed-grow-mix`

## One-paragraph description

Several stationary "seed" sprites of distinct colours stand on a small
grid alongside immovable wall sprites and a sparse set of "target" cells
(each target marked with a tiny coloured pip telling the player which
colour the cell wants to end up). The player has no avatar — they play
by clicking a seed (ACTION6) to expand that seed's coloured region
outward by exactly one cardinal-adjacent "ring" of currently-uncoloured
non-wall cells (cells already painted any colour are inert; walls block
spread). ACTION5 fires a global "mix" event: every cell that lies on the
frontier between two different region colours (and every cell already
coloured by either of those two colours that is contiguous with the
contact) is re-coloured to a third **mix** colour determined by a
fixed pairwise mixing table for that level. Win: every target cell is
painted in its pip's colour; lose if the depleting step counter runs
out before that predicate is satisfied.

The mechanic draws on **objectness** (each seed is a persistent entity
whose coloured region is its own connected blob), **basic geometry &
topology** (rings expand by 4-cardinal frontier, walls block expansion,
contact graphs trigger the mix), and **basic physics** (a level-3
"wind bias" rule extends one cardinal direction's ring an extra step,
modelling directional spread).

## Compositional plan (preview, full version in spec)

- **L1** — single seed, single colour, single target inside an open
  pocket. The player clicks the seed and watches the ring grow once,
  iterating until the target cell is painted. **Mechanic 1:
  *click-to-grow*.**
- **L2** — two seeds (e.g. yellow + blue), one target whose pip colour
  is a third value (e.g. green). The player must grow both regions
  until they touch, then fire ACTION5 to mix the contact into the
  third colour. **Mechanic 2 added: *mix-at-frontier*.** Strict
  necessity: the green target is unreachable without the mix verb,
  because no green seed exists.
- **L3** — three seeds, three targets, plus a stationary "wind"
  sprite at one edge of the playfield. While the wind is present,
  every grow ring extends one extra cell in the wind's direction
  (asymmetric expansion). One target is positioned so that only the
  wind-biased ring covers it; another target requires a mix; the
  third requires plain growth. **Mechanic 3 added: *wind-biased
  growth*.** Strict necessity: that wind-only target is otherwise
  unreachable from any seed within the step budget.

The full spec will state per-level witness sequences making each
mechanic load-bearing.

## Similarity checks

### Against `taxonomy-of-25-games.md` (positive `similarity-check.md`)

Family-level scan: no taxonomy row's `mechanic_family` shares any
2-word prefix with `seed-grow-mix`. Description-level scan flags two
near-misses:

- **ft09 (stamp-3x3-paint).** Both involve clicks that paint cells.
  **Distinguishing rule:** ft09 always stamps a fixed 3×3 pattern
  *centered on the click location*, with no reference to any
  pre-existing region; gv47 expands an existing connected region
  outward from a *fixed seed sprite*, painting the n-th cardinal-
  adjacent ring on the n-th click of that seed. Click coordinates do
  not select a target cell — they select *which seed* (and therefore
  which existing region) to expand. ft09 also has no equivalent of
  ACTION5 mix: ft09 produces colour by re-stamping, not by combining
  two existing regions.
- **dc22 (colour-cycle-walk).** Both involve coloured regions that
  change colour over the course of play. **Distinguishing rule:**
  dc22 has an *avatar* that walks an arena and toggles a coloured
  trigger to advance every same-coloured wedge through a fixed colour
  sequence; the colour change is *cell-local* and cycle-driven. gv47
  has no avatar, no cycle, and no per-cell colour-list — colour is
  produced either by ring-growth from a stationary seed or by a global
  *mix* event that combines two regions into a third colour. Different
  state object (region vs cell), different verb (click-to-grow vs
  walk-to-trigger).

No other reference game involves region-growth-by-frontier, region-
contact mixing, or seed-localised expansion.

### Against `prior-games/index.md` (positive `similarity-check.md`)

| prior | family | description | family match? | flag? |
|---|---|---|---|---|
| kf42 | tether-pawn-cycle | two pawns + tether + colour pads | no | no |
| qz73 | radial-cycle-lock | central rotor + tip locks | no | no |
| kx14 | tide-tilt-buoyant | water tank + tilt + anchor | no | no |
| qb84 | bead-lift-swap | pure-arrow chain + lift/drop pegs | no | no |
| lq5x | lantern-cone-illuminate | avatar + directional light cone + filters | partial | yes |

**lq5x distinguishing rule:** lq5x projects a **transient** directional
**cone** from a moving **avatar** — a cell is illuminated only while
the cone covers it, and the player's primary verbs are *moving the
avatar* and *rotating the cone via ACTION5*. gv47 has **no avatar at
all**: the player triggers **persistent** concentric **rings** of
growth from **stationary seeds** by clicking each seed; ACTION5
*mixes contacting regions into a new colour* rather than steering a
transient field. The "covering-cells-with-the-source's-colour"
notion is the only shared notion at the goal level; the verb, the
topology of the spreading region (cone vs concentric ring), the
persistence rule (volatile vs persistent), and the role of ACTION5
(rotate cone vs combine regions into a derived colour) all differ.

### Against `negative-similarity-check.md` (8 dimensions, vs each prior)

Walking the 8-dimension shared-features test against each prior:

| dim | kf42 | qz73 | kx14 | qb84 | lq5x |
|---|---|---|---|---|---|
| 1. on the board | pawns vs seeds — different | rings vs seeds — different | tank vs seeds — different | beads vs seeds — different | avatar+lantern vs seeds-only — different |
| 2. player input | walk vs click | rotate+lock vs click | raise/tilt/anchor vs click | arrow-chain+lift vs click | walk+rotate vs click |
| 3. goal | re-tint pawns vs paint cells | align tips vs paint cells | balls into sockets vs paint cells | swap-sequence vs paint cells | illuminate rings vs paint cells (mild overlap) |
| 4. lose | step counter — shared | step counter — shared | step counter — shared | step counter — shared | step counter — shared |
| 5. supporting cast | pawns/pads vs seeds/walls/targets | rings/sockets vs seeds/walls/targets | balls/water/sockets vs seeds/walls/targets | beads/edges vs seeds/walls/targets | cone/filters/rings vs seeds/walls/targets |
| 6. visual signature | dark frame, chunky red/blue pawns | mid-grey field, scattered hollow rings | split-tone tank | dark with green/yellow/magenta plus-signs | dark + yellow rings |
| 7. pixel grain | 1×1 chunky | 4×4 hollow rings | 1×1 dots in tank | 5×5 plus-glyphs | small avatar + ring-glyphs |
| 8. core dynamic | navigate-and-recolour | rotation-alignment | fluid-and-tilt | chain-traversal | direction-projection |

Shared dimensions per prior: kf42 = 1 (#4); qz73 = 1; kx14 = 1; qb84 = 1;
lq5x = 1.5 (#4 + half-#3). All under the 3-dim rejection threshold.

**Visual-signature commitment** (negative-check Principle 2): gv47's
palette will be light-grey background (palette 2) with **distinctly-
coloured filled region patches** (yellow=11, blue=9, red=8 / replaced
with green=14 once mixing introduced) plus a near-black wall colour
(palette 4) and a small accent for the seed pips. This deliberately
diverges from all five priors' palettes (dark frames + sparse
coloured glyphs).

**Pixel-grain commitment** (Principle 1): the dominant visual mass is
*coloured region patches*, not 1×1 chunky pieces. The seed sprites
are 3×3 with a 1-cell hollow centre; targets are 3×3 frames with a
1×1 pip; walls are filled rectangles. Region patches grow to fill the
playfield over the course of a level — fundamentally different grain
than any prior.

**Core-dynamic commitment** (Principle 3): the player thinks "in what
order do I click these seeds, and where do I trigger a mix, so that
each target cell ends up the right colour?" — a *colour-territory and
mixing* dynamic. None of the five priors share this dynamic.

## Verdict

NOVEL. No taxonomy or prior-games entry shares ≥3 negative-check
dimensions; only mild positive flags (ft09, dc22, lq5x) all addressed
with concrete distinguishing rules. Proceed to `write_spec`.
