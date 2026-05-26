# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (revision 2): 9-section spec
- workspace/critique-pass.md: confirmation that all 21 checklist items pass
- skills/code/universal-scaffold.md: file scaffold + style rules
- skills/code/novaengine-api.md: API reference (Sprite, Level, Camera, GameAction, InteractionMode, RenderableUserDisplay)
- game_sources_3_lvls/cn04 (read in full at study state): reference for ACTION6+ACTION5 dispatch + StepCounterHud pattern

## Deliverables Produced
- prior-games/kj82/kj82.py (730 lines)
- prior-games/kj82/metadata.json
- workspace/implement-summary.md

## Notes
- One bug found and fixed during runtime smoke: post_permeable was wrongly blocking the pawn's walk path. Spec was updated mentally — permeable posts allow passage for both planks and pawns; only blocking posts gate passage. Code updated to reflect this; witnesses now pass.
- Pawn-on-anchor cell test: at L1, pawn starts on plank cell (13, 10) which is offset (3, 0) from anchor (10, 10) — non-anchor. Pivot-carry works as designed.
- All three witnesses replay end-to-end and reach WIN state with score==3.
