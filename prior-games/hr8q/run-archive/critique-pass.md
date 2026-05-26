# Critique pass — hr8q

(After in-place revision of L3 to use the *three-input formula*
mechanic — the original *finite-inventory-with-multi-target* pick
failed strict necessity at item 10a because removing the
inventory constraint left the witness functioning unchanged. The
revised L3 strictly requires the third slot to produce blue.)

## Checklist (`design-constraints/checklist.md`)

1. ✅ All sprite pixels in 0..15 ∪ {-1}. Spec §3 explicitly lists
   palette values per sprite; no glyphs.
2. ✅ Spec §3-§7 align with `code/universal-scaffold.md`'s
   sections. Implementation will follow the scaffold.
3. ✅ `available_actions = [5, 6]` ⊂ `[1..7]`.
4. ✅ EXACTLY 3 levels (L1, L2, L3) — see §4.
5. ✅ `hr8q` — 4 lowercase alphanumeric chars; not in 25
   reference IDs; not in `prior-games/index.md`; not an English
   word.
6. ✅ Mechanics use only **objectness** and **basic
   geometry/topology** priors (`core-knowledge-priors.md`). No
   physics, no agentness; no other categories.
7. ✅ No letters, digits-as-glyphs, real-world clipart, or
   cultural conventions. The slot widget is purely topological:
   adjacent input squares → adjacent result square. No "+", "=",
   or arrow shapes.
8. ✅ Three distinct mechanics: pair-blend-and-commit,
   intermediate-as-ingredient, three-input formula. ≥2.
9. ✅ L1 tutorial: one mechanic active (pair-blend-and-commit),
   two ingredients only, single target, no on-screen text. Random
   policy can stumble through.
10. ✅ L2 and L3 increase difficulty by COMPOSING mechanics. L2
    requires both pair-blend AND intermediate-as-ingredient (see
    §4 L2 necessity). L3 requires all three. Neither L2 nor L3
    is "L1 with a bigger grid".
10a. ✅ Mechanics counts: L1=1 (pair-blend-and-commit); L2=2
    (+intermediate-as-ingredient); L3=3 (+three-input formula).
    Strict necessity confirmed independently for each mechanic
    in the per-level *Necessity per mechanic* sub-bullet of §4:
    - L1 pair-blend: only path to consume the target.
    - L2 pair-blend: every commit (incl. the chain's first step)
      is a pair-blend.
    - L2 intermediate: target maroon unreachable from primary
      pairs; the only chain requires distilling purple from a
      mismatched commit.
    - L3 pair-blend: chain step 1 (distilling purple) IS a pair
      commit.
    - L3 intermediate: blue's only recipe `(purple, pink, yellow)`
      requires purple; purple is not a primary; the only path is
      distillation.
    - L3 three-input: blue is not produced by any pair recipe;
      remove the third slot ⇒ no blue ⇒ unsolvable.
    No hidden mechanics — every mechanic listed for a level is
    exercised by that level's witness.
11. ✅ The mechanic family `pair-blend-recipe` does NOT appear
    in `taxonomy-of-25-games.md` (verified by reading every
    row's `mechanic_family`).
12. ✅ The mechanic family `pair-blend-recipe` does NOT appear
    in `prior-games/index.md` (current rows: kf42
    `tether-pawn-cycle`, qz73 `radial-cycle-lock`, kx14
    `tide-tilt-buoyant`, qb84 `bead-lift-swap`, lq5x
    `lantern-cone-illuminate`, gv47 `seed-grow-surround-dissolve`).
13. ✅ The closest near-miss in priors (gv47, also a colour-mix
    primitive) has a concrete distinguishing rule articulated in
    §9 and in `mechanic-pick.md`. The negative-similarity walk
    over 8 dimensions yields 1/8 overlap (only the universal
    step-counter axis); below the 3-of-8 rejection threshold.
14. ✅ Win condition (§7): `len(self.target_queue) == 0`. Holds
    across all 3 levels. Concrete & testable.
15. ✅ Lose condition (§8): `self.steps_used >= self.max_steps`
    while the queue is non-empty. Concrete & testable. There is
    no other lose path.
16. ✅ Per-level *Difficulty justification* with all four
    bullets ((a) random-resistance, (b) human time, (c) planning
    depth, (d) step budget) is present for L1, L2, L3 in §4. L2
    names a concrete per-step reasoning chain; L3 names a
    concrete trivial heuristic that fails (the *two-slot
    heuristic*) plus an adjacent witness-pair commute test
    (swap actions 6,7) that breaks the witness solution.

## Novelty re-check (full-spec, not just family name)

- Walked positive `similarity-check.md` against all 25 reference
  rows + 6 prior-games rows. Closest near-misses (sb26, su15,
  tn36, gv47) all have concrete distinguishing rules in §9.
- Negative-similarity 8-dimension walk against gv47: 1/8 overlap.
  Against other priors: ≤ 1/8 each. PASS.
- L2 and L3 stay within the same family — they don't drift toward
  a different prior. The third-slot mechanic at L3 doesn't echo
  any reference game's "third action" pattern (e.g. tn36 chains
  click-instructions on a runway, not a third formula slot;
  sb26's slots are a guess board, not a recipe input).

**VERDICT: NOVEL on both the positive and negative similarity
checks.**

## Structural sanity

- 3 levels exactly.
- Action mapping concrete (§5).
- Win/lose are testable predicates (§7, §8).
- Sprite roster is implementable (§3).
- HUD widgets are concrete (§6).

## Transition

PASS — proceed to `implement`.
