# critique-pass — pj7k spec, revision 1

Re-checked the revised `mechanic-spec.md` against every item in
`design-constraints/checklist.md` plus the novelty rules.

| # | Check | Verdict |
|---|---|---|
| 1 | Sprite palette values in 0..15 (and -1 for transparent) | ✅ PASS — all sprites in §3 use values from {1, 4, 8, 9, 11, 12, 14, 15, -1}. |
| 2 | Universal scaffold conformance | ✅ PASS — §3 specifies sprite bank, §6 describes HUD widget class, §5 wires `available_actions`. |
| 3 | `available_actions` subset of [1..7] | ✅ PASS — `[1, 2, 3, 4, 5]`. |
| 4 | Exactly 3 `Level(...)` entries | ✅ PASS — §4 has L1, L2, L3 only. |
| 5 | ID 4 chars, lowercase, alphanumeric, not English, not reserved, not in prior-games | ✅ PASS — `pj7k`. |
| 6 | Mechanics draw only from `core-knowledge-priors.md`'s four categories | ✅ PASS — rolling = physics + objectness + topology; twist = geometry; locks = topology + objectness. |
| 7 | No letters / digits / clipart / cultural conventions | ✅ PASS — target hollow rings and lock plus-crosses are explicitly permitted by `forbidden-elements.md`; cube-face-strip layout is abstract. |
| 8 | At least TWO distinct mechanics in the environment | ✅ PASS — three (rolling-paint, twist, locks). |
| 9 | L1 tutorial: base dynamic system, reduced state, no on-screen text | ✅ PASS — cube + two targets only, no walls / locks. |
| 10 | L2 and L3 increase difficulty by composition, not size | ✅ PASS — same 4×4 grid; new mechanics added per level. |
| 10a | No hidden mechanics; strict-necessity for each | ✅ PASS — L1 mech count = 1, L2 = 2 (twist necessary because target (1,0)=14 forces a pre-east twist), L3 = 3 (locks necessary under the "sprite-becomes-wall-if-logic-removed" convention; targets behind locks unreachable). |
| 11 | Mechanic family absent from `taxonomy-of-25-games.md` | ✅ PASS — `rolling-cube-face-paint` is not in the table. |
| 12 | Mechanic family absent from `prior-games/index.md` | ✅ PASS — 8 priors enumerated; none use cube-rolling. |
| 13 | Distinguishing rule articulated for near-misses | ✅ PASS — §9 names ls20, re86, cn04 with concrete differences. |
| 14 | Win condition stated as a testable predicate | ✅ PASS — §7: every `target` cell's required sub-tag colour equals the paint colour at the same cell. |
| 15 | Lose condition stated | ✅ PASS — §8: step counter reaches zero. |
| 16 | Difficulty floor and ceiling per level | ✅ PASS — L1 (a-d), L2 (a-d), L3 (a-d) all filled; L2 names per-step reasoning chain; L3 names trivial heuristic ("always twist before every roll" defeated at step 6 of trace) AND commute test (swapping witness actions 4 ↔ 5 makes lock at (3, 0) reject). |

Novelty re-check on the FULL spec (not just the family name):

- vs. taxonomy: no description-level overlap with any of the 25
  reference games. NOVEL.
- vs. prior-games: no description-level overlap with any of the 8
  priors. NOVEL.
- Negative-similarity test: walked all 8 dimensions; no single
  prior shares 3+ dimensions. NOVEL.

**Verdict: PASS.** Transition to `implement`.
