# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic).
- workspace/study-notes.md (from #01 study).
- skills/code/{spec-template, universal-scaffold, novaengine-api, id-generation}.md.
- skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements}.md.
- skills/global/{action-enum, color-legend, paths}.md.

## Deliverables Produced
- workspace/mechanic-spec.md: 9-section spec for gv47, with sprite roster (10 sprites + paint_cell runtime), 3 levels each with witness, mechanic enumeration M1/M2/M3, full §6 internal state and mix-rule semantics, §7/§8 testable predicates, novelty note vs ft09/dc22/lq5x.

## Notes
- Refined family from `seed-grow-shrink` to `seed-grow-mix` after realising strict necessity for "retract" was hard to construct; mix-at-frontier gives clean strict-necessity for L2's green target and L3's purple target. Updated mechanic-pick.md to match.
- L3 layout went through one self-revision in the spec (replacing the yellow target with a green-target at (10,10) plus a red target inside the pre-mix red region) so the witness's mix events do not erase any single-colour target. Captured the revision inline in §4.
- Action subset chosen as [5, 6] — minimal verb space (mix + click). Avoids adding arrow-key motion that none of the priors' play uses with this style.
- Step budgets: L1=30, L2=50, L3=80 (monotone increasing per `difficulty-rules.md` § d L3 addendum). Witness lengths 11 / 12 / 26 — every level is 2.5–4× generous.
EOF
