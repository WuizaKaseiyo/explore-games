# Step #06: smoke_test

## Inputs Consumed
- `prior-games/dj5h/dj5h.py` (from #05 implement).
- `mechanic-spec.md` (witness sequences and per-level descriptions, from #03 write_spec).
- `skills/code/smoke-test-checks.md` (universal-check + custom-check templates, from #01 study).

## Deliverables Produced
- `workspace/smoke-test-custom.py`: 4 mechanic-invariant checks (`check_action4_moves_avatar_right`, `check_click_on_wheel_selects_pulley`, `check_action5_flips_pulley_state`, `check_toggle_carries_avatar_when_on_low_platform`). All four pass.
- `workspace/smoke-test-pass.md`: per-check PASS table, ready for `finalize`.
- `workspace/smoke-frames/level_{1,2,3}.png`: rendered initial frames at 512×512 (8× upscale of 64×64 frame, NEAREST).

## Notes
- All 9 universal checks pass on first attempt (visit 1/6).
- All 4 custom checks pass on first attempt.
- WITNESS_WINS replays each spec witness against the loaded game and confirms each level advances; the L3 witness's final ACTION5 fires `next_level()` after reaching the goal at HIGH on PC-red, which the engine resolves to `WIN` since L3 is the last level.
- Visual sanity inspection: all 3 frames match the spec — pulley wheel(s) at top with rope-hanging coloured platforms, floor islands with avatar, peg/socket/wall in L2/L3, cable polyline visible across L3 between PA and PC. Goal marker renders slightly behind the platform's top edge at HIGH (same layer 2) but remains identifiable; non-catastrophic.
