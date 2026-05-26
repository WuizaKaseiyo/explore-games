# mz6t — majority-vote-stabilize

## Summary

The player faces a 5×5 grid of small cells, each in one of three colour states (light-blue solid disc / orange hollow ring / pink plus-sign), plus a half-scale target panel on the right edge of the frame showing the desired final configuration. The only verbs are ACTION6 (click a cell to advance its state by `+1 mod 3`) and ACTION5 (tick — apply majority-vote propagation to every voting cell simultaneously). Walls (rendered as maroon woven blocks) appear from L2; they don't vote and aren't voted on, reducing the voter count of adjacent cells. Anchor cells (rendered with corner pips) appear at L3; they freeze permanently the first time their colour state matches a per-cell target, after which they keep voting but no longer get voted on. The win check fires only on ACTION5; the lose check fires when the per-level step budget exhausts.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Tick: apply synchronous majority-vote propagation across all voting cells (excluding walls and locked anchors). For each cell, count colour states among its non-wall, in-grid cardinal neighbours; if any colour `C` has `count(C) ≥ 3`, the cell adopts `C`; otherwise the cell keeps its current state. Walls don't change. The win check fires immediately after this update. | Always. The win check fires *only* in this branch. |
| ACTION6 | Click: read `data["x"], data["y"]`, convert to grid cell `(col, row)`. If the cell is a normal voter or an unlocked anchor, advance its state by `+1 mod 3` and check anchor lock. If the cell is a wall or a locked anchor, click is a no-op (still consumes a step). | Always; per-cell gating instead of per-action gating. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 (click cycles state) + M2 (tick applies majority-vote propagation; win check fires only on ACTION5) — base dynamic system | 5×5 grid; initial layout is a 3×3 hollow-square of orange around a lb centre, with one corner of the inner block also lb. Player must click the off-corner `(1,1)` to orange and tick; the centre `(2,2)` flips orange via tick (4 of 4 neighbours orange). Witness `[ACTION6@(14,14), ACTION5]` (2 actions). Step budget 25. |
| 2 | + M3 (walls don't vote and aren't voted on) | Walls at the 4 inner-corner cells `(1,1), (3,1), (1,3), (3,3)`; the initial-row-2 orange line is *protected* by these walls — without them, tick would out-vote the line back to lb. The diff cells `(2,0), (0,2), (4,2), (2,4)` each have a wall as one neighbour, reducing voter count to ≤3 and forbidding any tick-flip; they must be clicked. Witness `[ACTION6@(22,6), ACTION6@(6,22), ACTION6@(38,22), ACTION6@(22,38), ACTION5]` (5 actions). Step budget 30. |
| 3 | + M4 (anchor freeze on first target match) | Same wall layout as L2 plus an anchor at `(2,2)` whose target is state-2 (pink). Player must click the anchor twice to advance it lb → orange → pink (matches target on the second click → lock); then click the 4 ring-of-orange diff cells `(0,2), (4,2), (2,1), (2,3)` and tick. Without the freeze, the final tick would flip the pink anchor to orange (4 orange neighbours) and the level would lose its centre colour. Witness `[ACTION6@(22,22), ACTION6@(22,22), ACTION6@(6,22), ACTION6@(38,22), ACTION6@(22,14), ACTION6@(22,30), ACTION5]` (7 actions). Step budget 35. |

## Win condition

Every non-wall cell's current state equals its per-cell target state. Anchor target colours are looked up in the level's `anchors` dict. Walls are accepted as walls. The check runs after every ACTION5; clicks alone never advance the level.

## Lose condition

`self._steps_used >= self._max_steps` where `self._steps_used` increments once per non-out-of-bounds action (clicks on walls and locked anchors still consume a step; clicks outside the playfield consume nothing).

## Internal state

- `_cell_sprite[(col, row)] -> Sprite` — handle to the placed sprite per cell, used for pixel-mutation when state changes.
- `_cell_state[(col, row)] -> int 0/1/2` — current colour state of voting cells; absent for walls.
- `_is_wall: set[(col, row)]` — wall positions (immutable).
- `_is_anchor: set[(col, row)]` — anchor positions.
- `_anchor_target[(col, row)] -> int 0/1/2` — per-cell target colour for anchors (used by both `_check_anchor_lock` and `_check_win`).
- `_anchor_locked: set[(col, row)]` — anchors that have already matched their target and are now permanently fixed.
- `_target_state[(col, row)] -> int 0/1/2` — per-cell target colour for non-wall cells (anchors contribute via `_anchor_target`, normal voters via the level's `target` array).
- `_steps_used` (private), `_max_steps` — step-budget tracking; private to avoid the engine's `_action_count` first-frame-loss bug noted in `code/smoke-test-checks.md`.

## Notable code patterns

- **Synchronous tick via two-pass dict snapshot**: `_apply_tick` reads `old_state = dict(self._cell_state)`, computes a new map by inspecting neighbour counts in `old_state`, then commits in a separate loop. This avoids cascade artefacts from in-place updates and matches the semantics of CA majority rules.
- **Per-state pixel template tables**: `_VOTE_NP[state]`, `_ANCHOR_ARMED_NP[state]`, `_ANCHOR_LOCKED_NP[state]` are pre-built numpy arrays so each `_update_cell_visual` is a `sprite.pixels = arr.copy()` rather than a fresh `np.array(list)` call.
- **HUD-only target panel**: instead of placing 25 mini-sprites per level for the target panel, a single `TargetPanelHud` (RenderableUserDisplay) reads from level-data and paints the panel cells directly into the camera's frame each render. Saves 75 sprites across 3 levels and keeps `level.get_sprites()` focused on the playfield.
- **Anchor armed→locked corner-pip swap**: anchors share the same colour-state cycle as voting cells but the 4 outer corner pixels carry a "lock indicator" (palette `5` armed → palette `14` locked). The pixel arrays differ only in those 4 corner cells, so the swap is one `sprite.pixels = arr.copy()` per state change.
- **Engine-side win-only-on-tick gate**: `step()` runs the win predicate inside `if self.action.id == GameAction.ACTION5 and self._check_win()`. This is what makes M2 (tick) strictly necessary — click-only sequences cannot win, regardless of whether they compose the target state, because the engine never inspects the win predicate after a click.
