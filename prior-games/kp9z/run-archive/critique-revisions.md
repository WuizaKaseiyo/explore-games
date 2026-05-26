# Critique revisions — round 1

## Summary
Spec passes 19 of 20 checklist items + novelty checks. One issue requires
revision before transitioning to `implement`.

## Issue 1 (checklist item 20 — shape-as-meaning)

**Violation**: section 3 (sprite roster) and section 4 (per-level cell
type assignments). The cell-type sprites (`cell_template_source`,
`cell_template_sink`, `cell_template_target_n`, `cell_template_redir_*`,
`cell_template_regular`) currently differ ONLY by the colour of the 2×2
type-center fill (palette 6 / 9 / 13 / 12 / 2). Their shape is
identical: each is a uniform 2×2 colored block at the cell's center,
inside a 6×6 frame.

Per checklist item 20:
> Colour alone is not enough: a level full of 4×4 blocks where the only
> difference between "type A" and "type B" is that A is red and B is
> blue tells the player nothing about what A or B are, what they do, or
> how they should be reasoned about. ... If a critique review cannot
> describe each sprite type's role from the spec's pixel-matrix alone,
> without reference to colour, the spec fails.

Stripping colour from the spec's current cell-type sprite designs:
- regular vs source vs sink: indistinguishable (all show the same 2×2
  filled center inside the same 6×6 frame).
- target: has 4 corner pips visible — distinguishable by *shape* (pip
  presence) from the rest.
- redirector: has frame-edge notch (orange) — distinguishable by *shape*
  from the rest.

So target/redirector shape-distinguish; regular/source/sink do not.

### Concrete fix suggestion

Move from a 6×6 sprite layout with a 2×2 type center to an 8×8 sprite
layout, and give each cell type a *distinct interior shape pattern* (not
just a different colour fill). Specifically:

- **Regular cell** — interior all backdrop (no inner shape). 8×8 = frame
  border only.
- **Source cell** — interior 2×2 center filled (palette 6 magenta) PLUS
  a 1-pixel-wide "stub" extending up from the center to the inner top
  edge. Shape: a "T" with the stem pointing up. Without colour the
  reviewer sees a clear T-shape — visually distinct from a uniform
  filled center.
- **Sink cell** — interior 2×2 center filled (palette 9 blue) with one
  diagonal corner pixel SET TO BACKDROP. Shape: a "3-pixel L" (one
  corner missing from the 2×2). Without colour the reviewer sees an
  L-shape with a hole — visually distinct from source's solid T-shape.
- **Target cell** — already shape-distinct via 4 corner pips (the
  green target pips at the 4 inner corners of the 8×8). Plus a 2×2
  filled center (palette 13 maroon). Optional extension: 1-pixel "ring"
  one ring around the center to disambiguate from sources. Without
  colour the reviewer sees a 2×2 center plus 4 corner dots — distinct
  shape.
- **Redirector_south cell** — 2×2 filled center (palette 12 orange)
  PLUS a 2-pixel orange "exit notch" embedded in the SOUTH frame edge
  of the 8×8 sprite (replacing 2 of the 8 frame pixels at row 7 cols 3–4
  with palette 12 instead of palette 4). Without colour the reviewer
  sees a 2×2 center + asymmetric break in the frame's bottom edge —
  distinct shape that also unambiguously names the exit direction
  *positionally* (not via an arrow glyph).

Update §3 sprite-roster pixel matrices accordingly. Update §4 to
reference the new sprite templates.

This also addresses a related concern: the previous redirector design
(asymmetric pixels INSIDE the 2×2 type indicator to encode N/S/E/W
direction) borderline-resembled an arrow glyph (item 7 — forbidden
elements). The frame-notch encoding moves the directional cue from
inside-the-cell to on-the-frame-edge, which is unambiguously
positional and not arrow-like.

## Issue 2 (no other issues — preventive notes only)

The critique passes everything else. Notes for the revision pass to
preserve:

- §4 strict counterfactual necessity tables for L1/L2/L3 are correct;
  the per-mechanic rows already enumerate alternate strategies and name
  the specific cells/sprites blocking each alternate. Do not lose this
  detail in the rewrite.
- Witness coordinate calculations (e.g. L3 source A at sprite anchor
  (1+6, 1+6) → mid-cell click ≈ (10, 10)) need to be RECOMPUTED for the
  8×8 sprite. New stride is 8 (sprite size 8) with 0 gap (frame edges
  abut), so for an N×N board total game-cells = 8N. L1 4×4: 32
  game-cells, fits exactly in 32×32 grid (anchor 0,0). L2/L3 5×5: 40
  game-cells, doesn't fit in 32×32 grid → bump grid to (40, 40) or use
  spacing logic. RECOMMENDED: use grid_size=(40, 40) for all 3 levels;
  L1's 4×4 board occupies the centre 32×32 of the 40×40 grid (anchor 4,
  4); L2/L3 occupy the full 40×40 (anchor 0, 0). Camera scale =
  64 // 40 = 1×, and the 8×8 sprite renders 8×8 onscreen pixels per
  cell. Sub-cell pool test: each pip 1 sprite-pixel = 1 onscreen pixel
  → after 2×2 pool merges with neighbours; this MIGHT lose pip detail.
  
  ALTERNATIVE: use grid_size=(40, 40) and camera scale 1× and INCREASE
  pip size from 1 sprite-pixel to 2 sprite-pixels (2×2 each). Then pip
  = 2×2 onscreen → 1 pooled pixel. Survives. Re-check sprite layout
  with bigger pips:
  ```
  Col:    0 1 2 3 4 5 6 7
  Row 0:  F F F F F F F F
  Row 1:  F t t c c t t F   -- 2×2 target / 2×2 current / 2×2 target
  Row 2:  F t t c c t t F
  Row 3:  F c c Z Z c c F
  Row 4:  F c c Z Z c c F
  Row 5:  F t t c c t t F
  Row 6:  F t t c c t t F
  Row 7:  F F F F F F F F
  ```
  Each pip is 2×2; type center 2×2; layout is dense but 8×8 still
  fits all elements.
  
  Refine: with 2×2 pips, max distinguishable counts is 4 (4 pip slots).
  My target_counts ≤ 1 in actual levels, so 1 pip slot used. Current
  counts 0..3, so 3 pip slots used (one slot reserved for transient
  topple = 4 grains). 4 slots is enough.

- Continue using the strict win predicate ("every cell at exact target
  count, including 0 for non-targets"). It's central to making sink
  and redirector counterfactually necessary.

- ACTION6-only `available_actions=[6]` is correct. Do not add other
  actions during the revision.

## Verdict
Spec needs revision: fix issue 1 (shape-as-meaning per item 20). Once
fixed, the spec is expected to pass critique on the next pass.
