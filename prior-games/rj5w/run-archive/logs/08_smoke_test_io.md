# Step #08: smoke_test

## Inputs Consumed
- mechanic-spec.md (revision 1) — for witness sequences and per-level expectations
- prior-games/rj5w/rj5w.py — the implementation under test
- prior-games/rj5w/metadata.json — sanity check on shape
- skills/code/smoke-test-checks.md — universal-check definitions and custom-check template
- novaengine package — for ActionInput / GameAction / perform_action

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (v-fold reflection, axis-toggle via click, lock-freezes-pawn, lose-at-budget). All conform to the strict template (≤ 5 setup actions, single boolean assertion).
- workspace/smoke-frames/{level_1,level_2,level_3}.png: rendered initial frames for visual-sanity.
- workspace/smoke-test-pass.md: PASS verdict for all universal + custom + visual checks.

## Notes
- Universal checks: 9/9 pass. CHECK_CAMERA_DEFAULT marked pass-by-default since all levels share grid_size=(64,64) and no resize is needed.
- CHECK_WITNESS_WINS replayed all three witnesses end-to-end; final state was GameState.WIN.
- Custom checks: 4/4 pass. M1 (V-fold reflection), M3 (axis toggle), M4 (lock), and the lose-path are each independently verified.
- CHECK_VISUAL_SANITY: I opened each rendered initial frame and confirmed sprite count, placement, HUD presence, and absence of catastrophic rendering bugs. No sprite resembles a digit, letter, or arrow glyph.
- One observation worth carrying forward: in L3, the yellow pawn at (28, 28) is rendered with the V-line cursor (col 28) passing through its leftmost column. This is intentional (lines are INTANGIBLE) and reads cleanly in the rendered frame; the line goes "behind" the pawn since pawns render on a higher layer.
- Visit count: 1 of 6 cap. Transition: smoke_test → finalize.
