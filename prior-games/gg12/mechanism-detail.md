# gg12 — constellation-lens-relay

## Summary

The board contains coloured star lenses connected by pale constellation
segments. Clicking a star rotates that star and every directly linked neighbour
one quarter-turn clockwise. The panel on the right shows the required final
lens orientation for each coloured star. The win condition is exact equality
between live lens orientations and the panel.

## Actions

- `ACTION6`: click a star lens. Empty space and the target panel are no-ops.

## Levels

- Level 1: three stars in a line; each endpoint also changes the centre.
- Level 2: four-star diamond with overlapping neighbour effects.
- Level 3: five-star loop with a chord, requiring reuse of earlier clicks.

## Win / Lose

Win when every live star points in the same direction as its matching target
icon on the right panel. Lose when the tight click budget reaches zero first.
