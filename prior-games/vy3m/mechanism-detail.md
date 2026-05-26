# vy3m — class-swap-roster

## Summary

The level contains 1-3 player-controlled actor sprites of distinct classes (Pusher, Puller, Stomper). ACTION5 cycles the active actor; only the active actor responds to ACTION1-4. Pusher walks into a crate to push it forward (single push). Puller walks AWAY from a crate (crate adjacent in opposite-of-motion direction) to drag it; walking INTO a crate is blocked. Stomper walks into a crate to push it (single OR chain-of-2 if cell beyond has another crate). Win when every target is covered by a crate. Lose when step budget exhausted.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION1-4 | Walk active actor 1 cell. Verb fires per active class. | always valid |
| ACTION5 | Cycle active class (Pusher → Puller → Stomper → Pusher) | always valid (cycles only among classes present in current level) |

## Per-level mechanic progression

| Level | Mechanic introduced | Specific challenge / witness |
|---|---|---|
| 1 | M1: Pusher's push | 10×10 grid, single corridor at y=4. Pusher (2,4) pushes crate (5,4) east to target (8,4). Witness `[ACTION4 × 5]`. |
| 2 | M2: class-swap + Puller's drag | 12×12 with 2 isolated lanes. Push lane: Pusher (1,2), crate_a (4,2), target_a (8,2). Pull lane: Puller (4,7), crate_b (5,7), target_b (3,7). Witness `[ACTION4 × 6, ACTION5, ACTION3 × 2]` — pusher delivers crate_a east; cycle to puller; puller drags crate_b west to target_b. |
| 3 | M3: extended class-swap + Stomper's chain-push-of-2 | 14×14 with 3 isolated lanes. Push lane and pull lane same as L2. Chain lane (row 12): Stomper (1,12), crate_c1 (3,12), crate_c2 (4,12), target_c (7,12). Witness `[ACTION4 × 6, ACTION5, ACTION3 × 2, ACTION5, ACTION4 × 4]` — pusher + puller as L2; cycle to stomper; stomper chain-pushes both crates east to land crate_c2 on target. |

## Win condition

Every `target` sprite has a `crate` sprite at its position.

## Lose condition

`self._steps_used >= self._max_steps` (per-level budgets: L1=30, L2=50, L3=80).

## Internal state

- `self._active_class: str` ∈ {"pusher", "puller", "stomper"}
- `self._steps_used: int`
- `self._max_steps: int`

## Notable code patterns

- **Class-conditional verb dispatch** in `step()`: directional ACTION1-4 routes through `_attempt_pusher_move`, `_attempt_puller_move`, or `_attempt_stomper_move` based on `self._active_class`. Each verb function handles wall / actor-blocking / crate-push / chain-push checks specific to that class.
- **Puller's blocking-when-walking-into-crate**: a key nuance — Puller's verb is "drag-when-walking-away", so walking-INTO-a-crate is rejected as a no-op (returns False). Distinct from Pusher (push) and Stomper (push) where walking-into is the verb-trigger.
- **Stomper's atomic chain push**: `_attempt_stomper_move` checks the second crate's destination cell BEFORE moving anything; if blocked, entire push fails (no partial state mutation). Order of moves: crate2 first (rear), crate1 second (front), stomper third — to avoid overlap.
- **Active-class HUD as colour badge** (top-left 4×4): the only persistent visual cue distinguishing which class is currently controlled. Solves checklist item 19 (no hidden state).
- **NEW: trivial heuristic gate (CHECK_TRIVIAL_FAILS)**: this is the first prior game generated under the upgraded smoke_test gate that runs the spec's declared trivial heuristic and asserts the level does not advance. vy3m's lane-isolation structure ensures the trivial "always Pusher, press right" heuristic cannot reach pull/chain lanes, so the gate confirms genuine planning depth.
