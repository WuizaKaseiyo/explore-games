# critique-pass — round 3 (clean)

All three issues from rounds 1 & 2 are addressed in the current
`mechanic-spec.md`. Independent re-review of the spec on its own (not
reading round-1 / round-2 verdicts) confirms it passes 16/16 + 10a +
novelty + negative-similarity. Verbose checks below; one line per
checklist item.

## §3.4 compliance checklist

| # | Item | Verdict |
|---|---|---|
| 1 | Sprite palette in 0..15 (+ -1 transparent) | ✅ palette set `{1, 3, 4, 5, 10, 12, 14, -1}` |
| 2 | File structure matches universal-scaffold | ✅ imports → sprite bank → levels → constants → HUD widget → game class |
| 3 | `available_actions` ⊆ [1..7] | ✅ `[1, 2, 3, 4, 6]` |
| 4 | EXACTLY 3 levels, structured per composition-and-tutorial | ✅ L1 base (N=2), L2 +platform (N+1=3), L3 +anchor (N+2=4) |
| 5 | 4-char ID, lowercase alnum, not English, no collision | ✅ `kx14` not in 25-set or in priors {kf42, qz73} |
| 6 | Mechanics from core-knowledge-priors.md only | ✅ physics + objectness + geometry/topology |
| 7 | No letters, digits-as-glyphs, clipart, cultural conventions | ✅ all sprites abstract; UP=raise-water is a discoverable physical rule |
| 8 | At least 2 distinct mechanics in environment | ✅ 4 mechanics across 3 levels |
| 9 | L1 = tutorial with reduced state space, no on-screen text | ✅ 1 ball, 1 target, no platforms, no anchor; both base verbs required |
| 10 | L2 / L3 increase difficulty by COMPOSITION, not just scaling | ✅ L2 adds topology (platform); L3 adds asymmetry (anchor) — neither is "more of the same" |
| 10a | One new mechanic per level; every listed mechanic exercised by witness | ✅ L1 witness uses M1+M2; L2 uses M1+M2+M3 (platform forces deflection); L3 uses M1+M2+M3+M4 (anchor enables swap that tilt alone cannot) |
| 11 | Mechanic family absent from taxonomy | ✅ `tide-tilt-buoyant` not in 25-row taxonomy |
| 12 | Mechanic family absent from prior-games index | ✅ not in {kf42, qz73}; concrete distinguishing rules vs each |
| 13 | Concrete distinguishing rules for any near-miss | ✅ §9 has rules for sp80, g50t, m0r0, ar25, ka59, kf42, qz73 |
| 14 | Win condition stated | ✅ §7 — colour-strict ball-on-target-ring |
| 15 | Lose condition stated | ✅ §8 — step-counter exhaustion (single fail mode) |
| 16 | Per-level: random-resistance + human-tractable + planning depth | ✅ L1 near-zero planning; L2 deliberate multi-step; L3 strictly deeper than L2 (greedy "raise + tilt" defeated by the swap requirement) |

## Witness-trace verification

| Level | Witness count claimed | Witness count traced | Match |
|---|---|---|---|
| L1 | 9 actions | 4 ACTION1 + 5 ACTION4 = 9 | ✅ |
| L2 | 15 actions | 3 ACTION1 + 2 ACTION4 + 3 ACTION1 + 7 ACTION4 = 15 | ✅ |
| L3 | 21 actions | 1 ACTION6 + 4 ACTION1 + 5 ACTION3 + 1 ACTION6 + 1 ACTION6 + 2 ACTION2 + 5 ACTION4 + 2 ACTION1 = 21 | ✅ |

## Novelty + negative-similarity (full spec)

- Positive similarity-check (per `similarity-check.md`): NOVEL against every row in `taxonomy-of-25-games.md` and `prior-games/index.md`. Closest taxonomy near-misses (sp80, g50t, m0r0, ar25, ka59) and both priors (kf42, qz73) have concrete distinguishing rules in §9; deep-analysis cross-reference confirms the rules hold against the deeper view.
- Negative-similarity (per `negative-similarity-check.md`): no prior shares ≥ 3 of the 8 dimensions; specifically dimensions 6 (visual signature), 7 (pixel grain), 8 (core dynamic) — the three named principles — diverge cleanly. The kf42→vh68 cautionary tale (small coloured pawns on dark walled grid) is explicitly avoided.

## Algorithmic documentation

§6 re-projection pseudocode now uses the corrected helper names
(`_max_platform_row_in_col_in_range` for rising, `_min_platform_row_in_col_in_range`
for falling) with explicit row-coord-convention comments. An
implementation that copies the pseudocode literally will produce the
correct platform-block semantics, consistent with the L1+L2+L3 witness
traces.

## Verdict

**PASS.** Transition to `implement`.
