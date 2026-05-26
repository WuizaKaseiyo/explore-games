# Step #05: implement

## Inputs Consumed
- `workspace/mechanic-spec.md` (from #03): the 9-section spec.
- `workspace/critique-pass.md` (from #04): clean checklist verdict.
- `skills/code/universal-scaffold.md`: file structure (sprite bank
  → levels → constants → HUD → game class).
- `skills/code/novaengine-api.md`: Sprite / Level / Camera / GameAction
  / InteractionMode signatures.
- `.venv/lib/python3.12/site-packages/novaengine/sprites.py`: confirmed
  the `Sprite.__init__(x=, y=, ...)` constructor accepts pixel-
  position directly (no `set_position` call needed for level-build).
- `.venv/lib/python3.12/site-packages/novaengine/level.py`: confirmed
  the `Level.__init__(data=...)` parameter takes a dict (the engine
  has no `Level.set_data` method; the spec was edited to use the
  constructor form).

## Deliverables Produced
- `prior-games/mw8p/mw8p.py` (423 lines).
- `prior-games/mw8p/metadata.json` (per schema).
- `workspace/implement-summary.md`.

## Notes
- One spec/engine mismatch fixed during implement: spec described
  per-level data via `level.set_data(...)`; the novaengine `Level` API
  has no `set_data` method (only `get_data`), so the implementation
  passes per-level data via `Level(data={...})` at construction time.
- All three level witnesses verified by direct engine replay (action
  sequences fired via `perform_action(ActionInput(...))`), each
  advancing the engine's `_score` by 1 and the third reaching the
  `WIN` state. No syntax or runtime errors.
- `__pycache__` cleanup performed.
