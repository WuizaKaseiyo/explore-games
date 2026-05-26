# gg11 — tide-current-drift

## Summary

A global current direction is set by the arrow keys (ACTION1=N,
ACTION2=S, ACTION3=W, ACTION4=E). ACTION5 advances the simulation by
one tick: every non-anchored coloured pawn moves exactly one cell in
the current direction, blocked by walls, grid edges, anchored pawns
(treated as walls), and other unanchored pawns ahead of them. ACTION6
clicks a pawn to toggle its anchor — anchored pawns ignore drift but
still block. The level wins when every pawn occupies its same-coloured
target.

## Action mapping

| Action | Semantic | Gate / when valid |
|---|---|---|
| ACTION1 | Set the global current direction to North; pawns do not move. | always; consumes 1 step |
| ACTION2 | Set current direction to South. | always; 1 step |
| ACTION3 | Set current direction to West. | always; 1 step |
| ACTION4 | Set current direction to East. | always; 1 step |
| ACTION5 | Tick: every non-anchored pawn drifts 1 cell in the current direction subject to walls / bounds / pawn collision. | always; 1 step |
| ACTION6 | Click a pawn cell to toggle its anchor (skipped on sticky-locked pawns). | click on empty / wall / sticky pawn = no-op (no step) |

## Per-level mechanic progression

| Level | Mechanic introduced | Specific challenge / constraint |
|---|---|---|
| 1 | Set-direction (ACTION1-4), drift tick (ACTION5), pawn-pawn collision, click anchor (ACTION6). | Two paired pawns must drift east through staggered wall baffles. The extra baffles block the old straight detour and require a small shared vertical correction before both pawns can align with their exits. |
| 2 | Sticky targets: once a pawn lands on its own target it auto-anchors irreversibly. | Two pawns start on the same upper row and must route around a central block plus an added asymmetric baffle in red's lane. The shortest route now needs an early vertical adjustment; focusing on only one pawn wastes too much budget. |
| 3 | Wall + multi-pawn sticky orchestration. | Three pawns still share the same global current, with an extra wall on the middle pawn's route. The player must take a longer shared detour that keeps all three lanes coordinated. |

## Win condition

After every effective action, walk every pawn. If each pawn's position
equals its same-colour target, fire `self.next_level()`. After level 3,
the engine auto-fires `self.win()`.

## Lose condition

Effective actions decrement the step bar. If it reaches zero before the
win predicate holds, `self.lose()` fires. Misclicks (on empty cells,
walls, or sticky-locked pawns) are free no-ops.

## Internal state

- `self.pawns`: list of `Pawn` records (name, pos, target, anchored,
  sticky).
- `self.current_dir`: one of N/S/W/E unit vectors.
- `self.walls`: set of wall cells (block both pawn types).
- `self.steps_left` / `self.max_steps`: visible step budget.

## Notable code patterns

- The `_drift_tick` sorts pawns by their position component along the
  current direction so the *leading* pawn moves first, preventing
  push-through collisions.
- Targets are rendered as a single coloured cell at a layer below the
  pawn body, so an arriving pawn cleanly occludes its target.
- Anchored pawns are visualised by a status-row pip rather than
  inline, keeping the grid sprites uncluttered: the bottom rim shows
  one cell per pawn, lit dark-grey when locked and the pawn's own
  colour when free.
- The direction indicator on the bottom rim lights one of four cells
  (N/S/W/E) yellow, so the active drift direction is always visible
  before the player commits a tick.
