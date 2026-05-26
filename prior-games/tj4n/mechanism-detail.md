# tj4n — walk-trail-loop-enclose

## Summary
A single blue avatar walks a 16-cell arena leaving a pink trail behind every step. When the avatar steps back onto a previously-walked trail cell, the loop closes — every yellow target sprite whose centre lies strictly inside the closed polygon is captured (set to `InteractionMode.REMOVED`), and any red forbidden sprite enclosed costs a strike. Three strikes lose the level; capturing every required sprite within the step budget wins. Higher levels add a vertical forbidden column that forces multiple smaller closures, then a few small pink-square waypoints the avatar's trail-head must visit by walking through.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move avatar up one cell (4 px) | always, blocked by forbidden / target / out-of-bounds |
| ACTION2 | Move avatar down one cell | as above |
| ACTION3 | Move avatar left one cell | as above |
| ACTION4 | Move avatar right one cell | as above |

ACTION5, ACTION6, and ACTION7 are intentionally NOT declared — closure fires automatically when the avatar steps onto its own trail (no commit verb needed), there are no clickable sprites, and the game has no undo. Per `skills/global/action-enum.md`, slot 7 is reserved for strict-undo and must be omitted when not used.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 (walk-deposits-trail) + M2 (closing-loop-captures-interior). | 3 yellow targets in a horizontal cluster at the centre of an empty arena. Discover that walking back onto your own trail closes the loop and captures interior cells. Witness `[1, 1, 4, 4, 4, 4, 4, 4, 2, 2, 2, 3, 3, 3, 3, 3, 3, 1]` (18 actions) — walk a tight rectangle around the three targets and step back onto the start. |
| 2 | + M3 (forbidden-exclusion-strike) + M4 (multi-closure-sequencing). | 4 corner targets (left and right pair) + 3 forbiddens in a vertical column at column x=8. A single big rectangle around all 4 targets encloses 3 forbiddens → 3 strikes → lose; two small loops on either side of the forbidden column win. Witness 54 actions — `loop1 = [3]*6 + [1]*8 + [4]*4 + [2]*8` then `loop2 = [4]*4 + [1]*8 + [4]*4 + [2]*8 + [3]*4`. |
| 3 | + M5 (pink-marker-waypoints). | Same 4 corner targets + 3 forbidden column as L2, plus three small pink 2×2 waypoints at cells `(2, 7)`, `(14, 7)`, and `(8, 14)`. The avatar must walk through every pink cell *and* complete the L2 closures; the pink markers don't block or strike. Witness 57 actions — replay the L2 two-loop witness (which naturally walks through `(2, 7)` on loop 1's left edge and `(14, 7)` on loop 2's right edge), then 3 final steps `[2, 3, 3]` from loop 2's closure cell `(40, 52)` down-left to `(32, 56)` to clear the third pink. |

## Win condition

Every sprite tagged `target` AND every sprite tagged `pink_marker` must have `interaction == InteractionMode.REMOVED`, AND `_strikes < 3`. When the predicate fires, the engine calls `next_level()` (or `win()` on L3).

## Lose condition

Either `_strikes >= 3` (three forbidden enclosures) or `_action_count >= step_budget` (50 / 110 / 200 for L1/L2/L3). No instant-fail collision; the playfield itself has no hazard sprites beyond forbiddens-as-strike-source.

## Internal state

- `_avatar_pos: tuple[int, int]` — pixel coords of avatar's top-left corner; multiples of 4.
- `_trail_seq: list[tuple[int, int]]` — ordered list of pixel coords where trail cells exist; oldest first. Each successful move appends the avatar's *previous* position.
- `_trail_sprites: list[Sprite]` — parallel list of trail Sprite refs, for batch-removal on closure.
- `_strikes: int` — count of forbidden-enclosure strikes; lose at 3 (L2+).
- `_post_closure_flash: int` — animation phase counter for the closure-feedback flash; -1 when idle, 0..3 during the four-frame flash, then committed back to -1.
- `_pending_capture: list[Sprite]`, `_pending_strike_sprites: list[Sprite]` — captures and strikes staged during the flash, committed at flash end.

## Notable code patterns

- **Trail-as-sprite-list with closure detection on revisit.** The avatar's trail is a sequence of `trail_cell` Sprite instances added to the level on each move. Closure is detected by `_trail_index(new_pos)` returning a non-negative index — meaning the new position appears in the historical trail; the cycle from that index forward is the polygon. Reusable as a "Jordan curve from walking" idiom.
- **Point-in-polygon ray casting on cell centres.** `_point_in_polygon(px, py, poly)` uses the standard half-plane crossing test on the polygon's vertex list (no winding assumption); for each of the 16×16 logical cells, the test is run on the centre `(cx*4 + 2, cy*4 + 2)` to avoid boundary ambiguity. Cheap on a 16×16 grid.
- **Multi-frame flash phase via complete_action gating.** On closure, `_post_closure_flash` is set to 0 and the step returns *without* `complete_action()`. The engine repeats `step()` with the same agent action until the flash phase increments to FLASH_FRAMES, at which point `_commit_closure()` runs and `complete_action()` fires. Same pattern as sk48's celebrate animation and sp80's spill animation.
- **Pink markers as sub-cell sprites with on-enter consumption.** Each `pink_marker` is a 4×4 sprite with a centred 2×2 pink block (the rest transparent), placed at cell top-left. On every successful avatar move, `_consume_pink_at(new_pos)` looks for any pink_marker at that cell and sets its interaction to REMOVED — the avatar's trail-head walks over the marker and "absorbs" it. Pink markers are `collidable=False` and not listed in `_is_blocked_for_avatar`, so they never block movement.
- **Layer hygiene for trail vs sprites.** Avatar at `layer=3`, targets/forbiddens/pink_markers at `layer=2`, trail at `layer=1`. The avatar always renders crisply on top of historical trail and on top of pink markers it's about to absorb.
- **Minimal action subset (`[1, 2, 3, 4]`, no commit / no click / no undo).** The closure mechanic fires automatically; there are no clickable sprites; the game has no undo. ACTION5/6/7 are omitted from `available_actions` rather than overloaded.
