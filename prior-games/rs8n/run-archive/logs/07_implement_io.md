# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revised post critique pass 1)
- critique-pass.md (verdict PASS)
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md
- game_sources_3_lvls/cn04 + wa30 + sk48 + tu93 (re-skimmed step() / on_set_level patterns from study state)

## Deliverables Produced
- prior-games/rs8n/rs8n.py (679 lines): full game source per universal-scaffold (imports → sprite bank alphabetised → levels → constants → HUD widget class → game class with `Rs8n(NovaBaseGame)` body order: `__init__` → `on_set_level` → helpers → sweep state machine → step → introspection).
- prior-games/rs8n/metadata.json: schema-conforming.
- workspace/implement-summary.md: paths, line count, plain-English rule, smoke-test result.

## Notes
- Two bugs caught during smoke test, both fixed before transitioning:
  1. **Items invisible to get_sprite_at at cell top-left** — items have transparent corners; default PIXEL_PERFECT collision skips them. Fix: `blocking=BlockingMode.BOUNDING_BOX` on items only (perimeter walls retain PIXEL_PERFECT so the interior remains walkable).
  2. **Non-collidable shifter skipped by get_sprite_at** — shifter is INTANGIBLE → `is_collidable` returns False; default query skipped it. Fix: pass `ignore_collidable=True` only on the shifter-detection query.
- Full witness `[4,4,5, 4,5, 4,5,2,2,2,2,2,4,5]` runs end-to-end and triggers `GameState.WIN`. Animation phases (`outgoing` / `return`) work correctly across all three levels' sweeps.
