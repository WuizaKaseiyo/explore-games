# gg25 - docking-orbit-control

Spacecraft traffic-control puzzle. `ACTION5` advances every unheld spacecraft
one slot along its authored flight path and also advances moving raiders or
asteroids. Some hazards move every tick; others move every second tick.
`ACTION6` holds/releases the clicked spacecraft, or toggles a clicked transfer
beacon that diverts ships between paths. Ships must reach their matching dock
positions without entering asteroid or raider slots.

Level 1 teaches the docking hold on two large separated flight paths while
moving hazards patrol other parts of the loops. Level 2 adds a transfer beacon
that must be enabled so a ship bypasses an asteroid field and reaches its dock
while a second ship threads a moving lower patrol. Level 3 uses four separated
quadrant-style paths spread across the full 64x64 frame, with no shared path
points. The key timing step is explicit: the upper-left ship must be held for
one clock before transfer, otherwise it enters the upper-right path exactly as
a raider patrol reaches the arrival slot. A second transfer and a dock hold keep
the level layered without making the orbits visually tangled.

The visual identity is spacecraft traffic rather than abstract phase dials:
thin hand-authored flight paths, coloured ships with nose and wing pixels,
square docking cradles, irregular asteroid clusters, angular raider ships, and
active/inactive transfer beacons spread across the full 64x64 frame.
