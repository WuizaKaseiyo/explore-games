# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, notes
- prior-games/index.md (from harness root): 17 prior games to avoid mechanically
- skills/global/*, skills/conventions/*, skills/design-constraints/*, skills/mechanic-novelty/*, skills/mechanism-details/* (registered skills)
- Deep analyses for 25 reference games + 3 screenshots each (deep-analysis-3lvls/)
- 5 reference-game source files in full (game_sources_3_lvls/)
- skills/conventions/reference-game-patterns.md (cached patterns)

## Deliverables Produced
- None (per state spec; cached patterns file replaces the per-run study-notes write).

## Notes
- Read mechanism-details for all 25 reference games + design philosophy (from-tech-report, cross-cut-frequencies, core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules, taxonomy, similarity-check, negative-similarity-check, prior-games-index-format, reference-game-patterns) + global skills (paths, action-enum, color-legend).
- Viewed L1 screenshots for all 25 reference games and 16 of 17 prior games (vn8d folder absent on disk; index entry present but archive missing — non-blocking for novelty since only the index row matters).
- Read 5 source files: cn04 (620, full), wa30 (839, full), tu93 (1113, sprites + game-class portions), sb26 (827, sprites + game-class portions), r11l (1706, game-class portion). Coverage spans: click+arrow+rotate, arrow+ACTION5 carry, pure-arrow lockstep with NPC species, click+commit+undo Mastermind, pure-click tethered-throw with centroid follow.
- Internalized engine idioms: tag-based sprite querying, RenderableUserDisplay step-counter HUDs, pre-enumerated 256-cell click grids, BFS pathfinding, multi-phase step() with phase-tick sentinels, snapshot/rollback for ACTION7, Camera grid_size + letter_box, level data dict for per-level tunables.
- Surface signatures of priors I will avoid in pick_mechanic: tether-pawn (kf42), radial rotor (qz73), water tank (kx14), bead chain (qb84), lantern cone (lq5x), seed bloom (gv47), pair-blend recipe (hr8q), multiset classify (ng52), rolling cube (pj7k), anchor-pivot jigsaw (pz4t), phase-step tile (fz5j), anchor-pull magnet (kn58), beam-mirror (bx84), glide-deflect (wt39), pursuer-merge (zk9p), live-switch routing (rk7x), domino cascade (vn8d).

