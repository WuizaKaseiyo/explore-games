# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec): full 9-section spec
- skills/design-constraints/checklist.md: items 1-21
- skills/mechanic-novelty/similarity-check.md: positive procedure
- skills/mechanic-novelty/negative-similarity-check.md: 8-dim test
- prior-games/index.md (24 priors)
- skills/mechanism-details/{ka59,m0r0,tu93,cn04,kf42(prior),kn58,gx7m,zd7m}.md (prior referent files via mechanism-detail and the prior-games/<id>/mechanism-detail.md)

## Deliverables Produced
- critique-pass.md: All 21 checklist items marked ✅ PASS with notes; per-mechanic counterfactual table for items 11/12 (12 cells, all "no" with concrete blockers); independent enumeration of plausible alternate strategies per level (also all rejected by reference to specific cells/sprites/rules); novelty re-check vs full spec (taxonomy + prior-games + 8-dim negative-similarity walk against the four closest priors) — all NOVEL with concrete distinguishing rules.

## Notes
- Visit count to critique_spec for this run: 1 (well below the 10-cap).
- The critique was adversarial: I re-enumerated plausible alternate strategies for each level rather than only restating the witness's mechanic dependencies. For L3, the named "trivial heuristic that fails" (greedy without re-flipping pad-flipped pawns) was concretely walked through tick-by-tick to verify the heuristic does in fact deadlock.
- Visual detail floor (item 20): pawn sprites are 5×5 with internal half-fill carrying the polarity bit; flip-pads are 3×3 with internal checkered pattern. The grid is NOT all 1×1 flat-coloured cells. PASS.
- Sprite UI ≈ role (item 21): yang/yin are mirror-symmetric (top-half-fill vs bottom-half-fill) — natural "two opposite states" reading. Colour rings imply colour-correlated behaviour (matched by D mechanic). Flip-pads are visually distinct from pawns and walls. PASS.
- No drift detected: L2's colour-key + L3's flip-pads stay within the polarity-attract-discharge family without resembling any taxonomy or prior entry on 3+ negative-similarity dimensions.
- Verdict: PROCEED TO implement.
