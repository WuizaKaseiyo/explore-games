# Step #07: implement

## Inputs Consumed
- `mechanic-spec.md` v3 (post-pass).
- `skills/code/universal-scaffold.md`.
- `skills/code/novaengine-api.md`.
- `skills/code/id-generation.md`.

## Deliverables Produced
- `prior-games/qm4t/qm4t.py` (514 lines).
- `prior-games/qm4t/metadata.json`.
- `runs/.../workspace/implement-summary.md` (per state contract).
- Spec witness corrections inlined in `mechanic-spec.md` (L2 and L3
  geometric fixes).

## Notes
- Convex hull via Andrew's monotone chain (returns vertices in image-coord
  CW order, which is fine for ray-casting).
- Point-in-polygon via standard ray-cast (works for any winding order).
- Pen overlay = 64×64 INTANGIBLE sprite recomputed every step.
  Boundary pixels = palette 1; interior = palette 2; rest = -1.
- Patroller cycle progresses every step (any action — including invalid
  clicks). Phase modulo 8.
- Strike resolution adds a `strike_marker` sprite to one of 3 fixed HUD
  slots; on the 3rd strike, `lose()` is called.
- Tally is a list of `tally_dot_<colour>` sprites; per matching capture,
  one is removed via `level.remove_sprite`.
- Spec witness for L2 and L3 had geometric errors caught only at
  smoke-time — corrections inlined in spec v3 during this state.
