# critique-revisions.md — second pass (v2)

Adversarial review of `mechanic-spec.md` v2 against the
checklist. The 4 v1 issues are all addressed. **One new issue
caught** during the verify-by-enumeration pass on item 12 at L3.

## Issue 5 — L3 M3 (selective subset choice) bypassable
**Violation:** strict counterfactual necessity for M3 at L3
(checklist item 12).

**Offending section:** Spec v2 §4 / Level 3 / "Necessity per
mechanic / M3":
> "L3 cannot be solved without triggering M3, because the
> level has 2 maroons placed at `(8, 32)` and `(58, 32)` ..."

**Why it fails:** with only 2 maroons and 3 patrollers, an
"all-encompassing pen committed on phase 4..7" captures 2
maroons (2 strikes) + 0 patrollers (correctly excluded by M4
timing) + 5 required-colour critters (tally clears). 2 strikes
is below the 3-strike lose threshold; the player wins L3
*without* triggering M3. M4 alone suffices. Per item 12 verify-
by-enumeration: this alternate strategy is plausible (requires
no greater-than-witness skill), so M3 is not strictly necessary
at L3.

**Concrete fix:** add a 3rd maroon at L3 — for example at
`(32, 4)` (top of playfield, between the cluster and the top
edge). Then a big pen (e.g. `(0,0)-(63,0)-(32,63)`) captures 3
maroons (3 strikes → `lose()`); a small witness pen still
excludes the 3rd maroon (the witness pen `(10,10)-(56,12)-
(38,56)-(8,56)` has top edge at y ≈ 10..12 in the relevant x
range, so `(32, 4)` is at y=4 < 10 — outside the pen). M3 is
restored as strictly necessary.

Update §3 sprite-roster mention if needed (no — the roster
already lists `critter_maroon` generically). Update §4 / L3
"Sprite layout" line for `critter_maroon` from "× 2 at
`(8, 32)`, `(58, 32)`" to "× 3 at `(8, 32)`, `(58, 32)`,
`(32, 4)`". Update §4 / L3 "Necessity per mechanic / M3" to
mention the 3rd maroon and the trivial-fallback strike count.
Verify witness pen still excludes the 3rd maroon at `(32, 4)`.

## All other items pass

- Items 1–6, 8–11, 13–21: pass on v2.
- Item 7 (forbidden glyphs): all sprites are abstract (vertical
  bar, rounded blob, tapered diamond, hollow square, filled
  square). Pass.
- Item 12 (counterfactual necessity): pass at L1 (M1, M2) and
  L2 (M1, M2, M3) — verified by enumeration. Fix Issue 5 to
  pass L3.
- Items 13–15 (novelty): the spec's distinguishing rules
  against gv47, xn5p, ng52, kn58, pz4t, su15, ar25, r11l are
  concrete (each names a structural property of qm4t that the
  prior lacks). Pass.
- Negative-similarity walk against the closest 3 priors gives
  ≤ 2 shared dimensions — below the 3-dimension reject
  threshold. Pass.

## Verdict
Spec v2 fails one checklist item (12 at L3). Transition back to
`write_spec` for revision pass v3 — small targeted fix only.
