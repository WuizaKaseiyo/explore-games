# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic): game ID `kj82`, mechanic family `plank-pivot-walk`, similarity rules
- skills/code/spec-template.md (from #01): the 9-section structure
- skills/design-constraints/composition-and-tutorial.md (from #01): exactly-3-levels rules
- skills/design-constraints/difficulty-rules.md (from #01): per-level (a)(b)(c)(d) bullets
- skills/design-constraints/checklist.md (from #01): items 11, 12, 18, 19, 20, 21
- skills/code/universal-scaffold.md (from #01): scaffold + style rules
- skills/code/novaengine-api.md (from #01): API reference
- skills/code/id-generation.md (from #01): ID rules

## Deliverables Produced
- mechanic-spec.md: 9-section spec. L1=2 mechanics, L2=3 (+post-toggle), L3=4 (+spring-launch). All carried-forward at each level; per-mechanic counterfactuals + alternate-strategy enumerations included for items 11/12.

## Notes
- Iterated through ~5 candidate L3 mechanics before settling on spring-launch. Walked-locks (rotate-fails-if-pawn-stepped-on) was attractive but failed item 12's "no trivial fallback" check because winning sequences can avoid triggering the fail event by planning ahead. Spring-launch is a positive verb that strictly cannot be replaced by any other mechanic in the spec's L3 layout.
- Designed pivot-with-carry as part of M2 (rather than as a separate L2-introduced mechanic) because the rule is universal across levels. L1's witness exercises pivot-carry too — pawn starts off-anchor at L1 so the carrying behaviour is observable from the very first pivot.
- L3's grid is 18×18 (vs. 16×16 for L1/L2) to give the spring its 5-cell launch range room.
- Step budgets: 30 / 50 / 60 — non-shrinking across levels per `difficulty-rules.md` § 2 (d).
- Spec emphasises the visual cues for state surfacing (anchor_halo overlay, two-sprite-swap for posts) per checklist item 19 — no behavioural state hidden behind pixel-mutation (per `reference-game-patterns.md`'s tu93 anti-pattern callout).

## Revision pass 2 (entered from critique_spec visit 1)
- Spring sprite redesigned to symmetric green-ring-with-pip (no directional bias). Launch direction inherited from underlying plank's orientation; spring is registered as child sprite of its plank.
- Grid sizes bumped from 16/16/18 to 32/32/32 throughout. Camera scale = 2 (each grid cell = 2×2 display pixels). Plank thickness raised from 1 cell to 2 cells (4 pixels at display).
- All coordinates rescaled. Post locations, plank lengths, witness sequences updated. Step budgets unchanged (30/50/60).
- Per-mechanic counterfactuals re-derived under new layout. Plank_gamma west/north rotations off-grid; plank_delta west off-grid (north on-grid but doesn't cover goal). Spring east-launch is unique path to goal — verified by per-orientation enumeration.

