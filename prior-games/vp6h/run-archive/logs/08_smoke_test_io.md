# Step #08: smoke_test

## Inputs Consumed
- prior-games/vp6h/vp6h.py (implementation from #07)
- skills/code/smoke-test-checks.md (9 universal checks + custom-check template)
- workspace/mechanic-spec.md revision 1 (for visual sanity grounding)

## Deliverables Produced
- workspace/smoke-runner.py — runs all 9 universal checks + 4 custom checks; renders L1/L2/L3 PNGs.
- workspace/smoke-test-custom.py — 4 custom checks: arrow movement, rail-click slides lantern, pickup-in-shadow advances level, pickup-in-light is no-op.
- workspace/smoke-frames/level_{1,2,3}.png — rendered initial frames per level.
- workspace/smoke-test-pass.md — all checks PASS.

## Notes
- All 9 universal checks pass. Camera viewport (16, 16) matches per level. Each level shows ≥10 distinct non-letter-box palette values. All declared actions [1, 2, 3, 4, 6] are branched in `step()`. No action raises. Pixel range stays in [1, 15]. `next_level()` and `lose()` calls are present in source.
- 4 custom checks pass. Visit 1 needed only one fix to a custom-check (initial version counted crystals on `current_level` AFTER pickup, but pickup transitioned to L2 which has 3 crystals — fixed by checking `_current_level_index == 1` after the action instead).
- CHECK_VISUAL_SANITY: opened the three rendered PNGs and confirmed each level matches the spec — yellow lantern at top (and bottom for L3), grey pillars, light-blue+purple crystals visible, magenta+maroon avatar, orange HUD bar. No glyphs resembling letters/digits. No catastrophic rendering bugs.
- Visit count for smoke_test: 1.
