# Step #01: study

## Inputs Consumed
- `task-overview.md` (from harness root): workflow framing, FSM diagram, paths, HITL=not allowed, autonomous-mode (no seed string passed).
- `skills/global/{paths.md, action-enum.md, color-legend.md}` (registered): repo path table, ACTION0–7 semantics + subset patterns across 25 games, palette 0–15.
- `skills/conventions/from-tech-report.md` (registered): §3.4 design philosophy, RHAE scoring, novelty axes, 12-question convention gate.
- `skills/design-constraints/{core-knowledge-priors.md, forbidden-elements.md, composition-and-tutorial.md, checklist.md}` (registered): four allowed priors, banned elements, 3-level mandate (override of §3.4 ≥6), 16-point spec checklist.
- `skills/mechanic-novelty/{taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md, prior-games-index-format.md}` (registered): 25-row taxonomy, two-axis novelty test, kf42→vh68 cautionary tale (3+ shared dimensions = reject).
- `prior-games/index.md` (cumulative): two priors — `kf42` tether-pawn-cycle, `qz73` radial-cycle-lock.
- `prior-games/kf42/mechanism-detail.md`, `prior-games/qz73/mechanism-detail.md` (deeper view of priors): tether-drag invariant, two-pass atomic rotation idiom.
- `prior-games/kf42/run-archive/smoke-frames/level_1.png`, `prior-games/qz73/run-archive/smoke-frames/level_1.png`: priors' visual signatures (kf42=dark walled grid + small red/blue rectangle pawns; qz73=grey field + small coloured tip squares around hub).
- `deep-analysis-3lvls/<id>/<id>-deep-analysis.md` for all 25 IDs (consumed via Explore subagent that compressed Frequency-table contributions across the 25 files into a single synthesis).
- `deep-analysis-3lvls/<id>/level_1.png` for ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30 (25/25 reference games sampled at L1).
- Three full reference-game source reads:
  - `game_sources/cn04/65d47d14/cn04.py` (681 LOC; click+arrow+ACTION5 modal; nub-pair-glyph).
  - `game_sources/tu93/2b534c15/tu93.py` (1251 LOC; pure cardinal arrows; maze-pickup-train).
  - `game_sources/r11l/aa269680/r11l.py` (1822 LOC; pure click; centroid-puppet-leg).

## Deliverables Produced
- `workspace/study-notes.md`: cross-cut frequency observations (X/25 across 14 dimensions), 8 recurring design moves, 6 recurring anti-patterns (including the kf42→vh68 visual-sameness trap), 4 open questions for `pick_mechanic`, per-game one-line essences for all 25 IDs, and a notes-block on what each of the three full-source reads anchored.

## Notes
- Defensive workspace check passed (only `.gitkeep`, `__pycache__`, `logs/` present before this state ran).
- The three full-source reads were chosen to span different action-subset patterns (modal click+arrow+ACTION5 = cn04; pure arrows = tu93; pure click = r11l) per the state's "click-only / arrow-only / click+arrow+modal" guidance, all under the 2000-line budget.
- Two priors exist; both share *small-rectangular-coloured-pawns + click-select* as a surface signature. The kf42→vh68 cautionary tale specifically warns against repeating that signature. Pick_mechanic must diverge on either palette / sprite-grain / core-dynamic, not just on verb-cardinality.
- §3.4-implied composition rule for our 3-level cap: L1 base system (one or more interacting mechanics, all required by witness), L2 = N+1, L3 = N+2 mechanics required by witness. No hidden mechanics.
- Deep-analysis Frequency-table extraction was delegated to an Explore subagent to keep main-context lean; visual-signature scan over screenshots was done in-context because the design-constraints check explicitly requires the eye for the negative similarity test.
