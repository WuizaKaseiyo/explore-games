# fw8c — pigment-mix-walk

## Summary
The player controls a hollow `carrier` pawn that walks a chamber via
cardinal arrow keys, with each step advancing one cell (8 pixels).
Stepping onto a `pad`-tagged sprite OR's that pad's pigment id into
the carrier's stored 3-bit pigment subset (one bit each for orange,
pink, light-blue); the carrier's centre re-tints to the resulting
mixed colour per a fixed 8-state mixing table. Stepping onto a
`slot`-tagged sprite whose demanded subset equals the carrier's
current set replaces the slot with `slot_consumed` AND clears the
carrier's set back to empty. From level 3 onward, `door`-tagged
sprites in the chamber act as state-conditional gates: each door is
passable iff the carrier's current set equals the door's demanded
subset. The level wins when every original slot is consumed, and
loses when the per-level step counter drains to zero.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move carrier 1 cell up | not blocked by wall or tangible door; not out of bounds |
| ACTION2 | Move carrier 1 cell down | as above |
| ACTION3 | Move carrier 1 cell left | as above |
| ACTION4 | Move carrier 1 cell right | as above |

`available_actions = [1, 2, 3, 4]` — pure-arrow game. ACTION5 / 6 / 7
are deliberately unexposed.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 — pickup-and-deliver: walk over a `pad` to OR its pigment into the carrier's set; walk over a `slot` matching the carrier's set to consume the slot and clear the carrier. | Single pad (orange) + single slot (orange). Tutorial: walk pad → walk slot. Witness `[ACTION4, ACTION4, ACTION2, ACTION2, ACTION4, ACTION4, ACTION4, ACTION2, ACTION2]` — 9 actions. |
| 2 | M2 (NEW) — multi-pigment mixture: visit two distinct `pad` sprites between consume events to build a 2-element pigment subset; deliver to a slot demanding the derived mixture colour. | 2 pads (orange, pink) + 2 slots (slot_pink demanding {pink}, slot_green demanding {orange, pink} → derived green via the scrambled mixing table). Witness `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION2, ACTION2, ACTION2, ACTION2, ACTION3, ACTION3, ACTION3, ACTION3, ACTION1, ACTION1, ACTION4, ACTION4, ACTION4, ACTION4, ACTION2, ACTION2]` — 20 actions. |
| 3 | M3 (NEW) — pigment-gated door: a `door`-tagged sprite is passable iff the carrier's current set equals the door's demanded subset. The L3 chamber is partitioned by an interior wall row at y=4 with a single `door_green` (demands {O, P}) at the gap; all 4 lower-half slots and pad_lightblue lie below the wall. The witness must accumulate {O, P} above the wall, cross with the matching state, then re-route below. | 3 pads (pad_orange, pad_pink_upper above; pad_pink_lower + pad_lightblue below) + 4 slots (slot_green, slot_pink, slot_lightblue, slot_magenta). Witness `[ACTION2, ACTION2, ACTION4, ACTION4, ACTION4, ACTION4, ACTION3, ACTION2, ACTION2, ACTION3, ACTION2, ACTION3, ACTION3, ACTION4, ACTION4, ACTION1, ACTION4, ACTION4, ACTION4, ACTION3, ACTION2, ACTION4, ACTION1, ACTION3, ACTION3, ACTION2]` — 26 actions. |

## Win condition
After every step, `_check_win` returns True iff every `slot`-tagged
sprite has interaction `REMOVED` (i.e., every original slot has been
consumed). On True, `self.next_level()` fires; after L3, the engine
fires `self.win()`.

## Lose condition
The per-level `step_budget` (30 / 45 / 70 for L1 / L2 / L3) read from
`level.get_data("step_budget")` decrements per action via
`self._action_count`; on `_action_count >= self._budget`,
`self.lose()` fires. No instant-fail collisions; wasted steps are the
only failure mode.

## Internal state
- `self._pigment_set: int` — 3-bit bitmask of pigments held; bit 0 =
  orange, bit 1 = pink, bit 2 = light-blue.
- `self._budget: int` — per-level step budget.
- `self._step_hud: StepCounterHud` — `RenderableUserDisplay` that
  paints a left-to-right depleting bar at row 0.
- Carrier position lives in the carrier sprite's `(x, y)` (snapped to
  cell × STEP_SIZE + SPRITE_INSET).
- `MIXING_TABLE: dict[int, int]` — fixed 8-state subset → palette
  table; `{O,P} → 14 (green)`, `{O,L} → 15 (purple)`,
  `{P,L} → 6 (magenta)`, `{O,P,L} → 5 (black)`.
- Per-level slot consumption is tracked via
  `Sprite.set_interaction(InteractionMode.REMOVED)`; a `slot_consumed`
  sprite is added at the same cell as the visual replacement.

## Notable code patterns
- **Mixing-legend HUD**: `MixingLegendHud` paints the bottom 8 rows of
  the rendered frame with three formula entries — each juxtaposes two
  4-px input pigment swatches against a 6-px result swatch (with a
  4-px light-grey gap in between) so the player can read the mixing
  rules off the screen without symbols, letters, or arrow glyphs. The
  legend overlays the bottom wall row visually; the wall sprites stay
  collision-active and the carrier never reaches that row.
- **Carrier re-tint**: `_retint_carrier()` resets the sprite's pixel
  array from the cached `_carrier_base_pixels` template, then
  `np.where`-substitutes the value-1 fill cells with the current
  mixture colour from `MIXING_TABLE`. Reusable as "live pawn-state
  visualisation" via per-step pixel rebuild.
- **Door state toggle**: `_update_doors()` walks all `door`-tagged
  sprites and sets `interaction` to `REMOVED` iff the carrier's
  pigment set equals the door's demand bitmask, else `TANGIBLE`.
  Called both before move (passability check) and after pickups
  (refresh for next turn).
- **Tag-encoded demand**: each slot/door's demanded pigment subset
  is encoded by a `demands_<colour>` tag (e.g. `demands_magenta`)
  parsed against the `SLOT_DEMANDS` / `DOOR_DEMANDS` lookup. Avoids
  per-instance demand state.
- **Slot consume idiom**: instead of mutating the original slot
  sprite's pixels, the consumed slot's interaction is set to
  `REMOVED` and a `slot_consumed` sprite (palette 2 outline / 4
  interior) is added at the same position. Cleaner than manual
  pixel mutation; the original slot remains queryable via
  `get_sprites_by_tag("slot")` for win-check filtering.
- **Cell-stride coordinate model**: every walkable position is
  `cell_idx * STEP_SIZE + SPRITE_INSET = ix * 8 + 1`. Sprites are
  6×6 placed at this inset within an 8-pixel cell, leaving 1-pixel
  gaps between cells for visual separation. The collision check
  uses the centre of the destination cell against bounding-box
  walls and tangible doors.
