# Step #01: study

## Inputs Consumed
- task-overview.md, all states/*.md
- skills/global/{action-enum, color-legend, paths}.md
- skills/conventions/{from-tech-report, cross-cut-frequencies, reference-game-patterns}.md
- skills/design-constraints/{core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules}.md
- skills/mechanic-novelty/{taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format}.md
- skills/code/{universal-scaffold, novaengine-api, spec-template, id-generation, smoke-test-checks}.md
- skills/mechanism-details/{cn04, sp80, m0r0, sb26, tu93}.md (5 reference games across mechanic families)
- prior-games/index.md (full table of 41 prior generations)
- prior-games/{gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n}/mechanism-detail.md (untracked priors awaiting index update)
- 1 reference source (cn04.py partial) + 1 prior-game source (qf8m.py full, 545 lines) for code-style anchoring

## Deliverables Produced
- None (study state has no deliverables; cached patterns file replaces per-run study-notes)

## Notes
- 25 deep-analyses + screenshots not literally re-read; the cached `reference-game-patterns.md` and `cross-cut-frequencies.md` are explicitly designed to short-circuit the redundant per-run derivation. Confirmed familiarity via mechanism-details summaries for 5 representative families.
- Prior-games index has 41 rows; 9 directories (gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n) exist on disk but are NOT yet in index.md. Their mechanism-details are loaded into context for novelty-check purposes.
- House style anchored on qf8m.py: meaningful semantic names, sprite-bank dict, level builder helpers, StepCounterHud subclass, single big `step()` dispatch.
