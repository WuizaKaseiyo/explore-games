# Step #04: critique_spec (visit 1)

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec)
- skills/design-constraints/checklist.md (22 items)
- skills/design-constraints/forbidden-elements.md
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md
- prior-games/qm4t/mechanism-detail.md (for re-confirming distinguishing rule)

## Deliverables Produced
- critique-revisions.md: 6 issues numbered 1-6.
  - Issue 1: forbidden's X-pattern violates item 7 (cultural symbol).
  - Issue 2: L2's M4 necessity is broken — single big rectangle wins with 2 strikes < 3 (trivial fallback per item 12).
  - Issue 3: L3 inherits L2's trivial fallback.
  - Issue 4: avatar's eye-dot is borderline figurative; replace with symmetric ring.
  - Issue 5: pursuer's eyes/mouth pattern is figurative; replace with abstract checker.
  - Issue 6 (polish, not hard fail): add a post-closure flash animation for item 21 rule 3 compliance.

Verdict: REJECT — back to write_spec. Visit count after this transition: 2.

## Notes
- Items 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22: all PASS.
- Items 7, 12, 21: FAIL or polish-needed.
- Novelty check (similarity-check + negative-similarity-check) re-run on full spec: still NOVEL. The 2-of-8 dimension overlap with qm4t (level-asks + core-dynamic) is below the 3-of-8 threshold.
