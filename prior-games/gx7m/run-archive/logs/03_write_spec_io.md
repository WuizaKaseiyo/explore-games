# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): family `gear-mesh-cascade`, ID `gx7m`, palette plan.
- skills/code/spec-template.md (9-section template).
- skills/code/universal-scaffold.md (scaffold + style rules).
- skills/code/novaengine-api.md (API signatures).
- skills/design-constraints/{checklist.md, composition-and-tutorial.md, difficulty-rules.md, core-knowledge-priors.md, forbidden-elements.md} (all loaded in #01 study, applied here for §4 + §7-9).
- skills/mechanic-novelty/* (re-grounding §9).

## Deliverables Produced
- workspace/mechanic-spec.md — Full 9-section spec covering: title, mechanic-family, sprite roster (12 sprites + 1 HUD widget), 3 levels with mechanics + necessity-per-mechanic + witness solutions + difficulty justifications (a-d each), action mapping, HUD + per-game state, win predicate, lose predicate, and novelty re-grounding.

## Notes
- Per-level mechanic counts: L1 has 1 mechanic (cascade), L2 has 2 (cascade + ratchet), L3 has 3 (cascade + ratchet + clutch). Each promotion adds exactly 1 new mechanic and carries every earlier one forward — satisfies checklist item 11 (+1-or-+2 rule).
- Per-mechanic counterfactual necessity (item 12) explicitly worked through for L3: parity-coupling argument shows lblue=90° + orange=180° (both parity-0 in the chain) is unsolvable without disengaging the clutch.
- Witness lengths: L1=2, L2=5, L3=11. Step budgets 20/30/50 (generous, never shrink).
- Random-resistance: L2 ~1/16,800 per attempt (3/50k expected wins), L3 ~5.7e-10 per attempt (3e-5 expected wins). L3 firmly below 1/10000 threshold; L2 is borderline-pass per the formal §3.5 check.
- Open concerns to flag in critique: (i) L1's random-resistance is ~1/36 — explicitly tutorial-grade per `composition-and-tutorial.md` § Tutorial. (ii) L2 random-resistance is borderline (~3 wins per 50k random plays); could be tightened by making the witness longer or adding decoy gears, but the current 5-action witness is the cleanest mechanic-introduction. Decision: accept and articulate in critique.
- Aesthetic plan: 6×6 octagonal gear sprites with internal cog-tooth pattern (palettes 2 inner, 4 teeth, +mark colour), 10×10 hollow collar-ring with single coloured target indent. Distinctive palette signature {2,3,4,13} + {6,7,10,12,14} + {11,15} diverges from priors.
