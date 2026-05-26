# gg13 — chromatic-drip-labyrinth

Move a droplet with the arrow actions. The droplet paints every reachable cell
it enters. Pigment wells are consumed when entered and mix with the carried
colour. Coloured gates are hard movement constraints: the droplet can enter a
gate cell only while carrying that gate's colour.

The board is rendered as a scaled laboratory tile map with stone walls,
rounded paint pools, framed target wells, visible pigment wells, and framed
colour gates. Targets are not generic dots: the ring colour shows the paint
colour required at that exact cell.

Levels progress from one required gate, to a two-gate route with a second
conversion, to a three-conversion route where green, yellow, and purple gates
must be crossed in order. The action budget equals the intended route length,
so random wandering cannot eventually finish the level.
