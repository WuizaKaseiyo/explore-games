# Game generation final report — Run #2

## Generated game

- **ID**: vy3m
- **Source**: `prior-games/vy3m/vy3m.py`
- **Metadata**: `prior-games/vy3m/metadata.json`
- **Lines of code**: ~340

## Mechanic

The level contains 1-3 player-controlled actor sprites of distinct classes (Pusher, Puller, Stomper), each with its own crate-interaction verb. ACTION5 cycles the active actor; only the active actor responds to ACTION1-4 (walk + class-specific verb on walking-into-crate). Pusher pushes a single crate forward. Puller drags a crate as it walks AWAY from the crate (crate is adjacent in opposite direction); walking INTO a crate with Puller is blocked. Stomper pushes single OR chains-pushes 2 adjacent crates. Win when every target cell is covered by a crate. Levels are arranged as isolated lanes (push, pull, chain), each requiring its specific class's verb; the player must cycle classes to deliver all crates.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1-4 | Walk active actor; verb fires per active class on walking-into-crate |
| ACTION5 | Cycle active class (Pusher → Puller → Stomper → Pusher; only cycles among classes present in current level) |

`available_actions = [1, 2, 3, 4, 5]` (ACTION6/7 unused).

## Levels

- **L1** (10×10): introduces M1 (Pusher's push). Single corridor; pusher pushes 1 crate to 1 target. Witness 5 actions.
- **L2** (12×12): introduces M2 (class-swap + Puller). Two vertically-isolated lanes; push lane needs Pusher's east-push; pull lane needs Puller's west-drag (push fails because pusher cannot reach pull-lane east of crate_b without crossing sealed wall). Witness 9 actions.
- **L3** (14×14): introduces M3 (extended class-swap + Stomper's chain-push). Three lanes; chain lane has 2 adjacent crates that Pusher's single-push cannot move (chain check fails) — Stomper required. Witness 14 actions.

## Novelty note

- Closest taxonomy: **ka59** (sokoban-explode-chase). Distinguishing rule: ka59's pawns share identical movement (slide-3-cells); vy3m has 3 distinct verbs (push / drag / chain-push) per class, where the player's load-bearing decision is "which class for this lane".
- Closest prior: **mr5q** (polarity-attract-discharge). Distinguishing rule: mr5q's pawns walk autonomously toward opposite polarity; vy3m's actors do NOT move autonomously — only the active actor responds to player input; class is fixed-per-actor.

## Index update

Appended row to `prior-games/index.md`:

```
| vy3m | class-swap-roster | Class-Roster Push-Pull-Chain — 1-3 player-controlled actor classes (Pusher / Puller / Stomper) with distinct verbs ... | 2026-05-08T... | (autonomous) |
```

## Run notes

- **NEW gate validated**: this run is the first to be smoke-tested with `CHECK_TRIVIAL_FAILS`. The spec's declared trivial heuristics for L2 (`[ACTION4 × 12]`) and L3 (`[ACTION4 × 15]`) were both replayed against the implementation and BOTH failed to advance the level — confirming vy3m has genuine planning depth. The contrast with run #1 (ej4t, where the witness == trivial heuristic = `[ACTION4 × N]`) demonstrates the gate working: ej4t's same heuristic would have flunked CHECK_TRIVIAL_FAILS if run today.
- **Bug found and fixed in test runner**: L1 witness was initially declared as 6 ACTION4 in WITNESSES dict, but L1 actually wins after 5 ACTION4 (2 walks + 3 pushes). The 6th leaked into L2, displacing the pusher and breaking the L2 witness. Fix: changed WITNESSES[1] to `[act(4)] * 5`. Game source unchanged.
- **All 11 universal checks pass + 3 custom checks**. CHECK_VISUAL_SANITY skipped (manual vision-pass).
- **Total run time**: ~50 minutes (faster than run #1 because study reused prior-session context for inputs 1-4; only step 5 was re-fetched fresh).
