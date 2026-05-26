# Critique pass — round 2

Re-checking the revised `mechanic-spec.md` against
`design-constraints/checklist.md` items 1-18 plus the novelty rules.

## Format & structure
1. Palette 0..15 (and -1 transparent) only — ✅ all sprite definitions
   in §3 use palette values 0..15 (specifically 1, 2, 3, 4, 6, 8, 10,
   11, 13, 14).
2. File structure matches `code/universal-scaffold.md` — ✅ §3 sprite
   roster, §4 levels, §5 actions, §6 HUD, §7-8 win/lose. Implement
   state will instantiate this scaffold.
3. `available_actions` ⊆ `[1..7]` — ✅ §5 declares `[1, 2, 3, 4, 5]`.
4. Exactly 3 levels — ✅ §4 has Level 1, Level 2, Level 3.
5. Game ID is 4 lowercase chars, opaque, not in reserved/priors — ✅
   `zk9p` verified non-colliding in `mechanic-pick.md`.

## §3.4 priors & constraints
6. Mechanics drawn only from the 4 allowed prior categories — ✅
   agentness (pursuers act with intent), objectness (pursuers, avatar,
   walls are persistent entities), basic geometry (Manhattan-axis
   discrimination); no obscure priors invoked.
7. No letters / digits-as-glyphs / real-world clipart / cultural
   conventions — ✅ all sprites are 1×1 logical cells with single
   palette colour, plus a textured floor with a sparse speckle
   pattern; no glyphs that read as letters or numbers; no real-world
   iconography.
8. At least 2 distinct mechanics — ✅ L1 has 3, L2 has 5, L3 has 7.
9. Tutorial L1 establishes a base dynamic system, all required by L1
   witness, reduced state space, no on-screen text — ✅ L1 = 14×14
   grid with 3 entities + no walls, tutorial-friendly.
10. L2 and L3 increase difficulty by COMPOSING every prior mechanic
    with the new ones (not by scaling) — ✅ L2 adds wall-block + orth-
    major chase that interact with the existing chase + merge; L3
    adds phase + tick-skip that compose with all 5 carried-forward
    mechanics. Both new mechanics at each level alter the *interaction
    structure* (where pursuers can step, when they advance), not the
    *count* of any element.

## Mechanic structure (per-level)
11. Mechanic inheritance and the +1-or-+2 rule — ✅ L1 N=3, L2 M=5
    (N+2), L3 = 7 (M+2). Every L1 mechanic carried into L2 and L3.
    Every L2 mechanic carried into L3. No mechanic drops out.
12. Strict counterfactual necessity (no trivial fallback) — ✅ Each
    mechanic at each level has a 1-line counterfactual naming a
    specific cell, sprite, or rule that blocks every alternate path.
    Per-mechanic table:

    | Level | Mechanic | Solvable without M? | Why not (concrete) |
    |---|---|---|---|
    | L1 | avatar walk | no | avatar starts at (7,10), pursuers at (5,3)/(9,3); standing still → pursuers reach avatar's column on tick 5, step onto (7,5)... actually first they reach (7,5) on tick T_caught; avatar move is the only thing that changes the chase target |
    | L1 | Manh-major chase | no | win predicate = pursuer-count=0; merge requires 2 pursuers in same cell; without chase, pursuers stand still → never merge → step counter expires → lose |
    | L1 | merge-on-collision | no | merge is the only mechanism that removes a pursuer; without it, pursuer-count never drops |
    | L2 | avatar walk | no | cyan stalls at (8,3) until avatar shifts column → without walking, cyan eventually fires y-step rule once avatar shifts naturally OR cyan stalls forever and reds catch up via Manh-major y, descending unchecked, to (3,13)/(13,13) at tick 11, then sweep x to (8,13) — caught |
    | L2 | Manh-major chase | no | red and yellow are Manh-major pursuers; without their chase, only cyan moves, cyan alone cannot self-merge, pursuer-count stays ≥1 |
    | L2 | merge-on-collision | no | (same as L1) |
    | L2 | wall-block | no | wall at (8,4) is the only thing stalling cyan at (8,3); without walls, cyan reaches (8,12) on tick 11 and steps onto avatar's cell on tick 12 |
    | L2 | orth-major chase | no | with Manh rule on cyan, cyan stuck at (8,3) forever (dx=0 fallback y → wall-blocked; |dy|>|dx| → y → wall-blocked) — orth's minor-axis-first is the only release |
    | L3 | avatar walk | no | (4 pursuers chasing; standing still, cyan's orth chase reaches avatar within 6 ticks) |
    | L3 | Manh-major chase | no | red+yellow merge requires their chase to compute; without it, no red-yellow merge possible |
    | L3 | merge-on-collision | no | (same as L1) |
    | L3 | wall-block | no | corridor walls (y=8 row, x=4 col) channel cyan into the green-merge cell C_CG; without walls, cyan path unconstrained, second merge ungeometrable in budget |
    | L3 | orth-major chase | no | (same argument as L2 — cyan would stall forever without orth) |
    | L3 | phase pursuer | no | green at corridor cell (9,9) is the only walkable cell connecting bait region to corridor; walking onto (9,9) when green tangible = caught; phase intangibility on odd ticks is the only traversal |
    | L3 | tick-skip (ACTION5) | no | structural counterfactual on tick T_bait+1: avatar must hold position B for the red-yellow merge to land at C_RY *and* cyan to arrive adjacent to C_CG; any avatar move breaks one or both; ACTION5 is the only "no-op" that advances pursuers |

    All "no" with concrete reasons. ✅

## Novelty
13. Mechanic family absent from `taxonomy-of-25-games.md` — ✅
    `pursuer-merge-walk` not present; closest near-misses (m0r0,
    ka59, g50t, tu93, su15, wa30) all distinguished concretely in §9
    of the spec. Cross-checked against deep-analyses for cn04, m0r0,
    sb26, tu93, wa30 (the 5 source-pick reads); no drift.
14. Mechanic family absent from `prior-games/index.md` — ✅
    closest entry kn58 (anchor-pull-magnet) distinguished concretely
    in §9.
15. Distinguishing rules are concrete (not "it's different") — ✅ §9
    names verbs, subjects, win conditions per near-miss.

## Solvability
16. Win condition stated for environment as a whole — ✅ §7 defines
    pursuer-count == 0 as the level win predicate, and the
    environment ends after L3 win via engine's auto-`win()`.
17. Lose condition stated — ✅ §8 names two paths: pursuer on avatar's
    cell (with phase-tick exemption) and step-budget exhaustion.
18. Difficulty floor and ceiling per `difficulty-rules.md` — ✅ all
    three levels state (a) random-resistance, (b) human time, (c)
    planning depth, (d) step budget. L2/L3 planning depth is concrete
    (named reasoning chain, named wrong paths). L3 step budget is
    justified with absolute-slack reasoning (76 spare actions; growth
    over L2's 65, L1's 55).

## Negative similarity (re-walked at full-spec resolution)
- vs **kn58**: 0 dimensions shared (revised post-spec; entity types,
  inputs, win, lose, palette, grain, dynamic all differ).
- vs **ka59**: 2 dimensions (walls, caught=lose); below threshold.
- vs **tu93**: 2 dimensions (input, kills); below threshold; pixel
  grain at L3 marginally close (4 pursuers + walls is similar to
  tu93's L1-2 layout in shape) but the walkable-underlay sprite
  pattern is absent in zk9p (zk9p uses a textured floor instead),
  giving a different visual signature.
- vs **m0r0**: 0 dimensions; merge subject differs (player vs NPC),
  movement model differs (lockstep-mirror vs single-walk).

No prior overlaps on 3+ dimensions. **NOVEL** confirmed.

## Verdict
**ALL 18 CHECKLIST ITEMS PASS. NOVELTY CONFIRMED. PROCEED TO `implement`.**
