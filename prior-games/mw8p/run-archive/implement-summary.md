# Implement summary — mw8p (revised after user feedback)

## Files written

- `prior-games/mw8p/mw8p.py` — 472 lines (revised from 423).
- `prior-games/mw8p/metadata.json` — unchanged.

## What changed in the revision

1. **Levels redesigned for actual reasoning** (per user critique
   "literally no reasoning needed"). Previously every witness was
   "7 RIGHT then 7 UP/DOWN" with NPCs doing the puzzle work
   autonomously. Now each level demands a non-obvious decision:
   - L1: DOWN-first wins / RIGHT-first loses at turn 8.
   - L2: RIGHT-first triggers M2 at turn 1 / DOWN-first loses by turn 5.
   - L3: forced M3 at turn 1, then 3-forward + 3-retreat + 7-forward + 7-down
     (counter-intuitive retreat is required because the greedy
     forward path loses at turn 4).

2. **Multi-frame animation for the chase and the eat** (per user
   critique "use animation to show the chase and eat"). Each
   ACTION1..4 now produces FIVE rendered frames via a
   `self._phase` counter that short-circuits `complete_action()`
   until phase 4 finishes:
   - Phase 0: A's full-cell move.
   - Phase 1: every B slides 4 px (half-step).
   - Phase 2: every B completes the full step + B-on-A resolves.
   - Phase 3: every C slides 4 px (half-step).
   - Phase 4: every C completes + M2 resolves + step counter ticks.

   The B's and C's now visibly slide between cells; M2's kill is
   visible as a one-frame "C on top of B" overlap (C is layer 2,
   B is layer 1) followed by B's removal on the next action's
   first frame. Animation verified by inspecting
   `g.perform_action(..., raw=True).frame` returning a 5-element
   list of (64, 64) frames per action.

## Verified at implement time

- `python -c "import ast; ast.parse(...)"` passes.
- `Mw8p()` instantiates without exception.
- `g.set_level(0..2)` produces (64, 64) frames with palette in [0, 15].
- L1 witness `[2]*7 + [4]*7` advances `_score` from 0 → 1.
- L2 witness `[4]*7 + [2]*7` advances `_score` from 1 → 2.
- L3 witness `[4,4,4,3,3,3,4,4,4,4,4,4,4,2,2,2,2,2,2,2]` advances
  `_score` from 2 → 3 AND the engine state transitions to `WIN`.
- Counterfactual losses verified by replay: L1 RIGHT-first loses
  at turn 8, L2 DOWN-first loses at turn 5, L3 naïve forward loses
  at turn 4. (See `smoke-test-pass.md` § Counterfactual losses.)
- Multi-frame animation: 5 frames per action confirmed by
  `len(perform_action(..., raw=True).frame) == 5`.

## Notes for future agents

- The pursuit policy uses Manhattan-dominant axis with tie → x.
  This tie-breaker is load-bearing: at L2, A's DOWN-first puts A
  at (0, 1) where `|A.y - B.y| = 4 = |A.x - B.x|`, and the tie
  resolution to x makes B step horizontal (away from C). The
  level designs assume this tie-breaker.
- B's `layer = 1`, C's `layer = 2`, A's `layer = 3`. The
  layering matters for the M2 visual (C must render on top of B
  for the "kill frame" to be legible) and for the M3 visual (A
  must render on top of C).
- `_b_pending` and `_c_pending` are computed once at phases 0 and
  2 respectively, NOT recomputed on each animation phase. This
  ensures consistency between half-step and full-step targets;
  changing the policy mid-animation would produce visual glitches.
