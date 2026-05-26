# Mechanic pick

## Run input
Autonomous mode — no seed provided.

## Game ID
`jx5k` — 4 lowercase alphanumerics, not in the 25 reserved reference IDs, not in `prior-games/index.md` (verified against the 36 prior rows kf42…zw91 plus the existing fb7t directory).

## Mechanic family
`constellation-edge-link` — geometry / topology + objectness priors.

## One-paragraph mechanic description
The board is a small fixed constellation of 4–8 coloured "node" sprites at known positions on an otherwise empty playfield. Each node has a target *degree* — a small ring of pip-marks around the node showing the number of edges the player must connect to it (1–3). The player's interaction is **edge construction**: ACTION6 click on a node selects it (a halo lights it); a second ACTION6 click on a *different* node creates a straight-line edge between the two centres if no edge exists, or removes the existing edge if one does; clicking on empty space deselects. Edges are visible thin coloured ribbons spanning between node centres; degree pips visually fill in as edges attach (an empty pip becomes a filled pip, mirroring satisfaction). Win = every node's filled-pip count exactly equals its required-pip count. L2 adds a **no-cross constraint** — proposed edges that would visually cross an existing edge are rejected (the proposed line briefly flashes red and no edge is created), forcing planning over edge-ordering and topology. L3 adds **node colour cycling**: ACTION5 with a node selected cycles that node's colour through a small palette, AND edges only connect nodes of matching colour, so the witness must actively recolour mismatched nodes before the desired edges become legal.

## Action palette
- `ACTION5` — cycle the selected node's colour (L3 mechanic; no-op at L1/L2 if selected, but ACTION5 is only listed in `available_actions` from L3 onward via per-level gating in `_get_valid_actions`). To keep one consistent enum across levels, ACTION5 is in `available_actions=[5, 6]` for the whole game; at L1 and L2 it is a no-op (visual: nothing happens) and the witness never uses it. (Per discoverability principle: a no-op action that has no effect is acceptable; the player learns it does nothing.)

  *Critique note for `critique_spec`:* listing ACTION5 on L1/L2 with no effect is borderline — the §3.4 "minimal action enum" preference. Acceptable here because the action is the freedom slot's per-game distinctive verb, kept in the enum so the agent's learned policy can transfer; it just gates internally. Will reaffirm in critique.
- `ACTION6` — click. Mediates select / pair-create-edge / pair-remove-edge / deselect.

## Cross-reference and distinguishing rules

### Vs. taxonomy of 25 reference games (full pass)
| Closest taxonomy entry | Distinguishing rule |
|---|---|
| `bp35 procedural-graph-walk` | bp35 has a *pre-built* graph the player walks a token along (LEFT/RIGHT step along current track, click teleports to highlighted neighbour). jx5k's player **constructs** the graph from scratch — no token, no graph traversal; the move set is "create / remove edges to satisfy degree constraints". Win = degree match, not "reach a target node configuration". |
| `lf52 procedural-graph-walk-undo` | Same family as bp35 (graph-walking with undo). jx5k still differs the same way — graph construction vs. graph traversal. |
| `cn04 nub-pair-glyph` | cn04 has spatial pieces with palette-8 nubs that must geometrically *kiss*; the win is local-pixel coincidence after slide+rotate of physical sprite shapes. jx5k's edges are abstract logical connections, not physical pixel coincidences; nodes do not move. |
| `sb26 tile-place-commit` | sb26 places coloured tiles into slots and commits a guess for mastermind feedback. jx5k has no slots, no commit verb, no per-step hint feedback; the game is constructive topology, not Mastermind. |
| `tn36 program-pawn-trace` | tn36 composes a program of move-and-rotate instructions then runs it. jx5k has no program-tape composition, no run-then-trace verb; edges are immediate not deferred. |
| `vc33 row-slide-pull-tab`, `lp85 row-col-shift-grid` | Both are positional-shift puzzles over a fixed token grid. jx5k has no token movement; nodes are pinned. |
| `re86 frame-paint-canvas` | re86 cycles which frame is active and slides one frame to a colour-zone. jx5k has no frames or canvas. |
| `g50t walk-vs-scroll`, `tu93 maze-pickup-train`, `sk48 paired-snake-trail` | All avatar-walking maze games. jx5k has no avatar, no maze, no walking. |

No taxonomy entry shares jx5k's family name nor (after description check) shares win-condition + primary-action + primary-constraint. **NOVEL** vs. taxonomy.

### Vs. prior-games/index.md (full pass)
The closest prior-games entries (clustered by surface signature) and the distinguishing rule for each:

| Closest prior entry | Distinguishing rule |
|---|---|
| `pz4t anchor-pivot-place` | pz4t tiles a single connected dark-grey region with coloured components; place-anchor + reflect/rotate to fit. jx5k has no spatial tiling; constructions are 1-D abstract edges between fixed points. |
| `vn8d domino-cascade-topple` | vn8d triggers a chain reaction through pillars on click. jx5k has no chain reaction; a click is local (creates/removes one edge), not a propagating event. |
| `zd7m cohort-step-route` | zd7m steps every movable pawn one cell with arrows, with anchors blocking and portals teleporting. jx5k has no moving pawns and no arrow movement. |
| `kn58 anchor-pull-magnet` | kn58 places a single magnetic anchor and every coloured pawn slides one cell toward it. jx5k has no movement, no magnetic field. |
| `bx84 beam-mirror-reflect`, `vp6h shadow-cast-collect`, `lq5x lantern-cone-illuminate` | Light/beam mechanics — beams or cones project across the playfield. jx5k has no projection; edges are placed by direct pair-click, not by ray-casting from a source. |
| `qm4t convex-pen-trap` | qm4t drops vertex-posts whose convex hull defines a pen, then commits to capture critters strictly inside. jx5k has no enclosure semantics — connecting two nodes does not "trap" anything; the win is degree-match per node, not interior-vs-exterior partition. The shapes drawn (polygon for qm4t, multigraph for jx5k) and the win predicate (containment vs. degree match) diverge sharply. |
| `qn7w pulse-chain-eject` | qn7w fires momentum pulses through ball-chains; chain-end ejects on each pulse. jx5k has no momentum, no chains, no eject — single static graph. |
| `gx7m gear-mesh-cascade` | gx7m discs propagate rotations across cardinal mesh. jx5k has no rotation, no cascade; edges are static after creation. |
| `pf3w wavefront-converge-timing` | pf3w activates emitters and ticks BFS wavefronts; win on a single tick when frontiers coincide with target receivers. jx5k has no emitters, no ticks, no wavefronts — the win is a static topological property, not a timing coincidence. |

No prior-game shares jx5k's family. The closest in coarse "fixed-point / click-place" surface is `qm4t convex-pen-trap`, but the win predicate (degree-match vs. point-in-polygon containment), the action vocabulary (pair-edges vs. vertex-posts + ACTION5 commit), and the player's mental model (graph topology vs. polygon enclosure) differ at every load-bearing axis.

### Negative similarity check (per `negative-similarity-check.md`)
Walking the seven dimensions against the closest priors / reference games:

**Vs. `qm4t convex-pen-trap`** (coarsest near-miss):
1. *What is on the board.* qm4t: empty arena populated with critters + tally-chips + patrollers + dropped vertex-posts. jx5k: 4–8 fixed coloured nodes with degree-pip indicators on an otherwise empty field.  Different.
2. *What the player physically does.* qm4t: clicks empty cells to drop vertex-posts, ACTION5 commits the polygon. jx5k: clicks pairs of nodes to create/remove edges. Different.
3. *What the level is asking for.* qm4t: capture every required-colour critter strictly inside hull while excluding forbidden critters/patrollers. jx5k: every node's edge count exactly matches its required degree. Different.
4. *What kills the player.* qm4t: too many strikes / step-budget. jx5k: step budget only.  Same generic failure mode (universal across the corpus); does not count toward overlap.
5. *Cast of supporting elements.* qm4t: critters, patrollers, vertex-posts, tally-chips. jx5k: nodes, edges, degree-pips. Different roster.
6. *Visible visual signature.* qm4t: critter sprites + posts + tallies + commit halo. jx5k: small ringed circular nodes + thin edge ribbons. Different palette signature (jx5k uses a single accent colour for edges + per-node colour panel).
7. *Pixel grain of primary sprites.* qm4t: irregular-shape critters and post-pillars. jx5k: round nodes with internal pip-rings + radial structure; edges have explicit thickness pattern (3-pixel thick line with palette accent).
8. *Core dynamic.* qm4t: spatial enclosure — does the polygon contain the right items? jx5k: graph topology — does the multigraph satisfy a degree sequence? Fundamentally different.

**Overlap dimensions: 0 (or 1 generic at most). Threshold for rejection is 3+. PASS.**

**Vs. `bx84 beam-mirror-reflect`** (closest "abstract-line-drawing" reference):
1. Board: bx84 has emitter, beam path, mirror cells, filter, prism. jx5k has nodes + edges, no emitter, no beam.  Different.
2. Action: bx84 — click empty cell to place mirror, click mirror to cycle orientation. jx5k — click pairs of nodes. Different.
3. Goal: bx84 — beam reaches a target. jx5k — degree match per node. Different.
6. Visual: bx84 has a moving beam (live cell update). jx5k has static edges added/removed in batches. Different.
8. Core dynamic: bx84 = live propagation routing. jx5k = topological constraint satisfaction. Different.

**Overlap dimensions: 0. PASS.**

**Vs. `bp35 / lf52 procedural-graph-walk(-undo)`** (only graph-themed reference games):
1. Board: bp35/lf52 — pre-built graph of 8×8 coloured nodes the token sits on. jx5k — small constellation of stars with no pre-built edges.  bp35 starts with a graph; jx5k starts WITHOUT one.
2. Action: bp35 — LEFT/RIGHT step along current track, click teleports to highlighted neighbour. jx5k — click pair to create/remove edge.  Different verbs.
3. Goal: bp35 — reach a procedurally-defined token configuration. jx5k — graph topology degree match.  Different.
8. Core dynamic: bp35 = routing decision on a fixed graph. jx5k = building a graph. **Inverse activities.**

**Overlap dimensions: 0–1 (only "graph" appears in both names — but the activity is opposite). PASS.**

The candidate is **NOVEL** under both the positive `similarity-check.md` and the negative `negative-similarity-check.md` tests.

## Provisional sketch (for `write_spec` to expand)
- Grid: 32×32 logical playfield (camera resized per level), nodes at quantised cell positions, with internal sprite detail (a 5-cell-radius ring of pips around each node centre), step-counter HUD on top row.
- Action enum: `[5, 6]`.
- Win: degree match across all nodes (per spec). Lose: step budget (universal pattern from cross-cut frequencies).
- L1: 4 nodes in a square, target degrees `[2, 2, 2, 2]` → witness builds a 4-cycle.
- L2: 5 nodes in a non-planar-friendly configuration, no-cross constraint blocks the obvious-but-crossing edges, witness threads the edges in a topology-aware order.
- L3: 5–6 nodes with mismatched starting colours and same-colour-only edge constraint, witness recolours specific nodes via ACTION5 before edges become legal.
