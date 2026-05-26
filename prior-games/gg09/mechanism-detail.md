# gg09 — gear-mesh-spin

## Summary

The player clicks gears to rotate their marker tooth. Meshed neighbours rotate
in the opposite direction, and the alternation propagates through the mesh
graph. ACTION5 toggles a lock on the last-clicked gear; locked gears do not
rotate and stop propagation.

## Actions

- `ACTION6`: click a gear to rotate it and propagate counter-rotation.
- `ACTION5`: toggle lock on the most recently clicked gear.

## Levels

- Level 1: linear gear chain.
- Level 2: branched mesh whose target is generated from a sequence that locks
  the central gear before rotating the side branches.
- Level 3: larger mesh whose target is generated from multiple lock/clutch
  phases, forcing the player to isolate parts of the graph.

## Win / Lose

Win when every gear marker matches its socket direction. Lose when the step
bar reaches zero. The vertical side energy bar is tight enough that the player
must exploit mesh rotations instead of correcting gears independently.
