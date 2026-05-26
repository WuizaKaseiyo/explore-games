# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revised)
- critique-pass.md
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md
- skills/global/{action-enum,color-legend,paths}.md
- prior-games/vt6q/vt6q.py (template for code structure)
- .venv/.../novaengine/{sprites,level,base_game}.py (API verification — Sprite has interaction property + set_interaction; Level has add_sprite + get_sprite_at(x, y, tag, ignore_collidable); is_collidable depends on TANGIBLE/INVISIBLE)

## Deliverables Produced
- prior-games/xz5g/xz5g.py (479 lines)
- prior-games/xz5g/metadata.json
- workspace/implement-summary.md

## Notes
- Witnesses verified by direct invocation: L1, L2, L3 each advance
  the score; L3 ends with state WIN.
- Caught and fixed an init ordering bug: the field defaults
  (_steps_left etc.) were being clobbered after super().__init__()
  ran on_set_level. Moved defaults to before super().__init__().
- Pixel matrices use exact spec arithmetic; rotation formula
  (CW/CCW) used directly for sprite repositioning.
- on_set_level resets per-level state including _visited_pins to
  empty, restores anchor_pin pixels to UNVISITED palette 14, and
  resets direction-indicator visibility.
- __pycache__ cleaned after smoke test.
