# Step #05: implement

## Inputs Consumed
- `mechanic-spec.md`, `critique-pass.md` (from earlier states).
- `skills/code/universal-scaffold.md`, `novaengine-api.md`, `id-generation.md` (from #01 study).
- `novaengine` source under `.venv/lib/python3.12/site-packages/novaengine/` (verified Level/Sprite/Camera/NovaBaseGame signatures).
- One reference game source `cn04.py` (verified Level kwarg style, super().__init__ signature).

## Deliverables Produced
- `prior-games/dj5h/dj5h.py` (1043 lines).
- `prior-games/dj5h/metadata.json`.
- `implement-summary.md` (in workspace).

## Notes
- File parses cleanly. Game instantiates without raising. All three witness sequences (`WITNESS_L1`, `WITNESS_L2`, `WITNESS_L3`) defined in the source advance the level / reach `WIN` when replayed against a fresh game instance.
- Initial geometry ironing took several iterations: WALK_STEP=4 forced a redesign of L2 to a single-pulley layout, and PLATFORM_W bumped from 5 → 7 cells so platforms align with avatar foot-cells stepped by 4 px. Witness lengths landed at 6/16/20 actions vs budgets 30/80/150 (≈5×, 5×, 7.5× generous).
- L3's cable-coupling is implemented by flipping both linked pulleys on a single ACTION5; opposite-phase coupling is encoded by the *initial states* (PA = LEFT_HIGH, PC = LEFT_LOW) — a simultaneous flip preserves the inverted relation. Cable polyline is rendered between PA and PC wheels along the beam.
- The hidden-floor-under-wall pattern is used to keep the path continuous after the wall removes (no special "floor reveal" logic needed — the floor sprites are TANGIBLE behind the wall sprite, and `_wall_blocks` skips REMOVED walls).
- `_get_valid_actions` excludes ACTION5 when no pulley is active — enforces "ACTION5 is only valid when a pulley is selected" (item 19 / state-visibility rule).
- Avatar variant swaps (`avatar` ↔ `avatar_carry_<colour>`) use `set_interaction(REMOVED/TANGIBLE)` to surface the carrying state in the rendered frame (item 19).
- ACTION7 absent (item 22).
- Metadata.json populated per `code/universal-scaffold.md` schema.
