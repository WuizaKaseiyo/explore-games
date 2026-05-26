# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (revision 1).
- workspace/critique-pass.md.
- skills/code/{universal-scaffold,novaengine-api,id-generation,spec-template}.md.
- skills/global/{paths,action-enum,color-legend}.md.

## Deliverables Produced
- prior-games/pj7k/pj7k.py (420 lines).
- prior-games/pj7k/metadata.json.
- workspace/implement-summary.md.

## Notes
- Used `_levels` (engine private) when probing in the smoke harness; engine exposes via `current_level`.
- Permutation tables verified against L2 witness trace.
- Camera viewport set to (16, 16) per universal-scaffold.md to ensure the engine renders at 4× scale matching the logical board.
- Cube sprite pixels rebuilt every step from the in-memory `self.faces` dict, not via `Sprite.rotate()`.
- Paint sprites are spawned at runtime with unique names (`paint_<colour>_<seq>`); old paint at the same cell is removed.
