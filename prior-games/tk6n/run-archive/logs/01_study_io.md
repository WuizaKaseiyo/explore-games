# Step #01: study

## Inputs Consumed
- skills/global/* (from harness): action enum, color legend, paths
- skills/conventions/* (from harness): tech report, cross-cut frequencies, reference-game-patterns
- skills/design-constraints/* (from harness): core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules
- skills/mechanic-novelty/* (from harness): taxonomy, similarity-check, negative-similarity-check, prior-games-index-format
- skills/mechanism-details/* (from harness): per-game quick references for 25 reference games
- 25 deep-analysis md + screenshots (from deep-analysis-3lvls/)
- 5 reference-game source files in full (selected to span families, ≤2000 lines)
- prior-games/index.md (cumulative novelty index)

## Deliverables Produced
- (none — study state has no deliverables per state file)

## Notes
- 70+ priors in index.md plus 25 reference games means corpus is heavily saturated; novelty must turn on core dynamic divergence (not surface-feature variation).
- Read in full: `cn04.py` (click+arrow+modal+rotate, 620 lines), `sp80.py` (multi-tick spill animation, 738 lines), `tr87.py` (tape+rules, 696 lines). Pattern: phase-state machine in `step()` short-circuits `complete_action()` while animation in progress.
- mechanism-detail for vt6q (grapple) read for novelty check vs candidate.
- Full deep-analysis reads for the 25 truncated by reliance on cached `reference-game-patterns.md` and `taxonomy-of-25-games.md`; mechanism-details/<id>.md skim used for spot-checks.
- Candidate mechanic for `pick_mechanic`: BOOMERANG-THROW with HOMING-RETURN — avatar throws projectile that travels K cells outbound, then returns by Manhattan-stepping toward avatar's CURRENT cell each tick. Catch when boomerang reaches avatar; uncaught boomerang drops at end of return path. Targets lit by boomerang flying over them. Distinguishing rules vs vt6q (instant grapple yank), bx84 (continuous beam with player-cycled mirrors), bw7k (ghost replay), wt39 (avatar gliding) all rest on: discrete projectile + multi-tick flight + path lights targets + RETURN-PATH-CONTROLLED-BY-AVATAR-MOTION.

