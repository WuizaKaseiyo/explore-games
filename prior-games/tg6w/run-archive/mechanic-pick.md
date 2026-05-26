# mechanic-pick (run 2026-05-07T14-32-08, autonomous)

## Game ID
**`tg6w`**

ID generation per `code/id-generation.md`: 4-char lowercase alphanumeric, opaque, not a recognisable English word. Verified non-collision against the 25 reserved reference IDs and the 24 prior-games entries (latest mr5q at the bottom of `prior-games/index.md`).

## Mechanic family
`settle-pile-tilt`

## One-paragraph description
Each arrow press sets the playfield's "down" direction (ACTION1 = up, ACTION2 = down, ACTION3 = left, ACTION4 = right); on the press, every loose **block** sprite slides multiple cells in the chosen direction simultaneously, sliding until it hits a wall or another already-settled block, then settles in place. Walls are fixed structural sprites that block all blocks. From level 2, walls have a colour accent; a block of colour C passes straight through walls whose accent matches C but is blocked by walls of any other colour — so the same arrow press routes different-coloured blocks down different lanes. From level 3, sticky-pad sprites occupy specific cells; the first block to slide across a sticky-pad gets caught and fixes in place mid-slide, and subsequent slides cannot dislodge it. The level wins when every coloured block sits on a same-coloured target cell. Lose when the step-counter HUD bar runs out (no per-action hazard).

Core-knowledge priors used (per `core-knowledge-priors.md`):
- **Objectness** — coherent block sprites with colour identity that pile against each other.
- **Basic physics** — gravity vector, slide-until-blocked dynamics, settle-on-impact.
- **Basic geometry & topology** — colour-keyed permeable walls partition the playfield into per-colour reachable regions.

## Closest taxonomy + prior-game entries with concrete distinguishing rules

### Closest taxonomy entries

**`g50t walk-vs-scroll`** — an avatar walks a scrolling board where the world slides one cell left every two turns; arrows step the avatar; ACTION5 fires a context-special ability. **Distinguishing rule**: g50t has a single avatar performing one-cell steps with the world's autonomous scroll as the time pressure; `tg6w` has multiple loose blocks that all slide simultaneously to the player-set "down" until each one hits something — the player chooses the slide direction, the world has no autonomous motion, and the win condition is positional pile-up rather than reaching a goal cell.

**`tu93 maze-pickup-train`** — a 3-cell-tall pawn hops three pixels at a time along walkable corridors; coloured arrows fall in step behind it; lead the train onto the goal-marker. **Distinguishing rule**: tu93 has a leader-follower train with one player-controlled lead and tagalong agents on a maze; `tg6w` has independent blocks with no leader-follower relationship — every block is equally moved by the gravity press, and the planning is about pile-ordering and channel selection, not about leading a chain.

**`sp80 pour-shelf-route`** — a row of horizontal coloured shelves over U-cups; click-and-slide a shelf, pour-key spills water cup-to-cup. **Distinguishing rule**: sp80's pourable substance is liquid that splits on shelves and falls straight off ends; pours are limited per-level (4 attempts) and the verb is shelf-positioning. `tg6w` does not pour anything: discrete block sprites slide together as a population, the verb is global gravity rotation rather than per-shelf positioning, and there is no "pour-attempt" budget — only the universal step counter.

### Closest prior-games entries

**`zd7m cohort-step-route`** — arrows step every movable pawn one cell; anchors selectively block; portals teleport into a sealed chamber. **Distinguishing rule**: zd7m's arrows move every pawn **exactly one cell** — Manhattan-routing planning where anchors are colour-keyed step-blockers and portals teleport. `tg6w`'s arrows slide every block **all the way until obstructed** (Sokoban-style multi-cell settle); the planning is trajectory prediction with pile-up dynamics, and the obstacles are colour-permeable walls rather than colour-keyed step-blockers. The cognitive task is fundamentally different: zd7m is "where does each pawn step this turn" (one-cell granularity), `tg6w` is "where does each block come to rest after a global avalanche" (slide-to-end granularity).

**`wt39 glide-deflect-thaw`** — pawn glides in pressed direction until wall; angled bumpers deflect 90°. **Distinguishing rule**: wt39 has a **single** pawn that glides; the gameplay is single-entity trajectory routing through bumpers. `tg6w` has **multiple** blocks that slide simultaneously and pile against each other; the distinguishing feature is the inter-block collision/settling dynamic, where block A may stop at row R because block B already settled there in this same press, and on the next press the chain reorganises. This pile-up coordination has no analogue in wt39's single-pawn glide. Bumpers (deflection) are also absent in `tg6w` — the only obstacle types are full walls, colour-keyed permeable walls, and sticky-pads.

**`kn58 anchor-pull-magnet`** — click any cell to place a single magnetic anchor; every coloured pawn slides one cell along its dominant Manhattan axis toward it. **Distinguishing rule**: kn58's verb is click-to-place-anchor; the slide direction is per-pawn (whichever axis is dominant from that pawn to the anchor) and one-cell-only. `tg6w`'s verb is arrow-press; the slide direction is **uniform across all blocks** (pure cardinal, set by the arrow), and the slide magnitude is **multi-cell** (slide-to-end). The geometry that distinguishes the two: kn58 collapses to "which target attracts each pawn", `tg6w` collapses to "which channel each block falls down" (with colour-permeable walls).

**`kx14 tide-tilt-buoyant`** — vertical fluid tank with ACTION1/2 raising/lowering water level, ACTION3/4 tilting floating balls, ACTION6 anchoring. **Distinguishing rule**: kx14 simulates a vertical fluid with continuous water-level state and ball-buoyancy; the action vocabulary is two-axis (level + tilt) plus anchor-click. `tg6w` has no fluid, no buoyancy, no continuous level — a pure 4-direction discrete tile-slide on a uniform grid with no axis privileged.

**`kp9z grain-accumulate-topple`** — click sources to drop grains; cells overflow at capacity 4; sinks absorb; click-rotatable redirectors forward grains. **Distinguishing rule**: kp9z grows the grain population by clicking sources; per-cell capacity drives a topple cascade. `tg6w` has a fixed-count block population from level start; there is no capacity, no topple, no source-click — only player-driven simultaneous slide. The cellular automaton flavour of kp9z is absent; `tg6w` is pure tile-physics-on-pressed-direction.

**`kf42 tether-pawn-cycle`, `qz73 radial-cycle-lock`, `lq5x lantern-cone-illuminate`, `gv47 seed-grow-surround-dissolve`, `hr8q pair-blend-recipe`, `ng52 multiset-signature-classify`, `pj7k rolling-cube-face-paint`, `pz4t anchor-pivot-place`, `vn8d domino-cascade-topple`, `fz5j phase-step-tile`, `bx84 beam-mirror-reflect`, `zk9p pursuer-merge-walk`, `rk7x live-switch-routing`, `gx7m gear-mesh-cascade`, `vp6h shadow-cast-collect`, `lv4k lever-balance-torque`, `xn5p chamber-stamp-partition`, `mr5q polarity-attract-discharge`, `qb84 bead-lift-swap`** — different verbs and different core dynamics; not flagged at the family level. Not enumerated above.

## Negative-similarity test (per `negative-similarity-check.md`)

Walked the 8 dimensions against the closest concerns (zd7m, wt39, kn58, kx14, kp9z); rendered initial frames opened above:

| Dimension | vs zd7m | vs wt39 | vs kn58 | vs kx14 | vs kp9z |
|---|---|---|---|---|---|
| 1. What's on the board | shared (multi-block grid) | not shared (single avatar, sparse bumpers) | not shared (sparse pair) | not shared (vertical fluid tank) | not shared (capacity-grain cellular) |
| 2. Player input | not shared (one-cell vs slide) | not shared (single-glide) | not shared (anchor-click) | not shared (level/tilt/anchor) | not shared (source-click) |
| 3. Goal | not shared (route to terminal vs settle on target) | not shared (avatar reaches goal cell) | not shared (each pawn on matching target) — partly shared in style | not shared (balls in cells) | not shared (grain into sinks) |
| 4. Lose | shared (step counter) | shared (step counter) | shared (step counter) | shared (step counter) | shared (step counter) |
| 5. Cast | not shared (anchors+portals vs walls+filters+sticky) | not shared (bumpers/thaw) | not shared (anchor) | not shared (water/balls/anchor) | not shared (sources/sinks/redirectors) |
| 6. Visual signature | divergent — `tg6w` will use a warm cream backdrop with deep navy walls and orange/green/purple accent blocks; zd7m is dark backdrop + pastel-pink/yellow/cyan | divergent — wt39 is white-backdrop with red avatar | divergent — kn58 is light-grey sparse | divergent — kx14 is half-air-half-water | divergent — kp9z is grey-backdrop dark-grey-cells |
| 7. Pixel grain | shared (3×3 sprites with internal pattern) | shared | shared | shared | shared |
| 8. Core dynamic | not shared — zd7m: "each press, every pawn moves 1 cell coordinated"; `tg6w`: "each press, every block avalanches to settle in a new pile against walls and each other" | not shared — wt39: "single pawn glides"; `tg6w`: "many blocks slide and pile" | not shared — kn58: "anchor pulls each pawn 1 cell along its dominant axis"; `tg6w`: "uniform-direction slide-to-end" | not shared — kx14: "raise water + tilt balls"; `tg6w`: "rotate gravity 4-cardinal" | not shared — kp9z: "capacity-driven topple cascade"; `tg6w`: "player-driven simultaneous slide" |

**Verdict**: closest concern is zd7m (3 shared dims: 1, 4, 7) — exactly at the threshold. The two heavier principles (6 visual signature, 7 pixel grain) split: 7 shared, 6 divergent. The fundamental dimension (8 core dynamic) is divergent: one-cell coordinated step vs slide-to-end pile dynamics is a substantively different cognitive task. Below the rejection threshold; **NOVEL**, with the visual-signature commitment recorded for the implement state to honour.

## Action subset preview
`available_actions = [1, 2, 3, 4]` — pure-arrow, no click, no ACTION5, no undo. Each arrow is a gravity vector; the freedom slot is intentionally empty because `tg6w`'s identity verb already lives on slots 1-4 (the directional slide). Per `action-enum.md` § "Distinctive verb on ACTION1-4" pattern (m0r0 mirror-orbs and tr87 cycle).

## Prior-games corpus state
`prior-games/index.md` contains 24 entries (kf42 → mr5q, latest 2026-05-07T14:21:03Z). All similarity rows above are addressed.
