# zw91 — inflate-fit-burst

## Summary
The player controls a single mobile avatar whose footprint cycles through three sizes (small=4×4, medium=8×8, large=12×12 cells); arrows step it one tile (4 cells) cardinally and ACTION5 grows it by one notch. Growing the avatar over a `shove_block` rolls the block in the cardinal direction away from the avatar's centre until it hits a wall or another block; from size 3, ACTION5 enters an "overloaded" state (visible halo) and a further ACTION5 fires a one-shot **burst** that destroys all `shove_block` and `breakaway_wall` sprites within Chebyshev-12 cells of the avatar's footprint. A level is won when the avatar's body fits a same-shape `socket` ring (matching size + same top-left). The level loses when the per-level step counter expires.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | UP — move avatar 4 cells north | always; no-op if new footprint overlaps `wall` or `shove_block` |
| ACTION2 | DOWN — move avatar 4 cells south | always; same collision check |
| ACTION3 | LEFT — move avatar 4 cells west | always; same collision check |
| ACTION4 | RIGHT — move avatar 4 cells east | always; same collision check |
| ACTION5 | size-cycle / overload / burst | always; behaviour branches on (`self.size`, `self.overloaded`): size 1 or 2 → try inflate +1 (cancels if walls/breakaways in new footprint, or any shove_block can't push); size 3 not overloaded → enter overloaded; size 3 overloaded → fire burst |

(`available_actions=[1, 2, 3, 4, 5]` — arrows + freedom slot, no click, no undo.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 (move) + M2 (size-cycle) — base dynamic system | Open chamber, single `socket_large` at the opposite corner. Witness `[ACTION4×10, ACTION2×10, ACTION5, ACTION5]` (22 actions): walk to the socket, cycle small→med→large to match. |
| 2 | + M3 (inflate-push): growing the avatar pushes adjacent shove-blocks radially outward | Vertical wall column with a 2-tile gap plugged by 2 shove-blocks blocks the only east passage. Witness `[ACTION4×5, ACTION1, ACTION5, ACTION4×5]` (12 actions): align at the gap row, inflate to size 2 — the push rolls both blocks east to the perimeter — then walk to the matching `socket_med`. |
| 3 | + M4 (overload-burst): from size 3, ACTION5 loads an overloaded halo; the next ACTION5 fires a Chebyshev-12 burst that destroys nearby shove-blocks and breakaway-walls (single-use) | Two wall columns: the first has a 3-tile gap with 3 shove-blocks; the second has a 3-tile gap of 3 breakaway-walls; an inner room with `socket_large` lies past both. Witness `[ACTION1, ACTION4×4, ACTION5×4, ACTION4×6, ACTION5×2]` (17 actions): navigate to tile (6, 6), cycle 1→2 (no push), cycle 2→3 (M3 push: all 3 blocks roll east into open tiles park-aligned with breakaways), enter overloaded, fire burst (M4: blocks AND breakaways destroyed), walk east through the cleared corridor, cycle to size 3 at the socket. |

## Win condition
Every sprite tagged `socket` is matched by the avatar: `(socket.x, socket.y) == (avatar.x, avatar.y)` AND the socket's size (derived from sprite width: 4=small, 8=med, 12=large) equals the avatar's current `self.size`. When all sockets match, `self.next_level()` fires.

## Lose condition
The per-level step counter (`self._step_hud.current`) drains by 1 every action; when it reaches 0, `self.lose()` fires. There is no other lose path — the avatar can always retreat or re-cycle; a misfired burst at L3 makes the level unsolvable but the player still loses by counter exhaustion rather than getting stuck in a no-win waiting room.

## Internal state
- `self.size: int ∈ {1, 2, 3}` — current avatar size; the visible cue is which of the three avatar sprite variants is TANGIBLE (the others are REMOVED).
- `self.overloaded: bool` — True iff the avatar is at size 3 and ACTION5 has been pressed once without yet firing burst; the visible cue is `overload_halo` set TANGIBLE at layer 5 and tracking the avatar's position every step.
- `self._step_hud.current: int` — remaining step budget; surfaced in the HUD bar on row 0 (palette 9 blue → palette 0 white).

## Notable code patterns
- **Sprite-variant swap for size cycling**: every level pre-places all three avatar variants (`avatar_small`/`avatar_med`/`avatar_large`) at the same top-left cell; size cycle is a TANGIBLE↔REMOVED swap on `self._swap_active_size(new_size)` rather than rewriting pixels — clean and avoids re-render artefacts. The pattern extends the two-sprite-swap idiom from `code/universal-scaffold.md` to three variants.
- **Roll-until-wall push semantics**: shove-blocks roll one tile per iteration in the push direction and stop the moment the next-tile destination is a `wall` / `breakaway_wall` / another `shove_block` / perimeter. `_block_dest_blocked(x, y, exclude=block)` is the single predicate that gates each roll step.
- **Inflate roll-back on cancel**: before any push begins, `_try_inflate` snapshots each affected block's position; if any block can't move at all (first destination already blocked), all moved blocks are restored and the inflate cancels.
- **Halo as persistent visible cue**: `overload_halo` is a 16×16 sprite with internal pink-spoke pattern; `_enter_overload` sets it TANGIBLE and repositions every move so it stays centred on the size-3 avatar; `_fire_burst` sets it REMOVED. This satisfies checklist item 19 (no hidden state — the cue persists for the full overloaded duration).
- **Cheby-12 burst zone**: `_fire_burst` computes `(xmin-12, ymin-12, xmax+12, ymax+12)` from the size-3 footprint and bounding-box-tests every `shove_block`/`breakaway` sprite for overlap; sprites that overlap are flipped to `InteractionMode.REMOVED`.
- **Tag-based dispatch**: walls (perimeter strips and interior wall_blocks) share tag `wall`; breakaway-walls share `wall` and `breakaway`. `level.get_sprites_by_tag("wall")` includes both during movement / inflate collision checks; the burst code checks `breakaway` separately to destroy them while leaving regular walls intact.
