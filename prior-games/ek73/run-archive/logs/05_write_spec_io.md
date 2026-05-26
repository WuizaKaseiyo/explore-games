# Step #05: write_spec (revision pass 2)

## Inputs Consumed
- workspace/critique-revisions.md (from #04): 5 issues + lighter ones to address.
- workspace/mechanic-spec.md (v1): the prior spec under revision.
- skills/code/spec-template.md, skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules}.md, skills/code/novaengine-api.md (from prior steps).

## Deliverables Produced
- `workspace/mechanic-spec.md` (v2 — overwritten): change-log header at top tagging each change to a critique issue. Major changes: L1 layout redesigned to make wake load-bearing (issue 4); L2 layout simplified, wrong-path argument now rests on step-budget tightness (issue 2); L3 mechanic switched from sticky-pad to **paired warp pad**, with new T-junction layout where both clearer and warp are strictly counterfactually necessary (issues 1, 3); L2 spiral co-cell duplication removed (issue 5); sticky_pad and sticky_overlay sprites dropped, warp_pad sprite added (lighter issue).

## Notes
- The warp-pad pair mechanic for L3 distinguishes from zd7m's portals (zd7m has cohort-step with non-consumable portals; ek73 has single-avatar wake-trail with one-shot warp pair).
- Strict counterfactual necessity for L3 is now defensible: WITHOUT clearer the chimney-top-via-vertical-branch traps; WITHOUT warp the after-`(1, 8)`-collect dead-end traps. Both fail with soft-lock.
- L2's wrong-path defense remains thin (acknowledged in spec). Defense rests on step-budget tightness (35 with witness ~32).
- L1 had an in-spec redesign mid-section: the FINAL committed layout is the 2-wide horizontal corridor (rows 3-4) + vertical arm (column 3). The witness explicitly engages with wake on the post-`(12, 3)` row-4 return.
- This is write_spec visit #2 of an effective 10-pass cap.
