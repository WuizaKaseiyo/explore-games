# Mechanic pick

## 4-character ID
`gx7m`

Verified: not in the 25 reserved IDs, not in `prior-games/index.md`,
not an English word (lowercase alphanumeric, opaque).

## Mechanic family tag
`gear-mesh-cascade`

## One-paragraph description

A small cluster of toothed-disc **gear sprites** sits on a grid, each
edge-to-edge with one or more cardinal neighbours along a fixed
mesh-graph. Every gear carries a single coloured **rim-mark** on
its 12-o'clock tooth. ACTION6 click on a gear's hub rotates THAT
gear one notch (45°) clockwise; the rotation propagates instantly
through every cardinally-meshed neighbour with the **sign flipped**
(neighbour rotates 45° counter-clockwise), and recursively through
the connected mesh component (sign flipping at each hop). The
puzzle is to drive every rim-mark onto its same-coloured
**target-indent** printed on the static **collar-ring** that frames
the gear. Levels 2 and 3 introduce a **ratchet gear** (a notched
disc that propagates rotation only in its currently-pointed
direction; the player cycles its direction by clicking its
external **direction-tang**) and a **clutch gear** (a disc whose
**lever-tang** can be clicked to engage / disengage the gear from
ALL its mesh-neighbours, so one click cuts one connected component
into two independently rotating components). All input is ACTION6;
`available_actions=[6]`. Step-counter HUD on row 0.

## Core-knowledge priors used (per `core-knowledge-priors.md`)

- **Objectness** — gears are persistent, distinct entities.
- **Geometry & topology** — rotation, mesh-adjacency graph, mark-to-
  target angular alignment, connected-component partitioning when a
  clutch disengages.
- **Physics** — gears with sign-flipping mesh transmission is a
  classic intuitive-mechanics rule.

Pillars covered (per `from-tech-report.md` § 1):

- Exploration: the cascade rule must be discovered (a single first
  click reveals neighbours rotating opposite).
- Modelling: once the rule is known, every action's effect is
  predictable across the whole connected component.
- Goal-setting: implicit — coloured target indents on each collar
  ring are visually coupled to the gear's rim-mark colour.
- Planning: the cascade couples gears, so reaching one mark's
  target may misalign another. L3 with clutch + ratchet creates
  multi-step planning depth.

## Action palette

`available_actions=[6]`. Pure click. Each click hits one of three
target kinds:

| Click target | Effect |
|---|---|
| Gear hub | Rotate that gear one notch CW; cascade propagates. |
| Ratchet direction-tang (L2+) | Cycle the ratchet's allowed direction (CW-only / CCW-only / blocked). |
| Clutch lever-tang (L3 only) | Toggle that clutch gear's engagement with its mesh-neighbours. |

This conforms to `action-enum.md`'s "distinctive-verb-on-ACTION6"
family (lp85, vc33, sc25, ft09, r11l) — the verb is encoded in
*what* is clicked, not in different action ids.

## Similarity check (positive — per `similarity-check.md`)

Walking every taxonomy row and prior-games row.

### Taxonomy near-misses

| Taxonomy entry | Family tag | Family-level match? | Description-level match? | Verdict |
|---|---|---|---|---|
| `qz73` (prior, but family seeds reasoning here too) | n/a | n/a | n/a | n/a |
| `cn04` | `nub-pair-glyph` | NO ("nub-pair" vs "gear-mesh" share zero word stems) | n/a | NOVEL |
| `ar25` | `shape-mirror-cover` | NO | n/a | NOVEL |
| `cd82` | `orbit-fire-paint` | NO | n/a | NOVEL |
| `lp85` | `row-col-shift-grid` | NO ("row-col" vs "gear-mesh") but click → fixed-permutation has a conceptual brush. **Description-level**: lp85's win is `every key sprite over its goal` (positional); gx7m's win is rim-mark angular alignment. Primary action: lp85 click → swap cells; gx7m click → rotate gear and cascade. Primary constraint: both use a step counter. Two of three differ. | NO | NOVEL |
| `s5i5` | `rod-stretch-retract` | NO | n/a | NOVEL |
| `dc22` | `colour-cycle-walk` | NO | n/a | NOVEL |
| `ls20` | `cycler-attribute-match` | NO; but "cycler" + "match" suggests possible overlap. **Description-level**: ls20 cycles a *single avatar's* shape/colour/rotation triplet via stepping on tiles; gx7m cycles individual gear angles via click cascade. Primary action: ls20 = walk; gx7m = click. Primary constraint: ls20 has enemies+lives; gx7m has none. | NO | NOVEL |
| `tr87` | `tape-rewrite-rule` | NO | n/a | NOVEL |
| `vc33` | `row-slide-pull-tab` | NO | n/a | NOVEL |
| All other 16 | various | NO at family-tag level | n/a | NOVEL |

No taxonomy row escalates past the description-level check. **No
distinguishing-rule paragraphs are required by similarity-check.md
for the 25 reference games.**

### Prior-games near-misses

The full list of 17 priors I evaluated:

| Prior | Family tag | Closest concern | Distinguishing rule |
|---|---|---|---|
| `kf42` | tether-pawn-cycle | None — different objects, different verb. | n/a |
| `qz73` | radial-cycle-lock | **POTENTIAL.** qz73 is "rotate central rotor of coloured tips, lock individual tips, align with same-coloured sockets". Both gx7m and qz73 ask the player to align rotated coloured marks with same-coloured outer-ring targets. | **(a) Object cardinality.** qz73 has ONE central rotor with embedded tips that all rotate together as one rigid body. gx7m has MANY independent gears arranged on a mesh. **(b) Propagation rule.** qz73 has no inter-rotor propagation (locked tips simply stop following the rotor). gx7m's defining mechanic IS sign-flipping rotational propagation through mesh-adjacency — clicking one gear immediately rotates every meshed neighbour in the opposite direction. **(c) Lock semantics.** qz73 locks an individual tip to *exclude* it from a single rotor's rotation. gx7m's clutch *partitions the mesh-graph* — disengaging a gear cuts the connected component into two pieces that now rotate independently of each other. The player's mental model is "graph of mutually-constrained rotations", not "rotor with selectively locked tips". |
| `kx14` | tide-tilt-buoyant | None — water tank vs gear cluster. | n/a |
| `qb84` | bead-lift-swap | None — chain navigation vs rotation cascade. | n/a |
| `lq5x` | lantern-cone-illuminate | None — light cone vs rotation. | n/a |
| `gv47` | seed-grow-surround-dissolve | None — paint regions vs gears. | n/a |
| `hr8q` | pair-blend-recipe | None — recipe formula vs gears. | n/a |
| `ng52` | multiset-signature-classify | None — classification vs gears. | n/a |
| `pj7k` | rolling-cube-face-paint | **POTENTIAL.** Both involve rotation + colour. | **(a) Object cardinality.** pj7k has one cube that physically rolls cell-to-cell, permuting its 6 faces. gx7m has many static gears that rotate in place. **(b) Action effect.** pj7k click moves the cube one cell, rotating the face indices; gx7m click stays in place and propagates rotation across mesh. **(c) Win condition.** pj7k wins by depositing a target painted-cell pattern via the cube's rolls; gx7m wins by aligning rim-marks to outer indents. The player's task in pj7k is path-planning a roller; in gx7m, it is solving a coupled rotational system. |
| `pz4t` | anchor-pivot-place | **POTENTIAL.** Both use rotation. | **(a)** pz4t is jigsaw-piece tiling (move + reflect + rotate to fit pieces into a region). gx7m is in-place rotation of gears with cascade. **(b)** pz4t's pieces are translated freely; gx7m's gears are positionally fixed. **(c)** pz4t's win is region-tiled-completely; gx7m's win is angular-mark-alignment. Different objects, different verbs, different goals. |
| `vn8d` | domino-cascade-topple | **POTENTIAL.** Both have "cascade". | **(a) Cascade type.** vn8d is a one-shot directional cascade — single click sends a chain reaction through pillars and the sim ends. gx7m's cascade is *bidirectional and instant* — the rotation propagates symmetrically through the mesh on every click and is then stable until the next click. **(b) Reversibility.** vn8d topples are irreversible (pillars stay down); gx7m is fully reversible (any rotation can be undone by 7 more clicks of the same gear). **(c) Object class.** vn8d has pillars + burst-pads + rotator-pads; gx7m has gears + ratchets + clutches. Different abstraction. |
| `fz5j` | phase-step-tile | None. | n/a |
| `kn58` | anchor-pull-magnet | **POTENTIAL.** Both have "single-click triggers global propagation". | **(a) What propagates.** kn58 propagates *translation* — every coloured pawn slides one cell toward the clicked anchor. gx7m propagates *rotation*. **(b) Object class.** kn58 has a clicked anchor + sliding pawns; gx7m has clicked gears in a mesh. **(c) Sign rule.** kn58 has no sign flipping (everything moves toward the anchor uniformly); gx7m's defining feature is per-mesh-edge sign flip. |
| `bx84` | beam-mirror-reflect | **POTENTIAL.** Both involve a propagating signal. | **(a) Signal type.** bx84 propagates a coloured beam through cells, reflecting off mirror sprites and recolouring through filters. gx7m propagates rotation through gear-mesh-adjacency, with sign flipping. **(b) Verb.** bx84 click drops/cycles a mirror at a cell; gx7m click rotates a gear in place. **(c) Win condition.** bx84 wins by routing the beam to a target; gx7m wins by per-gear angular alignment of marks. |
| `wt39` | glide-deflect-thaw | None. | n/a |
| `zk9p` | pursuer-merge-walk | None. | n/a |
| `rk7x` | live-switch-routing | None. | n/a |

## Negative similarity check (per `negative-similarity-check.md`)

Walking the 8 dimensions against every prior. The closest priors
for surface-overlap analysis are **qz73** (both ask for rotated-
mark-to-coloured-target alignment) and **bx84** (both involve
propagation through cells).

### Versus qz73

| Dimension | Shared? |
|---|---|
| 1. What is on the board | NO. qz73 has one central rotor with radiating tips on a sparse field; gx7m has multiple gears arranged in a mesh cluster. |
| 2. What player does | YES — clicks. (Cosmetic — many priors share this.) |
| 3. What level asks for | PARTIAL. Both ask "align colored mark to colored target". This is the strongest concern. |
| 4. What kills player | YES — step counter (universal). |
| 5. Supporting cast | qz73 has rotor + sockets. gx7m has gears + ring + lever-tangs (L3) + ratchet-tangs (L2). Different cast beyond "marks + targets". |
| 6. Visible visual signature | NO. qz73 (per its L1 frame, also re-rendered in `prior-games/qz73/run-archive/smoke-frames/level_1.png`) is one rotor on grey background with sparse 1×1 socket dots; gx7m has dense octagonal toothed-disc sprites with internal cog patterns occupying ~40% of the playfield. |
| 7. Pixel grain | NO. qz73 sprites are mostly thin radial bars (1×N rectangles); gx7m gears have rich 6×6 internal cog-tooth alternating pattern. Per Principle 1 of negative-similarity, gx7m has high pixel-detail richness. |
| 8. Core dynamic | NO. qz73 = "spin one rotor; lock individual tips so they don't follow." gx7m = "every click rotates a connected component of gears, with sign flipping at each mesh edge — figure out which gear-and-clicks-count to apply so the *whole graph's marks* land on targets simultaneously, knowing the cascade couples them." |

Total shared dimensions: 2 (cosmetic — input verb + universal step
counter), with one partial on dim 3. Dimensions 6, 7, 8 (the
heavy named principles) all diverge. Below the 3-dim threshold.
Pass.

### Versus bx84

| Dimension | Shared? |
|---|---|
| 1. What is on the board | NO. bx84 has a beam (coloured line) + mirror sprites + emitters; gx7m has gear sprites. |
| 2. What player does | NO. bx84 click drops or cycles a mirror at an empty cell; gx7m click rotates an existing gear. |
| 3. What level asks for | NO. bx84 = beam reaches target; gx7m = angular mark alignment. |
| 4. What kills player | YES — step counter (universal). |
| 5. Cast | NO. bx84 = mirrors/filters/prisms; gx7m = gears/ratchets/clutches. |
| 6. Visual signature | NO. bx84 has a vivid coloured beam line traversing the grid; gx7m has static dense gear cluster. |
| 7. Pixel grain | NO. bx84 mirror sprites are thin diagonals; gx7m gears are dense rounded shapes. |
| 8. Core dynamic | NO. bx84 = "compose a path for a single propagating beam"; gx7m = "rotate a coupled graph". |

Total shared: 1 (universal step counter). Pass.

### Versus all 15 other priors

Each shares at most dim 4 (universal step counter). All below the 3-
dim threshold.

### Versus the 25 reference games

The closest reference is **lp85** (click-only with permutation
applied to cells). Shared dims: 2 (verb = click; step counter).
Different on remaining 6 dims, including all 3 heavy principles.
Pass.

**Verdict: NOVEL.** The mechanic is original on both axes 1 (vs
preexisting video games — gear puzzles exist as a tabletop genre
but the sign-flipping mesh-cascade rule is rare and the 64×64
NovaPlay framing is unique) and axis 2 (vs the 25 + 17 prior
games — qz73 was the closest surface concern and clearly
diverges on the heavy principles).

## Visual signature plan (executed during write_spec / implement)

To diverge from qz73's `{4, 8, 9}`-dominant palette and from the
prior-games pattern of "small 1×1 pawns on empty field", gx7m
will use:

- **Letter-box / background**: maroon (palette 13) and off-black
  (palette 4) — outside playfield is maroon; inside is off-black.
- **Gears**: light-grey (2) ring + grey (3) cog teeth + per-gear
  rim-mark colour drawn from {pink 7, orange 12, light-blue 10,
  green 14}.
- **Collar-ring (target-indents)**: same per-gear hue as the
  rim-mark, drawn as a single coloured cell at the target angle.
- **Ratchet direction-tang**: yellow (11) external nub.
- **Clutch lever-tang**: purple (15) external nub.

This palette signature ({2, 3, 4, 13} structural + {7, 10, 12, 14}
mark colours + {11, 15} interaction tangs) is distinct from every
prior's recorded palette.
