# Implement summary

## Files written

- `prior-games/kj82/kj82.py` — 730 lines.
- `prior-games/kj82/metadata.json`.

## Plain-English rule summary

The player controls a small pawn that walks one cell per arrow on
top of long pinned planks. Clicking a plank selects it; the modal
verb pivots the active plank around its anchor end, sweeping its
free tip across a quarter-arc and carrying the pawn with it. Posts
toggle between solid and hollow on click — a solid post blocks
plank rotations whose arc would pass through it. A pad on a plank
fires the pawn a fixed distance along the plank's axis when the
pawn ends a turn standing on it. The player's goal is to reach the
destination tile before the energy bar drains.

## Implementation notes

- Sprite bank holds 9 base sprites (planks of 2 lengths,
  anchor_fixture, anchor_halo, pawn, goal_tile, post_blocking,
  post_permeable, spring); each level clones the relevant ones at
  level-build time.
- Plank rotation handled by mutating `sprite.pixels` (np.rot90)
  and `sprite.set_position` per orientation; cells per orientation
  computed by direct rotation of east-frame body offsets.
- Pawn-carry computed via the same CW rotation transform applied
  to the pawn's offset from the anchor.
- Post toggle uses the universal-scaffold "two-sprite swap"
  pattern (swap `InteractionMode.TANGIBLE` ↔ `REMOVED` between
  co-positioned blocking/permeable variants).
- Spring is registered as a child of its plank; the spring sprite
  follows the plank during rotation, and the launch direction is
  read from the plank's current orientation at fire time.
- Step counter HUD is a 32-cell yellow-on-black bar at the bottom
  row, modeled on cn04's `qdcvayjdkm`.
- All 3 witness sequences (L1: 6 actions; L2: 23 actions; L3:
  18 actions) verified end-to-end — final state == WIN, score
  == 3 (one point per level).

## Smoke verification

```
$ python -c "import ast; ast.parse(open('...kj82.py').read())"
parse OK

$ python -c "from kj82 import Kj82; g = Kj82(); print(len(g._levels))"
3

$ python <witness replay script>
==== L1 ==== score=1 state=NOT_FINISHED pawn=(8, 6)   [advanced to L2]
==== L2 ==== score=2 state=NOT_FINISHED pawn=(8, 8)   [advanced to L3]
==== L3 ==== score=3 state=WIN pawn=(16, 20)
```
