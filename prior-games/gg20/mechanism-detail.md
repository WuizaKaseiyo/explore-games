# gg20 — counterweight-beam-balance

Side-view torque mobile based on the revised `Counterweight-Beam-Balance`
idea. Click a tray stone, then a pan, to place weights on tilting beams.
Level 2 adds cascaded secondary beams; level 3 adds sliding stones.
`ACTION5` advances sliding-stone migration.

Stone colours encode different weights, with small pips marking the actual
weight on tray stones and larger pan stones. The visual mobile now uses
shorter beams, shallower pan ropes, and smaller pan spans so nested level-3
scales do not overlap. The visible pan direction follows the torque convention
directly: a heavier right pan drops right, and a heavier left pan drops left.
The right target panel is intentionally simple: each beam has a horizontal
left/center/right guide, and the highlighted mark sits on the side that should
be heavy. Level 3 now requires offset combinations rather than obvious
single-stone differences: the first two beams use `5` against `4` to achieve
a difference of `1`, the third beam still requires sliding-stone timing, and
the last beam uses a combined `4` against `2`. This produces
`[-1, +1, -2, +2]`. The win condition checks the actual weight differences on
each beam, so the level completes as soon as the displayed target differences
are achieved.
