# Step #04: critique_spec (visit 1)

## Inputs Consumed
- mechanic-spec.md (from #03): full 9-section spec.
- skills/design-constraints/checklist.md: 21-item compliance checklist.
- skills/design-constraints/difficulty-rules.md: critique check § 3 (a-e per level).
- skills/design-constraints/composition-and-tutorial.md: mechanic inheritance + +1-or-+2 rule.
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md: re-run on full spec.

## Deliverables Produced
- critique-revisions.md: 3 substantive issues (M3 walls hidden; L3 layout inconsistent; L3 heuristic-fail weak), 2 sanity issues, 2 clarifications. Items 1-10, 13-21 pass. Novelty stands.

## Notes
- Visit count of `critique_spec`: 1 (per state log). Revision cap 10 — plenty of headroom.
- The biggest concern is M3 (walls) at L3 — passive constraint that the witness avoids by construction, never actively triggers. Solution: replace with `multi-edge` (parallel edge support) — an active mechanic the witness must execute. This also avoids the spec's wall-rasterisation precision concern (no need to compute Bresenham line / wall intersection) — the multi-edge mechanic is purely combinatorial.
- Spec novelty at L3 actually IMPROVES under the multi-edge proposal — multi-graph mechanics aren't represented in the existing taxonomy or prior-games corpus.