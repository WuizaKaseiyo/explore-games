# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (revised, post-critique)
- workspace/critique-pass.md
- skills/code/universal-scaffold.md
- skills/code/novaengine-api.md
- prior-games/tj4f/tj4f.py (skim for modern scaffold style)
- game_sources_3_lvls/cn04/65d47d14/cn04.py (skim for runtime pixel mutation pattern)

## Deliverables Produced
- prior-games/kp9z/kp9z.py: 354 lines. Universal-scaffold layout: imports → palette/sprite-layout constants → cell-pixel factory + sprite factory → level layouts (L1/L2/L3) + level builder → 3-element levels list → StepCounterHud → Kp9z class with on_set_level / cascade helpers / _refresh_cell_pixels / _check_win / step / _get_hidden_state. Semantic naming throughout.
- prior-games/kp9z/metadata.json: schema-conformant.
- workspace/implement-summary.md.

## Verification
- ast.parse on kp9z.py: OK.
- Runtime instantiation: OK (3 levels, available_actions=[6], game_id="kp9z").

## Notes
- Cell sprites are 10x10 with internal frame + pip slots + type center. Sub-cell pip and notch features are 2x2 each, surviving 2x2 average pool.
- Cascade resolves in a bounded loop (max iterations = board_size² × 8) to handle the deterministic Abelian-sandpile redistribution. Redirector is special-cased: capacity 1, emits a single grain in its declared direction (south for the level layouts here).
- HUD bar at row 63 (palette 14 fill, palette 4 empty).
- Game grid_size set to (64, 64) for all levels; camera default applies; cell anchors recalculated per level (L1 anchor (12,12), L2/L3 anchor (7,7)).
- No comments reveal the mechanic (per universal-scaffold style rule).
