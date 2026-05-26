# Step #05: implement

## Inputs Consumed
- `workspace/mechanic-spec.md` (from #03 write_spec).
- `workspace/critique-pass.md` (from #04 critique_spec).
- `skills/code/{universal-scaffold,novaengine-api,id-generation}.md`.
- `prior-games/kf42/kf42.py` (skimmed for house style — helper
  functions building per-level sprite lists, etc.).
- `game_sources/cn04/65d47d14/cn04.py` (read in full at study time;
  used as the template for `_get_valid_actions`,
  `display_to_grid` round-trip, and overall game-class structure).
- `novaengine` package source at
  `.venv/lib/python3.12/site-packages/novaengine/base_game.py`
  — needed to resolve runtime smoke-test failures (collidable filter
  on `get_sprite_at`; `next_level()` on last level → `win()`).

## Deliverables Produced
- `prior-games/qz73/qz73.py` (394 lines).
- `prior-games/qz73/metadata.json`.
- `workspace/implement-summary.md`.

## Notes
- Initial draft made tips `collidable=False`. The runtime smoke
  test surfaced that `get_sprite_at(x, y, "tip")` filters out
  non-collidables by default, so the click-to-lock path silently
  failed (lock state never changed). Fixed by setting
  `collidable=True` on the tip sprite.
- Initial draft of `_check_win` had `return matched` inside the
  inner loop instead of `break`, which would have returned
  prematurely on the first matching socket-slot pair. Fixed before
  the smoke test — caught by careful re-read.
- The `next_level()` on the last level transitions to
  `GameState.WIN` (per `novaengine.base_game.next_level` line 412).
  The level index does NOT advance past the last-index; the
  smoke-test verifies `WIN` via `g._state == GameState.WIN` rather
  than `g._current_level_index >= 3`.
- The "skip-locked-slots" rotation rule is essential. Without it
  L3 has no solution under the chosen colour assignment because
  rotated unlocked tips would collide with locked tips.
- Total qz73.py size (394 lines) is comfortably below the
  state's "400-1500 lines" guidance and matches the compactness of
  cn04 (681 lines for a similar surface complexity).
