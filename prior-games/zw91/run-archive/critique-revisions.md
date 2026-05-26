# critique-revisions.md (visit 1)

The spec passes most checklist items but has a **load-bearing geometric inconsistency** in L3 that breaks the witness, plus a few smaller clarifications.

## Issue 1 (BLOCKING) — checklist item 12: L3 witness cycle 2→3 at (7, 6) fails because tile (8, 8) is wall

**Section quoted:** §4 — Level 3 — Layout & Witness step 8.

> First vertical wall column at tile_x=8 (same as L2): `wall_block` at tiles (8, 1..5) and (8, 8..14); gap at (8, 6), (8, 7).
> ...
> 8. ACTION5 (cycle 2→3): footprint extends to cells (28..39, 24..35) = tiles (7-9, 6-8). Block at (10, 6) is NOT in new footprint. Inflate succeeds. Avatar at tile (7, 6) size 3.

**The bug:** the L3 wall column structure has walls at tiles (8, 1..5) **and (8, 8..14)** — i.e., tile (8, 8) is a wall_block. The witness's cycle-2→3 at top-left tile (7, 6) makes the avatar's size-3 footprint cover tiles (7-9, 6-8). The wall at tile (8, 8) is *inside* this footprint. Per the inflate rule "candidate footprint contains wall → cancel", the inflate fails. The witness cannot reach size 3 at (7, 6); it cannot fire burst at the position needed to cover the breakaway-walls.

This breaks the M4 counterfactual claim too — the spec asserts burst is necessary, but with the broken geometry, burst is **unreachable**, which means the level is unsolvable, not just that M4 is gated.

**Fix-direction:** widen both wall column gaps from 2 tiles to 3 tiles. New layout:

- First wall column at tile_x=8: walls at tiles (8, 1..5) and (8, 9..14). Gap at (8, 6), (8, 7), (8, 8) — three tiles. Place three `shove_block` instances at (8, 6), (8, 7), (8, 8) plugging the gap.
- Second wall column at tile_x=11: walls at tiles (11, 1..5) and (11, 9..14). Gap at (11, 6), (11, 7), (11, 8) — three tiles. Place three `breakaway_wall` instances at (11, 6), (11, 7), (11, 8) plugging the gap.

With the 3-tile gap, the size-3 footprint at (7, 6) covers (7-9, 6-8) — the column has gap exactly at (8, 6-8) (initially blocked by shove-blocks but moveable by M3 push). Inflate proceeds.

The L3 witness must be re-derived with three blocks (not two) and three breakaways (not two). The witness step-by-step push trace becomes:

- Cycle 1→2 push at (7, 6): blocks at (8, 6) and (8, 7) (tiles in size-2 footprint (7-8, 6-7)) push east one tile each → (9, 6), (9, 7). Block at (8, 8) is *not* in size-2 footprint, stays put.
- Cycle 2→3 push at (7, 6): blocks at (9, 6), (9, 7), and (8, 8) — all in size-3 footprint (7-9, 6-8). Push east. (9, 6)→(10, 6); (9, 7)→(10, 7); (8, 8) rolls east twice (8, 8) → (9, 8) → (10, 8) until escaping the footprint.
- Burst at (7, 6) size 3: zone Cheby-8 from footprint cells (28..39, 24..35) = cells (20..47, 16..43). Blocks at tiles (10, 6-8) cells (40..43, 24..35) ∈ zone — destroyed. Breakaways at tiles (11, 6-8) cells (44..47, 24..35) ∈ zone — destroyed.
- Witness count remains 17 actions.

## Issue 2 (BLOCKING) — checklist item 12: L3 burst-skip-M3 alt-path needs explicit refutation

The current spec defends M3-necessity via "the wall column at tile_x=8 has the same gap-with-blocks pattern as L2…" but does not enumerate the alt-path "player size-3-bursts the blocks first at a position where blocks are in burst zone, then later inflates without M3 firing."

**Fix-direction:** add a concrete alt-path enumeration to the M3 counterfactual paragraph. Argument: burst zone Cheby-8 from a size-3 footprint covers a 28-cell-wide zone. To cover both blocks (cells x=32..35) and breakaways (cells x=44..47) — total x-range 32..47, width 16 — in one burst, the avatar's size-3 footprint must straddle a position with x-range overlapping both. Computing: footprint x-range [tx, tx+11]; zone x-range [tx-8, tx+19]. For zone to cover x=32..47: tx-8 ≤ 32 → tx ≤ 40 AND tx+19 ≥ 47 → tx ≥ 28. So tx ∈ [28, 40]. For avatar size 3 to be feasible at tx, the footprint must not overlap walls/blocks. Tx=28 (tile_x=7) footprint tiles (7-9, *) — tile (8, *) has shove_blocks at (8, 6-8) and walls elsewhere; for any ty in (3..8), footprint includes block-or-wall in tile_x=8. Tx=32 (tile_x=8) — footprint includes tile (8, *) — wall column. Tx=36 (tile_x=9) — footprint tiles (9-11, *) — tile (11, *) has wall/breakaway. Tx=40 (tile_x=10) — footprint tiles (10-12, *) — tile (11, *) ditto. **No feasible size-3 position covers both blocks and breakaways in one burst** — therefore the player cannot skip M3 by direct burst. M3 is necessary because the only avatar-size-3 position from which burst can destroy both block-set and breakaway-set is tx=28 (tile (7, 6)), and reaching that position with the size-3 inflate succeeding requires that the tile-(8, 6-8) blocks have already been pushed east — which is M3.

## Issue 3 (CLARIFY) — push-roll rule semantics

**Section quoted:** §2 and §5 ACTION5.

> the block rolls one tile per cell of growth in the radial direction away from the avatar's centre until it hits a collidable wall

This is ambiguous: "one tile per cell of growth" suggests a 4-tile roll for a 1→2 cycle (since growth is 4 cells), but the witness only assumes a 1-tile roll. Settle on one rule.

**Fix-direction:** rewrite the rule as: *"When ACTION5 grows the avatar from size N to size N+1, each `shove_block` whose cells lie inside the new footprint is rolled in the cardinal direction `sign(block.center − avatar.center)` (with east breaking ties when both axes tie) until it (a) escapes the new footprint into an empty tile, OR (b) the next tile in the push direction is wall, breakaway-wall, or another shove-block. In case (a) the block parks at the first escape tile. In case (b) the block stops at its current position; if a block could not move at all (its first attempted destination was blocked), the entire inflate cancels and all moved blocks roll back. Otherwise the inflate commits."* This rule is unambiguous and matches the witness's per-step claims.

## Issue 4 (CLARIFY) — checklist item 19: visible cue for "overloaded" must persist

The spec already declares an `overload_halo` sprite. Confirm it is rendered at layer 5 (above the avatar) for the entire duration of the overloaded state — not just a one-frame flash — per checklist item 19's requirement that visible cues persist as long as the state is in effect.

**Fix-direction:** add an explicit sentence: *"`overload_halo` is set to `interaction=TANGIBLE` at the moment the avatar enters overloaded and remains so until burst fires; it tracks the avatar's position. The persistent halo is the visible cue that the next ACTION5 will fire burst rather than continue size-cycling."*

## Issue 5 (CLARIFY) — checklist item 20: walls and avatars at full 64×64 grid

The spec uses `grid_size=(64, 64)` and a 1-cell-per-display-pixel scale. Avatar sprites at 4×4 / 8×8 / 12×12 cells render at 4 / 8 / 12 display pixels, which at full resolution is reasonable; sockets at 4 / 8 / 12 display pixels match. Wall_strip at 64×4 with internal brick texture (alternating cells per row, 2-row tall bricks) reads as a textured wall. **No bump needed** — confirming the spec already passes item 20.

## Issue 6 (CLARIFY) — checklist item 18 (d) step budgets

L1: 50 over a 22-action witness (~2.3×) — generous. L2: 60 over a 12-action witness (5×) — generous. L3: 100 over a 17-action witness (~6×) — generous AND L3-budget > L2-budget per `difficulty-rules.md` § d. **Pass.**

## Verdict

Two BLOCKING issues (1 and 2) and three CLARIFY issues (3, 4, 5). Loop back to `write_spec` for revision. Issue 5 is informational (already passes); document for completeness.
