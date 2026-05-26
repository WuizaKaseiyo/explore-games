# Critique-pass for `nb6t` — visit 2/10

| # | Item | Verdict |
|---|------|---------|
| 1 | Palette 0..15 + -1 transparent | ✅ {0, 4, 6, 8, 9, 11, 12, 15} |
| 2 | Universal scaffold | ✅ (deferred to implement) |
| 3 | `available_actions` ⊆ [1..7] | ✅ [1, 2, 3, 4, 5, 6] |
| 4 | Exactly 3 levels | ✅ |
| 5 | 4-char opaque ID, no collision | ✅ `nb6t` |
| 6 | Mechanics from §3.4 priors | ✅ Objectness + geometry + kinematic-physics |
| 7 | No glyphs / letters / clipart / cultural conventions | ✅ |
| 8 | ≥ 2 distinct mechanics | ✅ M1 change-active-hinge, M2 rotate, M3 length-adjust, M4 carry-and-drop |
| 9 | L1 establishes base, no text, all required | ✅ M1 + M2 both witness-required |
| 10 | L2 + L3 difficulty by composition | ✅ Same grid; new mechanics layered |
| 11 | Mechanic inheritance + +1-or-+2 | ✅ L1 = 2, L2 = 3, L3 = 4 |
| 12 | Strict counterfactual necessity | ✅ Per-mechanic table at each level (L1 M1+M2; L2 M1+M2+M3; L3 M1+M2+M3+M4) |
| 13 | Mechanic family absent from taxonomy | ✅ `hinge-chain-reach` not in taxonomy |
| 14 | Mechanic family absent from prior-games | ✅ Not in 30-entry index |
| 15 | Distinguishing rules concrete | ✅ vs s5i5, cn04, qz73, gx7m, pj7k |
| 16 | Win condition stated | ✅ Tip-on-target (L1, L2); object-on-drop-zone (L3) |
| 17 | Lose condition stated | ✅ Step-counter exhaust |
| 18 | Difficulty floor and ceiling (a, b, c, d) per level | ✅ All four bullets present per level; random-resistance near-zero across all 3 |
| 19 | No hidden state | ✅ Active-halo, tip-carry-halo, step bar all persistent |
| 20 | Not low-resolution | ✅ 64×64 grid, scale=1, pixel-rich sprite designs |
| 21 | UI teaches | ✅ Hinge=ring, halo=highlight, tip=dot, target=ring, drop-zone=colour-matched ring |

**Novelty verdict**: NOVEL for every taxonomy and prior-games row. Negative-similarity check passes on the heavy axes for the closest neighbours (s5i5, qz73, cn04). 

**Transition**: → `implement`.
