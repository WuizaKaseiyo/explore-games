# Step #04: critique_spec (visit 1/10)

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec)
- skills/design-constraints/checklist.md (items 1-22)
- skills/design-constraints/difficulty-rules.md (per-level a/b/c/d/e bullets)
- skills/mechanic-novelty/{similarity-check, negative-similarity-check}.md
- skills/mechanism-details/cn04.md (closest taxonomy near-miss)
- prior-games/index.md

## Deliverables Produced
- critique-revisions.md: numbered issue list, primarily flagging in-spec dead-end
  derivations in the L3 section that need to be cleaned up before the spec is
  reviewable end-to-end.

## Notes
- L3 section contains an aborted constraint-solve and a "REVISION OF BASE TABLE"
  marker followed by a second pass; readers cannot tell which numbers are the
  final ones. The witness coordinate-set was rewritten three times in-line.
- L1 / L2 sections look clean and internally consistent.
- The lock mechanic's strict-counterfactual argument (item 12) is presence-based;
  needs a sharper formulation since simply "leave the would-be-lock untouched"
  could replicate the lock's effect for the same witness.
- The novelty argument is solid (mechanic-pick.md verified; no near-misses
  introduced by the spec's flesh-out).
- Transitioning back to write_spec for a single targeted rewrite of the L3
  section.
