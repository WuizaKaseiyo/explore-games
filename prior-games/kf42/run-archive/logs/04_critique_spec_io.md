# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec): 9-section spec.
- skills/design-constraints/checklist.md: 16 binary checks.
- skills/design-constraints/{forbidden-elements,composition-and-tutorial,core-knowledge-priors}.md: re-grounding for adversarial review.
- skills/mechanic-novelty/{similarity-check,taxonomy-of-25-games}.md: full-spec novelty re-run.
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md: structural verification (action set, ID format).
- deep-analysis-3lvls/{m0r0,r11l,sk48,ls20}/<id>-deep-analysis.md: authoritative near-miss check.
- workspace/mechanic-pick.md: ID `kf42` and family tag.
- workspace/logs/state_log.md: visit-count check (this is the 1st entry to critique_spec; cap of 5 not yet at risk).

## Deliverables Produced
- workspace/critique-revisions.md: 5 issues (3 substantive: target-pad shape silhouettes "0", cycler-pad shape ambiguous as "L"/"⌐", L2/L3 cycler semantics drift; 2 clarifications: hidden-state encoding layout, win-condition edge-case formalisation). Decision: loop back to write_spec.

## Notes
- 12 of 16 checklist items pass cleanly on first read; one passes with a clarification request; three fail (items 7 ×2 sprite-shape ambiguities; the L2/L3 cycler-drift weakens item 10 but doesn't break it).
- Novelty re-check against deep-analyses for m0r0/r11l/sk48/ls20 confirms NOVEL — distinguishing rules at the deeper view also hold.
- Looping to write_spec: this is critique-pass #1; the cap of 5 visits is well clear.
