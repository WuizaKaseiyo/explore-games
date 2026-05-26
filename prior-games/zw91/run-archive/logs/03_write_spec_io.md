# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): chosen family, ID, distinguishing rules.
- skills/code/spec-template.md: 9-section template.
- skills/design-constraints/composition-and-tutorial.md: 3-level structure, +1-or-+2 rule.
- skills/design-constraints/difficulty-rules.md: per-level (a)/(b)/(c)/(d) bullets.
- skills/design-constraints/checklist.md: items 1–21.
- skills/design-constraints/forbidden-elements.md.
- skills/code/universal-scaffold.md.
- skills/code/novaengine-api.md.

## Deliverables Produced
- mechanic-spec.md: full 9-section spec with grid_size=(64,64) layouts, 22/12/17-action witnesses for L1/L2/L3, and per-level mechanic-necessity counterfactuals + difficulty justifications.

## Notes
- 4 mechanics across 3 levels: L1=2 (move + size-cycle), L2=3 (+inflate-push), L3=4 (+overload-burst). +1 each promotion.
- Avatar anchored top-left; growth extends right + down asymmetrically.
- Sockets are INTANGIBLE so they don't block movement / push-rolls.
- Breakaway-walls are collidable like normal walls until burst destroys them.
- Burst zone = footprint Chebyshev-distance-8 (= 2 tiles outward).
- `available_actions=[1,2,3,4,5]`. ACTION5 is the freedom slot — the modal verb for size-cycle/overload/burst.
- All 3 levels use grid_size=(64,64); no per-level resize needed; camera default=64x64 fits.
- HUD: single step-counter on row 0 (palette 9 → palette 0).
- Visual cues: which avatar variant is TANGIBLE = current size (rendered footprint is the cue). Overloaded state has an explicit `overload_halo` sprite.
- Witnesses are all sequences of ACTION1, ACTION2, ACTION4, ACTION5 (no ACTION3 LEFT — could add to budget but not necessary).
