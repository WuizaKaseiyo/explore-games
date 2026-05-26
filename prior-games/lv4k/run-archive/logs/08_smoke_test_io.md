# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/lv4k/lv4k.py (the implementation)
- skills/code/smoke-test-checks.md (universal checks + custom-check template)
- workspace/mechanic-spec.md (spec to compare against in CHECK_VISUAL_SANITY)

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (click_selects_tray_weight, place_changes_torque, passenger_displaces_on_high_tilt, l1_minimal_solve_advances). Each follows the strict template.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames per level.
- workspace/smoke-test-pass.md: all checks PASS.

## Notes
- All 8 universal structural/runtime checks PASS (CHECK_CAMERA_DEFAULT n/a since levels share grid_size).
- CHECK_VISUAL_SANITY initially flagged a forbidden-elements concern: the fulcrum_post sprite originally rendered as an upward-pointing arrow (narrow triangular head + thin post), which violates `forbidden-elements.md` ("an arrow shape implying direction"). Redesigned the fulcrum_post sprite as a trapezoidal block with a darker rectangular core — no directional implication — and re-rendered. Frames now pass visual sanity.
- All 4 custom checks PASS.
- All 3 witnesses (L1: 4 actions, L2: 6, L3: 8) end-to-end run correctly post-redesign; final state = WIN after L3.
- Visit count 1 / 6. Transitioning to finalize.
