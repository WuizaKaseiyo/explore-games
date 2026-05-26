# mr5q — polarity-attract-discharge

## Summary

The board hosts a small population of coloured "polarity orbs" — 9×9 sprites with a green or orange ring frame and an interior pattern that shows polarity (a yellow plus-cross interior = plus polarity; a single yellow horizontal bar interior = minus polarity). Two verbs only: ACTION6 (click on an orb to flip its polarity, plus↔minus) and ACTION5 (advance one global tick — every orb takes one cell step toward its nearest same-colour opposite-polarity neighbour, with walls blocking and polarity-gates blocking the wrong polarity). Two same-colour opposite-polarity orbs whose top-lefts are within Chebyshev distance ≤ orb size discharge, removing both. The level wins when the board is empty. Cross-colour orbs are mutually invisible — they neither attract nor discharge each other.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Advance one global tick: every alive orb computes its nearest same-colour opposite-polarity neighbour (Manhattan), takes one BFS-shortest-path step toward it (with dominant-axis-toward-target priority and wall/gate/occupant constraints), then any same-colour plus+minus pair within Chebyshev distance ≤ orb size discharges. | always |
| ACTION6 at (px, py) | Convert (px, py) display pixels to grid via `camera.display_to_grid`. If the cell is inside any active orb's 9×9 bbox, toggle that orb's polarity by swapping `InteractionMode.TANGIBLE` and `REMOVED` between its plus and minus variants. | always; clicks outside any orb are no-ops |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Click-to-flip + Attract-tick + Discharge-on-adjacency (the base dynamic system; 3 mechanics required by the witness). | 2 green-plus orbs on the same row, no walls. The player must flip one orb so the pair is opposite-polarity, then tick until they slide together and discharge. Witness ≈ `[ACTION6@orb_47_28, ACTION5 × ~14]` (1 click + ~14 ticks). |
| 2 | + Colour-keyed attract-and-discharge (NEW at L2: cross-colour orbs are mutually invisible for both attract and discharge). | 4 orbs in 2 colour groups (green pair on the upper row, orange pair on the lower row), all starting plus. Without colour-keying, every orb would lock onto its closest opposite-polarity neighbour regardless of colour and the cross-colour pairs would deadlock blocking each other; with colour-keying, each colour pair attracts independently. Witness ≈ `[ACTION6@green_47_12, ACTION6@orange_47_38, ACTION5 × ~14]`. |
| 3 | + Walls block movement (NEW at L3: walls are static obstacles that orbs route around — the attract-step's BFS automatically detours, but the player has to grant the orbs more time and read off the indirect path). | 4 orbs in 2 colour groups. The green pair on the upper row fuses directly. The orange pair on the lower row has a tall vertical wall pillar in the middle of the row, so each orange orb's attract-walk has to detour up-and-around the pillar (or down, depending on the BFS shortest path). Witness ≈ `[ACTION6@green_49_6, ACTION6@orange_51_36, ACTION5 × ~28]`. |

## Win condition

Active-orb count == 0 → `self.next_level()`. The active count starts at the number of orb instances and decrements every time a same-colour plus+minus pair discharges (both orbs marked `alive=False` and their `InteractionMode` set to `REMOVED`).

## Lose condition

`self._step_counter_value == 0` after any action → `self.lose()`. There is no instant-fail collision. There is no soft-lock state because ACTION6 is always available — flipping any orb changes its target set, so the world cannot get permanently stuck.

## Internal state

- `_orbs: list[dict]` — one entry per orb instance, each holding the `plus` and `minus` sprite variants (pre-placed at the same cell), the orb's `colour` (green/orange), the `active` polarity ("plus" or "minus"), and an `alive` flag.
- `_step_counter_value, _step_budget` — countdown to lose-on-budget.
- `_step_counter_ui` — `StepCounterHud` `RenderableUserDisplay` painting the depleting bar in row 0.
- `_wall_cells: set[tuple]` — grid cells covered by the union of all wall sprites' opaque pixels.

## Notable code patterns

- **Two-sprite swap idiom for polarity** (per universal-scaffold): each orb instance has both polarity variants pre-placed at the same grid coord; `flip` swaps `InteractionMode.TANGIBLE`/`REMOVED` between them. Clean visual + collision toggle.
- **Display-pixel-resolution rendering**: the playfield is the full 64×64 grid (no upscaling). Orbs are 9×9 sprites with internal multi-pixel structure (a 5-pixel plus-cross or a single 5-pixel horizontal bar) so the polarity reads off the rendered frame at native resolution and survives downsampling tests legibly damaged.
- **BFS attract step with dominant-axis-toward-target priority on the expansion order**: stable convergence behaviour when multiple shortest paths exist; the chosen first step prefers the dominant axis from source to target.
- **Chebyshev-distance discharge predicate**: `max(|ax - bx|, |ay - by|) ≤ ORB_SIZE` covers both bbox-edge-touching and corner-touching for sized sprites; the walkable rule prevents bbox overlap during movement, so this predicate effectively fires on edge/corner contact only.
- **Two-pass move resolution** (compute desires → drop conflicts where two orbs target the same destination → commit moves) for deterministic concurrent-pursuit behaviour.
