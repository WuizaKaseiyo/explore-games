# Critique pass — cv5b spec (visit 2/10)

## Checklist (`design-constraints/checklist.md`)
| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | Palette 0..15 + -1 transparent | ✅ PASS | Uses {0,1,4,5,7,10,11,12,13,14}; all valid. |
| 2 | Universal scaffold structure | ✅ PASS | Spec follows; `implement` will enforce file layout. |
| 3 | `available_actions ⊆ [1..7]` | ✅ PASS | `[1, 2, 3, 4, 5, 6]`. |
| 4 | EXACTLY 3 `Level(...)` entries | ✅ PASS | L1, L2, L3 only. |
| 5 | 4-char lowercase ID, no ref / no prior collision | ✅ PASS | `cv5b`. |
| 6 | Mechanics from §3.4 priors only | ✅ PASS | objectness + basic geometry/topology + basic physics. |
| 7 | No letters / digits-as-glyphs / clipart / cultural | ✅ PASS | Abstract shapes only; launcher is a frame+dots, not a real-world catapult; targets are rings; shields are bars. |
| 8 | ≥ 2 distinct mechanics | ✅ PASS | 5 total (arc-fire, walk, power-cycle, shield, wind). |
| 9 | L1 base dynamic system, witness-required, reduced state, no on-screen text | ✅ PASS | L1 = single-mechanic tutorial (arc-fire); 1-action witness; trivial state space. |
| 10 | L2/L3 difficulty by COMPOSITION not scaling | ✅ PASS | L2 adds walk + power-cycle (different verbs/rules). L3 adds shield + wind (new environment rules). Each composes earlier mechanics; not just bigger grid or more pieces. |
| 11 | Mechanic inheritance & +1-or-+2 rule | ✅ PASS | L1=1, L2=3 (+2), L3=5 (+2); each level's witness exercises every carried mechanic AND every new mechanic. |
| 12 | Strict counterfactual necessity (per-mechanic table) | ✅ PASS | Per-mechanic counterfactuals stated in §4 for all 9 (mech, level) pairs; concrete cell/distance/budget arguments cite specific positions and ranges (not hand-waved). Walked alternates: walk-only L2 wins exceed step_budget; fire-only L2 has no fire that reaches both targets; up-and-around L3 path triggers shield rule via walk-block; firing-without-wind-correction lands one cell off. |
| 13 | Mechanic family absent from taxonomy-of-25 | ✅ PASS | Re-walked: closest taxonomy = cd82 (orbit-fire-paint). Distinguishing rules concrete; no overlap on apex/range cycle, parabolic-arc, mobile launcher. |
| 14 | Absent from prior-games/index.md | ✅ PASS | Closest priors bx84 (beam-mirror), vt6q (grapple-anchor), qn7w (pulse-chain), pf3w (wavefront), lq5x (lantern-cone). Distinguishing rules concrete in §9 of spec. |
| 15 | Distinguishing rules concrete (not vague) | ✅ PASS | All near-miss rules cite specific mechanics or geometry differences. |
| 16 | Win condition stated, testable | ✅ PASS | `len(targets_remaining) == 0 → next_level()`; predicate is `arc_end_cell == target_centre`. |
| 17 | Lose condition stated | ✅ PASS | `step_counter == 0 → lose()`. |
| 18 | Difficulty floor/ceiling — 4 bullets per level | ✅ PASS | (a) random-resistance, (b) human time, (c) planning depth, (d) step budget — all 4 stated for L1, L2, L3. L2/L3 planning-depth bullets name plausible-wrong alternatives + reasoning chain + heuristic-vs-witness divergence. |
| 19 | No hidden state — every mutable state has persistent visual cue | ✅ PASS | Power level → 3 visible launcher variants (1/2/3 dots). In-flight marble → animated white dot during fire phase. Targets remaining → ring sprites still rendered until consumed. Launcher position → sprite at (lx, ly). Step counter → HUD bar at row 0. |
| 20 | No low-resolution rendering | ✅ PASS | 64×64 native grid (no upscale). Launcher 6×6 with internal pattern (frame + dot row + interior). Targets 3×3 hollow rings. Shields 2×6 bars. Each primary sprite has shape AND palette differentiation. |
| 21 | UI teaches — sprite UI ≈ role | ✅ PASS | Launcher reads as "machine with charge level"; arc-preview-dots curve readably; targets read as "fitting destination" hollow rings; shields read as walls; wind reads as stippled vertical band. Identical visuals (3 launcher variants) share role differing only in dot count → reads as "same launcher, different state". |
| 22 | ACTION7 strict-undo or absent | ✅ PASS | ACTION7 NOT in `available_actions`. No undo verb claimed; the slot is correctly omitted (not overloaded). |

## Novelty (re-run on full spec)

- vs taxonomy: PASS. Closest is cd82 (fire-paint); cv5b's parabolic
  arc + mobile-launcher + apex/range cycle + barrier clearance are
  cumulatively distinctive.
- vs prior-games: PASS. Closest is bx84 (beam-mirror); cv5b's
  parabolic curve (vs straight beam) + power-cycle (vs mirror
  placement) + wind-deflection at L3 are distinguishing.
- Negative-similarity (vs bx84): 2/8 dimensions shared (level goal,
  lose condition); 6/8 distinct. Below the 3-of-8 reject threshold.
  PASS.

## Verdict
ALL CHECKLIST ITEMS PASS. NOVELTY VERIFIED. Transition to `implement`.
