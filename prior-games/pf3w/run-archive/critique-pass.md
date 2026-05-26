# Critique pass — `pf3w` (visit 2 of 10; passes after 1 revision)

## Checklist (`design-constraints/checklist.md` items 1-21)

| # | Item | Verdict | Brief justification |
|---|---|---|---|
| 1 | Palette 0..15 + -1 transparent | ✅ PASS | Spec uses palettes 3, 4, 6, 10, 11, 14, 5; transparent is -1. |
| 2 | Universal scaffold | ✅ PASS | Spec follows code/universal-scaffold.md (sprite bank, levels, constants, HUD widget, game class with on_set_level, step, _get_hidden_state, _get_valid_actions). |
| 3 | available_actions ⊆ [1..7] | ✅ PASS | `[5, 6]`. |
| 4 | EXACTLY 3 levels | ✅ PASS | L1, L2, L3 enumerated. |
| 5 | 4-char ID, lowercase, alphanumeric, opaque, non-colliding | ✅ PASS | `pf3w`; verified against 25 references + 24 priors. |
| 6 | Mechanics from core-knowledge-priors.md only | ✅ PASS | Objectness + geometry/topology + physics. |
| 7 | No letters/digits/clipart/cultural-conventions | ✅ PASS | Sprites are crosses, square-rings, checker-walls. No glyphs that read as letters or digits. |
| 8 | ≥ 2 distinct mechanics in environment | ✅ PASS | Environment has M1, M2, M3a, M3b. |
| 9 | L1 tutorial: reduced state space, no on-screen text | ✅ PASS | L1 has 1 emitter + 1 target + outer border; no text. |
| 10 | L2/L3 difficulty by composition not scaling | ✅ PASS | L2 adds M2 (timing); L3 adds M3a (wall) + M3b (color-keying); all earlier mechanics carry forward. |
| 11 | Mechanic inheritance + 1-or-+2 per level | ✅ PASS | L1=1, L2=2 (= N+1), L3=4 (= L2-count + 2). All within rule. |
| 12 | Strict counterfactual necessity, per-mechanic-per-level table | ✅ PASS | Per-mechanic counterfactuals stated for L1 (M1), L2 (M1, M2), L3 (M1, M2, M3a, M3b). Each cites a specific cell/sprite/rule that blocks every alternate path; specifically: L2 M2 blocks via lit-tick-set-disjoint at no-stagger; L3 M2 blocks via 25-vs-22 BFS-distance asymmetry; L3 M3b blocks via cross-color routing being shorter (26 actions) only without M3b. |
| 13 | Mechanic family absent from taxonomy | ✅ PASS | `wavefront-converge-timing` not in taxonomy. |
| 14 | Mechanic family absent from prior-games | ✅ PASS | Not in 24 priors. |
| 15 | Distinguishing rule articulated for any near-miss | ✅ PASS | Concrete rules vs cd82, sp80, bp35, g50t, ka59, re86, ft09 (taxonomy) and bx84, vp6h, gv47, vn8d, kp9z, gx7m (priors). |
| 16 | Win condition stated as testable predicate | ✅ PASS | All targets currently in their `_lit` variant → next_level. |
| 17 | Lose condition stated | ✅ PASS | `self._action_count >= step_budget` → lose. |
| 18 | Per-level (a) random-resistance, (b) human-tractable, (c) planning depth, (d) step budget | ✅ PASS | All four bullets present per level; L2 enumerates 3-action post-discovery decision space and names the wrong-slot-first plausible alternative; L3 enumerates same and names the no-stagger plausible heuristic that fails. Step budgets monotonically increase 30 → 35 → 70. |
| 19 | No hidden state | ✅ PASS | Each emitter's `T_activated` is encoded into its current wavefront radius, which is rendered as the wavefront sprite's pixel matrix every step. The visible cue persists for the lifetime of the active emitter. |
| 20 | No info loss at 32×32 | ✅ PASS (after revision) | Spec revised in pass 1 to use `grid_size=(64, 64)` with `LOGICAL_CELL_SIZE=4`. All gameplay-relevant sprites have internal sub-cell pixel patterns: emitter slot uses hollow-frame-per-logical-cell; lit emitter uses filled-frame-per-arm + fully-yellow-center; targets use hollow-frame-per-arm + transparent-or-yellow-center; walls use 4×4 checker; wavefront sprite paints frontier cells as hollow-frame palette. Each pattern visibly damages under 2:1 downsampling (frame-vs-center distinctions average away, checker collapses). |
| 21 | UI teaches role | ✅ PASS | Sprite UI ≈ sprite role: dim grey hollow cross reads as inactive button; lit colored cross with yellow center reads as active source; hollow colored ring reads as receiver; filled colored ring with yellow center reads as received-signal. Identical-visuals ≈ shared-roles: same-shape slots/targets share role; color signals which slot pairs with which target. Visual carries mechanic: wavefront expansion is directly observable as colored halo cells advancing per ACTION5. |

## Novelty (`mechanic-novelty/similarity-check.md` + `negative-similarity-check.md`)

Re-walked the full spec (not just family name) against:

- **25 reference games**: every plausible near-miss (cd82, sp80, bp35, g50t, ka59, re86, ft09) consulted via `mechanism-details/<id>.md` and crossed-checked against deep-analyses. None of the seven shares the *load-bearing* axis of `pf3w` (multi-source wavefront synchronization with `ACTION5` as global-tick verb). All distinguishing rules from `mechanic-pick.md` § Novelty check vs. 25 reference games still hold for the fleshed-out L1/L2/L3 spec.
- **24 prior-games entries**: every plausible near-miss (bx84, vp6h, gv47, vn8d, kp9z, gx7m) consulted via `prior-games/<id>/mechanism-detail.md` and rendered initial-frame screenshots. Negative-similarity walk on each puts shared dimensions at 1-3 of 8, all heavy-weighted dimensions (visual, pixel grain, core dynamic) DIFFERENT. PASS.

**Verdict: NOVEL.**

## Outcome

All 21 checklist items + novelty PASS after revision pass 1. Transition to `implement`.
