# Critique revisions — visit 1

Two issues found. Both must be fixed before transitioning to
`implement`.

## Issue 1 — `spring_east` chevron may read as an arrow glyph (item 7 / `forbidden-elements.md`)

- **Checklist item violated:** item 7 (no cultural conventions /
  no arrow glyphs implying direction). Per
  `forbidden-elements.md`: "Cultural conventions: ... an arrow
  shape implying direction."
- **Offending spec section:** §3 sprite roster, the
  `spring_east` row, which describes "green chevron pointing
  east".
- **Why this matters:** a green chevron `>` is exactly the visual
  the report flags as cultural — it relies on the
  acquired-knowledge association "chevron points in the
  launch direction". The forbidden-elements gate is hard, not
  soft.
- **Concrete fix:** redesign the spring sprite so its visual
  cannot read as an arrow:
  - New visual: 3×3 cells, palette 14 (green) ring around
    palette 0 (white) inner pip, with palette 5 (black) corner
    pixels — symmetric in all four directions, NO directional
    bias.
  - Move the launch-direction information INTO the M4 mechanic
    rule itself: the spring inherits its launch direction from
    the orientation of the plank it currently sits on. So a
    spring on a plank oriented east launches the pawn east; a
    spring on a plank oriented south launches south, etc. The
    plank's anchor-end-vs-tip-end visual already encodes
    direction, and that is acceptable (the anchor is a fixed
    fixture at one end of the plank — readable as "this side
    is pinned"; the tip is "the free side").
  - Update §3, §5 (action mapping if relevant), §4 L3
    description, and the §4 L3 counterfactual for M4 to reflect
    this revised mechanic and visual.

## Issue 2 — grid sizes 16×16 and 18×18 fail item 20 (low-resolution rendering)

- **Checklist item violated:** item 20 ("don't generate a
  low-resolution game"). The item explicitly names 12×12, 14×14,
  16×16 as too-small grids that render as chunky uniform-colour
  blocks.
- **Offending spec section:** §4 — L1 and L2 declare grid_size
  16×16; L3 declares 18×18. At scale = 64/16 = 4, every grid
  cell renders as a 4×4 uniform-colour block (16 display pixels
  of one palette value). At 64/18 ≈ 3.55, similar.
- **Why this matters:** the rendered frame would be coarse
  4-pixel blocks tiling the screen, exactly the anti-pattern
  item 20 describes. Even if the spec's PIXEL-CELL pattern is
  rich at the cell level, the cell IS the pixel unit at scale 4.
- **Concrete fix:** bump every level's grid_size to 32×32 (scale
  = 64/32 = 2 — each grid cell renders as 2×2 display pixels) or
  larger. Plank length and other coordinates need rescaling.
  Suggested approach:
  - L1 grid 32×32; plank length 8 (anchor + 7 body cells).
  - L2 grid 32×32; plank lengths 13.
  - L3 grid 32×32; plank lengths 13 and 8; spring at length-8
    plank's east tip; goal 5 cells east of spring.
  - Step budgets stay generous: 30 / 50 / 60 still work.
  - All counterfactual enumerations remain valid under the
    rescaled coords (post in path of rotation arc, spring needed
    to reach goal off-plank, etc.).
  - Make the plank visually richer at the per-cell level: each
    plank renders as 2 cells thick × N cells long (instead of 1
    × N), so at scale 2 each plank renders as 4 display pixels
    thick × 2N display pixels long — clearly reading as a
    "wooden plank" not a "single-pixel line". Internal pattern:
    top row palette 12 (orange), bottom row palette 13 (maroon).
  - The pawn (3×3 cells), goal (4×4), post (3×3), and spring
    (3×3) are all multi-cell sprites with internal pattern, so
    they pass item 20 naturally at the per-cell render scale of
    2.

## Items confirmed PASSING (no revision needed)

- 1 palette range — only values 0..15 plus -1.
- 2 universal scaffold — spec's structure matches.
- 3 available_actions subset — `[1, 2, 3, 4, 5, 6]`.
- 4 exactly 3 levels — L1, L2, L3.
- 5 4-char ID, opaque, no collision — `kj82` confirmed.
- 6 core priors — objectness + geometry/topology + physics.
- 8 ≥ 2 mechanics — 4 mechanics across the game.
- 9 L1 tutorial — single plank, no posts/springs, no hazards,
  random-stumbleable per spec.
- 10 L2/L3 compose — every prior mechanic carries forward.
- 11 +1-or-+2 inheritance — N=2 → 3 (+1) → 4 (+1).
- 12 strict counterfactual necessity — per-mechanic per-level
  table + alternate-strategy enumeration.
- 13 mechanic absent from taxonomy — distinguishing rules vs
  cn04, ar25.
- 14 mechanic absent from priors — distinguishing rules vs
  pz4t, bx84, wt39, pj7k, xn5p.
- 15 distinguishing rules concrete.
- 16 win condition — pawn-on-goal predicate.
- 17 lose condition — step-budget exhaustion.
- 18 difficulty floor and ceiling — (a)(b)(c)(d) per level
  with concrete random-resistance, ~2 min human time, decision
  space + plausible-wrong + witness reasoning chain (L2),
  trivial heuristic + divergence (L3), step budgets 30/50/60.
- 19 no hidden state — visual cues for active-plank
  (anchor_halo overlay), post state (two-sprite-swap),
  pawn position, step budget.
- 21 design UI to teach — the plank + anchor visual reads as
  "long board with one pinned end"; post reads as a solid
  obstacle-or-toggle; pawn is small and clearly the only
  movable agent. After fix 1, spring sprite reads as a "special
  pad" that the pawn lands on; after fix 2, the rendering is
  detailful at scale 2.

## Novelty re-check (post-fix anticipation)

After Issue 1 fix (spring inherits direction from underlying
plank), the mechanic remains distinct from every taxonomy and
prior entry. The spring's "direction-from-plank" rule does not
overlap with any prior's mechanic — bx84 has a beam from a
fixed emitter; lq5x has a lantern cone with a separate rotation
verb; vp6h has shadows; sp80 has flow-routing; kj82's spring is
a one-shot pawn-launcher whose direction reads off the underlying
rotated plank. No new similarity drift introduced.

After Issue 2 fix (32×32 grid), no novelty implications — grid
size is purely a rendering concern, not a mechanic concern.
