# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec): 9-section spec including witnesses.
- workspace/critique-pass.md (from #04 critique_spec): PASS verdict.
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md.
- game_sources/cn04/65d47d14/cn04.py (read in #01 study): pattern templates for `RenderableUserDisplay`, `_get_valid_actions`, level-data dict reads, sprite cache pattern.
- game_sources/sp80/0ee2d095/sp80.py (read in #01 study): tag-based queries, multi-state game logic, `level.set_data` patterns.
- .venv/lib/python3.12/site-packages/novaengine/{camera.py,base_game.py,sprites.py}: API verification — checked Camera._calculate_scale_and_offset, NovaBaseGame.perform_action loop, Sprite.clone signature.

## Deliverables Produced
- prior-games/lq5x/lq5x.py (440 lines): full game source.
- prior-games/lq5x/metadata.json: schema-conformant.
- workspace/implement-summary.md: paths, line count, plain-English summary.

## Notes
- Sprite roster simplified from spec §3 to use 1×1 lantern (instead of 3×3) — 1×1 renders correctly at the per-grid scale (5×5 pixels for a 12×12 grid) and avoids sprite-bounds quirks. Targets remain 3×3 hollow rings; pickups and filters remain 1×1. The "lantern centre" position is just the sprite's (x, y).
- One bug discovered + fixed during smoke-test: `lit_targets` was a `set[str]` keyed on `t.name`, but Sprite clones share the same name (`tytkbflqjr` for both yellow targets in L1). When one target was lit, the other appeared lit too because the predicate checked name membership. Fixed by switching `lit_targets` to a `set[int]` keyed on `id(t)` (Python object identity per cloned Sprite instance).
- `_scan_filter_and_targets` runs after every action, in two passes: filter pass (find filters in cone, pick closest by Manhattan, update `cone_color` to its colour); target pass (for each target, if its centre is in cone AND `cone_color == target_color`, add to lit set).
- ConeOverlay (HUD) reads game state via a `configure(...)` method called from `_update_overlay`, which the game class invokes after every action. Overlay paints background-coloured (palette 5) pixels inside the cone to a "lit" shade — palette 1 (off-white) when cone is yellow; palette 13 (maroon) when cone is red. Sprites inside the cone remain visible because their pixels aren't background.
- The transition condition for `smoke_test` (both files exist + .py parses + runtime instantiation works) is satisfied. Proceeding.
