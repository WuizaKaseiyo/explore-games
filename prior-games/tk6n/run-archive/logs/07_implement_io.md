# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (revision 2)
- skills/code/universal-scaffold.md
- skills/code/novaengine-api.md
- prior reference: cn04, sp80, tr87 source

## Deliverables Produced
- prior-games/tk6n/tk6n.py (716 lines)
- prior-games/tk6n/metadata.json
- workspace/implement-summary.md

## Notes
- Initial L3 geometry placed avatar (16,32) and guard (14,32) so
  their footprints overlapped at level start; revised to avatar
  (6,32) and guard at (20,32) patrol cols 12..24, with throw_range=
  36 and step_budget=100. M3 (guard) is exercised because the
  boomerang's east-from-row-32-area path inevitably crosses guard's
  row range and triggers the freeze rule.
- Discovered API mismatch: novaengine `Sprite` exposes
  `is_collidable`, not `collidable`. Fixed.
- Boomerang launched from avatar's center cell `(avatar.x+1,
  avatar.y+1)` so the boomerang appears one row south-east of
  avatar's anchor; this places the boomerang's row at avatar.y+1
  which still overlaps target footprint (4×4 at row 32..35) when
  avatar at row 32.
- Guard freeze is implemented via sprite swap (guard ↔
  guard_frozen) with a `freeze_remaining` counter ticking down
  each step.
- ACTION5 has dual semantics (throw when held; pickup when
  dropped); `_get_valid_actions` removes ACTION5 from valid list
  while boomerang is in flight.
