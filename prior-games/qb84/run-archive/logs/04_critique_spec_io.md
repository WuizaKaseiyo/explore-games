# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec): full 9-section spec.
- skills/design-constraints/checklist.md: 16 items + 10a.
- skills/mechanic-novelty/{similarity,negative-similarity}-check.md.
- skills/design-constraints/composition-and-tutorial.md.
- workspace/mechanic-pick.md (from #02): for cross-reference of
  novelty claims and palette commitment.
- prior-games/{kf42,qz73,kx14}/mechanism-detail.md: for novelty
  re-validation against priors at full-spec depth.
- skills/mechanism-details/{tr87,vc33,lp85,ls20,sb26}.md: for
  taxonomy near-miss re-validation.
- workspace/logs/state_log.md: visit-count check (this is visit #1
  to critique_spec — well under cap of 5).

## Deliverables Produced
- workspace/critique-pass.md: all 16 + 10a items pass; novelty PASS
  at full-spec depth; negative-similarity PASS (no prior shares ≥3
  dimensions). Transitioning to `implement`.

## Notes
- Borderline judgement on item 10a: cursor stepping (ACTION3/4) treated
  as constant verb primitive across all 3 levels rather than a counted
  mechanic. Defended by analogy to ls20 (WASD movement is the navigation
  primitive; counted mechanics are the cycler interactions). If a future
  audit overturns this, the spec's L1 N-count would shift to 3 and L2/L3
  to 4/5, breaking item 10a's strict +1 rule. Flagged as a known
  judgement call.
- L3 adjacent commute failure validated by manual trace: swapping
  witness actions 8 and 9 → pair propagation fires at cursor=6 (B6
  directly), pushes yellow into B7, breaks B7's target.
- Full-spec re-check vs tr87 confirmed: serpentine chain + small
  corner target ref + dark-bg/magenta-yellow-green-purple palette
  keep visual signature divergent from tr87's grey/cyan/pink tape
  display.

