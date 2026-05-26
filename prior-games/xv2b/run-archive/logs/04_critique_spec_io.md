# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (from #03)
- workspace/mechanic-pick.md (from #02)
- skills/design-constraints/checklist.md (re-read)
- skills/mechanic-novelty/* (re-read for re-validation)

## Deliverables Produced
- workspace/critique-pass.md: PASS verdict on all 22 checklist items + novelty re-validation. Verified witnesses by hand-trace at all three levels (L1=18 actions, L2=9, L3=29). Verified L3's pump strict-necessity by enumerating the spam-everything heuristic and the skip-drain alternate, both fail.

## Notes
- Hand-traced each level's witness to verify mechanics fire as planned and final state matches targets. All three witnesses converge.
- Snapshot semantics within an ACTION5 tick are critical — verified the spec's ordering (snapshot → queue valve+pump transfers → apply → drain consume) produces deterministic, replayable trajectories.
- Verified L1 trajectory is intricate (B oscillates near 5-7 mid-run) but converges to (8,8,8) at tick 16 by mass conservation.
