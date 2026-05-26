# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == grid_size for every level |
| CHECK_SPRITE_CONTENT | 4 | 6 | 8 | distinct non-letter-box palette values per level (≥ 2 threshold) |
| CHECK_ACTION_BRANCHES | ✅ | — | — | ACTION6 (the only declared action) has a `step()` branch |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION6 click runs without exception |
| CHECK_PALETTE_RANGE | 0..15 | 0..15 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source (`self.win()` not used; engine auto-fires `win` after final `next_level()`) |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 witness: score 0→1; L2: 1→2; L3: state==WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels are 64×64 (no per-level resize *needed*); source still resizes defensively in `on_set_level` |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per level

- **L1** (`level_1.png`): one purple-rimmed pusher button on the left, four blue round balls in a contiguous horizontal chain, one black hollow ring socket on the right of the chain, step-counter bar visible at bottom (row 63). Matches spec § 4 L1 layout (1 pusher, 4 balls, 1 socket; horizontal chain).
- **L2** (`level_2.png`): pusher on left, horizontal stem of 3 blue balls leading to a junction node with a green tab in the *bottom half* (default active = "down"), vertical up-branch of 3 balls leading to a hollow blue socket at the top, vertical down-branch of 3 balls leading to a solid black wall (dead_end_wall) at the bottom. Junction's green tab indicator is clearly visible in the lower half. HUD bar visible. Matches spec § 4 L2 layout.
- **L3** (`level_3.png`): two chains converging on a central merge_pad. Bottom-left: blue chain A (pusher → 2 stem balls → junction with green tab in bottom half → 3 up-branch balls reaching toward centre, 1 down-branch ball + black wall below). Top-right: yellow chain B (pusher → 2 stem balls → junction with green tab in bottom half → 2 left-branch balls reaching toward centre, 1 down-branch ball + black wall below). Merge_pad with orange centre pip visible at the chains' convergence. HUD bar visible. Matches spec § 4 L3 layout.

No catastrophic rendering bugs. No sprite shapes that resemble letters, digits, or directional arrows. The pusher_knob redesign (Critique-1 Issue 2) renders as a clean recessed button without directional protrusion.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_pulse_eject_fills_l1_socket` | socket pix[2,2]=9 | One click on the only L1 pusher fills the only L1 target socket. Confirms pulse-eject + socket-fill mechanic end-to-end. |
| `check_junction_click_cycles_active_branch` | before=down after=up | L2 junction click toggles the active_branch state from "down" to "up" (binary cycle). Confirms junction-routing cycle invariant. |
| `check_dead_end_wall_consumes_eject` | down-branch len: 3 → 2; socket_filled=False | L2 fire with default-down junction shrinks down-branch by exactly 1 ball *and* leaves the up-branch's socket empty. Confirms dead_end_wall consumes ejects without filling sockets — the counterfactual rationale of L2's junction-routing necessity. |
| `check_merge_pad_lights_on_second_deposit` | merge_pad pix[2,2]=0 deposits={(20, 22): 2} | After flipping both junctions and firing both chains, the merge_pad's deposit count is 2 and its centre is filled white (palette 0). Confirms merge-on-coincidence end-to-end. |

Visit count: 1/6.

All checks pass. Transitioning to `finalize`.
