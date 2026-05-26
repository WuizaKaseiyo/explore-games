# tb4k — implement summary

## Files
- `prior-games/tb4k/tb4k.py` (390 lines)
- `prior-games/tb4k/metadata.json`

## Mechanic in plain English
A small rectangular brick tumbles end-over-end on a tiled floor under
cardinal arrow input. It has three footprint states (standing,
lying-horizontal, lying-vertical) that alternate deterministically
with each move. Some floor cells are hazardous and destroy the brick
if any part of its footprint overlaps them; later levels add narrow
corridors flanked by hazards where the brick's footprint orientation
matters. The brick must come to rest in the standing state exactly
on the goal cell.

## Runtime smoke test results
- Instantiation: ✅ (`Tb4k()` constructed cleanly).
- L1 witness (8 × ACTION4 + 8 × ACTION2): ✅ — brick reached
  standing (11, 11), engine fired `next_level()`, advanced to L2.
- L2 witness (4E + 2N + 4E + 2S + 4E): ✅ — brick reached
  standing (14, 4), advanced to L3, lives stayed at 3 (witness
  avoids holes).
- L3 witness (2N + 4E + 4E + 2N + 2E): ✅ — brick reached
  standing (12, 1) on L3.
- Hole-death path: ✅ — driving the brick onto standing (8, 4)
  hole at L2 decremented lives from 3 → 2 and respawned the brick
  at the start cell (2, 4).
