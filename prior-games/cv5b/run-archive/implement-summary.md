# Implement summary — cv5b

## Files written
- `prior-games/cv5b/cv5b.py` — 428 lines.
- `prior-games/cv5b/metadata.json`.

## Plain-English summary
A movable launcher walks a sky playfield and emits a marble along a
parabolic arc to a clicked landing cell. The launcher carries a
3-state charge level cycled via the freedom slot, with each charge
choosing a different arc shape and reachable distance. Solid bars in
the playfield block the launcher's movement and absorb arcs that pass
through them; a stippled vertical band deflects an arc's final
landing cell by one position. Each level is won by directing arcs
to land on every coloured ring; level progression composes walk
+ charge + barrier-clearance + deflection.

## Engine smoke test (instantiation + witness replay)
Successfully instantiated `Cv5b()` with 3 levels and
available_actions=[1, 2, 3, 4, 5, 6]. Replayed the spec's per-level
witnesses end-to-end: L1 (1 action) → L2 (14 actions) → L3 (36 walks
+ 2 cycles + 1 fire = 39 actions to WIN state). All transitions
fired `next_level()` correctly; final state = WIN; targets_remaining
== 0 at finish.
