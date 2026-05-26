# Step #05: implement

## Inputs Consumed
- `workspace/mechanic-spec.md` (from #03 write_spec).
- `workspace/critique-pass.md` (from #04 critique_spec).
- `skills/code/universal-scaffold.md`: file structure, two-sprite-swap idiom, simultaneous-conflict resolution, camera viewport rule.
- `skills/code/novaengine-api.md`: API signatures (Sprite, Level, Camera, NovaBaseGame, GameAction, InteractionMode).
- Five reference source files re-skimmed in spirit (cn04, sp80, tr87, r11l, wa30) for house-style patterns.

## Deliverables Produced
- `prior-games/fz5j/fz5j.py` (608 lines).
- `prior-games/fz5j/metadata.json`.
- `workspace/implement-summary.md`.

## Notes
- Caught an L3 layout bug during smoke-test: the row-2 wall barrier had gaps at cols 1, 10, AND 14 (only intended col 10), and the col-9/11 bracket walls only ran to row 11. Both gave the avatar bypass routes around the witness path. Patched: row-2 walls now cover cols 1-9 and 11-14 (only col 10 open), and bracket walls extend through row 14.
- Two-sprite-swap implementation: each phase tile cell pre-places both `*_open` and `*_closed` sprites at the same position; `_refresh_phase_tiles()` flips `InteractionMode.TANGIBLE` / `InteractionMode.REMOVED` on each step based on `(step_counter % period) == offset`. Fragile cells additionally pre-place a `fragile_locked` sprite (initially REMOVED) that becomes TANGIBLE on first blocked entry.
- Camera resize unnecessary because all levels declare `grid_size=(64, 64)` directly.
- Smoke tests verified:
  - L1 witness (14 ACTION4) → advances to L2.
  - L2 witness (16 ACTION4) → advances to L3.
  - L3 witness (11 ACTION4 + 15 ACTION2) → reaches goal, full game state = WIN.
  - L1 budget-exhaust (22 ACTION1 wall-bounces) → GAME_OVER at t=22.
  - Fragile mis-timed entry (deliberate U+D wiggle to misalign residue at (10,12)) → cell locked, BFS detects path-blocked, GAME_OVER fires.
- No `__pycache__` directories left behind under `prior-games/fz5j/`.
