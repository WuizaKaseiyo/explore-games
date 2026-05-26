# Step #08: smoke_test (visit 1)

## Inputs Consumed
- states/smoke_test.md (from harness root): 10-check battery + custom-check authoring rule.
- skills/code/smoke-test-checks.md (from prior steps): full check definitions, palette table, custom-check templates.
- prior-games/ek73/ek73.py + metadata.json (from #07): the implementation under test.
- workspace/mechanic-spec.md (v2, from #05): witness sequences for CHECK_WITNESS_WINS.

## Deliverables Produced
- `workspace/smoke-test-pass.md`: PASS table for all 9 universal + 1 visual + 4 custom checks.
- `workspace/smoke-test-custom.py`: 4 custom checks (arrow-moves, self-wake-kills, clearer-wipes-wake, warp-teleports). All passing.
- `workspace/smoke-frames/level_{1,2,3}.png`: rendered initial frames for visual sanity.

## Notes
- One implementation bug found and fixed mid-state: the pad-effect order in `step()` was applying clearer BEFORE wake-add, so the just-vacated cell got re-laid as wake AFTER clearer fired, leaving wake age 1 at the cell behind the avatar. L3's witness then soft-locked at (8, 1) because the descent path's first cell was wake-blocked. Fix: reordered `step()` to do (move → age existing wake → add vacated → trigger pad effects), so clearer wipes the just-added wake too. After the fix, L3 witness correctly reaches WIN at action 23.
- Visit count: 1/6.
- Transitioning to finalize.
