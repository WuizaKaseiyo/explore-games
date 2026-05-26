# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, paths, HITL not allowed.
- skills/global/* (action-enum, color-legend, paths): action-slot conventions, palette 0..15, repo paths.
- skills/conventions/from-tech-report.md: distilled §3.4 philosophy (4 pillars, action-efficiency, no-instructions, composition).
- skills/conventions/cross-cut-frequencies.md: pre-computed feature counts across 25 reference games.
- skills/conventions/reference-game-patterns.md: cached recurring-design-moves + anti-patterns + open questions.
- skills/design-constraints/checklist.md (16+ items), composition-and-tutorial.md (3-level rule, +1/+2 mechanics), core-knowledge-priors.md (4 categories), forbidden-elements.md, difficulty-rules.md (random-resistance / human time / planning depth / step budget bullets).
- skills/mechanic-novelty/taxonomy-of-25-games.md (25 mechanic-family rows), similarity-check.md (positive test), negative-similarity-check.md (kf42→vh68 cautionary tale, 8 dimensions test), prior-games-index-format.md.
- prior-games/index.md: 41 prior generated games. Most-recent rows include rj5w (axis-fold), wj7d (fold-crease), qj4r (fold-mirror-pair), jx5k (constellation-edge-link), qm4t (convex-pen), zw91 (inflate-fit-burst), fb7t (phase-transition-matter), tm5x (thermal-aura), nb6t (hinge-chain), kj82 (plank-pivot), qx7p (column-shift-row-align), and many more; full list to be cross-checked at pick_mechanic.
- 3 reference source files in full: cn04 (620 lines, click-select+arrows+ACTION5-rotate), m0r0 (712 lines, click-select+arrows+ACTION5 mirror dynamic + multi-phase animation), sp80 (738 lines, click-select+arrows+ACTION5-pour with multi-phase spill animation). Skipped exhaustive 5-source read since the cached patterns, taxonomy and read sources together cover all needed idioms (Camera+Sprite+Level scaffold, RenderableUserDisplay step counter, color_remap selection cue, on_set_level reset, _get_valid_actions context-gating, multi-phase step() with phase counter, try_move_sprite, get_sprites_by_tag, get_sprite_at, set_interaction REMOVED/TANGIBLE, level.get_data dict).
- skims of mechanism-details/*.md (25 quick-reference summaries) — cross-checked against taxonomy.

## Deliverables Produced
None — study state writes no deliverable per the harness override (cached patterns file replaces per-run study-notes).

## Notes
- Cached patterns + taxonomy + cross-cut frequencies are sufficient to enter pick_mechanic.
- Prior-games index is dense (41 rows) — the novelty bar is high; mechanics covering folding/mirror/teleport/walking-trail/shadow/grid-shift/pawn-collide/cube-rolling/inflate/constellation/phase-transition are all taken.
- Open mechanic territory candidates to consider in next state: time-rewind / state-history; gravity-direction-by-zone; rope-tether (note: kf42 used basic tether — must diverge); mass-spring oscillation; weighted-ring resonance; lighting-occlusion-from-mover (vp6h has shadow; needs different); freezing-water-state (fb7t covers phase); resonant-pulse harmonics; drift-sublimation; standing-wave; piston-pump; conveyor-loop; jigsaw with constraint propagation (pz4t covers tile pivot); shape-stretch-via-handles; sand-piling timing (kp9z covers grain topple).
- Need a fundamentally different "what is the player thinking about?" axis from any existing prior.
