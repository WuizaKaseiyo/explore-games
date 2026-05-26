# wm6q — edge-color-rotate-match

## Summary
The playfield is a fixed grid of 16×16 square tiles, each carrying four
colored edge bands (red, blue, yellow, green palette) and an inner glyph
indicating its kind. The player's single verb is ACTION6 click, which
rotates the clicked tile's 4-edge colour permutation 90° clockwise; tiles
never move. The level wins when every shared edge between two adjacent
tiles carries the same colour on both sides. Levels add a **locked tile**
(black-square glyph; fixed edges, clicks no-op) and a **linked pair**
(purple-ring glyph on two tiles; clicks on either rotate both in lockstep).
Step-budget exhaustion triggers `lose()`.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | CLICK at `(x, y)`. Resolved via `camera.display_to_grid` to a tile-cell hit. Regular tile → rotation += 1 mod 4 + step counted. Locked tile → no-op, no step. Linked-pair tile → rotates BOTH members + 1 step. | Always valid. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | rotate-via-click (base mechanic) | Two regular tiles in a row; align the single shared edge. Witness `[ACTION6@(40, 32), ACTION6@(40, 32)]` (2 clicks on tile B → R=2 makes B.left = blue, matching A.right = blue). step_budget = 12. |
| 2 | + locked-tile | 2×2 grid with locked tile at top-left corner anchoring 2 boundaries. Rotate the 3 free tiles to match the lock's fixed edges. Witness `[ACTION6@(40, 16), ACTION6@(40, 16), ACTION6@(24, 32), ACTION6@(24, 32), ACTION6@(24, 32)]` (5 clicks: 2 on tile (1,0) → R=2; 3 on tile (0,1) → R=3). step_budget = 25. |
| 3 | + linked-pair | 3×3 grid with locked centre and diagonal linked pair. Cascade through lock-anchored neighbours → outer-corner regulars → joint linked-pair rotation R_link = 2. Witness `[ACTION6@(32, 16), ACTION6@(48, 16), ACTION6@(16, 32), ACTION6@(48, 32), ACTION6@(32, 48), ACTION6@(16, 48), ACTION6@(16, 16), ACTION6@(16, 16)]` (8 clicks: 6 single-tile rotations + 2 clicks on (0,0) advancing R_link = 0 → 2 for both pair members). step_budget = 50. |

## Win condition

Predicate: for every internal grid edge (between two adjacent tiles in the
level's tile grid), the colour of the source tile's outward-facing band
equals the colour of the neighbour tile's facing-back band. Implemented
in `_check_win`, which iterates over the level's `tile`-tagged sprites
indexed by their pixel-origin and checks both `right` and `bottom` shared
edges against the corresponding neighbour. Fires `self.next_level()` after
each handled action when the predicate is True.

## Lose condition

`_steps_used >= step_budget` triggers `self.lose()`. `_steps_used` is a
private game attribute incremented at the end of each handled-action branch;
locked-tile no-op clicks do NOT increment `_steps_used` (preserving the
"clicks-on-the-lock waste no budget" semantic). Per-level budgets: L1 = 12,
L2 = 25, L3 = 50.

## Internal state

- `_tile_rotations: dict[str, int]` — per-tile current rotation R ∈ {0,1,2,3}.
- `_tile_meta: dict[str, dict]` — per-tile pixel origin, base assignment,
  glyph kind, and (for linked tiles) the partner's sprite name.
- `_steps_used: int` — clicks consumed at the current level.
- `StepBarHud` (HUD) — paints frame row 63 yellow/black proportional to
  `(step_budget − _steps_used) / step_budget`.
- No selection state, no mode toggle, no charge counter — every state the
  player must reason about is reflected directly in the rendered tile
  pixels.

## Notable code patterns

- **Per-tile pixel rebuild on rotation** — `_paint_tile_pixels(base,
  rotation, glyph)` returns a fresh 16×16 numpy array each time a tile
  rotates; the sprite's `.pixels` is reassigned in place. No incremental
  pixel mutation, no rotation matrix on Sprite — the rotation lives in the
  game's `_tile_rotations` dict and is materialised into pixels on every
  click.
- **Glyph-driven dispatch** — locked vs linked vs regular is encoded in the
  tile's `glyph` field in `_tile_meta`; the click handler branches on this
  to decide whether to rotate (regular), no-op (locked), or rotate-both
  (linked).
- **Pixel-origin grid indexing for the win check** — `_check_win` builds an
  `(origin_x, origin_y) → tile_name` map from each tile's `pixel_origin`
  and checks 16-pixel-stride neighbours rather than relying on grid-cell
  identifiers. This works for any level layout where tiles are placed on
  the same grid lattice.
- **HUD as a stateful `RenderableUserDisplay`** — `StepBarHud.set_state(max,
  used)` is called at every action to keep the bar in sync; the widget
  renders directly onto frame row 63 in `render_interface(frame)`.
- **Click resolution via bounding-box scan** — `_tile_at_display(x, y)`
  iterates over each tile's pixel rectangle to find the hit (rather than
  relying on `level.get_sprite_at`, which depends on collidable flags). The
  scan is O(N_tiles) per click, fine for ≤ 9 tiles.
