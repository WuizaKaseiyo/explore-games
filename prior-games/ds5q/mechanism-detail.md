# ds5q — wall-erode-chain

## Summary
The player controls a small framed token (`avatar`) that walks one logical 8-pixel tile per arrow press inside a stone-bordered chamber. ACTION5 strikes a coloured pickaxe: it decrements the hardness counter of every wall in the avatar's 4-cardinal neighbourhood whose colour matches the avatar's current charge, and walls reach floor when their hardness drops to zero. The charge state is set by stepping onto a coloured charge-pad on the floor; uncharged strikes do nothing. Stone sprites are un-erodable and channel the path. Win condition: reach the exit cell on every level within a per-level step budget. Lose condition: action count meets or exceeds the level's step budget.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move avatar north 8 px (one tile up) | Always emitted; movement blocked by walls and stones, and by the grid edge |
| ACTION2 | Move avatar south 8 px | Always emitted; same blocking rules |
| ACTION3 | Move avatar west 8 px | Always emitted; same blocking rules |
| ACTION4 | Move avatar east 8 px | Always emitted; same blocking rules |
| ACTION5 | Strike: decrement hardness of each same-colour 4-cardinal-adjacent wall by 1 | Always emitted; effect conditional on charge state being non-`None` and an adjacent wall sharing that colour |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | base system: walk + erode-adjacent | Stone-walled corridor at row 4 with two grey-hardness-1 walls between start and exit; avatar's charge is auto-set to "grey" so erode is immediate. Witness: `[4, 4, 5, 4, 4, 5, 4, 4, 4]` (9 actions). Step budget 30. |
| 2 | + colour-pickaxe-match | Avatar starts uncharged; the red wall at (3, 4) requires red charge from the pad at (1, 0), the blue wall at (5, 4) requires blue charge from the pad at (6, 2); col 3 and col 7 are sealed by stones with the only openings being the two walls and the exit, and the (5, 4) blue wall is the unique entry into the exit corridor. Witness: `[1, 1, 1, 1, 4, 2, 2, 2, 2, 4, 5, 4, 4, 1, 1, 4, 4, 3, 3, 2, 2, 5, 4, 4, 4]` (25 actions). Step budget 80. |
| 3 | + layered-hardness | Walls expose hardness as stripe count (1, 2, or 3 stripes); col 3 has two openings — `wall_red_h2` at (3, 1) and `wall_red_h3` at (3, 4) — so multi-strike erosion on whichever route is chosen is unavoidable. Path A via (2, 1) takes 22 actions; the row-4 monotone-progress path B takes 27. Witness (Path A): `[1, 1, 1, 1, 4, 2, 4, 5, 5, 4, 4, 2, 4, 4, 3, 3, 2, 2, 5, 4, 4, 4]` (22 actions). Step budget 90. |

## Win condition

After every action, if the avatar's tile coordinates equal the exit's tile coordinates, `next_level()` fires. The exit sprite is INTANGIBLE so the avatar can stand on its cell.

## Lose condition

At the start of `step()` (before action processing), if `_action_count >= step_budget`, `lose()` fires. The step budget is read from `level.get_data("step_budget")` in `on_set_level`.

## Internal state

- `self.charge_state: str` — current charge colour (`"red"`, `"blue"`, `"grey"`, or `"none"`). Defaults to `level.get_data("charge_initial")` per level (`"grey"` at L1, `"none"` at L2/L3).
- `self.step_budget: int` — per-level step cap (30 / 80 / 90).
- `self.wall_hardness: dict[(gx, gy) → int]` — current hardness per wall position; the source-of-truth for collision and erode.
- `self.wall_color_at: dict[(gx, gy) → str]` — colour of the wall at each tile.
- `self.wall_variants: dict[(gx, gy) → dict[hardness → Sprite]]` — pre-placed sprite variants per position; the active variant has `InteractionMode.TANGIBLE` and others are `REMOVED`. Erosion swaps interaction modes.
- `self.stone_tiles: set[(gx, gy)]` — tiles occupied by an un-erodable stone.
- `self.pad_at: dict[(gx, gy) → str]` — charge-pad colour per tile.
- `self.exit_tile: (gx, gy)` — exit's tile.
- `self.avatar_variants: dict[charge_str → Sprite]` — three avatar sprite variants (uncharged / red / blue); only one is `TANGIBLE` at a time, swapped by `_set_charge`.

## Notable code patterns

- **Sprite-swap idiom** for both wall hardness layers and avatar charge state: pre-place all variants at the same pixel coordinates, set all-but-active to `InteractionMode.REMOVED`, swap on event. Mirrors `universal-scaffold.md` § "Two-sprite swap". Used at scale for walls (up to 3 variants per cell) and for the avatar (3 variants always).
- **Tile-level collision via Python dicts** rather than engine pixel-perfect collision. `_try_walk` looks up the destination tile in `self.stone_tiles` and `self.wall_hardness`; cheap, deterministic, and naturally handles the "wall removed" transition (key is deleted from `wall_hardness`).
- **Step counter HUD** (`StepCounterHud`) renders a horizontal bar across row 0 of the frame using palette 4 over palette 0; `set_max(N)` is called per level in `on_set_level` and `set_current(N - action_count - 1)` is called once per step.
- **Sprite name parsing for hardness/colour discovery** (`wall_<color>_h<N>`) — `on_set_level` walks `level.get_sprites()` once and populates the four state dicts plus the variant table. No per-instance metadata is required at construction time.
- **Charge-pad pickup is a post-action position check**, not a click handler. After every step's movement is committed, the avatar's tile is looked up in `self.pad_at` and the charge state updated if the avatar landed on a different-colour pad. Avoids any reliance on engine collision events.
