# ek73 — wake-trail-evade

## Summary
A single yellow-cross avatar walks one logical cell per arrow-press across a walled 16×16 logical grid (rendered on a 64×64 frame with `CELL_STRIDE=4`) to consume every orange-star collectible in the level. Each cell the avatar **vacates** is left behind as a magenta wake mark for K=3 turns then fades — stepping onto an active wake cell triggers `self.lose()`. Level 1 establishes the base dynamic in a T-shape playfield. Level 2 introduces a one-shot **wake-clearer pad** that erases every active wake cell when the avatar overlaps it. Level 3 introduces a one-shot **paired warp pad** that teleports the avatar between two paired pads; the avatar's vacated cell still becomes wake age 1, but the destination cell does not.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move avatar one logical cell up | always; rejected (no-op, step counter still ticks) if destination is wall/off-grid; LOSES if destination is age-1/2/3 wake |
| ACTION2 | Move avatar one logical cell down | as above |
| ACTION3 | Move avatar one logical cell left | as above |
| ACTION4 | Move avatar one logical cell right | as above |

(`available_actions=[1, 2, 3, 4]` — pure cardinal movement. ACTION5/6/7 absent.)

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Walk-with-decaying-wake (K=3) | T-shape playfield: 2-wide horizontal corridor at rows 3-4 plus 1-wide vertical arm at column 3. Avatar at `(3, 3)`; two collectibles at `(12, 3)` and `(3, 13)`. Witness ([4]×11, [2]×1, [3]×11, [2]×9 — 32 actions total): walk east on row 3, descend to row 4, return west on row 4 (forced detour around fresh wake), then south on column 3 to the south collectible. |
| 2 | + wake-clearer pad | 2-wide horizontal corridor rows 7-8 cols 1-14, 1-cell branch up at column 8 to `(8, 5)` clearer, west row-5 stub to `(2, 5)` collectible; east-end collectible at `(14, 8)`. Avatar at `(2, 8)`. Witness ([4]×12, [1]×1, [3]×6, [1]×2, [3]×6 — 27 actions): east 12 to `(14, 8)` collect; north into row 7; west on row 7 to column 8; north 2 into branch and clearer at `(8, 5)`; west on row 5 to `(2, 5)` collect. |
| 3 | + paired warp pad | T-junction: horizontal corridor row 8 cols 1-14, vertical branch column 8 rows 1-7, side cells `(1, 9)` and `(14, 9)` reserved for warp-pair. Three collectibles at `(8, 1)`, `(1, 8)`, `(14, 8)`; clearer at `(8, 1)` co-located with collectible; warp pair at `(1, 9) ↔ (14, 9)`. Avatar at `(8, 8)`. Witness ([1]×7, [2]×7, [3]×7, [2]×1, [1]×1 — 23 actions): north 7 to `(8, 1)` collect+clearer; south 7 to `(8, 8)`; west 7 to `(1, 8)` collect; south 1 to `(1, 9)` warp; teleports to `(14, 9)`; north 1 to `(14, 8)` collect. |

## Win condition

Every `collectible`-tagged sprite is `InteractionMode.REMOVED` → `self.next_level()`. After the third level, the engine's default fires `self.win()`.

## Lose condition

Three predicates trigger `self.lose()`:
- Successful move's destination overlaps an `InteractionMode.TANGIBLE` wake-tagged sprite.
- Step counter reaches 0 (`self._action_count >= _step_budget`; budgets are 60 / 50 / 80 for L1 / L2 / L3).
- Soft-lock detector: at end of step, all four cardinal neighbours of the avatar are walls/off-grid OR active wake AND the win predicate is not satisfied.

## Internal state

- `self._wake: dict[(lx, ly), int]` — mapping of logical-cell coordinates to wake age (1, 2, or 3). Aged on every successful move; entries reaching age 4 are removed.
- `self._wake_sprites: dict[(lx, ly), Sprite]` — parallel dict mapping each wake cell to the currently-spawned `wake_age{1,2,3}` sprite that renders it. Sprites are swapped (one removed, one re-spawned) when an age tier changes.
- `self._walkable: set[(lx, ly)]` — the level's walkable cell set, computed in `on_set_level` from the level number.
- `self._step_budget: int` — read from `level.get_data("step_budget")`.
- The HUD widget `StepCounterHud` lives on `self._step_counter_ui` and renders into row 63.

## Notable code patterns

- **Logical-vs-pixel coordinates with stride**: every game-relevant sprite is 4×4 pixels and snapped to logical positions at multiples of 4 on a 64×64 grid. The wa30 pattern. `_to_pixel(lx, ly)` and `(p.x // 4, p.y // 4)` are the conversion helpers.
- **Walkable-cell precomputation**: `_l1_walkable()`, `_l2_walkable()`, `_l3_walkable()` build the per-level walkable set; `_build_walls(walkable)` then places a wall sprite at every non-walkable cell. Movement logic checks the walkable set, not sprite collision — keeps the dispatch O(1) per move.
- **Wake aging via dict snapshot**: `_age_all_wake` builds a new dict, dropping entries that would age past K. `_refresh_wake_sprite_visuals` swaps each cell's wake sprite to the right age tier so the rendered frame shows the wake's lifetime.
- **Pad-effect ordering matters**: clearer pad effects fire AFTER the new wake mark is added on the vacated cell, so clearer wipes the just-added wake too. This ensures the witness can step onto a clearer and have the descent path clean of wake.
- **One-shot pads via InteractionMode.REMOVED**: clearer and warp pads are consumed by setting their `InteractionMode` to REMOVED — the sprite stays in the level but doesn't render or trigger again. The two-sprite-swap idiom from `code/universal-scaffold.md`.
- **Soft-lock detection**: at end of step, scan the avatar's 4 cardinal neighbours. If all are walls/off-grid OR active wake (lethal) and win is not yet satisfied, fire lose immediately rather than wait for budget exhaustion. Per `difficulty-rules.md` § 1's no-win-waiting-room rule.
