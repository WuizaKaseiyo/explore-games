# gg05 — sandbar-river-block

## Summary

A boat follows directed river currents across a 64x64 river map. The river is
drawn as a wide bed, but internally the boat moves between current nodes. At a
junction it takes the first open current, and some first-choice branches lead
to red bad ports.

`ACTION6` drops a limited sandbar on a river or bank cell. Sand spreads one
cell in the four cardinal directions after each placement. A node is blocked
when spreading sand reaches it, so a dam placed on the next wrong tributary
actually closes that branch before the boat arrives.

The player must block bad tributaries before the boat reaches their junctions
without accidentally clicking a useful river cell and choking the route to the
green port.

## Levels

- Level 1: one wrong tributary branches upward from a broad straight river.
- Level 2: two wrong branches on an elbow river with rocks and wider banks.
- Level 3: three wrong branches on a longer zig-zag river, requiring earlier
  and more careful sand placement.

## Win / Lose

Win when the boat reaches the green destination port. Lose when the limited
sand budget is exhausted first.
