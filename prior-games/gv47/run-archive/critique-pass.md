# critique-pass — gv47

Re-critique after revision v1 (wind_arrow → wind_strip). All checks
re-run on the updated `mechanic-spec.md`.

## Checklist (`design-constraints/checklist.md`)

- ✅ **1.** Every sprite uses palette 0..15 only. Roster values: {0, 2,
  3, 4, 8, 9, 10, 11, 14, 15} + transparent `-1` only inside the
  pre-revision `wind_arrow` (now `wind_strip`, all-`10`, no transparent).
- ✅ **2.** Spec describes the universal scaffold (imports → sprite
  bank → levels → constants → HUD widget → game class). Implementation
  in next state.
- ✅ **3.** `available_actions = [5, 6]` ⊆ `[1..7]`.
- ✅ **4.** EXACTLY 3 levels enumerated in §4 with the L1/L2/L3
  composition structure.
- ✅ **5.** Game ID `gv47` is 4 lowercase alphanumeric, not a word, not
  in the 25 reference IDs, not in `prior-games/index.md`.
- ✅ **6.** Mechanics draw only from objectness, geometry/topology,
  basic physics. No agentness, no acquired symbolism.
- ✅ **7.** No letters / digits-as-glyphs / clipart / cultural
  conventions. Revision v1 replaced `wind_arrow` with `wind_strip`
  (1×8 light-blue bar, no symbolic shape). Seed and target sprites
  are square frames around 1×1 pips — topology, not letterforms.
- ✅ **8.** Three distinct mechanics (M1 click-to-grow, M2 mix-at-
  frontier, M3 wind-biased growth) > 2 minimum.
- ✅ **9.** L1 establishes the base dynamic (M1 only); reduced state
  space (12×12, 1 seed, 1 target, simple wall column); no on-screen
  text.
- ✅ **10.** L2 and L3 each compose every mechanic available; not
  scaling grid size or item count alone.
- ✅ **10a.** L1 N=1 (M1 only, witness exercises M1). L2 N+1=2 (M1+M2,
  witness exercises both, mix is *strictly* required for the green
  target). L3 N+2=3 (M1+M2+M3, witness exercises all three, wind is
  *strictly* required to reach (10,10) within budget). Necessity is
  argued per-mechanic in each level subsection.
- ✅ **11.** Mechanic family `seed-grow-mix` absent from
  `taxonomy-of-25-games.md`; near-misses ft09 and dc22 distinguished
  with concrete rules in §9.
- ✅ **12.** Mechanic family absent from `prior-games/index.md`;
  near-miss lq5x distinguished in §9 with concrete rule (volatile
  cone vs persistent ring; ACTION5 steers vs combines).
- ✅ **13.** Concrete distinguishing rules stated for every flagged
  near-miss — none vague.
- ✅ **14.** Win condition stated as a testable predicate in §7
  (`_check_win` over all `target` sprites).
- ✅ **15.** Lose condition stated in §8 (`steps_remaining == 0`).
- ✅ **16.** Per-level (a)/(b)/(c)/(d) all four bullets present:
  - L1: random-resistance argued (Binomial calc); human time 30–60s;
    planning depth near-zero (per L1 rule); step budget 30 over an
    11-action witness, ~2.7×.
  - L2: random-resistance sub-percent; human ~2 min; planning depth
    NON-TRIVIAL with the per-step reasoning chain quoted ("To paint
    (6,7) green I need yellow and blue in contact near (6,7)…");
    step budget 50 over 12-action witness, ~4×.
  - L3: random-resistance astronomically small; human ~3 min;
    planning depth STRICTLY DEEPER than L2 with a named trivial
    heuristic that fails ("spam-grow then mix all-at-once") AND a
    witness-pair commute test (action 7 ↔ action 8 swap breaks
    purity of the mix events); step budget 80 (>L2's 50) over a
    26-action witness.

## Negative-similarity re-walk (`negative-similarity-check.md`)

Walked the 8 dimensions against each prior on the *fleshed-out* L1/L2/L3
spec. No prior shares ≥3 dimensions with gv47. Highest overlap is lq5x
at 1.5 (#4 step counter + half-#3 cover-cells-with-source-colour). PASS.

## Verdict

**NOVEL** vs taxonomy and prior-games index. **All 16 checklist items
+ 10a PASS.** Transition to `implement`.
