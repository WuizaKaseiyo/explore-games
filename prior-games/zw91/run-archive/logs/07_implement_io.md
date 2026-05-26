# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revised).
- skills/code/universal-scaffold.md.
- skills/code/novaengine-api.md.
- skills/code/id-generation.md.
- novaengine source under .venv (for Sprite, Level, Camera, BaseGame signatures).

## Deliverables Produced
- `prior-games/zw91/zw91.py` (594 lines).
- `prior-games/zw91/metadata.json`.
- implement-summary.md.

## Notes
- During runtime witness replay, the L3 cycle 2→3 at top-left tile (7, 6) was found to FAIL because the (8, 8) shove-block's center is straight south of the size-3 avatar centre, so the dominant-axis push rule pushes south into a wall, cancelling the inflate.
- Fix: changed `BURST_RADIUS` from 8 to 12 (Chebyshev-12 = 3 tiles) and re-derived the L3 witness to fire burst from tile (6, 6). At (6, 6) all three blocks naturally push east (each block's centre is east-or-southeast of avatar centre, with the dominant-axis rule and east-tiebreak picking east).
- Spec updated accordingly (rule, witness step-by-step, M3 alt-path enumeration, L3 (c) planning depth).
- Counterfactual M3-necessity still holds with Chebyshev-12: feasible burst positions for both target sets are tile_x ∈ {6, 7, 8}; all three require M3 to fire during the 2→3 cycle.
- All 3 witnesses replay end-to-end to WIN state (programmatically verified).
- `__pycache__` cleaned up after smoke instantiation.
