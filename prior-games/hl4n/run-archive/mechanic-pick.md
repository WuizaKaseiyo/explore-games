# Mechanic Pick

## ID
`hl4n`

ID generation per `code/id-generation.md`: 4 lowercase alphanumeric, not in the 25-reference list, not in `prior-games/index.md` (60 entries), not an English word. Verified non-colliding.

## Mechanic family tag
`row-col-tint-cross`

## Seed
None — autonomous run.

## One-paragraph description

A square grid of plain cells whose colors are entirely controlled by per-row and per-column "tint markers" sitting outside the playfield (one marker pinned to the left of every row, one pinned above every column). Clicking a row marker cycles that row's tint through a small palette and instantly recolors every cell in the row to that tint; clicking a column marker does the same for the column. A handful of cells inside the grid are "lock targets" — they have a thick outlined ring around them that flashes when the cell's current rendered color matches the lock's required color. The level wins when every lock target is satisfied. L1 only enables row-tint markers (column markers are inert decoration / absent), so the player learns "click left-edge marker → recolors row". L2 introduces column-tint markers that *override* row-tint per cell — once a column is non-background, every cell in that column shows the column tint instead of the row tint. L3 introduces a "bright-wins" blend rule: when both row and column have been set away from background, the cell shows the *brighter* of the two tints (palette-index higher → wins), so the player must coordinate row + column hues precisely so the desired color wins the brightness comparison. Step counter HUD; lose on counter exhaustion.

## Core knowledge priors used (per `design-constraints/core-knowledge-priors.md`)

- **Objectness** — markers, cells, lock targets are persistent entities; clicks recolor through stable references.
- **Basic geometry & topology** — row/column membership is the load-bearing geometric concept; the player reasons about which row + column intersect at each lock target.

No physics, no agentness — this is a static-recoloring puzzle.

## Action set
ACTION6 only. (Pure click game; the markers are clickable, the playfield is inert.) — Per `action-enum.md`'s subset patterns: `[6]` is a well-attested pure-click family (r11l, vc33, sc25, ft09, lp85). No undo (no ACTION7), no movement.

## Similarity check (per `mechanic-novelty/similarity-check.md`)

### Against the 25-reference taxonomy
The family tag `row-col-tint-cross` shares the `row-col` / `column-…-row` prefix with three reference entries; per the family-level check, all three escalate to description-level review:

- **lp85 — `row-col-shift-grid`**: clicked button physically *shifts* an entire row or column by one cell (Rubik-style permutation of token positions). My candidate does NOT move tokens; it recolors entire rows/columns in place. Win condition for lp85 is positional alignment of distinct-shape tokens; mine is color alignment of stationary cells. Concrete distinguishing rule: **tokens move in lp85, tokens are stationary and only their fill changes in mine**. (Read `mechanism-details/lp85.md`: button click triggers a hard-coded permutation of cell positions; mine triggers a uniform recolor of one row's pixels.)
- **vc33 — `row-column-swap-stripe`**: clicking a marker triggers an in-row/in-column swap of two stone groups across the marker. Again, vc33 *moves* stones; mine recolors stationary cells. Distinguishing rule: **vc33's click triggers a positional swap; mine triggers a hue change with no positional effect**.
- **qx7p (taxonomy adjacency, but qx7p is in `prior-games/index.md` not the taxonomy)**: covered below.

No other taxonomy entry matches at the description level. ft09 (`stamp-3x3-paint`) recolors cells, but it stamps a 3×3 region around a clicked cell, not an entire row/column.

### Against `prior-games/index.md` (60 entries)
The family-level check flags entries whose tags share `row-col`, `column`, or `tint`/`paint`/`recolor` semantics. After review:

- **qx7p — `column-shift-row-align`** (closest prior): "vertical colour-band columns slid past a horizontal scan line to match a target row colour pattern". qx7p's primary action is *sliding* whole columns past a fixed scan line; cells move physically. Mine: cells are stationary; only their fill is set by a row+column tint pair. **Distinguishing rule: qx7p shifts color-bands; mine cycles per-row and per-column tint values, leaving cell positions fixed.**
- **xn5p — `chamber-stamp-partition`**: pawn walks chamber and stamps walls to partition a region into per-color subregions. Both end up rendering colored regions, but the verb is different — xn5p uses *walking + wall stamping*; mine uses *clicking row/column markers*. xn5p has a movable pawn; mine has no pawn. **Distinguishing rule: xn5p's player walks and stamps walls; mine's player clicks edge markers and never moves an avatar.**
- **gv47 — `seed-grow-surround-dissolve`**: click colored seeds to *grow* regions over time. gv47 is dynamic / temporal (regions expand each tick); mine is instantaneous (click → instantly recolor). **Distinguishing rule: gv47 has time-based region growth; mine has no time component, recoloring is single-step.**
- **ft09 — taxonomy entry, redundancy with above**: stamp 3×3, single-cell hub. Already addressed.
- **mz6t — `majority-vote-stabilize`**: click cycles 3 colour states; ACTION5 ticks majority-vote. mz6t has a time-tick rule; mine has no temporal component. **Distinguishing rule: mz6t cycles per-cell and uses majority-vote propagation; mine cycles per-row/column with no propagation.**
- **vd3g — `valley-dig-roll`** & **kp9z — `grain-accumulate-topple`**: terrain / grain mechanics, fundamentally different (gravity-based). No overlap.
- **wq3m — `current-drift-route`** & **rk7x — `live-switch-routing`**: routing/conveyor mechanics, fundamentally different (items move on a flow). No overlap.
- **qf8m — `rook-cross-toggle`**: click a tile to flip a (2N-1)-cell row+col cross. **Closest prior on the row+column axis**. qf8m flips a single cross per click (the clicked cell's entire row + entire column toggle their bit-state). Mine: clicking a row marker affects ONLY that row, not the column; the *intersection* of two clicks is what's interesting in my candidate (each cell sees row-hue ∨ column-hue under the L3 blend rule), whereas qf8m couples row+column unconditionally. **Distinguishing rule: qf8m's click flips a coupled row+column cross of a fixed cell; mine's row marker affects only one row, column marker only one column, and the row/column interaction (override → blend across L1/L2/L3) is the load-bearing learnable mechanic — not a fixed coupling.**

No prior has the row-tint + column-tint + per-cell-blend composition.

## Negative similarity check (per `mechanic-novelty/negative-similarity-check.md`)

Walking the 8 dimensions against the closest priors (qx7p, lp85, vc33, qf8m, xn5p):

| Dim | qx7p | lp85 | vc33 | qf8m | xn5p |
|---|---|---|---|---|---|
| 1. What's on the board | grid of color-bands + scan line | grid of named cells + buttons | striped stones + rails + markers | grid of 3-state cells | maze + walking pawn + walls |
| 2. Player physically does | clicks tile to slide column | clicks button to permute | clicks marker to swap | clicks tile to flip cross | walks + stamps walls |
| 3. Level asks for | row pattern matched | tokens on goal cells | stones over color slots | pattern stable under mod-N | per-color subregions |
| 4. Kills player | step budget | step budget | step budget | step budget | step budget |
| 5. Cast | bands + rails + scan line | cells + buttons | stones + markers + rails | tri-state tiles | walls + pawn + colored regions |
| 6. Visual signature | vertical bands | grid of named pieces | striped layout + flanking rails | uniform tri-state grid | walking pawn in maze |
| 7. Pixel grain | flat-color band cells | small named pieces | thin stripes | flat tri-state cells | mixed |
| 8. Core dynamic | sliding bands match | permutation puzzle | swap puzzle | row+col coupled flip | wall-partition |

Mine: 1. plain colored grid + edge-pinned tint markers + lock-target rings; 2. clicks edge markers (no in-grid clicks, no walking); 3. lock targets must show their required color; 4. step budget; 5. cells + edge markers + lock-target rings; 6. plain interior + decorated edge strip + thick outline rings; 7. internal pixel-pattern in markers (small concentric triangles per palette index) and rings; 8. row+column hue cycling with override-then-blend rule across levels.

Sharing-count summary:
- vs qx7p: shares (1 weak — both have a colored grid; 4; 5 weak). 2 dimensions, OK.
- vs lp85: shares (4; 5 weak). 1-2 dimensions, OK.
- vs vc33: shares (4; 5 weak). 1-2 dimensions, OK.
- vs qf8m: shares (1 — grid; 4; 5 — flat cells). 3 dimensions — borderline. **But the core dynamic (8) is fundamentally different**: qf8m's coupled row+column flip is one click changing 2N-1 cells in a + shape; mine's separate row + column tint markers with override/blend means a click changes ONE row OR ONE column. A player would not perceive these as the same game.
- vs xn5p: shares (4). 1 dimension, OK.

No prior shares ≥ 3 dimensions in a way that includes the core-dynamic axis (8). Negative test passes.

## Action palette + camera + resources (open questions from `reference-game-patterns.md`)

- **Action palette**: pure click `[6]`. No movement, no ACTION5 (every distinctive verb lives in *which* marker is clicked, not in modal slots). No undo.
- **Camera**: fixed 64×64. Logical playfield will be 32×32 (interior 8×8 of 4-px cells), with a 16-px wide column at the left for row-markers and a 16-px tall row at the top for column-markers, and the remaining 16-px right strip for the step counter HUD. **NOT** the small-grid + auto-scale anti-pattern from `cross-cut-frequencies.md` — design at full 64×64.
- **Resources beyond step counter**: just step counter. No accumulating progress dot needed (the lock-target rings serve that role visually).
- **Core-knowledge prior pairing**: objectness + basic geometry/topology. Underrepresented in the corpus among non-motion mechanics — most Nova games lean on physics or agentness; this one is a pure logic+visual puzzle.
