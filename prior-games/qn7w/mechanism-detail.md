# qn7w — pulse-chain-eject

## Summary
The player clicks a pusher knob at one end of a stationary chain of touching coloured balls; the pusher fires a single momentum pulse that propagates through the chain. **Intermediate balls do not move** — only the chain's far-end ball ejects, travelling exactly one ball-width along the chain's terminal axis. The ejected ball lands on the immediately adjacent cell, where it may fill a colour-matched target socket, deposit on a merge pad, or be consumed by a wall. The level wins when every target socket is filled and every merge pad has received its required two deposits; the level loses if the step budget runs out. The defining property — energy concentrates at the chain terminus rather than distributing through the cascade — is the inverse of cascade-style mechanics like domino topple or sandpile overflow.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click. If on a `pusher_knob`: fire a pulse along its attached chain — eject the active branch's terminal ball by one ball-width along the branch's axis. If on a `junction_node`: cycle the junction's active branch (binary, e.g. up ↔ down). Other clicks: no-op. | `_get_valid_actions()` enumerates only the centres of `pusher_knob` and `junction_node` sprites in the current level (~1 to 4 valid clicks per level). |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | `pulse-eject` (base dynamic system) | Tutorial: one horizontal 4-ball chain, one pusher, one matching socket adjacent to the chain's right terminus. Witness: `[ACTION6@(11, 33)]`. The single click ejects the terminal ball into the socket. |
| 2 | + `junction-routing` (composes pulse-eject) | Stem leads to a T-junction with two branches — up-branch terminates at the only target socket (blue), down-branch (default active) terminates at a `dead_end_wall` that consumes ejects. The junction's green tab indicates which branch is currently active; clicking the junction toggles the tab between top/bottom halves. Witness: `[ACTION6@(31, 33), ACTION6@(7, 33)]` — flip the junction to up, then push. |
| 3 | + `merge-on-coincidence` (composes both prior) | Two chains converge orthogonally on a single `merge_pad`: chain A (blue, lower half) has a vertical up-branch ending one ball-width below the pad; chain B (yellow, upper half) has a horizontal left-branch ending one ball-width to the right of the pad. Both junctions default to "down", routing to dead_end_walls; both must be flipped before firing. The merge_pad accepts deposits from any colour and lights up white only after receiving two. Witness: `[ACTION6@(23, 49), ACTION6@(5, 49), ACTION6@(41, 25), ACTION6@(59, 25)]` — flip A, push A (deposit 1), flip B, push B (deposit 2 → win). |

## Win condition

After every action, `_check_win()` walks every `target_socket` sprite in the level and confirms its centre pixel `[2, 2]` is non-transparent (i.e. filled), then walks every `merge_pad` sprite and confirms its deposit count is ≥ 2. If both predicates hold, `next_level()` is called.

## Lose condition

`self._action_count >= step_budget` (the per-level value from `Level.data["step_budget"]`: 6 / 16 / 30 for L1/L2/L3) → `self.lose()`. There is no instant-fail collision and no enemy. The only loss mode is budget exhaustion.

## Internal state

- `self._chains: list[dict]` — per-chain runtime model deep-copied from `Level.data["chains"]` in `on_set_level`. Each entry holds: pusher position, stem ball positions, junction position (or `None`), branches (each with a list of ball positions and an axis vector), `active_branch` name (mutated by junction clicks), and stem_axis / chain axis vectors.
- `self._merge_pad_deposits: dict[(int, int), int]` — tracks deposit count per merge_pad position; mutated when an eject lands on a pad.
- `self._step_counter_ui: StepCounterHud` — RUD subclass; depleting bar on row 63.
- Per-level visual mutations live on the sprite pixels themselves: junctions repainted by `_junction_pixels(active_branch)`; sockets switched between empty / filled patterns; merge_pads switched between empty / half-filled / fully-lit.

## Notable code patterns

- **Position-matched sprite lookup helper.** `Level.get_sprite_at(x, y, tag=...)` requires a non-transparent pixel under (x, y); sprites with rounded silhouettes (`-1` corners) cannot be located by their top-left position via this method. The fix is `_sprite_at_position(x, y, tag)` that iterates `level.get_sprites_by_tag(tag)` and matches `.x, .y` directly. Used for terminal-ball lookup in `_fire_pulse` and target-socket / merge-pad lookup in `_process_eject`.
- **State-as-pixels rendering, not separate sprite swaps.** Each junction, target_socket, and merge_pad has a *single* sprite whose `.pixels` array is mutated to reflect runtime state (active branch direction; filled/empty; 0/1/2 deposits). Module-level helper functions (`_empty_socket_pixels`, `_filled_socket_pixels`, `_junction_pixels`, `_half_merge_pad_pixels`, `_full_merge_pad_pixels`) construct each variant. This keeps sprite count constant and makes the state visually obvious.
- **Branch-axis vectors stored alongside ball lists.** Each branch's data is `{"balls": [(x, y), ...], "axis": (dx, dy)}`. The eject direction comes from the branch's axis, computed once at level build time. Generalises trivially to chains in any cardinal direction.
- **Restricted-action enumeration via `_get_valid_actions`.** Only pusher and junction sprite centres appear as valid ACTION6 candidates, so the agent does not waste budget exploring the empty 64×64 click-space. Reference precedent: r11l, su15.
- **Camera viewport defensively resized in `on_set_level`.** All three levels are 64×64 (no resize strictly needed) but `self.camera.width / .height` are written anyway, future-proofing the code if a level adopts a different grid size.
