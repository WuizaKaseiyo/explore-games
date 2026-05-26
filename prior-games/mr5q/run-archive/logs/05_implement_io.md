# Step #05: implement

## Inputs Consumed
- mechanic-spec.md (from #03)
- critique-pass.md (from #04)
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md, smoke-test-checks.md
- Reference source files (read in study): cn04, sk48, m0r0, sp80, sb26 — used for code style (sprite dict, Level list, two-sprite swap idiom, RenderableUserDisplay, Camera+interfaces composition).

## Deliverables Produced
- `prior-games/mr5q/mr5q.py` (557 lines): full implementation with sprite bank, level definitions, StepCounterHud, and Mr5q class implementing flip + attract-tick + discharge + colour-key + flip-pad mechanics.
- `prior-games/mr5q/metadata.json`: schema-conformant.
- `implement-summary.md` (in workspace): explains spec→implementation deltas (4×4 vs 5×5 pawns, 16×16 vs 14×14 grid, removed L2 wall, widened L3 wall gaps, Cheb-distance discharge predicate, Manhattan-greedy in lieu of BFS).

## Notes
- The spec's pawn size (5×5) and 14×14 grid were too tight to fit the multi-pawn level layouts cleanly; switched to 4×4 pawns on a 16×16 grid. The half-fill polarity cue is preserved (top-row yellow vs bottom-row magenta inside the green/orange/purple ring frame).
- The spec's discharge predicate (Manhattan ≤ 1) was replaced with Chebyshev distance ≤ PAWN_SIZE — necessary for sized sprites; effectively triggers on bbox edge-or-corner-touching adjacency.
- Initial BFS-based routing oscillated when both pawns pursued each other through diagonal positions; replaced with Manhattan-greedy + dominant-axis-toward-target priority + wall-and-occupant fallback. This is sufficient for L1/L2/L3 layouts as designed.
- L2's column-wall was dropped because a 1-cell gap is impassable for 4-cell pawns; the colour-key mechanic alone suffices to require flips and provides random-resistance.
- L3's wall gaps were widened to 4 cells so the 4×4 pawn can fit through; the flip-pad is positioned at the unique pawn-position that fits in the gap, forcing pad-traversal.
- Smoke test passed: `Mr5q()` instantiates; ACTION5 + ACTION6 calls run without raising; level state advances correctly when L1 win predicate fires.
- Cleaned up `__pycache__` after smoke test.
