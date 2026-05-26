# Mechanic Pick — ek73 — Wake-Trail Evade

## ID
**`ek73`** — 4 lowercase alphanumeric, not English, not in the 25 reference list, not in `prior-games/index.md`.

## Mechanic family
`wake-trail-evade`

## One-paragraph description
A single avatar walks one cell per arrow-press around a walled playfield to collect every coloured target item. The cell the avatar VACATES on each step is left behind as a glowing **wake** mark that lingers for K turns then fades — so behind the avatar, a short tail of recent footprints persists in the rendered frame. **Stepping onto an active wake cell loses the level**, so the player must plan paths that don't loop back into their own recent footprints. L1 establishes the base dynamic with K=3 and a tutorial layout where one hairpin turn is enough to teach "your own trail kills you, but only briefly". L2 adds **wake-clearer pads** — a small number of one-shot floor pads scattered in the level that, when stepped on, instantly erase every currently-active wake cell, letting the avatar back out of self-trapped corridors. L3 adds **wake-anchor cells** — stepping on an anchor freezes the entire current wake into permanent stone walls (palette-grey, immovable) for the rest of the level, turning the player's own trail into a structural element used to gate off zones. The L3 witness must walk through wake-decay corridors AND step on a clearer pad to recover from a deliberate self-trap AND step on an anchor at the right moment to permanently seal a side-passage so a final collectible behind a one-way bottleneck becomes reachable.

## Action palette
`available_actions=[1, 2, 3, 4]` — pure cardinal movement. ACTION5 is intentionally absent because the distinctive verb already lives in the consequence of arrow-pressing (the wake creation). Pure-arrow is one of the established subset patterns (~7/25 reference games) and avoids declaring a slot whose verb would be redundant.

## Action enum check
- ACTION1-4: walk one cell up/down/left/right. Movement is rejected (no-op, step counter still ticks) if the destination is a wall, off-grid, or an active wake cell — wait, NO — stepping on a wake cell is the LOSE condition, not a blocked move. The destination check that rejects a move is for walls and off-grid only. Wake cells are walkable (and lethal); the player must reason about that.
- Unused: 5, 6, 7. Documented absence per `action-enum.md`.

## Core-knowledge prior coverage
- **Objectness** — avatar, wake cells, collectibles, pads, anchors are all coherent persistent entities.
- **Basic geometry & topology** — central reasoning is about *which paths remain available given my own trail's decay schedule* — connectedness of the unblocked region as a function of time. Wake-anchor's "freeze trail into walls" is a topological transformation (turning a temporary boundary into a permanent one).
- **Basic physics** — minimal; no gravity, no momentum.
- **Agentness** — minimal; no NPCs, no chasers.

The pair (objectness + topology) is one of the under-represented corners of the priors-cube per `reference-game-patterns.md` § "Open questions": geometry+topology shows up in only a handful of reference games (`ar25`, `cn04`) and the player reasoning about own-trail-as-time-varying-boundary isn't covered by either.

---

## Similarity check (positive — `mechanic-novelty/similarity-check.md`)

Walking the candidate against every taxonomy entry and every prior-game entry. For each row I either record "no overlap" or articulate the concrete distinguishing rule.

### Taxonomy of 25 reference games

| ref | mechanic_family | overlap? | distinguishing rule |
|---|---|---|---|
| ar25 | shape-mirror-cover | no | reflectors copy-mirror sprites; no walking, no trail. |
| bp35 | gravity-fall-navigation | no | auto-falling avatar; no trail. |
| cd82 | orbit-fire-paint | no | basket on a ring stamps a canvas. |
| cn04 | nub-pair-glyph | no | rotate-translate jigsaw; click+arrow+ACTION5; no trail. |
| dc22 | colour-cycle-walk | no | trigger cycles every wedge; no own-trail constraint. |
| ft09 | stamp-3x3-paint | no | pure-click stamp game; no walking. |
| g50t | walk-vs-scroll (ghost-replay) | NEAR-MISS — both involve the player's past actions affecting the present. | g50t REPLAYS a committed path as a separate ghost and the player respawns at start; the past-self constraint is *positive* (covering targets via union of paths). ek73 has no commit/replay/respawn loop — the wake is a *negative* constraint (you can't step there) that tracks the live avatar continuously and decays per turn. |
| ka59 | sokoban-explode-chase | no | block-slide + detonation chains. |
| lf52 | fog-of-war-sokoban | no | block push under fog; no trail. |
| lp85 | row-col-shift-grid | no | Rubik permutation buttons. |
| ls20 | cycler-attribute-match | no | shape/colour/rotation match. |
| m0r0 | mirror-orb-merge | no | mirrored quad control. |
| r11l | centroid-puppet-leg | no | tray-leg throw with centroid head-follow. |
| re86 | flood-fill-multi-canvas | no | paint canvas via marker walk; no decaying trail constraint. |
| s5i5 | rod-stretch-retract | no | telescoping rods. |
| sb26 | mastermind-feedback | no | guess-row commit. |
| sc25 | spell-grid-pattern | no | spell-toggle 3×3. |
| sk48 | paired-snake-trail | NEAR-MISS — both are "avatar walks, trail of cells gets coloured behind it". | sk48's trail is *permanent* (every cell behind both heads stays coloured for the rest of the level) and the win predicate is *colour-match symmetry* between two heads' trails. ek73's trail is *temporary* (decays in K turns), there is only ONE avatar (no mirror-mate), and the trail is a *hazard the avatar must avoid*, not a *visible record to be matched*. |
| sp80 | liquid-flow-routing | no | piece-place + spill animation. |
| su15 | radial-blast-capture | no | click radial vacuum. |
| tn36 | program-shape-buttons | no | code-pad programming. |
| tr87 | symbol-cycle-rules | no | rewrite-rule symbol cycle. |
| tu93 | lockstep-multi-maze | no | every primary agent moves in lockstep; no decaying trail. |
| vc33 | row-column-swap-stripe | no | pure click row-shift swap. |
| wa30 | carry-pickup-drop | no | carrier with ACTION5 pick/drop. |

### Prior-games index (27 rows)

| prior | mechanic_family | overlap? | distinguishing rule |
|---|---|---|---|
| kf42 | tether-pawn-cycle | no | two-pawn tether with click-select; no own-trail. |
| qz73 | radial-cycle-lock | no | rotor + lock. |
| kx14 | tide-tilt-buoyant | no | water-level tank. |
| qb84 | bead-lift-swap | no | chain navigation with peg-swap. |
| lq5x | lantern-cone-illuminate | no | cone projection. |
| gv47 | seed-grow-surround-dissolve | no | region-grow paint by clicking seeds. |
| hr8q | pair-blend-recipe | no | click-2-ingredients blend. |
| ng52 | multiset-signature-classify | no | bin partition by stick signature. |
| pj7k | rolling-cube-face-paint | no | rolling cube deposits faces. |
| pz4t | anchor-pivot-place | no | piece placement with click-anchor. |
| vn8d | domino-cascade-topple | no | chain-reaction click. |
| fz5j | phase-step-tile | NEAR-MISS — both lose-on-step-on-bad-cell on a walk-around-grid game. | fz5j's bad cells are tiles whose period is **pre-determined and externally observable**; the player reads the level's clocks and times entry. ek73's bad cells are **player-created** by walking and **decay deterministically after a fixed number of the player's own moves**. Reasoning gate is "plan around the consequences of my own choices" vs "read the level's external timetable". Also fz5j has 3 lives + respawn; ek73 has zero lives — a single self-step ends the level. |
| kn58 | anchor-pull-magnet | no | one-shot magnet click. |
| bx84 | beam-mirror-reflect | no | beam + mirrors. |
| wt39 | glide-deflect-thaw | NEAR-MISS — both have "cell becomes brittle/changed after the avatar interacts with it". | wt39's avatar GLIDES (continues until wall) and brittle thaw-tiles **crack permanently after one slide** (one-way state change). ek73's avatar STEPS one cell at a time, the cell-state change is **temporary** (auto-reverts after K turns under normal play), and the change is the *vacated* cell becoming hazardous to the avatar — wt39's avatar glides on top of the brittle tile then off without consequence. Different verb (step vs glide), opposite directionality (temporary decay vs permanent crack), opposite causality (active hazard vs spent floor). |
| zk9p | pursuer-merge-walk | no | lure AI pursuers into self-collision. |
| rk7x | live-switch-routing | no | autonomous courier with junction toggles. |
| gx7m | gear-mesh-cascade | no | rotation propagation. |
| vp6h | shadow-cast-collect | no | shaded-by-lanterns cell mask. |
| kp9z | grain-accumulate-topple | no | sandpile capacity overflow. |
| zd7m | cohort-step-route | NEAR-MISS — both arrow-walk on a grid + step counter as the lose. | zd7m moves **every movable pawn** simultaneously per arrow press and the constraint is selectively-blocking anchors + sealed-chamber portals. ek73 has **a single avatar** and the constraint is its **own decaying trail behind it**. zd7m's cognitive load is "how do I route N pawns past obstacles together"; ek73's is "how do I route ONE pawn so its own past doesn't trap its future". Different cardinality of agents, different constraint source (level layout vs avatar-history). |
| lv4k | lever-balance-torque | no | torque sum. |
| xn5p | chamber-stamp-partition | no | walk + stamp walls to subdivide. (Player creates *intentional* walls; ek73 creates *consequential* walls via mere walking, and they decay.) |
| mr5q | polarity-attract-discharge | no | polarity flip + walk-toward. |
| pf3w | wavefront-converge-timing | no | BFS frontier timing. |
| tg6w | settle-pile-tilt | no | tilt + slide of loose blocks. |

**Result of positive check:** four near-miss flags (`g50t`, `sk48`, `fz5j`, `wt39`, `zd7m` — five actually). Each has a concrete distinguishing rule that survives the description-level test (win condition / primary action / primary constraint must all match for a reject; for each of these only one of those three matches).

---

## Similarity check (negative — `mechanic-novelty/negative-similarity-check.md`)

The positive check gives me arguments for novelty. The negative check asks the opposite question: *what does the candidate share with each prior, walking the eight dimensions?* I rendered ek73's L1 mentally (avatar at (3,3), 6 collectibles in a 16-cell walled chamber, brick-pattern walls) and reviewed `level_1.png` for the closest priors (`fz5j`, `wt39`, `zd7m`, `zk9p`, `sk48`).

Pre-emptive divergences engineered into the spec:

- **Dim 6 (visual signature / palette).** Avoid the kf42→vh68 cautionary `{4 wall, 8 red, 9 blue}` collapse. ek73's intended palette is **`{2 light-grey playfield, 4 off-black brick walls, 6 magenta wake, 11 yellow avatar, 12 orange collectibles, 14 green clearer-pads (L2), 13 maroon anchors (L3)}`** — wake-magenta + avatar-yellow is a colour pairing none of the priors I checked use prominently for primary sprites.
- **Dim 7 (pixel grain).** Avatar is rendered as a 5×5 sprite with an internal cross + eye dot pattern (not a 1×1 or solid 3×3 rectangle); collectibles are 4×4 four-pointed-star sprites with internal hollow centre; walls have a 2-pixel mortar pattern; wake cells are 4×4 sprites with a fading inner glyph (4-frame age states drawn as different internal patterns) — i.e., the wake cell's *internal pattern* encodes its remaining lifetime, so the player reads "this trail expires soon" off the screen alone.
- **Dim 8 (core dynamic).** "Plan around my own consequences" is genuinely distinct from every prior I walked — none of them have the player's recent input history visibly painted as constraint on subsequent input.

Closest concerning prior: **`fz5j` (phase-step-tile)** — shared dimensions: 1 (object-on-grid), 2 (walk-avatar), 4 (lose-on-step-on-bad-cell). That's three. The sharing-on-dim-4 is meaningful because both games punish stepping on a transient bad cell. **However** dim 8 is the heaviest and clearly diverges (player-created vs externally-clocked); dim 6 and 7 are engineered to diverge (different palette, different sprite grain — fz5j's red flower decoration + bright yellow markers + cyan square outlines on dark grey vs ek73's magenta-trail + yellow-cross-avatar + brick walls). Three shared dimensions of which *all three are the lighter ones* is below the qualitative bar set in the negative-similarity-check file ("sharing on dimensions 6, 7, or 8 is heavier"). **Accepted, with mitigations explicit in the spec.**

Other priors all overlap on at most 2 dimensions (dim 1 + dim 2 from "walk-on-grid" being a shared family) and diverge on 4-8. **No reject.**

---

## Open design questions for `write_spec`

Per `reference-game-patterns.md` § "Open questions for `pick_mechanic` to resolve":

- **Action palette**: pure arrow `[1,2,3,4]` (committed above).
- **Camera mode**: fixed-grid 64×64 with playfield grid_size something like 24×24 and `Camera(letter_box=PADDING_COLOR)` centring. (Decide exact grid_size in `write_spec`; aim for the larger end of the reference range so internal sprite detail reads at display-pixel resolution per checklist item 20.)
- **Resources**: just step-counter HUD (universal). No accumulating "captured count" needed; collectibles disappear visibly when picked up — the diff between original and current frame *is* the progress display.
- **Distinctive verb home**: arrow press IS the distinctive verb because it's what creates the wake. ACTION5 unused.
- **Core-knowledge prior pairing**: objectness + topology, with minor physics (the wake-anchor's "freeze into wall" reads as a kind of crystallisation but isn't really physics).

These choices feed straight into spec sections 1-3.
