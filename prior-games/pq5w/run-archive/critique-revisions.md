# Critique revisions (visit #1)

## Issue 1 — L1 wall is bypassable within the step budget

**Checklist item violated**: 12 (strict counterfactual necessity / no
trivial fallback).

**Offending spec section**: §4 Level 1 — base dynamic system.

**Quote from spec**:
> "A vertical 3-cell wall at (8, 6..8) blocks the direct walk from
> the left half to the right half."
> "*L1 cannot be solved without triggering portal-traverse because
> the wall sprites at logical cells (8, 6), (8, 7), (8, 8) block
> row y=7 at x=8, and the step budget is 30 — the shortest
> wall-skirting walk ... requiring at least 22 STRIDE-cell walks;
> budget rejects.*"

**Problem**: 22 walks ≤ 30-step budget. The reasoning is wrong —
the budget does NOT reject a 22-step detour. A player can simply
skirt the 3-cell wall by going via (1,7) → (1,5) → (14,5) → (14,7)
in 17 walks (going up 2 cells, then 13 cells right above the wall,
then down 2 cells), which fits comfortably in budget. This means
the **portal-traverse mechanic is NOT counterfactually necessary**
in L1, violating checklist item 12.

**Concrete fix**: extend the L1 wall to a full vertical column at
x=8 spanning all rows y=0..14 (15 wall sprites). With a full-column
wall, no walking path across x=8 exists, and portal-traverse is
the only way to cross from the left half to the right half.

The L1 layout becomes:
```
y=0  ........#.......
y=1  ........#.......
y=2  ........#.......
y=3  ........#.......
y=4  ........#.......
y=5  ........#.......
y=6  ........#.......
y=7  .X.A....#...B.G.
y=8  ........#.......
y=9  ........#.......
y=10 ........#.......
y=11 ........#.......
y=12 ........#.......
y=13 ........#.......
y=14 ........#.......
```

The witness is unchanged (5 actions: 4 RIGHT walks plus 1
teleport-resolve). The necessity sentence becomes:

> *"L1 cannot be solved without triggering portal-traverse because
> the wall sprites at column x=8, y=0..14 (15 sprites) form a
> complete vertical barrier — no walking path exists from the left
> half (x≤7) to the right half (x≥9), so the avatar can only reach
> the goal by stepping onto portal A and teleporting to portal B."*

## Verdict

Re-enter `write_spec` and apply Issue 1's fix.
