# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (from #05 write_spec rev-2): full 9-section spec.
- workspace/critique-pass.md (from #06 critique_spec): 16/16 PASS + NOVEL verdict.
- workspace/mechanic-pick.md (from #02 pick_mechanic): ID `kf42`, family `tether-pawn-cycle`.
- skills/code/universal-scaffold.md: file structure (imports → sprites → levels → constants → HUD → game class).
- skills/code/novaengine-api.md: NovaBaseGame / Sprite / Level / Camera / RenderableUserDisplay / GameAction / InteractionMode / BlockingMode / ActionInput signatures.
- skills/global/{action-enum.md, color-legend.md, paths.md}: action and palette references.
- Reference games re-skimmed in spirit (read-in-full during study): m0r0 (orbit-pair clicker), sb26 (`_get_valid_actions` idiom), tu93 (clean step-bar HUD).

## Deliverables Produced
- prior-games/kf42/kf42.py (407 lines): full Python implementation of the spec; sprite bank (5 entries), 3 levels with helper builders, palette/dimension constants, two HUD widgets (StepBarHud + ActiveMarkerHud), the Kf42(NovaBaseGame) class with on_set_level, _get_hidden_state, _get_valid_actions, helper methods (_wall_at, _apply_cycler, _try_move_active, _check_win), and step().
- prior-games/kf42/metadata.json: matches the implement.md schema.
- workspace/implement-summary.md: file paths, line count, plain-English summary.

## Notes
- ast.parse: PASS.
- Smoke test: instantiation succeeds; pawns/targets/walls populate correctly; ACTION6 click selects the expected pawn; ACTION4 (right) moves the active pawn and triggers the tether-drag once the constraint binds.
- The engine attribute names are `_levels` and `_available_actions` (with leading underscore) — relevant when reading state externally.
- `__pycache__` directory cleaned post-test.
- Engine uses `BlockingMode.NOT_BLOCKED` on pawns to allow co-stacking (which the win predicate rejects naturally) and on cycler/target pads to allow pawns to land on top.
