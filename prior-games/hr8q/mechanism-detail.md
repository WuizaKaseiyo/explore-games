# hr8q — pair-blend-recipe

## Summary

Pair-Blend Recipe is a turn-based recipe puzzle on a 64×64 grid
with no avatar and no spatial canvas. The player clicks ingredient
blocks on a right-side palette to fill input slots in a left-side
formula widget; the result auto-displays from the level's
visible mix table. Pressing the commit verb (ACTION5) either
consumes the current target chip (when the result matches) or
distils the result back into the palette as a new one-shot
intermediate (when it doesn't). Each level shows its full mix table
as 3-or-4-cell colour strips at the bottom of the frame, so the
recipes are learnable from the rendered frame alone — no
on-screen text. Difficulty grows from a one-shot pair (L1) to a
chained recipe requiring an intermediate (L2) to a triple-arity
formula with a third input slot (L3).

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Commit. With 2 slots filled, look up unordered pair in `pair_mix_table`; with 3 (L3 only) look up unordered triple in `triple_mix_table`. Match → consume target chip and advance the queue. Valid mismatch → distil result as a new intermediate ingredient (`uses=1`) appended to the palette. Invalid recipe → slots clear and any intermediate in the slots is consumed. Under-filled (0 or 1 slots) → state-no-op (still costs a step). | Always valid; effect depends on slot fill count and the level's mix tables. |
| ACTION6 | Click at `(x, y)`. Pixel coords are converted via `camera.display_to_grid`. Hits an ingredient block → fill the next empty slot with that block's colour AND toggle its `selected_ring` to visible. Hits a slot frame → clear that slot. Anywhere else → no-op. | Always valid; effect depends on which sprite the click cell hits. |

`available_actions = [5, 6]`.

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | pair-blend-and-commit | Two ingredients (magenta, light-blue), single target (purple). The single pair recipe `(magenta, light-blue) → purple` matches the target directly. Witness `[ACTION6@magenta, ACTION6@light-blue, ACTION5]` (3 actions). Step budget 30. |
| 2 | + intermediate-as-ingredient | Three ingredients (magenta, light-blue, pink), single target (maroon). No primary pair produces maroon; the only path is to commit `(magenta, light-blue) → purple` (mismatch, distilled) then `(purple, pink) → maroon` (match, win). Witness `[ACTION6@magenta, ACTION6@light-blue, ACTION5, ACTION6@purple, ACTION6@pink, ACTION5]` (6 actions). Step budget 50. |
| 3 | + three-input formula | Four ingredients (magenta, light-blue, pink, yellow); a third input slot becomes visible at L3 only. Single target (blue). Pair recipe `(magenta, light-blue) → purple`; triple recipes `(purple, pink, yellow) → blue` and decoy `(magenta, light-blue, yellow) → green`. Path: pair-commit to distil purple, then triple-commit `(purple, pink, yellow) → blue`. Witness `[ACTION6@magenta, ACTION6@light-blue, ACTION5, ACTION6@purple, ACTION6@pink, ACTION6@yellow, ACTION5]` (7 actions). Step budget 60. |

## Win condition

`self.next_level()` (and ultimately `self.win()` on L3) fires when
`len(self.target_queue) == 0` after a successful commit pops the
current queue head.

## Lose condition

`self.lose()` fires when `self.steps_used >= self.max_steps` while
the queue is still non-empty. There is no other lose path —
unwinnable inventory states are not detected by the engine; the
player simply burns through the budget without progress.

## Internal state

- `self.ingredients: list[IngredientHandle]` — primary + intermediate ingredient bundle (block sprite, selection ring, optional pip, colour, kind, uses).
- `self.pair_mix_table: dict[frozenset[int], int]` — unordered pair → output colour.
- `self.triple_mix_table: dict[frozenset[int], int]` — unordered triple → output colour (populated only at L3).
- `self.target_queue: list[int]` — colour values for queued targets (single-element queues in this design).
- `self.target_chip / target_fill_sprite` — current visible target chip widgets.
- `self.slot_colors: list[int | None]` of length 3; `self.slot_fills: list[Sprite | None]` of length 3.
- `self.current_result_color: int | None` — recomputed on every slot mutation; rendered in the result-slot fill sprite.
- `self.steps_used: int`, `self.max_steps: int` — step-bar HUD source.
- `self.slot3_visible: bool` — gated to L3 via `set_interaction(REMOVED|TANGIBLE)` on slot frame 2.

## Notable code patterns

- **Slot/result placeholder swap via `InteractionMode`**. Slot fills
  and result fill are pre-instantiated 6×6 sprites that flip between
  TANGIBLE (visible filled colour) and REMOVED (cleared).
  `pixels = np.full((6, 6), color, dtype=np.int16)` re-paints the
  fill colour without re-creating the sprite.
- **Sprite lookup by name**. Slot frames and target/result frames
  are placed in `_bare_level()` with unique names (`slot_frame_0`,
  …, `result_frame`, `target_frame`) and rewired in `on_set_level`
  via `level.get_sprites_by_name(...)` — `tags` is a read-only
  property and cannot be reassigned at runtime.
- **Ingredient handle bundle**. Each ingredient block is wrapped in
  a small dataclass-style object that carries its selection-ring
  sprite, optional pip sprite, colour, kind, and uses-remaining,
  letting `_handle_click` and `_handle_commit` operate on a single
  handle reference instead of juggling parallel lists.
- **Mix-rule HUD strip generator**. `_make_rule_strip` paints a
  variable-length sequence of 3×3 colour patches separated by
  1-pixel off-black gaps; the same helper renders both pair and
  triple rules. Strip layout encodes the recipe topologically
  (`[A][B][C]` for pair, `[A][B][C][D]` for triple).
- **Dynamic intermediate spawning**. `_distil_intermediate(color)`
  is invoked from `_handle_commit` when a valid recipe's result
  doesn't match the queue head; it adds a fresh `IngredientHandle`
  to the palette at the next free intermediate-column slot via
  `level.add_sprite`, with a single white `intermediate_pip` below
  to visually mark it as one-shot.
