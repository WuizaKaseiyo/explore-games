# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (from #03)
- workspace/mechanic-pick.md (from #02)
- skills/design-constraints/checklist.md: 22 items reviewed
- skills/design-constraints/difficulty-rules.md: § Critique check
- skills/mechanic-novelty/{similarity-check, negative-similarity-check}.md: re-run on the full spec
- L1 screenshots (vc33, lp85, jx5k) viewed in #02 — visual-signature comparison still holds for the fleshed-out spec

## Deliverables Produced
- workspace/critique-pass.md: per-item ✅/PASS markers for items 1-22 + novelty verdict NOVEL.

## Notes
- Verified counterfactual necessity (item 12) by enumerating all 16 (L2) and 32 (L3) toggle states. L2 has 2 valid winning configs (1,1,0,0) and (0,1,1,0), both witnesses use BINARY+LONG; the third candidate (0,0,1,1) is blocked by `blocker_yellow` at (col=1, y=36). L3 has 4 valid winning configs ((1,1,0,0,0), (0,1,1,0,0), (0,1,0,0,1), (1,1,1,0,1)) — all use BINARY+LONG+SHIFT-G; binary-only paths fail because slot 0 demands G which only SHIFT-G produces and routing constraints prevent the right strand-pairings.
- Random-resistance argument for L2 leans on absorbing-loss states (blocker hits) + step budget cap. Acknowledge: random win probability is "low but not vanishingly small" — the harness criterion is "non-trivial reason a random agent fails", which is met.
- ACTION7 strict-undo rule (item 22): confirmed absent from `available_actions=[6]`. No risk of overload.
- Visit count to critique_spec: 1 (this is the first entry). Cap is 10. Plenty of headroom if needed for revisions.
