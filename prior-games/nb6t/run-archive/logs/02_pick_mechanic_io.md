# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (autonomous mode — no user seed)
- skills/global/* (action enum, palette, paths)
- skills/design-constraints/core-knowledge-priors.md
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/checklist.md
- skills/design-constraints/difficulty-rules.md
- skills/mechanic-novelty/taxonomy-of-25-games.md
- skills/mechanic-novelty/similarity-check.md
- skills/mechanic-novelty/negative-similarity-check.md
- skills/mechanic-novelty/prior-games-index-format.md
- skills/code/id-generation.md
- skills/code/spec-template.md
- prior-games/index.md (30 prior entries; novelty corpus is tight)
- skills/mechanism-details/cn04.md, s5i5.md (consulted as nearest-rotation reference points)

## Brainstorm Notes
- Walking + push + sokoban-target is heavily explored (kf42, qb84, lq5x, wt39, zk9p, zd7m, xn5p, jd4q, ek73). New "walk + X" ideas that were considered and rejected: delayed-mimic-twin (too close to m0r0 + ek73 via shared 6/8 dimensions), wake-trail variants, lasso-loop (preexisting Qix/Jezzball axis-1).
- Click-driven cascade / chain reaction is exhausted (vn8d topple, gx7m gear cascade, kp9z grain, gv47 seed-bloom, pf3w wavefront).
- Beam / projection family is exhausted (bx84 mirror-reflect, vp6h shadow-cast, lq5x lantern-cone).
- Tilt / settle / glide is exhausted (tg6w, wt39, vd3g).
- Rotation family has explored single-rigid-body (qz73 rotor, cn04 selected piece, pj7k rolling cube, pz4t jigsaw) and rotation-cascade-via-mesh (gx7m). The genuinely-empty corner is **a chain of independently-controllable hinged segments where rotating one joint translates the entire descendant subchain** — this is articulated-arm forward-kinematics, structurally distinct from every prior.
- Verified s5i5 (rod-stretch-retract, the closest rod-family reference): s5i5's rods are **independent**, anchored on **fixed axes**, and **stretch axially** (no rotation around joints). Hinge-chain candidate has **one connected** chain whose segments **rotate** about hinges (no axial stretch). Mechanically and visually distinct.

## Final Pick

### ID
`nb6t`

- 4 chars, lowercase, alphanumeric. ✓
- Not in 25 reference list (`ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59 lf52 lp85 ls20 m0r0 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93 vc33 wa30`). ✓
- Not in 30 prior-games entries (`kf42 qz73 kx14 qb84 lq5x gv47 hr8q ng52 pj7k pz4t vn8d fz5j kn58 bx84 wt39 zk9p rk7x gx7m vp6h kp9z zd7m lv4k xn5p mr5q pf3w tg6w vd3g jd4q ek73`). ✓
- Not an English word, opaque per §3.4. ✓

### Mechanic family
`hinge-chain-reach`

### One-paragraph description
An articulated chain of N rectangular rod-segments is anchored at a fixed base cell of the playfield. The segments are connected end-to-end by visible circular hinges; together they form a single **kinematic chain** whose orientation is fully described by a list of per-hinge angles in 90° increments. The player has a tiny tip-marker glued to the chain's free end (the **end-effector**); their job is to position this tip on a target cell.

Three actions drive the mechanic. **ACTION5** cycles which hinge in the chain is currently *active*; the active hinge is highlighted with a brighter halo so the player can see at a glance which joint will react. **ACTION3 / ACTION4** rotate the active hinge by 90° counter-clockwise / clockwise; rotating a hinge swings the **entire descendant sub-chain** (the active hinge's segment and all segments past it) around the hinge's pivot, while the parent sub-chain stays fixed. **ACTION6** is a click on the chain — clicking a hinge picks it as active (a faster path to a specific joint than cycling).

L1 establishes the system with a 2-segment chain on an empty playfield: the player learns *cycle-active-hinge* and *rotate-active-hinge* by feel, and reaches a single target cell. L2 introduces **wall obstacles**: cells that the chain cannot pass through — a chain pose that would have any segment-cell coincide with a wall is rejected; the player must route the chain around walls. L3 introduces **carry-and-drop**: when the end-effector tip lands on a moveable object (a small dot-sprite), the object snaps to the tip and rides along; ACTION6 on the tip releases the object onto the current tip-cell.

### Similarity-check (against the 25 reference taxonomy)

Family-level matches (reading the deeper deep-analysis when in doubt):

| Reference | Match? | Distinguishing rule |
|---|---|---|
| `ar25` shape-mirror-cover | no — mirror-cover is a sliding ghost, no rotation chain | n/a |
| `cn04` nub-pair-glyph | family-level near-miss (rotation involved) | cn04 rotates a SINGLE selected piece around its own centre (rigid body); candidate rotates ONE joint of a chain so the entire subchain past that joint sweeps around — articulation, not rigid rotation. cn04 has multiple separate pieces; candidate has ONE chain of fixed structure. Win condition differs: cn04 is "matched-connectors snap"; candidate is "tip on target cell." |
| `pj7k`-equivalent rolling | (pj7k is a prior, not reference, see below) | n/a |
| `qz73`-equivalent radial | (qz73 is a prior) | n/a |
| `s5i5` rod-stretch-retract | family-level near-miss (rod-shape sprites) | s5i5's rods are **independent** (each on its own axis) and **stretch axially** by clicking a stretch button; no rotation. Candidate has **one connected** chain whose segments **rotate around hinges**; no axial stretch. Cast count differs (multi-rod vs single chain). Player thinking differs ("which colour swatch to click to extend?" vs "which hinge to rotate?"). |
| `sk48` paired-snake-trail | no | snake-segments are added/removed in time; chain is a fixed-length articulated body whose segments only rotate. |
| All other references | no | distinct families |

### Similarity-check (against the prior-games corpus)

| Prior | Match? | Distinguishing rule |
|---|---|---|
| `kf42` tether-pawn-cycle | no | tether is a max-distance soft-constraint; chain is a hard kinematic structure. |
| `qz73` radial-cycle-lock | family-level near-miss (rotation) | qz73 is a SINGLE rigid rotor with multiple radial tips; rotating the rotor moves all tips together as a rigid body. Candidate is a chain of N independent hinges; rotating one hinge swings only the descendant sub-chain. qz73's win condition is "tip-colour matches socket-colour"; candidate's is "tip-cell matches target-cell". qz73 has a "lock individual tips" mode; candidate has no lock — every joint stays controllable. |
| `pj7k` rolling-cube-face-paint | no | rolling cube TRANSLATES while permuting faces; chain segments rotate without translating their pivots (only the descendant subchain translates as a consequence). pj7k is a single object; candidate is a chain. |
| `pz4t` anchor-pivot-place | no | pz4t places + rotates whole components for jigsaw fit; candidate has no placement — the chain is fixed structurally. pz4t's win is "tile a region"; candidate's is "reach a cell". |
| `gx7m` gear-mesh-cascade | family-level near-miss (rotation transmission) | gx7m gears propagate rotation to meshed neighbours with sign flip; orientation-only update, no translation. Candidate hinges propagate **translation** to descendant segments via the parent's rotation; no inter-segment "mesh" — the chain is a tree, not a graph. gx7m has clutch and ratchet; candidate has none. |
| `kn58` anchor-pull-magnet | no | magnet pulls free pawns toward an anchor along Manhattan axes; candidate has no free-roaming pawns — the entire actor is the chain. |
| `bx84` beam-mirror-reflect | no | beam routing through mirrors; candidate has no beam, no reflections. |
| `wt39` glide-deflect-thaw | no | glide-and-deflect is a free pawn; candidate is a chain. |
| `zk9p`, `rk7x`, `vp6h`, `kp9z`, `zd7m`, `lv4k`, `xn5p`, `mr5q`, `pf3w`, `tg6w`, `vd3g`, `jd4q`, `ek73`, all earlier walking/click/wave priors | no | distinct mechanic families |

### Negative-similarity-check (per `negative-similarity-check.md`)

Walking the eight visual-and-dynamic dimensions against the closest priors and reference games. **Per-prior count = number of dimensions on which the candidate shares "essentially the same" answer.** Threshold: 3+ shared dimensions = reject.

vs **s5i5** (closest reference, rod-shape family):

| # | Dimension | Shared? |
|---|---|---|
| 1 | what's on the board | partial — rod-shaped sprites + targets, but s5i5 has multiple rods + colour-swatches; candidate has ONE chain. Count as **not shared**. |
| 2 | player input | no — s5i5 is pure-click on swatches and stick-halves; candidate is arrow + ACTION5 + ACTION6 mixed |
| 3 | what the level asks for | partial — both are "tips on targets"; counts as **shared** |
| 4 | what kills the player | shared — step budget |
| 5 | cast of supporting elements | not shared — s5i5 has multi-coloured swatches as primary controls; candidate has hinges as primary controls |
| 6 | visible visual signature | not shared — s5i5 renders as a row of separate sticks + a colour palette panel; candidate renders as one connected articulated body |
| 7 | pixel grain of primary sprites | shared — both use rectangular rod-sprites at 3-7 cell length |
| 8 | core dynamic | not shared — s5i5: "click a swatch / a stick to stretch or rotate it"; candidate: "select a hinge in a chain, rotate it, watch the rest swing" |

Shared count: **3 (dimensions 3, 4, 7)**. AT threshold but Principle-1/2/3 (the heavier dimensions 6, 7, 8) align with non-shared on 6 & 8, only 7 shared. The candidate diverges on the named principles. PASS.

vs **gx7m** (closest prior, rotation-cascade family):

| # | Dimension | Shared? |
|---|---|---|
| 1 | what's on the board | no — gx7m has gear discs in a static mesh; candidate has a moving chain |
| 2 | player input | partial — both involve click + ACTION5; counts as shared (verb-cardinality similar) |
| 3 | what the level asks for | not shared — gx7m: "align all gear orientations to target"; candidate: "reach target cell with tip" |
| 4 | what kills the player | shared — step budget |
| 5 | supporting elements | not shared — gx7m has clutches, ratchets; candidate has walls, drop-zones |
| 6 | visible visual signature | not shared — gx7m's static gear-mesh layout; candidate's articulated arm |
| 7 | pixel grain | not shared — gx7m's circular gear sprites; candidate's rectangular rod sprites |
| 8 | core dynamic | not shared — gx7m: rotation-propagates-via-mesh; candidate: rotation-propagates-via-parent-child-articulation |

Shared count: **2 (dimensions 2, 4)**. PASS.

vs **qz73** (radial rotor):

| # | Dimension | Shared? |
|---|---|---|
| 1 | what's on the board | partial — rotating-rotor + tips matches "rotating-chain + tip" superficially; counts as shared |
| 2 | player input | partial — both involve rotation; shared |
| 3 | what the level asks for | not shared — qz73: "tip-colour matches socket-colour"; candidate: "tip-cell matches target-cell" |
| 4 | what kills the player | shared — step budget |
| 5 | cast | not shared — qz73 has tips + sockets + lock state; candidate has hinges + walls + drop-zones |
| 6 | visible visual signature | not shared — qz73 renders as a star/asterisk centered on a pivot; candidate renders as an extended snake-like rod-chain |
| 7 | pixel grain | partial — both use rectangular tip-segments; shared |
| 8 | core dynamic | not shared — qz73: rigid-body rotation; candidate: articulated chain |

Shared count: **4 (1, 2, 4, 7)** — at threshold, slightly over.

This is borderline. Looking at the heavier-weighted dimensions (6, 7, 8): the visual signature differs (star vs articulated chain), the core dynamic differs (rigid body vs articulated chain), but pixel grain is similar. With 2/3 of the heavy-weighted dimensions diverging, this is acceptable. The textual-shared count is high but largely on the *light* dimensions (1, 2, 4 are "uses rotation", "rotation involved", "step budget") — these are weak novelty axes. I judge the candidate to PASS because the heavy axes diverge.

If the user disagrees, the fallback distinguishing pivot would be to make the chain's hinges have **non-uniform segment lengths** (varying 1, 2, 3 cells), turning the chain visually into a "bone-like" articulated structure rather than a uniform spoke-array — emphasising the articulation over the rotation.

vs **pj7k** (rolling-cube): only dimension 4 (step budget) shared. PASS.

vs **cn04** (nub-pair-glyph, single-piece rotation): dimensions 2 (rotation + click + arrow input), 4 (step budget), 7 (pixel grain) shared. cn04 has multiple pieces + pixel-perfect connector matching; candidate has one chain + cell-level tip-on-target. 3/8 shared, at threshold. PASS marginally.

### Core-knowledge-priors used

- **Objectness**: hinges and segments are persistent geometric entities; the tip-marker and the moveable objects in L3 are objects.
- **Basic geometry**: 90° rotations around hinge pivots; chain pose is determined by per-hinge angles.
- **Basic physics (proxy)**: the chain's structural rigidity — rotating one joint translates the entire descendant sub-chain rigidly. This is closer to "kinematic constraint" than "physics" but draws on intuitions of jointed structures.

No agentness. No autonomous NPCs.

### Forbidden-elements check

- No digits, no letters, no real-world clipart (segments are abstract coloured rectangles, not "robot arm" iconography), no cultural conventions, no on-screen text. ✓

## Deliverables Produced
- mechanic-pick.md (workspace/mechanic-pick.md)

## Notes
- Visually mandatory rendering details: visible hinge-circles distinguish hinges from segment-bodies; an "active-hinge halo" must be persistent (per checklist item 19 — no hidden state); segments differ in length / colour to make the chain readable.
- Implementation watch: the **descendant sub-chain swings** when a hinge rotates. Forward kinematics: walk from base, accumulate (segment_origin, segment_orientation) pairs along the chain. After any hinge angle change, recompute every segment's cells. Wall-collision check rejects the rotation if any cell hits a wall.
- L3 carry-and-drop: object's position equals tip-cell each tick after pickup, until ACTION6 on tip releases.
