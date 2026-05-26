# Fix Revisions (visit 1)

Edits applied to `prior-games/yf3h/yf3h.py` driven by `workspace/smoke-test-failures.md`.

1. **CHECK_VISUAL_SANITY (L3)** — sprite overlaps and OOB placement.
   - **Edit**: Redesigned the L3 level layout to use a 16×16 grid (vs 12×12 for L1/L2) and re-anchored every sprite so all bounding boxes fit within the grid AND no two gameplay sprites overlap. New L3 positions:
     - emitter_red (1, 5), emitter_blue (11, 6), emitter_green (1, 11)
     - resonator_multi_red_blue (6, 6), resonator_green (11, 11)
     - phase_delay_tile (11, 2)
     - pip_red (6, 4), pip_blue (9, 4)
   - **Mechanic preserved**: Manhattan distances re-computed so the multi-resonator activation only happens with phase-delay tile active. Without delay, red→multi=6 and blue→multi=5 (mismatched). With delay tile at distance 4 from blue, blue is delayed 1 tick → blue effective arrival = tick 6 = red's arrival. Tile is at distance 13 from red and 19 from green, so the tile does not affect the deciding tick for those rings.
   - **File range**: `levels = [...]` block, L3 entry replaced (the L3 `Level(...)` constructor's positional args + `grid_size=(16, 16)`).

2. **check_phase_delay_tile_toggle FAIL** — clicking a phase-delay tile didn't toggle it.
   - **Edit**: Removed `interaction=InteractionMode.INTANGIBLE` from the `phase_delay_tile` Sprite constructor in the sprite bank, so the sprite uses the default `InteractionMode.TANGIBLE`. `level.get_sprite_at` requires TANGIBLE for hit-testing; INTANGIBLE sprites were silently skipped. The collidable=False keyword stays — the tile still doesn't block sprite movement (this game has no movement).
   - **File range**: sprite bank `"phase_delay_tile"` entry; one line removed (the `interaction=` argument).

3. **Ring overlay sized to level grid** — implementation cleanup so L3's 16×16 overlay isn't capped to the 12×12 module constant.
   - **Edit**: `_clear_ring_overlay` and `_paint_ring_overlay` now compute width/height from `self.current_level.grid_size` instead of the module-level `GRID_SIZE = (12, 12)` constant. The sprite bank's initial `ring_overlay.pixels` is still 12×12 but is overwritten by `_clear_ring_overlay` in `on_set_level` to the right shape.
   - **File range**: `_clear_ring_overlay` and `_paint_ring_overlay` method bodies; ~6 line changes total.

## Post-edit verification

- `python -c "import ast; ast.parse(...)"` → SYNTAX OK.
- `uv run python -c "g = Yf3h(); ..."` → instantiated OK; level grid sizes (12,12)/(12,12)/(16,16); sprites per level 3/5/9.
- `__pycache__` cleaned up.

Ready for re-entry to `smoke_test`.
