# Critique pass — vp6h, round 2

**Decision: PASS. Transition to `implement`.**

## Round-1 issues — all resolved

| # | Issue | Resolution verified |
|---|---|---|
| 1 | L3 phase 4 witness traversed col-13 bot-pillar | ✅ Phase 4 re-routed via col 11; new path (7,9)→(11,9)→(11,4)→(13,4); avatar's 2×2 footprint never overlaps a pillar; pickup at (13,4) verified double-shaded under top@cols 0..4 + bot@cols 10..14 (col 13 outside top-range; bot-pillar at col 13 rows 8..10 occludes upward bot-rays from reaching row 4). |
| 2 | L2 phase 1 off-by-one | ✅ Phase 1 = `ACTION4, ACTION1` = 2 actions, avatar (1,13)→(2,12); footprint at (2,12) overlaps A and is top-shaded (col 2 outside default cols 5..9). Total L2 = 25 actions. |
| 3 | L1 off-by-one | ✅ Witness = `ACTION4 ×5, ACTION1` = 6 actions, avatar (2,13)→(7,12); pickup at (7,12) where col-7 pillar (rows 3..7) occludes the cell from above. |
| 4 | Crystal palette green→cultural | ✅ Crystal pixels now `[[10, 15], [15, 10]]` (light-blue + purple). Purple has no cultural-go/safe association. |
| 5 | L2 col-2 pillar inconsistency | ✅ col-2 pillar removed from L2 layout. M2 necessity now grounded in two distinct facts: (a) col 6 has no pillar so its lit-state is purely a function of lantern position; (b) collecting A first is required because sliding leftward to expose col 6 covers col 2 (no pillar) → A becomes lit. Both facts hold under the revised layout. |
| 6 | BlockingMode unspecified | ✅ §3 sprite roster appended: pillars use `BlockingMode.PIXEL_PERFECT` (default; equivalent to BOUNDING_BOX since pillars have no -1 cells). Crystals and lanterns use `InteractionMode.INTANGIBLE`. |
| 7 | L2 stage-conflation | ✅ Resolved by Issue 5 fix; the "plausible-but-wrong slide-first" path is now genuinely wrong because col 2 has no pillar and goes lit under top@cols 0..4. |

## Checklist re-walk on revised spec

| # | Item | Verdict |
|---|---|---|
| 1 | Sprite palette in 0..15 plus -1 | ✅ All sprites use values from {0,1,2,3,4,5,6,10,11,12,13,15} ∪ {-1}. |
| 2 | Universal scaffold structure | ✅ Spec is compatible with universal-scaffold.md (final structural verification deferred to implement). |
| 3 | `available_actions` subset of [1..7] | ✅ `[1, 2, 3, 4, 6]`. |
| 4 | Exactly 3 levels | ✅. |
| 5 | 4-char ID not reserved | ✅ `vp6h`. |
| 6 | Mechanics from priors | ✅ objectness + geometry + topology. |
| 7 | No letters/digits/clipart/cultural | ✅ post Issue-4 fix. |
| 8 | At least two distinct mechanics | ✅ M1, M2, M3. |
| 9 | L1 base dynamic system | ✅ M1 alone, fixed lantern, 1 pillar, 1 crystal, no on-screen text. |
| 10 | L2/L3 increase difficulty by composing | ✅ L2 = M1+M2 firing simultaneously; L3 = M1+M2+M3. |
| 11 | Mechanic inheritance and +1-or-+2 | ✅ N=1, N+1=2, +1=3. |
| 12 | Strict counterfactual necessity per mechanic | ✅ post Issue-5 fix. L1 M1 borderline-acceptable per the "tutorial-discovery" interpretation; L2 M1 and M2 grounded in concrete cell/pillar facts; L3 all three grounded. |
| 13 | Family absent from taxonomy | ✅ shadow-cast-collect. |
| 14 | Family absent from prior-games | ✅. |
| 15 | Distinguishing rule for similars | ✅ §9 + revision-1 mechanic-pick.md cross-references. |
| 16 | Win condition | ✅ `crystals_remaining == 0` per level. |
| 17 | Lose condition | ✅ `step_counter <= 0`. |
| 18 | Difficulty floor and ceiling | ✅ all four bullets per level; L2 planning-depth justification names heuristic (slide-first), wrong path consequence (A becomes lit), witness reasoning chain (defensive ordering); L3 names trivial heuristic (greedy reactive sliding, ~10-15 wasted actions vs witness pre-positioning), divergence (witness pre-positions both lanterns; greedy slides reactively after walk-onto-unsafe). Budget ratios: L1 6/40 (6.7×), L2 25/70 (2.8×), L3 25/120 (4.8×). |

## Novelty re-check on full revised spec

Re-grounding against `mechanic-novelty/similarity-check.md` and `negative-similarity-check.md`:

- **Taxonomy near-misses unchanged.** The mechanics M1, M2, M3 are
  unchanged in substance from revision 0. Distinguishing rules vs
  lq5x, ar25, ka59, m0r0, sp80, etc. remain valid.
- **Prior-games near-misses unchanged.** Distinguishing rules vs
  lq5x, bx84, lf52, kn58, gv47, fz5j remain valid.
- **Negative-similarity walk vs lq5x level_1.png unchanged.** Heavy
  axes (visual signature, pixel grain, core dynamic) still diverge:
  - vp6h's L1 with the col-7 pillar will render as a mostly-bright
    16×16 grid (top-lantern over cols 5..9; cols 5,6,8,9 lit; cols
    0..4 and 10..15 dark; col 7 has a vertical strip dark below row
    7) — fundamentally different from lq5x's mostly-dark level_1
    with bright cone.

**Verdict: NOVEL.**

## Verdict

The revision-1 spec passes all 18 checklist items and the novelty
tests. Transition to `implement`.
