# Game generation final report

## Generated game
- **ID**: jx5k
- **Source**: `prior-games/jx5k/jx5k.py`
- **Metadata**: `prior-games/jx5k/metadata.json`
- **Lines of code**: 644

## Mechanic
The player constructs a small multigraph by pair-clicking coloured node sprites: ACTION6 selects a node (a halo lights it), and a second ACTION6 on a different node cycles the edge state for that pair. Each node has a target degree shown as a small ring of pip markers around its perimeter, which fills as edges attach. Win = every node's filled-pip count equals its target. L1 (4 nodes, target degree 2 each) introduces the bare edge-link mechanic with a 4-cycle witness. L2 (5 nodes, central + 4 outer, targets `[3, 3, 3, 3, 4]`) adds a colour-cycle action (ACTION5) plus a same-colour-only edge constraint, requiring the witness to recolour mismatched starting nodes before edges become legal. L3 (4 nodes diamond, targets `[4, 2, 4, 2]`) extends the per-pair edge cycle to allow parallel double-edges and tunes target degrees so a parallel edge is required on exactly one pair (n0–n2). Lose = step counter exhausts.

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Cycle the currently selected node's colour through the level's palette (L2/L3 = `[blue, red]`); auto-deselect after cycling. No-op when no node selected. Hidden via `_get_valid_actions` at L1. |
| ACTION6 | Click at display `(x, y)`. Select a node, toggle/advance an edge between selected and clicked nodes, click an existing edge sprite at L3 to remove it, or deselect on empty / on-self click. |

## Levels

- **L1** — 4 corner nodes, single edges only, build a perimeter 4-cycle. Step budget 30; witness 8 actions.
- **L2** — 5 nodes (cross + centre), starting colours `[red, blue, red, blue, red]` mismatched against neighbours; recolour both blue nodes to red, then build 4 radials + 4 perimeter (target `[3, 3, 3, 3, 4]`). Step budget 50; witness 20 actions.
- **L3** — 4 nodes diamond, starting colours `[red, blue, red, blue]`; recolour both blue, build 5 distinct edges with one (n0–n2) doubled to satisfy the unique target `[4, 2, 4, 2]`. Step budget 50; witness 16 actions.

## Novelty note

- **Closest taxonomy entries**: `bp35 procedural-graph-walk` and `lf52 procedural-graph-walk-undo` — distinguishing rule: bp35/lf52 walk a *pre-built* graph; jx5k *constructs* a multigraph. Different verb (track-step vs. pair-click-edge), different win condition (token-configuration vs. degree-sequence match), different graph type (simple vs. multigraph).
- **Closest prior-game entry**: `qm4t convex-pen-trap` — distinguishing rule: qm4t commits a polygon hull and captures critters strictly inside; jx5k builds a multigraph and matches a degree sequence. Different win predicate (containment vs. degree match), different action vocabulary (vertex-post drop + ACTION5 commit vs. immediate pair-click).

Negative-similarity walk-through against `qm4t`, `bx84`, `bp35` showed 0 dimensions of overlap with each. Multi-graph mechanics are absent from both the 25-game taxonomy and the 36 prior-games corpus.

## Index update

One row appended to `prior-games/index.md`:

```
| jx5k | constellation-edge-link | Constellation Edge-Link — pair-click coloured nodes to build a multigraph satisfying per-node target degrees; L2 adds colour-cycle, L3 adds parallel double-edges. | 2026-05-08T01:19:48Z | (autonomous) |
```
