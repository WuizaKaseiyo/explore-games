# Step #08: smoke_test (visit 1/6)

## Inputs Consumed
- prior-games/nb6t/nb6t.py (the just-generated source).
- prior-games/nb6t/metadata.json (the metadata sibling).
- mechanic-spec.md (rev. 2): for witness sequences and visual claims.
- skills/code/smoke-test-checks.md: 10 universal checks + custom-check template.

## Universal Checks Result
All 10 universal checks PASS.

| Check | Verdict |
|---|---|
| CHECK_CAMERA_VIEWPORT | PASS — camera == grid_size for every level |
| CHECK_SPRITE_CONTENT | PASS — 5 distinct non-letter-box values per level |
| CHECK_ACTION_BRANCHES | PASS — all 6 declared actions referenced in source |
| CHECK_ACTION_RUNTIME | PASS — no exceptions for any of {1..6} |
| CHECK_PALETTE_RANGE | PASS — frames in [0, 15] |
| CHECK_WIN_PATH_EXISTS | PASS — `self.next_level()` present |
| CHECK_LOSE_PATH_EXISTS | PASS — `self.lose()` present |
| CHECK_CAMERA_DEFAULT | PASS — uniform 64×64 grid; resize not required |
| CHECK_VISUAL_SANITY | PASS — rendered PNGs match spec per-level |
| CHECK_WITNESS_WINS | PASS — all three witnesses advance correctly to WIN |

## Custom Checks Authored
Authored 4 custom checks in `workspace/smoke-test-custom.py`, each ≤ 5 setup actions, ONE action under test, ONE boolean assertion, testing one essential mechanic invariant:

1. `check_action5_cycles_active_hinge` (Pattern C — modal action toggles state).
2. `check_action3_rotates_active_ccw` (Pattern C — modal action toggles state).
3. `check_action2_retracts_active_length` (Pattern C — modal action toggles state).
4. `check_click_on_hinge_sets_active` (Pattern B — click selects sprite).

All 4 custom checks PASS.

## Deliverables Produced
- `workspace/smoke-test-custom.py` (4 functions).
- `workspace/smoke-test-pass.md` (universal + custom checks table).
- `workspace/smoke-frames/level_1.png`, `level_2.png`, `level_3.png` (rendered initial frames per level).

## Notes
- Visit count: 1/6.
- During implement state, two pre-smoke bugs were caught and fixed: (1) action-count off-by-one in lose-check / HUD-update, (2) drop-then-immediate-pickup ordering bug. Both fixed before smoke_test.
- Transition: → `finalize`.
