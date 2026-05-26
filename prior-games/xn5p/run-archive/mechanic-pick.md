# Mechanic Pick — `xn5p`

## 4-character ID

`xn5p`

Verified non-collision:
- Not in the 25 reserved reference IDs.
- Not in the 22 entries of `prior-games/index.md` (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k).
- Not a recognisable English word; opaque per §3.4.

## Mechanic family tag

`chamber-stamp-partition`

## One-paragraph description

A pawn walks a single wall-bounded "chamber" populated by 2-3 colours of "molecule" sprites scattered inside the open region. The pawn moves with arrows; a press of ACTION5 **stamps** a permanent wall block at the pawn's current cell (the pawn remains; subsequent moves leave the stamp in place). A connectivity check runs after every action: the chamber's open cells are flood-filled into connected components, and the level wins the moment every component holds molecules of *exactly one colour* (and every colour is represented in some component). The player's job is to subdivide the chamber by stamping a separating barrier between the colour groups, navigating around molecules and walls. Step counter HUD bar drains 1 per action; running out loses. Core priors: **objectness** (pawns, molecules, walls as discrete entities) + **basic geometry & topology** (connectedness, region partition).

## Per-level escalation (preview for write_spec)

- **L1** introduces M1 = walk + stamp + partition-win. Two molecules of distinct colours, separated only by an empty mid-strip; player must stamp the strip to disconnect.
- **L2** adds M2 = **pushable molecules** (walking the pawn into a molecule cell pushes the molecule one cell in walk direction, sokoban-style). Forces molecule rearrangement before partitioning when the start layout has same-coloured molecules on opposite sides of an unavoidable narrow channel.
- **L3** adds M3 = **decaying stamps** (a stamped wall dissolves after K=4 turns). The win check still requires a valid partition at the moment of evaluation; player must stamp, push, and finalise within the decay window.

## Novelty: similarity check (positive test)

### vs taxonomy of 25 reference games

| Closest reference | Description | Distinguishing rule |
|---|---|---|
| **ka59** (sokoban-explode-chase) | Click switches active pawn; arrows slide it 3 cells and recursively push other pawns; explode-tiles spray; a chaser shuffles toward the active pawn; cover every coloured target square. | ka59's win condition is *cover-coloured-target-tiles* (geometric position match per pawn). `xn5p`'s win condition is *partition-by-region-into-monochromatic-components* (a topological invariant on the chamber's connectivity graph). ka59 has no stamp/wall-creation verb; `xn5p` has no chaser, no explode-tile, and only one player-controlled entity. |
| **gv47** (seed-grow-surround-dissolve, prior-game — see also below) | (n/a in taxonomy) | n/a |
| **ar25** (shape-mirror-cover) | Slide a shape and a mirror line to make a same-shape ghost cover scattered dots. | ar25's verb is sliding pre-existing sprites (shape + mirror); `xn5p`'s verb is *creating new wall cells* by stamping. ar25's goal is symmetry-cover; `xn5p`'s goal is partition. No shared mirror or symmetry concept. |
| **cn04** (nub-pair-glyph) | Click selects a glyph; arrows slide it; ACTION5 rotates 90°. Arrange so every glyph's nubs kiss neighbours. | Both use click+arrows+ACTION5, but cn04's ACTION5 is *rotate-the-selection* and the win is sprite-orientation-based (every nub paired). `xn5p`'s ACTION5 is *stamp-a-wall-here* and the win is region-connectivity-based. |
| **wa30** (lock-drag-crate) | Walk player; lock onto an adjacent crate to drag it into a goal frame; drone competes for crates. | wa30 has avatar + crates + goal frames (visual position match). `xn5p` has avatar + molecules + chamber (no goal frames; win is topological, not positional). wa30's lock/drag adheres a crate; `xn5p`'s push (L2) is a one-cell shove with no adhesion. |

No taxonomy entry overlaps on family or core-dynamic to a degree that requires a heavier distinguishing argument; the verb (`stamp a wall here`) and the win predicate (`every connected component is monochromatic`) are absent from the 25 reference games.

### vs `prior-games/index.md`

| Closest prior | Description | Distinguishing rule |
|---|---|---|
| **gv47** (seed-grow-surround-dissolve) | Click stationary coloured seeds to expand each seed's persistent connected region by one cardinal ring per click; surround a pip with paint to auto-dissolve; ACTION5 globally mixes contacting colour pairs. | Both touch "regions on a grid". gv47 *grows* regions outward from stationary seeds; `xn5p` partitions a single pre-existing chamber by *placing barriers*. gv47's win is per-pip 8-neighbour Chebyshev colour match; `xn5p`'s win is connectivity-class-equals-colour-class on the chamber's open cells. gv47 has no avatar; `xn5p` has a walking avatar. gv47 has no walls created at runtime; `xn5p`'s primary verb does exactly that. |
| **ka59 (taxonomy)** / no direct prior | n/a | (covered above) |
| **kn58** (anchor-pull-magnet) | Click any cell to place a single magnetic anchor; every coloured pawn slides one cell toward it. | kn58's verb is anchor-placement → global-pawn-slide (a single-anchor field). `xn5p` has no field, no global slide; pawn moves cell-by-cell and stamps create walls only at the pawn's cell. |
| **pz4t** (anchor-pivot-place) | Tile a single connected dark-grey region with all coloured components; clicked-pixel sets placement anchor; arrows reflect, ACTION5 rotates. | pz4t is jigsaw-tile-placement on a fixed region. `xn5p` modifies the region (subdivides it) and never adds polyomino pieces. |
| **wt39** (glide-deflect-thaw) | Pawn glides in pressed direction until wall; bumpers deflect; thaw-tiles crack. | wt39's avatar glides (no per-cell control); `xn5p`'s avatar moves one cell per arrow. wt39 has no stamp/region verbs. |
| **zk9p** (pursuer-merge-walk) | Avatar baits autonomous pursuers into self-collisions; merged pursuers vanish; win when none remain. | zk9p's molecules ARE adversaries that move autonomously toward the avatar. `xn5p`'s molecules are stationary objects (or pushable in L2/L3) — never autonomous. zk9p's win is *eliminate*; `xn5p`'s is *partition*. |

## Novelty: negative similarity check (per `negative-similarity-check.md`)

Walking the eight dimensions for the closest single prior, **gv47**:

| Dimension | gv47 | xn5p | Shared? |
|---|---|---|---|
| 1. What is on the board | Stationary seeds + pips + walls | Walking pawn + scattered molecules + walls + (open chamber) | NO — different cast |
| 2. Player physical input | Click-on-seed (grow) + ACTION5 mix | Arrows (walk) + ACTION5 (stamp) | NO — different input modality |
| 3. What the level asks for | Surround every pip with own-colour paint | Partition chamber so each region is monochromatic | NO — different goal class (point-cover vs topology) |
| 4. What kills the player | Step budget | Step budget | YES |
| 5. Supporting elements | Coloured pips + ring HUD | Walls + step HUD + pen-coloured molecule sprites | mostly NO |
| 6. Visual signature | Painted regions growing across cells | Chamber with discrete molecule sprites + a walking avatar + stamped walls | NO |
| 7. Pixel grain of primary sprites | 1×1 paint cells | 3×3 multi-pixel pawn + 3×3 molecule sprites + 3×3 stamped wall | NO — different |
| 8. Core dynamic | Click-grow-and-surround | Walk-and-stamp-to-partition | NO — different |

Sharing on dimension 4 only. Far below the 3-of-8 reject threshold.

Closest second-prior, **zk9p**: shared dim 1 (avatar+NPCs+walls), 4 (step budget), 5 (avatar+multi-NPC), 7 (similar grain). But zk9p's NPCs are *autonomous adversaries* and `xn5p`'s molecules are *stationary objects of a topological partition* — dim 3 and 8 are flatly different. Sharing 3-4 dimensions with zk9p is borderline; the differentiator is that `xn5p`'s molecules don't move on their own and the win condition is a connectivity invariant on the chamber, not a kill-count. Visual differentiation will further reinforce: stamped walls, an open chamber bounded by thick palette-3 walls, and 3×3 molecule sprites with internal pixel structure (rings or plus-shapes), rather than zk9p's 1×1 pursuer dots on a textured floor.

## Novelty: vs preexisting video games (manual axis)

Closest preexisting genre is region-partition logic puzzles — Slither Link (boundary-drawing on a fixed grid) and Loops of Zen / topology puzzles (rotate tiles to fix loop topology). `xn5p` differs by having an *avatar that walks the chamber and stamps walls in real time*; the player is inside the puzzle, not over it. Sokoban-style box-pushing (the L2 mechanic) is borrowed in form but is subordinate to the partition-goal; sokoban's goal is moving boxes onto target cells, not partitioning the chamber by topology. The decaying-stamp L3 mechanic adds time-pressure at the per-stamp level — not a feature of any well-known partition puzzle I am aware of.

## Action palette

`available_actions = [1, 2, 3, 4, 5]` — cardinal motion (1-4) + the freedom slot (5) for stamp. No click; the pawn's position is the only spatial-input handle. ACTION5 is where the game's identity verb lives, per `action-enum.md`.
