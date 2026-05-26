# pf3w — wavefront-converge-timing

## Summary

The player has no avatar. The chamber pre-places several "emitter slot" sprites (visually inactive grey hollow crosses) and "target receiver" sprites (hollow colored rings). The two verbs are `ACTION6` (click an inactive slot to activate it as a colored pulse-emitter) and `ACTION5` (advance a global tick counter by 1). Each activated emitter's wavefront expands outward by one logical-cell of BFS distance per global tick, rendered as a colored 1-cell-thick halo trail that visibly curves around walls. A target lights (its hollow ring center fills with yellow) on the *single* tick when a same-colored frontier cell coincides with the target's center. The level wins when every target is simultaneously lit on the same tick — solving the puzzle requires choosing *when* to activate each emitter so multiple wavefronts converge on multiple receivers at the same global tick. The step counter is the only failure mode.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Advance the global tick counter by 1; recompute every active emitter's wavefront frontier; recompute every target's lit state. | always (until step budget exhausts) |
| ACTION6 | Click at (x, y) to activate the inactive slot whose 3×3 logical-cell footprint covers the click position; the slot's color (blue or magenta) is determined by the slot's pre-placed color tag. | only on cells holding an `emitter_slot_dim_*` sprite |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 — Click-place emitter + tick to deliver wavefront. Single emitter, single same-colored target. | Player learns the click + tick verb by activating the only slot (the click lights only the slot's yellow center; the FIRST `ACTION5` produces the first visible Manhattan-2 ring outside the slot's arms — `VISIBLE_RADIUS_OFFSET=1` keeps radius 1 hidden under the slot for clean discovery) and pressing ACTION5 until the wavefront's frontier reaches the target. Witness: `[ACTION6@(13,33), ACTION5×8]` (9 actions). |
| 2 | M2 — Inter-emitter timing offset for simultaneous arrival. Two emitters (same color) and two targets at distinct BFS distances; the player must stagger ACTION6 placements so both wavefronts arrive at their targets on the same global tick. | Plausible-but-wrong post-discovery alternative: activate both slots simultaneously — wavefronts then arrive at different ticks (target_A at radius 9, target_B at radius 7) and the win-check never fires. Witness: `[ACTION6@(13,17), ACTION5×2, ACTION6@(13,49), ACTION5×6]` (10 actions). |
| 3 | M3a — Wall-routed BFS distance: a wall column with a single-row gap forces the wavefront to curve through the gap, making BFS distance differ from Manhattan distance. M3b — Color-keyed targets: each target lights only via a same-colored wavefront, ruling out cross-color synchronization. | The witness exercises both new mechanics: BFS distances of 22 (slot_blue → target_blue) and 20 (slot_magenta → target_magenta) require stagger 2 (slot_blue first); cross-color routing is closed by M3b enforcement. Trivial post-discovery heuristic that fails: "activate both slots at the same tick" — wavefronts hit at radii 22 and 20, never together. Witness: `[ACTION6@(9,9), ACTION5×2, ACTION6@(17,53), ACTION5×19]` (23 actions). |

## Win condition

After every step (whether the action was ACTION5 or ACTION6), the game checks every target sprite's center logical cell against the union of same-color wavefront frontiers. If every target's center is on a same-color frontier on this tick, `self.next_level()` fires.

## Lose condition

The engine's `_action_count` reaches `level.get_data("step_budget")` (30 for L1, 35 for L2, 70 for L3) — `self.lose()` fires.

## Internal state

- `_global_tick: int` — incremented by ACTION5; used as the temporal coordinate for wavefront radius math.
- `_active_emitters: list[dict]` — each entry carries the emitter sprite reference, its color, its `T_activated` snapshot of `_global_tick`, its center logical-cell coords, and a precomputed BFS distance grid from its center.
- `_walkable: np.ndarray (16, 16) bool` — built per-level from wall-tagged sprites; True where the wavefront can reach.
- `_wavefront_blue_sprite`, `_wavefront_magenta_sprite` — global per-color sprites covering the entire 64×64 frame; their pixel matrices are recomputed each step to render the current frontier set.
- `_max_steps: int` — read from `level.get_data("step_budget")` per level.
- `_step_counter_hud: StepCounterHud` — depleting bar at row 0.

## Notable code patterns

- **Logical-cell-over-pixel-grid pattern.** The level's `grid_size=(64, 64)` matches the engine's default camera, so no per-level camera resize is needed; the game treats every 4×4 pixel block as a "logical cell" and operates BFS, slot footprint detection, and target lit-state checks at logical-cell granularity (16×16 logical grid). Sprite pixel arrays use sub-cell pattern (hollow-frame-per-cell, filled-frame-per-cell, 4×4 wall checker) so the rendering visibly damages on 2:1 downsampling per `checklist.md` item 20.
- **BFS-distance precomputation per active emitter.** When `ACTION6` activates a slot, the game runs a single 4-connected BFS from the slot's center logical cell over the static walkable mask and caches the distance grid in the emitter's record. Per-step frontier computation is then O(grid) per emitter via `mask = (distance_grid == current_radius)`.
- **Wavefront sprite as live overlay.** Two persistent, layer-1 sprites (`wavefront_blue` and `wavefront_magenta`) cover the full 64×64 grid; each step the game class clears their pixels and repaints the union of all same-color frontier cells using a hollow-frame-per-cell sub-cell pattern. No per-emitter per-tick sprite spawning — one sprite per color, mutated in place.
- **Two-state target rendering via in-place pixel mutation.** Each `target_*` sprite has its 4×4 center cell pixels set to either fully-transparent (unlit) or filled-yellow-with-dark-inner (lit) per step, based on whether the target's center logical cell coincides with a same-color frontier this tick. No two-sprite-swap; the same sprite instance toggles.
- **Click-to-logical-cell with slot-footprint hit-test.** ACTION6 click coords pass through `camera.display_to_grid` (returns pixel-grid coords; with `grid_size=(64, 64)` and default camera, this is identity), then are converted to logical-cell coords via `// 4`. The hit-test iterates `slot_dim`-tagged sprites and checks the click logical-cell is inside the slot's 3×3-cell bounding box (any click within the slot footprint counts, not just the center).
- **`available_actions=[5, 6]` minimal action enumeration.** No avatar, no individual sprite to nudge → no cardinal motion (1-4) and no undo (7). The `_get_valid_actions` override returns one ACTION5 plus one ACTION6 per remaining dim slot at its center pixel coordinate, giving any agent (including text-only LLM agents) a pre-enumerated candidate set without having to compute slot positions themselves.
