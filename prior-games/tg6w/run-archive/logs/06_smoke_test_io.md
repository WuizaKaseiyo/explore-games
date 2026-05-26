# Step #06: smoke_test

## Inputs Consumed
- prior-games/tg6w/tg6w.py (full): the implemented game source
- skills/code/smoke-test-checks.md (full): 9 universal-check definitions + custom-check template/constraints
- prior-games/tg6w/tg6w.py source code (re-read indirectly via running): action handlers, win/lose paths, camera mutation
- mechanic-spec.md (re-read for visual-sanity comparison): per-level expected sprite count, placement, HUD presence

## Deliverables Produced
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png: rendered initial frames per level (512×512 nearest-neighbour upscale of the 64×64 engine output) for the visual-sanity pass.
- workspace/smoke-test-custom.py: 4 custom checks: `check_down_advances_l1`, `check_no_op_action_consumes_step`, `check_rim_blocks_wrong_colour`, `check_sticky_catches_first_crosser`. Each ≤ 5 setup actions, ONE action under test (or in the L3 case, 3 setup actions then a check on accumulated state), ONE boolean assertion. Deterministic, < 1s wall time.
- workspace/smoke-test-pass.md: summary table per the schema in `code/smoke-test-checks.md`. All 9 universal checks pass; all 4 custom checks pass.

## Notes
- Every universal check passed on the first attempt.
- Visual-sanity (CHECK_VISUAL_SANITY) confirmed L3's deliberate "sticky-pad on yellow-target" overlay — rendered as yellow target corners + magenta plus-pattern centre, matching the spec's § 4.L3 prose and § 3 sprite-roster commentary.
- Custom-check fix mid-run: my first version of the slide-to-bottom check forgot that L1 transitions to L2 on the witness ACTION2 press, so the post-action `g.current_level` returns L2's blocks (still at row 1 base 3). Replaced with a level-advance check (`current_level_index: 0 → 1`), which is a cleaner integration test of the same M1 invariant.
- `__pycache__` cleaned post-test.
