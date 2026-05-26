# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revised, post-critique)
- skills/code/universal-scaffold.md (file structure, naming)
- skills/code/novaengine-api.md (Sprite/Level/Camera signatures)
- 5 reference source files read in #01 (cn04, m0r0, sp80, sk48, cd82) for API idiom + style.

## Deliverables Produced
- `prior-games/qn7w/qn7w.py` (648 lines)
- `prior-games/qn7w/metadata.json` (schema-conformant)
- workspace/implement-summary.md

## Notes
- Followed universal-scaffold.md exactly: imports → sprite bank → levels → constants → HUD widgets → game class. Class body order: `__init__` → `on_set_level` → `_chain_by_*` helpers → `step` → `_cycle_junction` / `_fire_pulse` / `_terminal_and_axis` / `_ball_color` / `_process_eject` / `_remove_terminal_from_chain` / `_check_win` → `_get_hidden_state` → `_get_valid_actions`. Module-level helpers for sprite-pixel patterns (`_empty_socket_pixels`, `_filled_socket_pixels`, `_empty_merge_pad_pixels`, `_half_merge_pad_pixels`, `_full_merge_pad_pixels`, `_junction_pixels`).
- All sprite names, helper names, and constants are semantic (per universal-scaffold.md "Style rules" — no obfuscated tokens). Class name `Qn7w` follows the Pascal-case-of-game-id convention.
- Per-level data dict (`Level(... data={"step_budget": N, "chains": [...]})`) drives runtime state initialisation in `on_set_level`.
- Camera viewport explicitly resized in `on_set_level` per scaffold guidance (defensive — all levels are 64×64 here, so it's a no-op, but it future-proofs the code).
- Bug found & fixed during smoke: `Level.get_sprite_at(x, y, tag=...)` requires a non-transparent pixel under (x, y); sprite top-left corners are `-1`. Replaced terminal-ball / socket / pad lookups with a position-matching helper.
- Witness solutions for L1, L2, L3 all execute correctly under direct method invocation. L2 counterfactual confirmed: without junction flip, the level cannot be won (down-branch consumed by wall, active branch empties, subsequent clicks become no-ops, socket never fills).
- `_get_valid_actions` enumerates only the centres of `pusher_knob` and `junction_node` sprites in the current level, keeping the agent's action space focused.
- Cleared `__pycache__` after smoke test.
- Transitioning to `smoke_test` for the harness's full smoke check.
