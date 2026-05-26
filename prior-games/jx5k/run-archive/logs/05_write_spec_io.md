# Step #05: write_spec (revision after critique visit #1)

## Inputs Consumed
- mechanic-spec.md (from #03, prior version): the spec being revised.
- critique-revisions.md (from #04): 3 substantive issues + 2 sanity + 2 clarifications.
- skills/code/spec-template.md (re-read), skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements}.md.

## Deliverables Produced
- mechanic-spec.md (revised): full rewrite with:
  - §3 sprite roster: collapsed `pip_required` into pip-slot positioning (per critique Issue 6); added per-pair multiplicity to `edge_strand_<pair>_<k>` (Issue 7); removed `wall_brick` (no longer needed since M3 changed).
  - §4 Level 3: rewritten end-to-end. Replaces M3 (walls) with **M3 = multi-edge / 3-state cycle** per Issue 1. New L3 layout: 4 nodes at cardinal positions, target degrees `[4, 2, 4, 2]`, witness uses exactly one double-edge (n0–n2). Concrete heuristic-fail argument: "double every edge" overshoots one endpoint and forces correction actions (Issue 3 resolved). Single concrete layout (Issue 2 resolved).
  - §5: per-level valid-action gating made explicit (Issue 4).
  - §9: added a 5th near-miss (`qb84 bead-lift-swap`) for completeness.

## Notes
- Verified L3's witness is unique by combinatorial argument: target degrees `[4, 2, 4, 2]` with 4 nodes and `max_edge_multiplicity = 2` admits exactly one valid graph — the doubled pair must be the one with both endpoints at target degree 4 (= n0–n2). Any other doubled pair overshoots a degree-2 node.
- L1 step budget = 30, L2 = 50, L3 = 50 — generous (3.75×, 2.5×, 3.1× witness respectively). Per `difficulty-rules.md` § 2d, generous budgets are required and budgets do not shrink across levels.
- Re-checked all 21 checklist items against revised spec; all PASS now (item 12 strict counterfactual passes because M3 is an active verb that is required for n0=4).
- Re-ran novelty: positive `similarity-check.md` (no family + description match) + negative `negative-similarity-check.md` (no 3+ dimension overlap). Multi-graph mechanics absent from the entire 25-game taxonomy + 36-prior-games corpus.