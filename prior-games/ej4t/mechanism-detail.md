# ej4t — radius-scope-influence

## Summary

The player avatar is surrounded by a visible translucent Manhattan-distance ring of radius R, painted as a halo over every cell within R cells of the player. The player walks the four cardinal directions; walking into a crate triggers a push, and chain-pushes (crate → crate) only commit when every crate in the chain (after the first) sits within R of the player's current cell. The level wins when every target sprite is covered by a crate. Two collectibles modify R as the player walks over them: extender pickups grow R by 1 (one-shot), and shrinker traps reduce R by 1 (one-shot, the trap stays visible as a "spent" grey cell). The player loses when the per-level step budget is exhausted.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | walk player up; if dest cell has a crate, attempt push | always valid |
| ACTION2 | walk player down; same push semantics | always valid |
| ACTION3 | walk player left; same push semantics | always valid |
| ACTION4 | walk player right; same push semantics | always valid |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1: chain-push gated by Manhattan ring (R=2). Two crates in a row-6 corridor; player must walk close enough that crate2 is within R when chain-pushing. | Witness `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]` (5 actions; player walks 4 east then chain-pushes both crates onto the target at (10, 6)). |
| 2 | M1 carried forward + M2: extender pickup grows R by +1. Player starts with R=1; without picking up the extender at (5, 7), chain push fails (chain length 2 needs R≥2). | Witness `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]` (5 actions; pickup auto-collected at step 2; then chain push). |
| 3 | M1 + M2 carried forward + M3: shrinker trap reduces R by 1. Two extenders + one shrinker on the only path; chain length 3 needs R=3, requires both extenders to net +1 after the trap. | Witness `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]` (7 actions; visits ext_a → trap → ext_b → push position → chain push 3 crates). |

## Win condition

Every `target` sprite's `(x, y)` is occupied by a `crate` sprite. Checked after every action via `_check_win()` calling `target_positions.issubset(crate_positions)`.

## Lose condition

`self._steps_used >= self._max_steps`. Per-level budgets: L1=25, L2=30, L3=35 (increasing, never shrinking, all generously over the witness).

## Internal state

- `self._R: int` — current Manhattan ring radius. Initialised per level via `_current_level_index` lookup (L1=2, L2=1, L3=2). Mutated by `_consume_pickups_at_player`.
- `self._steps_used: int` — private step counter, incremented inside successfully-handled action branches. Distinct from engine's `self._action_count` to avoid the RESET-counts-as-step bug.
- `self._max_steps: int` — per-level budget set in `on_set_level`.
- `self._step_counter_hud: StepCounterHud` — bottom-row depleting bar.
- `self._ring_hud: RingOverlayHud` — translucent halo painter, re-renders each tick using current player position + R.

## Notable code patterns

- **Chain-push atomic commit**: `_attempt_push_chain` builds the full chain by walking consecutive crate cells in the direction of movement, then validates ALL crate-crate links (crates 1..N) against the radius gate before committing any movement. If any link is out of range or the destination is blocked, the entire push is rejected — no partial state mutation.
- **Pickup consumption via `InteractionMode.REMOVED`**: extender / shrinker sprites stay in the level's sprite list but are switched to `REMOVED` mode after consumption. Cleaner than `set_visible(False)` because collision is also gated; cleaner than deleting from the list because the engine's per-level reset logic stays intact across attempts.
- **Ring overlay as HUD widget, not as dynamic sprite pool**: `RingOverlayHud` extends `RenderableUserDisplay` and computes ring cells from player position + R each frame, drawing a 1-pixel-thick translucent border on every in-ring cell. Avoids the complexity of managing a dynamic sprite pool with `set_position` / `InteractionMode` toggles per cell.
- **Per-level params via `_current_level_index` instead of `level.get_data`**: simpler than threading `level_data` through; the three levels' parameters are fixed and inline-readable in `on_set_level`.
- **Sprite-anchor coordinates**: walls/crates/targets are placed at integer (x, y) cell coordinates; their pixel patterns (4×4 / 4×4 / 3×3) overflow into adjacent cells visually but the collision and push logic checks only the top-left anchor cell. Acceptable for 12×12 / 14×14 / 16×16 grids where overflow doesn't reach grid boundaries given placement.
