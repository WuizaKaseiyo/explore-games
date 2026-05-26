# critique-pass — yh3p (round 2, all clear)

Re-walked checklist items 1-22 + similarity-check + negative-
similarity-check on `mechanic-spec.md` revision 2. All previously-
flagged issues resolved. Spec ready for `implement`.

## Resolution of round-1 issues

| Issue | Status | Where verified |
|---|---|---|
| 1. Inconsistent L3 wall layout | ✅ FIXED | §4 L3 Layout — single coherent description: vertical wall (8, 0..6), horizontal wall (0..6, 8); gaps at (8, 7), (7, 8), (8, 8) all explicitly named. Witness routes verified against this layout. |
| 2. `bud_notched` reads as letter | ✅ FIXED | §3 `bud_notched` redesigned as closed-ring flower with 2-pixel yellow stamen extending out the intake side; rotated silhouette is "flower-with-tab", not letter-shaped. Verified by mentally rotating the pixel array at all 4 cardinals. |
| 3. Tip activity after auto-bloom unspecified | ✅ FIXED | §5 action mapping explicitly: "Auto-bloom-on-entry preserves tip activity". §4 L2 M2-necessity argument re-derived under this rule. |
| 4. L3 M2 necessity argument | ✅ FIXED | §4 L3 M2-row leads with the dormancy-after-bloom argument (M2 required regardless of wall topology because each successful M3 sets tip dormant); topology argument retained as supporting evidence. |
| 5. L1 frame visual sparseness | ✅ ADDRESSED (soft) | §3 adds `soil_texture` decorative INTANGIBLE background sprite; L1/L2/L3 layouts list it as an optional decoration. |

## Checklist items 1-22

| # | Item | Verdict |
|---|---|---|
| 1 | Palette values 0..15 (and -1 transparent) | ✅ |
| 2 | Universal scaffold structure | ✅ |
| 3 | `available_actions` ⊆ [1..7] | ✅ `[1, 2, 3, 4, 5, 6]` |
| 4 | EXACTLY 3 levels | ✅ |
| 5 | 4-char ID, opaque, not in reserved/index | ✅ `yh3p` |
| 6 | Mechanics from core priors | ✅ objectness + topology + light geometry |
| 7 | No letters/digits/clipart/cultural | ✅ (Issue 2 fix: bud_notched redesigned) |
| 8 | ≥ 2 mechanics | ✅ M1 + M2 + M3 |
| 9 | L1 tutorial, base system, no on-screen text | ✅ |
| 10 | L2/L3 increase difficulty by composition | ✅ |
| 11 | Mechanic inheritance + 1-or-+2 rule | ✅ L1=1, L2=2 (+1), L3=3 (+1); all carried |
| 12 | Strict counterfactual necessity table + enumeration | ✅ |
| 13 | Mechanic family absent from taxonomy | ✅ |
| 14 | Mechanic family absent from prior-games index | ✅ |
| 15 | Concrete distinguishing rule for similar-sounding | ✅ |
| 16 | Win condition stated | ✅ `len(buds_remaining) == 0` |
| 17 | Lose condition stated | ✅ `step_bar.current_steps <= 0` |
| 18 | Difficulty floor + ceiling per `difficulty-rules.md` | ✅ all 4 bullets per level |
| 19 | No hidden state | ✅ visibility-cue table |
| 20 | Don't generate low-resolution game | ✅ (soil_texture addition + sprite internal pattern) |
| 21 | UI to teach (sprite ≈ role; identical-visual ≈ shared role) | ✅ |
| 22 | ACTION7 strict-undo or absent | ✅ omitted |

## Novelty re-check

- Family-level: `vine-branch-bloom` does not match any taxonomy or
  prior-game family tag. ✅
- Description-level: re-walked the closest 4 taxonomy entries and
  closest 7 prior-game entries; each near-miss has a concrete
  distinguishing rule (cited in §9 of the spec).
- Negative-similarity 8-dimension test: max overlap with any single
  prior remains 2 dimensions. Below the 3-dimension reject
  threshold. ✅

## Witness routes verified

L1 witness: 12 actions, fits 24-step budget (2.0×). ✅

L2 witness: 22 actions, fits 50-step budget (2.27×). ✅

L3 witness: 40 actions, fits 100-step budget (2.5×). ✅

Each witness route was traced cell-by-cell against the cleaned-up
layout; all routes use only open cells; all bud arrivals happen
with the correct intake-matching tip facing.

## Verdict

**PASS.** Transition to `implement`. critique_spec visit count
after this entry: 2 of 10; 8 entries remain budgeted but unused.
