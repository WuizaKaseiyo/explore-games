# Step #03: implement

## Inputs Consumed
- workspace/mechanic-spec.md, critique-pass.md
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md
- prior-games/hr8q/hr8q.py (template style, especially the `clone(new_name=...)` pattern)
- novaengine source for API verification

## Deliverables Produced
- prior-games/ng52/ng52.py (561 lines)
- prior-games/ng52/metadata.json
- workspace/implement-summary.md

## Notes
- Discovered and fixed a pixel-count bug in the L2/L3 object roster: the original Z-tromino had 4 pixels, not 3. Replaced with three distinct connected L-tromino orientations (L, J, R).
- Importing the module via `importlib.util.spec_from_file_location` requires registering the module in `sys.modules` BEFORE `exec_module` (otherwise `dataclass` fails to resolve `cls.__module__`). This affects both the smoke runner and the custom-check loader; the runner script handles it explicitly.
- Witnesses for L1 (7 actions), L2 (13), L3 (13 with distractor untouched) all reach `GameState.WIN`.
