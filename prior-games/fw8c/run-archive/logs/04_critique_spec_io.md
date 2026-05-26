# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03): full 9-section spec for fw8c.
- skills/design-constraints/checklist.md (from study): 22 items.
- skills/design-constraints/composition-and-tutorial.md (from study).
- skills/design-constraints/difficulty-rules.md (from study): per-level (a)/(b)/(c)/(d) rules.
- skills/design-constraints/forbidden-elements.md (from study).
- skills/design-constraints/core-knowledge-priors.md (from study).
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md (from study).
- skills/mechanism-details/ls20.md, hr8q.md, tm5x.md, pk4m.md (re-read for spec-level novelty re-check).
- prior-games/index.md (66 entries).
- skills/global/action-enum.md (ACTION7 strict-undo rule, item 22).

## Deliverables Produced
- critique-revisions.md: 6 issues identified.
    - Issue 1 (item 12): L2 M3 post-consume reset is not strictly counterfactually necessary. Recommend dropping M3 from L2 (Option A).
    - Issue 2 (item 18(c)): L3 greedy heuristic doesn't fail (27 actions vs witness 29). Recommend introducing pigment-gated door as M3 (Option B).
    - Issue 3 (item 10): L3 composition is weak — M4 (triple-pigment) is just M2 at higher cardinality (the canonical anti-pattern of single-mechanic difficulty escalation).
    - Issue 4 (item 7 borderline): mixing table partially aligns with cultural color-mixing intuition. Recommend re-randomising.
    - Issue 5: spec quality — inline self-corrections (meta-narrative leftovers) in §4.
    - Issue 6: L3 wall-layout self-contradiction.

## Notes
- Verdict: REVISE. Transition back to write_spec for revision 2.
- The proposed Option B fix (pigment-gated door) is the highest-leverage change: it simultaneously addresses Issue 2 (greedy heuristic), Issue 3 (genuine composition), and dovetails with the spec's existing M3 hint that I'd already considered during write_spec but rejected for forcing-difficulty reasons.
- After revision, the post-revision mechanic enumeration should be: L1 = M1 (1 mechanic). L2 = M1 + M2 (2 mechanics, +1). L3 = M1 + M2 + M3-door (3 mechanics, +1). All within +1-or-+2 budget.
- Critique visit count: 1 of 10 maximum.
