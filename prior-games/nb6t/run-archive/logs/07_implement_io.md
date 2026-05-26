# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (rev. 2): full 9-section spec.
- skills/code/universal-scaffold.md: file structure and style rules.
- skills/code/novaengine-api.md: engine API.
- skills/code/id-generation.md: ID rules.
- skills/code/spec-template.md: spec format reference.
- novaengine source under .venv (sprites.py, level.py, base_game.py, camera.py): API verification.

## Implementation Decisions
- **File structure**: imports → sprite-bank builders → sprite bank dict → levels list → constants → HUD widget → game class. Matches `code/universal-scaffold.md`.
- **Naming**: meaningful semantic names throughout per `universal-scaffold.md` § Style rules. Class name `Nb6t` (Pascal of game ID).
- **Pose representation**: each segment carries (theta_i ∈ {0, 90, 180, 270}, length_i ∈ {1..14}). The chain's hinge positions are computed via forward-kinematics from the base.
- **Rendering**: `_render_chain` rebuilds segment pixel arrays per (theta, length), repositions sprites, places hinges/tip/halo. Called after every action.
- **Pose validity**: `_pose_in_bounds` checks every segment-cell's bounding box against grid limits. Rotations and length-changes that would go out-of-bounds are rejected (action consumed, no state change).
- **HUD**: `StepCounterHud` subclass renders bar at row 63, filled-cells = 64 * (current/max).
- **Action gating**: `_get_valid_actions` returns actions per the level's `level_actions` data list. L1 = [3,4,5,6]; L2,L3 = [1..6].
- **Carry-and-drop**: pickup is auto-triggered when tip cell == object cell and not carrying. Drop is via ACTION6 click on tip when carrying. Critical: win check runs *before* pickup check in `step()` so a drop-on-target wins before re-pickup.

## Bugs Found and Fixed During Smoke Test
1. **Step ordering bug**: initial implementation ran `_check_pickup` before `_check_win_loss`. After ACTION6 drop on drop-zone, the carrying state was cleared but `_check_pickup` immediately re-picked up the dropped object (tip cell == object cell). Fixed by reordering to `_render_chain → _update_hud → _check_win → _check_pickup → _check_lose`. Win check is run with the just-dropped state.
2. **Action-count off-by-one**: initial code used `self._action_count + 1 >= budget` for lose check and `budget - action_count - 1` for HUD. The engine increments `_action_count` in `_set_action` *before* `step()` runs, so inside `step()` the count already reflects this action. Fixed to `>= budget` and `budget - action_count`. Verified: 40-budget L1 with ACTION5 spam triggers GAME_OVER at action_count = 40.

## Smoke Test Results
End-to-end runtime smoke test (instantiate + run all three witnesses):
- L1 witness `[3, 3, 5, 3, 5, 3]` — score 0 → 1, level advances to L2. ✓
- L2 witness `[3, 3, 2, 2, 2, 2, 5, 3, 5, 3]` — score 1 → 2, level advances to L3. ✓
- L3 witness `[3, 3, 2, 2, 2, 2, 5, 3, 5, 3, 4, 5, 3, 3, 2, 2, 2, 2, 6@(32,20)]` — score 2 → 3, state = WIN. ✓
- Lose test: 45 ACTION5 presses on L1 (budget 40) → GAME_OVER at action_count=40. ✓
- Render test: all three levels render to a 64×64 frame using palette values within the spec's set; no exceptions. Distinct values per frame: {0, 4, 8, 9, 11, 15} (HUD bar + chain + tip + drop-zone visible).

## Notes
- File is 579 lines (within the 400-1500 expected range per the implement state).
- Magenta (6) base-anchor interior is mostly hidden under hinge_0 — visible only at corners. This is acceptable; the base reads as a small fixed marker at the chain origin even with partial coverage.
- Sprite collidability is uniformly `False` (interaction = INTANGIBLE). Click detection uses `ignore_collidable=True` and PIXEL_PERFECT blocking-mode pixel-non-(-1) check.

## Deliverables Produced
- `prior-games/nb6t/nb6t.py` (579 lines)
- `prior-games/nb6t/metadata.json`
- `implement-summary.md` (workspace/implement-summary.md)
