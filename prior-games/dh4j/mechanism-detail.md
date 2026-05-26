# dh4j — tile-coded-stride

## Summary

A single magenta avatar leaps across an 8-col × 7-row cell grid where every walkable cell carries a visible 1/2/3-pip stride encoding. Pressing a cardinal arrow translates the avatar by exactly that pip count in the pressed direction; intermediate cells are fly-over (the leap crosses walls), and only the destination must be in-bounds and non-wall — otherwise the press is a no-op. Wall barriers across the playfield force the player to use multi-cell leaps. A *switch button* (visibly raised, distinct from any floor cell) toggles every pip-2 and pip-3 floor cell in place — the pip patterns themselves visibly transform (a 2-pip cell sprouts a third pip, and vice versa), directly tying the visual cue to the stride change. A *pivot* cell visibly carries one extra maroon "bonus pip" alongside its stride pips; on landing the maroon pip transfers to the avatar (rendered as a maroon corner dot on the avatar) for a one-shot +1 stride on the next press; on consumption the maroon pip vanishes from both. The level wins when the avatar reaches the goal cell; the level loses when the step budget exhausts. Levels compose by stacking wall barriers (1-row → 2-row → 3-row) so each level requires one more stride source than the previous.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | UP leap: translate avatar by `(0, -N)` cells where `N = origin_cell_pip_count + pending_bonus`; destination must be non-wall and in-bounds. | always |
| ACTION2 | DOWN leap: same as UP but `(0, +N)`. | always |
| ACTION3 | LEFT leap: same but `(-N, 0)`. | always |
| ACTION4 | RIGHT leap: same but `(+N, 0)`. | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | cell-pip-stride-leap; goal-overlap-wins | Avatar starts at (0, 4) — top-left of the bottom half; the stride-3 cell at (3, 4) is 3 cells away. The goal at (7, 0) is in the top-right corner so the player must leap up then walk across the top half. One-row wall barrier at y=3. Witness `[R, R, R, U, R, R, R, R, U]` (9 actions). |
| 2 | + switch-button-swaps-pip-counts | Two-row wall barrier at y=2..3. The leap cell at (3, 4) is a 2-pip cell (stride-2 → wall hit). The visibly-raised orange/maroon switch button at (5, 4) toggles every pip-2↔pip-3 floor cell in place — the player sees the cells' pip patterns physically transform. Walk RIGHT × 4 (lands on switch via stride-2 leap from the 2-pip cell), LEFT × 2 back to the now-3-pip leap cell, UP-leap to (3, 1), then RIGHT × 4 + UP to the top-right corner goal. Witness `[R, R, R, R, L, L, U, R, R, R, R, U]` (12 actions). |
| 3 | + pivot-bonus-pip-pickup (one-shot) | Three-row wall barrier at y=2..4. The pivot at (3, 5) visibly carries 2 stride pips PLUS one maroon bonus pip. The switch at (5, 6) is positioned BELOW the pivot row so the player must detour. Stride-4 is required to clear 3 walls; achievable only as pip-3 (after switch) + bonus pip (from pivot). After the leap to (3, 1), walk RIGHT × 4 + UP to the top-right corner goal at (7, 0). Witness `[D, R, R, R, R, R, U, L, L, U, R, R, R, R, U]` (15 actions). |

## Win condition

When the avatar's grid-cell position overlaps the `goal_cell`'s position (cell-aligned), `self.next_level()` fires. The check runs after every animation frame of a slide and at the final destination, so reaching the goal mid-slide ends the slide early and advances. After L3 wins, the engine auto-fires `self.win()`.

## Lose condition

`self.lose()` fires when `self._action_count > self._max_steps` (the level's `step_budget`). No instant-fail, no hazards, no respawn lives.

## Internal state

- `_pending_bonus` — `int` (0 or 1); set to 1 when the avatar lands on a pivot, consumed on the next press.
- `_armed_pivot` — Sprite or None; the specific pivot cell that armed the bonus; consumed (maroon bonus pip removed, `"pivot"` tag dropped) when the bonus is consumed.
- `_slide_remaining`, `_slide_dx`, `_slide_dy` — multi-frame slide animation phase machine; while `_slide_remaining > 0`, each `step()` advances the avatar one cell along `(dx, dy)` and decrements.
- `_max_steps` — per-level step budget (30 / 50 / 80 for L1 / L2 / L3).
- Engine's built-in `_action_count` is the step counter (one per `perform_action` call).

## Notable code patterns

- **Direct pip-count swap (no legend abstraction)**: the switch's effect is implemented by overwriting each pip-2/pip-3 floor sprite's pixel matrix with the matching `_floor_pip_{2,3}()` (or `_pivot_pip_{2,3}()` for the pivot composite) and swapping its tag. The pip count visibly changes — no color-coded legend layer required to communicate the mechanic.
- **Layout-string maps**: each level's layout is authored as a list of 7 strings of 8 chars (`'.'` = pip-1, `'2'` = pip-2, `'3'` = pip-3, `'W'` = wall, `'G'` = goal, `'S'` = switch button, `'P'` = pivot composite, `'A'` = avatar start). `_build_level_sprites` interprets the chars and emits placed `Sprite` instances.
- **Phase-tick slide animation**: `step()` short-circuits with `_slide_remaining > 0` to advance one cell per engine frame; only calls `complete_action()` when the slide finishes or the goal is reached mid-slide.
- **In-place pixel mutation for avatar bonus marker**: rather than swapping between two avatar sprites, the maroon 2×2 corner accent at pixels `(1..2, 5..6)` is painted on (color 13) or cleared (color 6) directly. The maroon color matches the bonus pip's color on the pivot cell — visually the bonus pip "moves" from cell to avatar.
- **Tag-based cell type lookup**: `_cell_at(x, y)` finds the topmost gameplay sprite by checking the `"switch"`, `"goal"`, and `"floor"` tag groups in order; `_stride_for_cell(cell)` reads `pip_1` / `pip_2` / `pip_3` tags. No legend transform needed.
