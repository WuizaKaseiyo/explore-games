# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec).
- workspace/critique-pass.md (from #04 critique_spec).
- skills/code/{universal-scaffold.md, novaengine-api.md, id-generation.md} (from #01 study).
- cn04 reference source (from #01 study).
- novaengine source (level.py, base_game.py, sprites.py, camera.py): for API details.

## Deliverables Produced
- prior-games/wt39/wt39.py: 337 lines.
- prior-games/wt39/metadata.json.
- workspace/implement-summary.md.

## Notes
- Caught one bug pre-smoke-test: `self._step_budget = 0` and `_steps_remaining = 0` were assigned AFTER `super().__init__()` which clobbered the values that `on_set_level` had already populated. Fixed by initialising those attributes BEFORE calling `super().__init__()`.
- Caught one API mismatch: novaengine-api.md cheatsheet implied `current_level` was prefixed `_current_level` but the property is `current_level`. Fixed all 4 helper methods.
- All 3 level witnesses verified end-to-end after fixes; full game clears to WIN.
- Used add_sprite/remove_sprite for thaw transition rather than the InteractionMode.REMOVED swap pattern; the dynamic add/remove is cleaner for this single transient state.
- Sprite naming is semantic per `code/universal-scaffold.md` § Style rules (no obfuscation).
EOF