# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revision 2 from #05): canonical layout per level + witnesses
- code/universal-scaffold.md (from study): file structure
- code/novaengine-api.md (read in this state): Sprite/Level/Camera/NovaBaseGame API
- .venv/.../novaengine/base_game.py (grep'd for `perform_action`): how to drive engine in tests

## Deliverables Produced
- prior-games/nz3v/nz3v.py: 415 lines, Python, parses cleanly.
- prior-games/nz3v/metadata.json: schema-compliant.
- implement-summary.md (workspace): summary + verification log.

## Notes
- Bug found and fixed mid-implementation: L1 target initially placed at (9, 9); spec says (10, 10). Updated `set_position(10, 10)`. After fix, L1 witness completes in 18 actions matching spec.
- All 3 witnesses (L1=18, L2=15, L3=15 actions) verified end-to-end via `perform_action`. State reaches `GameState.WIN` at end of L3 witness.
- Dark-cell death path verified.
- ACTION3 (left) with switch direction: `(_rotor_angle + _direction) % 4` correctly cycles 0 → -1 % 4 = 3 (SW) when direction=-1, matching the L3 witness's NW → SW transition at action 10.
- HUD overlays (WedgeOverlay / RotorDirectionMarker / StepCounterHud) all render without raising; 64×64 frame integrity preserved.
- `__pycache__` cleanup attempted; no cache directory present after run.
- Grid 12×12 with 5× camera scale produces 60×60 playable region centered in 64×64 with 2-px letterbox each side.
