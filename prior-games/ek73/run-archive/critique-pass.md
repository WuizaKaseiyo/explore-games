# critique-pass — pass 2 of `mechanic-spec.md`

## Verdict: PASS — proceed to `implement`.

The v2 spec addresses the major issues from pass 1. L3's strict counterfactual necessity is now demonstrated for both clearer and warp. L1 makes wake load-bearing in the witness via the row-3-then-row-4 detour. L2's wrong-path defense is thinner than ideal but rests on step-budget tightness (35 vs 32 witness), which is a valid (if last-resort) difficulty-rules.md § 2d defense.

Below: one line per checklist item plus the novelty verdict.

| Item | Verdict | Note |
|---|---|---|
| 1 (palette 0..15) | ✅ | Sprites use 1, 4, 5, 6, 9, 10, 11, 12, 14 only (subset of 0..15). |
| 2 (universal scaffold) | ✅ | Implementation will follow `code/universal-scaffold.md`. |
| 3 (available_actions ⊆ [1..7]) | ✅ | `[1, 2, 3, 4]`. |
| 4 (exactly 3 levels) | ✅ | L1, L2, L3. |
| 5 (4-char ID, not reserved) | ✅ | `ek73`. |
| 6 (priors only) | ✅ | Objectness + topology, no symbols. |
| 7 (no letters/digits/clipart) | ✅ | Yellow cross, orange star, magenta-fade-glyph, green-asterisk, blue-rings — abstract shapes. |
| 8 (≥ 2 mechanics) | ✅ | 3 mechanics (walk-with-decay, clearer, warp). |
| 9 (L1 tutorial) | ✅ | L1 has 1 base mechanic, reduced state (16×16 logical), no on-screen text. |
| 10 (L2/L3 compose mechanics) | ✅ | L3 witness requires walk + clearer + warp simultaneously. |
| 11 (mechanic inheritance, +1/+2) | ✅ | L1=1, L2=2, L3=3. Each carries forward. |
| 12 (strict counterfactual necessity) | ✅ | Per-mechanic table: L3's clearer (vertical-branch trap) and warp (west-corridor dead-end) both fail closed. L1 wake is load-bearing in witness. L2 wrong-path defense via budget. |
| 13 (mechanic family absent from taxonomy) | ✅ | `wake-trail-evade` not in any of 25 reference families. |
| 14 (mechanic family absent from priors) | ✅ | Not in 27 prior-game rows. |
| 15 (distinguishing rules for near-misses) | ✅ | Five near-miss rows have concrete distinguishing rules (g50t, sk48, fz5j, wt39, zd7m). |
| 16 (win condition) | ✅ | All collectibles consumed. |
| 17 (lose condition) | ✅ | Step-on-wake / step-budget / soft-lock. |
| 18 (difficulty floor and ceiling) | ✅ (with caveat) | L1 (a)(b)(c)(d) clean; L2 (c) thin (budget-tightness defense); L3 (a)(b)(c)(d) clean with named greedy heuristic. |
| 19 (no hidden state) | ✅ | Wake-age via 3 distinct sprites; pads visible until consumed. |
| 20 (don't generate low-resolution) | ✅ | grid_size=(64,64), CELL_STRIDE=4, 4×4 sprites with internal patterns. |
| 21 (UI to teach) | ✅ | Sprite roles articulated; shape + palette differentiated per kind. |

Novelty verdict: **NOVEL** against all 25 taxonomy rows and all 27 prior-game rows.

## Visit count
This is critique_spec visit #2 of 10.
