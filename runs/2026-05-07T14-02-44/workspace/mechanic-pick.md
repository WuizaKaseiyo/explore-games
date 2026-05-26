# Mechanic Pick

## 4-character ID
`yf3h`

Reserved-list check (per `skills/code/id-generation.md`):
- Not in 25 reference IDs (`ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59 lf52 lp85 ls20 m0r0 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93 vc33 wa30`).
- Not in `prior-games/index.md` (22 entries: `kf42 vh68 qz73 kx14 qb84 lq5x gv47 hr8q ng52 pj7k pz4t vn8d fz5j kn58 bx84 wt39 zk9p rk7x gx7m vp6h kp9z zd7m lv4k`).
- Not a recognisable English word; opaque per §3.4.
- Pascal class derivation: `Yf3h` (valid Python identifier).

## Mechanic family
`pulse-arm-burst-resonate`

## Description
A small grid contains stationary **emitter** sprites of distinct colours and one or more **resonator** target cells that each display a coloured-pip *multiset requirement* immediately above them. Clicking an emitter (`ACTION6`) **arms** or **disarms** it as a toggle — armed emitters render with a brightened halo; disarmed ones render dim. Pressing `ACTION5` simultaneously **fires every armed emitter**: each fires one transient concentric pulse-ring that begins at radius 0 (the emitter cell) and expands outward 1 cell per animation tick, in Manhattan-ring shape, until the ring leaves the level bounds. As each ring sweeps outward, on every animation tick the cells at exact Manhattan distance R from its emitter constitute the ring's footprint for that tick. When a ring of colour C passes over a resonator on tick T, the resonator's matching colour-pip in its multiset display flashes for tick T (visibly brightens). A resonator **activates permanently** when, on the SAME animation tick, every colour-pip in its multiset is concurrently flashing — i.e., when one ring of each required colour passes over the resonator simultaneously. Each `ACTION5` "burst" consumes one step from the budget; each `ACTION6` (arm/disarm or, from L3, phase-delay-tile toggle) consumes one step. The level wins when every resonator is activated; the level loses when the step budget reaches zero.

From L2, **colour-keyed resonator** rule: a resonator's multiset display lists specific colours; only same-colour rings register flashes on the matching pip. A wrong-colour ring sweeping over the resonator does nothing (its colour is not in the multiset).

From L3, **phase-delay tiles** are introduced: each phase-delay tile is in `inactive` (dim) or `active` (lit) state; clicking it toggles the state. When active, any ring passing through the tile's cell is delayed by exactly 1 tick before continuing — i.e., the ring's footprint at that cell stays at radius R for tick T and tick T+1 (one extra tick), and downstream cells receive the ring 1 tick later. This lets the player compensate for unequal Manhattan distances when aligning multi-colour resonators that require simultaneous arrival.

## Allowed core-knowledge priors used
- **Objectness**: emitters, resonators, delay tiles are persistent objects with state.
- **Basic geometry**: Manhattan ring = the set of cells at fixed L1-distance from the emitter.
- **Basic physics**: wave-front propagation at fixed unit speed; phase-delay = local slow-down.

No agentness (no NPCs); no symbolic/cultural priors; no real-world clipart.

## Action mapping
- `ACTION5`: fire (burst all armed emitters simultaneously).
- `ACTION6`: click — toggles arm-state of the clicked emitter, OR (from L3) toggles active-state of the clicked phase-delay tile, OR no-op (still consumes 1 step) on any other cell.

`available_actions = [5, 6]`. Click-and-modal-key combination is in the `~12/25` mixed-input family per cross-cut frequencies.

## Per-level mechanic count plan (vs checklist item 11)
- **L1**: M1 (`arm-fire-ring-strike-resonator`) — 1 mechanic.
- **L2**: M1 + M2 (`colour-keyed resonator`) — 2 mechanics, +1 from L1.
- **L3**: M1 + M2 + M3 (`phase-delay tile`) — 3 mechanics, +1 from L2.

Each level's witness exercises every listed mechanic; full counterfactuals will be detailed in the spec.

## Similarity-check pass (vs taxonomy + prior-games)

### Positive similarity check (per `similarity-check.md`)

For each row in the taxonomy and prior-games index, compared:
- (i) Family-tag overlap — does my `pulse-arm-burst-resonate` share first-two-words after hyphen with any other family-tag?
- (ii) Description-level: win condition match? primary action match? primary constraint match?

**Taxonomy rows** flagged for description-level escalation (none had family-tag overlap; flagging based on description):

- **cd82 (`orbit-fire-paint`)**: shares "fire" verb. Distinguishing rule: cd82 fires a directional projectile (half-canvas axial paint or diagonal-wedge); mine fires omnidirectional concentric rings. cd82's win is canvas-pattern matching (image); mine's is per-resonator multiset activation. No overlap on core dynamic.
- **ka59 (`sokoban-explode-chase`)**: shares "outward burst" surface (explode-tiles spray neighbours). Distinguishing rule: ka59's explosion is a 1-tick instantaneous push of adjacent pawns; mine's ring is a multi-tick travelling wave-front across open space. ka59 has multiple controllable pawns; mine has none.
- **m0r0 (`mirror-orb-merge`)**: no surface overlap, but flagged for completeness (mirror-image dynamics). Distinguishing rule: m0r0 is paired-pawn motion under mirror-coupling; mine has no pawns and no mirroring.

**Prior-game rows** flagged for description-level escalation:

- **bx84 (`beam-mirror-reflect`)**: emitter-target topology; both involve `(emitter → transformer → target)`. Read `prior-games/bx84/mechanism-detail.md` in full. Distinguishing rule: bx84 fires a single LINEAR beam that is routed via mirror geometry (player click places `\`/`/` mirrors that reflect the beam by 90°); mine fires CONCENTRIC RINGS expanding omnidirectionally and uses MULTISET-MATCHING (one ring per required colour, all arriving SAME TICK) at each resonator. bx84 has no notion of "target needs N concurrent inputs"; mine's central puzzle IS that simultaneity requirement.
- **gv47 (`seed-grow-surround-dissolve`)**: both have outward expansion from a clicked source. Read `prior-games/gv47/mechanism-detail.md`. Distinguishing rule: gv47's expansion is PERSISTENT region-fill (cells stay coloured and target pips dissolve when surrounded); mine's is TRANSIENT ring-front (each ring exists only at radius R on tick R, then moves on). gv47 player thinks "what cells get covered"; mine player thinks "what tick each cell is touched and by which colours simultaneously".
- **gx7m (`gear-mesh-cascade`)**: both have cascade-like dynamics from a click point. Read `prior-games/gx7m/mechanism-detail.md`. Distinguishing rule: gx7m's cascade propagates rotation BFS through a STATIC mesh-graph of gears (instant 1-step BFS, parity-flip per hop); mine's propagation is GEOMETRIC (Manhattan rings through OPEN SPACE) and TIMED (one cell per animation tick over many ticks). gx7m has no concept of "ring", "colour multiset", or "phase delay".
- **kp9z (`grain-accumulate-topple`)**: both have player-controlled accumulation toward targets, both are click-only (mine adds ACTION5). Read `prior-games/kp9z/mechanism-detail.md`. Distinguishing rule: kp9z accumulates persistent grain counts at cells, with a topple rule (overflow at capacity 4 fans grains to 4 cardinals); mine has no per-cell counts — only resonators care about charge, and they care via multiset-matching, not numeric accumulation.
- **vn8d (`domino-cascade-topple`)**: shares "single click triggers cascade". Distinguishing rule: vn8d's cascade is INSTANT chain-reaction through pre-placed PILLARS (the level layout determines the path); mine's expansion is OMNIDIRECTIONAL across open space (geometry determines path) and TIMED (multi-tick).
- **kn58 (`anchor-pull-magnet`)**: shares "click any cell triggers a global one-step effect". Distinguishing rule: kn58 moves all coloured pawns one cell toward the click; mine has no pawns and no movement — only ring-pulse propagation. Different cast and different rules.
- **fz5j (`phase-step-tile`)**: shares "tile-period" surface (cells with timing properties). Distinguishing rule: fz5j is an avatar walking on tiles that pulse open/closed on per-cell periods (avatar-vs-timing puzzle); mine has no avatar, and "delay" is a fixed +1 tick offset on passing rings, not a periodic open/closed schedule. Different cast (avatar vs none) and different role (hazard vs alignment-tool).
- **gx7m sec. clutch / ratchet (`gear-mesh-cascade`)**: same row already addressed above.

For every flagged row, the distinguishing rule is concrete (cited cells, sprite roles, dynamics — not "different colours", not "harder").

### Negative similarity check (per `negative-similarity-check.md`)

Walking the 7 dimensions against the closest prior (bx84):

| # | Dimension | bx84 | yf3h | Same? |
|---|---|---|---|---|
| 1 | What's on board | emitter + mirrors + filters + prism + targets | emitters + resonators + (L3) phase-delay tiles | NO — shape language differs (right-angle reflectors vs phase-tile flips) |
| 2 | Player input | click only; click on empty places mirror, on mirror cycles | click toggles arm; ACTION5 burst-fires | NO — modal ACTION5 is a distinct verb |
| 3 | What level asks | light every target via beam routing | activate every resonator via multiset matching | YES (both: "activate every target") but mechanically different (geometric vs simultaneity) |
| 4 | What kills | step budget | step budget | YES |
| 5 | Cast of supporting elements | mirrors, filters, prisms | phase-delay tiles, walls | NO — different roles, different shapes |
| 6 | Visible visual signature | linear beam (1-pixel wide, in palette of beam colour) | concentric Manhattan rings (1-pixel-wide ring expanding outward) plus multiset pip displays | NO — fundamentally different visual idiom |
| 7 | Pixel grain | multi-pixel sprites (mirrors/prisms are 3×3+) | multi-pixel sprites (emitters/resonators 5×5+) | YES (similar grain, both use multi-pixel) |
| 8 | Core dynamic | static linear beam routing through mirror geometry | timed concurrent ring expansion + multiset-on-same-tick activation | NO |

Same on dimensions {3, 4, 7}. Per the rule "sharing on dimensions 6, 7, 8 is heavier than sharing on the others, because those are the named principles", I share on 7 (grain) but DIFFER on 6, 8 (the principles' visual signature and core dynamic). Three dimensions of overlap, with two of the three being weak (every step-budget game shares 4; every "hit-all-targets" game shares 3). Not over the rejection threshold.

Walking the 7 dimensions against gv47:

| # | Dimension | gv47 | yf3h | Same? |
|---|---|---|---|---|
| 1 | Board | seeds + pips + walls | emitters + resonators + delay tiles | NO |
| 2 | Input | click + ACTION5 (mix) | click + ACTION5 (fire) | YES (same input cardinality) |
| 3 | Asks | surround pips with same-colour paint to dissolve | activate resonators via colour-multiset | NO |
| 4 | Kills | step budget | step budget | YES |
| 5 | Cast | seeds, pips, walls | emitters, resonators, phase-delay tiles | NO |
| 6 | Visual | persistent coloured region-fill, target pips with black rings | transient Manhattan rings + multiset pips above resonators | NO |
| 7 | Grain | multi-pixel | multi-pixel | YES |
| 8 | Core dynamic | grow persistent regions; mix on contact | fire transient rings; multiset hit on tick | NO |

Same on {2, 4, 7}. Different on principles {6, 8}. Acceptable.

Walking the 7 dimensions against gx7m:

| # | Dimension | gx7m | yf3h | Same? |
|---|---|---|---|---|
| 1 | Board | gears + ratchets + clutches | emitters + resonators + phase-delay tiles | NO |
| 2 | Input | click only | click + ACTION5 | NO |
| 3 | Asks | rotate all gears to target rotation | activate all resonators via multiset | NO (same surface "match all targets" but different mechanically) |
| 4 | Kills | step budget | step budget | YES |
| 5 | Cast | gear discs / bolt-toggles | emitters / resonators / delay tiles | NO |
| 6 | Visual | gear-discs with rim-marks rotating | concentric ring-fronts expanding | NO |
| 7 | Grain | 5×5 gears | 5×5 emitters | YES |
| 8 | Core dynamic | parity-cascade through static mesh-graph | wave-propagation through open space, multiset-tick activation | NO |

Same on {4, 7}. Different on principles {6, 8}. Acceptable.

### Verdict
NOVEL. The mechanic is meaningfully distinct from every prior on the principles axes (visual signature, pixel grain semantics, core dynamic). Distinguishing rules are concrete and cite specific cell-level / state-level rules.
