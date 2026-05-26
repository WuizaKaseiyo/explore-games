# Step #04: critique_spec (round 1)

## Inputs Consumed
- workspace/mechanic-spec.md (full spec from #03)
- workspace/mechanic-pick.md (novelty argument from #02)
- skills/design-constraints/{checklist, difficulty-rules, composition-and-tutorial, core-knowledge-priors, forbidden-elements}
- skills/mechanic-novelty/{similarity-check, negative-similarity-check, taxonomy-of-25-games, prior-games-index-format}
- skills/global/{action-enum, color-legend}

## Deliverables Produced
- workspace/critique-revisions.md: 6 issues identified.
  - Issues 1, 2, 3, 4: arithmetic inconsistencies in §4 — max-range value used inconsistently (32 vs 48 across levels), L2 wall clearance borderline under floor() rounding, L3 multi-target witness arithmetic doesn't cleanly demonstrate the asymmetric position binding, L1 doesn't require walking under the corrected max range.
  - Issue 5: §4's mid-narrative "REVISION:" notes obscure the final design — needs clean rewrite.
  - Issue 6: step budgets minor tweak for revised witness lengths.

Verdict: REJECT. Transition back to `write_spec` for round 2.

## Notes
- Structural items (1-10, 13-17, 19-22) all pass cleanly.
- Novelty (items 13-15) passes both positive similarity (taxonomy + prior-games) and negative-similarity dimensions.
- The CORE mechanic and design intent are sound; only the per-level geometric specifics need re-derivation with consistent max range and explicit floor()-rounding-safe margins.
- Critique computed all corrected arithmetic in critique-revisions.md so write_spec round 2 can incorporate the locked numbers directly without re-deriving.
