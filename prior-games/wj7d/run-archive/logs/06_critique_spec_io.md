# Step #06: critique_spec (visit #2)

## Inputs Consumed
- mechanic-spec.md (revised clean version from #05)
- skills/design-constraints/checklist.md (21 items)
- skills/design-constraints/difficulty-rules.md
- skills/design-constraints/forbidden-elements.md
- skills/mechanic-novelty/{similarity-check,negative-similarity-check}.md
- prior-games/index.md

## Work — adversarial walk

Re-walking checklist 1–21 against the revised spec. Issues #1–3
of critique #1 have been addressed.

1. **Palette 0..15 + (-1).** ✅ (0,4,7,8,9,10,11,14,15 + -1)
2. **Universal scaffold.** ✅ (followed in implement)
3. **available_actions ⊂ [1..7].** ✅
4. **Exactly 3 levels.** ✅
5. **4-char ID.** ✅ (`wj7d`)
6. **Mechanics from core-knowledge-priors.** ✅
7. **No letters/digits/clipart/cultural conventions.** ✅
8. **At least TWO mechanics.** ✅
9. **L1 tutorial reduced state space.** ✅
10. **L2/L3 increase via composition.** ✅
11. **Mechanic inheritance + +1-or-+2.** ✅
12. **Strict counterfactual necessity.** ✅ (per-mechanic table
    implicit in "Necessity per mechanic" subsections)
13. **Mechanic family absent from taxonomy.** ✅
14. **Mechanic family absent from prior-games.** ✅
15. **Distinguishing rule for near-misses.** ✅
16. **Win condition stated.** ✅
17. **Lose condition stated.** ✅
18. **Difficulty floor and ceiling.** ✅ NOW PASSES — L2's
    "harder-first by movement count" + collision rejection is
    a genuine post-discovery planning failure; L3's "click
    convenient crease cell" with col 32/40/16 alternatives is
    a genuine post-discovery planning failure (the player
    knows the mechanic but hasn't computed the unique correct
    pivot column 33).
19. **No hidden state.** ✅
20. **Don't generate low-resolution.** ✅ (64×64 native;
    6×6 stamps with internal accents)
21. **UI to teach.** ✅

## Per-mechanic counterfactual necessity table

| Level | Mechanic | Solvable without M? | Concrete reason |
|---|---|---|---|
| L1 | M1 MOVE-stamp | no | Stamp at (8,8) folded → reflected at cols 8..13 rows 49..54; shadow at cols 24..29 rows 45..50; zero overlap. |
| L1 | M2 FOLD-commit | no | `cells_covered` only mutates via FOLD. |
| L2 | M1 MOVE-stamp | no | Both stamps' starting reflections have zero overlap with their respective shadows. |
| L2 | M2 FOLD-commit | no | Same as L1. |
| L2 | M3 SELECT-among-stamps | no | At level start no stamp selected; arrows are no-ops; player must click each stamp before acting. |
| L3 | M1 MOVE-stamp | no | Red stamp at y=12; required source y=16 for fold to land at shadow row 16. Without DOWN, fold rows 12..17 ∩ shadow 16..21 = 2 rows partial coverage. |
| L3 | M2 FOLD-commit | no | Same as L1. |
| L3 | M3 SELECT-among-stamps | no | Stamps and crease both require explicit ACTION6 click to act on. |
| L3 | M4 MOVE-CREASE | no | Blue at (40,8) reflected across H@31 → rows 53..58; blue shadow at rows 41..46; zero overlap. Crease must move to row 27 for blue to be coverable. |
| L3 | M5 RE-ORIENT-CREASE | no | Red shadow at (45, 16); H crease at any row preserves x; red x stays 16 ≠ 45. Vertical crease (re-orient required) is the only way to flip x. |

## Plausible alternate strategies — independent enumeration

For L2:
- Strat A: fold red first via "harder-first" greedy heuristic.
  Walked above: collision rejects the 4th DOWN; ACTION5 from
  y=16 produces partial coverage → lose.
- Strat B: fold both stamps without selecting (just press ACTION5).
  Arrows are no-ops without selection (per § 5); ACTION5 with
  no stamp selected is also no-op (per § 5). Player burns budget.
- Strat C: fold blue first but skip movement. Fold from (24, 24)
  → reflected rows 33..38; blue shadow at rows 41..46; zero
  overlap. Blue consumed → lose.
- Strat D (witness): fold blue first WITH movement, then red.

Only D wins; A, B, C all lose. ≥ 1 plausible-but-wrong strategy
named per the post-discovery rule. ✓

For L3:
- Strat A: fold both stamps with default crease. Blue: zero
  overlap (rows 53..58 vs 41..46). Lose immediately.
- Strat B: move crease only (don't re-orient). Blue covered;
  red folds with H crease anywhere, preserves x=16, shadow x=45,
  no overlap. Red consumed → lose.
- Strat C: re-orient crease at convenient col (32, 40, 16, etc.).
  Red folds; partial or no overlap; shadow not fully covered →
  red consumed → lose. (This is the named heuristic.)
- Strat D (witness): move crease H to row 27, fold blue,
  re-orient at col 33, fold red.

Only D wins. ✓

## Novelty re-check

Re-walked the fleshed-out spec against:
- Taxonomy entries `ar25, cn04, cd82, pz4t, re86, sb26, lp85,
  vc33, qx7p, ft09, sk48, sp80, m0r0, wa30, ka59` — all
  distinguishing rules from § 9 of spec hold; mechanic family
  is absent from taxonomy.
- Prior-games entries `bx84, qz73, pj7k, kf42, kx14, qb84,
  lq5x, gv47, hr8q, ng52, vn8d, fz5j, kn58, wt39, zk9p, rk7x,
  gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w, tg6w, vd3g,
  jd4q, ek73, tm5x, qx7p, kj82, nb6t, qm4t, qn7w, zw91, fb7t`
  — none match the wj7d core verb (consume-by-mirror-fold
  across a movable axis).
- Negative similarity (7 dimensions) vs ar25 (closest):
  divergent on 6 (palette: stamp/shadow pairs in pink/light-
  blue), 7 (pixel grain: 6×6 patterned stamps), 8 (core
  dynamic: discrete consume-by-fold). Pass.

## Verdict

✅ **PASS** on all 21 checklist items + novelty.

Transition: → implement.

## Deliverables Produced
- critique-pass.md
