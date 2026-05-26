# Step #06: smoke_test

## Inputs Consumed
- `prior-games/fz5j/fz5j.py` (from #05 implement).
- `workspace/mechanic-spec.md`: source of truth for visual sanity comparison.
- `skills/code/smoke-test-checks.md`: 9 universal checks + custom-check authoring template.

## Deliverables Produced
- `workspace/smoke-test-custom.py`: 4 custom checks (`check_right_moves_avatar`, `check_phase_tile_blocks_on_wrong_residue`, `check_step_counter_ticks_on_blocked_move`, `check_lose_at_budget`).
- `workspace/_smoke_runner.py`: harness that runs all 9 universal + custom checks and renders 3 PNGs.
- `workspace/smoke-frames/level_{1,2,3}.png`: rendered initial frames for visual sanity.
- `workspace/smoke-test-pass.md`: pass report.

## Notes
- All 9 universal checks PASS (camera viewport, sprite content, action branches, action runtime, palette range, win path, lose path, camera default, visual sanity).
- All 4 custom checks PASS.
- Visual sanity: phase tiles whose (period, offset) makes them closed at step 0 render as solid black squares — initially this might confuse a player into thinking they are walls, but the first action triggers a step counter increment and the tile pulses open if its residue matches. This is consistent with the mechanic ("learn by playing"). Documented in pass report.
- No `__pycache__` directories created in `prior-games/fz5j/` (smoke loader uses `importlib.util.spec_from_file_location` which does not write bytecode by default).
