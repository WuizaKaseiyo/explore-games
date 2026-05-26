# Mechanic pick

## ID
`rj5w`

Generated per `code/id-generation.md`: lowercase 4-char `r`+`j`+`5`+`w`,
not in the 25-game reserved list, not in `prior-games/index.md`'s
`game_id` column (incl. unindexed `fb7t`), not an English word, opaque.

## Mechanic family tag
`axis-fold-mirror`

## Mode (autonomous run)
No seed was provided. Family chosen autonomously after walking the
under-explored corners of the priors-cube and shipping the candidate
through both similarity checks.

## One-paragraph description
The playfield is a single rectangular sheet of "paper" with a thin
fold-line cursor stretched across it (vertical in L1; horizontal axis
joins in L2). Coloured **nub pawns** sit on the sheet and matching
**target rings** sit elsewhere on it; the player moves the fold-line
with arrows and presses ACTION5 to **commit a fold along the line —
the shorter half flips onto the longer half**. Every pawn on the
shorter half teleports to its position reflected through the
fold-line; pawns already on the longer half (or sitting exactly on
the line) stay put. Pawns whose reflected destination collides with a
wall stay put (the wall acts as an anchor); pawns whose reflected
destination is a **burn cell** are destroyed and trigger `lose()`.
The level is won when every nub pawn coincides with a same-colour
target ring. L1 introduces the single-axis fold and a clean
left-half-onto-right-half puzzle; L2 adds a perpendicular
(horizontal) fold-line that the player switches to via ACTION6 (click
a line to make it active) and forces a vertical→horizontal fold
sequence to align both row and column; L3 keeps both axes active and
adds **anchor walls** (block reflections of specific pawns) plus
**burn cells** (force ordering — fold the wrong way first and a pawn
dies on a burn) so the player has to plan a multi-fold sequence that
both routes around walls and dodges burns.

## Action subset
`[1, 2, 3, 4, 5, 6]`. ACTION1/2 move the active fold-line up/down (no-op
when the active line is vertical); ACTION3/4 move it left/right (no-op
when horizontal); ACTION5 commits the fold along the active line;
ACTION6 clicks on a fold-line cursor to make it the active one
(L2/L3 only — in L1 only the vertical line exists and ACTION6 is a
no-op). `_get_valid_actions` hides ACTION1/2/6 in L1 and prunes the
inactive-axis arrows in L2/L3 as needed.

## Core-knowledge prior coverage
- **Geometry & topology** (primary): reflection across a line, axis
  positioning. The win condition is purely geometric — every nub at
  the mirror image of its target.
- **Objectness** (primary): pawns and targets are persistent entities
  whose identity survives the fold; burn cells and walls are
  persistent obstacles.
- **Basic physics** (secondary): the fold is a discrete reflection
  transform — no momentum or gravity, but the "shorter half flips
  onto longer half" rule is the closest physical analogue to paper
  folding and reads as a plausible physical operation.

No agentness, no real-world clipart, no symbols, no letters, no
digits-as-glyphs.

## Novelty — positive similarity check (per `mechanic-novelty/similarity-check.md`)

### Taxonomy near-misses

| Reference | Family | Family-level match? | Description-level match? | Distinguishing rule |
|---|---|---|---|---|
| `ar25` | shape-mirror-cover | partial ("mirror" word overlap) | no | ar25 has STATIC reflector lines and the player slides pieces while the mirror passively duplicates them at reflected positions; the pieces exist simultaneously at real and mirrored positions. `rj5w` has a PLAYER-POSITIONED fold-line and a discrete commit verb that PERMANENTLY teleports pawns to their reflected positions; pawns never co-exist at both spots. |
| `m0r0` | mirror-orb-merge | partial ("mirror" word overlap) | no | m0r0 mirrors **input directions** continuously — every arrow press moves all four orbs simultaneously, each with sign-flipped axes — the mirror is in the *input transform*. `rj5w` mirrors **positions of pawns** discretely on commit, and the mirror axis is itself a movable cursor; the player's arrow presses move the axis, not the pawns. |
| `cn04` | nub-pair-glyph | no | no | cn04 is rotate+slide individual pieces to match boundary nubs; pieces move by single-cell arrows. `rj5w`'s pieces don't move via arrows at all; they only move when a fold commits. |
| `lp85` | row-col-shift-grid | no | no | lp85 shifts entire rows/columns one cell on a button-click (row stays a row, column stays a column). `rj5w` reflects pawns through an axis (a column's pawns end up at the mirrored column). Different transform group. |
| `vc33` | row-slide-pull-tab | no | no | vc33 slides every pawn in a row one cell on a tab-click. `rj5w` reflects across an axis. |
| `sk48` | paired-snake-trail | no | no | sk48 has two heads whose moves are mirrored continuously by a fixed axis. `rj5w` has many pawns whose reflection happens only on commit, with player-chosen axis position. |
| `tg6w` (prior) | settle-pile-tilt | no | no | tg6w tilts the playfield direction so blocks slide. `rj5w` reflects pawns across an axis on commit; no slide, no gravity. |
| `bx84` (prior) | beam-mirror-reflect | partial ("mirror" word overlap) | no | bx84 places mirrors at single cells that reflect a coloured beam. `rj5w` has no beam; the entire playfield reflects across a line. |

### Prior-games near-misses
Walked every row of `prior-games/index.md` (36 entries) plus the
unindexed `fb7t` (Phase-Transition Matter). No row's
(win condition × primary action × primary constraint) triple matches
`rj5w`'s. The closest by a single dimension are `bx84` and the
ones tabled above; each is distinguished above.

## Novelty — negative similarity check (per `mechanic-novelty/negative-similarity-check.md`)

For every relevant prior, ran the eight-dimension shared-features
walk. The mental L1 rendering: a pale (palette 1 off-white) sheet
of paper, ~50×50 of the 64×64 frame, with a single vertical
fold-line drawn as a 1-cell-wide stripe in palette 12 (orange) at
roughly column 32; two distinct nub-pawns on the left half (palette
14 green and palette 15 purple, each a richly-patterned 5×5 sprite
with an inner ring + crosshair), two matching target rings on the
right half (same colours, hollow squares with a subtle inner mark);
step-counter bar in palette 6 (magenta) along row 63.

The closest shared-features candidates and the dimensions they share:

- **vs `ar25`**: shares dim 6 (palette has reflective/mirror language only loosely; ar25's actual palette is darker). Shares dim 8 (reflection is a core dynamic, but ar25's static-mirror dynamic feels nothing like fold-and-flip). 1-2 shared dimensions, well under the threshold.
- **vs `m0r0`**: shares dim 8 partially (mirror motif). Visual signatures completely different (m0r0 is the dual-half black-on-yellow/orange split; `rj5w` is a single sheet with a single fold-line). 1 shared dimension.
- **vs `wa30` (sparse-pawns-on-empty-grid anti-pattern flagged in `negative-similarity-check.md`)**: dim 5 (cast — pawns + targets) and dim 7 (sprite grain) could overlap if pawns are 1×1 plain. **Mitigation**: pawns and targets are designed as 5×5 patterned sprites with internal structure (inner ring + cross), and the fold-line is the dominant visual feature, not the pawns. 0-1 shared dimensions after mitigation.
- **vs `kf42`/`vh68` cautionary tale**: those used `{4 wall, 8 red, 9 blue}` palette + small plain pawns. `rj5w` uses `{1 off-white background, 12 orange fold-axis, 14 green pawn A, 15 purple pawn B, 8 red burn cell, 4 wall, 6 magenta HUD}` — divergent dominant palette (off-white/orange vs grey/red/blue). 0 shared palette dimensions.

No prior overlaps on 3+ dimensions. Negative test passes.

## Open issues for `write_spec`
- Exact playfield logical-grid resolution: per checklist item 20,
  avoid a chunky upscaled small grid. Plan: full 64×64 cell grid;
  pawns and targets are 5×5 sprites with internal pattern; walls and
  burn cells are 4×4 patterned tiles.
- Fold-line cursor visual: thin coloured stripe across the entire
  sheet. Active vs inactive coloured differently in L2/L3.
- Anchor-wall semantics: a pawn whose mirror lands on a wall stays
  put. Spec must also clarify what happens if the mirror destination
  is **off the sheet** — convention: stays put.
- Step budgets: generous over the witness, never tight. Witness
  optimum is around 2-4 actions for L1, 6-9 for L2, 10-14 for L3;
  budget at ~3-4× witness per `difficulty-rules.md` § d.
