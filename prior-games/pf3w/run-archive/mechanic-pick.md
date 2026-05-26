# Mechanic Pick — `pf3w`

## Run inputs
- Seed: (autonomous; no seed provided)

## 4-character ID
**`pf3w`** — verified non-colliding:
- Not in the 25 reserved reference IDs (`ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30`).
- Not in `prior-games/index.md` (24 priors as of run start: `kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q`).
- Lowercase alphanumeric, four characters, mixes letters and a digit, not a recognisable English word.

## Mechanic family tag
**`wavefront-converge-timing`**

## One-paragraph mechanic description

The board is a square chamber that contains zero or more "target" sprites — small colored ring-icons at fixed cells — and the player has only two verbs. **ACTION6 (click)** drops a "pulse-emitter" sprite at the clicked empty cell: a 3×3 disk with a colored center matching one of the target colors plus a thin counter-ring around it. **ACTION5 (tick)** advances the world by one global pulse-tick. On every tick, every emitter's outgoing wavefront expands by one cell of BFS distance through the open chamber (walls block, the wavefront flows around them); the wavefront's *current frontier* — the set of cells whose BFS distance from the emitter equals (ticks since that emitter was placed) — is rendered as a colored 1-pixel outline matching the emitter's color, and the rendered ring grows outward in lockstep with the tick count. A target's center pixel "lights up" (changes from a hollow ring to a filled colored square) on the *single* tick when the matching-color wavefront's frontier passes through its cell — the next tick the frontier has already moved past, so the target's center returns to hollow. **The level wins on the single tick when every target is simultaneously lit; if step-budget runs out without that synchronization, the level loses.** Because the player chooses *when* (which inter-tick gap) to place each emitter, the game becomes a planning puzzle over emitter *placement* (which color at which cell) and emitter *timing* (how many ticks elapse between placements), constrained by the BFS distance from each emitter to its assigned target through the maze. L2 introduces multi-target synchronization (two targets at different distances from their emitter cells require staggered placement to converge on the same tick); L3 introduces walls that route the BFS around them and color-keyed targets that need a specifically-colored emitter, forcing the player to compose distance, timing, color, and routing simultaneously.

## Core knowledge priors used

| Prior | How it's used |
|---|---|
| Objectness | Emitters and targets are coherent persistent sprites at fixed cells; rendered wavefront frontiers are derived but visually distinct objects. |
| Basic geometry & topology | The wavefront is a *level-set* (cells equidistant from an emitter under graph-BFS); walls in L3 make the BFS metric topology-dependent (a target close in Euclidean distance can be far in BFS distance because the front must walk around a wall). |
| Basic physics | The intuitive "ripple from a pebble in water" — a wave-front expanding outward from a source, propagating one unit per tick — gives the player an immediate physical analogue. |
| Agentness | NOT load-bearing. No autonomous adversary or pursuer; the world is purely reactive to the player's `ACTION5` ticks. |

Three priors load-bearing (objectness, geometry-topology, physics), no agentness — keeps the puzzle planning-pure rather than dodging-pure.

## Action enum

`available_actions = [5, 6]` — pure click + global-tick. Slots 1-4 (cardinal motion) are *deliberately omitted* — there is no avatar to walk and the player cannot nudge an individual sprite. Slot 7 (undo) is also omitted; backing out of a misplaced emitter requires re-running the level (step counter is generous enough). Random-policy resistance comes from this minimalism: with only "click somewhere" and "tick", random play has near-zero chance of producing the right placements at the right inter-tick gaps for L2/L3.

## Novelty check — vs. the 25 reference games

For each potentially-relevant entry in `taxonomy-of-25-games.md` (verified by reading `mechanism-details/<id>.md` for each near-miss):

| Reference | Family overlap? | Description overlap? | Distinguishing rule (concrete) |
|---|---|---|---|
| **cd82** (orbit-fire-paint) | partial — both involve a ring/wavefront-style visual | partial — cd82 emits a basket along an 8-slot RING ORBIT and stamps colour over a HALF/WEDGE of the canvas. | cd82's basket travels on a single 8-cell cyclic ORBIT (1D), and its "fire" verb stamps a fixed half-canvas region in one shot. `pf3w`'s wavefront is omnidirectional BFS-radius expansion through a 2D chamber with wall-routing — the emitter never moves; only its level-set radius does. cd82 has no time-elapsed-between-placements axis at all. |
| **sp80** (pour-shelf-route) | partial — both use a "commit a flow then watch it propagate" verb | partial — sp80 commits ACTION5 and a per-cell liquid simulation runs frame-by-frame with bend-rules around pipes/sinks. | sp80's commit triggers a *single deterministic spill* per `ACTION5`, after which the world resets to "change" mode for the player to rearrange pieces. `pf3w`'s `ACTION5` is the *only* time-advancement verb, applied repeatedly to a *persistent* world state — emitters never reset, the puzzle is precisely about how many ticks elapse between placements. sp80's verb is "lay pipes then run a 1-shot sim"; `pf3w`'s is "place emitters whose level-sets co-evolve over many ticks". |
| **bp35** (gravity-fall-navigation) | none | none | bp35 has a player avatar that side-steps while gravity falls. `pf3w` has no player avatar at all. Mentioned only because both share an "animation runs over multiple frames" feel; nothing else aligns. |
| **g50t** (walk-vs-scroll) | partial — both include a visible "phase counter" the player races against | partial — g50t has a scrolling timer and ghost-replay of past walks. | g50t's player walks an avatar with arrow keys and presses ACTION5 to commit the path as a ghost. `pf3w` has zero arrow keys and zero avatar; its only clock is the ACTION5 tick advance. The "ghost" idea (replay of past attempts) is fundamentally different from "live wavefront expanding from a fixed-position emitter". |
| **ka59** (sokoban-explode-chase) | partial — both feature a "trigger that fans out" | partial — ka59's trigger blocks detonate and ricochet pawns one cell in the orthogonal direction. | ka59's detonation is a single 1-step cardinal push to immediate neighbours per fired trigger, not a continuously-expanding wavefront over arbitrarily many ticks. `pf3w`'s wavefront expands by one BFS-distance unit *per ACTION5* and continues forever; ka59's ricochet is a 4-frame animation that ends. |
| **re86** (frame-paint-canvas) | none meaningful | none | re86 has frame sprites the player slides across a hidden canvas. No tick mechanic, no wavefront, no synchronization. |
| **ft09** (stamp-3x3-paint) | none | none | ft09 stamps a 3×3 colour pattern at the click site, fixed-pattern. `pf3w`'s click drops an emitter that emits over many ticks. Nothing else aligns. |

No reference game uses a **multi-source wavefront synchronization** dynamic. The closest in surface signature (cd82's ring, sp80's flow-sim) diverge sharply on the load-bearing axis: `pf3w`'s puzzle IS the inter-emitter timing offset, which neither reference game has any analogue of.

## Novelty check — vs. `prior-games/index.md` (24 priors)

The priors most likely to share surface signature with `pf3w` are `bx84` (beam emitter + propagation), `vp6h` (lantern light cones), `gv47` (seed-grow-and-surround), `vn8d` (domino-cascade), `kp9z` (grain-accumulate-topple), and `gx7m` (gear-mesh-cascade). Each is checked against both the positive `similarity-check.md` test and the negative `negative-similarity-check.md` test.

### vs. bx84 (beam-mirror-reflect)
- **Family:** `beam-mirror-reflect` vs `wavefront-converge-timing` — first words diverge ("beam" vs "wavefront"); descriptions diverge.
- **Win condition:** bx84 = beam reaches target receivers via mirror-routed reflection. `pf3w` = all targets simultaneously lit on a single tick by their matching-color wavefronts. Different (bx84 has no synchronization-of-arrivals constraint; even if a beam reaches multiple receivers, they fire whenever the beam visits them, not on a single tick).
- **Primary action:** bx84 = click empty cell to drop a mirror; click mirror to cycle orientation. `pf3w` = click empty cell to drop an emitter; ACTION5 to tick globally. **There is no orientation/rotation in `pf3w` and no mirrors at all.** Different.
- **Primary constraint:** bx84 = beam is a 1D directed line, requires mirrors to reach off-axis targets. `pf3w` = wavefront is a 2D BFS frontier that automatically flows around walls; no mirrors needed. Geometrically different (1D directed vs 2D radial).
- **Distinguishing rule:** bx84's player agency is *spatial* (where to drop mirrors so the beam path threads through targets). `pf3w`'s player agency is *spatial AND temporal* (where AND when to drop emitters so multiple wavefronts arrive at multiple targets on the same tick). The temporal axis is absent from bx84 — bx84's beam is a single instantaneous line; `pf3w`'s wavefront is a per-tick-advancing level-set.
- **Negative-similarity walk (8 dimensions, threshold = 3+):**
  1. Board: both have emitters + targets + walls → SHARED.
  2. Player input: bx84 click-mirror-rotate; `pf3w` click-place + ACTION5 → DIFFERENT (no rotate, no mirror sprite kind in `pf3w`; ACTION5-tick is novel).
  3. Asks: bx84 route beam through receivers; `pf3w` synchronize multi-source arrivals → DIFFERENT (no sync axis in bx84).
  4. Kills: both step counter → SHARED.
  5. Cast: bx84 has emitter+mirrors+filters+prism+receivers; `pf3w` has emitters+walls+targets, NO mirrors NO prisms NO splitting. mostly DIFFERENT (only walls are shared cast).
  6. Visual signature: bx84 yellow horizontal beam on black with yellow-bordered target sprites (per the rendered level_1.png); `pf3w` will use a different palette (e.g., palette `{1 cream-bg, 3 wall-grey, 6 magenta-emitter1, 14 green-emitter2, 11 yellow-target-fill, 9 blue-emitter3}` with multi-pixel ring sprites for emitters and concentric BFS-distance frontiers rendered as outlines). DIFFERENT.
  7. Pixel grain: bx84 uses 1-cell beam pixels and small 3×3 emitter / target sprites. `pf3w` uses 3×3 emitters with internal counter-ring AND target sprites with hollow-ring + center-pixel design (for "lit/unlit" cue) plus the rendered wavefront outlines themselves. DIFFERENT (more sub-cell structure on emitter and target sprites; the wavefront outline IS the fill pattern).
  8. Core dynamic: bx84 = "deflect a 1D beam path with mirrors to thread through receivers". `pf3w` = "place multiple radial-wavefront emitters whose level-sets converge simultaneously on multiple targets, choosing the inter-emitter tick gap". DIFFERENT.
  - **Shared count: 2 of 8 (dimensions 1, 4)** — well below the 3+ rejection threshold. The heavy-weighted dimensions (6, 7, 8) all diverge. PASS.

### vs. vp6h (shadow-cast-collect)
- **Family:** `shadow-cast-collect` vs `wavefront-converge-timing` — disjoint roots.
- **Win condition:** vp6h = collect crystals by walking onto cells shaded by every active rail-mounted lantern. `pf3w` = synchronize wavefronts at fixed targets, no walking.
- **Primary action:** vp6h = arrow keys (avatar walks). `pf3w` = ACTION5 + ACTION6 (no avatar, no arrows).
- **Primary constraint:** vp6h = lantern positions are FIXED at level start (player moves the avatar through shadow patterns). `pf3w` = emitter positions are PLAYER-CHOSEN at runtime by clicking.
- **Distinguishing rule:** vp6h has *static lighting* and a *moving player*; `pf3w` has *moving lighting* (radial wavefronts that grow tick-by-tick) and *no player avatar at all*. The verb cardinality is inverted — vp6h is arrow-only, `pf3w` is click+commit-tick.
- **Negative-similarity walk:**
  1. Board: vp6h has avatar + crystals + lanterns; `pf3w` has emitters + targets → PARTIAL (both have "things on a grid" but different cast).
  2. Input: arrow-only vs click+ACTION5 → DIFFERENT.
  3. Asks: vp6h walk-into-cells; `pf3w` synchronize radial fronts → DIFFERENT.
  4. Kills: both step budget → SHARED.
  5. Cast: vp6h avatar+crystals+rail-lanterns; `pf3w` emitters+colour-targets → mostly DIFFERENT.
  6. Visual: vp6h grey + dark grey + magenta avatar (per rendered level_1.png); `pf3w` will use a different palette with cream/grey backdrop + colored emitter centers (magenta/green/blue) and yellow target rings. DIFFERENT.
  7. Pixel grain: vp6h uses 2×2 cells for sprites; `pf3w` uses 3×3 multi-pixel emitter rings, 3×3 target rings, plus rendered wavefront outlines. DIFFERENT.
  8. Core dynamic: vp6h = "walk into shaded cells"; `pf3w` = "place + tick to synchronize radial fronts at fixed cells". DIFFERENT.
  - Shared count: 1 of 8 (dim 4). PASS.

### vs. gv47 (seed-grow-surround-dissolve)
- **Family:** `seed-grow-surround-dissolve` vs `wavefront-converge-timing` — first words diverge ("seed-grow" vs "wavefront-converge").
- **Win condition:** gv47 = surround coloured pips with same-coloured paint (auto-dissolves the ring). `pf3w` = simultaneous arrival of wavefronts at targets.
- **Primary action:** gv47 = click a seed to grow its persistent paint region by one ring (the region accumulates each click). `pf3w` = click empty cell to PLACE an emitter (a new sprite kind), then `ACTION5` advances all emitters together.
- **Distinguishing rule:** gv47's regions ACCUMULATE — every painted cell stays painted forever after that click. `pf3w`'s wavefront is a *level-set frontier* — only the cells at exact BFS distance R from the emitter are highlighted on tick R, and on tick R+1 those cells are no longer highlighted (the frontier has moved outward). gv47's win condition is *spatial* ("paint surrounds pip"); `pf3w`'s win condition is *temporal* ("targets all lit on the same tick"). The two share "click drops a propagation source" but on every other axis they diverge.
- **Negative-similarity walk:**
  1. Board: both have a chamber with colored sprites → PARTIAL.
  2. Input: gv47 click-grow + ACTION5-mix; `pf3w` click-place + ACTION5-tick → PARTIAL on click-as-input but DIFFERENT on ACTION5 semantics (mix vs tick).
  3. Asks: gv47 region-paint surrounds pip (spatial); `pf3w` wavefront frontiers converge at targets (temporal-spatial) → DIFFERENT.
  4. Kills: both step budget → SHARED.
  5. Cast: gv47 seeds + pips + paint regions; `pf3w` emitters + targets + walls + wavefront outlines → DIFFERENT (no paint accumulation in `pf3w`).
  6. Visual: gv47 grey backdrop + yellow seeds + dark-grey pips (per rendered level_1.png shows yellow squares with white-pixel centers and dark blocks); `pf3w` will use cream backdrop + multi-color emitter centers + yellow target rings + visible BFS-frontier outlines. DIFFERENT (the rendered frontier is a wholly new visual element absent from gv47).
  7. Pixel grain: gv47 uses 4×4 seed sprites with center pixels (yellow with white center); `pf3w` will use 3×3 emitters with colored center + counter-ring + target ring with center-fill cue. Comparable grain but different sprite design.
  8. Core dynamic: gv47 = "click to accumulate per-region paint, surround pip"; `pf3w` = "click to place radial-wavefront emitter, time placements so frontiers converge". DIFFERENT.
  - Shared count: 2-3 of 8 (dims 1, 2-partial, 4) — borderline 2-3. Heavy-weighted dimension 6, 7, 8 all DIFFERENT. PASS (the load-bearing distinction is "accumulating regions" vs "transient frontiers", which is a coarse-axis divergence).

### vs. vn8d (domino-cascade-topple)
- **Family:** `domino-cascade-topple` vs `wavefront-converge-timing` — disjoint roots.
- **Win condition:** vn8d = topple every required pillar. `pf3w` = synchronize.
- **Primary action:** vn8d = click an empty cell to place a topple-source; chain reaction propagates instantly through pillar graph. `pf3w` = click an empty cell to place emitter; wavefront propagates radially over MANY ticks, each tick advanced by `ACTION5`.
- **Distinguishing rule:** vn8d's cascade is *single-shot per click* (the chain reaction runs to completion in animation, then halts). `pf3w`'s wavefront is *persistent and per-tick* (it expands by 1 BFS step per `ACTION5` and never halts until level ends). vn8d has no `ACTION5` (only ACTION6); `pf3w` has no chain-trigger logic at all (every emitter advances independently and identically per global tick).
- **Negative-similarity walk:**
  1. Board: both have a chamber with sources + walls → SHARED.
  2. Input: vn8d ACTION6 only; `pf3w` ACTION5 + ACTION6 → DIFFERENT (vn8d has no global-tick verb).
  3. Asks: vn8d topple-all; `pf3w` synchronize-at-tick → DIFFERENT.
  4. Kills: both step budget → SHARED.
  5. Cast: vn8d pillars + burst-pads + rotator-pads; `pf3w` emitters + targets + walls (no per-cell-binary-state pillars) → DIFFERENT.
  6. Visual: different. (vn8d uses pillar sprites with directional spinner-pads; `pf3w` uses multi-color emitter rings + frontier outlines). DIFFERENT.
  7. Pixel grain: comparable but different sprite design. Mildly DIFFERENT.
  8. Core dynamic: vn8d = "trigger a graph-based binary topple cascade"; `pf3w` = "place radial wavefronts and time their convergence". DIFFERENT.
  - Shared count: 2 of 8 (dims 1, 4). PASS.

### vs. kp9z (grain-accumulate-topple)
- **Family:** `grain-accumulate-topple` vs `wavefront-converge-timing` — disjoint roots.
- **Win condition:** kp9z = absorb a target number of grains at sinks. `pf3w` = synchronize wavefronts at targets.
- **Primary action:** kp9z = click a grain source to drop one grain; cells topple at capacity 4. `pf3w` = click empty cell + ACTION5.
- **Distinguishing rule:** kp9z's propagation is *cell-capacity overflow* (a cell holding 4 grains spills 1 to each cardinal neighbour). `pf3w` has no per-cell capacity at all — the wavefront is a level-set, not a particle count. kp9z has no synchronization-of-arrivals; `pf3w` has no per-cell counter.
- **Negative-similarity walk:**
  1. Board: kp9z is a cell-grid with grain stocks per cell; `pf3w` is a chamber with emitter+target+wall sprites → PARTIAL (both grids).
  2. Input: kp9z click + click; `pf3w` click + ACTION5 → DIFFERENT.
  3. Asks: kp9z fill-target-counts; `pf3w` synchronize-arrivals → DIFFERENT.
  4. Kills: both step budget → SHARED.
  5. Cast: kp9z grains + sources + sinks + redirectors; `pf3w` emitters + targets + walls (no redirectors, no sinks) → DIFFERENT.
  6. Visual: kp9z renders cells with mini-icons inside (red/green/pink dots inside grey cells per rendered level_1.png); `pf3w` will render emitter sprites + outward-rippling colored frontier outlines + ringed target sprites. DIFFERENT.
  7. Pixel grain: kp9z uses small mini-icon cells (~2×2 dots inside grey 4×4 cells); `pf3w` uses 3×3 emitter sprites with internal structure + frontier outlines + 3×3 target rings with center-fill. Comparable grain but different sprite design.
  8. Core dynamic: kp9z = "click sources, balance per-cell grain capacity to fill sinks"; `pf3w` = "click+tick so multi-source level-sets co-arrive at multiple targets". DIFFERENT.
  - Shared count: 2 of 8 (dims 1, 4). PASS.

### vs. gx7m (gear-mesh-cascade)
- **Family:** `gear-mesh-cascade` vs `wavefront-converge-timing` — disjoint roots.
- **Win condition:** gx7m = match a target rotation pattern across geared discs. `pf3w` = synchronize wavefronts.
- **Distinguishing rule:** gx7m propagates *signed rotation values* across a sparse cardinal-mesh graph; `pf3w` propagates *BFS distance frontiers* across a dense walkable chamber. gx7m has no spatial expansion at all — each gear has fixed position and only its rotation is the world variable. `pf3w` has emitters at variable positions and the world variable is the frontier set of cells.
- **Visual:** gx7m level_1.png shows 3 disc-sprites in a horizontal row with colored accent dots — minimalist and gear-like. `pf3w` will look fundamentally different (multi-color radial outlines on a chamber).
- **Negative-similarity walk:** shared count: 1 of 8 (dim 4). PASS.

## Novelty: vs preexisting video games (manual axis)

Closest preexisting genres:
- **Pinball / billiards** (a launched ball bounces around). `pf3w` is not ball-launching — there is no projectile that travels along a path; the wavefront expands omnidirectionally as a static-shape level-set, with no momentum or bounce.
- **Sonar / radar** (concentric pulses from a source). The mechanic of "concentric pulses" is the closest preexisting visual metaphor, but no preexisting *puzzle game* I am aware of is built around timing multi-source pulses to *converge simultaneously* at multiple receivers; sonar games are detection/dodging, not synchronization.
- **Music rhythm games** (timing inputs to align with beats). `pf3w`'s "place the right emitter at the right tick gap" has a faint rhythm flavour, but rhythm games' beats are externally-driven (the song); `pf3w`'s ticks are entirely player-driven (you press `ACTION5` when ready).
- **Tower-defence radial AOE abilities** (a tower fires an expanding ring). Tower-defence games are real-time dodging by enemy mobs of those AOEs; `pf3w` is turn-based with no mobs and the AOE *is* the puzzle.

No preexisting commercial video game I can think of is built around the *exact* mechanic of "place radial-distance emitters, choose inter-source tick gaps, synchronize convergence at multiple receivers". Sonar / radar imagery is the closest visual ancestor, but the puzzle structure is novel.

## How discovery works (no on-screen instructions)

L1 has 1 emitter and 1 target. The very first `ACTION6` click drops an emitter sprite — visibly distinct (3×3 with colored center + outer counter-ring). The player presses `ACTION5` and instantly sees a colored 1-cell-thick *outline* appear around the emitter at radius 1. A second `ACTION5` and the outline jumps outward to radius 2. After K presses, the outline reaches the target's cell, and the target's center pixel changes from hollow to filled (lit). Win triggers. The discoverable mechanic is:
- "Click drops something."
- "ACTION5 makes the something grow outward by one cell."
- "When the growing outline reaches the target, the target lights up and I win."

L2 introduces a second target at a different distance from the placeable emitter region. The L1 strategy ("place anywhere convenient and tick") fails — the second target lights on a different tick. The player learns: place TWO emitters, but stagger their placement times so both wavefronts converge simultaneously.

L3 introduces walls (BFS routing rather than Euclidean) and color-keyed targets (each emitter palette-pick must match the receiver's color). The player learns wall-routing by observation — the wavefront kinks around the wall as the rendered outline visibly does so.

## Per-level escalation preview (for write_spec)

- **L1**: M1 = "click-place emitter + ACTION5-tick → wavefront expands → reach single target". Single emitter, single target, no walls. Discoverability gate.
- **L2**: M1 + M2 = "M1 plus inter-emitter timing offset". Two emitters, two targets at distinct distances, no walls. The player must choose the *gap* between placing emitter A and emitter B such that both wavefronts arrive at their targets on the same tick.
- **L3**: M1 + M2 + M3 = "M1, M2, plus wall-routed BFS distance with color-keyed receivers". Two emitters of different colors (enforced by available emitter palette), two color-keyed targets, walls that re-shape BFS distance. Player must (a) choose which color emitter for which target, (b) choose placement positions taking BFS routing into account, (c) stagger placement timing so both arrivals coincide.

`pf3w`'s mechanic is novel along the full spec axis: positive `similarity-check.md` produces concrete distinguishing rules against every plausible-near-miss; negative `negative-similarity-check.md` puts every prior at ≤ 2 of 8 shared dimensions; preexisting-video-game novelty rests on the absence of a synchronization-puzzle built on this exact dynamic.
