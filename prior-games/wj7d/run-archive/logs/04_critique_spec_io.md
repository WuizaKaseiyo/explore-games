# Step #04: critique_spec (visit #1)

## Inputs Consumed
- mechanic-spec.md (from #03)
- skills/design-constraints/checklist.md (21 items)
- skills/design-constraints/difficulty-rules.md
- skills/design-constraints/forbidden-elements.md
- skills/mechanic-novelty/{similarity-check,negative-similarity-check}.md
- prior-games/index.md + ar25/cn04/cd82/pz4t deep-references in spirit

## Work — adversarial walk of all 21 checklist items

1. **Palette 0..15 + (-1) only.** ✅ (palette uses 0,4,7,8,9,10,11,14,15,-1)
2. **Universal scaffold.** ✅ (will follow on implement)
3. **available_actions ⊂ [1..7].** ✅ ([1,2,3,4,5,6])
4. **Exactly 3 levels.** ✅
5. **4-char ID, opaque, not collision.** ✅ (`wj7d`)
6. **Mechanics from core-knowledge-priors.** ✅ (geometry+objectness)
7. **No letters/digits/clipart/cultural conventions.** ✅ (cross,
   ring, line, halo — abstract topological shapes; cross with
   white accent does NOT read as Red Cross logo because of
   colour bg + small accent + non-Red-Cross proportions)
8. **At least TWO mechanics.** ✅ (already 2 at L1: MOVE+FOLD)
9. **L1 tutorial reduced state space, no on-screen text.** ✅
10. **L2/L3 increase via composition.** ✅
11. **Mechanic inheritance + +1-or-+2 per level.** ✅ (L1=2,
    L2=3 [+1], L3=5 [+2])
12. **Strict counterfactual necessity per mechanic.** ✅ (each
    of L1×2 + L2×3 + L3×5 = 10 mechanic-level pairs has
    a concrete reason naming a cell/sprite/rule)
13. **Mechanic family absent from taxonomy.** ✅ (fold-crease-
    overlay not in 25-game taxonomy)
14. **Mechanic family absent from prior-games index.** ✅
15. **Distinguishing rule for near-misses.** ✅ (§9)
16. **Win condition stated.** ✅ (§7)
17. **Lose condition stated.** ✅ (§8 — step exhaust + unwinnable)
18. **Difficulty floor and ceiling.** ⚠️ ISSUE — L2 and L3
    planning-depth (c) bullets cite discovery-stage missteps as
    "trivial heuristic that fails", violating the stage-
    conflation guard in `difficulty-rules.md` § 3.d.
19. **No hidden state.** ✅ (selection halo + crease colour +
    visible orientation H/V + visible position + covered cells
    rendered)
20. **Don't generate low-resolution.** ✅ (grid 64×64 native;
    6×6 stamps with internal accent; 4-px arrow step does not
    upscale; rich pixel detail)
21. **UI to teach.** ✅ (mirror relationship between stamp and
    matching shadow visually obvious; crease bisects field
    suggesting axis-of-symmetry; halo + crease-yellow show
    selection)

## Novelty re-check on the full spec

- Taxonomy walk: ar25 (continuous mirror-ghost vs discrete
  consume-fold), cn04 (rotate-in-place vs reflect-across-axis),
  cd82 (paint-wedge vs reflect-stamp), pz4t (per-piece local
  anchor vs global axis crease) — all distinguishing rules
  hold in the fleshed-out spec.
- Prior-games walk: bx84 (per-step beam propagation vs one-shot
  stamp commit) and other 33 priors — none uses
  fold/reflect/crease as the core verb.
- Negative similarity (7 dimensions): vs ar25 — divergent on
  6 (palette), 7 (pixel grain — 6×6 patterned stamps vs ar25
  small pieces), 8 (core dynamic — discrete commit vs
  continuous slide). 3 shared (1, 3, 4 — universal). Pass.
  No prior reaches 3+ shared on heavy dimensions.

## Verdict

⚠️ FAIL on item 18 (issues #1 and #2 in critique-revisions.md;
plus a minor #3 about per-level data dict explicitness).

Transition: back to write_spec.

## Deliverables Produced
- critique-revisions.md: 3 issues + concrete fixes.

## Notes
- Items 1-17 + 19-21 + novelty all clean.
- Issue #1 is the heaviest fix (L2 layout reshape to enforce
  ordering); issue #2 is a paragraph-rewrite plus a numerical
  trace; issue #3 is a 5-line addition.
- This is visit #1 of #4. Plenty of revision budget left.
