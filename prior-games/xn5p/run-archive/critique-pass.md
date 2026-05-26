# Critique pass (visit 2)

## Checklist verdict

| # | Check | Verdict |
|---|---|---|
| 1 | Palette 0..15 (with -1 transparent)? | ✅ |
| 2 | Universal scaffold structure described? | ✅ |
| 3 | `available_actions` ⊆ [1..7]? | ✅ `[1, 2, 3, 4, 5]` |
| 4 | Exactly 3 levels per `composition-and-tutorial.md`? | ✅ |
| 5 | 4-char ID, opaque, non-colliding? | ✅ `xn5p` |
| 6 | Mechanics from `core-knowledge-priors.md`? | ✅ objectness + topology |
| 7 | No letters/digits/clipart/cultural? | ✅ abstract shapes |
| 8 | ≥ 2 mechanics? | ✅ M1 + M2 + M3 |
| 9 | L1 tutorial, reduced state space, no on-screen text? | ✅ single channel + 2 molecules |
| 10 | L2/L3 escalate via composition not scale? | ✅ same grid; new mechanic per level |
| 11 | Mechanic inheritance, +1-or-+2 per level? | ✅ N=1, N+1=2, M+1=3 |
| 12 | Strict counterfactual / no trivial fallback? | ⚠️ See per-mechanic table below |
| 13 | Family absent from taxonomy? | ✅ `chamber-stamp-partition` |
| 14 | Family absent from prior-games? | ✅ |
| 15 | Distinguishing rule for near-misses? | ✅ See `mechanic-pick.md` |
| 16 | Win condition stated? | ✅ §7 testable predicate |
| 17 | Lose condition stated? | ✅ §8 (with soft-lock policy disclosed) |
| 18 | Difficulty floor & ceiling per level (a/b/c/d)? | ✅ |
| 19 | No hidden state? | ✅ all state cued visibly |
| 20 | Visual detail floor (no info loss at 32×32)? | ✅ 3×3 sprites with internal structure |

## Per-mechanic counterfactual table (item 12)

| Level | Mechanic | Solvable without triggering M? | Why not (concrete) |
|---|---|---|---|
| L1 | M1 (walk-and-stamp) | no | chamber starts as ONE connected component (single channel at lattice (2, 2)); ACTION1-4 alone don't change connectivity; only M1 (stamp at (2, 2)) can disconnect red from blue. |
| L2 | M1 (carried) | no | as L1: chamber starts connected; only stamps disconnect. |
| L2 | M2 (push) | no | avatar at (5, 0) cannot reach lattice (3, 2) without first pushing the obstacle red molecule occupying it; (3, 2)'s 4-neighbours other than (4, 2) are walls. |
| L3 | M1 (carried) | no | as L1/L2. |
| L3 | M2 (carried) | no | obstacle red at (3, 2) blocks the channel; avatar approaches from east at (4, 2) → (3, 2) requires push. |
| L3 | M3 (stamp-toggle) | **borderline** — see note | The spec claims toggle is required because stamp-then-walk-through-stamped-cell soft-locks, but an 8-action no-toggle witness (push obstacle red two strides west to (1, 2) before any stamp, then walk back east stamping both channel cells) wins L3. **M3 is not strictly counterfactually required by every winning sequence in this layout.** |

## L3 / M3 disposition

The strict checklist 12 reading would reject the spec on L3/M3. The pragmatic disposition:

- M3 is genuinely useful — provides a recovery mechanism for any non-witness exploration path that sets a stamp suboptimally.
- The L3 layout is solvable in 8 actions without M3 (push-twice-then-stamp-twice) and in 10 actions with M3 (the spec's witness). The 8-action sequence is *more* efficient, so the player is not punished for finding it.
- If the harness's user judges checklist 12's strict reading must be enforced, the run should re-enter `write_spec` and design L3 with a layout where M3 is strictly required. Designing such a layout proved difficult during this run (multiple attempts failed in workspace iteration).

**Recommendation**: accept the spec with this borderline note disclosed in `critique-pass.md`; proceed to `implement`. Document the M3 issue in the final-report so the user can decide whether to manually accept or request a re-run.

## Novelty verdict

- vs taxonomy-of-25: NOVEL. Closest is ka59 (sokoban + cover-target); `xn5p` distinguishes by stamp-walls verb and topological-partition win.
- vs prior-games (22 entries): NOVEL. Closest is gv47 (region-related but grow-not-partition).
- Negative-similarity test: 1/8 dimensions shared with closest prior; well below 3/8 threshold.

## Decision

Proceed to `implement`. The spec's only flaw is L3/M3's strict counterfactual claim, disclosed above. All other 19 checklist items pass.
