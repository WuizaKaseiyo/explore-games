# mechanic-pick — Run #4

## ID

**`cy3k`** — verified not in 25-ref reserved list, not in `prior-games/index.md` (29 entries incl. ej4t, vy3m, tw94), not a recognisable English word. **Pascal class name `Cy3k`** — first letter caps, `y3k` preserved (last char `k` lowercase since digits aren't letters in Pascal-case rule).

## Mechanic family tag

**`cluster-cycle-rewrite`**

## Skeleton-diversity declaration

| field | value |
|---|---|
| `family_class` | symbolic-rewrite |
| `primary_skeleton` | symbolic-rewrite |
| `secondary_skeleton` | classification-sorting |
| `interaction_type` | arrows |
| `state_surface` | visible |
| `state_model` | symbolic-state |
| `objective_shape` | match-pattern |

## Skeleton-diversity verdict

| check | result |
|---|---|
| Recent-5 prior skeletons | tw94=topology-transform, vy3m=multi-actor-coordination, ej4t=object-placement, tg6w=global-field-update, pf3w=cellular-propagation |
| Candidate `primary_skeleton` in recent-5? | **NO** — symbolic-rewrite is not in recent 5 ✓ |
| Full-corpus high-frequency (≥6 of 29)? | global-field-update=6 (only one) — symbolic-rewrite count = 1 (pj7k), not high-freq ✓ |
| Override needed? | NO |
| **Verdict** | **PASS** |

## One-paragraph description

A 4×4 (L1) / 6×6 (L2) / 7×7 (L3) grid of single-cell coloured squares (palette of 4 colours per level). The player controls a small cursor avatar that walks the grid with arrow keys (ACTION1-4). ACTION5 cycles the colour at the cursor's cell forward through the 4-colour alphabet — but the cycle propagates to **every cell in the same 4-connected cluster of cells that currently share the cursor's colour**. So pressing ACTION5 once on a 1-cell island cycles 1 cell; pressing it on a cell embedded in a 7-cell same-colour blob cycles all 7. Win condition: the grid matches the target pattern displayed alongside the playfield.

**M1** (L1): single cluster cycling — the player learns that ACTION5 cycles the entire same-colour cluster of the cursor's cell. **M2** (L2): cluster *fission* — when a cluster cycles past a "barrier colour" (one specific palette value, e.g. palette 4), the cluster splits because cells of the new colour no longer match the previous colour neighbours. Players must reason about how cycle ordering re-shapes cluster boundaries. **M3** (L3): cluster *fusion* — cycling adjacent same-coloured clusters across a shared neighbour merges them into one cluster on the next ACTION5; players must orchestrate which clusters fuse first to get the target.

## Distinguishing rules vs near-misses

### Closest taxonomy near-miss: `tr87` (tape-rewrite-rule)

**Shared surface**: both involve cycling through an alphabet of glyphs/colours via key press.

**Concrete distinguishing rule**: tr87 is **1-D** (single tape; bracket cursor moves left/right; UP/DOWN cycles a single bracketed card). cy3k is **2-D** (grid; cursor moves N/S/E/W; ACTION5 cycles the cursor's cell). tr87's "cycle" affects a single card; cy3k's "cycle" propagates to the cursor's entire same-colour 4-connected cluster (cluster discipline is the load-bearing mechanic). tr87 has rewrite-rule "books" prescribing what input maps to what output; cy3k has no per-target rule book — the player infers desired cycle-sequences by looking at the target pattern. Different interaction grammar (1D vs 2D), different cycle scope (single vs cluster), different rule encoding (visible rule book vs implicit pattern-match).

### Closest taxonomy near-miss: `pj7k` (rolling-cube-face-paint, also `symbolic-rewrite`)

**Shared surface**: both are `symbolic-rewrite` skeleton; both have a single avatar walking a small grid that rewrites cell state.

**Concrete distinguishing rule**: pj7k's avatar is a 3-D cube whose face permutation is the symbolic state — rolling it permutes faces and the bottom face's colour deposits onto the cell. cy3k has a flat 1-cell cursor and the symbolic state lives in the *cells*, not the avatar. pj7k's rewrite is per-cell deposit; cy3k's rewrite is per-cluster cycle (multi-cell propagation). Avatar geometry, rewrite locality, and state location all differ.

### Closest prior near-miss: `ng52` (classification-sorting; my secondary_skeleton)

**Shared surface**: both involve grouping cells/objects by feature.

**Concrete distinguishing rule**: ng52 is partition-by-stick-signature into bins; cy3k is cycle-clusters-to-match-pattern. ng52 has explicit movable objects; cy3k has stationary cells whose colour cycles. Different objective shape (`classify-objects` vs `match-pattern`), different interaction (click placement vs arrow + ACTION5).

## Negative-similarity 7-dim test

vs **pj7k** (closest skeleton match):
1. Board: grid of cells + cursor (shared, 1)
2. Action verb: cycle current cell + cluster (different from pj7k's roll-cube)
3. Goal: match target pattern (shared with several priors, 2)
4. Death: step budget (universal, 3)
5. Cast: cursor + grid + target (different from pj7k's cube + cells)
6. Visual signature: 4-color grid + small cursor (different from pj7k's 3D cube)
7. Pixel grain: rich (equivalent)
8. Core dynamic: cluster-cycle-with-fusion-fission (vs cube-roll-deposit)

Shared on dims 1, 3, 4 = 3 dimensions but 4 is universal so effectively 2. Just under threshold. ✓ NOVEL.

## Inspiration source

Synthesized — drew on **PuzzleScript demo `tr87` style** (cycle through glyph alphabet) + **cellular-automata cluster propagation** (4-connected component logic from Conway / Game of Life family) + adapted away from sokoban entirely. No single PuzzleScript demo directly maps to this mechanic; it is a fresh composition.

## Considered alternatives

| candidate | family_class | primary_skeleton | reject reason |
|---|---|---|---|
| stack-recipe-tower (recipe-composition) | recipe-composition | recipe-composition | rejected — too close to hr8q pair-blend-recipe (same skeleton, same `complete-recipes` objective shape) |
| signature-sort-grid | classification-sorting | classification-sorting | rejected — too close to ng52 (same skeleton, same `classify-objects` shape) |
| sentence-rewrite-tape | symbolic-rewrite | symbolic-rewrite | rejected — too close to tr87 25-ref (1D rewrite tape, identical mechanism class) |
| pivot-glyph-rotate | symbolic-rewrite | symbolic-rewrite | rejected — too close to qz73 radial-cycle-lock and pj7k rolling-cube |
| **cluster-cycle-rewrite** (this) | symbolic-rewrite | symbolic-rewrite | **selected** — 2D cluster propagation is genuinely fresh; passes recent-5 and high-freq diversity gates |

## Action mapping (preview)

`available_actions = [1, 2, 3, 4, 5]`. ACTION1-4 walks cursor 1 cell. ACTION5 cycles cluster forward through alphabet. ACTION6/7 unused.

## Per-level grid sizes (preview)

- L1: 6×6 grid, 4-colour alphabet, 2-3 clusters (M1 only)
- L2: 8×8 grid, 4-colour alphabet, includes barrier colour for fission (M1+M2)
- L3: 10×10 grid, 4-colour alphabet, fusion potential between adjacent clusters (M1+M2+M3)
