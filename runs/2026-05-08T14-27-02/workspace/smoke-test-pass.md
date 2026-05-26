# smoke-test-pass — `vy3m`

13 PASS, 0 FAIL, 1 SKIPPED.

## Universal checks (11 — note: NEW CHECK_TRIVIAL_FAILS)

| # | Check | Result |
|---|---|---|
| 1 | CHECK_CAMERA_VIEWPORT | PASS |
| 2 | CHECK_SPRITE_CONTENT | PASS |
| 3 | CHECK_ACTION_BRANCHES | PASS (5/5 declared actions) |
| 4 | CHECK_ACTION_RUNTIME | PASS |
| 5 | CHECK_PALETTE_RANGE | PASS |
| 6 | CHECK_WIN_PATH_EXISTS | PASS |
| 7 | CHECK_WITNESS_WINS | PASS (L1: 5 actions; L2: 9 actions; L3: 14 actions reach WIN) |
| **8** | **CHECK_TRIVIAL_FAILS (NEW)** | **PASS** |
| 9 | CHECK_LOSE_PATH_EXISTS | PASS |
| 10 | CHECK_CAMERA_DEFAULT | PASS |
| 11 | CHECK_VISUAL_SANITY | SKIPPED (vision-pass; manual verification) |

### CHECK_TRIVIAL_FAILS detail

The new gate replays each level's declared trivial heuristic and asserts the level does NOT advance:

- **L2** trivial = `[ACTION4 × 12]` ("always Pusher, press right"): runs from L2 start; pusher pushes crate_a past target (target_a uncovered after crate goes to (9,2)+); pull lane is sealed by walls (rows 6, 8); Puller never activated; crate_b never moves. L2 score stays at 1. **Trivial fails as expected — game has planning depth.**
- **L3** trivial = `[ACTION4 × 15]`: same pattern; pusher pushes crate_a past target; pull and chain lanes sealed; Puller and Stomper never activated. L3 doesn't WIN. **Trivial fails as expected.**

Both witness AND trivial checks pass simultaneously: witness is the *intended* solve, trivial is the *anti-solve*. The contrast confirms vy3m has genuine planning structure.

## Custom checks (3)

| # | Check | Result |
|---|---|---|
| 1 | custom_action5_cycles_class | PASS (Pusher → Puller → Pusher cycle) |
| 2 | custom_puller_blocked_by_crate_in_front | PASS (Puller walking into crate is no-op) |
| 3 | custom_stomper_chain_push | PASS (Stomper chain-pushes 2 adjacent crates one cell each) |

## Found-and-fixed bug (in test only, not game source)

L1 witness initially had 6 ACTION4 (1 too many; 5 suffices). The 6th ACTION4 spilled into L2 after L1's `next_level()` fired, displacing pusher one cell ahead and causing crate_a to be pushed past target. Fixed by adjusting WITNESSES dict to `[act(4)] * 5` for L1. **Game source unchanged.**

This is the kind of bug the new gate would NOT have caught (it was a witness off-by-one, not a trivial-heuristic failure). CHECK_WITNESS_WINS caught it correctly.
