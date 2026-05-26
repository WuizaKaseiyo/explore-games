# gg18 — pendulum-sync-rail

Side-view pendulum phase puzzle based on the revised `Pendulum-Sync-Rail`
idea. `ACTION6` pushes a visible bob one phase step forward through the swing
cycle; `ACTION5` ticks time. Level 2 adds rail coupling between adjacent
pendulums. Coupling can add a forward phase step when it pulls a neighbour
closer, but it never reverses the bob along its visible arc. Level 3 adds a
heavy bob plus a damper clip that can decouple one pendulum from the rail
segment.

The target strip at the bottom shows target phase pips and current phase pips
for every pendulum. Win when the live phase vector matches the target before
the exact action budget expires.
