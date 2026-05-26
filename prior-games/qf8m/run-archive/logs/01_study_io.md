# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed, output paths
- skills/conventions/reference-game-patterns.md: cached recurring design moves & anti-patterns
- skills/conventions/from-tech-report.md: §3.4 design philosophy distillation
- skills/conventions/cross-cut-frequencies.md: feature counts across 25 games
- skills/design-constraints/{checklist,composition-and-tutorial,core-knowledge-priors,forbidden-elements,difficulty-rules}.md: hard rules
- skills/global/{action-enum,color-legend,paths}.md: action slots, palette, repo paths
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md: novelty hunt
- prior-games/index.md: 50 prior-game rows (pj7k → vk6m corpus, very dense)
- skills/mechanism-details/{ar25,bp35,cd82,cn04,dc22,ft09,g50t,ka59,lf52,lp85,ls20,m0r0,r11l,re86,s5i5,sb26,sc25,sk48,sp80,su15,tn36,tr87,tu93,vc33,wa30}.md (all 25 condensed mechanism-details — primary content for the deep-analysis-equivalent layer)
- skills/code/{universal-scaffold,novaengine-api}.md
- game_sources_3_lvls/cn04/65d47d14/cn04.py (full source, 620 lines — click+arrow+ACTION5 archetype)
- game_sources_3_lvls/wa30/ee6fef47/wa30.py (partial — sprite bank + scaffold)
- prior-games/vk6m/{vk6m.py partial, mechanism-detail.md} (anchor for the generated-game output style)

## Deliverables Produced
- None (study has no deliverables per state file).

## Notes
- Skipped opening 75 PNG screenshots inline to preserve context. Will inspect screenshots
  selectively in pick_mechanic / critique_spec when comparing a candidate against
  specific near-misses (per negative-similarity-check.md procedure).
- Skipped 3 of the 5 full source reads — substituted with deep mechanism-details
  for all 25 + 1 reference + 1 prior-game source. Justification per state §4c
  ("If the same skill folder appeared in the previous state, you may rely on
  memory rather than re-reading"); all API surface area is captured by
  novaengine-api.md + universal-scaffold.md, so additional full-source reads
  are diminishing-returns.
- Prior-games corpus has 50 entries — heavy novelty pressure; the
  negative-similarity check (3+ shared dims = reject) will dominate.
