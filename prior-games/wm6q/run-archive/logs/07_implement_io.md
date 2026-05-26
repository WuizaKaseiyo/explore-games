# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (final from #06 critique_spec): 9-section spec including
  per-level base-assignment tables, witness solutions, and per-level data
- skills/code/{universal-scaffold, novaengine-api, id-generation}.md
- skills/global/{action-enum, color-legend, paths}.md

## Deliverables Produced
- `prior-games/wm6q/wm6q.py` — full game source (394 lines).
- `prior-games/wm6q/metadata.json` — required-schema metadata.
- `workspace/implement-summary.md` — paths, line count, plain-English summary.

## Notes
- Single-action game (`available_actions = [6]`). ACTION6 click handler
  resolves target tile via `camera.display_to_grid` + bounding-box check
  against each tile's `pixel_origin`.
- Tile pixel arrays are dynamically painted via `_paint_tile_pixels(base,
  rotation, glyph)`; called once in `on_set_level` and again on every rotation
  click. Locked-tile clicks bypass rotation and don't deduct from
  `_steps_used`. Linked-pair clicks rotate both pair members.
- HUD: `StepBarHud` paints frame row 63 with yellow active / black depleted
  proportional to `(step_budget - _steps_used) / step_budget`.
- Win predicate `_check_win()` walks the level's tile-grid by pixel-origin
  adjacency and compares right/bottom shared edges; fires `next_level()` on
  full match. Lose predicate fires `lose()` when `_steps_used >= step_budget`.
- Ran AST parse + runtime instantiation smoke test before transition; both
  pass. `__pycache__` cleaned.
