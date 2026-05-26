# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (round 2 from #05): 9-section spec.
- workspace/critique-pass.md (from #06): NOVEL verdict + per-mechanic table.
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md.
- skills/global/* (action-enum, color-legend, paths).
- Reference: cn04, m0r0, sp80 (read in full at study) for engine idioms — adopted: declarative `sprites = {...}` dict, `levels = [...]` flat constant, `Camera(interfaces=[...])` HUD registration, `set_interaction(InteractionMode.REMOVED/TANGIBLE)` two-sprite-swap idiom for both wall hardness variants and avatar charge variants, `level.get_data(...)` for per-level parameters.

## Deliverables Produced
- `prior-games/ds5q/ds5q.py` (566 lines).
- `prior-games/ds5q/metadata.json`.
- `workspace/implement-summary.md`.

## Notes
- AST parse passes. Instantiation passes. All three witnesses simulated end-to-end via `perform_action(ActionInput(...))` calls reach the exit at the action counts predicted by the spec (L1=9, L2=25, L3=22).
- Architecture: per-cell wall hardness tracked in `self.wall_hardness` (Python dict); each wall position pre-places hardness variants 1..N at the same pixel coords with all-but-active set to `InteractionMode.REMOVED`; on erode, swap interaction down one variant. Avatar uses the same 3-variant swap pattern for `avatar_uncharged` / `avatar_red` / `avatar_blue`. Walls and stones use direct dict lookup for movement collision (rather than engine pixel collision).
- Sprite naming follows the spec roster: `wall_<color>_h<hardness>`, parsed in `on_set_level` to populate state dicts.
- No `__pycache__` left behind under prior-games/ds5q/.
- Step counter HUD draws a depleting bar at row 0 (palette 4 over palette 0).
