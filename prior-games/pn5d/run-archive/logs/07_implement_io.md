# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (round-2 revision)
- skills/code/universal-scaffold.md (cached)
- skills/code/novaengine-api.md (cached)
- 5 reference source files cached from study state for idiom alignment.

## Deliverables Produced
- prior-games/pn5d/pn5d.py — 432 lines.
- prior-games/pn5d/metadata.json
- workspace/implement-summary.md

## Notes
- Sprite naming uses semantic English (vessel_outline, liquid_fill, target_mark, overflow_cap, valve_open, valve_closed, pour_cursor) per `code/universal-scaffold.md` § Style rules.
- L1 has 2 vessels with one fixed-open valve (no `valve_closed` sibling created — `make_valve_sprites` returns None for the closed slot when `fixed=True`).
- L2 has 3 vessels, both valves initially open (closed siblings REMOVED).
- L3 has 4 vessels, all 3 valves initially closed (open siblings REMOVED), C with overflow cap at level 2.
- Layout (per the spec's revised round-2 numbers):
  - VESSEL_TOP_Y = 8, VALVE_Y = 18, CURSOR_Y = 4.
  - L1 vessels at x = 23, 33; L2 at 16, 26, 36; L3 at 12, 23, 34, 45.
- `on_set_level` clones the clean level into the live slot and reconstructs `_vessels` and `_valves` lists by tag-querying.
- `_connected_group` does BFS through open valves to find which vessels rise on a pour.
- Post-pour, overflow caps clip oversize surfaces and surfaces are clamped at INTERNAL_H = 12.
- `_get_hidden_state` exposes vessel levels + valve open/closed flags as a single column.
- AST parse + runtime instantiation both pass; `__pycache__` cleaned.
