# gg26 - sheep-pasture-fence

Pasture enclosure puzzle on a 16x16 logical grid rendered across the full 64x64
canvas. `ACTION6` clicks a square to place a fence, or clicks an existing fence
to pick it up again. Each click spends one retry energy. The level also has a
hard fence budget, shown as fence pips in the HUD.

The sheep moves conceptually by four-direction reachability only. Stones, water,
and placed fences block movement; diagonals do not connect. After every click,
the game flood-fills from the sheep. If that reachable grass region touches the
board edge, the sheep can escape and the pasture is not valid. If the region is
closed and its square count meets the level target, the enclosed grass changes
colour for a short confirmation animation before the game advances.

There are three tuned levels. Level 1 teaches a compact jagged brook paddock:
three required gaps, a 42-square target, and a 46-square witness pasture. Level
2 uses a larger zigzag stream boundary with four required gaps and internal
rocks; its 72-square target sits below a 77-square witness pasture. Level 3 is
the grand hollow: an edge-hugging, non-rectangular natural barrier with six
required gaps, a 122-square target, and a 129-square witness pasture. Each level
has one spare fence and enough retry energy for several add/remove experiments,
but omitting any witness gap leaves an escape path to the board edge.

The visual identity is a grassland map: varied grass, water, stones, wood
fences, a friendly sheep sprite, a bottom HUD for fence budget/retry energy/area
target, and an enclosed-area colour change. Comments in the renderer mark where
to add richer pasture dressing and a more detailed sheep animation later.
