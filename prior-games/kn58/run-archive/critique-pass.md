# critique-pass for kn58 — visit #2 (post-revision)

| # | Item | Verdict |
|---|------|---------|
| 1 | Palette values 0..15 + −1 transparent | ✅ PASS — sprites use {−1, 0, 4, 5, 8, 10, 12, 14, 15}. |
| 2 | Universal scaffold structure | ✅ PASS at spec level (implementation will verify). |
| 3 | `available_actions` ⊂ [1..7] | ✅ PASS — `[6]` (pure click). |
| 4 | Exactly 3 levels | ✅ PASS. |
| 5 | 4-char ID, lowercase alphanumeric, not reserved/in priors, not English word | ✅ PASS — `kn58`. |
| 6 | Mechanics from `core-knowledge-priors.md` | ✅ PASS — objectness + geometry/topology + physics. |
| 7 | No letters / digits / clipart / cultural conventions | ✅ PASS — anti-anchor revised to "corner-dot frame with inner block"; pawn/target/anchor/wall all abstract. |
| 8 | ≥ 2 distinct mechanics | ✅ PASS — 6 (M1, M2, M3, M4, M5, M7). |
| 9 | L1 tutorial — base dynamic system, all required, reduced state space, no on-screen text | ✅ PASS — L1 = 1 pawn + 1 target on bare arena, M1+M2+M3 only. |
| 10 | L2/L3 increase difficulty by COMPOSING all mechanics | ✅ PASS — L2 forces pocket-detour with M4+M5; L3 forces row-detour around stuck pawn + anti-anchor route. |
| 11 | Mechanic inheritance + 1-or-+2 per level | ✅ PASS — L1: 3, L2: 5 (+2), L3: 6 (+1). All earlier mechanics required at every later level. |
| 12 | Strict counterfactual necessity / no trivial fallback | ✅ PASS — L1, L2, L3 each have witness-required mechanics named with trivial-heuristic-fail justifications. L3's "click target_orange every tick" heuristic is concretely shown to deadlock at (7, 8) due to M4. |
| 13 | Family absent from taxonomy | ✅ PASS — `anchor-pull-magnet` not in `taxonomy-of-25-games.md`. |
| 14 | Family absent from `prior-games/index.md` | ✅ PASS — closest is `anchor-pivot-place` (pz4t) but verb and goal disjoint. |
| 15 | Distinguishing rules articulated for near-misses | ✅ PASS — spec §9 + `mechanic-pick.md` enumerate concrete rules vs ka59, m0r0, wa30, r11l, kf42, pz4t. |
| 16 | Win condition stated | ✅ PASS — every pawn matched + stuck → `next_level()`. |
| 17 | Lose condition stated | ✅ PASS — step counter zero → `lose()`. |
| 18 | Per-level (a) random-resistance, (b) human time, (c) planning depth, (d) step budget — all 4 bullets, L2/L3 chain named | ✅ PASS — L1 (30 / ~30s / near-zero / 30), L2 (zero / ~2 min / pocket-detour reasoning chain named, "click target" deadlocks / 80), L3 (zero / ~2.5 min / "click target" deadlock at (7,8) named + commute test for actions 7↔8 / 60). |

**Novelty (positive similarity check):** NOVEL against every taxonomy and prior-games row. Distinguishing rules cited.

**Novelty (negative similarity check):** PASS — closest prior is ka59 (4 light dimensions shared on board class, click verb modality, target-cover goal, step-budget lose), but all 3 heavy axes (palette signature, pixel grain, core dynamic) diverge cleanly. No prior shares 3+ heavy dimensions.

**Verdict:** TRANSITION TO `implement`.
