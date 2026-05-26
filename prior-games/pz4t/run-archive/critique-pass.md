# Critique pass — pz4t (visit 1 of max 5)

All 16 checklist items + 10a + novelty + negative-similarity
re-check.

1. ✅ Palette only 0..15 (+ -1).
2. ✅ Universal scaffold structure (will be verified at implement).
3. ✅ `available_actions = [5, 6, 7]` ⊂ [1..7].
4. ✅ Exactly 3 Level entries.
5. ✅ ID `pz4t` — 4 lowercase alphanumeric, not a word, not in
   reserved or priors.
6. ✅ Mechanics from §3.4 priors only (objectness + basic geometry).
7. ✅ No letters/digits/clipart/cultural conventions. Components
   are abstract bar / L / S / Z / T multi-cell shapes; targets
   are dim-grey shadow cells; HUD is a depleting bar.
8. ✅ ≥ 2 distinct mechanics (anchor-place, rotate, flip — three).
9. ✅ L1 is tutorial: 10×10, single mechanic, no on-screen text,
   solvable in 4 actions; mechanic is required by the witness.
10. ✅ L2/L3 add mechanics, not just scale.
10a. ✅ Strict necessity:
    - L1: removing anchor-place ⇒ no movement ⇒ unsolvable.
    - L2: removing rotation ⇒ vertical-bar component cannot fit
      horizontal target ⇒ unsolvable.
    - L3: removing flip ⇒ Z-tetromino cannot become S-tetromino
      (Z has 180° symmetry; rotations of Z are {Z, Z90}; neither
      is S). The L3 red component is Z and the red target is S;
      strict necessity holds.
11. ✅ Family `anchor-pivot-place` not in taxonomy.
12. ✅ Family not in `prior-games/index.md` (10 entries, none match).
13. ✅ Distinguishing rules cited for sb26 (taxonomy) and ng52
    (prior).
14. ✅ Win condition stated (each component fitted = bbox cells
    equal target shadow cells).
15. ✅ Lose: step counter exhaustion.
16. ✅ Difficulty floor and ceiling per level (4 bullets each):
    - L1: random-resistance ✓, ~60s ✓, near-zero planning ✓,
      step budget 16 = 4× witness ✓.
    - L2: random ✓, ~2min ✓, multi-step planning chain explicitly
      named (5-step per-component chain) ✓, budget 28 = 4× ✓.
    - L3: random ✓, ~3min ✓, strictly deeper (flip not reducible
      to rotation, named heuristic "always rotate never flip"
      defeated, named commute pair: actions 2 and 3 of red Z
      witness — flip then place vs place then flip — non-
      commutative because flip-with-nothing-held is a no-op) ✓,
      budget 40 ≥ 28 ✓.

## Novelty re-check

Walked taxonomy + 10 priors against the full spec. Closest match
is sb26 (`tile-place-commit`); distinguishing rule (free 2D
translation by anchor vs discrete slot index) is concrete.
Negative-similarity ≤ 2 dimensions on named principles for every
prior.

## Verdict

**ALL CHECKS PASS.** Transition to implement.
