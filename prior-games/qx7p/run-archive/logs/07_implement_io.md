# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (final).
- skills/code/universal-scaffold.md.
- skills/code/novaengine-api.md.
- skills/code/id-generation.md (verified ID).
- 5 reference source files (cn04, sp80, m0r0, sk48, tr87) for API/style anchoring.

## Deliverables Produced
- prior-games/qx7p/qx7p.py (456 lines).
- prior-games/qx7p/metadata.json.
- workspace/implement-summary.md.

## Notes
- Caught and fixed an L3 design bug during runtime smoke: bound-pair sums must MATCH for both pairs to be simultaneously solvable at one scan-line offset; redesigned with both sums = 4 and a {6, 7, 8} offset cycle.
- All 3 levels passed end-to-end witness replay.
- Camera default 64×64 matches grid_size = (64, 64) — no per-level resize.
- ACTION5 gate by `len(scan_line_rows) > 1` (only L3 has multiple rows).
- pycache cleaned.
