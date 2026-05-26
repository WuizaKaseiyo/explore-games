# Step #09: implement

## Inputs Consumed
- mechanic-spec.md v3
- critique-pass.md (clean verdict)
- skills/code/{universal-scaffold, novaengine-api, id-generation, smoke-test-checks}.md
- novaengine package signatures (base_game.py, level.py, sprites.py, camera.py)
- Reference game styles (cn04, sp80, wa30, sk48, tr87) from study state for layout idioms

## Deliverables Produced
- prior-games/dh4j/dh4j.py (673 lines)
- prior-games/dh4j/metadata.json
- implement-summary.md

## Notes
- Sprite pixel matrices implemented via tiny helper functions `_floor_pip_*(accent)` that emit the 8x8 pattern parameterized by the accent color — avoids 12 near-duplicate sprite definitions.
- Level layouts authored as string maps (`LEVEL_*_LAYOUT`) for readability; `_build_level_sprites` interprets the chars and emits placed Sprite instances.
- Slide animation done via the standard novaengine phase-tick idiom: `step()` short-circuits with `_slide_remaining > 0` to advance one cell per frame, only calling `complete_action()` when the slide finishes.
- Smoke-tested all 3 witnesses (L1: [UP, UP] → score 1; L2: [R, R, L, L, U, U, U] → score 2; L3: [R, U, R, R, L, L, L, U, U] → WIN). All three witnesses produce expected avatar trajectories and the game reaches WIN state.
- Cleaned up __pycache__ post-instantiation.
