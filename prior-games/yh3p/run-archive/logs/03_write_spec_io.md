# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): mechanic family `vine-branch-bloom`, ID `yh3p`, action subset, novelty notes.
- skills/code/spec-template.md: 9-section spec layout.
- skills/code/universal-scaffold.md: file structure + camera viewport rule + style rules + common patterns.
- skills/code/novaengine-api.md: API signatures.
- skills/design-constraints/*.md (composition-and-tutorial, difficulty-rules, checklist, core-knowledge-priors, forbidden-elements).
- skills/global/*.md.

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec. Sections include sprite roster (root, stalk, tip_active, tip_dormant, bud_closed, bud_notched, bloom, wall + step_bar HUD), 3-level progression with per-level mechanics enumeration (L1=1, L2=2, L3=3), per-mechanic counterfactual necessity table, written-out witness solutions per level (L1: 12 actions, L2: 22 actions, L3: 40 actions), action mapping for [1,2,3,4,5,6], HUD description, win/lose predicates, and novelty notes vs taxonomy and prior-games index.

## Notes
- Grid dimensions chosen as 64×64 with cell-stride=4 (wa30 idiom): real pixel-level rendering, no engine upscaling, sprites have rich internal pattern (root is 8×8 with maroon-rim-red-mid-green-core; stalks are 4×4 with green field + maroon centre; tips are 4×4 yellow-eye teardrops; buds are 4×4 ring-with-or-without-notch; walls are 4×4 crosshatch). Avoids the "low-resolution chunky upscale" anti-pattern (checklist item 20).
- Mechanic inheritance: L1=1 (extend-tip), L2=2 (+click-rebranch), L3=3 (+directional-bloom-commit). No level introduces zero new mechanics; no level introduces ≥3 new mechanics. Every L1 mechanic carries forward.
- L1/L2 use `bud_closed` (no notch, auto-blooms on contact). L3 uses `bud_notched` (requires ACTION5 with facing-match). This means ACTION5 is functionally inert in L1/L2 but the spec doesn't *require* it as a mechanic at those levels; the player simply hasn't met a notched bud yet. Per checklist item 11 a mechanic exposed but never used in a level is "hidden in the weak sense" — but ACTION5 is genuinely new at L3, not pre-existing-and-untriggered. The spec language must be careful here; flagging this for critique to validate.
- L3 layout was iterated mid-spec to ensure (a) the L-shape walls actually have a unique 1-cell crossing per quadrant pair (so the counterfactual-necessity argument for click-to-rebranch holds), and (b) bud notch directions are arranged so that the most-direct path arrives at one bud (R) with the WRONG facing — making the trivial heuristic explicitly fail.
- L3 witness contains the exact action sequence: 19 actions for branch 1 (root → bud P), 10 for branch 2 (re-anchor → bud Q), 11 for branch 3 (re-anchor → bud R). 40 total within 100-step budget.
- Novelty note recapitulates the mechanic-pick.md analysis with concrete distinguishing rules; explicitly notes that prior-games/index.md is non-empty (66 entries).
