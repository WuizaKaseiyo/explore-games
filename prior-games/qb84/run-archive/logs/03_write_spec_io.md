# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): family `bead-lift-swap`,
  ID `qb84`, action-space [1,2,3,4], 3-level composition arc draft,
  palette commitment, sticky-peg + pair-peg mechanics outlined,
  named trivial heuristic that L3 defeats.
- skills/code/spec-template.md: 9-section structure.
- skills/code/universal-scaffold.md: file structure and camera-
  viewport rule (we'll use full 64×64 so no resize needed).
- skills/code/novaengine-api.md: Sprite, Level, Camera, NovaBaseGame
  signatures.
- skills/design-constraints/{checklist,composition-and-tutorial,
  forbidden-elements,core-knowledge-priors}.md: §3.4 binding rules
  (3 levels, +1 mechanic per promotion, witness exercises every
  mechanic, no symbols/text, prior categories used).
- skills/global/{action-enum,color-legend,paths}.md.

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec.
  - L1 = 8-action witness, 24-step budget, 6-bead S-curve.
  - L2 = 12-action witness, 32-step budget, 8-bead zigzag, sticky pegs.
  - L3 = 14-action witness, 60-step budget, 10-bead double-S, pair pegs +
    sticky-trap (`pg_l3_g`).
  - Mechanic counts: L1 = N=2 (lift, drop); L2 = N+1=3 (+sticky); L3 =
    N+2=4 (+pair-propagation). Cursor stepping treated as constant verb
    primitive (not counted).
  - Adjacent commute failure for L3 named: actions 8 (lift on B5) and 9
    (cursor 5→6).
  - Trivial heuristic L3 defeats: "for each bead at wrong colour, find
    a peg of target colour next to it and lift/drop" — fails because
    B6's target 15 has no directly-reachable colour-15 plain peg.
  - All sprite names opaque; palette commitment locked.

## Notes
- Caught a pair-peg rule inconsistency mid-write — initial L3 witness had
  B5 swap producing same-colour no-op; redesigned B5 initial colour and
  target so propagation does useful work. Explicit rule retained:
  pair-peg propagation copies the OTHER pair peg's colour (as of action
  start) into the cursor's chain neighbour, NEVER overwrites a locked
  bead, NEVER consumes an extra step.
- Treated cursor stepping (ACTION3/4) as a constant verb primitive
  rather than a counted mechanic. This is a judgement call; flagged for
  critique_spec to scrutinise (item 10a wording: "let N ≥ 1 be the count
  of mechanics required by L1's witness"). If critique decides cursor
  stepping is a counted mechanic, the level structure must shift to
  N=3/4/5 or the mechanics must merge.

