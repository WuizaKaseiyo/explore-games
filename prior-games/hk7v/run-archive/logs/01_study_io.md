# Step #01: study

## Inputs Consumed
- skills/global/* (from harness): action enum, color legend, paths — read in full
- skills/conventions/* (from harness): from-tech-report, cross-cut-frequencies, reference-game-patterns — read in full
- skills/design-constraints/* (from harness): core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules — read in full
- skills/mechanic-novelty/* (from harness): taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format — read in full
- skills/mechanism-details/cn04.md — read for one near-comparable click-rotate mechanic
- prior-games/index.md — read in full (63 prior-game rows)
- game_sources_3_lvls/cn04/65d47d14/cn04.py — read in full (620 lines, click+arrow+rotate)
- game_sources_3_lvls/sp80/0ee2d095/sp80.py — partial (anchored sprite/level scaffold style)
- screenshots: cn04 level_1.png, sp80 level_1.png — for visual aesthetic anchor

## Deliverables Produced
- None (per state's transition condition; cached patterns file replaces per-run study-notes.md)

## Notes
- Prior corpus is dense (63 games). Major mechanic families saturated:
  walk+verb, click-place, click-toggle, rotate, mirror/fold, tilt/slide,
  cycle-attribute, pulse/wave, routing, stack/load, grow/spread, connect-edge.
- Design/visual conventions internalised: 64×64 grid, 16-color palette,
  step-counter HUD universal, tag-based sprite querying universal,
  ACTION5 = freedom-slot modal verb, ACTION7 strict undo or absent,
  L1=tutorial small/random-soluble, L2=+1-or-+2 mechanic with composition,
  L3=+1-or-+2 mechanic with full composition.
- Anti-patterns to avoid: low-resolution chunky-block aesthetic, repeated
  `{4 wall, 8 red, 9 blue}` palette, hidden mechanics, decorative-only
  mechanics that don't change witness, tight step budgets.
- Pixel-detail richness is mandatory (checklist 20). Sprites must have
  internal pattern, not just color-difference.

