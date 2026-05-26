# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md (from #03): full 9-section spec; pixel matrices, level layouts, mechanics, witnesses.
- workspace/critique-pass.md (from #04): no spec issues; safe to implement as-is.
- skills/code/universal-scaffold.md (carried): file structure, Camera viewport rule, Style rules.
- skills/code/novaengine-api.md (carried): Sprite/Level/Camera/RenderableUserDisplay/NovaBaseGame APIs.
- prior-games/{kp9z,gx7m,vp6h}/{kp9z,gx7m,vp6h}.py: re-skimmed for code patterns (sprite-bank dict + clone+set_position; Level(sprites, grid_size, data); on_set_level resizing camera; step() dispatching on action.id; HUD subclass overriding render_interface).

## Deliverables Produced
- `prior-games/yf3h/yf3h.py` (629 lines, syntactically parses, instantiates without error; level count = 3; available_actions = [5, 6]).
- `prior-games/yf3h/metadata.json` (per finalize/index-row-format expected schema).
- workspace/implement-summary.md.

## Notes
- Followed `universal-scaffold.md` exactly: imports → sprite bank → levels → constants → HUD widget → game class. All names are semantic (no obfuscated tokens).
- Camera viewport rule: `on_set_level` resizes `camera.width = gw; camera.height = gh` from `level.grid_size`. All 3 levels share `(12, 12)` so this is informational; the resize would matter if grid_size differed.
- Multi-tick animation: implemented via the deferred-`complete_action()` pattern documented in `reference-game-patterns.md` § "Multi-phase step() with phase-tick sentinels". `step()` checks `_anim_active`; if True, advances one tick and returns WITHOUT `complete_action()`, expecting the engine to call `step()` again. If the engine doesn't support this pattern, smoke_test will catch it and `fix_implementation` can switch to inline-loop animation (compute final state synchronously, lose visual animation).
- Per-pixel-mutation visual cues: emitter arm-state, resonator activation, and phase-delay-tile state are all implemented by reassigning `sprite.pixels = np.array(...)` to the new pattern (matches the `_refresh_cell_pixels` pattern in `kp9z`).
- `_get_hidden_state` returns a 4×4 int16 grid summarising the per-game state (steps remaining, armed-emitter count, active-delay-tile count, activated-resonator count, animation flags).
- Click handling: `display_to_grid` → `level.get_sprite_at(gx, gy, tag)` for "emitter" then "phase_delay" — armable beats togglable if both occupy the same cell (none do in the levels).
- Cleaned up `__pycache__/` after the instantiation smoke test (per implement state §6).