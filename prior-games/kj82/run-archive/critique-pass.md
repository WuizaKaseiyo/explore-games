# Critique pass — visit 2

Spec revision 2 (`workspace/mechanic-spec.md`) addresses both
issues from visit 1's `critique-revisions.md`. All checklist
items now pass.

## Item-by-item verdict

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Palette 0..15 (and -1 transparent) | ✅ | Spec uses {0, 1, 4, 5, 6, 8, 10, 11, 12, 13, 14} only. |
| 2 | Universal scaffold structure | ✅ | Spec follows imports → sprites → levels → constants → HUD → game class order; implementation phase will materialise it. |
| 3 | `available_actions` ⊆ [1..7] | ✅ | `[1, 2, 3, 4, 5, 6]`. |
| 4 | Exactly 3 levels | ✅ | L1, L2, L3 declared in §4. |
| 5 | 4-char ID, opaque, no collision | ✅ | `kj82` — verified non-English-word, not in 25 reference, not in 29 priors. |
| 6 | Core priors only | ✅ | Objectness + geometry/topology + physics. No agentness misuse. |
| 7 | No letters/digits/clipart/cultural | ✅ | Spring redesigned to symmetric green-ring (no chevron/arrow). Plank, pawn, goal, post, spring — all abstract shapes. No letters/digits/arrows/clipart. |
| 8 | ≥ 2 distinct mechanics | ✅ | 4 mechanics across the game (M1-M4). |
| 9 | L1 tutorial | ✅ | 1 plank, no posts/springs, no hazards, all required mechanics exercised by witness. Reduced state space (single plank). |
| 10 | L2/L3 compose mechanics | ✅ | Every L1 mechanic still required at L2; every L2 mechanic still required at L3; new mechanics added per level interact with carried-forward ones. |
| 11 | +1-or-+2 inheritance per level | ✅ | L1 N=2 → L2 N+1=3 → L3 3+1=4. Each promotion adds exactly 1 new mechanic; no level promotion adds 0 or ≥3. |
| 12 | Strict counterfactual necessity | ✅ | Per-mechanic per-level table provided in §4 of spec; alternate-strategy enumeration walks 4-6 candidates per level showing each fails without the respective mechanic. L3's M4 verified by per-orientation per-plank enumeration ruling out walking-to-goal alternatives. |
| 13 | Mechanic absent from taxonomy | ✅ | Distinguishing rules vs cn04 (rotate-translate-jigsaw — in-place rotation, no anchor-pinned planks; verb set differs) and ar25 (mirror-cover — no reflectors in kj82). |
| 14 | Mechanic absent from priors | ✅ | Distinguishing rules vs pz4t (place-then-rotate jigsaw — user-chosen anchors, free translation; kj82 anchors are level-fixed and planks pinned), bx84 (beam-mirror — no beam in kj82), wt39 (glide-deflect — discrete walk in kj82, not slide), pj7k (rolling-cube — separate avatar in kj82, not cube-as-avatar), xn5p (chamber-stamp — no stamping in kj82). |
| 15 | Distinguishing rules concrete | ✅ | All flagged near-misses have specific, mechanically-grounded rules — verb-set differences, geometry differences, win-condition differences. No vague "different colours / harder" hand-waves. |
| 16 | Win condition stated | ✅ | "pawn's grid cell == goal_tile's grid cell" — uniform across all 3 levels. |
| 17 | Lose condition stated | ✅ | "_action_count >= _max_steps" — uniform. No hidden lose paths. |
| 18 | Difficulty floor and ceiling | ✅ | (a) random-resistance, (b) human-time, (c) planning depth, (d) step budget — all four bullets present per level. L2 enumerates ≥ 2 useful first actions (4); L3 ≥ L2's count (4). L3 names a trivial heuristic (greedy monotone progress) that fails at (16, 9). Step budgets 30/50/60 do not shrink across levels. |
| 19 | No hidden state | ✅ | active_plank state surfaced via anchor_halo overlay; post state via two-sprite-swap visual difference; pawn position rendered directly; step budget via depleting bar; spring direction implicit from underlying plank's orientation (visible). |
| 20 | Don't generate low-resolution game | ✅ | Grid 32×32 at scale 2 (NOT 16×16 at scale 4). Planks 2 cells thick × 8/13 long (4×16 or 4×26 display pixels) with internal stripe. Pawn/goal/post/spring all multi-cell sprites with internal pattern. Shape carries meaning (each sprite type distinguishable by shape, not just colour). |
| 21 | Design UI to teach | ✅ | Plank reads as "long wood board with one fixed end" via anchor visual + plank stripe; pawn reads as "small character" via 3×3 ring+pip pattern; goal as "destination ring"; post as "obstacle" (filled solid) vs "passable" (hollow ring); spring as "special pad" (green-ring abstract). All multi-cell with distinguishing shape. |

## Novelty re-check

Re-walked similarity-check.md against the **fleshed-out** spec
(not just the family name). Closest taxonomy entries: cn04, ar25.
Closest prior-games: pz4t, bx84, wt39, pj7k, xn5p. For every
flagged near-miss, §9 of `mechanic-spec.md` articulates a concrete
distinguishing rule that survives the level-by-level scrutiny —
no rule drifts at L2 or L3 of the spec.

Re-walked negative-similarity-check.md (8 dimensions) against
each flagged near-miss. Shared dimension count is ≤ 1 (the
universal step-budget lose condition) for every prior. Below the
3+ rejection threshold. **PASS.**

## Verdict

**All 21 checklist items pass. Novelty PASS. Transitioning to
`implement`.**
