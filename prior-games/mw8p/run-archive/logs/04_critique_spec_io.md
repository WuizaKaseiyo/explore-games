# Step #04: critique_spec

## Inputs Consumed
- `workspace/mechanic-spec.md` (from #03): the 9-section spec.
- `workspace/mechanic-pick.md` (from #02): the novelty argument.
- `skills/design-constraints/checklist.md`: 22-item gate.
- `skills/design-constraints/composition-and-tutorial.md`: mechanic
  inheritance rule.
- `skills/design-constraints/difficulty-rules.md`: per-level
  bullet a/b/c/d.
- `skills/mechanic-novelty/{similarity,negative-similarity}-check.md`:
  re-grounded against the full spec.

## Deliverables Produced
- `critique-pass.md`: 22-item PASS table, per-mechanic
  counterfactual table with concrete blocking-cell justifications
  for L1/L2/L3, alternate-strategy enumeration per level, full
  8-dimension negative-similarity walk vs zk9p showing 4 LOW-weight
  shared dimensions (D1/2/4/5) and 4 divergent (D3/6/7/8 — including
  all 3 principle dimensions).

## Notes
- Adversarial walk did not surface any item failing. The L2 alternate-
  strategy enumeration confirms DOWN-first loses without firing M2,
  forcing RIGHT-first as the unique short witness. The L3 enumeration
  confirms M3 must fire on turn 1 (only legal first move is onto C₁).
- M1's "strict counterfactual necessity" reading: interpreted as
  "M1's pursuit rule fires unconditionally every turn — every winning
  sequence triggers M1 ≥ N times where N = action count". This is
  the only viable interpretation since same-cell lose is a
  passive constraint (it shapes legal moves but doesn't fire on a
  winning sequence). The critique accepts this reading because the
  alternative (requiring M1's lose branch to actually fire) would
  make every chase-style game definitionally non-compliant, which
  contradicts the existence of `ka59`, `zk9p`, `nf3z`, etc. in the
  reference set.
- Visit count for critique_spec state: 1 (this entry). Well under
  the cap of 10.
- Transition condition met: all checklist items pass + novelty
  returns NOVEL → next state is `implement`.
