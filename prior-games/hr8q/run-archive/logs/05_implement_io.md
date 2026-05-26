# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md
- workspace/critique-pass.md
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md
- prior-games/qb84/qb84.py and prior-games/qz73/qz73.py (template style)
- novaengine source for API verification (sprites.py, base_game.py, level.py)

## Deliverables Produced
- prior-games/hr8q/hr8q.py (729 lines)
- prior-games/hr8q/metadata.json
- workspace/implement-summary.md

## Notes
- Two engine pitfalls discovered during smoke:
  1. `Sprite.tags` is a property without a setter — must set unique
     `name=` (or use `clone(new_name=...)`) for sprites we need to
     look up later. Used `get_sprites_by_name` instead of
     `get_sprites_by_tag` for slot frames.
  2. `g.action = ...` is read-only; must use `g.perform_action(ActionInput(...))`
     to drive the engine in a smoke loop (which advances levels in
     the engine's main loop, not inside `step()`).
- L1 witness (3 actions), L2 witness (6 actions), L3 witness (7
  actions) all reach `GameState.WIN` as the spec predicts.
