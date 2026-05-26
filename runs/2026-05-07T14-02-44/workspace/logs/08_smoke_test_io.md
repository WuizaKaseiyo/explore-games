# Step #08: smoke_test (visit 2/6)

## Inputs Consumed
- prior-games/yf3h/yf3h.py: post-fix source (L3 redesigned for 16×16 grid; phase_delay_tile collidable=True).
- workspace/fix-revisions.md (from #07).
- workspace/smoke-test-custom.py (from #06): the 4 custom checks.
- workspace/mechanic-spec.md (carried): per-level descriptions for CHECK_VISUAL_SANITY.

## Deliverables Produced
- workspace/smoke-test-pass.md: all 9 universal + 4 custom checks PASS.
- workspace/smoke-test-custom.py: unchanged from visit 1 (the checks themselves were correct; the implementation was the bug).
- workspace/smoke-frames/level_{1,2,3}.png: re-rendered after L3 redesign.

## Notes
- L3 grid changed to 16×16; CHECK_CAMERA_DEFAULT now correctly triggers (different grid_sizes across levels) and the per-level camera resize in `on_set_level` handles it.
- L3 rendered frame: 3 corner-positioned emitters (red top-left, blue top-right, green bottom-left), multi-resonator centred with red+blue pips above, green-resonator at right-bottom, phase-delay tile (4 magenta corner-dots inactive state) at top-right.
- check_phase_delay_tile_toggle now passes after switching `phase_delay_tile.collidable=True`. The engine's `level.get_sprite_at` honours `collidable` by default — collidable=False sprites are silently skipped from hit-testing. INTANGIBLE was a separate but compounding issue (also removed in #07).
- Visit count: 2/6 — transitioning to finalize.