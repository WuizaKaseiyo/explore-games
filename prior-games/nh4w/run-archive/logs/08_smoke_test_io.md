# Step #08: smoke_test (round 1)

## Inputs Consumed
- prior-games/nh4w/nh4w.py
- workspace/mechanic-spec.md (for witnesses + counterfactual claims)
- skills/code/smoke-test-checks.md
- skills/global/{action-enum, color-legend}

## Deliverables Produced
- workspace/smoke-test-custom.py (4 custom checks)
- workspace/smoke-test-pass.md (all 10 universal checks PASS, all 4 custom checks PASS)
- workspace/smoke-frames/level_{1,2,3}.png (rendered initial frames)

## Notes
- Universal checks all passed on first run.
- Initial CHECK_WITNESS_WINS for L3 FAILED: the L3 yellow shot from x=8 was incorrectly classified as colliding with ceiling1's bbox at frame x=16 (sprite y=43 overlapping ceiling y=43). Bbox collision was too pessimistic against the tapered stalactite. Switched implementation to PER-PIXEL collision (only fail if both projectile and blocker have non-transparent pixels at the same world coordinate).
- After per-pixel switch, the L3 yellow shot landed cleanly. But COUNTERFACTUAL binding then revealed the opposite problem: x=4 yellow / x=4 blue / x=8 blue all LANDED when spec wanted them BLOCKED. Per-pixel collision against the tapered stalactite tip (`[-1,-1,-1,13,-1,-1,-1,-1]` last row of original design — single drip pixel) was too thin to actually block projectiles passing under at columns away from the drip.
- Resolution: redesigned stalactite shape to have a SOLID 6-pixel-wide maroon bottom row (the dripping edge) instead of a single-pixel tip. This makes per-pixel collision reliable while preserving the tapered visual. Also shifted ceiling2 clearance from 14 to 13 (sprite height from 36 to 37) to ensure x=8 blue exceeds the new ceiling2 by enough margin.
- After both fixes: all witnesses pass, all 8 counterfactual cases match spec expectations (yellow only x=8, blue only x=12).
- Visual sanity per L1/L2/L3: all PASS via inline PNG inspection. The HUD (green) is visible at top, brick walls are unmistakable as walls, stalactites read as hanging blockers with red drip tips, targets read as framed squares of distinct colors.
