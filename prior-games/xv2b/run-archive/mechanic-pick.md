# mechanic-pick

## Game ID
`xv2b`

Verified non-colliding:
- Not among the 25 reserved reference IDs (ar25 … wa30).
- Not among the 50 entries in `prior-games/index.md` (kf42 through mz6t — `xv2b` does not appear; closest `x*` priors are `xn5p` and `xz5g`, neither equal to `xv2b`).
- Lowercase alphanumeric, 4 characters, not an English word.

## Mechanic family
`vessel-valve-equalize`

## One-paragraph description

Three or more tall narrow vertical vessels stand side-by-side on the
playfield, each filled to some current water level (rendered as a
solid blue fill rising from each vessel's floor). Between every pair
of adjacent vessels, at one or two specific heights, sits a small
valve sprite — visibly OPEN (a horizontal slit in the wall) or
CLOSED (solid wall). Each vessel carries a thin coloured target-line
on its side at a specific height: the win condition is that every
vessel's blue surface ends up at its target line. The player has two
verbs: ACTION6 toggles the clicked valve (or, at L2/L3, clicks a
drain or pump glyph that sits flush on a vessel's edge), and ACTION5
advances the simulation one tick — every OPEN valve whose **slit is
at or below the lower of the two water surfaces** transfers one cell
of water from the higher-level vessel to the lower-level vessel
toward equalisation. L2 adds **drains** — a small dark-bordered hole
sprite on a vessel's bottom-corner that, on every ACTION5 tick,
removes one cell of water from that vessel; the player must route
flow so target levels are achieved before drain consumption empties
the vessel below its target. L3 adds **pumps** — a small fin/wedge
sprite between two vessels that, when toggled active and on each
ACTION5 tick, transfers one cell of water from its source vessel
into its destination vessel **regardless of relative levels** (i.e.
uphill), which the player must combine with valves and drain
avoidance to lift water past local minima onto target lines that
are higher than any natural-flow gravity would produce.

## Similarity-check pass

### Against the 25-game taxonomy

The candidate's family / verb has no exact match in
`taxonomy-of-25-games.md`. The closest near-misses and their
distinguishing rules:

- **sp80 (pour-shelf-route)** — sp80's water is *discrete drops* that
  fall from spouts, are split by movable shelves, and either land in
  cups or are wasted; the player slides shelves around to redirect
  drops, with a hard cap of four "pour attempts" per level. The
  candidate's water is a **continuous fill-level** that equalises
  across connected vessels; there are no drops, no shelves, no
  "pour" event — the simulation is a per-tick equalisation between
  adjacent vessels. The player verb is *toggle valve / activate
  pump*, never *slide a shelf*. Witness reasoning is about
  graph-of-vessels connectivity, not about drop trajectory.

- **lv4k (lever-balance-torque)** — lv4k's physics prior is a
  rotational torque integer (mass × signed arm length summing to
  zero on a horizontal beam); the candidate's physics prior is
  hydrostatic equalisation across connected reservoirs. The player
  in lv4k *places integer-mass weights* on a beam; the candidate's
  player *toggles binary valves*. Distinct primary action and
  distinct conserved quantity (mass-arm vs water-volume).

- **vc33 / lp85 (row-slide / row-col-shift)** — both shift entire
  linear arrays by clicked tabs/buttons. Candidate has no row or
  column slide; vessels are stationary and content (water level)
  changes by hydrostatic flow.

### Against `prior-games/index.md`

- **kx14 (tide-tilt-buoyant)** — closest prior on the "vertical
  fluid" axis. kx14 is a *single tank* whose water surface is
  raised/lowered by ACTION1/2 directly while floating balls tilt
  via ACTION3/4 and anchor via ACTION6 — the surface itself is the
  primary verb. The candidate has **N ≥ 2 separate vessels**
  connected by *togglable valves*; the player never lifts a surface
  directly, only opens/closes flow paths and lets gravity equalise.
  No floating balls, no anchors, no tilt. Verb cardinality differs
  (water-surface raise/lower vs. valve-toggle), and the puzzle
  shape differs (per-vessel target levels with combinatorial flow
  routing across the inter-vessel valve graph).

- **sp80** — same distinguishing rule as the taxonomy entry above.

- **vd3g (valley-dig-roll)** — vd3g toggles binary terrain HIGH/LOW
  on a flat 64×64 arena; marbles roll downhill cell-by-cell into
  adjacent low cells. Candidate has no marbles; water is a
  *bulk-conserved continuous level* in confined vertical vessels,
  not a single rolling object. Player verbs differ (toggle terrain
  cell vs. toggle inter-vessel valve), and the level's puzzle shape
  is "vessel water levels match target lines" not "marble reaches
  goal cell".

- **kp9z (grain-accumulate-topple)** — kp9z drops *discrete grains*
  via clickable sources; cells topple at capacity 4 in cardinal
  directions, redirectors deflect grains, sinks absorb. Candidate
  has no grains, no per-cell capacity-overflow rule; flow is a
  global per-tick equalisation between connected vessels rather
  than per-cell topple. Distinct on what flows (level vs grains),
  distinct on what triggers transfer (gravity-equalisation vs
  capacity-threshold).

- **rk7x (live-switch-routing)** — rk7x routes a *single autonomous
  courier* through coloured stops via clickable junction blades;
  the courier is one moving entity. Candidate has no courier; what
  flows is a continuous bulk fluid distributed across many
  vessels. Both share the verb "click to toggle a routing element",
  but the routed substrate differs (courier vs water level), the
  puzzle goal differs (delivery sequence vs. per-vessel level
  match), and the visual signature differs (thin track lines + dot
  vs. tall water columns + valves).

- **tg6w (settle-pile-tilt)**, **kn58 (anchor-pull-magnet)**,
  **mr5q (polarity-attract-discharge)**, **vt6q
  (grapple-anchor-yank)**, **pv5q (pivot-rod-swing)** — none
  involve water levels or valve graphs; quick rejection.

## Negative similarity check (per `negative-similarity-check.md`)

Walking the eight dimensions against the closest prior **kx14**
(visually inspected `prior-games/kx14/run-archive/smoke-frames/level_1.png`):

1. **What is on the board.** kx14: one large tank with water filling
   the bottom half + small orange-bordered pawns. Candidate: ≥2
   tall narrow vertical vessels with target lines + small valve
   sprites between vessels. **Distinct.**
2. **What the player physically does on input.** kx14: arrow keys
   raise/lower the water surface directly + ACTION3/4 tilt + click
   anchor. Candidate: only click (toggle valves / pump glyphs) +
   ACTION5 sim-tick. **Distinct.**
3. **What the level is asking for.** kx14: get balls to float at
   target positions tied to surface height. Candidate: each vessel
   independently reaches its own target line. **Distinct shape**
   (per-object floating heights vs. per-vessel surface heights).
4. **What kills the player.** Both: step budget runs out. **Shared
   weakly** (universal feature).
5. **Cast of supporting elements.** kx14: floating balls, anchors.
   Candidate: valves, drains, pumps. **Distinct.**
6. **Visible visual signature.** kx14: one big light-blue rectangle
   in lower half of frame on light-grey background, plus tiny
   pawns. Candidate: 3+ thin tall blue columns side-by-side, each
   with target-line tick on the side, valves between, no large
   horizontal water expanse. **Distinct** — the thin-column tile
   scaffold vs the single-tank fill is the most visible difference.
7. **Pixel grain of primary sprites.** kx14's pawns are simple
   ringed squares. Candidate's vessels have explicit walls, water
   meniscus on top, target-line tick, internal valve sprites with
   open/closed slit detail — **richer per-sprite pixel detail**
   than kx14's pawns.
8. **The core dynamic.** kx14: surface-height driven floating + tilt
   ball routing (player thinks about ball altitude vs. water
   level). Candidate: bulk hydrostatic equalisation + uphill
   pump-overrides (player thinks about which valve graph routes
   make each vessel's level converge). **Distinct.**

Shared dimensions: only #4 (universal step-budget kill). All seven
substantive dimensions diverge. The candidate passes the negative
similarity check against kx14.

Walking the same eight dimensions against the next-closest prior
**sp80** (the only other "blue-water + vertical-element" reference):
sp80 has *drops*, *shelves*, and *cups*; the candidate has none of
those, has no drops at all (continuous fill instead), and has no
slidable elements (vessels are fixed). Shared: dim 6 (some blue
water on screen). All other dimensions diverge.

Verdict: **NOVEL**. The candidate diverges from every taxonomy and
prior-games entry on the core dynamic plus visual signature plus
primary action; no single prior overlaps on three or more of the
eight dimensions.

## Action subset and prior categories

- `available_actions = [5, 6]`. ACTION5 = simulate one global tick;
  ACTION6 = click to toggle the clicked valve / pump / drain. No
  arrows are needed (the playfield is not a walkable grid). No
  undo: every action's effect is partially reversible by toggling
  back, and adding a strict-undo would only add planning slack
  without changing the puzzle.
- Core-knowledge priors exercised (per
  `core-knowledge-priors.md`): **basic physics** (hydrostatic
  equalisation; gravity; uphill-pumping requires extra work) +
  **objectness** (valves and pumps are coherent persistent
  togglable entities) + **basic geometry / topology** (the valve
  graph defining which vessels are connected at which heights).
  No agentness or cultural-conventions prior involved.
