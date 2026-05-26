# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): chosen mechanic family, ID, novelty notes
- skills/code/spec-template.md: 9-section template
- skills/code/{universal-scaffold, novaengine-api, id-generation}.md: implementation grounding
- skills/design-constraints/{composition-and-tutorial, difficulty-rules, checklist, core-knowledge-priors, forbidden-elements}.md: re-consulted for §4 per-level structure and §5 action mapping
- skills/global/{action-enum, color-legend}.md: action subset rationale, palette choices

## Deliverables Produced
- workspace/mechanic-spec.md: 9-section spec covering Title, Mechanic family, Sprite roster, Level progression (3 levels with mechanics-required, necessity-per-mechanic, witness, difficulty justification per level), Action mapping, HUD/state, Win condition, Lose condition, Novelty note.

## Notes
- Per-level mechanic counts: L1=1 (BINARY), L2=2 (BINARY+LONG), L3=3 (BINARY+LONG+SHIFT-G). +1 each level — within the +1-or-+2 rule.
- The blocker is treated as a SPATIAL CONSTRAINT, not a player-exercised mechanic. It is necessary for the counterfactual necessity argument of LONG at L2 (without the blocker, a binary-only path (c1=0,c2=0,c3=1,c4=1) wins, defeating LONG necessity) and similarly load-bearing at L3.
- Action subset chosen: `[6]` only. ACTION7 is omitted entirely per `action-enum.md`'s strict-undo rule (this game has no meaningful undo). Click-only fits the corpus pattern (ft09, lp85, r11l, vc33, sc25 also use [6] only).
- Native 64×64 grid_size; no upscaling. Strand columns at x=17/33/49 with 3-pixel-wide strands. Crossings 19×7 sprites between adjacent strand pairs; long crossing 35×7 spanning all three.
- Witness for each level is 2 clicks. Step budget 30/24/22 — generous over 2 in all cases (15×, 12×, 11×).
