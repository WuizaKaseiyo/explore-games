# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (full revised spec).
- skills/code/universal-scaffold.md (file structure, naming rules, viewport rules).
- skills/code/novaengine-api.md (API cheatsheet).
- skills/code/id-generation.md (ID rules).
- The 5 reference sources read in study (cn04 / sk48 / sp80 / tr87 / m0r0) for stylistic templates.

## Deliverables Produced
- prior-games/tj4n/tj4n.py (599 lines)
- prior-games/tj4n/metadata.json
- workspace/implement-summary.md

## Notes
- `Tj4n()` instantiates without raising; ast.parse passes.
- Engine attribute is `_levels` (not `levels`); the smoke-test command in implement.md's example uses `g.levels` which fails — adjusted to `g._levels` for the verification.
- Implementation mirrors sk48-style for trail-sprite-as-list, sp80-style for animation phase machine, and m0r0-style for movement guard.
- One simplification vs the spec: undo (ACTION7) is single-step and clears its stack on closure (closures aren't undoable in this implementation). Documented in the source. The witness solutions don't use ACTION7, so this doesn't affect solvability.
- Layer ordering: avatar=3, target/forbidden/pursuer=2, trail/wall=1 — avatar is always on top, trail/wall behind targets.
