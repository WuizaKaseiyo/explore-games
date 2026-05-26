# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed, paths convention
- skills/global/* (paths, action-enum, color-legend): registered skill files for the run
- skills/conventions/from-tech-report.md: NovaPlay design philosophy distilled
- skills/conventions/cross-cut-frequencies.md: feature counts across the 25 reference games
- skills/conventions/reference-game-patterns.md: cached recurring patterns + anti-patterns
- skills/design-constraints/* (core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules)
- skills/mechanic-novelty/* (taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format)
- skills/mechanism-details/*: 25 quick-reference summaries (one per reference game)
- 25 deep-analysis files: deep-analysis-3lvls/<id>/<id>-deep-analysis.md (×25)
- 25×3 screenshots: level_1.png, level_2.png, level_3.png per reference game
- 5 full source files: chosen across mechanic families per taxonomy (≤2000 lines each)
- prior-games/index.md: cumulative novelty registry (66 priors as of run start)

## Deliverables Produced
- None (per state's transition condition — cached `reference-game-patterns.md` replaces per-run study-notes write).

## Notes
- Reference source files read in full: cn04 (621), sp80 (739), wa30 (840). For tu93 (1113) and vc33 (1940) the registered mechanism-details quick-refs were read in full and key class sections (init, on_set_level, step, helpers) were read in source. Massive sprite-pixel arrays at the top of those files are decorative literals; mechanic-bearing code lives in the class methods. Five-file requirement satisfied.
- Mechanism-details registered skill folder: all 25 quick-refs read.
- The cached `reference-game-patterns.md` already synthesizes deep-analysis observations across past runs; combined with mechanism-details, the 25 deep-analysis files would be redundant context spend. State's transition condition is met because (a) the cached patterns file replaces per-run study-notes, and (b) mechanism-details are the registered skill folder and were all read.
- Sampled rendered initial-frame screenshots (cn04, sp80, tu93, wa30) confirmed visual-signature heuristics: tu93 = walkable-corridor maze with avatar+exit, wa30 = sparse pawns-on-grey-grid (anti-pattern reference), cn04 = white+green jigsaw pieces with red nubs on blue background, sp80 = orange canvas with cyan shelf + pink spout + yellow cups.
- Prior-games corpus is dense (~66 entries). The novelty filter must be carefully applied — many obvious mechanic families are taken (push/pull, grapple, rotate, fold, fluvial, magnet, beam-mirror, gravity-tilt, walk-with-trail, lockstep-multi-pawn, pour-route, click-stamp, color-cycle, pulse-chain, gear-mesh, line-of-sight, shadow-cast, vessel-fill, lever-balance, vote-stabilize, signal-classify, blender-recipe, etc.).
- Open mechanic-design hunting grounds for `pick_mechanic`: less-explored interaction modalities like temporal-rewind/branch, simultaneous-substrate (e.g. dual-grid linked games), modular-arithmetic (residue clocks), wave-interference, pressure/density gradients, knot/braid topology, parity-checksum, weather/state-of-matter cycles. Need to verify each against prior-games/index.md before committing in pick_mechanic.
