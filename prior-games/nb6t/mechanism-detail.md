# nb6t — hinge-chain-reach

## Summary

A chain of three rectangular rod-segments is anchored at a fixed cell of the playfield. Each segment has an independent absolute heading (E / N / W / S) and an integer length (1..14); the chain's hinge positions and tip are derived by walking the chain from the base. The player selects an active hinge (cycle via ACTION5 or click via ACTION6) and rotates its segment 90° in either direction; from L2 onward the player can also extend or retract the active segment by 1 cell at a time. Win condition is *tip on target* (L1, L2) or *colour-matched object delivered to its drop-zone via carry-and-drop* (L3). Step-counter HUD at row 63 is the only lose trigger.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | EXTEND the active segment by +1 cell (max 14). | L2+, and L_active < 14, and resulting pose in-bounds. |
| ACTION2 | RETRACT the active segment by -1 cell (min 1). | L2+, and L_active > 1. |
| ACTION3 | Rotate the active segment 90° CCW (E→N→W→S→E). | always. |
| ACTION4 | Rotate the active segment 90° CW (E→S→W→N→E). | always. |
| ACTION5 | CYCLE the active hinge: `active = (active + 1) mod N_segments`. | always. |
| ACTION6 | CLICK at (x, y). On a hinge cell → set active to that hinge. On the tip cell while carrying → drop the carried object. Otherwise no-op. | always. |

(L1 gates ACTION1/2 out via `_get_valid_actions`. L2, L3 expose all six actions.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base system: cycle + rotate. | Tutorial. Tip must reach (4, 8) from base (16, 32). Witness `[ACTION3, ACTION3, ACTION5, ACTION3, ACTION5, ACTION3]` (length 6). Final pose `(W12, N12, N12)`. Available actions {3, 4, 5, 6}; step budget 40. |
| 2 | + segment-length-adjustment (one new mechanic). | Tip must reach (8, 8). Tip x = 8 is not a multiple of 12 from base x = 16; reachable only by retracting seg 0 from 12 to 8. Witness `[ACTION3, ACTION3, ACTION2, ACTION2, ACTION2, ACTION2, ACTION5, ACTION3, ACTION5, ACTION3]` (length 10). Final pose `(W8, N12, N12)`. Available actions {1..6}; step budget 100. |
| 3 | + carry-and-drop (one new mechanic). | Pickup object_red at (8, 8); deliver to drop_zone_red at (32, 20). Pickup-pose `(W8, N12, N12)` and drop-pose `(E4, N12, E12)` share NO segment (theta, length) values — the player must rotate seg 0 W→S→E (two CCW), retract seg 0 8→4, rotate seg 2 N→E, then click the tip. Witness `[ACTION3, ACTION3, ACTION2, ACTION2, ACTION2, ACTION2, ACTION5, ACTION3, ACTION5, ACTION3, ACTION4, ACTION5, ACTION3, ACTION3, ACTION2, ACTION2, ACTION2, ACTION2, ACTION6@(32,20)]` (length 19). Available actions {1..6}; step budget 100. |

## Win condition

`next_level()` fires when:
- (L1, L2) the chain's tip cell coincides with the level's `target_center` cell.
- (L3) the moveable `object_red` sprite is at `drop_zone_red_center` AND no object is currently carried.

The win check runs at the end of each `step()`, BEFORE pickup detection — so a click that drops the carried object onto the drop-zone wins immediately, without a re-pickup re-grabbing the just-dropped object.

## Lose condition

When `_action_count >= step_budget` for the current level, `lose()` fires. There is no other lose state: every rotation and length-change is reversible via the opposite action, so the player can never soft-lock.

## Internal state

- `_pose`: list of 3 `(theta, length)` tuples describing each segment.
- `_active_hinge`: int ∈ {0, 1, 2}.
- `_carrying`: Sprite reference (the picked-up object) or None.
- `_step_counter_ui`: HUD widget instance maintaining `(max_steps, current_steps)`.
- `_level_actions`: list of action ids valid at the current level (returned from `_get_valid_actions`).
- `_has_carry`: bool from `level.get_data("has_carry")`; gates the carry-and-drop branch.

## Notable code patterns

- **Forward-kinematics chain rendering**: `_hinge_positions()` walks the pose vector to compute every hinge position; `_render_chain()` rebuilds each segment sprite's pixel array from `(theta, length)` and repositions it. Reusable for any vector-sum polyline mechanic.
- **Pose validity gate**: `_pose_in_bounds()` enumerates every cell each segment would occupy (3-cell perpendicular width) and rejects any pose with an out-of-bounds cell. Rotations and length-adjusts wrap this gate so the action consumes a step counter unit but has no state effect on rejection.
- **Win-before-pickup ordering**: `step()` calls `_check_win → _check_pickup → _check_lose` in this order. Critical for the carry-and-drop mechanic — a drop on the drop-zone fires `next_level()` before the same tip-cell triggers a re-pickup of the just-dropped object.
- **Tag-based click dispatch**: hinges share the `sys_click` tag; the tip-marker also has `sys_click`. ACTION6 uses `level.get_sprite_at(gx, gy, tag="sys_click", ignore_collidable=True)` to find the topmost click-tagged sprite at the click cell, then dispatches by sprite name (`hinge_*` → set active; `tip_marker` → drop).
- **In-place pixel rebuilding**: each segment's `pixels` is reassigned to a freshly-built array per `(theta, length)` change, similar to s5i5's stretch-and-retract pattern but driven by the segment's heading rather than a stretch flag.
