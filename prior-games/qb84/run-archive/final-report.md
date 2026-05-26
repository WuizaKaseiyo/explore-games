# Game generation final report

## Generated game
- **ID**: qb84
- **Source**: `prior-games/qb84/qb84.py`
- **Metadata**: `prior-games/qb84/metadata.json`
- **Lines of code**: 519

## Mechanic

A serpentine chain of coloured beads needs to be recoloured to
match a target sequence. The player has a logical cursor that
selects one bead at a time; ACTION3/4 step the cursor backward and
forward along the chain. ACTION1 ("lift") swaps the active bead's
colour with whichever peg sprite occupies the bead's "above" slot,
and ACTION2 ("drop") does the same for the "below" slot. The level
wins when every bead's colour matches the target reference strip.
The only failure is exhausting a per-level step counter. Level 2
introduces sticky pegs that lock the bead's colour after a single
swap. Level 3 introduces pair pegs whose swap propagates the
partner peg's colour into the chain neighbour, and a sticky-trap
that punishes the trivial "lift on every wrong bead" heuristic.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Lift: swap active bead's colour with its above-slot peg (if any). Sticky peg locks the bead. Pair peg propagates partner colour into chain neighbour. No-op (no step) if no peg or bead locked. |
| ACTION2 | Drop: same as ACTION1 but for the below-slot peg. |
| ACTION3 | Cursor index decrement (clamped 0). |
| ACTION4 | Cursor index increment (clamped len-1). |

## Levels
- **L1 (base dynamic, N=2 mechanics):** 6-bead S-curve, 3 plain pegs. Witness exercises both lift (above-peg) and drop (below-peg). 24-step budget, 8-action witness.
- **L2 (+sticky-peg lock, N+1=3):** 8-bead extended S-curve, 5 pegs with 2 sticky. Witness uses lift, drop, AND sticky-locking via two distinct sticky pegs. 32-step budget, 12-action witness.
- **L3 (+pair-peg propagation, N+2=4):** 10-bead double-S, 7 pegs including a pair-A/pair-B propagating duo and a sticky-trap. Witness uses lift, drop, sticky-locking, AND pair-peg propagation; commuting actions 8 and 9 of the witness breaks the level. 60-step budget, 14-action witness.

## Novelty note

- **Closest taxonomy entry**: tr87 (tape-rewrite-rule) — also pure-arrow with horizontal layout. Distinguishing rule: tr87 cycles a card's intrinsic symbol identity at a fixed slot via UP/DOWN; qb84 PHYSICALLY displaces a bead between the chain and an adjacent peg and SWAPS their colours. tr87 has no perpendicular displacement and no colour transfer to a separate sprite.
- **Closest prior-game entry**: qz73 (radial-cycle-lock) — both have a structured array layout and lock concept. Distinguishing rule: qz73's verb is ACTION5 = "advance every unlocked tip one slot CW" (global rotation operator); qb84's verb is ACTION1/2 = "displace ONE bead perpendicular to chain" (per-bead local swap). Different action-space ([5,6] vs [1,2,3,4]) and different layout topology (radial 8-slot vs serpentine chain).

## Index update

One row appended to `prior-games/index.md`:

```
| qb84 | bead-lift-swap | Bead-Lift Swap-Sequence — pure-arrow chain navigation; lift/drop swaps the active bead's colour with an above/below peg; sticky and pair pegs at L2/L3. | 2026-04-29T02:37:20Z | (autonomous) |
```
