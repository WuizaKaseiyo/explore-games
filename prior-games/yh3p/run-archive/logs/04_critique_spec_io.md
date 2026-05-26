# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (from #03): the full 9-section spec to review.
- workspace/mechanic-pick.md (from #02): mechanic family + ID + novelty notes.
- skills/design-constraints/checklist.md (items 1-22).
- skills/design-constraints/* (composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements).
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md, taxonomy-of-25-games.md.
- prior-games/index.md.

## Deliverables Produced
- workspace/critique-revisions.md: 5 issues — 2 blocking (Issue 1: inconsistent L3 wall layout; Issue 2: bud_notched as 4×4 ring with one open side reads as letter C/U/n/⊃), 2 minor improvements (Issue 3: tip activity after auto-bloom unspecified; Issue 4: simplify L3 M2 necessity using dormancy argument), 1 borderline soft suggestion (Issue 5: L1 visual sparseness — wa30 has similar). Other checklist items 1-22 all PASS. Novelty re-check NOVEL.

## Notes
- Critique-spec visit #1 of 10. Sending back to write_spec.
- Issue 2 is the key catch: the original bud_notched as a 4×4 ring with one transparent side renders as a horseshoe / C / U / n / ⊃ depending on rotation — all are letters, violating §3.4. Suggested fix: closed-ring flower with a yellow stamen extending out the intake side, so the silhouette is "flower-with-tab" not "broken ring".
- Issue 1 is a textual cleanup: the spec's iterative re-design of the L3 wall layout left two contradictory descriptions in the document. Fixing requires single coherent layout statement.
- Issue 4 is a robustness improvement: leading the L3 M2 necessity argument with the dormancy-after-bloom rule makes it independent of the wall topology, which makes the spec more obviously correct.
- All other checklist items pass cleanly — including the heavyweight item 12 enumeration, novelty checks, action-mapping concreteness, win/lose predicates, and per-level difficulty bullets.
