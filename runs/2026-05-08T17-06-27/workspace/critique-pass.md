# critique-pass — `tw94`

## 21 checklist items

| # | Item | Result |
|---|---|---|
| 1 | Palette 0..15 | PASS |
| 2 | Universal scaffold | PASS |
| 3 | available_actions ⊂ [1..7] | PASS — `[1, 2, 3, 4]` |
| 4 | EXACTLY 3 levels | PASS |
| 5 | 4-char ID | PASS — `tw94` |
| 6 | 4 priors only | PASS — Objectness + Geometry/topology |
| 7 | No letters/digits/clipart/cultural | PASS — abstract sprites only |
| 8 | ≥ 2 mechanics | PASS — 3 (M1, M2, M3) |
| 9 | L1 tutorial | PASS — single corridor + horizontal wrap; reduced state |
| 10 | L2/L3 composition | PASS — L2 adds vertical wrap; L3 adds row-parity selectivity |
| 11 | Mechanic inheritance +1/+2 | PASS — L1=1, L2=2 (+1), L3=3 (+1) |
| 12 | Strict counterfactual | PASS (table below) |
| 13 | Family absent from 25-ref | PASS |
| 14 | Family absent from 28-prior | PASS |
| 15 | Distinguishing rules concrete | PASS |
| 16 | Win condition stated | PASS |
| 17 | Lose condition stated | PASS |
| 18 | Difficulty + trivial heuristic | PASS (per L2/L3 declared, structurally distinct) |
| 19 | No hidden state | PASS — wrap_indicator pip sprites at wrappable-edge cells |
| 20 | Visual richness | PASS |
| 21 | UI teaches | PASS — pips at edges show which axes wrap; player learns row-parity by trial |

### Item 12 per-mechanic counterfactual

| L | M | Solvable without? | Why not |
|---|---|---|---|
| L1 | M1 (H wrap) | NO | Wall at (2, 4) blocks west push of crate; east push reaches (7, 4) at boundary; without wrap, push at boundary fails; only east-wrap delivers crate to target at (1, 4) via (7→0). |
| L2 | M1 | NO | Crate_a at (10, 4) with wall at (5, 4) blocking direct west; east-wrap is shortest delivery. |
| L2 | M2 (V wrap) | NO | Crate_b at (4, 10) with wall at (4, 5) blocking direct north; south-wrap (vertical) is the only delivery path. |
| L3 | M1 | NO | Same as L2's crate_a (on EVEN row 4 — wraps OK at L3). |
| L3 | M2 | NO | Same as L2's crate_b (on EVEN col 4 — wraps OK at L3). |
| L3 | M3 (row-parity) | NO | Crate_c at (3, 5) on ODD row 5 — horizontal wrap disabled at L3. Player MUST push crate_c vertically to row 4 (even, wraps), wrap east, push south back to row 5 at target_c. Direct east-wrap on row 5 fails (boundary blocks since odd row no wrap). |

## NEW gate (CHECK_TRIVIAL_FAILS)

- L2 trivial = `[ACTION4 × 20]` (always press right): pushes player east, eventually pushes crate_a via east-wrap to target_a; crate_b never moved (different col, no vertical wrap triggered by ACTION4). L2 score does not advance to 2 (only target_a covered, target_b not). ✓ Mentally walked: trivial diverges from witness (witness uses ACTION2 to push crate_b south).
- L3 trivial = `[ACTION4 × 30]`: same as L2 (crate_a delivered via east-wrap on row 4 even — wraps); crate_b on col 4 even (vertical wrap) but never touched (different row); crate_c on row 5 odd (no H wrap) — push east hits boundary, fails. Crate_b and crate_c not delivered. ✓

## Verdict

**PASS — transition to `implement`.**
