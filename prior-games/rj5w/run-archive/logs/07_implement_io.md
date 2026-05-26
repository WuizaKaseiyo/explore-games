# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revision 1) and critique-pass.md
- skills/code/{universal-scaffold,novaengine-api,id-generation,spec-template}.md
- Reference source files re-skimmed in study (cn04, wa30, tr87, tu93, r11l) for house style
- novaengine package source (`base_game.py`, `enums.py`) — for ActionInput / perform_action / set_level signatures

## Deliverables Produced
- `prior-games/rj5w/rj5w.py` (443 lines)
- `prior-games/rj5w/metadata.json`
- `implement-summary.md` (workspace) summarising paths + smoke-test verdict

## Notes
- Universal scaffold followed: imports → sprite bank → levels → constants → HUD class → game class.
- Semantic naming throughout (no obfuscation): `pawn_green`, `target_yellow`, `fold_line_v`, `StepCounterHud`, `_commit_fold`, `_check_win`, `_dim_pawn`, etc.
- Fold-line cursors use `InteractionMode.INTANGIBLE` so they don't block pawns; their orange/grey state is achieved via runtime `color_remap`.
- Locked pawns are dimmed via `color_remap(<base>, 3)`; the persistent visual cue per checklist item 19.
- Two bugs were caught at smoke-test time and fixed in-state (not flagged to fix_implementation): attribute init order + RESET budget decrement. Both fixes are local to the game class.
- AST parse OK; instantiation OK; all three witness sequences end-to-end win.
- `__pycache__` cleaned after smoke test.
