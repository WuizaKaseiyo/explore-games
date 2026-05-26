# Step #05: implement

## Inputs Consumed
- mechanic-spec.md (from #03): the spec.
- critique-pass.md (from #04): green-light verdict + implementation notes (reserve y=0 for HUD; same-parity goals).
- skills/code/universal-scaffold.md: file structure.
- skills/code/novaengine-api.md: API reference.
- game_sources_3_lvls/cn04/65d47d14/cn04.py (read in #01): reference style.
- .venv novaengine/base_game.py: confirmed `perform_action(ActionInput)` is the runtime entry point and `g._levels` is the levels list attribute.

## Deliverables Produced
- prior-games/tb4k/tb4k.py (390 lines): full implementation.
- prior-games/tb4k/metadata.json: standard metadata.
- implement-summary.md: paths, line count, runtime smoke test results.

## Notes
- Syntax check passed via `ast.parse`.
- Runtime smoke test ran all three level witnesses successfully + verified hole-death respawn.
- One minor naming surprise: NovaBaseGame stores levels under `_levels` (not `levels`); test scripts must use `g._levels`.
- ACTION input is set via `g.perform_action(ActionInput(id=...))`, not by directly assigning `g.action`.
- __pycache__ cleaned up.
