# critique-pass — `vy3m`

## 21 checklist items

| # | Item | Result |
|---|---|---|
| 1 | Palette 0..15 | PASS |
| 2 | Universal scaffold | PASS (in spec § 6) |
| 3 | available_actions ⊂ [1..7] | PASS — `[1, 2, 3, 4, 5]` |
| 4 | EXACTLY 3 levels | PASS |
| 5 | 4-char ID | PASS — `vy3m` |
| 6 | 4 priors only | PASS — Objectness + Agentness |
| 7 | No letters/digits/clipart/cultural | PASS — pusher/puller/stomper differ in body palette only (no letter forms); all sprites abstract |
| 8 | ≥ 2 mechanics | PASS — 3 mechanics (M1, M2, M3) |
| 9 | L1 tutorial, base mechanic | PASS — Pusher only, single push, no lose hazard |
| 10 | L2/L3 composition | PASS — L2 adds class-swap+pull; L3 adds class-swap-extended+chain-push |
| 11 | Mechanic inheritance +1/+2 | PASS — L1=1, L2=2 (+1), L3=3 (+1) |
| 12 | Strict counterfactual | PASS (table below) |
| 13 | Family absent from 25-ref | PASS |
| 14 | Family absent from 27-prior | PASS |
| 15 | Distinguishing rules concrete | PASS |
| 16 | Win condition stated | PASS |
| 17 | Lose condition stated | PASS |
| 18 | Difficulty + trivial heuristic | PASS (new gate — see below) |
| 19 | No hidden state | PASS — ActiveClassHud cues active class colour |
| 20 | Visual richness | PASS — every sprite has internal pattern |
| 21 | UI teaches | PASS — 3 distinct class colours; crates orange; targets yellow disc |

### Item 12 per-mechanic counterfactual table

| L | Mechanic | Solvable without M? | Why not |
|---|---|---|---|
| L1 | M1 push | NO | Walls confine to row-4 corridor; only push moves crate east to target. |
| L2 | M1 push | NO | Push lane has only Pusher's verb to deliver crate_a east. |
| L2 | M2 class-swap+pull | NO | Pull lane vertically isolated from push lane; Puller starts in pull lane; pull is the only verb that moves crate_b west to target_b (push from west would require pusher east of crate, no path). |
| L3 | M1 push | NO | Push lane same as L2. |
| L3 | M2 class-swap+pull | NO | Pull lane same as L2. |
| L3 | M3 chain-push (Stomper) | NO | Chain lane: crate_c1 + crate_c2 adjacent in row 12; pushing crate_c1 east meets crate_c2 in cell beyond; non-Stomper push fails on chain; only Stomper's chain-push-of-2 propagates. |

### NEW gate — Trivial-heuristic for items 18 + critique_spec common failure mode

**L2 trivial heuristic** = `[ACTION4 × 12]`. Mentally walked against L2 layout:
- Pusher delivers crate_a after 5 ACTION4s (3 walks + 2 pushes? Let me recount: pusher (1,2) → (2,2) → (3,2) → (4,2) [crate, push to (5,2)] → (5,2) [crate, push to (6,2)] → (6,2) [crate, push to (7,2)] → (7,2) [crate, push to (8,2)=target]. That's 7 ACTION4s for crate_a).
- ACTION4 ×5 more: pusher pushed past target, drives east into walls (col 9, 10 = walls or boundary).
- Pull lane is sealed; Puller never activated. Crate_b stays at (5, 7). Target_b not covered.
- L2 does NOT advance. ✓

**L3 trivial heuristic** = `[ACTION4 × 15]`. Same logic: Pusher delivers crate_a; subsequent ACTION4s no-op; Puller and Stomper never activated; crate_b and crate_c stay put. ✓

Structurally distinct from witness:
- L2 witness includes `ACTION5` (cycle) and `ACTION3` (west pulls); trivial has only `ACTION4`.
- L3 witness includes 2× `ACTION5` and 2× `ACTION3`; trivial has only `ACTION4`.

Prose for why-fails references specific cells / classes / sealed-lanes. Concrete, not abstract.

## Negative-similarity check

vs **ka59**: shared dim 1 (avatar+crates+targets), 4 (universal step-budget). 2 shared. Under threshold.
vs **mr5q**: shared dim 1, 4. Different on 2 (no autonomous walking), 5 (different cast — no pawn-flip), 8 (different core dynamic — class-as-control vs polarity-flip). 2 shared. Under threshold.

## Verdict

**PASS — transition to `implement`.**

Trivial heuristic gate (item 18 new) cleanly distinguishes from witness. Layout has multiple-lane structure; no single corridor that defeats planning. Counterfactual per mechanic is concrete (not waved).
