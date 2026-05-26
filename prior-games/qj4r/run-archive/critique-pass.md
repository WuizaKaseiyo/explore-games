# Critique pass — round 2

## Checklist verdict

| # | Check | Result |
|---|---|---|
| 1 | Palette ⊆ {0..15, -1} | ✅ {0,1,2,3,4,12,13,15} only |
| 2 | Universal scaffold | ✅ to be enforced in implement |
| 3 | available_actions ⊆ [1..7] | ✅ [1,2,3,4] |
| 4 | Exactly 3 levels | ✅ |
| 5 | 4-char lowercase ID, not in reserved/priors | ✅ qj4r |
| 6 | Priors only | ✅ geometry/topology + objectness |
| 7 | No letters/digits/clipart/cultural | ✅ all sprites are abstract patterns |
| 8 | ≥ 2 mechanics | ✅ M1, M2, M3 |
| 9 | L1 tutorial reduced state, no on-screen text | ✅ 1 piece + 1 target |
| 10 | L2/L3 compose mechanics | ✅ each adds 1 new + carries forward |
| 11 | +1-or-+2 per level | ✅ L1=1, L2=1+1=2, L3=2+1=3 |
| 12 | Strict counterfactual necessity (per-mechanic table below) | ✅ |
| 13 | Family absent from taxonomy | ✅ no fold/contract entry |
| 14 | Family absent from priors | ✅ no prior with central-axis-fold dynamic |
| 15 | Distinguishing rule articulated | ✅ §9 vs ar25, m0r0, bx84, wt39, tg6w, pz4t, qm4t |
| 16 | Win condition stated | ✅ §7 (per-colour count + per-decoy count predicate) |
| 17 | Lose stated | ✅ §8 (step budget) |
| 18 | Difficulty floor/ceiling per level | ✅ all 4 bullets per level (random-resistance, human time, planning depth, step budget); budgets monotone 8/14/22 |
| 19 | No hidden state — visible cue per state mutation | ✅ merge → piece_orange_merged distinct pattern; decoy removal → sprite disappears; active region contraction → active_floor mutates |
| 20 | Not low-resolution (rich pixel pattern) | ⚠️ borderline — 4×4 sprites carry ≤ 4 pixels of internal pattern; recommend bumping to 6×6 sprites at implement time if rendered frames look coarse |
| 21 | UI teaches (sprite role guessable from screen) | ✅ same-colour piece+target pairs cue role; merged piece's distinct pattern signals merge; decoy's swirl signals "different" |

## Per-mechanic counterfactual necessity (item 12)

| Level | Mechanic | Solvable without triggering M? | Why not |
|---|---|---|---|
| L1 | M1 (fold) | no | Piece movement is fold-only; without M1 the piece never leaves (2,4). |
| L2 | M1 | no | Piece movement is fold-only. |
| L2 | M2 (same-colour merge) | no | Win predicate requires `count(orange pieces) == 1`; level starts with 2 oranges; only M2's collapse rule reduces the count. |
| L3 | M1 | no | Piece movement is fold-only. |
| L3 | M2 (same-colour merge) | no | Win predicate requires `count(orange pieces) == 1`; level starts with 2 oranges; only M2 collapses. |
| L3 | M3 (decoy cleanup) | no | Win predicate requires `count(grey decoys) == 0`; only M3's cleanup rule (piece-on-decoy coincidence after a fold) removes a decoy. |

All three mechanics are TRANSFORMATION mechanics whose distinguishing behaviour is the state mutation they cause. Each is *required to be triggered at least once* by every winning path because the win predicate's invariants cannot otherwise be satisfied.

## Novelty re-check (full-spec)

- **ar25** (taxonomy): re-confirmed distinguishing rule — qj4r contracts the playfield per fold; ar25 never does. qj4r's pieces transform (merge/cleanup); ar25's pieces just walk.
- **m0r0** (taxonomy): qj4r's "mirror" applies once per fold to the entire playfield; m0r0's mirror is per-pawn axis-flipped continuous motion. Distinct.
- **bx84, wt39, tg6w, pz4t, qm4t** (priors): all distinct on core dynamic, action verb, and visual signature.
- **Negative similarity check** re-walked on the L3 fleshed-out spec — no prior shares 3 dimensions of the heavy {6, 7, 8}.

VERDICT: **PASS** — proceed to implement.

(Caveat: item 20 borderline. Consider bumping sprite size from 4×4 to 6×6 in implement if rendered output reads as too coarse; will be self-checked during smoke test.)
