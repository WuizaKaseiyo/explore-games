# Step #05: write_spec (visit 2 — revision after critique)

## Inputs Consumed
- mechanic-spec.md (existing draft from #03)
- critique-revisions.md (from #04 critique_spec): 3 numbered issues
- skills/code/spec-template.md (target structure)
- skills/design-constraints/{checklist, difficulty-rules, composition-and-tutorial}.md

## Deliverables Produced
- mechanic-spec.md (revised): rewrote §4 Level 3 from scratch with one final
  base-assignment table, one constraint-propagation derivation, one verified
  internal-boundary check (12 of 12), one witness, and a single counterfactual
  table; sharpened §4 Level 2's locked-tile counterfactual argument from the
  incorrect 4-fold-uniform-rotation claim to a defensible visual-cue + search-
  space-collapse argument; replaced the bogus uniform-k refutation in §4 L2's
  alternate-strategies block with the correct one.

## Sections changed
- §4 Level 2 — Necessity per mechanic (locked-tile bullet): rewritten.
- §4 Level 2 — Verification by enumeration table (locked-tile row): rewritten.
- §4 Level 2 — Plausible alternate strategies (uniform-k bullet): rewritten.
- §4 Level 3 — entire subsection (Layout through Difficulty justification):
  rewritten.

Sections UNCHANGED: §1, §2, §3, §4 Level 1, §4 Level 2 (other than the two
items above), §5, §6, §7, §8, §9.

## Quoted critique-revisions.md issues each change addresses
- Issue 1 ("L3 contains in-line dead-end derivations"): addressed by fully
  rewriting §4 Level 3.
- Issue 2 ("L3 final witness coordinates rewritten three times"): addressed by
  the same rewrite — only one witness now appears, with concrete display-pixel
  coordinates per tile-centre.
- Issue 3 ("Lock mechanic's strict-counterfactual argument is presence-based
  and weak"): addressed by the §4 Level 2 sharpening: the lock's distinguishing
  behaviour is reframed as the visual glyph + win-predicate evaluation, with
  search-space-collapse as the load-bearing role.

## Notes
- L3 witness length = 8 (was indeterminate in the previous draft).
- L3 step budget held at 50 (~6× witness — generous, per L3 rule).
- The L3 base-assignment table was constructed from scratch via constraint
  propagation: lock → 4 cardinal neighbours (each requires R = 1 from R_init =
  0, so each = 1 click) → 2 outer-corner regulars (cascade, each = 1 click) →
  linked pair joint constraint (R_link = 2 unique, so 2 clicks on either
  member). Total 6 + 2 = 8 clicks.
- Verified all 12 internal edges align in the final state.
