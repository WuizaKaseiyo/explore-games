# hl4n — row-col-tint-cross

## Summary
The player clicks tint markers along the left and top edges of an 8×8 grid to cycle each row's and column's tint through a small palette; each click instantly repaints every cell in the targeted row or column. The combiner rule is **last-click-wins**: each cell shows whatever color was most recently painted onto it, whether by a row click or a column click. A handful of cells in each level carry ringed "lock target" sprites whose perimeter shows the required color; the level wins when every lock cell renders its required color. A horizontal step counter HUD bar drains 1 per click; running out loses the level. Pure-click game (`available_actions = [6]`); no movement, no undo.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click `(x, y)` in display pixels. The game's `step()` calls `camera.display_to_grid(x, y)` and then `level.get_sprite_at(...)` to find the clicked sprite. If the sprite is tagged `row_marker`, cycle that row's tint through `[2, 8, 11, 14]`. If `col_marker`, cycle that column's tint. Otherwise no-op. | Always. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 row-tint cycling. Each cell is painted by its row marker only (column markers absent). | Three lock targets in three distinct rows; click each row marker N times to land on its required tint. Witness: `[ACTION6@(4,20), ACTION6@(4,32)×2, ACTION6@(4,44)×3]` (6 actions). |
| 2 | M1 + M2 (column-tint cycling with last-click-wins). Both row and column markers present; each click repaints all cells in the affected row or column to the new tint. The cell's final color is whatever was painted most recently. | Five lock targets sharing rows or columns with conflicting required colors. The player must order the clicks so that each lock cell ends up painted by the right axis last. Witness: `[ACTION6@(4,20), ACTION6@(4,38)×3, ACTION6@(4,44)×3, ACTION6@(32,4)×2, ACTION6@(4,32)]` (10 actions). |
| 3 | Same M1 + M2 last-click-wins rule, more lock targets and tighter ordering. | Seven lock targets across rows/columns with multiple conflict pairs. One lock at cell (2, 3) requires the row click for that cell to be the LAST relevant click — forcing the player to paint a column for one constraint, then overwrite it with a row paint for the conflicting cell. Witness: `[ACTION6@(14,4)×3, ACTION6@(32,4)×2, ACTION6@(38,4)×3, ACTION6@(50,4)×2, ACTION6@(44,4), ACTION6@(20,4), ACTION6@(4,26)×3]` (15 actions). |

## Win condition

After every click that lands on a row or column marker: cycle that row/column's tint, repaint every cell in the affected row (or column) to the new tint, update each lock target's corner pixels (white if satisfied, required-color if not), then check whether every lock target's underlying cell renders its required color. If all satisfied, fire `self.next_level()`. After L3's locks are all satisfied, the engine fires `self.win()`.

## Lose condition

Step counter HUD `step_counter_hud` drains 1 per action; when `_action_count >= max_steps`, fire `self.lose()`. No other lose path. Per-level budgets: 30 / 60 / 80 (non-shrinking).

## Internal state

- `row_tints: list[int]` — current palette index for each of the 8 rows. Reset to `[BACKGROUND] * 8` per level.
- `col_tints: list[int]` — same for columns. Reset per level.
- `_cells_by_pos: dict[(gx, gy), Sprite]` — position-to-cell-sprite lookup, rebuilt in `on_set_level`.
- `step_counter_hud: StepCounterHud` — `RenderableUserDisplay` subclass tracking remaining clicks and rendering the bottom-row depleting bar.

## Notable code patterns

- **Tint cycling via index lookup**: `TINT_CYCLE.index(current)` then `(idx + 1) % 4`. Reusable for any "cycle a discrete value through a fixed alphabet" mechanic.
- **Last-click-wins via direct repaint**: rather than recomputing every cell from a combiner each step, the game just repaints the affected row (or column) immediately on the click. Cells "remember" their most recent paint by virtue of not being re-touched. Side benefit: the rendered cell color directly answers "which marker was clicked here last", which is what the player needs to reason about.
- **Lock target with required-color encoded in tag**: each lock sprite has a `req_<n>` tag (e.g. `req_8`, `req_11`, `req_14`); `_lock_required(lock)` extracts the integer. Lets one query loop handle all required-color values.
- **Lock target visual feedback via corner pixels**: `_render_lock_state()` flips the four corner pixels of each lock's perimeter ring between the required-color and white (palette 0) depending on satisfaction. Cheap visual cue without re-rendering the entire sprite.
- **Marker rendering via numpy slice**: `marker.pixels[1:5, 1:5] = tint` paints the 4×4 interior of a 6×6 sprite in one operation, leaving the 1-pixel frame intact.
- **No animation phases, no undo, no selection state**: the game is fully stateless between actions beyond `(row_tints, col_tints)` — every step recomputes cells from scratch. Keeps the implementation small (~390 lines including sprite art).
