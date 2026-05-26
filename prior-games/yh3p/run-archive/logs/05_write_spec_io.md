# Step #05: write_spec (revision 1)

## Inputs Consumed
- workspace/critique-revisions.md (from #04): 5 issues, 2 blocking.
- workspace/mechanic-spec.md (from #03): the v1 spec being revised.
- skills/code/spec-template.md, skills/code/universal-scaffold.md.
- skills/design-constraints/* (all).

## Deliverables Produced
- workspace/mechanic-spec.md (overwritten): revision 2 of the spec, with all 4 critique issues addressed at the top of the document and section-by-section quote-for-quote remediation.

## Notes
- Issue 1 fix: deleted both contradictory wall layouts; replaced with single coherent description (vertical wall (8, 0..6), horizontal wall (0..6, 8), open gaps at (8, 7), (7, 8), (8, 8)). Witness routes verified against this layout.
- Issue 2 fix: bud_notched redesigned. Old design = 4×4 ring with one transparent side (read as C/U/n/⊃). New design = closed ring with a 2-pixel yellow stamen extending out one side; silhouette is "flower with tab", not letter-shaped.
- Issue 3 fix: §5 action mapping explicitly states M1 onto bud_closed auto-blooms but does NOT change tip activity (tip remains active, facing preserved). §4 L2 M2-necessity argument re-derived under this rule and remains valid (topology argument: gap at (8,15) becomes vine when first branch crosses, blocking second branch — still requires M2).
- Issue 4 fix: §4 L3 M2-necessity now leads with the dormancy argument (after each successful M3, tip is dormant; only ACTION6 re-activates; 3 buds → ≥2 M2 invocations regardless of walls). Topology argument retained as supporting evidence.
- Issue 5 soft fix: added optional `soil_texture` decorative sprite to §3, non-collidable INTANGIBLE background filling 64×64 with a sparse off-white speckle pattern. Provides visual density without introducing pseudo-mechanics.
- Mid-spec realisation: the question of "what does M1 onto bud_notched do?" was unaddressed in v1. Resolved in v2 by explicit rule: tip enters bud_notched cell freely, but M1 from there is BLOCKED until M3 succeeds or ACTION6 re-anchors. This makes M3 strictly necessary at L3 (otherwise the tip would just "walk through" notched buds without blooming them).
- Visit count for write_spec: 2 (entries #03, #05).
