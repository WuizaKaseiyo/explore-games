# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (from #03): the full 9-section spec under review.
- workspace/mechanic-pick.md (from #02): novelty grounding.
- skills/design-constraints/checklist.md (the 18-item checklist).
- skills/design-constraints/{composition-and-tutorial.md, difficulty-rules.md, core-knowledge-priors.md, forbidden-elements.md}.
- skills/mechanic-novelty/{similarity-check.md, negative-similarity-check.md, taxonomy-of-25-games.md}.
- prior-games/index.md (re-checked for any post-pick novelty drift).

## Deliverables Produced
- workspace/critique-pass.md — Per-checklist-item verdict (all 18 ✅), per-mechanic counterfactual-necessity table (item 12, 6 rows across L1/L2/L3), novelty + negative-similarity re-run, item-18 difficulty table, common-failure-mode sweep, final verdict NOVEL + PASS.

## Notes
- One non-blocking implementation note flagged for the `implement` state: `_get_valid_actions` should enumerate the standard 256-cell ACTION6 grid (per `r11l` convention) rather than the spec's "≤ 7 click cells per level" wording. Random-resistance arithmetic in critique-pass.md assumes the 256-cell enumeration, which yields ~1e-13 per attempt for L2 and ~1e-25 for L3 — both far below the 1/10,000 threshold.
- Adversarial walk produced no rejection-triggering issues. The borderline concern was L2's first-action enumeration being just 4 specific cells if the agent sees a small action set — resolved by following the standard 256-cell enumeration.
- L2's witness count: 5 (the spec text earlier said 6 then revised down to 5; the per-mechanic necessity table is consistent with 5 actions: tang + R-hub + 3×pink. The witness narrative in spec §4 L2 walks this out correctly.)
- Decision: TRANSITION TO IMPLEMENT (not write_spec). The spec passes all 18 checklist items, novelty, and negative-similarity. State_log will record this as visit #1 to critique_spec; revision cap (10) untouched.
