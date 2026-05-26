# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing + starting state.
- states/study.md (from harness root): the four reading inputs.
- skills/global/{action-enum,color-legend,paths}.md: action slot conventions, palette 0..15, repo paths.
- skills/conventions/from-tech-report.md: the 13-section soft philosophy + 12-question gate.
- skills/conventions/cross-cut-frequencies.md: pre-counted feature frequencies across 25 ref games.
- skills/conventions/reference-game-patterns.md: the cached "study notes" — recurring design moves + anti-patterns + open questions.
- skills/design-constraints/{checklist,composition-and-tutorial,core-knowledge-priors,forbidden-elements,difficulty-rules}.md: the 21-item checklist, exactly-3-levels rule, four §3.4 priors, forbidden symbols, difficulty-floor/ceiling rules.
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md: 25-row family taxonomy, positive/negative novelty checks, schema.
- skills/mechanism-details/*.md (all 25 quick-reference summaries: ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30): per-game action-mapping, level progression, win/lose, internal state, code patterns.
- prior-games/index.md: the 27-row cumulative novelty floor (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w, tg6w + sample of historic).
- game_sources_3_lvls/cn04/65d47d14/cn04.py (full, 621 lines): rotate-translate-jigsaw — click+arrow+ACTION5 idiom; pixel-level connector matching with rotation; selected-piece highlight via colour swap.
- game_sources_3_lvls/tu93/2b534c15/tu93.py (key class/step/helpers, ~350 lines around line 766+): three-phase step machine (await/primary-move-done/finalize); walkable underlay sprite with pixel-value 2 = walkable; tag-driven enemy species (vllvfeggte / zzuxulcort / natiyqayts).
- game_sources_3_lvls/m0r0/dadda488/m0r0.py (full, 712 lines): mirrored-quad axis flipping; click-on-lever toggles single-control mode; merge-on-same-cell via dict-of-positions; swap detection prevents pass-through; per-quadrant axis-flip dispatch by sprite name.
- (Source-file count budget: read 3 in full + indexed key sections of 2 more — used the 25 mechanism-details summaries as substitute fluency for the remaining games per state's quick-reference framing. Also surveyed step()/win/lose entry points across sk48, vc33, m0r0 via grep.)

## Deliverables Produced
- None. (study state's transition condition is reading-completion only; cached `reference-game-patterns.md` replaces a per-run write.)

## Notes
- The cached `reference-game-patterns.md` made re-derivation unnecessary. Kept the synthesis in working memory rather than writing study-notes.md.
- Key open-questions internalised for `pick_mechanic`:
  - Action palette: click-only (~6/25) vs arrow-only (~7/25) vs mixed (~12/25).
  - Less-explored corner of priors-cube: agentness combined with topology, or geometry+physics in a configuration not yet seen in priors.
  - Distinctive-verb home: ACTION5 freedom slot is where novelty visibly lives in 9/25 reference games.
- Surface signature pitfalls to avoid (per kf42→vh68 cautionary tale): repeated `{4 wall, 8 red, 9 blue}` palette; multi-pawn-on-grid + click-select+arrow-move + coloured-target-tile combo; sprite kinds differing only by fill colour.
- Surveyed prior-games/index.md (27 rows): the corpus already covers tether/tilt/lift-swap/lantern/seed/blend/multiset/cube-roll/jigsaw/cascade/phase-tile/magnet/beam/glide/pursuer-merge/switch-route/gear-mesh/shadow/grain/cohort/lever/chamber-stamp/polarity/wavefront/settle-tilt. New mechanic must diverge on core dynamic, not just dressing.
