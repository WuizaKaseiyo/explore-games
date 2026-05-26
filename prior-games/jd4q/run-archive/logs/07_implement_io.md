# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (revised, all 21 checklist items pass)
- skills/code/universal-scaffold.md
- skills/code/novaengine-api.md

## Deliverables Produced
- `prior-games/jd4q/jd4q.py` (530 lines): full source following universal-scaffold (imports → sprites → constants → HUD → level builders → game class). Semantic naming throughout (avatar, echo, door_open/sealed, pickup_a/b/c, goal, eraser, StepCounterHud, _handle_walk, _handle_egress, _handle_ingress, _check_win, etc.). No mechanic-revealing comments.
- `prior-games/jd4q/metadata.json`: per spec schema.
- `workspace/implement-summary.md`

## Notes
- Verified `python -c "import ast; ast.parse(...)"` parses the .py file (no SyntaxError).
- Runtime smoke test: instantiated `Jd4q()` successfully; traversed L1 (11 east-walks → next_level), L2 (south×6 east×6 east×6 click south×6 → next_level), L3 (south×6 east×6 north×6 click east×6 click south-eraser south×5 → WIN). Game state reaches `GameState.WIN` after L3 witness.
- Spec drift caught and fixed during smoke test: eraser was firing on egress instead of ingress per spec ("walking onto"). Fixed to fire when avatar enters the eraser cell (`_handle_ingress`); witness still solves all 3 levels. Trivial-fallback dynamics (greedy "C first" → trap) hold both ways.
- Cleaned up `__pycache__` from prior-games/jd4q/.
