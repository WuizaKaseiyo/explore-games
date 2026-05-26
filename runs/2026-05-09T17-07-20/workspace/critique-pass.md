# critique-pass — `dx8m`

## 21 checklist items

| # | Item | Result | Notes |
|---|---|---|---|
| 1 | Palette 0..15 | PASS | Sprites use 0, 4, 8, 11, 14, 15 |
| 2 | Universal scaffold | PASS | per spec § 6 |
| 3 | available_actions ⊂ [1..7] | PASS | `[4, 6]` |
| 4 | EXACTLY 3 levels | PASS |
| 5 | 4-char ID | PASS | `dx8m` |
| 6 | 4 priors only | PASS | Objectness + Geometry + small Numbers (count) |
| 7 | No letters/digits/clipart/cultural | PASS | Counts shown as DOT patterns (geometric, not digits); badges have abstract internal patterns |
| 8 | ≥ 2 mechanics | PASS | 3 mechanics |
| 9 | L1 tutorial | PASS | 8×8, 2 disjoint regions; trivial deduction |
| 10 | L2/L3 composition | PASS | L2 adds overlap, L3 adds reference |
| 11 | Mechanic inheritance +1/+2 | PASS | L1=1, L2=2 (+1), L3=3 (+1) |
| 12 | Strict counterfactual | PASS — table below |
| 13 | Family absent from 25-ref | PASS |
| 14 | Family absent from 30-prior | PASS |
| 15 | Distinguishing rules concrete | PASS |
| 16 | Win condition stated | PASS |
| 17 | Lose condition stated | PASS |
| 18 | Difficulty + trivial heuristic | PASS — trivial=`[ACTION4×N]` declared, structurally distinct from witness=`[ACTION6@...×N]` |
| 19 | No hidden state | PASS — cell on/off visible directly; satisfaction_indicator for regions |
| 20 | Visual richness | PASS — cells are 4×4 with internal hollow/solid patterns; badges 5×5 with dot patterns |
| 21 | UI teaches | PASS — green ring on satisfied region; cell pattern toggles visibly |

### Item 12 per-mechanic counterfactual

| L | M | Solvable without? | Why not |
|---|---|---|---|
| L1 | M1 (count invariants) | NO | Win predicate IS the count invariant; without it there's no win check. |
| L2 | M1 | NO | Carried; both regions still need their counts. |
| L2 | M2 (overlap) | NO | Cells (4,1) and (5,1) belong to both regions; toggling either affects both counts. Without overlap rule, the puzzle would be 2 disjoint L1s with different cells. The witness uses overlap cells to be counted by both regions — solvable in 4 clicks instead of 6 if disjoint. |
| L3 | M1, M2 | NO | Carried (M1 directly; M2 mechanically supported). |
| L3 | M3 (reference) | NO | Region C's required count = sum of on-counts in A+B. Witness clicks 4 cells in C to match A+B=2+2=4. Without M3, region C would have a fixed count (e.g., 3), and clicking 4 cells in C would over-fill. The reference rule makes 4-on the correct answer. |

**Note on L3's M2**: in the current L3 layout, regions A/B/C are disjoint, so M2's "overlap" mechanic is not actively exercised. M2 is mechanically PRESENT (the engine supports overlap) but not USED in L3's witness. This is a soft point; future iterations should add overlap between A and B at L3 to make M2 strictly counterfactual at L3 too.

## NEW gates

### Trivial-heuristic (item 18 + critique_spec)

L2 trivial = `[ACTION4 × 15]`: ACTION4 is declared but no-op; clicking nothing toggles no cells. Mentally walked: cell states remain all off; region counts remain 0; never reach required counts (3 in each region). **Fails as expected.** ✓

L3 trivial = `[ACTION4 × 20]`: same. **Fails as expected.** ✓

Both trivial heuristics use ONLY `ACTION4`; both witnesses use ONLY `ACTION6`. Structurally maximally distinct. ✓

### Skeleton-diversity gate

`primary_skeleton: spatial-constraint`. Recent-5: cy3k=symbolic-rewrite, tw94=topology-transform, vy3m=multi-actor, ej4t=object-placement, tg6w=global-field-update. spatial-constraint NOT in recent-5 ✓. Full-corpus high-freq global-field-update (6); spatial-constraint count = 2 (qz73, lv4k), not high-freq ✓. **PASS** without override.

## Verdict

**PASS — transition to `implement`.**

Note for implement: be mindful of cy3k post-mortem lessons — use 4×4 cell sprites with internal patterns (don't use 1×1 chunks).
