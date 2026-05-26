# Critique pass — ng52

## Checklist (`design-constraints/checklist.md`)

1. ✅ All sprite pixels in 0..15 ∪ {-1}. Sprites use blue (9),
   purple (15), off-black (4), background (2), and -1 transparent.
2. ✅ Spec §3-§7 align with `code/universal-scaffold.md`.
3. ✅ `available_actions = [5, 6]` ⊂ `[1..7]`.
4. ✅ EXACTLY 3 levels (L1, L2, L3) — see §4.
5. ✅ `ng52` — 4 lowercase alphanumeric chars; not in 25 reference
   IDs; not in `prior-games/index.md` (kf42, qz73, kx14, qb84,
   lq5x, gv47, hr8q); not an English word.
6. ✅ Mechanics use only **objectness** and **basic
   geometry/topology** priors (`core-knowledge-priors.md`). No
   physics, no agentness.
7. ✅ No letters, digits-as-glyphs, real-world clipart, or
   cultural conventions. Bins are hollow rectangles; signatures
   are solid-colour 1×L runs; objects are abstract non-convex
   pixel clusters.
8. ✅ Three distinct mechanics: place-and-commit-classify,
   multi-stick compositional bin, selective placement with
   distractors.
9. ✅ L1 tutorial: one mechanic active, 3 single-stick
   single-colour bins, 3 small objects (3, 4, 5 blue pixels each),
   no on-screen text. Random policy can stumble through the
   tutorial in this design space, satisfying §3.4's "tutorial may
   be solubly random" expectation.
10. ✅ L2 and L3 increase difficulty by COMPOSING mechanics. L2
    requires combining 2 objects per bin to satisfy multi-colour
    signatures. L3 adds the distractor-recognition layer. Neither
    enlarges the grid or adds "more obstacles".
10a. ✅ Mechanic counts: L1=1; L2=2 (+ multi-stick compositional
    bin); L3=3 (+ selective placement under distractors). Strict
    necessity per the spec's per-level *Necessity per mechanic*
    bullet:
    - L1 place-and-commit: only path to fire `next_level()`.
    - L2 multi-stick compositional bin: pool is designed so no
      single object's multiset matches any bin's signature;
      every bin needs ≥2 objects. Removing the mechanic ⇒
      unsolvable.
    - L3 selective placement: pool total pixels = `{blue:18,
      purple:5}`; bin signature total = `{blue:13, purple:5}`.
      The 5-blue surplus is exactly the distractor O7. Removing
      the "leave some in pool" mechanic (forcing every object to
      be placed) ⇒ no partition fits ⇒ unsolvable.
    No hidden mechanics: every mechanic listed for a level is
    exercised by that level's witness.
11. ✅ Family `multiset-signature-classify` not in
    `taxonomy-of-25-games.md`.
12. ✅ Not in `prior-games/index.md`.
13. ✅ Closest near-misses (sb26, hr8q, su15, tn36) each have
    concrete distinguishing rules in §9 of the spec and full
    rules in `mechanic-pick.md`. The negative-similarity walk
    against hr8q (load-bearing recent prior) is 0/8 substantive
    + 1/8 universal (step counter) — well below the 3-of-8
    rejection threshold.
14. ✅ Win condition (§7): every bin's pixel-colour multiset
    equals its declared signature multiset, on commit. Concrete
    & testable.
15. ✅ Lose condition (§8): `steps_used >= max_steps` while
    unsolved. Concrete & testable. Failed commits snap back, do
    NOT trigger lose.
16. ✅ Per-level *Difficulty justification* with all four bullets
    is present for L1, L2, L3 in §4. L2 names a per-step
    reasoning chain. L3 names a concrete trivial heuristic that
    fails (the *exhaustive-placement* heuristic — placing the
    distractor in any bin breaks the commit) plus an adjacent
    witness-pair commute test (swap actions 4 and 5) that breaks
    the 13-action witness solution.

## Novelty re-check (full-spec)

- Walked positive `similarity-check.md` against all 25 reference
  rows + 7 prior-games rows. Closest near-misses (sb26, su15,
  tn36, hr8q) all have concrete distinguishing rules in §9.
- Negative-similarity walk vs hr8q (the load-bearing recent
  prior): 0/8 substantive + 1/8 universal = NOVEL.
- L2 and L3 do not drift toward any other family — multi-stick
  signatures and distractor recognition are *additions* in the
  same partition-classification family, not pivots into a new
  surface look.

**VERDICT: NOVEL on both checks.**

## Structural sanity

- 3 levels exactly.
- Action mapping concrete (§5).
- Win/lose are testable predicates (§7, §8).
- Sprite roster is implementable (§3).
- HUD widget is concrete (§6).
- Witnesses are written out action-by-action with click coords.

## Transition

PASS — proceed to `implement`.
