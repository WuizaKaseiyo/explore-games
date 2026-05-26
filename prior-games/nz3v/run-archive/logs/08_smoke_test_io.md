# Step #08: smoke_test (visit 1 of 6)

## Inputs Consumed
- prior-games/nz3v/nz3v.py (from #07): generated source
- code/smoke-test-checks.md (from state Skills): 10 universal-check definitions + custom-check template

## Deliverables Produced
- smoke-test-custom.py (workspace): 4 custom checks (action4-moves-east, action-counter, rotor-advances-after-K, stop-tile-freezes).
- smoke-test-pass.md (workspace): PASS table for all 10 universal + 4 custom checks.
- smoke-frames/level_{1,2,3}.png (workspace): rendered initial-state PNGs of each level for the visual sanity pass.

## Notes
- All 10 universal checks pass; all 4 custom checks pass.
- Visual sanity inspection on all 3 PNG renders confirms correct sprite placement, wedge-pattern tint over NW quadrant, rotor with both yellow notch + magenta direction marker visible, walls/stop-tile/switch correctly placed per level layout, step-counter bar visible on bottom row.
- L1 witness (18 actions), L2 witness (15 actions), L3 witness (15 actions) all advance the engine state through the level sequence to GameState.WIN.
- Custom check `check_stop_tile_freezes_rotor` shows `frozen_after=3` immediately after stepping on the tile (K_FREEZE=4 minus the in-step `_advance_rotor` decrement = 3); semantically correct.
- No transition back to `fix_implementation` needed; transition forward to `finalize`.
