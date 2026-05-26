# cy3k — cluster-cycle-rewrite

## Skeleton labels

```yaml
primary_skeleton: symbolic-rewrite
secondary_skeleton: classification-sorting
interaction_type: arrows
state_model: symbolic-state
objective_shape: match-pattern
family_class: symbolic-rewrite
```

## Summary

The grid is a field of single-cell coloured squares from a 4-colour alphabet (yellow / green / red / purple). The player controls a 3×3 cursor avatar that walks the grid with arrow keys. ACTION5 cycles the colour at the cursor's cell forward (yellow→green→red→purple→yellow), AND propagates the cycle to **every cell in the cursor's 4-connected same-colour cluster**. Win condition: the grid matches a target pattern displayed in the top-right HUD. L1 introduces the base cluster-cycle rule. L2 adds *fixed cells* — cells marked with a fixed_marker do not cycle even when their cluster cycles, so the player must reason about clusters that contain stuck cells. L3 adds *transparent cells* — cells that preserve 4-connectivity (clusters span across them) but do not themselves cycle, allowing remote cells to fuse into one cluster.

## Action mapping

| Action | Semantic |
|---|---|
| ACTION1-4 | Walk cursor 1 cell in cardinal direction (no walls; movement only blocked by grid boundary) |
| ACTION5 | Cycle cursor's cell colour forward; propagates to all cells in the 4-connected same-colour cluster (excluding fixed cells; using transparent cells as connectivity bridges) |

`available_actions = [1, 2, 3, 4, 5]`. ACTION6/7 unused.

## Per-level mechanic progression

| Level | Mechanic | Specific challenge / witness |
|---|---|---|
| 1 | M1: cluster-cycle | 6×6 grid with 4 quadrants of 9 cells each (yellow / red / purple / green). Witness: cycle each cluster once in any order to match target where every cluster has cycled forward by one. `[ACTION5, ACTION4 × 3, ACTION5, ACTION2 × 3, ACTION5, ACTION3 × 3, ACTION5]` (13 actions). |
| 2 | M2: fixed cells | 6×6 grid same start as L1 + fixed_marker at (0,0) and (5,5). Target: cycle clusters but fixed cells stay at original colour. Witness similar to L1. |
| 3 | M3: transparent cells | 8×8 grid with 4 quadrants of 16 cells + fixed at (0,0) + transparent at (3,3). Target: cycle each cluster once, fixed and transparent stay. **Order matters**: cycle B before C, otherwise C+B fuse via transparent (3,3) bridge once both purple, causing double-cycle of C. Witness: `[ACTION5, ACTION2 × 2, ACTION5, ACTION4 × 2, ACTION1, ACTION5, ACTION2, ACTION5]` (10 actions, A→B→C→D order). |

## Win condition

For each cell (x, y): `cell_colour[(x,y)] == target_pattern[(x,y)]`. Targets are pre-computed per level.

## Lose condition

`self._steps_used >= self._max_steps`. Per-level: L1=50, L2=80, L3=120.

## Internal state

- `self._steps_used: int`, `self._max_steps: int`
- Cell colours stored in each `cell` Sprite's `pixels[0][0]` directly (no separate dict)
- `TARGETS` constant: per-level dict `(x, y) -> target_colour` for win check

## Notable code patterns

- **4-connected BFS with transparent-bridge support** (`_compute_cluster`): standard BFS on 4-neighbours, but transparent cells are added to a `bridge` set (not the cluster) and their 4-neighbours are still explored. This lets a cluster span across transparent cells — useful for L3 fusion semantics.
- **Per-cell sprite colour mutation**: each cell is a 1×1 Sprite; cycling sets `cell.pixels[0][0]` to the next colour. Avoids a separate state dict; the rendered sprite is the source of truth.
- **Fixed-cell skip during cycle**: in `_cycle_cluster_at_cursor`, after BFS finds the cluster, iterate cluster members and skip `_is_fixed(x, y)` when applying the new colour. Cluster membership includes fixed cells (BFS doesn't exclude them by colour), but the cycle effect doesn't.
- **Transparent doesn't cycle**: `_compute_cluster` returns empty if cursor itself is on a transparent cell, so ACTION5 from a transparent cell is a no-op. Transparent cells appear in `bridge`, never in `cluster`, so they never receive the cycle effect.
- **NEW: skeleton-diversity gate** (`primary_skeleton: symbolic-rewrite`): this is the first prior game generated under the upgraded `mechanic-novelty/skeleton-diversity-check.md` rule. The recent-five-prior skeleton window before this run was `topology-transform`, `multi-actor-coordination`, `object-placement`, `global-field-update`, `cellular-propagation` — all walk-and-push or click-place adjacent. `symbolic-rewrite` is genuinely fresh in the corpus (only 1 prior, pj7k); the gate forced this skeleton diversification.
