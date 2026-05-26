# gg17 — fuse-burn-ignite

`ACTION6` clicks ignition pads to start burning neighbouring fuse cells, bridge
nodes to unblock fuse segments, and scissor nodes to cut selected shortcuts.
Invalid in-grid clicks spend budget, so the player cannot freely probe the map.
`ACTION5` advances the burn frontier one graph step. Bombs record the tick at
which adjacent fire reaches them, and the level wins only when all bombs fire
inside the level's synchronisation window.

Level 1 is a staggered two-fuse timing puzzle with one blocked bridge on the
long path. Level 2 adds a branching fuse network with three bridge gates, so
the correct opening and ignition order is required under a tight budget. Level
3 is stricter than level 2: all three pads are required, four bridges must be
opened, and the left fuse has a shortcut that must be cut before ignition. The
left pad starts one tick before the right and bottom pads so all three bombs
fire on the same turn.

The right-edge energy bar and bottom fire chevrons show remaining budget and
the order of bomb firings.
