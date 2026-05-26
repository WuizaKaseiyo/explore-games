# Mechanic Pick — qn7w

## Game ID
**qn7w** — verified 4 chars, lowercase alphanumeric, opaque (not a word), absent from the 25 reference IDs (`ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59 lf52 lp85 ls20 m0r0 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93 vc33 wa30`), and absent from `prior-games/index.md` (33 entries: kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w, tg6w, vd3g, jd4q, ek73, tm5x, qx7p, kj82, nb6t).

## Mechanic family tag
**`pulse-chain-eject`** — Newton's-cradle-style momentum transfer along a stationary chain of balls.

## One-paragraph description

Linear chains of stationary coloured balls sit on visible rails inside the playfield, with a distinctive "pusher knob" at one end of each chain and one or more "target sockets" elsewhere on the board. The player clicks a pusher knob to send a single momentum pulse along the rail; the pulse propagates instantly through the chain as a brief flash, but **the intermediate balls do not move** — only the ball at the far end of the chain ejects. The ejected ball flies one step (or until colliding with another ball/wall) along the chain's terminal axis. The level is won when every target socket has received an ejected ball of its required colour. Chains shorten by one ball per pulse, so each chain has a finite number of pulses available before collapsing. The defining property — energy *concentrates* at the terminal rather than distributing through every cell — is what makes this mechanic distinct from every cascade-style prior. Across the three levels, the base system (pulse → terminal-eject) is enriched first by colour-coded **T-junction routing** (a junction node that gates which branch ejects based on the pulse's colour) and then by **end-ball merge-on-coincidence** (two end-balls landing on the same cell fuse into a double-ball that satisfies a 2-ball target socket).

## Core-knowledge-prior compliance

Mechanics drawn from `core-knowledge-priors.md`:
- **Objectness** — balls, pusher knobs, target sockets, junction nodes are persistent collidable entities.
- **Basic physics** — momentum transfer (Newton's cradle), with the conservation rule "only the terminal ball ejects".
- **Basic geometry & topology** — chain branching at junctions; terminal-eject direction is the chain's axis at the eject point.

No agentness needed (no autonomous chasers/patrolers). No forbidden symbol/letter/digit shapes; no cultural conventions used.

## Similarity check (positive — `similarity-check.md`)

Concrete distinguishing rule for every taxonomy near-miss and prior-games near-miss:

### Reference-game taxonomy near-misses

| Taxonomy entry | Surface overlap | Concrete distinguishing rule |
|---|---|---|
| **ka59 (sokoban-explode-chase)** | Both have "click sets in motion a coloured-block dynamic"; ka59 has trigger blocks that detonate ricochets pushing neighbours. | ka59's player drives an active **moving block** (slides via arrow keys) and explosions DISPLACE NEIGHBOURING BLOCKS (every neighbour shifts one cell). qn7w has no player avatar that moves on the grid — the player only clicks pusher knobs — and the chain's intermediate balls are **explicitly stationary**; the only thing that moves is the terminal ball, by exactly one cell along the chain's axis. ka59 spreads displacement; qn7w concentrates it. |
| **r11l (centroid-puppet-leg)** | Both use ACTION6 click as the only verb. | r11l clicks **a destination cell** to throw a tray-leg piece across the grid; multiple legs can be in flight; head-piece follows centroid of legs. qn7w clicks **a specific pusher-knob sprite**; the pulse's destination is determined by the chain's geometry (not by where the player clicks); only one ball ever ejects per click, and it travels at most one cell or until it hits something. |
| **bp35 (gravity-fall-navigation)** | Both can have "click portal-style sprites that move pieces". | bp35's player auto-falls; click teleports a player avatar through portal pairs. qn7w has no falling, no portals, no player avatar — pulses propagate through pre-placed touching ball-chains, not through grid-distant teleports. |
| **vc33 (row-column-swap-stripe)** | Both are pure-click games with tagged "trigger" cells. | vc33 clicks a marker tile (`ZGd`) to **swap stones across rows/columns** (every stone in the row moves). qn7w clicks a pusher knob to **eject one ball off the chain end**; intermediate balls do not move and the chain shortens by one each pulse. |
| **lp85 (row-col-shift-grid)** | Both use only ACTION6. | lp85's button click applies a **predefined permutation of every cell in a row/column**. qn7w's pusher click moves **exactly one cell** (the terminal ball) and leaves every other cell untouched. |

### Prior-games near-misses

| Prior | Surface overlap | Concrete distinguishing rule |
|---|---|---|
| **vn8d (domino-cascade-topple)** | Both are click-triggered cascade-type mechanics with "specialty cells" (vn8d: burst-pads / rotator-pads; qn7w: junction nodes). | vn8d's cascade is **distributional**: every pillar in the chain topples (visible state change in every cell), burst-pads splay outward in all 4 directions, rotator-pads turn corners — energy spreads from the click point outward. qn7w's pulse is **concentrational**: every intermediate ball stays in its position with no state change; the *only* visible movement is the terminal ball ejecting. The rule difference is binary — vn8d's mid-cells move; qn7w's mid-cells do not. The visual signatures are also very different: vn8d's cells get knocked down (reduced to flat shapes); qn7w's chain shortens by one at the terminal end while the body of the chain remains structurally identical. |
| **kp9z (grain-accumulate-topple)** | Both involve "click triggers a flow that ends at sinks". | kp9z is a **sandpile cellular automaton**: each cell holds an integer grain count, overflows at capacity 4 to all 4 cardinal neighbours, with rotatable redirectors forwarding one grain in their direction. Cells have a continuous integer state. qn7w's chain cells have **no per-cell state at all** — they're just present-or-absent ball sprites; there is no per-cell counter, no overflow threshold, no neighbour-broadcast. A pulse fires once and transmits along a 1-D chain, ejecting only the terminal. |
| **ka59 (also a prior-relevant near-miss)** | Same as taxonomy entry above. | (See above.) |
| **kn58 (anchor-pull-magnet)** | Both have "click triggers piece movement along axis". | kn58's click places a **single global anchor** that pulls *every* coloured pawn one cell along its dominant Manhattan axis. qn7w's click acts on **one specific chain only**; only the terminal ball of that chain moves; pawns/balls on unrelated chains are unaffected. |
| **bx84 (beam-mirror-reflect)** | Both involve a "signal travels along a path from emitter to target". | bx84's beam travels along **line-of-sight** in straight cardinal lines through *empty* cells, reflecting off mirror sprites; the beam is a continuous path of cells lighting up. qn7w's pulse travels along a **physical chain of touching ball sprites** (not LOS through empty cells); no cells light up along the path; only the terminal ball moves. The chain is a placed object, not a line of empty cells. |
| **xn5p (chamber-stamp-partition)** | Both involve a "stamping/triggering" element. | xn5p's pawn walks the chamber and stamps wall-cells to subdivide a connected region into per-colour subregions — the mechanic is **topological partition**, with the player creating walls. qn7w has no walking, no wall-stamping, no region partition; it is momentum transfer through pre-placed chains. |
| **gx7m (gear-mesh-cascade)** | Both can be "rotational/transmissive cascade through coupled elements". | gx7m's discs *all rotate* when their cardinal neighbours rotate (with sign flip across mesh); every disc in the connected component visibly spins. qn7w's chain balls explicitly do *not* move when the pulse passes; only the terminal ball ejects. |
| **rk7x (live-switch-routing)** | Both have junction-style routing. | rk7x has an **autonomous coloured courier** that walks one cell per click; player toggles junction blades to route it. qn7w has no autonomous mover and no per-click micro-step; one click triggers an instantaneous pulse with one terminal eject. |
| **vd3g (mound-and-marble-routing)** | Both involve flow toward targets. | vd3g toggles binary terrain HIGH/LOW and lets marbles flow downhill across many cells. qn7w has no terrain editing, no gravity flow, no multi-cell marble travel — pulse moves exactly one ball one step. |
| **wt39 (glide-deflect-thaw)** | Both involve "object slides until something". | wt39's pawn glides in pressed direction until wall; bumpers deflect 90°. qn7w has no glide — pulses are instantaneous along chains and the only travelling object is the ejected terminal ball, which moves a single cell off the chain. |

For all other prior entries (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, fz5j, zk9p, vp6h, zd7m, lv4k, mr5q, pf3w, tg6w, jd4q, ek73, tm5x, qx7p, kj82, nb6t), the family-level check (`mechanic_family` tag comparison + first-two-words split) finds no overlap. None share a "chain / pulse / eject" or "Newton's cradle" descriptor.

## Negative similarity check (`negative-similarity-check.md`)

Walking the eight dimensions against the closest-feeling prior, **vn8d (domino-cascade-topple)**:

| # | Dimension | vn8d | qn7w (pulse-chain-eject) | Shared? |
|---|---|---|---|---|
| 1 | What's on the board | Pillars, burst-pads, rotator-pads, target lights | Ball-chains on rails, pusher knobs, target sockets, junction nodes | **Different** |
| 2 | Player physical action | Single click on a pillar to topple it | Single click on a pusher knob to fire a pulse | Shared (both single-click triggers) |
| 3 | What level asks for | Light up all targets via a multi-direction cascade | Eject balls into matching-colour target sockets | Different (qn7w is *terminal-only*; vn8d is *every cell visited*) |
| 4 | What kills | Step budget | Step budget | Shared (universal across the corpus) |
| 5 | Supporting elements | Burst-pads / rotator-pads (modulate cascade direction) | Junction nodes (gate which branch ejects); merge-pads (fuse two arrivals) | Different (qn7w's specialty cells affect *which* terminal moves; vn8d's affect *which directions* the cascade spreads) |
| 6 | **Visual signature** (heavy axis) | Toppled pillars, "everything fell over" aesthetic | Linear ball-chains with detailed round balls, distinct pusher knobs, hollow target sockets, ball flying off the end | **Different** |
| 7 | **Pixel grain of primary sprites** (heavy axis) | Pillar-shaped cells (likely small uniform blocks) | Round balls with internal pixel pattern (highlight, shadow); distinct pusher-knob shape with a protruding handle; sockets with hollow ring; chain rails as 3-pixel rules | **Different** |
| 8 | **Core dynamic** (heavy axis) | Cascade *distributes* energy: every pillar in the cascade falls; the cascade can branch in 4 directions via burst-pads | Pulse *concentrates* energy: every intermediate ball stays put; only the terminal ball moves; energy passes invisibly through the body of the chain | **Different** (this is the binary distinguishing feature) |

Shared dimensions: **2 strongly (the click verb), 4 strongly (universal step budget); 3 only weakly ("hit targets" is a generic puzzle-game goal)**. Diverges on dimensions **1, 5, 6, 7, 8** — including all three "heavy" axes (6, 7, 8). This is well below the 3+ rejection threshold *and* well below the threshold weighted toward the heavy axes. **Pass.**

Cross-checking against second-closest prior **kp9z (grain-accumulate-topple)**: shared on dimensions 2, 4 only; differs on 1, 3, 5, 6, 7, 8 (kp9z has per-cell integer state, 4-direction overflow, sinks-as-collectors, sandpile aesthetic vs qn7w's stateless touching-ball chain with concentrational dynamics). **Pass.**

Cross-checking against **bx84 (beam-mirror-reflect)**: shared on dimensions 2 (click), 4 (budget); differs on 1 (beam line-of-sight vs touching-ball chain), 6 (light beam vs balls), 7 (line beam vs round balls + pusher knobs), 8 (LOS reflection vs momentum transmission with terminal-only motion). **Pass.**

## Summary verdict
Verdict: **NOVEL**. Family is absent from the 25-game taxonomy and from the 33-entry prior-games corpus. Positive similarity-check produces concrete distinguishing rules against every near-miss; negative similarity-check passes (≤ 2 strong shared dimensions against any prior; divergence on all three heavy axes). Proceed to `write_spec` with id=`qn7w` and family `pulse-chain-eject`.
