# Step #08: smoke_test

## Inputs Consumed
- prior-games/qj4r/qj4r.py + metadata.json (from #07 implement)
- workspace/mechanic-spec.md (rev 2) for witness sequences
- skills/code/smoke-test-checks.md (universal + custom check spec)

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom-check functions (M1 reflection, M2 merge, M3 decoy cleanup, action-counter)
- workspace/smoke-test-pass.md: all universal + custom checks PASS
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames per level

## Notes
- All 9 universal checks PASS; all 4 custom checks PASS.
- Visual sanity: rendered frames match spec — checkered active region, correct piece/target/decoy roster per level, HUD bar visible.
- Initial bug in check_fold_reflects_piece: tested ACTION3 (the L1 winning fold) which advanced past the level before the post-fold sprite state could be inspected; switched to ACTION2 (non-winning fold) which exposes the y-axis reflection cleanly.
- Transitioning to finalize.
