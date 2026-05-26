# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (rev 2)
- workspace/critique-pass.md
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md
- novaengine source: .venv/lib/python3.12/site-packages/novaengine/{sprites,base_game,enums,level}.py (verified Sprite.clone/pixels assignment, GameAction enum, on_set_level call ordering)

## Deliverables Produced
- prior-games/qj4r/qj4r.py (435 lines): full game implementation
- prior-games/qj4r/metadata.json: standard metadata
- workspace/implement-summary.md: file paths + plain-English summary + smoke-test results

## Notes
- Initial bug: `_cell_size` was assigned AFTER super().__init__() but `set_level(0)` (called by super) invoked on_set_level which used self._cell_size. Fixed by moving attribute init before super().__init__().
- All three level witnesses verified pre-finalize: `[ACTION3]` for L1, `[ACTION3, ACTION4]` for L2, `[ACTION3, ACTION4, ACTION1]` for L3. Final game state = `GameState.WIN`.
- Used semantic names throughout (no obfuscation per universal-scaffold style rules).
- __pycache__ cleaned up.
