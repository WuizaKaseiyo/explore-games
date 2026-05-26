# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): mechanic family + ID + sketch
- skills/code/spec-template.md: 9-section spec format
- skills/code/universal-scaffold.md: file structure + camera viewport rule + two-sprite swap idiom
- skills/code/id-generation.md (re-checked): mr5q non-collision verified
- skills/design-constraints/checklist.md: items 1-21 (in particular 11/12/18/19/20/21 for §4)
- skills/design-constraints/composition-and-tutorial.md: exactly 3 levels, +1-or-+2 per level promotion
- skills/design-constraints/difficulty-rules.md: per-level random-resistance, human time, planning depth, step budget
- skills/design-constraints/forbidden-elements.md: re-checked the half-fill / cross-on-ring patterns are topological motifs not symbol/digit/letter glyphs
- skills/design-constraints/core-knowledge-priors.md: mapped to 4 of 4 priors (objectness, agentness, basic physics, basic geometry/topology)

## Deliverables Produced
- mechanic-spec.md: full 9-section spec.
  - §1 Title; §2 Mechanic family with prior categories; §3 Sprite roster including yang/yin pixel matrices, flip-pad, wall, and explicit no-hidden-state + visual-detail-floor + sprite-UI-≈-role justifications.
  - §4 Three levels with explicit mechanic enumeration (L1=3, L2=4, L3=5; +1 per promotion), per-mechanic counterfactual necessity sentences, and per-level witness solutions written out action-by-action with click coordinates.
  - §4 Each level's difficulty justification covers all four bullets (random-resistance, human-tractable, planning depth post-discovery, step budget). L2 enumerates post-discovery decision space, names a plausible-but-wrong alternative, and traces witness reasoning. L3 names a trivial heuristic that fails (greedy without re-flipping pad-flipped pawns) and shows where heuristic diverges from witness.
  - §5 Action mapping: `available_actions=[5,6]` with concrete tick-step rule (Manhattan dominant axis, deterministic tie-break, wall-and-occupant fallback).
  - §6 HUD = StepCounterHud (depleting bar in row 0); per-game state list.
  - §7 Win predicate: active-pawn count == 0 → next_level().
  - §8 Lose predicate: step_counter == 0 → lose(); explicit reasoning for why no soft-lock detection is needed (ACTION6 always available as recovery).
  - §9 Novelty note re-citing the closest taxonomy entries and prior-games entries with concrete distinguishing rules; negative-similarity-check verdict (2 of 8 shared, well below threshold).

## Notes
- Decided on EXACTLY 3 levels, grid (14, 14) for all three, with the camera viewport explicitly resized in `on_set_level` (per universal-scaffold.md camera rule).
- Pad mechanic (E at L3) is necessary because the y=9 wall is solid except at the two pad cells — pad-traversal is forced for any cross-y=9 attract-walk. Witness explicitly issues a re-flip ACTION6 after each pad crossing.
- Witness solutions for L2 and L3 acknowledge the wall-fallback path determinism ambiguity (some ticks choose orthogonal-fallback steps). The exact action count is approximate at the spec level and is determined precisely by the implementation in `implement` state.
- Visual signature deliberately diverges from kf42 and zd7m (palette {1,3,6,10,11,12,14,15} vs kf42 {4,8,9} and zd7m {3,7,11,10}); pixel grain is 5×5 with internal half-fill (vs kf42's plain 1×1/2×2/3×3 and zd7m's 4×4 ring + centre-pixel).
- Step budgets: L1=30, L2=80, L3=200. All ≥ 4× witness length, generous over witness as required by difficulty-rules.md § 2 (d).
